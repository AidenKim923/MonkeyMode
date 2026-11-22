#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Check that README.md and its README.<lang>.md translations share one structure.

Compared with README.md, every translation must have:
- the same heading levels in the same order, and the same explicit anchors (<a id="...">),
- the same tables, each with the same number of rows and columns,
- identical fenced code blocks (code is never translated),
- the same images and badges, and the same number of <details> sections,
- the same set of local link targets.

In every README, local links and images must point to files that exist.

    uv run tools/readme_parity.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^```[^\n]*\n.*?^```", re.MULTILINE | re.DOTALL)
HEADING = re.compile(r"^(#{1,6}) ", re.MULTILINE)
ANCHOR = re.compile(r'<a id="([^"]+)"></a>')
IMG = re.compile(r'<img [^>]*src="([^"]+)"')
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
HREF = re.compile(r'href="([^"]+)"')
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def tables(text: str) -> list[tuple[int, int]]:
    found, rows, cols = [], 0, 0
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            if rows == 0:
                cols = line.count("|") - line.count("\\|")
            rows += 1
        elif rows:
            found.append((rows, cols))
            rows = 0
    return found


def local_targets(text: str) -> set[str]:
    targets = set(MD_LINK.findall(text)) | set(HREF.findall(text))
    return {t for t in targets if not re.match(r"^[a-z]+:", t) and not t.startswith("#")}


def summary(text: str) -> dict[str, object]:
    code = FENCE.findall(text)
    prose = COMMENT.sub("", FENCE.sub("", text))
    return {
        "headings": [len(h) for h in HEADING.findall(prose)],
        "anchors": ANCHOR.findall(prose),
        "tables": tables(prose),
        "code blocks": code,
        "images": IMG.findall(prose),
        "details": prose.count("<details>"),
        "local links": sorted(t for t in local_targets(prose) if not re.match(r"^README(\.[A-Za-z-]+)?\.md$", t)),
    }


def main() -> int:
    readmes = sorted(ROOT.glob("README*.md"))
    base_path = ROOT / "README.md"
    base = summary(base_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    for path in readmes:
        text = path.read_text(encoding="utf-8")
        info = summary(text)
        if path != base_path:
            for key, expected in base.items():
                if info[key] != expected:
                    problems.append(f"{path.name}: {key} differ from README.md")
        for target in local_targets(COMMENT.sub("", FENCE.sub("", text))) | set(info["images"]):
            if re.match(r"^[a-z]+:", target):
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not (ROOT / file_part).exists():
                problems.append(f"{path.name}: broken link or image {target}")
        if path.name != "README.md" and "](README.md)" not in text:
            problems.append(f"{path.name}: language switcher has no link back to README.md")
    for p in problems:
        print(p)
    print(f"{len(readmes)} READMEs checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
