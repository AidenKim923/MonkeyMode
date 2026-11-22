# Third-party notices

MonkeyMode is MIT-licensed (see [LICENSE](LICENSE)). It includes adapted work from the projects below, which keep their own licenses. Each license text is in [`licenses/`](licenses/), and every plugin folder carries a copy of `LICENSE`, `NOTICE` and `licenses/` so an installed plugin stays compliant on its own.

| Component | Version | License | Upstream | Adapted into |
|---|---|---|---|---|
| BMad Method (core + BMM) | 6.12.4 | MIT, Copyright (c) 2025 BMad Code, LLC | https://github.com/bmad-code-org/BMAD-METHOD | workflow skills in `plugins/mm-core/skills/`, persona skills in `plugins/mm-agents/skills/`, runtime scripts in `plugins/mm-core/template/_mm/scripts/`, catalog `plugins/mm-core/template/_mm/_config/mm-help.csv`, agent descriptors in `plugins/mm-core/template/_mm/config.toml` |
| BMad Game Dev Studio | 0.7.2 (sha `2486f5f`) | MIT, Copyright (c) 2026 BMad Code, LLC | https://github.com/bmad-code-org/bmad-module-game-dev-studio | game workflow, testing and agent skills in `plugins/mm-core/skills/` and `plugins/mm-agents/skills/` |
| CLI-Anything skills | upstream `main` at time of import | Apache-2.0 | https://github.com/HKUDS/CLI-Anything | `plugins/mm-art-tools/skills/mm-cli-blender`, `mm-cli-renderdoc`, `mm-cli-nsight-graphics` |

The upstream skills as imported are preserved in this repository's history (first commit after `chore: init`), so every change below can be diffed.

## Trademarks

BMad™, BMad Method™, BMad Core™ and BMad Code™ are trademarks of BMad Code, LLC ([guidelines](licenses/BMAD-TRADEMARK.md)). MonkeyMode is an independent project, not affiliated with or endorsed by BMad Code, LLC, and does not use BMad as a product, skill or plugin name.

## Modifications

### BMad Method and Game Dev Studio

1. **Renamed** every skill to the `mm-` prefix. The full old-to-new map, including merges, is in [`docs/INVENTORY.md`](docs/INVENTORY.md#skill-name-map).
2. **Merged** skills where a generic BMad Method skill and a Game Dev Studio skill did the same job: the Game Dev Studio version was kept and references to the dropped one were pointed at it (for example code review, correct course, epics and stories, PRD, UX, architecture, retrospective, sprint planning, quick dev, project context, product/game brief, developer and architect personas).
3. **Rebranded** product wording: "BMad", "BMad Method", "BMM", "Game Dev Studio" and "GDS" in skill text became "MonkeyMode"; module IDs `core`/`bmm`/`gds` became one module `mm`.
4. **Moved the runtime**: `{project-root}/_bmad/` became `{project-root}/_mm/`, `_bmad-output/` became `_mm-output/`, and the three module config files (`_bmad/{core,bmm,gds}/config.yaml`) became one `_mm/config.yaml`. The scripts in `_mm/scripts/` look for `_mm/` instead of `_bmad/`. The help catalog was merged into `_mm/_config/mm-help.csv` (rows of dropped skills and documentation `_meta` rows removed). The render directive `[[bmad-snapshot:...]]` became `[[mm-snapshot:...]]`.
5. **Tuned defaults**: `customize.toml` of 22 workflow and persona skills now ships MonkeyMode `persistent_facts` (and one `activation_steps_append` for architecture review) pointing at the project's `AGENTS.md`, `docs/ai/` and `.monkeymode/config.json`. The "DO NOT EDIT" header was replaced with a note on where to override.
6. **Links removed**: links to upstream documentation sites and mentions of upstream-only tools (module builder, TEA module) were replaced with neutral wording.
7. `mm-review/scripts/word_metrics.py`: the `CJK` regex character class is written with `\uXXXX` escapes instead of literal characters. Behavior is unchanged.
8. **Subagents in the help catalog**: `_mm/_config/mm-help.csv` has added rows with module `Agents` for the MonkeyMode Claude Code subagents (MonkeyMode's own work), and `mm-help/SKILL.md` has an added paragraph on how to recommend and call them.

All bundled Python tests (`scripts/tests/`) pass after these changes.

### CLI-Anything

Only the `name:` field in each `SKILL.md` frontmatter changed (`cli-anything-<tool>` → `mm-cli-<tool>`). The body, including the real CLI command names (`cli-anything-blender` and so on), is unchanged. Apache-2.0 section 4: the upstream repository ships no NOTICE file; the license text is included and this section states the change.
