#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Claude Code PostToolUse hook: run guardrails on the file that was just edited.

Reads the hook payload from stdin. Does nothing unless the project has
guardrail profiles in guardrails/ and the edited file is in scope of one. On a
violation it prints the messages to stderr and exits 2, which Claude Code
feeds back to the agent so it fixes the root cause.

Prefers the project's own tools/guardrails/check.py (so local edits to the
checker apply) and falls back to the copy next to this file.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load_checker(project: Path):
    for candidate in (project / "tools" / "guardrails" / "check.py", Path(__file__).with_name("check.py")):
        if candidate.is_file():
            spec = importlib.util.spec_from_file_location("monkeymode_guardrails_check", candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    return None


def guardrail_level(project: Path) -> str:
    """strict / standard / relaxed from .monkeymode/config.json; always strict when the user cannot read code."""
    coding = os.environ.get("CLAUDE_PLUGIN_OPTION_CODING_LEVEL", "").lower()
    if "can't" in coding or "cannot" in coding:
        return "strict"
    path = project / ".monkeymode" / "config.json"
    try:
        cfg = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (OSError, json.JSONDecodeError):
        cfg = {}
    if cfg.get("coding_level") == "cannot-read-code":
        return "strict"
    level = cfg.get("guardrail_level")
    return level if level in ("strict", "standard", "relaxed") else "strict"


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()).resolve()
    if not (project / "guardrails").is_dir():
        return 0

    target = Path(file_path)
    if not target.is_absolute():
        target = project / target
    try:
        rel = target.resolve().relative_to(project).as_posix()
    except ValueError:
        return 0

    checker = load_checker(project)
    if checker is None:
        return 0
    try:
        profiles = checker.load_profiles(project)
    except FileNotFoundError:
        return 0
    if not target.is_file() or not any(checker.in_scope(rel, p) for p in profiles):
        return 0

    level = guardrail_level(project)
    _, violations = checker.run(project, [str(target)], staged=False)
    if level != "strict":
        violations = [v for v in violations if not v.startswith("GUARD:NO_COMMENT ")]
    if not violations:
        return 0
    if level == "relaxed":
        context = "Guardrail warnings (relaxed level, not blocking):\n" + "\n".join(violations)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}))
        return 0
    print("\n".join(violations), file=sys.stderr)
    print(
        "Guardrail violation in the file you just edited. Fix the root cause; do not edit guardrails/, "
        "add allowlist entries, or bypass hooks.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
