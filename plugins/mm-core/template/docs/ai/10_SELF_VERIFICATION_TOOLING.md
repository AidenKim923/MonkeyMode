# Self-verification tooling

> How an agent, after building a feature, runs **build → test → run → read logs → screenshot** on its own.
> Core tools are Python (run with `uv`) or PowerShell 7 scripts in `tools/`, so Claude Code, Codex and other agents use the same commands. Outputs collect in `.agent-output/` (git-ignored); log files go to `logs/{YYYY-MM-DD}/` (git-ignored).

## Core tools (every engine)

| Goal | Command | Exit codes |
|---|---|---|
| Guardrails (comments, banned APIs, secrets) | `uv run tools/guardrails/check.py --all`, `--staged`, or `<file>...` | 0 pass · 1 violation · 2 no config |
| Summarize log errors | `pwsh tools/Read-LogErrors.ps1 -LogPath <log>` | 0 · 1 errors found |
| Screenshot one window **[Windows]** | `pwsh tools/Save-Screenshot.ps1 -ProcessId <pid> -Name <name>` | 0 |
| Run several game instances, capture, read logs **[Windows]** | `pwsh tools/Start-Game.ps1 -Exe <exe> -Instances <n> -Seconds 30 [-HostArgs ...] [-ClientArgs ...]` | 0 · 1 log errors |
| Concept images (Codex CLI) | `pwsh tools/Invoke-CodexImage.ps1 -SpecFile <json>` or `-Prompt <text> -Name <name>` | 0 · 1 a job failed |
| Concept gallery and decision page | `pwsh tools/Start-ConceptServer.ps1` (`-Stop` to stop) | 0 · 1 |

## Engine tools

Build, test and module-rule commands are engine-specific and listed in [`docs/engine/build-and-test.md`](../engine/build-and-test.md), together with the one-shot selective verification command used by the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md).

## After building a feature

1. **Build/compile check**: run the engine's compile or test command. A compile error must surface as a failing exit code.
2. **Tests**: run the affected-scope tests first, as in [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) step 3.
3. **Run**: features you must see (gameplay, UI, networking) get a build launched with `Start-Game.ps1` or the engine's run command. Multi-client checks use `-Instances <target player count>`.
4. **Logs**: the run tools call `Read-LogErrors` at the end. Known harmless lines can go into `guardrails/log-ignore.txt`, one per line, but **adding to the ignore list needs user approval**.
5. **Screenshot**: when the feature shows on screen, capture it, **open the image yourself to check it**, then show the user.

### Screenshot rules

- Capture game screens **per window** (`-ProcessId`). Without arguments the script captures **every monitor**, including chat and messenger windows. Use a full capture only for desktop diagnosis, and delete the file afterwards.
- Capture each instance separately (`host`, `client1`, ...). The point is to spot mismatches between screens.
- To show the user: (1) put the file's **absolute path** in the report (`.agent-output/screenshots/`); (2) if the user cannot easily open paths, publish the image as a page and share the link.
- Check captures for personal information before reporting ([asset and data policy](07_ASSET_AND_DATA_POLICY.md), section 6).
- A screenshot is visual material, not proof of `done`. Behavior checks such as state consistency are proven by tests or logs.

## Known limits

- Some editors lock the project while open, so batch/headless runs fail. If the editor cannot be closed, report `unverified` and ask the user to close it or run the tests inside the editor.
- `Start-Game` host/client arguments (`-HostArgs`, `-ClientArgs`) are defined once the game has a connect entry point. Until then they are passed through as-is.
- Multiplayer connection and sync must be **judgeable from logs or state dumps**, not only by a human watching. If there is no path that logs game state, build one first.
- Record the verification status of each tool in your project (which ones you have actually run, and which paths stay untested) in this section.
