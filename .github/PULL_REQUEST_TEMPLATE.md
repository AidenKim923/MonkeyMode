## What and why

<!-- What this changes and the problem it solves. Link the issue if there is one. -->

## How it was verified

<!-- Commands you ran and their results. For guardrail rules: the violating and passing examples. For engine statements: the official doc link. -->

## Checklist

- [ ] Skill names use the `mm-` prefix; folder name matches `name:`
- [ ] No reference outside the plugin's own folder
- [ ] English text (translations only in `README.<lang>.md`); no project-specific names, personal paths or secrets
- [ ] New guardrail rules come with a violating and a passing example I ran
- [ ] Engine statements are verified against official docs or marked *needs verification*
- [ ] `claude plugin validate` passes for the marketplace and every changed plugin (`--strict`)
- [ ] Script tests pass; `uv run tools/scrub.py` passes
- [ ] Docs updated (README and translations if the structure changed, GUIDE, INVENTORY, ONBOARDING)
- [ ] Changes to adapted third-party files are listed in `THIRD_PARTY_NOTICES.md`
