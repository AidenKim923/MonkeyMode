## Engine: Bevy

Engine rules live in [`docs/engine/`](docs/engine/README.md) (adapter status: needs community verification; Bevy APIs change between versions, so check names against `Cargo.toml`). The short version:

- Systems never block: no `thread::sleep`, no `block_on`, no raw threads. Use timers and task pools.
- Order every dependent system explicitly (`.chain()`, `.before/.after`, sets). Gameplay simulation runs in `FixedUpdate`. `Commands` apply at the next sync point.
- Log with `info!/warn!/error!` and a target; no `println!`/`dbg!` in game code.
- Networked state is replicated components owned by the server; client messages are validated on the server.
- Self-verify: `uv run tools/guardrails/check.py --all`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test -p <affected crate>`.
