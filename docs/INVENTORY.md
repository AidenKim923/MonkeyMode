# Inventory: what MonkeyMode took from its source project, and why

MonkeyMode was extracted from a private Unity 6 + Mirror co-op game project that used BMad Method and BMad Game Dev Studio with its own agent rules, guardrails and tools. This file records the decision for every part of that source: **include** (as is, apart from renaming), **generalize** (rewritten in English, project specifics removed, engine specifics moved to an adapter), or **drop**.

Nothing project-specific was kept: no game name, characters, story, people, accounts, machine paths, server addresses or keys. Placeholders such as `<YourGame>` are filled by `mm-setup`.

## Shared vs. per-engine

| Area | Shared (`mm-core`) | Per engine (`mm-godot`, `mm-unity`, `mm-unreal`, `mm-bevy`) |
|---|---|---|
| Workflow templates | Game brief, GDD, narrative, UX, PRD, architecture, epics and stories, story, sprint status, playtest plan, performance test plan, test design, code review checklist, retrospective, decision log, project context, readiness report (inside the `mm-` skills) | none |
| Agent operating docs | `docs/ai/01-15`: execution policy, task brief, verification playbook, network authority (engine-neutral), handoff, response style, asset and data policy, planning and parallel work, pre-commit procedure, self-verification, token policy, guardrails, banned-API principles, workflow, team git workflow | `docs/engine/`: project context, architecture addendum, guardrails, build and test, multiplayer, version control (plus asset import for Unity) |
| Guardrails | `guardrails/secrets.json` (secrets, personal paths), the checker `tools/guardrails/check.py`, the after-edit hook, the git pre-commit hook | `guardrails/<engine>.json` banned patterns; Unity also `module-rules.json` and `asmdef_rules.py`; Bevy also `clippy.toml.example` |
| Tools | Log summary, window screenshots, multi-instance launcher, concept gallery and decision page | Unity: batch-mode tests and builds, change scope, selective verify, build entry point |
| Version control hints | `.gitignore` lines for MonkeyMode outputs | Engine `.gitignore` and `.gitattributes` lines (LFS lines commented out until enabled) |
| Guides | Blender asset pipeline, character production pipeline | Unity asset import checklist |
| Skills | 42 workflow and utility skills plus `mm-setup` | One `mm-<engine>` skill each |

Optional packs: `mm-agents` (persona agents and party mode, kept apart because they are a heavier, conversational way of working that many users never need) and `mm-art-tools` (concept art and graphics-tool CLIs, which need extra installs).

## Source inventory

