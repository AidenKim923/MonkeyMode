Read by Codex and other agents; Claude Code loads it through `CLAUDE.md`. Details live in [`docs/ai/`](docs/ai/README.md) and [`docs/engine/`](docs/engine/README.md): open only the doc relevant to the current task. Project settings are in `.monkeymode/config.json` (change them with `mm-setup`).

## Project

<YourGame>. Genre: {{GENRE}}. Platforms: {{PLATFORMS}}. Stage: {{STAGE}}. Design source of truth: [`docs/project/`](docs/project/README.md).

## Working with this user

{{USER_SECTION}}

## Rules

1. **Guardrails over comments.** Rules are enforced by compilers, module boundaries, guardrail profiles and tests. Fix the root cause of a failure; never bypass guardrails (editing rules, allowlists, `--no-verify`). → [guardrails](docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md)
2. **Banned APIs and patterns** are in `guardrails/*.json`. Ask before using any other tricky API. → [list](docs/ai/13_BANNED_APIS.md), [engine notes](docs/engine/guardrails.md)
3. **Self-verify**: build, test, run, check logs. Screenshot visible results per window and report the path. → [tooling](docs/ai/10_SELF_VERIFICATION_TOOLING.md), [engine commands](docs/engine/build-and-test.md)
4. **Before committing**: diff → trace impact → selective regression (add tests if thin) → self-fix loop. → [procedure](docs/ai/09_PRE_COMMIT_PROCEDURE.md)
5. **Save tokens**: narrow scope first (path → module → symbol → history), reuse scripts, split unrelated requests into sessions. → [policy](docs/ai/11_TOKEN_AND_SESSION_POLICY.md)
6. **Completion report, 4 items**: changes · impact · verification · follow-ups/guardrail proposals. → [style](docs/ai/06_RESPONSE_STYLE_GUIDE.md)
7. {{MULTIPLAYER_SECTION}}
8. Analysis requests are not edit approval. Tunable values go in data assets. Unverified means `unverified`.
9. **Commit or push only on explicit request**, after rule 4. No history rewriting. {{TEAM_SECTION}}
10. AI-made assets (models, animation, level and challenge quality) are not final until the user approves them. → [asset policy](docs/ai/07_ASSET_AND_DATA_POLICY.md)

{{ENGINE_SECTION}}

## Tools and assets

- Guardrails: `uv run tools/guardrails/check.py --all` (also runs after every edit in Claude Code and, if enabled, in the git pre-commit hook: `git config core.hooksPath .githooks`).
- {{IMAGES_SECTION}}
- Choices between UI mockups or image-based assets: `mm-decision-picker` puts them on `http://localhost:5090/` so the user picks there. Never ask the user to copy results.
- 3D work: Blender CLI first (`mm-cli-blender`, or `blender -b` scripts), an MCP bridge only for what the CLI cannot do. Installing tools needs user confirmation.

## Source of truth on conflict

Current code/config → `git status`/`git diff` → this file, `docs/ai/` and `docs/engine/` → `docs/project/` → earlier handoffs → past conversation. Code wins over docs; report the discrepancy. The user's latest explicit instruction is never overridden by old docs.

## Undecided

List the decisions the user has not made yet (for example networking library version, platform services, save format, voice chat, camera). Agents report options and impact for these and never settle them.

- `<add undecided items here>`

## Workflow

MonkeyMode skills (`mm-*`) run the design-to-ship workflow; start with `mm-help`. Drafts go to `_mm-output/`; lasting decisions to `docs/project/`. This file, `docs/ai/` and `docs/engine/` override skill instructions. Customize skills in `_mm/custom/`, not in the skill files. → [workflow](docs/ai/14_GAME_DEV_WORKFLOW.md)

## Work records

Docs outside `docs/work/` state current facts only: no dates, "decided on", or change-history wording. Write progress, work notes and handoffs to `docs/work/{date}/{topic}.md` and add one line to [`docs/work/pointer.md`](docs/work/pointer.md). Records are committed: no secrets, accounts or personal paths. Logs go to `logs/{YYYY-MM-DD}/`; `logs/` and `.agent-output/` are git-ignored.
