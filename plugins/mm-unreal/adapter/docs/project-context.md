# Project context: Unreal Engine

> Fill this in once; `mm-generate-project-context` uses it as a seed. Blank values are undecided.

| Item | Value |
|---|---|
| Engine version | `<5.x>` (`EngineAssociation` in `<YourGame>.uproject`) |
| Engine install / source build | `<launcher install path or source build>`: set `UE_ROOT` for the commands in build-and-test |
| C++ / Blueprint split | `<e.g. systems in C++, content and tuning in Blueprints/DataAssets>` |
| Game modules | `<YourGame>`, `<YourGame>Editor`, `...` (from `Source/*/*.Build.cs`) |
| Plugins in use | `<Enhanced Input, Gameplay Ability System, CommonUI, ...>` |
| Networking | `<none / built-in replication (listen / dedicated) / Iris>`; players `<n>`; online subsystem `<Null / Steam / EOS>` |
| Target platforms | `<Win64, Linux, Mac, consoles, Android, iOS>` |
| Log categories | `Log<YourGame>`, `Log<Module>` |
| Shared maps (edit only with approval or One File Per Actor) | `<list>` |

## Layout

```
<YourGame>.uproject
Source/<YourGame>/            Public/ Private/ <YourGame>.Build.cs
Source/<YourGame>Editor/      editor-only module
Content/                      .uasset/.umap (binary)
Config/                       Default*.ini
Plugins/                      project plugins (each with its own Source/)
```

## Naming (Epic coding standard)

Class prefixes: `U` UObject, `A` Actor, `F` struct/plain class, `E` enum, `I` interface, `T` template, `S` Slate widget. Booleans `bIsAlive`. Assets: `BP_`, `WBP_`, `M_`, `MI_`, `T_`, `SM_`, `SK_`, `ABP_`, `DA_`.
