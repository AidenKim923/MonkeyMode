## What and why

<!-- What this changes and the problem it solves. Link the issue: "Closes #123". -->

## Type of change

- [ ] 🐛 Bug fix
- [ ] ✨ New or improved skill, tool or hook
- [ ] 🎮 Engine adapter correction or addition
- [ ] 🛡️ Guardrail rule
- [ ] 📚 Docs or translation
- [ ] 🔧 CI, tooling or repository maintenance

## Plugins touched

- [ ] `mm-core`
- [ ] `mm-unity`
- [ ] `mm-godot`
- [ ] `mm-unreal`
- [ ] `mm-bevy`
- [ ] `mm-agents`
- [ ] `mm-art-tools`
- [ ] None (repository files only)

## How it was verified

<!-- Commands you ran and their results. For guardrail rules: the violating and passing examples. For engine statements: the official doc link. -->

## Checklist

- [ ] `uv run tools/scrub.py` passes
- [ ] `claude plugin validate .` and `claude plugin validate plugins/<changed> --strict` pass (or `uv run tools/check_manifests.py` if you do not have the CLI)
- [ ] Script tests pass (`uv run --with pytest python -m pytest -q tests` in each changed `scripts/` folder)
- [ ] Skill names use the `mm-` prefix; folder name matches `name:`; no reference outside the plugin's own folder
- [ ] English text (translations only in `README.<lang>.md`); no project-specific names, personal paths or secrets
- [ ] New guardrail rules come with a violating and a passing example I ran
- [ ] Engine statements are checked against official docs or marked *needs verification*
- [ ] Docs updated as relevant: README, GUIDE, INVENTORY, ONBOARDING, CHANGELOG
- [ ] **Translations:** if README.md changed structurally, all 10 `README.<lang>.md` files are updated and `uv run tools/readme_parity.py` passes (or this PR says which translations still need updating)
- [ ] Changes to adapted third-party files are listed in `THIRD_PARTY_NOTICES.md`
