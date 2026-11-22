# MonkeyMode user guide

> **I'm Monkey Game Developer 🐒** This guide covers everything from installing MonkeyMode to shipping a playtested build. The README is the short version; [ONBOARDING.md](ONBOARDING.md) has the full setup flow chart; [INVENTORY.md](INVENTORY.md) says where every part came from.

## Contents

1. [What MonkeyMode is](#1-what-monkeymode-is)
2. [Install](#2-install)
3. [Set up a project with /mm-setup](#3-set-up-a-project-with-mm-setup)
4. [The end-to-end process](#4-the-end-to-end-process)
5. [Guardrails and hooks](#5-guardrails-and-hooks)
6. [Images and concept art](#6-images-and-concept-art)
7. [Engine notes](#7-engine-notes)
8. [Customizing](#8-customizing)
9. [FAQ and troubleshooting](#9-faq-and-troubleshooting)

---

## 1. What MonkeyMode is

MonkeyMode is a set of plugins that teach an AI coding agent how to make a game the way a careful studio would:

- **A workflow.** About 40 `mm-` skills take you from a rough idea to a game design document (GDD), a technical architecture, epics and stories, implemented stories with code review, playtest plans and retrospectives. Each skill writes a real file you can read and keep.
- **Working rules for the agent.** `AGENTS.md` and `docs/ai/` tell the agent to check its own work (build, test, run, screenshot) before it says "done", to label anything it could not check as `unverified`, to stay inside the requested scope, and to report in a fixed four-part format.
- **Guardrails.** Machine-checked rules block the mistakes agents keep making in game code (fragile scene lookups, blocking calls, unsafe networking, secrets in the repository). They run after every edit and, if you enable it, before every commit.
- **Engine adapters.** Godot, Unity, Unreal and Bevy each get their own docs, banned patterns, build and test commands, and multiplayer notes. Everything else is shared.

It adapts to you. If you say you don't read code, agents explain in plain words with screenshots, verify everything themselves, ask before risky steps, and run at the strictest guardrail level.

## 2. Install

### Claude Code

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # or mm-godot, mm-unreal, mm-bevy
```

Optional packs:

```
/plugin install mm-agents@monkeymode      # persona agents and party mode
/plugin install mm-art-tools@monkeymode   # concept art, Blender/RenderDoc/Nsight CLIs
```

Installing an engine plugin pulls in `mm-core` automatically. From a local clone you can use the path instead of `<owner>/MonkeyMode` (`/plugin marketplace add ./MonkeyMode`), or try it for one session without installing: `claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity`.

**Plugin settings** (asked when you enable `mm-core`, changeable under `/plugin` → MonkeyMode core → configure, or `claude plugin configure mm-core@monkeymode`):

| Setting | Choices | Meaning |
|---|---|---|
| `coding_level` | I can read code / I can't read code | How agents verify and explain their work |
| `uses_chatgpt` | yes / no | Whether concept art comes as ChatGPT prompts |

### Requirements

| Tool | Needed for |
|---|---|
| Claude Code v2.1.271+ | plugin settings with fixed choices |
| Python 3.11+ and [`uv`](https://docs.astral.sh/uv/) | workflow scripts, guardrails, the setup script |
| PowerShell 7 (`pwsh`) | the `.ps1` tools (screenshots, multi-instance launch, Unity batch scripts) |
| Node.js 18+ | the local concept gallery and decision page |
| Git | everything; Git LFS for large binary assets |

### Other agents (Codex and anything that reads `AGENTS.md`)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

The same questions are asked in the terminal; skills are copied to `<your game>/.agents/skills/`. The after-edit hook is Claude Code only; other agents rely on the pre-commit hook and on running the guardrail check as `AGENTS.md` tells them to.

## 3. Set up a project with /mm-setup

Open your game's folder and run `/mm-setup`. It interviews you, then a script installs the files. Questions already answered by your plugin settings or by an earlier run are skipped; it tells you which answers it reused.

| # | Question | What the answer changes |
|---|---|---|
| 1 | Can you read code? *(skipped if set in plugin settings)* | "I can't" forces strict guardrails and plain-language, self-verifying agents; question 8 is never asked |
| 2 | Engine: Godot / Unity / Unreal / Bevy / Other *(detected engine pre-selected)* | Installs that engine's adapter; "Other" installs a fill-in template |
| 3 | Do you also use ChatGPT? *(skipped if set)* | Yes: concept art arrives as paste-ready ChatGPT prompts. No: Codex CLI or alternatives |
| 4 | Solo or team? | Team adds branch and pull request rules and a review checklist |
| 5 | Genre, target platforms (PC / mobile / web / console) | Recorded in `AGENTS.md` and the config |
| 6 | Multiplayer? (and max players) | Yes adds the networking guides and networked-only guardrails |
| 7 | Stage: idea / planning / building / polishing | Picks the recommended first skill |
| 8 | Guardrail level: strict / standard / relaxed *(only if you read code)* | How hard the guardrails push back (section 5) |
| 9 | Docs folder (default `docs/`) | Where all MonkeyMode docs go |

What you get:

```
AGENTS.md            MonkeyMode section between <!-- monkeymode:start/end --> markers
CLAUDE.md            @AGENTS.md
.monkeymode/         config.json: your project answers (read by every mm- skill)
_mm/                 workflow runtime: config, skill catalog, scripts, custom/ overrides
docs/ai/             agent operating docs (01-15)
docs/engine/         engine adapter docs
docs/project/        your approved design, filled over time
docs/work/           work records and handoffs
guardrails/          secrets.json + <engine>.json
tools/               guardrail checker and verification tools
.githooks/           optional pre-commit check
```

**Running it again** shows your current answers and asks what to change. Only the MonkeyMode section of `AGENTS.md`, the `@AGENTS.md` line in `CLAUDE.md`, `.monkeymode/config.json` and the guardrail profiles are updated; your own edits elsewhere are kept. In guardrail profiles, rules you added yourself are kept too.

## 4. The end-to-end process

Ask `/mm-help` at any point; it looks at what exists and tells you the next step. Drafts go to `_mm-output/`; when you approve a decision, the agent writes it into `docs/project/` as current fact. Progress notes and handoffs go to `docs/work/`.

| Step | Run | Produces (default locations; skills report the exact path) | Notes |
|---|---|---|---|
| 1. Idea | `mm-brainstorm-game` | `_mm-output/brainstorming-session-<date>.md` | Game-specific techniques on top of `mm-brainstorming`. `mm-research` for market or technical research |
| 2. Brief | `mm-create-game-brief` | a game brief in `_mm-output/` | Core fantasy, audience, hook, references, scope |
| 3. Design | `mm-gdd` | `_mm-output/planning-artifacts/gdds/<name>/gdd.md`, `epics.md`, `decision-log.md` | Express or facilitative. Numbers are assumptions until playtested |
| 3b. Story | `mm-create-narrative` | `_mm-output/narrative-design.md` | For story-driven games; finalize the GDD after it |
| 3c. UX | `mm-ux` | UX design and experience docs in `_mm-output/planning-artifacts/` | Camera, controls, HUD and screens are decided here |
| 4. Architecture | `mm-game-architecture` | `game-architecture.md` in `_mm-output/` | Reads `docs/engine/architecture-addendum.md`; keeps undecided tech behind interfaces; ends with guardrail proposals; offers an independent review |
| 4b. Guardrails | you approve the proposals | new rules in `guardrails/<engine>.json` | Agents never change guardrails on their own |
| 4c. Context | `mm-generate-project-context` | `_mm-output/project-context.md` | The short rule sheet agents follow while coding |
| 5. Epics and stories | `mm-create-epics-and-stories`, then `mm-check-implementation-readiness` | `_mm-output/planning-artifacts/epics.md`, `implementation-readiness-report-<date>.md` | Each story carries a risk level, a verification level and, for networked work, a multiplayer grade |
| 6. Sprint | `mm-sprint-planning`, `mm-sprint-status` | `_mm-output/implementation-artifacts/sprint-status.yaml` | |
| 7. Dev story | `mm-create-story` → `mm-dev-story` | a story file in `_mm-output/implementation-artifacts/`, code, tests | Runs the pre-commit procedure and the four-part report before "done" |
| 8. Review | `mm-code-review` | review findings, follow-up tasks | Checks against the guardrails and, for teams, the review checklist |
| 9. Playtest | `mm-playtest-plan`, `mm-performance-test` | `_mm-output/playtest-plan.md`, a performance test plan | Feel and visuals need your approval; automated checks are not enough |
| 10. Retro | `mm-retrospective` | `_mm-output/implementation-artifacts/epic-<n>-retro-<date>.md` | After each epic |

**Shortcuts:** `mm-quick-dev` for small changes without the full chain; `mm-correct-course` when a sprint goes off track; `mm-document-project` to describe an existing codebase before working on it; `mm-investigate` for debugging; `mm-walkthrough` for a guided tour of a change; `mm-write-handoff` when you stop mid-task.

**Tests:** `mm-test-framework` sets up a test framework for your engine, `mm-test-design` plans coverage, `mm-test-automate` and `mm-e2e-scaffold` write tests, `mm-test-review` checks them.

### How "done" works

Every story is reported in four parts: what changed, what it can affect, how it was verified (with evidence), and follow-ups or guardrail proposals. Verification uses levels L1 (static checks), L2 (the behavior observed), L3 (integration, with several players connected for multiplayer, grades M0-M3). Anything not checked is written as `unverified`, never as done.

## 5. Guardrails and hooks

Guardrails are rule files in `guardrails/` checked by `tools/guardrails/check.py`:

- `secrets.json` (every engine): API keys, tokens, private keys, credential assignments, absolute paths into someone's home folder.
- `<engine>.json`: the engine's tricky APIs, each with a message saying what is banned, why, and what to use instead.

They run in three places:

| When | How | Applies to |
|---|---|---|
| After every edit (Claude Code) | `mm-core`'s PostToolUse hook | the file just edited |
| Before every commit (optional) | `.githooks/pre-commit` (`git config core.hooksPath .githooks`) | staged files |
| On demand | `uv run tools/guardrails/check.py --all` | the whole project |

Behavior by level:

| Level | Who gets it | After-edit hook |
|---|---|---|
| **strict** | Everyone who doesn't read code (forced); others by choice | Every rule blocks the edit and the agent must fix the cause, including the no-comment rule where the engine profile has it (Unity) |
| **standard** | Default for people who read code | Rules block; comments allowed |
| **relaxed** | By choice | Rule hits are shown to the agent as warnings; nothing blocks |

Agents are told never to work around a guardrail (editing the rule, adding an allowlist entry, `--no-verify`). If a rule is wrong, they stop and ask you.

**Coding level changes more than guardrails.** For "I can't read code", every agent must run tests, the build or the game itself before reporting done, explain results in plain words and screenshots instead of code, and ask before deleting or moving files, large refactors, installing packages, committing or pushing. For "I can read code", reports come as a diff summary with the reason for each change.

## 6. Images and concept art

Install `mm-art-tools`, then ask for concepts ("make three character concepts for the shopkeeper"). `mm-concept-art` reads `uses_chatgpt` from the project config:

**With ChatGPT (recommended):**

1. The agent reads your art direction from `docs/project/` and writes one paste-ready prompt per concept (subject, composition, style, background, aspect ratio), plus a request for variations.
2. You paste them into ChatGPT and save the images as `.agent-output/concepts/<date>/<name>.png`.
3. You tell the agent; it checks them against the art direction and shows them in the local gallery (`pwsh tools/Start-ConceptServer.ps1`, then `http://localhost:5090/`).
4. To choose between versions, `mm-decision-picker` puts them on a page where you click your choice; the agent reads it from there.
5. Adopted images are recorded with the tool and its terms in `docs/licenses/ASSET_REGISTRY.md`.

**Without ChatGPT:** the agent uses the Codex CLI if it is installed, or offers Blender blockouts (`mm-cli-blender`), free asset libraries with clear licenses (CC0 sources such as Poly Haven, Kenney, ambientCG), or the same prompts for another generator.

Concepts are never final until you approve them. Purchased-asset files, other people's work, brands and personal information never go into prompts.

## 7. Engine notes

Each adapter installs into `docs/engine/` with the same seven docs: README, project context (fill it in), architecture addendum, guardrails, build and test, multiplayer, version control.

| Engine | Highlights | Checked against |
|---|---|---|
| **Unity** | No scene-wide `Find*`, `Resources.Load`, `async void`, tween libraries or direct `Debug.Log`; assembly dependency rules (`.asmdef`); batch-mode test and build scripts; Mirror and Netcode for GameObjects notes; asset import checklist | Field-tested in a Unity 6 + Mirror project |
| **Godot** | Call down, signal up: no `../` or `/root/` node paths, no `find_child` at runtime, no string-name `connect`/`call`/`rpc`; typed GDScript; resources are shared until duplicated; `@rpc("any_peer")` validates the sender; headless import, GUT and gdUnit4 commands | Godot 4.7 docs |
| **Unreal** | No raw `new`/`delete` of UObjects; `UPROPERTY() TObjectPtr<>` members; no world-wide actor searches or synchronous loads at runtime; per-module log categories; Server RPCs on owned actors with validation; `Automation RunTest` from the command line; LFS and locks for `.uasset`/`.umap` | Unreal Engine 5.9 docs (partly) |
| **Bevy** | Systems never block; explicit system ordering; simulation in `FixedUpdate`; buffered events are `Message`s since 0.17; logs via `info!`/`warn!`; Clippy `disallowed-methods`; lightyear, bevy_replicon, bevy_renet options | Bevy 0.20 docs |

Anything an adapter could not confirm is marked *needs verification* in its docs. Single-player games skip the multiplayer doc and the networked-only rules.

## 8. Customizing

- **Project rules:** edit `AGENTS.md` outside the MonkeyMode markers, and anything in `docs/ai/`, `docs/engine/` and `docs/project/`. These override skill instructions.
- **Skill behavior:** add `_mm/custom/<skill>.toml` (team, committed) or `<skill>.user.toml` (personal). Arrays such as `persistent_facts` append to the skill's defaults, scalars replace them. `/mm-customize` walks you through it.
- **Guardrails:** add rules to `guardrails/<engine>.json`, or a new `guardrails/<name>.json` profile. Format: `docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md`. Test each rule with one bad and one good example.
- **Undecided items:** list them in the Undecided section of `AGENTS.md`; agents will offer options instead of deciding.

## 9. FAQ and troubleshooting

**`/mm-setup` says the engine adapter is missing.** Install the engine plugin (`/plugin install mm-<engine>@monkeymode`) and run `/mm-setup` again, or answer "Other".

**A skill says `.monkeymode/config.json` is missing.** Run `/mm-setup`. Until then skills ask what they need.

**The guardrail hook blocks an edit I want.** Read the message: it says why the pattern breaks and what to use instead. If the rule really is wrong for your project, change or remove it yourself in `guardrails/` (agents are not allowed to), or choose the relaxed level by re-running `/mm-setup`.

**`uv: command not found` in hook output.** Install `uv` (`pip install uv`, or the installer at docs.astral.sh/uv). The hook and the workflow scripts need it.

**Hooks don't run before commits.** Enable them once per clone: `git config core.hooksPath .githooks`.

**My plugin setting seems ignored.** Restart Claude Code after changing plugin settings. The project config (`.monkeymode/config.json`) wins over plugin settings; run `/mm-setup` to change it.

**Unity batch-mode tests fail immediately.** The Unity editor probably has the project open (project lock). Close it, or run the tests in the editor's Test Runner.

**I use another engine.** Choose "Other" in `/mm-setup` and fill in `docs/engine/README.md`; add a guardrail profile for your language. Contributions of new adapters are welcome (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

**Can I use MonkeyMode without Claude Code?** Yes: see section 2, "Other agents".

**Does MonkeyMode send my project anywhere?** No. Everything runs locally. Prompts you paste into ChatGPT or other services are your choice; the asset policy (`docs/ai/07`) tells agents what must never be sent.
