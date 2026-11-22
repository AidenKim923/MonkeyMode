# Project context: Unity

> Fill this in once; `mm-generate-project-context` uses it as a seed. Agents treat blank values as undecided.

| Item | Value |
|---|---|
| Unity version | `<e.g. 6000.x.yf1>` (from `ProjectSettings/ProjectVersion.txt`) |
| Render pipeline | `<URP / HDRP / Built-in>` |
| Input | `<Input System / legacy>` |
| Networking | `<none / Mirror <version> / Netcode for GameObjects <version> / other>`; topology `<listen server / dedicated>`; players `<n>` |
| Scripting backend | `<Mono / IL2CPP>` per platform |
| Target platforms | `<Windows, macOS, Linux, consoles, mobile>` |
| Packages agents may not install | `<e.g. the networking library: the user adds it>` |
| Logging wrapper | `<AssemblyPrefix>Core.Logging.Log` (or yours) |
| Shared scenes (edit only with approval) | `<Bootstrap, Lobby, ...>` |

## Folders

```
Assets/_Game/
  Art/  Animations/  Audio/  Prefabs/  Scenes/  ScriptableObjects/
  Scripts/<Module>/        one folder per assembly
  Editor/Automation/       AgentBuild.cs and other editor tooling
  Tests/EditMode/  Tests/PlayMode/
```

Third-party packages stay where they install (`Packages/`, `Assets/ThirdParty/`); guardrails ignore them.

## Naming

- Assemblies: `<AssemblyPrefix><Module>` (for example `<AssemblyPrefix>Core`), test assemblies `<AssemblyPrefix><Module>.Tests`.
- Namespaces follow assemblies.
- Prefabs and assets: `<category>_<name>_<variant>` (for example `prop_crate_small`).
