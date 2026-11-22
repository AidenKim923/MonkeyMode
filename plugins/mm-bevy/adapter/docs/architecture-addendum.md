# Architecture addendum: Bevy

> Read by `mm-game-architecture`. Needs community verification; check names against your Bevy version.

## ECS model

- **Entities** are IDs, **components** are plain data (`#[derive(Component)]`), **systems** are functions whose parameters (`Query`, `Res`, `ResMut`, `Commands`, `EventReader/Writer`) declare their data access. **Resources** are singletons.
- Each feature is a **Plugin** that registers its components, resources, events and systems. `main.rs` only adds plugins.
- Tuning values live in resources or assets (RON/TOML loaded through the `AssetServer`), not in code constants.

## Schedules and ordering

- Systems in the same schedule run **in parallel and in no fixed order** unless ordered. Order explicitly with `.chain()`, `.before()/.after()`, or `SystemSet`s configured with `configure_sets`.
- Gameplay simulation belongs in `FixedUpdate` (fixed timestep; required for deterministic or networked simulation). Visual interpolation and UI go in `Update`.
- `Commands` are deferred: spawned entities and inserted components are not visible to other systems until the command flush at the next sync point. Plan ordering around it.
- Game flow uses `States` (`OnEnter`, `OnExit`, `run_if(in_state(...))`) instead of booleans checked in every system.

## Data-access conflicts

Two `Query`s in one system that can both access the same component mutably panic at startup. Use `Without<T>` filters, a `ParamSet`, or split the system.

## Async and blocking

Systems must never block. File, network or heavy work goes to `IoTaskPool` / `AsyncComputeTaskPool`; store the `Task` in a component and poll it each frame. Never `block_on` inside the app.

## Module boundaries

Crates in a workspace give compiler-enforced boundaries. Keep rendering out of the core crate so headless tests and a dedicated server can build without it. UI communicates through events and read-only queries.

## Physics in networked games

The server runs physics in `FixedUpdate`; clients either predict (with rollback, as lightyear supports) or interpolate replicated transforms. Never let two peers own the same body.
