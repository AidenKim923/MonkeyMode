# Build and test: Godot

> Command-line reference for agents, checked against the Godot 4.7 command-line docs and the GUT and gdUnit4 docs. Replace `godot` with your editor binary (for example `godot4`, `Godot_v4.x-stable_win64_console.exe`; on Windows use the `_console` build to see output). Set it once in `project-context.md`.

## Commands

| Goal | Command | Pass signal |
|---|---|---|
| Guardrails | `uv run tools/guardrails/check.py --all` | exit 0 |
| Import and parse everything headless (catches script errors) | `godot --headless --path . --import` ("waits for any resources to be imported, and then quits"; if your version lacks it, `--editor --quit`) | exit 0 and no `SCRIPT ERROR` / `Parse Error` lines in output |
| GUT tests (GUT 9.x for Godot 4) | `godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | exit 0 (1 on failures) |
| gdUnit4 tests | set `GODOT_BIN` to the editor binary, then `addons/gdUnit4/runtest.sh -a res://tests` (Linux/macOS) or `addons\gdUnit4\runtest.cmd -a res://tests` (Windows) | exit 0 (100 failures, 101 warnings) |
| Export a build | `godot --headless --path . --export-release "<preset name>" build/<YourGame>.exe` (`--export-debug` for a debug template; the output folder must exist) | exit 0, file exists |
| Run a scene for N frames | `godot --path . res://scenes/test/test_scene.tscn --quit-after <frames>` (iterations, not seconds) | log contains the expected lines |

Export needs export templates installed and a preset in `export_presets.cfg`.

## Reading results

- Script errors print as `SCRIPT ERROR:` / `ERROR:` with `res://` paths. Pipe output to a log file under `logs/{date}/` and summarize with `pwsh tools/Read-LogErrors.ps1 -LogPath <log>`.
- Some versions return exit code 0 even when scripts fail to parse; always scan the log, not only the exit code.

## Multi-instance runs

The editor can launch several instances with their own arguments (Debug → Customize Run Instances; *needs verification* of the exact menu and the version that added it). For builds, `pwsh tools/Start-Game.ps1 -Exe <exe> -Instances <n> -HostArgs "--host" -ClientArgs "--join 127.0.0.1"` once the game parses those arguments (`OS.get_cmdline_user_args()` reads arguments after `--`).

## Typical failures

| Symptom | Check first |
|---|---|
| `Invalid get index` / null instance after reparenting | Node paths; switch to exports or `%UniqueName` |
| Resource changes leak between instances | Shared resource mutated without `duplicate()` |
| Code after `await` never runs | The node was freed while waiting |
| Works in editor, fails in export | Files filtered out of the export preset; `res://` paths with wrong case on case-sensitive platforms |
