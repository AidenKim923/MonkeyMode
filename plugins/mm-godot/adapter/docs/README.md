# Engine adapter: Godot

> Installed by `mm-setup` into `docs/engine/`. The engine-neutral half of the rules is in [`docs/ai/`](../ai/README.md).

**Verification status: needs community verification.** Written for Godot 4.x from engine documentation knowledge. It has not yet been field-tested in a MonkeyMode project. Corrections are welcome; mark verified sections as you confirm them.

| Doc | Content |
|---|---|
| [Project context](project-context.md) | Fill in: Godot version, language (GDScript / C#), folders, autoloads |
| [Architecture addendum](architecture-addendum.md) | Scenes and nodes, signals, autoloads, resources |
| [Guardrails](guardrails.md) | Node path and signal rules, banned patterns |
| [Build and test](build-and-test.md) | Headless runs, GUT / gdUnit4, export presets |
| [Multiplayer](multiplayer.md) | High-level multiplayer: `MultiplayerAPI`, `@rpc`, spawner and synchronizer |
| [Version control](version-control.md) | `.godot/`, `.import` files, UIDs, LFS |

Files this adapter adds: `guardrails/godot.json` (GDScript rules).

C# projects: the GDScript rules do not apply to `.cs` files. Reuse the C# ideas from the Unity adapter (async void, raw threads, reflection) by adding a C# profile, and read Godot's C# docs for signal and `GodotObject` lifetime rules.
