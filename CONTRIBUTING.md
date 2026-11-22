# Contributing to MonkeyMode

Thanks for helping. MonkeyMode is a Claude Code plugin marketplace plus a setup script for other agents. Read [AGENTS.md](AGENTS.md) for the repository rules (agents working on this repo follow them too) and [docs/INVENTORY.md](docs/INVENTORY.md) for where things came from.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ground rules

1. **Every plugin is self-contained.** Claude Code installs a plugin folder on its own; nothing in `plugins/<plugin>/` may reference files outside it.
2. **Every skill name starts with `mm-`.**
3. **English everywhere**, except the translated `README.<lang>.md` files.
4. **No project-specific content**: no game names, people, accounts, absolute personal paths, keys or server addresses. Use placeholders (`<YourGame>`, `<AssemblyPrefix>`); `setup_project.py` fills them.
5. **Engine-specific content lives in an engine adapter**, never in the shared `docs/ai/`.
6. **Third-party content keeps its license.** Record every change to adapted files in `THIRD_PARTY_NOTICES.md`.

## Repository layout

| Path | What |
|---|---|
| `.claude-plugin/marketplace.json` | The `monkeymode` marketplace |
| `plugins/mm-core/skills/` | Engine-agnostic skills, including `mm-setup` |
| `plugins/mm-core/template/` | Files `mm-setup` installs into game projects |
| `plugins/mm-core/hooks/hooks.json` | The after-edit guardrail hook |
| `plugins/mm-<engine>/adapter/` | An engine adapter |
| `plugins/mm-agents/`, `plugins/mm-art-tools/` | Optional packs |
| `tools/scrub.py` | Release scrub (language, names, paths, secrets) |

## Adding a skill

1. Pick the plugin: `mm-core` for engine-agnostic workflow, an engine plugin for engine-only skills, a pack for optional tooling.
2. Create `plugins/<plugin>/skills/mm-<name>/SKILL.md`:

   ```markdown
   ---
   name: mm-<name>
   description: What it does and when to use it, with the phrases a user would actually say. This is what the agent matches on.
   ---

   # Title

   Steps the agent follows. Point at project files by their project path (docs/ai/..., docs/engine/...).
   Read .monkeymode/config.json and adapt to coding_level; if the file is missing, ask or suggest mm-setup.
   ```

   The folder name and `name:` must match. Keep supporting files (templates, references, scripts) inside the skill folder and refer to them by relative path. `${CLAUDE_PLUGIN_ROOT}` is substituted in skill text when loaded as a plugin; also say what to do when it is not (agents without plugins).
3. **Workflow skills** that should be customizable per project also get a `customize.toml` with a `[workflow]` (or `[agent]`) table. Arrays (`persistent_facts`, `activation_steps_prepend`, `activation_steps_append`) append to defaults when a project overrides them in `_mm/custom/<skill>.toml`; scalars replace. Start `persistent_facts` with the two MonkeyMode facts every workflow carries (AGENTS.md precedence, the coding-level behavior); copy them from an existing skill such as `mm-dev-story`.
4. If the skill belongs in the workflow order, add a row to `plugins/mm-core/template/_mm/_config/mm-help.csv` (phase, `preceded-by`, `followed-by`, outputs) and to `docs/ai/14_GAME_DEV_WORKFLOW.md`.
5. Scripts go in `scripts/` with tests in `scripts/tests/` (standard-library Python, PEP 723 header, runnable with `uv run`).
6. Update the skill counts and tables in `README.md`, `docs/GUIDE.md` and `docs/INVENTORY.md` if they change.

## Adding an engine adapter

Copy an existing adapter (`plugins/mm-godot` is a good template) to `plugins/mm-<engine>/` and keep the same shape:

