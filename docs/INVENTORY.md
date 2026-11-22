# Inventory: what's in MonkeyMode

What is shared across engines, what is per engine, and how upstream skill names map to `mm-` names.

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
| Subagents | 16 in the optional `mm-agents` pack (none in `mm-core`) | One `mm-<engine>-expert` each |

Optional packs: `mm-agents` (Claude Code subagents, persona skills and party mode, kept apart because they are a heavier way of working that many users never need; the core workflow runs fully without them) and `mm-art-tools` (concept art and graphics-tool CLIs, which need extra installs).

## Subagents

Claude Code subagents (`agents/*.md` in a plugin), all MonkeyMode's own work. Read-only agents get only `Read, Grep, Glob`. "Full" is `Read, Grep, Glob, Edit, Write, Bash, Skill`.

| Agent | Plugin | Tools | Related skills |
|---|---|---|---|
| `mm-game-designer` | mm-agents | Read, Grep, Glob, Edit, Write | `mm-gdd` |
| `mm-level-designer` | mm-agents | Read, Grep, Glob, Edit, Write | `mm-gdd` |
| `mm-gameplay-programmer` | mm-agents | full | `mm-dev-story`, `mm-quick-dev` |
| `mm-code-reviewer` | mm-agents | read-only | `mm-code-review` |
| `mm-qa-tester` | mm-agents | full | `mm-test-framework`, `mm-test-design`, `mm-test-automate`, `mm-playtest-plan` |
| `mm-performance-profiler` | mm-agents | full | `mm-performance-test`, `mm-cli-renderdoc`, `mm-cli-nsight-graphics` |
| `mm-network-engineer` | mm-agents | full | `docs/ai/04` |
| `mm-technical-artist` | mm-agents | full | `mm-cli-blender`, `mm-cli-renderdoc`, `mm-cli-nsight-graphics` |
| `mm-ui-ux-designer` | mm-agents | Read, Grep, Glob, Edit, Write, Bash | `mm-ux`, `mm-decision-picker` |
| `mm-narrative-writer` | mm-agents | Read, Grep, Glob, Edit, Write | `mm-create-narrative` |
| `mm-audio-designer` | mm-agents | Read, Grep, Glob, Edit, Write | none |
| `mm-economy-balancer` | mm-agents | Read, Grep, Glob, Edit, Write, Bash | none |
| `mm-build-release-engineer` | mm-agents | full | none |
| `mm-localization` | mm-agents | full | none |
| `mm-guardrail-auditor` | mm-agents | read-only | `tools/guardrails/check.py` |
| `mm-docs-writer` | mm-agents | Read, Grep, Glob, Edit, Write | `mm-write-handoff`, `mm-document-project` |
| `mm-godot-expert` | mm-godot | full | `mm-godot` |
| `mm-unity-expert` | mm-unity | full | `mm-unity` |
| `mm-unreal-expert` | mm-unreal | full | `mm-unreal` |
| `mm-bevy-expert` | mm-bevy | full | `mm-bevy` |

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
| `clarify-ambiguous-request` | `mm-clarify-ambiguous-request` | mm-core | rewritten in English, generalized |
| `present-alternatives` | `mm-present-alternatives` | mm-core | rewritten in English, generalized |
| `write-handoff` | `mm-write-handoff` | mm-core | rewritten in English, generalized |
| `decision-picker` | `mm-decision-picker` | mm-core | rewritten in English, generalized |
| `concept-art` | `mm-concept-art` | mm-art-tools | rewritten in English, generalized |
| (new) | `mm-setup` | mm-core | new |
| (new) | `mm-unity` | mm-unity | new |
| (new) | `mm-godot` | mm-godot | new |
| (new) | `mm-unreal` | mm-unreal | new |
| (new) | `mm-bevy` | mm-bevy | new |

`mm-brainstorm-game` and `mm-brainstorming` were not merged: the game skill is a layer on top of the general brainstorming engine and calls it, so both are needed for it to work.

Legacy upstream IDs that only appeared as references (v6 shims such as the old PRD, research, story and review skill IDs) were redirected to the skills above.
