# MonkeyMode

> **I'm Monkey Game Developer 🐒**
>
> Even a not-so-smart agent (or dev) gets smart when it runs with MonkeyMode.

MonkeyMode is an open-source game-dev kit for AI coding agents. It gives an agent a tested way to work on a game: a design-to-ship workflow (brief → GDD → architecture → stories → dev → review → playtest), rules that make it verify its own work instead of claiming success, guardrails that block the mistakes agents keep making in game code, and per-engine knowledge for **Godot, Unity, Unreal and Bevy**.

It was extracted from a real Unity + Mirror co-op project and generalized. It ships as a Claude Code plugin marketplace and also works for agents that read `AGENTS.md` (Codex and others).

## What's inside

| Plugin | What you get |
|---|---|
| **`mm-core`** (required) | 42 `mm-` workflow skills (game brief, GDD, narrative, UX, architecture, epics and stories, dev story, code review, sprint planning and status, playtest plan, performance and test design, retrospective, research, quick dev, review, help, ...), `mm-setup` onboarding, agent operating docs (`docs/ai/`: execution policy, verification playbook, network authority, handoff, pre-commit procedure, guardrails, ...), the guardrail checker with an after-edit hook, a secrets/personal-path profile, a concept gallery and decision page |
| **`mm-unity`** | C# banned APIs, assembly direction rules, batch-mode test/build scripts, Mirror and Netcode notes, asset import checklist. *Field-tested* |
| **`mm-godot`** | GDScript node path and signal rules, headless test commands, high-level multiplayer notes. *Checked against the Godot 4.7 docs* |
| **`mm-unreal`** | UObject/GC rules, banned C++ patterns, UBT and automation-test commands, replication notes. *Partly checked against the Unreal Engine 5.9 docs* |
| **`mm-bevy`** | No blocking in systems, system ordering, Clippy bans, cargo test commands, lightyear/replicon/renet notes. *Checked against Bevy 0.20* |
| `mm-agents` (optional) | Persona agents (game designer, architect, developer, solo dev, tech writer, analyst, PM, UX designer) and party mode |
| `mm-art-tools` (optional) | `mm-concept-art` (ChatGPT prompts, Codex CLI, or alternatives) and CLI harnesses for Blender, RenderDoc, Nsight Graphics |

### Shared vs. per engine

| Shared (mm-core) | Per engine (mm-&lt;engine&gt;) |
|---|---|
| Workflow templates: game brief, GDD, narrative, UX, PRD, architecture, epics/stories, story, playtest plan, performance test plan, test design, code review checklist, retrospective, decision log, project context | Project-context template |
| Agent behavior, verification, handoff, scope control, git hygiene, team workflow | Architecture addendum (scene/asset structure; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Guardrail checker, after-edit and pre-commit hooks, secrets profile | Engine guardrail profile and banned patterns |
| Self-verification tools (logs, screenshots, multi-instance launch) | Build and test commands (Unity also ships scripts) |
| Engine-neutral network authority rules and test grades | Multiplayer notes (Mirror/NGO, replication, high-level multiplayer, lightyear/renet) |
| Asset and character pipeline guides | `.gitignore` / LFS hints, asset import (Unity) |

The full list of what came from where is in [`docs/INVENTORY.md`](docs/INVENTORY.md).

## Install (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Optional packs: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Requirements: Claude Code v2.1.271 or later (plugin settings with fixed choices), Python 3.11+ and [`uv`](https://docs.astral.sh/uv/) (workflow scripts and guardrails), PowerShell 7 for the `.ps1` tools, Node.js 18+ for the local concept/decision page.

When you enable `mm-core`, Claude Code asks two questions about you (you can change them later under `/plugin` → MonkeyMode core → configure):

| Setting | Choices | Default |
|---|---|---|
| `coding_level` | I can read code / I can't read code | I can't read code |
| `uses_chatgpt` | yes / no ("For images we recommend ChatGPT") | yes |

## Quick start

1. Open your game project in Claude Code and run **`/mm-setup`**. It asks about the engine, solo or team, genre and platforms, multiplayer, your project stage, guardrail level (only if you read code) and the docs folder, then installs everything and tells you the next step. The full branching flow is in [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Run the skill it recommends, for example `/mm-brainstorm-game` for a fresh idea or `/mm-document-project` for an existing codebase.
3. Ask `/mm-help` whenever you are unsure what comes next.

What lands in your project:

```
AGENTS.md            MonkeyMode section (rules, your answers, engine snippet)
CLAUDE.md            @AGENTS.md
.monkeymode/         config.json (your project answers)
_mm/                 workflow runtime: config, catalog, scripts, custom/ overrides
docs/ai/             agent operating docs
docs/engine/         engine adapter docs
docs/project/        your approved design (filled over time)
docs/work/           work records and handoffs
guardrails/          secrets.json + <engine>.json
tools/               guardrail checker, verification tools
.githooks/           optional pre-commit guardrails
```

## Without Claude Code (AGENTS.md agents)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

This asks the same questions, installs the same files, and copies the skills to `.agents/skills/`. See [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Customizing

- Project rules: edit `AGENTS.md` (outside the MonkeyMode markers), `docs/ai/` and `docs/engine/` in your project. They override skill instructions.
- Skill behavior: put overrides in `_mm/custom/<skill-name>.toml` (team) or `<skill-name>.user.toml` (personal). Arrays such as `persistent_facts` append to the skill's defaults. `/mm-customize` walks you through it.
- Guardrails: add rules to `guardrails/<engine>.json` or a new `guardrails/<name>.json` profile (format in `docs/ai/12`). Change them only on purpose; agents are told never to loosen them on their own.

## Testing the install

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

The last command starts Claude Code with the plugins loaded for one session, without adding the marketplace.

## Credits and license

MonkeyMode is MIT-licensed ([LICENSE](LICENSE)). Its workflow skills are based on [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) and the BMad Game Dev Studio module (MIT), and the graphics-tool skills on [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). MonkeyMode is independent and not endorsed by their authors. Details and every modification: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Corrections to the Godot, Unreal and Bevy adapters are especially welcome: they were checked against the official docs but not yet used in a real project, and the items still open are marked *needs verification* in each adapter.
