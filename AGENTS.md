# AGENTS.md: MonkeyMode repository

This file is for agents working **on MonkeyMode itself**. To use MonkeyMode in a game project, see [README.md](README.md) and [docs/ONBOARDING.md](docs/ONBOARDING.md): the setup script writes a separate `AGENTS.md` into that project.

## Layout

| Path | What |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace `monkeymode` listing every plugin |
| `plugins/mm-core/` | Core plugin: `skills/` (all engine-agnostic `mm-` skills, including `mm-setup`), `template/` (files installed into game projects), `hooks/hooks.json` |
| `plugins/mm-<engine>/` | Engine plugin: `skills/mm-<engine>/` and `adapter/` (`adapter.json`, `AGENTS.snippet.md`, `docs/`, `guardrails/`, optional `tools/`, `gitignore`, `gitattributes`) |
| `plugins/mm-agents/`, `plugins/mm-art-tools/` | Optional packs |
| `docs/INVENTORY.md` | Provenance of every part and the skill name map |
| `docs/ONBOARDING.md` | The setup interview and what each answer changes |

## Rules

1. Every plugin must be self-contained: Claude Code installs a plugin folder on its own, so nothing may reference files outside it. Each plugin carries `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` and `licenses/`; keep them in sync with the root copies.
2. Every skill name starts with `mm-`. Upstream project names appear only in `NOTICE`, `THIRD_PARTY_NOTICES.md`, `licenses/`, the README credit (all languages) and the name map in `docs/INVENTORY.md`.
3. Everything is in English, except the translated `README.<lang>.md` files. No project-specific content: no game names, people, accounts, absolute personal paths, keys or server addresses. Placeholders use `<YourGame>`, `<AssemblyPrefix>` and the like; `setup_project.py` fills them.
4. Engine-specific content goes in the engine plugin's `adapter/`, never in `plugins/mm-core/template/docs/ai/`. Adapters keep the same shape: README, project-context, architecture-addendum, guardrails, build-and-test, multiplayer, version-control. Mark content you could not confirm in official docs as "needs community verification".
5. Guardrail rules need one violating and one passing example run before they ship (`uv run plugins/mm-core/template/tools/guardrails/check.py --root <test project> --all`).
6. Record every change to adapted upstream files in `THIRD_PARTY_NOTICES.md`.

## Checks before committing

```
claude plugin validate . && for p in plugins/*; do claude plugin validate "$p" --strict; done
uv run --with pytest python -m pytest -q plugins/*/skills/*/scripts/tests
uv run plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <empty temp folder> --set engine=other --set coding_level=can-read-code --set uses_chatgpt=no --set team=solo --set multiplayer=no --set stage=idea --set guardrail_level=standard --apply
```

Scrub before release: `uv run tools/scrub.py` (non-English text outside `README.<lang>.md`, upstream skill-name prefixes outside the attribution files, absolute personal paths, secrets).

Contributor guide: [CONTRIBUTING.md](CONTRIBUTING.md). User guide: [docs/GUIDE.md](docs/GUIDE.md).
