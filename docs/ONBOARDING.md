# Onboarding: how MonkeyMode sets up a project

MonkeyMode asks two kinds of questions:

| Kind | Where it is stored | Asked by | Answers |
|---|---|---|---|
| **About you** (same for every project) | Claude Code plugin settings (`userConfig` of `mm-core`) | Claude Code when you enable `mm-core`, changeable in `/plugin` → configure | `coding_level`, `uses_chatgpt` |
| **About this project** | `.monkeymode/config.json` in the project | `/mm-setup` (or `setup_project.py --interactive`) | everything else |

The project file wins when both have a value. `/mm-setup` skips questions that are already answered and can be run again at any time: it shows the current values and asks only what you want to change.

## The interview

```
           ┌──────────────────────────────┐
  start ──▶│ 1. Can you read code?        │  (skipped if set in plugin settings)
           └──────────────┬───────────────┘
                          ▼
           ┌──────────────────────────────┐
           │ 2. Engine                    │  godot / unity / unreal / bevy / other
           │    (detected engine is       │  → needs the mm-<engine> plugin;
           │     pre-selected)            │    "other" installs a fill-in stub
           └──────────────┬───────────────┘
                          ▼
           ┌──────────────────────────────┐
           │ 3. Do you also use ChatGPT?  │  (skipped if set)
           └──────┬────────────────┬──────┘
             yes  │                │ no
   ChatGPT prompts + import       Codex CLI if present, otherwise
   checklist from mm-concept-art   Blender blockouts, free asset libraries,
                  │                │ other generators
                  └───────┬────────┘
                          ▼
           ┌──────────────────────────────┐
           │ 4. Solo or team?             │  team → docs/ai/15 (branches, PRs,
           └──────────────┬───────────────┘          review checklist)
                          ▼
           ┌──────────────────────────────┐
           │ 5. Genre, target platforms   │  pc / mobile / web / console (multi)
           └──────────────┬───────────────┘
                          ▼
           ┌──────────────────────────────┐
           │ 6. Multiplayer?              │  yes → max players; networking guides
           └──────────────┬───────────────┘        and networked-only guardrails
                          ▼                       no → both left out
           ┌──────────────────────────────┐
           │ 7. Stage                     │  idea / planning / building / polishing
           └──────────────┬───────────────┘  → decides the recommended next skill
                          ▼
              can read code?
             yes │              │ no
                 ▼              ▼
   ┌──────────────────────┐   guardrails = strict (never asked)
   │ 8. Guardrail level   │
   │ strict / standard /  │
   │ relaxed              │
   └──────────┬───────────┘
              ▼
   ┌──────────────────────────────┐
   │ 9. Docs folder (docs/)       │
   └──────────────┬───────────────┘
                  ▼
   write .monkeymode/config.json · install core + engine adapter ·
   add the MonkeyMode section to AGENTS.md · make CLAUDE.md load it ·
   print a plain-language summary and the next step
```

### What each answer changes

| Answer | Effect |
|---|---|
| **I can't read code** | Guardrails forced to strict. `AGENTS.md` tells every agent to verify its own work (tests, build, run the game) before saying done, explain in plain words and screenshots instead of code, and ask before risky actions (deleting or moving files, large refactors, installing packages, pushing). Skills read the same setting from `.monkeymode/config.json` |
| **I can read code** | Your guardrail level applies; reports come in reviewable form (diff summary and why each change was made) |
| Engine | Copies the adapter's docs to `docs/engine/`, its guardrail profile to `guardrails/`, its tools to `tools/`, and appends its `.gitignore` / `.gitattributes` lines (LFS lines commented out) |
| ChatGPT yes / no | Routes `mm-concept-art` (needs the `mm-art-tools` pack) |
| Team | Installs `docs/ai/15_TEAM_GIT_WORKFLOW.md`; `AGENTS.md` rule 9 points to it |
| Multiplayer yes | Installs `docs/ai/04` and `docs/engine/multiplayer.md`; `AGENTS.md` requires multi-client checks (M2) for networked changes |
| Multiplayer no | Leaves those out and drops networked-only guardrail rules (time-scale writes and similar) |
| Stage | idea → `mm-brainstorm-game`; planning → `mm-create-game-brief` (or `mm-gdd`); building → `mm-document-project` then `mm-dev-story`; polishing → `mm-playtest-plan` |
| Guardrail level | **strict**: every rule blocks after each edit, including the no-comment rule where the engine profile has it (Unity). **standard**: rules block, comments allowed. **relaxed**: rule hits are shown to the agent after edits but do not block; the git pre-commit hook (if enabled) still checks |
| Docs folder | All installed docs and links use it instead of `docs/` |

Existing files are never overwritten unless you pass `--force`. Three things are always updated: the MonkeyMode section of `AGENTS.md` (between `<!-- monkeymode:start -->` and `<!-- monkeymode:end -->`), the `@AGENTS.md` line in `CLAUDE.md`, and `.monkeymode/config.json`.

## Without Claude Code (Codex and other AGENTS.md agents)

Clone MonkeyMode and run the same interview in a terminal (Python 3.11+, `uv` recommended):

```
uv run plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

- `--copy-skills agents` copies the core skills and your engine's skill into `<your game>/.agents/skills/` (Codex reads them there). Use `claude` or `both` for `.claude/skills/`.
- `--packs mm-agents,mm-art-tools` adds the optional packs.
- `--git-hooks` sets `core.hooksPath` so guardrails run before every commit.
- Non-interactive: replace `--interactive` with `--set key=value` pairs (keys: `coding_level`, `engine`, `uses_chatgpt`, `team`, `genre`, `platforms`, `multiplayer`, `max_players`, `stage`, `guardrail_level`, `docs_dir`, `project_name`).
- `--show` prints the current config and the open questions; `--detect` prints the detected engine; `--dry-run` lists what would be written.

Agents that read `AGENTS.md` pick up the rules immediately. The after-edit hook is Claude Code only; other agents rely on the pre-commit hook and on running `uv run tools/guardrails/check.py --all` as `AGENTS.md` instructs.

## When the config is missing

Every `mm-` skill checks `.monkeymode/config.json`. Without it, skills ask what they need (for example the coding level, in plain language) or suggest running `/mm-setup`. The guardrail hook defaults to strict when there is no config.
