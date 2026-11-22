# Build and test: Unity

> PowerShell 7 scripts in `tools/`. Logs go to `logs/{date}/`, results to `.agent-output/`. **[Windows]** paths by default; set `UNITY_EXE` elsewhere.

## Commands

| Goal | Command | Exit codes |
|---|---|---|
| One-shot selective verify (pre-commit steps 1-3) | `pwsh tools/Invoke-SelectiveVerify.ps1 [-Base HEAD] [-Mode EditMode]` | 0 pass · 1 fail · 2 unverified / tests missing |
| Change scope and impact only | `pwsh tools/Get-ChangeScope.ps1 [-Json]` | 0 |
| Guardrails | `uv run tools/guardrails/check.py --all` | 0 · 1 |
| Assembly direction | `uv run tools/guardrails/asmdef_rules.py` | 0 · 1 |
| Unity tests | `pwsh tools/Invoke-UnityTests.ps1 -Mode EditMode\|PlayMode [-Assemblies A,B] [-Filter ...]` | 0 · 1 failed · 2 compile error · 3 timeout |
| Unity build | `pwsh tools/Invoke-UnityBuild.ps1 [-Target StandaloneWindows64]` | 0 · 1 failed · 3 timeout |
| Run builds, multi-instance, capture | `pwsh tools/Start-Game.ps1 -Exe <exe> -Instances <n>` | 0 · 1 log errors |

The scripts find the Unity project at the repository root or in a single sub-folder with `ProjectSettings/ProjectVersion.txt`. The editor is located from that file's version under the Unity Hub install folder; set `UNITY_EXE` to override.

## Tests

Unity Test Framework. EditMode tests in `Assets/_Game/Tests/EditMode/`, PlayMode tests in `Assets/_Game/Tests/PlayMode/`, each in a `<AssemblyPrefix><Module>.Tests` assembly so `Get-ChangeScope` can map changed assemblies to the tests that cover them.

## Known limits

- Batch mode fails while the editor has the same project open (project lock). If the editor cannot be closed, report `unverified` and ask the user to close it or run the Test Runner in the editor.
- `Invoke-UnityBuild` needs `Assets/_Game/Editor/Automation/AgentBuild.cs` (copy it from `tools/unity-templates/AgentBuild.cs`) and at least one enabled scene in Build Settings.
- `Invoke-SelectiveVerify` exits 2 when no test assembly covers the affected scope: add tests, then run again.
- Typical environment noise at editor shutdown (a socket accept exception, a licensing access-token line) is not a build or test failure. Adding it to `guardrails/log-ignore.txt` needs user approval.

## Typical failures

| Symptom | Check first |
|---|---|
| Compile errors will not go away | Is the editor still recompiling, or in Play Mode? |
| References show as Missing | Missing `.meta` file or GUID collision |
| Images or models show as text | `git lfs install` and `git lfs pull` |
| Scene changes do not appear | Is another scene open? |
