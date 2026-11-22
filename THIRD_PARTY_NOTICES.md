# Third-party notices

MonkeyMode is MIT-licensed (see [LICENSE](LICENSE)). It redistributes the components below under their own licenses. Each license text is in [`licenses/`](licenses/).

| Component | Version | License | Upstream | Where in this repo |
|---|---|---|---|---|
| BMad Method (core + BMM) | 6.12.4 | MIT, Copyright (c) 2025 BMad Code, LLC | https://github.com/bmad-code-org/BMAD-METHOD | `skills/bmad-*`, `skills/monkeymode-init/template/_bmad/scripts/`, `.../_bmad/_config/bmad-help.csv`, `.../_bmad/core/module-help.csv`, `.../_bmad/bmm/module-help.csv`, agent descriptors in `.../_bmad/config.toml` |
| BMad Game Dev Studio | 0.7.2 (sha `2486f5f`) | MIT, Copyright (c) 2026 BMad Code, LLC | https://github.com/bmad-code-org/bmad-module-game-dev-studio | `skills/gds-*`, `.../_bmad/gds/module-help.csv` |
| CLI-Anything skills | upstream `main` at time of import | Apache-2.0 | https://github.com/HKUDS/CLI-Anything | `skills/cli-anything-blender`, `skills/cli-anything-renderdoc`, `skills/cli-anything-nsight-graphics` |

## Trademarks

BMad™, BMad Method™, BMad Core™ and BMad Code™ are trademarks of BMad Code, LLC ([guidelines](licenses/BMAD-TRADEMARK.md)). MonkeyMode is an independent project, not affiliated with or endorsed by BMad Code, LLC. The `bmad-*` and `gds-*` skill IDs are kept unchanged so the bundled workflows keep working and so their origin stays obvious; MonkeyMode does not use BMad as its product name.

## Modifications

The bundled skill files are byte-identical to the upstream release, with these exceptions:

| File | Change | Why |
|---|---|---|
| `skills/bmad-review/scripts/word_metrics.py` | The `CJK` regex character class is written with `\uXXXX` escapes instead of literal characters. Behavior is unchanged. | Keeps the repository free of non-English literal text so the release scrub stays meaningful. |

MonkeyMode's own tuning of BMad is **additive**: it lives in override files (`skills/monkeymode-init/template/_bmad/custom/*.toml`) that BMad's own customization resolver merges over the stock `customize.toml` files. The `_bmad/config.toml` and module `config.yaml` files in the template are MonkeyMode-written equivalents of what the BMad installer generates, with placeholders instead of install answers.

The CLI-Anything skills are unmodified. Apache-2.0 section 4: no NOTICE file ships with the upstream repository; the license text is included.
