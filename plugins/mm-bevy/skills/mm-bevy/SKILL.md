---
name: mm-bevy
description: Bevy engine adapter for MonkeyMode. Use when working on Bevy code, scenes or assets in a MonkeyMode project, when mm-setup needs the Bevy adapter folder, or when the user asks how MonkeyMode's rules apply to Bevy (Rust ECS: components, systems, schedules and ordering, plugins, lightyear/replicon/renet).
---

# Bevy adapter

Adapter folder (pass it to `mm-setup` as `--adapter-dir`): `${CLAUDE_PLUGIN_ROOT}/adapter`

If that path was not substituted (an agent without Claude Code plugins), the adapter is the `adapter/` folder next to this plugin's `skills/` folder.

Verification status: checked against Bevy 0.20 and current networking crates; not field-tested in a project yet. Open items are marked *needs verification* in the adapter docs. Read `adapter/adapter.json` for details.

## In a project that is set up

The adapter's docs are installed in the project's `docs/engine/` (or the docs folder named in `AGENTS.md`). Before changing Bevy code:

1. Read `docs/engine/architecture-addendum.md` for structure and conventions, and `docs/engine/guardrails.md` for the banned patterns and why they are banned.
2. Self-verify with the commands in `docs/engine/build-and-test.md`: cargo clippy -D warnings and cargo test per affected crate. Always run `uv run tools/guardrails/check.py --all` too.
3. For networked features read `docs/engine/multiplayer.md` together with `docs/ai/04_NETWORK_AUTHORITY_AND_TESTING.md`.
4. Read `.monkeymode/config.json`: if `coding_level` is `cannot-read-code`, verify by running the game or tests yourself and explain the result in plain words with screenshots.

## In a project that is not set up

Run `mm-setup` first. Until then, read the docs directly from `${CLAUDE_PLUGIN_ROOT}/adapter/docs/`.
