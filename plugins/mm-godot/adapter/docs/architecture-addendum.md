# Architecture addendum: Godot

> Read by `mm-game-architecture`. Needs community verification.

## Scripting model

- A game is a tree of **nodes**; reusable pieces are **scenes** (`.tscn`) instanced into other scenes. One script per node, typed GDScript (or C#).
- **Call down, signal up.** A parent may call methods on its children; children never reach up. They emit signals and the parent (or whoever instanced them) connects.
- **Autoloads** are global singletons. Keep them few: logger, event bus, session/network manager, save service. Game state that belongs to a level does not go in an autoload.
- **Resources** (`.tres`, custom `Resource` classes with `@export` fields) hold data and tuning values. Note that a resource loaded from disk is shared between users unless duplicated (`resource_local_to_scene` or `.duplicate()`); mutating a shared resource at runtime changes it for everyone.
- Groups (`add_to_group`) for loose collections ("enemies", "interactables"); prefer typed exports for specific references.

## Module boundaries

Godot has no assembly system for GDScript. Keep boundaries by folder and by convention:

- `scripts/core/`: logging, IDs, pure rules (no scene access): unit-testable.
- Feature folders under `scenes/` own their scripts; cross-feature calls go through signals, an event bus autoload, or interfaces (duck-typed `has_method` is banned; use `class_name` types).
- UI reads game state through signals or a read-only state object; game logic never references UI nodes.

## Processing

- `_process` for visuals, `_physics_process` for physics and gameplay ticks. Disable processing when idle (`set_process(false)`).
- Never cache `get_node` results in `_process`; resolve references in `_ready` (`@onready var hp_bar: ProgressBar = %HpBar`).
- `await` on signals and timers is tied to the object: if the node is freed while waiting, code after `await` does not resume for it; guard state accordingly and never leave half-applied state across an `await`.

## Threads

Scene tree access is main-thread only. Use `WorkerThreadPool` for pure computation and return results with `call_deferred` on a method reference.

## Physics in networked games

The server (authority) simulates `RigidBody3D/2D`; other peers show interpolated transforms via `MultiplayerSynchronizer`, with their own copy frozen. See [multiplayer](multiplayer.md).
