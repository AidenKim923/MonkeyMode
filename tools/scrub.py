#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Release scrub for the MonkeyMode repository.

Fails when tracked files contain:
- non-English scripts (Hangul, kana, CJK, Cyrillic, ...) outside README.<lang>.md translations,
- upstream skill-name prefixes (bmad-, gds-) outside the attribution files,
- absolute paths into a user's home folder,
- secrets, using the core guardrail profile.

    uv run tools/scrub.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]

TRANSLATION = re.compile(r"(^|/)README\.[a-z]{2}(-[A-Z]{2})?\.md$")
SCRIPT_RANGES = [(0x0400, 0x04FF), (0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xAC00, 0xD7AF), (0x1100, 0x11FF), (0x3130, 0x318F)]
NON_ENGLISH = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in SCRIPT_RANGES) + "]")
UPSTREAM_TEST_DATA = {
    "plugins/mm-agents/skills/mm-agent-game-dev/gametest/knowledge/localization-testing.md": "upstream localization examples (Russian plural forms)",
    "plugins/mm-agents/skills/mm-agent-game-dev/gametest/knowledge/save-testing.md": "upstream Unicode save-name test case",
    "plugins/mm-core/skills/mm-brainstorming/scripts/tests/test_brain.py": "upstream Unicode round-trip test data",
}
UPSTREAM = re.compile(r"(?<![\w/.-])(bmad|gds)-[a-z]", re.IGNORECASE)
UPSTREAM_ALLOWED = re.compile(r"(^|/)(NOTICE|THIRD_PARTY_NOTICES\.md|README(\.[a-zA-Z-]+)?\.md|INVENTORY\.md)$|(^|/)licenses/|^tools/scrub\.py$")
HOME_PATH = re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+(?![<{$%])[^\\/\s\"'`]+|/home/(?![<{$])[a-z_][a-z0-9_.-]*/|/Users/(?![<{$]|Shared/)[A-Za-z0-9._-]+/")
TEXT_SUFFIXES = {".md", ".json", ".toml", ".yaml", ".yml", ".txt", ".py", ".ps1", ".cs", ".mjs", ".js", ".html", ".csv", ".cmd", ".sh", ".example", ""}


def tracked() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard"], capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p]


def main() -> int:
    problems: list[str] = []
    files = tracked()
    for rel in files:
        path = ROOT / rel
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        translation = bool(TRANSLATION.search(rel)) or rel in UPSTREAM_TEST_DATA
        for n, line in enumerate(text.splitlines(), 1):
            if not translation and NON_ENGLISH.search(line):
                problems.append(f"NON_ENGLISH {rel}:{n}")
            if not UPSTREAM_ALLOWED.search(rel) and UPSTREAM.search(line):
                problems.append(f"UPSTREAM_NAME {rel}:{n}: {line.strip()[:80]}")
            if HOME_PATH.search(line):
                problems.append(f"HOME_PATH {rel}:{n}")

    profile = ROOT / "plugins/mm-core/template/guardrails/secrets.json"
    checker = ROOT / "plugins/mm-core/template/tools/guardrails/check.py"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "guardrails").mkdir()
        data = json.loads(profile.read_text(encoding="utf-8"))
        for rule in data["rules"]:
            rule["excludePaths"] = []
        (tmp_root / "guardrails" / "secrets.json").write_text(json.dumps(data), encoding="utf-8")
        for rel in files:
            src = ROOT / rel
            if src.is_file() and src.suffix in TEXT_SUFFIXES and not rel.endswith("guardrails/secrets.json"):
                dest = tmp_root / "repo" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src.read_bytes())
        result = subprocess.run([sys.executable, str(checker), "--root", str(tmp_root), "--all"], capture_output=True, text=True)
        if result.returncode != 0:
            problems.extend("SECRET " + line for line in result.stderr.splitlines() if line.startswith("GUARD:"))

    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"scrub failed: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print(f"scrub passed: {len(files)} tracked files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
