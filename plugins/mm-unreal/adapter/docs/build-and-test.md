# Build and test: Unreal Engine

> Command lines for agents. Needs community verification. `UE_ROOT` is the engine folder (the one containing `Engine/`); `<Project>` is the path to `<YourGame>.uproject`. Windows paths shown; on Linux/macOS use `.sh` and the platform's binaries.

## Commands

| Goal | Command | Pass signal |
|---|---|---|
| Guardrails | `uv run tools/guardrails/check.py --all` | exit 0 |
| Build editor target (compile check) | `"%UE_ROOT%/Engine/Build/BatchFiles/Build.bat" <YourGame>Editor Win64 Development -Project="<Project>" -WaitMutex` | exit 0 |
| Run automation tests headless | `"%UE_ROOT%/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "<Project>" -ExecCmds="Automation RunTests <YourGame>.;Quit" -unattended -nullrhi -nosplash -nop4 -log -ReportExportPath="<abs path>/.agent-output/test-results"` | exit 0 and the report shows no failures |
| Package a build | `"%UE_ROOT%/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun -project="<Project>" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<abs path>/.agent-output/builds"` | exit 0, archive exists |
| Dedicated server build | add `-server -serverplatform=Win64 -noclient` (needs a `<YourGame>Server.Target.cs`) | exit 0 |

## Tests

- **Automation tests** (`IMPLEMENT_SIMPLE_AUTOMATION_TEST`, or the newer `TEST_CLASS` / Low Level Tests) under `Source/<Module>/Private/Tests/`. Name them `<YourGame>.<Module>.<Behavior>` so `RunTests <YourGame>.<Module>` selects the affected module.
- **Functional tests** (`AFunctionalTest` actors in test maps) for in-world behavior.
- **Gauntlet** drives multi-process sessions (server + clients) for M2/M3-style checks.

## Reading results

Logs land in `Saved/Logs/`. Copy or point `-abslog=<path>` to `logs/{date}/` and summarize with `pwsh tools/Read-LogErrors.ps1 -LogPath <log>`. Look for `Error:` and `LogAutomationController: Error`.

## Known limits

- The editor holds locks on DLLs while open; Live Coding and command-line builds can conflict. Close the editor or use Live Coding only.
- First builds and shader compiles take a long time; set generous timeouts and report `awaiting verification` rather than cutting them short.

## Typical failures

| Symptom | Check first |
|---|---|
| Linker errors for engine symbols | Missing module in `.Build.cs` dependencies |
| Crash on object access after a while | Raw pointer without `UPROPERTY` collected by GC |
| Works in PIE, broken in packaged build | Assets only referenced softly were not cooked; add them to the Asset Manager or cook rules |
| Blueprint changes "lost" | Binary asset conflict; check file locks and LFS |
