# Team git workflow

> Installed when `mm-setup` records a team project. Solo projects do not get this file.

## Branches

- One branch per task: `<type>/<short-topic>` (`feat/grab-objects`, `fix/door-desync`, `docs/gdd-update`). Never work directly on the main branch.
- Keep branches short-lived; rebase or merge the main branch in before opening a pull request (never rewrite shared history).
- Scenes/levels and binary assets are not mergeable: claim them before editing (LFS lock, or a note in the team channel) and say so in the pull request.

## Pull requests

- Agents open a pull request only when the user asks, after the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md).
- The description is the four-part [completion report](06_RESPONSE_STYLE_GUIDE.md): changes, impact, verification (with grades and player counts), follow-ups.
- Link the story or task. List edited scenes/levels and data assets explicitly.
- One topic per pull request. Unrelated cleanups go in their own.

## Review checklist

- [ ] The change matches the story's acceptance criteria; nothing outside its scope changed
- [ ] Guardrails and engine checks pass (`uv run tools/guardrails/check.py --all` and the engine commands in `docs/engine/build-and-test.md`)
- [ ] Tests cover the changed behavior; new tests were added where coverage was thin
- [ ] Networked changes: authority stays on the server, requests are validated, multi-client check at M2 recorded
- [ ] No tuning numbers in code; no secrets, personal paths or account data
- [ ] Shared scenes/levels and binary assets were edited by one person only
- [ ] Unverified items are labeled `unverified` with a reason
- [ ] Docs that state current facts were updated (`docs/project/`, `docs/engine/`), history went to `docs/work/`

Reviewers use `mm-code-review` for a structured pass; it reads this checklist through `AGENTS.md`.

## Ownership

If the team wants code owners, add a `CODEOWNERS` file and list owners per folder. Agents never edit `CODEOWNERS` or branch protection without approval.
