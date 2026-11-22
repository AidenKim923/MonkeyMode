---
name: mm-setup
description: Set up or change MonkeyMode for this game project through a short interview - coding level, engine, ChatGPT use, solo or team, genre and platforms, multiplayer, project stage, guardrail level, docs folder - then write .monkeymode/config.json, install the shared docs, guardrails and tools plus the chosen engine adapter, wire AGENTS.md/CLAUDE.md, and recommend the first skill to run. Use when the user says "set up MonkeyMode", "/mm-setup", when another mm- skill finds no .monkeymode/config.json, or when the user wants to change a setting. Safe to re-run.
---

# MonkeyMode setup

You run a short, friendly interview and then a script that does the file work. Keep the tone plain: the user may not read code.

The script is `${CLAUDE_PLUGIN_ROOT}/skills/mm-setup/scripts/setup_project.py` (if `${CLAUDE_PLUGIN_ROOT}` was not substituted, use the `scripts/` folder next to this file). Run it with `uv run <script> --target <project root> ...`. It needs Python 3.11+ and `uv`; if `uv` is missing, `python <script>` works too.

## 1. Read what is already known

1. Run `--show`. It prints the current `.monkeymode/config.json` (or defaults), the questions still open (`missing`) and detected engines.
2. Person-level answers from the plugin settings, when set (empty means unset):
   - coding level: `${user_config.coding_level}` ("I can read code" → `can-read-code`, "I can't read code" → `cannot-read-code`)
   - uses ChatGPT: `${user_config.uses_chatgpt}`
   If a value above still shows the literal placeholder text (it starts with a dollar sign and `{user_config.`), the setting is **unset**: ask the question. The project file wins over these. Skip any question either source already answers, and say in one line which answers you took from where ("From your plugin settings: you read code, no ChatGPT."). The user changes plugin settings in `/plugin` → MonkeyMode core → configure, or with `claude plugin configure mm-core@monkeymode`.
3. **Re-run:** if the config file exists, first show the current values in a short plain list, then ask one question: what should change? Ask only those questions again, then apply.

## 2. Interview (in this order, skipping what is answered)

Use the question tool (AskUserQuestion) with the choices below; put the recommended choice first. Bundle up to four independent questions per round; respect the branches.

| # | Question | Choices | Branch |
|---|---|---|---|
| 1 | Can you read code? | I can read code / I can't read code | `cannot-read-code` → guardrails are forced to strict; never ask question 8 |
| 2 | Which engine? | Godot / Unity / Unreal / Bevy / Other | Pre-select the detected engine. Other → no adapter |
| 3 | Do you also use ChatGPT? | Yes (recommended for images) / No | Yes → concept art comes as ready-to-paste ChatGPT prompts plus an import checklist. No → Codex CLI if present, otherwise Blender blockouts, free asset libraries, other generators |
| 4 | Solo or team? | Solo / Team | Team → branch and pull request rules and a review checklist are installed |
| 5 | Genre, and target platforms | Genre: free text. Platforms (multi-select): PC / Mobile / Web / Console | |
| 6 | Multiplayer? | No / Yes | Yes → ask the maximum player count and install the networking guides. No → networking docs and networked-only guardrails are left out |
| 7 | Where are you now? | Just an idea / Planning / Already building / Polishing | Decides the recommended next skill |
| 8 | Guardrail level? | Standard (recommended) / Strict / Relaxed | Only when the user reads code. Strict: everything blocks, including the no-comment rule where the engine supports it. Standard: rules block, comments allowed. Relaxed: rules warn after edits but do not block |
| 9 | Docs folder? | docs/ (default) / other | |

The game name defaults to the project folder name; ask only if the folder name looks like a placeholder.

## 3. Engine adapter

For Godot, Unity, Unreal or Bevy the matching plugin (`mm-godot`, `mm-unity`, `mm-unreal`, `mm-bevy`) must be installed. Load its skill (`mm-<engine>`): it prints its adapter folder. If it is not installed, tell the user the one command to run (`/plugin install mm-<engine>@monkeymode`) and wait, or continue with engine `other` if they prefer.

## 4. Apply

Run the script once with every answer:

```
uv run <script> --target <project root> --apply --adapter-dir <adapter folder> \
  --set coding_level=<can-read-code|cannot-read-code> --set engine=<godot|unity|unreal|bevy|other> \
  --set uses_chatgpt=<yes|no> --set team=<solo|team> --set genre="<text>" --set platforms=<pc,mobile,web,console> \
  --set multiplayer=<yes|no> [--set max_players=<n>] --set stage=<idea|planning|building|polishing> \
  [--set guardrail_level=<strict|standard|relaxed>] --set docs_dir=<docs/> [--set project_name="<name>"]
```

Add `--git-hooks` if the user agrees to guardrail checks before every commit (recommend it for `cannot-read-code`). Existing files are kept; the `AGENTS.md` MonkeyMode section (between `<!-- monkeymode:start -->` markers), `CLAUDE.md`'s `@AGENTS.md` line and `.monkeymode/config.json` are always updated. Use `--dry-run` first if the project already has many files and the user wants to see the list.

## 5. Report

Relay the script's summary in plain words: what was set, what was installed, what was kept, and the **recommended next step** (idea → `mm-brainstorm-game`; planning → `mm-create-game-brief` or `mm-gdd`; building → `mm-document-project` then `mm-dev-story`; polishing → `mm-playtest-plan`). Offer to start it now.

## Without Claude Code

The same interview runs in a terminal: `python setup_project.py --target <project> --interactive --apply --copy-skills agents` (from a MonkeyMode checkout; `--packs mm-agents,mm-art-tools` adds optional packs). See `docs/ONBOARDING.md` in the MonkeyMode repository.