| Source | Decision | Where it went / why |
|---|---|---|
| `.claude/skills/bmad-*`, `gds-*` (62 skills, byte-identical to BMad Method 6.12.4 and Game Dev Studio 0.7.2 at import) | include, renamed and merged | `plugins/mm-core/skills/`, `plugins/mm-agents/skills/`. 15 duplicates merged (table below). Tuning baked into `customize.toml` |
| `.agents/skills/` | drop | Identical mirror of `.claude/skills/` for Codex. `mm-setup --copy-skills agents` recreates it in user projects |
| `.claude/skills/clarify-ambiguous-request`, `present-alternatives`, `write-handoff` | generalize | Rewritten in English as `mm-` skills, no project names, aware of the user's coding level |
| `.claude/skills/decision-picker`, `concept-art` | generalize | `mm-decision-picker` (core) and `mm-concept-art` (art pack) with ChatGPT, Codex and alternative routes; model name no longer hard-coded |
| `.claude/skills/cli-anything-blender`, `-renderdoc`, `-nsight-graphics` | include | `plugins/mm-art-tools/skills/mm-cli-*`; Apache-2.0, only the skill name changed |
| `_bmad/scripts/*.py` | include, adapted | `plugins/mm-core/template/_mm/scripts/` (look for `_mm/`) |
| `_bmad/config.toml`, `{core,bmm,gds}/config.yaml` | generalize | One `_mm/config.toml` and `_mm/config.yaml` with placeholders; install answers (user name, languages, project name) removed |
| `_bmad/_config/bmad-help.csv`, `*/module-help.csv` | include, merged | `_mm/_config/mm-help.csv` (one catalog, upstream documentation URLs removed) |
| `_bmad/_config/manifest.yaml`, `files-manifest.csv`, `skill-manifest.csv` | drop | Installer bookkeeping (hashes, install dates, paths that do not exist in a plugin layout) |
| `_bmad/config.user.toml` | drop | Personal install answers (contained a user name) |
| `_bmad/custom/config.toml`, `.gitignore`, `render/.gitignore` | include | Template comments rewritten for `_mm/` |
| `_bmad/{bmm,core}/v6-shims/README.md` | drop | The shims were not installed; legacy IDs are mapped in the name map instead |
| `_bmad-output/`, `.agent-output/` | drop | Example outputs and generated images of the source game; used only to see what the templates produce |
| `AGENTS.md` | generalize | `plugins/mm-core/template/AGENTS.base.md`, assembled by `mm-setup` with the engine snippet and the user's answers. Game facts, decisions, company and tool model names removed |
| `CLAUDE.md` (`@AGENTS.md`) | include | Written by `mm-setup` when missing |
| `.claude/settings.json` (PostToolUse guardrail hook) | generalize | `plugins/mm-core/hooks/hooks.json`; a Python hook that respects the guardrail level |
| `.githooks/pre-commit` | generalize | Calls the Python checker; the assembly check runs only when module rules exist |
| `guardrails/banned-patterns.json` | generalize | `plugins/mm-unity/adapter/guardrails/unity.json`; messages in English, logging wrapper name generic |
| `guardrails/module-rules.json` | generalize | Unity adapter; the source game's module list replaced by a layered example |
| `guardrails/log-ignore.txt` | include | Empty in the source too |
| `docs/ai/01-13`, `README.md` | generalize | `plugins/mm-core/template/docs/ai/`, engine-neutral; Unity and Mirror specifics moved to `plugins/mm-unity/adapter/docs/` |
| `docs/project/00-02, 05, 06, 08`, the archived early draft, `Data/prop_inventory.csv` | drop | The source game's design, story, roadmap, props and character work |
| `docs/project/03` (Unity + Mirror architecture) | generalize | Its general Mirror rules went to `mm-unity/adapter/docs/multiplayer.md` and `architecture-addendum.md`; the game's modules dropped |
| `docs/project/04` (Blender pipeline) | generalize | `template/docs/guides/asset-pipeline-blender.md` |
| `docs/project/07` (character production pipeline) | generalize | `template/docs/guides/character-production-pipeline.md` and `mm-unity/adapter/docs/asset-import.md`; the game's characters and scripts removed |
| `docs/work/**` (notes, handoffs, about 250 renders) | drop | Project history. The workflow lessons in it were distilled into `docs/ai/14_GAME_DEV_WORKFLOW.md` and the skill defaults; `docs/work/pointer.md` is kept as an empty template |
| `tools/Test-Guardrails.ps1`, `Test-AsmdefRules.ps1` | generalize | Ported to Python (`tools/guardrails/check.py`, `asmdef_rules.py`) so the same checker runs in hooks on every OS; now supports several profiles and per-rule extensions |
| `tools/lib/Common.ps1` | generalize | Split: generic helpers in core, Unity helpers in `mm-unity/adapter/tools/lib/Unity.ps1`; no hard-coded install path |
| `tools/Invoke-UnityTests.ps1`, `Invoke-UnityBuild.ps1`, `Get-ChangeScope.ps1`, `Invoke-SelectiveVerify.ps1`, `unity-templates/AgentBuild.cs` | generalize | Unity adapter; messages in English; executable name and namespace from placeholders |
| `tools/Start-Game.ps1`, `Read-LogErrors.ps1`, `Save-Screenshot.ps1` | generalize | Core template (engine-neutral, Windows) |
| `tools/Start-ConceptServer.*`, `tools/concept-server/` | generalize | Core template; UI in English, generic title |
| `tools/Invoke-CodexImage.ps1` | generalize | `plugins/mm-art-tools/tools/`; model optional, runs from the plugin folder |
| `tools/hooks/claude-post-edit.ps1` | generalize | Replaced by `post_edit_hook.py` |
| `tools/blender/*` | drop | Build and render scripts for the source game's characters |
| `Assets/`, `ProjectSettings/`, `Packages/`, `*.csproj`, `*.slnx`, `ArtSource/`, `Library/`, `Logs/`, `UserSettings/`, `.vsconfig` | drop | The game itself and generated files |
| `.gitignore` | generalize | Split into the core fragment and the Unity adapter's `gitignore` |
| `README.md` | drop | Game name only |

