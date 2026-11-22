# Build and test: Godot

> Command-line reference for agents. Needs community verification. Replace `godot` with your editor binary (for example `godot4`, `Godot_v4.x-stable_win64_console.exe`; on Windows use the `_console` build to see output). Set it once in `project-context.md`.

## Commands

| Goal | Command | Pass signal |
|---|---|---|
| Guardrails | `uv run tools/guardrails/check.py --all` | exit 0 |
| Import and parse everything headless (catches script errors) | `godot --headless --path . --import` (Godot 4.2+; on older versions `--editor --quit`) | exit 0 and no `SCRIPT ERROR` / `Parse Error` lines in output |
| GUT tests | `godot --headless --path . -s res://addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` | exit 0 |
| gdUnit4 tests | `godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --add res://tests --ignoreHeadlessMode` (or the `runtest` wrapper script shipped with gdUnit4) | exit 0 |
| Export a build | `godot --headless --path . --export-release "<preset name>" build/<YourGame>.exe` | exit 0, file exists |
| Run a scene for N seconds | `godot --path . res://scenes/test/test_scene.tscn --quit-after <frames>` | log contains the expected lines |

Export needs export templates installed and a preset in `export_presets.cfg`.

## Reading results

- Script errors print as `SCRIPT ERROR:` / `ERROR:` with `res://` paths. Pipe output to a log file under `logs/{date}/` and summarize with `pwsh tools/Read-LogErrors.ps1 -LogPath <log>`.
- Some versions return exit code 0 even when scripts fail to parse; always scan the log, not only the exit code.

## Multi-instance runs

The editor can launch several instances (Debug → Customize Run Instances, Godot 4.3+), each with its own arguments such as `--server` / `--client`. For builds, `pwsh tools/Start-Game.ps1 -Exe <exe> -Instances <n> -HostArgs "--host" -ClientArgs "--join 127.0.0.1"` once the game parses those arguments (`OS.get_cmdline_user_args()` reads arguments after `--`).

## Typical failures

| Symptom | Check first |
|---|---|
| `Invalid get index` / null instance after reparenting | Node paths; switch to exports or `%UniqueName` |
| Resource changes leak between instances | Shared resource mutated without `duplicate()` |
| Code after `await` never runs | The node was freed while waiting |
| Works in editor, fails in export | Files filtered out of the export preset; `res://` paths with wrong case on case-sensitive platforms |
