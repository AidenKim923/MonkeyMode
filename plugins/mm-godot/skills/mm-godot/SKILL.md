---
name: mm-godot
description: Godot engine adapter for MonkeyMode. Use when working on Godot code, scenes or assets in a MonkeyMode project, when mm-setup needs the Godot adapter folder, or when the user asks how MonkeyMode's rules apply to Godot (scenes and nodes, typed GDScript (or C#), signals, autoloads, Resources, high-level multiplayer).
---

# Godot adapter

Adapter folder (pass it to `mm-setup` as `--adapter-dir`): `${CLAUDE_PLUGIN_ROOT}/adapter`

If that path was not substituted (an agent without Claude Code plugins), the adapter is the `adapter/` folder next to this plugin's `skills/` folder.

Verification status: checked against the official Godot 4.7 docs. Open items are marked *needs verification* in the adapter docs. Read `adapter/adapter.json` for details.

## In a project that is set up

The adapter's docs are installed in the project's `docs/engine/` (or the docs folder named in `AGENTS.md`). Before changing Godot code:

1. Read `docs/engine/architecture-addendum.md` for structure and conventions, and `docs/engine/guardrails.md` for the banned patterns and why they are banned.
2. Self-verify with the commands in `docs/engine/build-and-test.md`: a headless import/parse run plus GUT or gdUnit4 tests. Always run `uv run tools/guardrails/check.py --all` too.
3. For networked features read `docs/engine/multiplayer.md` together with `docs/ai/04_NETWORK_AUTHORITY_AND_TESTING.md`.
4. Read `.monkeymode/config.json`: if `coding_level` is `cannot-read-code`, verify by running the game or tests yourself and explain the result in plain words with screenshots.

## In a project that is not set up

Run `mm-setup` first. Until then, read the docs directly from `${CLAUDE_PLUGIN_ROOT}/adapter/docs/`.
