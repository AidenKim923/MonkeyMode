# Architecture addendum: Unity

> Read by `mm-game-architecture` before it chooses patterns. Engine-neutral rules are in `docs/ai/`.

## Scripting model

- C# MonoBehaviours on GameObjects, composed in prefabs and scenes. Data and tuning in **ScriptableObjects**, never in code constants.
- One lifetime owner per coroutine. Visual effects use coroutines; I/O and network waits use `Awaitable` with `destroyCancellationToken`. Do not mix the two inside one feature.
- Logging goes through one wrapper (for example `Log.Info/Warn/Error(category, message)` printing `[<TAG>][LEVEL] category: message`) so agents can judge behavior from logs.

## Assemblies (module boundaries)

Split `Assets/_Game/Scripts/` into assemblies with one-way dependencies; the compiler enforces references and `tools/guardrails/asmdef_rules.py` enforces direction. The shipped `guardrails/module-rules.json` is a layered example:

```
Core ← Domain ← Networking ← Physics ← Gameplay ← App
                    ↑                              ↑
                    UI ────────────────────────────┘      Editor references everything
```

- `Core`: contracts, logging, IDs. References nothing.
- `Domain`: pure game rules, testable without the engine running.
- `UI`: may read state only through contracts in Core; only App and Editor may reference UI, so headless/server runs never depend on screens.
- `App`: composition root. Only Editor references it.
- `Editor`: editor-only platform; runtime never references it.

Add or rename modules to match your architecture, then update `module-rules.json` (user approval).

## Scenes

- A bootstrap scene owns `DontDestroyOnLoad` objects; nothing else uses it.
- Shared scenes are edited by one person/agent at a time and only with approval: scenes do not merge.
- Prefer additive scenes for levels so content work does not collide with systems work.

## References instead of lookups

Serialized inspector references, injection at creation, or a registry that objects add themselves to. No `GameObject.Find*`, `FindObjectsByType`, or `Resources.Load` at runtime (see [guardrails](guardrails.md)).

## Physics in networked games

The server simulates rigid bodies; clients interpolate. Never simulate the same body on both. See [multiplayer](multiplayer.md).
