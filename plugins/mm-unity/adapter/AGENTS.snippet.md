## Engine: Unity

Engine rules live in [`docs/engine/`](docs/engine/README.md). The short version:

- Gameplay code lives under `Assets/_Game/` and is split into assemblies (`.asmdef`) whose dependency directions are checked by `uv run tools/guardrails/asmdef_rules.py` against `guardrails/module-rules.json`.
- Banned APIs (`guardrails/unity.json`): tween libraries, `SendMessage`/string `Invoke`, scene-wide `Find*`, `Resources.Load`, `async void`, raw `Thread`, runtime reflection, direct `Debug.Log`, `Time.timeScale` writes, Mirror `requiresAuthority = false`. Reasons and alternatives: [`docs/engine/guardrails.md`](docs/engine/guardrails.md).
- Never read `.unity`/`.prefab` files whole; search by name. Never edit `Library/`, `Temp/`, `obj/`. Moving or deleting assets breaks `.meta` GUIDs: needs approval.
- Self-verify with `pwsh tools/Invoke-SelectiveVerify.ps1` (guardrails + asmdef + affected tests), `pwsh tools/Invoke-UnityTests.ps1 -Mode EditMode`, `pwsh tools/Invoke-UnityBuild.ps1`. Batch mode fails while the editor has the project open.
- Tunable values go in ScriptableObjects.
