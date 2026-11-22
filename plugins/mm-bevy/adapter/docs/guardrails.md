# Guardrails: Bevy

> Enforced by `guardrails/bevy.json` on `*.rs` outside `target/`. Evidence marks: **[source]** checked against Bevy 0.20 docs · **[knowledge]** general Rust knowledge · **[judgment]** a MonkeyMode default.

## Enforced (regex)

| ID | Target | Why it is tricky | Instead | Evidence |
|---|---|---|---|---|
| BEVY_BLOCKING_SLEEP | `std::thread::sleep` | Blocks a scheduler thread; stalls the frame and the server tick | `Timer`, `on_timer` run condition (`bevy::time::common_conditions`), task pools | [knowledge] |
| BEVY_BLOCK_ON | `block_on(...)` (`bevy::tasks::block_on`, futures-lite, pollster) | Blocks a scheduler thread | Spawn on `IoTaskPool`/`AsyncComputeTaskPool`, poll the `Task` with `check_ready` | [source] `bevy_tasks` |
| BEVY_RAW_THREAD | `std::thread::spawn` | Escapes scheduling; cannot touch the `World` | Task pools; results back through components or channel resources | [knowledge] |
| BEVY_PRINTLN | `println!`, `eprintln!`, `print!`, `dbg!` (tests, examples, `src/bin` excluded) | Agents need levels and targets in logs | `info!`, `warn!`, `error!`, `debug!` with a `target:` | [judgment] |
| BEVY_EXCLUSIVE_WORLD_SYSTEM | `fn x(world: &mut World)` systems | Still supported (`&mut World` is a system param since 0.20), but it serializes the schedule and hides data dependencies | Regular system params + `Commands`; justify exceptions | [judgment] |
| BEVY_VIRTUAL_TIME_SPEED | `Time<Virtual>` `set_relative_speed`/`pause()` | Peers drift; replicated simulation desyncs (networked games) | Server-driven `State` or run conditions | [source] `Time<Virtual>` API; ban is [judgment] |

The no-comment rule is **off** for Rust.

## Symbol-accurate layer: Clippy

Copy `clippy.toml.example` to `clippy.toml` and run `cargo clippy --all-targets -- -D warnings`. `disallowed-methods` catches the same calls by symbol path, including through `use` aliases that regex misses. Also consider `#![deny(clippy::unwrap_used)]` in gameplay crates (with `expect` and system error handling as the alternative) once the team agrees.

## Review rules (not mechanical)

| Rule | Why |
|---|---|
| Every system that depends on another's output is ordered (`.chain()`, `.after()`, sets) | Unordered systems run in arbitrary order; bugs appear intermittently |
| Gameplay simulation in `FixedUpdate`, not `Update` | Frame-rate-dependent behavior; network desync |
| No two queries in one system with overlapping mutable access | Panics when the system is initialized |
| `Commands` results are not read in the same system that issued them | Deferred until the next sync point |
| Server-authoritative state is replicated components, not one-off network messages | Late joiners miss messages |
| Client input messages are validated on the server before applying | Clients would skip rules |