## Skill name map

Every shipped skill uses the `mm-` prefix. Upstream names appear only in this table, in `NOTICE` and in `THIRD_PARTY_NOTICES.md`.

| Upstream / source name | MonkeyMode name | Plugin | Note |
|---|---|---|---|
| `bmad-advanced-elicitation` | `mm-advanced-elicitation` | mm-core | adapted |
| `bmad-agent-analyst` | `mm-agent-analyst` | mm-agents | adapted |
| `bmad-agent-pm` | `mm-agent-pm` | mm-agents | adapted |
| `bmad-agent-ux-designer` | `mm-agent-ux-designer` | mm-agents | adapted |
| `bmad-brainstorming` | `mm-brainstorming` | mm-core | adapted |
| `bmad-build-auto` | `mm-quick-dev-auto` | mm-core | adapted |
| `bmad-customize` | `mm-customize` | mm-core | adapted |
| `bmad-deep-recon` | `mm-research` | mm-core | adapted |
| `bmad-forge-idea` | `mm-forge-idea` | mm-core | adapted |
| `bmad-help` | `mm-help` | mm-core | adapted |
| `bmad-party-mode` | `mm-party-mode` | mm-agents | adapted |
| `bmad-prfaq` | `mm-prfaq` | mm-core | adapted |
| `bmad-review` | `mm-review` | mm-core | adapted |
| `bmad-spec` | `mm-spec` | mm-core | adapted |
| `bmad-walkthrough` | `mm-walkthrough` | mm-core | adapted |
| `cli-anything-blender` | `mm-cli-blender` | mm-art-tools | adapted |
| `cli-anything-nsight-graphics` | `mm-cli-nsight-graphics` | mm-art-tools | adapted |
| `cli-anything-renderdoc` | `mm-cli-renderdoc` | mm-art-tools | adapted |
| `gds-agent-game-architect` | `mm-agent-game-architect` | mm-agents | adapted |
| `gds-agent-game-designer` | `mm-agent-game-designer` | mm-agents | adapted |
| `gds-agent-game-dev` | `mm-agent-game-dev` | mm-agents | adapted |
| `gds-agent-game-solo-dev` | `mm-agent-game-solo-dev` | mm-agents | adapted |
| `gds-agent-tech-writer` | `mm-agent-tech-writer` | mm-agents | adapted |
| `gds-brainstorm-game` | `mm-brainstorm-game` | mm-core | adapted |
| `gds-check-implementation-readiness` | `mm-check-implementation-readiness` | mm-core | adapted |
| `gds-code-review` | `mm-code-review` | mm-core | adapted |
| `gds-correct-course` | `mm-correct-course` | mm-core | adapted |
| `gds-create-epics-and-stories` | `mm-create-epics-and-stories` | mm-core | adapted |
| `gds-create-game-brief` | `mm-create-game-brief` | mm-core | adapted |
| `gds-create-narrative` | `mm-create-narrative` | mm-core | adapted |
| `gds-create-story` | `mm-create-story` | mm-core | adapted |
| `gds-dev-story` | `mm-dev-story` | mm-core | adapted |
| `gds-document-project` | `mm-document-project` | mm-core | adapted |
| `gds-e2e-scaffold` | `mm-e2e-scaffold` | mm-core | adapted |
| `gds-game-architecture` | `mm-game-architecture` | mm-core | adapted |
| `gds-gdd` | `mm-gdd` | mm-core | adapted |
| `gds-generate-project-context` | `mm-generate-project-context` | mm-core | adapted |
| `gds-investigate` | `mm-investigate` | mm-core | adapted |
| `gds-performance-test` | `mm-performance-test` | mm-core | adapted |
| `gds-playtest-plan` | `mm-playtest-plan` | mm-core | adapted |
| `gds-prd` | `mm-prd` | mm-core | adapted |
| `gds-quick-dev` | `mm-quick-dev` | mm-core | adapted |
| `gds-retrospective` | `mm-retrospective` | mm-core | adapted |
| `gds-sprint-planning` | `mm-sprint-planning` | mm-core | adapted |
| `gds-sprint-status` | `mm-sprint-status` | mm-core | adapted |
| `gds-test-automate` | `mm-test-automate` | mm-core | adapted |
| `gds-test-design` | `mm-test-design` | mm-core | adapted |
| `gds-test-framework` | `mm-test-framework` | mm-core | adapted |
| `gds-test-review` | `mm-test-review` | mm-core | adapted |
| `gds-ux` | `mm-ux` | mm-core | adapted |
| `bmad-agent-architect` | `mm-agent-game-architect` | mm-agents | merged into the game version |
| `bmad-agent-dev` | `mm-agent-game-dev` | mm-agents | merged into the game version |
| `bmad-architecture` | `mm-game-architecture` | mm-core | merged into the game version |
| `bmad-build` | `mm-quick-dev` | mm-core | merged into the game version |
| `bmad-code-review` | `mm-code-review` | mm-core | merged into the game version |
| `bmad-correct-course` | `mm-correct-course` | mm-core | merged into the game version |
| `bmad-create-epics-and-stories` | `mm-create-epics-and-stories` | mm-core | merged into the game version |
| `bmad-prd` | `mm-prd` | mm-core | merged into the game version |
| `bmad-product-brief` | `mm-create-game-brief` | mm-core | merged into the game version |
| `bmad-project-context` | `mm-generate-project-context` | mm-core | merged into the game version |
| `bmad-qa-generate-e2e-tests` | `mm-test-automate` | mm-core | merged into the game version |
| `bmad-retrospective` | `mm-retrospective` | mm-core | merged into the game version |
| `bmad-sprint-planning` | `mm-sprint-planning` | mm-core | merged into the game version |
| `bmad-ux` | `mm-ux` | mm-core | merged into the game version |
| `gds-domain-research` | `mm-research` | mm-core | merged into the game version |
| `clarify-ambiguous-request` (project skill) | `mm-clarify-ambiguous-request` | mm-core | rewritten in English, generalized |
| `present-alternatives` (project skill) | `mm-present-alternatives` | mm-core | rewritten in English, generalized |
| `write-handoff` (project skill) | `mm-write-handoff` | mm-core | rewritten in English, generalized |
| `decision-picker` (project skill) | `mm-decision-picker` | mm-core | rewritten in English, generalized |
| `concept-art` (project skill) | `mm-concept-art` | mm-art-tools | rewritten in English, generalized |
| (new) | `mm-setup` | mm-core | new |
| (new) | `mm-unity` | mm-unity | new |
| (new) | `mm-godot` | mm-godot | new |
| (new) | `mm-unreal` | mm-unreal | new |
| (new) | `mm-bevy` | mm-bevy | new |

`mm-brainstorm-game` and `mm-brainstorming` were not merged: the game skill is a layer on top of the general brainstorming engine and calls it, so both are needed for it to work.

Legacy upstream IDs that only appeared as references (v6 shims such as the old PRD, research, story and review skill IDs) were redirected to the skills above.
