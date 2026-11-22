# Engine adapter: Unity

> Installed by `mm-setup` into `docs/engine/`. These docs are the Unity half of the rules; the engine-neutral half is in [`docs/ai/`](../ai/README.md).

**Verification status:** field-tested. Tested with Unity 6 (URP) + Mirror: batch-mode tests and builds were run; launching several clients through `Start-Game.ps1` was not exercised end to end. Netcode for GameObjects (NGO) notes are from documentation knowledge and need community verification.

| Doc | Content |
|---|---|
| [Project context](project-context.md) | Fill in: Unity version, render pipeline, packages, folders, assemblies |
| [Architecture addendum](architecture-addendum.md) | Folder layout, assemblies, ScriptableObjects, scenes |
| [Guardrails](guardrails.md) | Banned APIs with reasons, alternatives and sources; Roslyn analyzer layer |
| [Build and test](build-and-test.md) | Batch-mode test/build scripts, exit codes, known limits |
| [Multiplayer](multiplayer.md) | Mirror and NGO: authority, common mistakes, multi-instance testing |
| [Version control](version-control.md) | `.gitignore`, LFS, `.meta` files, Smart Merge |
| [Asset import](asset-import.md) | FBX/glTF import checklist for models and characters |

Files this adapter adds to the project:

| Path | Purpose |
|---|---|
| `guardrails/unity.json` | Banned API profile for `Assets/_Game/**/*.cs` (no-comment rule on) |
| `guardrails/module-rules.json` | Allowed assembly dependency directions |
| `tools/guardrails/asmdef_rules.py` | Checks `.asmdef` references against the module rules |
| `tools/Invoke-UnityTests.ps1`, `tools/Invoke-UnityBuild.ps1` | Batch-mode tests and builds **[Windows paths; pwsh 7]** |
| `tools/Get-ChangeScope.ps1`, `tools/Invoke-SelectiveVerify.ps1` | Changed files → affected assemblies → tests to run first |
| `tools/unity-templates/AgentBuild.cs` | Build entry point to copy into `Assets/_Game/Editor/Automation/` |
