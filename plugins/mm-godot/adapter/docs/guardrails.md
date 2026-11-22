# Guardrails: Godot

> Enforced by `guardrails/godot.json` on `*.gd` outside `addons/` and `.godot/`. Evidence marks: **[knowledge]** engine documentation knowledge, not re-checked here · **[judgment]** a MonkeyMode default. **Needs community verification.**

## Enforced

| ID | Target | Why it is tricky | Instead | Evidence |
|---|---|---|---|---|
| GODOT_PARENT_NODE_PATH | `get_node("../...")`, `$"../..."` | The script depends on where its scene is instanced; reparenting breaks it with no error until runtime | Typed `@export var target: Node3D`, `%UniqueName` inside the same scene, parent wires children, signals up | [knowledge] |
| GODOT_ABSOLUTE_NODE_PATH | `get_node("/root/...")` | Hard-codes the tree layout and autoload names | Reference the autoload by name, typed export, group registry | [knowledge] |
| GODOT_RUNTIME_FIND | `find_child`, `find_children`, `get_tree().root.find...` | Name- and hierarchy-dependent, slow; the Godot equivalent of scene-wide Find | Exports, groups, registry autoload | [knowledge] |
| GODOT_STRING_SIGNAL_CONNECT | `connect("signal", ...)` | Godot 3 string API; renames break silently | `signal_name.connect(callable)` | [knowledge] |
| GODOT_STRING_CALL | `.call("m")`, `.call_deferred("m")`, `.rpc("m")`, `.rpc_id(id, "m")` | String method names: renames break silently; RPC targets implicit | Method references: `m.call_deferred()`, `m.rpc()`, `m.rpc_id(id)` | [knowledge] |
| GODOT_BLOCKING_DELAY | `OS.delay_msec/usec` | Blocks the main thread; freezes the game and the server | `await get_tree().create_timer(t).timeout`, `Timer` node | [knowledge] |
| GODOT_TIMESCALE_WRITE | `Engine.time_scale =` | Peers' clocks drift; physics sync breaks (networked games) | Server-side pause gate, one session clock | [judgment] |
| GODOT_DIRECT_PRINT | `print`, `print_rich`, `printerr`, ... outside the logger | Agents need categorized, leveled logs | A logger autoload (`Log.info(category, msg)`) | [judgment] |

The no-comment rule is **off** for GDScript: the detector only understands C-style comments.

## Review rules (not mechanical)

| Rule | Why |
|---|---|
| `@rpc("any_peer")` handlers check `multiplayer.get_remote_sender_id()` and validate the request | Any peer can call them; this is where clients would skip game rules |
| State is synced with `MultiplayerSynchronizer` (or RPC'd once to late joiners), never only by one-shot RPCs | Late joiners miss one-shot RPCs |
| No mutation of shared `Resource` instances at runtime without `duplicate()` | Every user of the resource sees the change |
| `@onready` + `%UniqueName` instead of `get_node` in `_process` | Per-frame lookups and fragile paths |
| Typed GDScript everywhere; `untyped_declaration` warning set to error | Catches whole classes of mistakes at parse time |
| Nothing after an `await` assumes the node still exists | Freed nodes do not resume |

## Semantic layer

Turn GDScript warnings into errors in Project Settings → Debug → GDScript (for example `untyped_declaration`, `unsafe_method_access`, `unused_variable`). A headless import/check run then fails on them ([build and test](build-and-test.md)).
