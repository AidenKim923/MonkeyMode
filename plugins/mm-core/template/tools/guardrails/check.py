#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""MonkeyMode guardrail checker: no-comment rule and banned API/pattern rules.

Runs every profile in guardrails/*.json (any JSON file with a "rules" array). Prints one line
per violation to stderr and exits 1 when anything is found, 0 otherwise.

    uv run tools/guardrails/check.py --all
    uv run tools/guardrails/check.py --staged
    uv run tools/guardrails/check.py path/to/File.cs [...]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True

CONFIG_DIR = Path("guardrails")
DEFAULT_EXCLUDE_DIRS = [".git", "node_modules", "Library", "Temp", "obj", "target", "ThirdParty"]
NO_COMMENT_MESSAGE = (
    "Comments are not allowed. Fix the reason you wanted one: (1) make the intent visible "
    "through names and smaller methods, or (2) enforce the constraint mechanically with types, "
    "module references, an analyzer or a guardrail rule. See docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md"
)


@dataclass
class Stripped:
    code: str
    comment_lines: list[int] = field(default_factory=list)


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    while True:
        if (current / CONFIG_DIR).is_dir() or (current / ".git").exists():
            return current
        if current.parent == current:
            return start.resolve()
        current = current.parent


def strip_c_like(text: str) -> Stripped:
    """Blank out string/char literals and comments, keeping line structure.

    Handles C# regular, verbatim (@""), interpolated ($"") and raw (\"\"\"...\"\"\")
    strings. Nested quotes inside interpolation holes are a known blind spot.
    """
    n = len(text)
    out: list[str] = []
    comments: list[int] = []
    line = 1
    i = 0
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if c == "\n":
            out.append(c)
            line += 1
            i += 1
            continue

        if c == "/" and nxt == "/":
            comments.append(line)
            while i < n and text[i] != "\n":
                i += 1
            continue

        if c == "/" and nxt == "*":
            comments.append(line)
            i += 2
            while i < n and not (text[i] == "*" and i + 1 < n and text[i + 1] == "/"):
                if text[i] == "\n":
                    out.append("\n")
                    line += 1
                i += 1
            i += 2
            continue

        verbatim = False
        j = i
        while j < n and text[j] in "$@":
            if text[j] == "@":
                verbatim = True
            j += 1
        if j < n and text[j] == '"':
            quotes = 0
            k = j
            while k < n and text[k] == '"':
                quotes += 1
                k += 1
            out.append('""')
            if quotes >= 3:
                closer = '"' * quotes
                end = text.find(closer, k)
                if end < 0:
                    end = n - quotes
                for m in range(k, end):
                    if text[m] == "\n":
                        out.append("\n")
                        line += 1
                i = end + quotes
                continue
            i = j + 1
            while i < n:
                ch = text[i]
                if ch == "\n":
                    out.append("\n")
                    line += 1
                if verbatim:
                    if ch == '"':
                        if i + 1 < n and text[i + 1] == '"':
                            i += 2
                            continue
                        break
                else:
                    if ch == "\\":
                        i += 2
                        continue
                    if ch == '"':
                        break
                i += 1
            i += 1
            continue

        if c == "'":
            out.append("''")
            i += 1
            while i < n and text[i] != "'":
                if text[i] == "\\":
                    i += 1
                i += 1
            i += 1
            continue

        out.append(c)
        i += 1
    return Stripped("".join(out), comments)


def load_profiles(root: Path) -> list[dict]:
    """Every guardrails/*.json with a "rules" array is a profile."""
    folder = root / CONFIG_DIR
    profiles = []
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        config = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(config.get("rules"), list):
            continue
        config["_name"] = path.stem
        config.setdefault("scopeRoot", "")
        config.setdefault("extensions", [".cs"])
        config.setdefault("noComments", False)
        config.setdefault("excludeDirs", DEFAULT_EXCLUDE_DIRS)
        config.setdefault("skipFileSuffixes", [])
        config.setdefault("skipHeaderMarkers", ["<auto-generated"])
        config["_compiled"] = [(rule, re.compile(rule["pattern"])) for rule in config["rules"]]
        profiles.append(config)
    if not profiles:
        raise FileNotFoundError(f"No guardrail profiles in {folder}. Run mm-setup or add guardrails/<name>.json.")
    return profiles


def in_scope(rel: str, config: dict) -> bool:
    scope = config["scopeRoot"].strip("/")
    rel = rel.replace("\\", "/")
    if scope and not (rel.startswith(scope + "/") or f"/{scope}/" in f"/{rel}"):
        return False
    exts = config["extensions"]
    if exts != ["*"] and not any(rel.endswith(ext) for ext in exts):
        return False
    if any(rel.endswith(suffix) for suffix in config["skipFileSuffixes"]):
        return False
    parts = set(rel.split("/")[:-1])
    return not parts.intersection(config["excludeDirs"])


def collect(root: Path, config: dict, paths: list[str], staged: bool) -> list[Path]:
    if staged:
        result = subprocess.run(
            ["git", "-C", str(root), "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=False,
        )
        candidates = [root / p for p in result.stdout.splitlines() if p]
    elif paths:
        candidates = []
        for p in paths:
            full = Path(p) if Path(p).is_absolute() else root / p
            candidates.extend(sorted(full.rglob("*")) if full.is_dir() else [full])
    else:
        start = root / config["scopeRoot"] if config["scopeRoot"] else root
        excluded = set(config["excludeDirs"])
        candidates = []
        for dirpath, dirnames, filenames in os.walk(start):
            dirnames[:] = [d for d in dirnames if d not in excluded]
            candidates.extend(Path(dirpath) / name for name in filenames)
        candidates.sort()
    files = []
    for path in candidates:
        if not path.is_file():
            continue
        try:
            rel = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
        if in_scope(rel, config):
            files.append(path)
    return files


def check_file(path: Path, root: Path, config: dict) -> list[str]:
    rel = path.resolve().relative_to(root.resolve()).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    head = "\n".join(text.split("\n")[:5])
    if any(marker in head for marker in config["skipHeaderMarkers"]):
        return []
    stripped = strip_c_like(text) if config.get("stripLiterals", True) else Stripped(text, [])
    found = []
    if config["noComments"]:
        for ln in sorted(set(stripped.comment_lines)):
            found.append(f"GUARD:NO_COMMENT {rel}:{ln}  {NO_COMMENT_MESSAGE}")
    lines = stripped.code.split("\n")
    for rule, pattern in config["_compiled"]:
        if any(ex in f"/{rel}" for ex in rule.get("excludePaths", [])):
            continue
        if rule.get("extensions") and not any(rel.endswith(ext) for ext in rule["extensions"]):
            continue
        for idx, code_line in enumerate(lines, start=1):
            if pattern.search(code_line):
                found.append(f"GUARD:{rule['id']} {rel}:{idx}  {rule['message']}")
    return found


def run(root: Path, paths: list[str], staged: bool) -> tuple[int, list[str]]:
    profiles = load_profiles(root)
    checked: set[Path] = set()
    violations: list[str] = []
    for config in profiles:
        for f in collect(root, config, paths, staged):
            checked.add(f)
            violations.extend(check_file(f, root, config))
    return len(checked), violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="files or folders to check (default: --all)")
    parser.add_argument("--all", action="store_true", help="check every in-scope file in the project")
    parser.add_argument("--staged", action="store_true", help="check files staged in git")
    parser.add_argument("--root", help="project root (default: nearest folder with guardrails/ or .git)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else find_project_root(Path.cwd())
    try:
        count, violations = run(root, [] if args.all else args.paths, args.staged)
    except FileNotFoundError as error:
        print(str(error), file=sys.stderr)
        return 2
    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        print(
            f"{len(violations)} guardrail violation(s) in {count} file(s). Do not work around the "
            "symptom; fix the root cause the message names, then run the check again.",
            file=sys.stderr,
        )
        return 1
    print(f"Guardrails passed: {count} file(s) checked, 0 violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