```
plugins/mm-<engine>/
  .claude-plugin/plugin.json     name, version, description, "dependencies": ["mm-core"]
  skills/mm-<engine>/SKILL.md    prints the adapter path; when to read which doc
  adapter/
    adapter.json                 name, detect markers, verification status, multiplayerOnlyRules
    AGENTS.snippet.md            the short rule list inserted into AGENTS.md
    docs/                        README, project-context, architecture-addendum, guardrails,
                                 build-and-test, multiplayer, version-control
    guardrails/<engine>.json     banned-pattern profile
    gitignore, gitattributes     lines appended to the project's files (LFS lines commented out)
    tools/                       optional engine scripts copied into the project's tools/
  LICENSE  NOTICE  THIRD_PARTY_NOTICES.md  licenses/
```

Then:

- Add detection to `detect_engine()` and the engine name to `ENGINES` in `plugins/mm-core/skills/mm-setup/scripts/setup_project.py`, and to the choice lists in `mm-setup/SKILL.md` and `docs/ONBOARDING.md`.
- Add the plugin to `.claude-plugin/marketplace.json`.
- Say how well it is verified: `adapter.json` `verification` (`field-tested`, `docs-checked`, `partly-docs-checked`), and mark every statement you could not confirm in official docs as *needs verification*.
- Run a setup into a throwaway project for the new engine (see Tests).

## Adding guardrail rules

Rules live in a profile (`guardrails/<name>.json`; format in `plugins/mm-core/template/docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md`). Each rule has an `id`, a regex `pattern`, a `message` and optional `excludePaths` and `extensions`.

- The message must say **what** is banned, **why** it breaks, **what to use instead**, and where it is documented. Agents follow the message, so a vague one gets worked around.
- Patterns run on code with comments and string literals blanked out (set `"stripLiterals": false` when the rule must see strings).
- Rules that only matter for networked games go in `multiplayerOnlyRules` in `adapter.json`, so single-player projects do not get them.
- **Test every rule with one violating and one passing example** before shipping:

  ```
  mkdir -p /tmp/gt/guardrails && cp plugins/mm-<engine>/adapter/guardrails/<engine>.json /tmp/gt/guardrails/
  # write bad and good example files under the profile's scopeRoot, then:
  uv run plugins/mm-core/template/tools/guardrails/check.py --root /tmp/gt --all
  ```

- Document the rule in the adapter's `docs/guardrails.md` with its evidence (source, knowledge or judgment).

## Tests and checks

Run all of these before opening a pull request:

```
claude plugin validate .
for p in plugins/*; do claude plugin validate "$p" --strict; done
for t in plugins/*/skills/*/scripts/tests; do (cd "$(dirname "$t")" && uv run --with pytest python -m pytest -q tests); done
uv run tools/scrub.py
```

Setup smoke test (any engine, into an empty temporary folder):

```
uv run plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <temp dir> --apply \
  --set engine=godot --set coding_level=can-read-code --set uses_chatgpt=no --set team=solo \
  --set multiplayer=no --set stage=idea --set guardrail_level=standard
```

Try it in Claude Code without installing: `claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-<engine>`, then `/mm-setup` in a sample project. To test the marketplace install without touching your own settings, point `CLAUDE_CONFIG_DIR` at a temporary folder and run `claude plugin marketplace add <path to this repo>` and `claude plugin install mm-<engine>@monkeymode`.

## Keeping license files in sync

The root `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` and `licenses/` are copied into every plugin. After changing them:

```
for p in plugins/*; do cp LICENSE NOTICE THIRD_PARTY_NOTICES.md "$p"/; cp licenses/* "$p"/licenses/; done
```

## Pull request checklist

- [ ] Skill names use the `mm-` prefix; folder name matches `name:`
- [ ] No reference outside the plugin's own folder
- [ ] English text (translations only in `README.<lang>.md`); no project-specific names, personal paths or secrets
- [ ] New guardrail rules come with a violating and a passing example you ran
- [ ] Engine statements are verified against official docs or marked *needs verification*
- [ ] `claude plugin validate` passes for the marketplace and every changed plugin (`--strict`)
- [ ] Script tests pass; `uv run tools/scrub.py` passes
- [ ] Docs updated: README (and translations if the structure changed), GUIDE, INVENTORY, ONBOARDING as relevant
- [ ] Changes to adapted third-party files are listed in `THIRD_PARTY_NOTICES.md`
