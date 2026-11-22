# AI operating docs

> How agents work in this project. Installed by MonkeyMode; edit freely to fit `<YourGame>`.

`mm-setup` installs only what applies: 04 is left out for single-player games and 15 for solo projects.

**Do not read all of these.** Open only the one that matches the task at hand. The root [`AGENTS.md`](../../AGENTS.md) is loaded automatically by agents; it links here.

These docs are engine-neutral. Engine-specific rules (project structure, banned patterns, build and test commands, multiplayer stack) live in [`docs/engine/`](../engine/README.md), installed from the engine adapter you picked at setup. Sections marked **[Windows]** are OS-specific.

## What to read when

| Situation | Read |
|---|---|
| Looking up the game's rules, story or structure | [`docs/project/`](../project/README.md), the design source of truth |
| Handing a task to an agent | [02 Task brief](02_TASK_BRIEF_TEMPLATE.md) |
| An agent says "done" | [03 Verification playbook](03_VERIFICATION_PLAYBOOK.md) |
| Deciding server vs client, or testing with several players | [04 Network authority and testing](04_NETWORK_AUTHORITY_AND_TESTING.md) |
| Pausing work or continuing a long session | [05 Handoff and context](05_HANDOFF_AND_CONTEXT.md) |
| Formatting an agent's report | [06 Response style](06_RESPONSE_STYLE_GUIDE.md) |
| Deciding whether a model, texture, sound or external AI may be used | [07 Asset and data policy](07_ASSET_AND_DATA_POLICY.md) |
| Turning design docs into tasks, or splitting work in parallel | [08 Planning to tasks and parallel work](08_PLANNING_TO_TASKS_AND_PARALLEL_WORK.md) |
| Before committing or applying code | [09 Pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) |
| Building, testing, running, reading logs, taking screenshots | [10 Self-verification tooling](10_SELF_VERIFICATION_TOOLING.md) |
| Several requests at once, or context cost is a worry | [11 Token and session policy](11_TOKEN_AND_SESSION_POLICY.md) |
| You want to write a comment, or a guardrail fired | [12 Guardrails instead of comments](12_GUARDRAILS_INSTEAD_OF_COMMENTS.md) |
| Checking whether an API or library is tricky | [13 Banned APIs](13_BANNED_APIS.md) |
| Running the MonkeyMode design-to-ship workflow | [14 Game dev workflow](14_GAME_DEV_WORKFLOW.md) |
| Branches, pull requests and reviews (team projects) | [15 Team git workflow](15_TEAM_GIT_WORKFLOW.md) |

## Document map

### Project source of truth (`docs/project/`)

Your game's design documents: overview, story bible, mechanics, architecture summary, roadmap. MonkeyMode only ships an empty index; you fill it as workflow outputs are approved (see [14](14_GAME_DEV_WORKFLOW.md)).

### Engine adapter (`docs/engine/`)

| Doc | Content |
|---|---|
| [README](../engine/README.md) | What the adapter covers and its verification status |
| [Project context](../engine/project-context.md) | Engine version, language, folder layout, naming (fill in) |
| [Architecture addendum](../engine/architecture-addendum.md) | Scene/asset structure, scripting model, module boundaries |
| [Guardrails](../engine/guardrails.md) | Engine banned patterns and why |
| [Build and test](../engine/build-and-test.md) | Commands agents run to self-verify |
| [Multiplayer](../engine/multiplayer.md) | Networking stack options and engine-specific pitfalls |
| [Version control](../engine/version-control.md) | .gitignore, LFS and merge hints |

### Guides (`docs/guides/`)

| Doc | Content |
|---|---|
| [Asset pipeline (Blender)](../guides/asset-pipeline-blender.md) | Model specs, automated checks, approval gates |
| [Character production pipeline](../guides/character-production-pipeline.md) | Studio character pipeline adapted for small teams |

### AI operations (`docs/ai/`)

| Doc | When |
|---|---|
| [01 Execution policy](01_AGENT_EXECUTION_POLICY.md) | Approval boundaries and stop conditions |
| [02 Task brief](02_TASK_BRIEF_TEMPLATE.md) | Feature, bug, research and asset requests |
| [03 Verification playbook](03_VERIFICATION_PLAYBOOK.md) | Tie completion claims to evidence |
| [04 Network authority and testing](04_NETWORK_AUTHORITY_AND_TESTING.md) | Server/client decisions, multi-client checks |
| [05 Handoff and context](05_HANDOFF_AND_CONTEXT.md) | Pausing, resuming, long sessions |
| [06 Response style](06_RESPONSE_STYLE_GUIDE.md) | Report format |
| [07 Asset and data policy](07_ASSET_AND_DATA_POLICY.md) | AI-generated assets, licenses, what may leave the machine |
| [08 Planning to tasks and parallel work](08_PLANNING_TO_TASKS_AND_PARALLEL_WORK.md) | Gap analysis, phase plans, parallel workers |
| [09 Pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) | Diff → impact → selective regression → self-fix loop |
| [10 Self-verification tooling](10_SELF_VERIFICATION_TOOLING.md) | `tools/` scripts for build, test, run, logs, screenshots |
| [11 Token and session policy](11_TOKEN_AND_SESSION_POLICY.md) | Light vs heavy work, narrowing scope, one session per request |
| [12 Guardrails instead of comments](12_GUARDRAILS_INSTEAD_OF_COMMENTS.md) | The no-comment rule and how rules are enforced mechanically |
| [13 Banned APIs](13_BANNED_APIS.md) | The banned API list, its reasoning and sources |
| [14 Game dev workflow](14_GAME_DEV_WORKFLOW.md) | Order of `mm-` skills and where outputs go |
| [15 Team git workflow](15_TEAM_GIT_WORKFLOW.md) | Team projects only: branches, pull requests, review checklist |

## Project baseline

Fill this table in when you set up the project. Agents treat empty values as undecided.

| Item | Value | Status |
|---|---|---|
| Engine | `<Engine>` `<version>` | |
| Networking | `<None / library, topology, max players>` | |
| Art pipeline | `<e.g. Blender CLI first, Blender MCP when the CLI cannot>` | |
| First milestone | `<e.g. vertical slice of one level>` | |
| Current code | `<What exists today>` | Update when code appears |

When a value is decided, update this table and the source document together.

## Maintenance

- When code and docs disagree, **code wins**; record the discrepancy.
- Do not copy one rule into several docs. Link to the original.
- Implemented numbers live in data assets (ScriptableObjects, Resources, DataAssets, config files: whatever your engine uses). For items without a data asset, `docs/project/` is the design source.
- Delete docs that no longer apply. If history matters, move it into a handoff under `docs/work/`.
- When you add or move a doc, update this map and [`AGENTS.md`](../../AGENTS.md).
