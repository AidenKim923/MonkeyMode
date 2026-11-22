# Asset and data policy

> What must not leave the machine, which licenses must be honored, and when AI-generated assets count as approved.

## 1. What may go into external AI tools and services

| Level | Content |
|---|---|
| Fine | Code and design docs you wrote, public API usage, general technical questions |
| Careful | Teammates' code (check with them first), unreleased story and level design |
| Never | Source code, models or textures of purchased assets; account details; API keys; personal information |

Treat any prompt or image sent to an external service (model generation APIs and the like) as published, and follow the table above.

## 2. Purchased and third-party assets

Do not upload original files of purchased assets to external AI. Many EULAs forbid redistribution, and whether an upload counts as redistribution is debatable, so take the safe side.

- Usage questions → quote official docs or mention API names only
- Errors → only the error message and your own calling code
- Integration → only your own wrapper code

Do not edit third-party originals (engine plugins, networking libraries, store assets) directly; that needs prior approval.

## 3. License tracking

Record every third-party asset, package, font or sound in the asset registry ([`docs/licenses/ASSET_REGISTRY.md`](../licenses/ASSET_REGISTRY.md)).

```markdown
| Asset | Author | Source | License | Commercial use | Acquired |
|---|---|---|---|---|---|
```

**"Free" and "commercial use allowed" are different.** Read the license text. Watch especially: CC models from Sketchfab and similar sites, free fonts, sound and music packs.

### AI-generated assets

When you use AI output (generative modeling, image or audio generation):

- Record the tool used and its commercial-use terms in the registry
- Do not put other people's works or brands into generation inputs (prompts, reference images)
- Final concept art and gameplay quality are **approved by a human**

## 4. Keep art source files out of the repository

Large working files (`.blend`, texture sources, bake scripts) live outside the engine project and are not committed. Add the source folder to `.gitignore` the first time you create it.

| | |
|---|---|
| Why | Large sources blow past repository limits quickly, and a committed file stays in history even after you remove it |
| What goes into the game | Imported results (.fbx/.glb/.gltf and so on) inside the engine project are committed |
| Source storage | `<decide and write it here>` |

If you do commit binaries, use Git LFS as described in `docs/engine/version-control.md`.

## 5. Never in code

- Personal account details, email addresses
- API keys, tokens
- Absolute local paths (`C:/Users/<name>/...`, `/home/<name>/...`)
- Hard-coded test IP addresses

Put sensitive settings in git-ignored files (`.env`, `*.local`). The core guardrail profile `guardrails/secrets.json` catches the common cases.

## 6. Screenshots and video

Before attaching to an issue or a presentation, check: other windows' content, real names in paths, notification pop-ups.

## 7. If something leaked

1. Stop sending anything further, immediately
2. Report what went out, when and where, separating facts from guesses
3. If it reached commit history, talk to the user (never rewrite history alone)
4. If it is a key or token, revoke it and issue a new one right away
