# Build and test: Bevy

> Needs community verification. All commands run from the workspace root.

## Commands

| Goal | Command | Pass signal |
|---|---|---|
| Guardrails | `uv run tools/guardrails/check.py --all` | exit 0 |
| Format check | `cargo fmt --all -- --check` | exit 0 |
| Lints (symbol-accurate bans) | `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| Tests | `cargo test --workspace` | exit 0 |
| Tests for affected crates only | `cargo test -p <crate>` for each crate in the diff (`git diff --name-only` → `crates/<crate>/`) | exit 0 |
| Release build | `cargo build --release` | exit 0 |
| Web build | `cargo build --release --target wasm32-unknown-unknown` (plus `wasm-bindgen` or `trunk`) | exit 0 |

Selective verification for the [pre-commit procedure](../ai/09_PRE_COMMIT_PROCEDURE.md): guardrails → `cargo clippy -p <affected>` → `cargo test -p <affected>` → full workspace only when a core crate changed.

## Headless tests

Test systems without a window by building a small `App`:

```rust
let mut app = App::new();
app.add_plugins(MinimalPlugins).add_plugins(MyGameplayPlugin);
app.world_mut().spawn(Player::default());
app.update();
let count = app.world_mut().query::<&Player>().iter(app.world()).count();
assert_eq!(count, 1);
```

Use `TimePlugin`/`Time::<Fixed>` manipulation or `app.world_mut().run_schedule(FixedUpdate)` to step fixed-timestep systems deterministically. Names differ between Bevy versions; check yours.

## Running several instances

Build once, then `pwsh tools/Start-Game.ps1 -Exe target/release/<game>.exe -Instances <n> -HostArgs "--server" -ClientArgs "--client 127.0.0.1"` once the game parses those arguments (for example with `clap`). On Linux/macOS, launch the binaries from a shell script with per-instance log files.

## Reading results

Set `RUST_LOG=info,<game>=debug` and write logs per instance (`bevy::log::LogPlugin` with a custom layer, or redirect stdout) under `logs/{date}/`. Summarize with `pwsh tools/Read-LogErrors.ps1 -LogPath <log>`; panics show as `panicked at`.

## Typical failures

| Symptom | Check first |
|---|---|
| Panic at startup about conflicting queries | Two queries with overlapping mutable access in one system |
| Behavior changes between runs | Missing system ordering |
| Entity "missing" right after spawning | `Commands` are deferred until the next sync point |
| Compile errors after `cargo update` | A Bevy or plugin minor version changed APIs; pin versions and read the migration guide |
| Long compile times | Enable `bevy/dynamic_linking` in dev only and a faster linker (lld/mold) |
