# Project context: Godot

> Fill this in once; `mm-generate-project-context` uses it as a seed. Blank values are undecided.

| Item | Value |
|---|---|
| Godot version | `<4.x.y>` (`config/features` in `project.godot`) |
| Language | `<GDScript / C# (.NET build) / both>` |
| Renderer | `<Forward+ / Mobile / Compatibility>` |
| Networking | `<none / high-level multiplayer (ENet, WebSocket, WebRTC) / Steam / other>`; topology `<listen server / dedicated>`; players `<n>` |
| Target platforms | `<desktop, web, mobile, console via third party>` |
| Test framework | `<GUT / gdUnit4 / none yet>` |
| Logger autoload | `<e.g. Log>` |
| Autoloads (singletons) | `<list>` |
| Shared scenes (edit only with approval) | `<main.tscn, ...>` |

## Folders (suggested)

```
res://
  scenes/<feature>/      .tscn + the scripts that belong to them
  scripts/<module>/      shared code without a scene
  resources/             .tres data (tuning lives here, not in code)
  autoload/              singletons registered in Project Settings
  assets/                art, audio, fonts (imported)
  addons/                third-party plugins (guardrails skip it)
  tests/                 GUT or gdUnit4 tests
```

## Naming (Godot style guide)

- Files and folders `snake_case`; node names `PascalCase`; `class_name` `PascalCase`; signals past tense (`health_changed`).
- Static typing on: `var speed: float = 4.0`, typed function signatures. Raise the untyped-declaration warning to an error under Project Settings → Debug → GDScript (setting name `untyped_declaration` in recent 4.x; *needs verification* for your version) as an extra guardrail.
