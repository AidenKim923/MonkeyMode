#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Offline manifest checks for the MonkeyMode marketplace.

A stand-in for `claude plugin validate` where the Claude Code CLI is not available (CI):
- every JSON file in the repository parses,
- .claude-plugin/marketplace.json lists each plugin once, with a source folder that exists,
- each plugin's .claude-plugin/plugin.json has a name matching its folder and the marketplace
  entry, and the same version as the marketplace entry,
- every skill folder has a SKILL.md whose frontmatter `name` matches the folder and that has
  a `description`, and skill names use the mm- prefix,
- hooks/hooks.json, when present, has a top-level "hooks" object.

    uv run tools/check_manifests.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.DOTALL)


def tracked_json() -> list[Path]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-co", "--exclude-standard", "*.json"], capture_output=True, text=True, check=True)
    return [ROOT / p for p in out.stdout.splitlines() if p]


def load(path: Path, problems: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        problems.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def main() -> int:
    problems: list[str] = []
    for path in tracked_json():
        if path.is_file():
            load(path, problems)

    market = load(ROOT / ".claude-plugin/marketplace.json", problems) or {}
    entries = market.get("plugins", [])
    if not market.get("name"):
        problems.append("marketplace.json: missing name")
    seen: set[str] = set()
    for entry in entries:
        name, source = entry.get("name"), entry.get("source", "")
        if not name or name in seen:
            problems.append(f"marketplace.json: missing or duplicate plugin name {name!r}")
            continue
        seen.add(name)
        folder = (ROOT / source).resolve()
        manifest_path = folder / ".claude-plugin/plugin.json"
        if not manifest_path.is_file():
            problems.append(f"marketplace.json: {name}: no plugin.json under {source}")
            continue
        manifest = load(manifest_path, problems) or {}
        if manifest.get("name") != name or folder.name != name:
            problems.append(f"{name}: plugin.json name {manifest.get('name')!r} and folder {folder.name!r} must match the marketplace entry")
        if entry.get("version") and manifest.get("version") != entry.get("version"):
            problems.append(f"{name}: version {manifest.get('version')!r} differs from marketplace {entry.get('version')!r}")
        if not manifest.get("description"):
            problems.append(f"{name}: plugin.json has no description")
        hooks = folder / "hooks/hooks.json"
        if hooks.is_file():
            data = load(hooks, problems)
            if data is not None and not isinstance(data.get("hooks"), dict):
                problems.append(f"{name}: hooks/hooks.json needs a top-level 'hooks' object")
        for skill in sorted((folder / "skills").glob("*/")):
            skill_md = skill / "SKILL.md"
            rel = skill_md.relative_to(ROOT)
            if not skill_md.is_file():
                problems.append(f"{rel}: missing")
                continue
            match = FRONTMATTER.match(skill_md.read_text(encoding="utf-8"))
            meta = dict(re.findall(r"^([a-z_-]+):\s*(.*)$", match.group(1), re.MULTILINE)) if match else {}
            if meta.get("name", "").strip("'\"") != skill.name:
                problems.append(f"{rel}: frontmatter name must be {skill.name!r}")
            if not meta.get("description"):
                problems.append(f"{rel}: frontmatter has no description")
            if not skill.name.startswith("mm-"):
                problems.append(f"{rel}: skill names use the mm- prefix")

    plugin_dirs = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    for missing in sorted(plugin_dirs - seen):
        problems.append(f"plugins/{missing}: not listed in marketplace.json")

    for p in problems:
        print(p)
    print(f"{len(seen)} plugins checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
