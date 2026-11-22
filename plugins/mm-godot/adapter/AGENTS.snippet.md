## Engine: Godot

Engine rules live in [`docs/engine/`](docs/engine/README.md) (adapter status: needs community verification). The short version:

- Call down, signal up. No `../` or `/root/` node paths, no `find_child` lookups at runtime, no string-name `connect`/`call`/`rpc`. Use typed exports, `%UniqueName`, groups and Signal/Callable objects.
- Typed GDScript; tuning values live in `Resource` files, not code. Duplicate shared resources before mutating them.
- `@rpc("any_peer")` handlers validate `multiplayer.get_remote_sender_id()` on the server.
- Never read `.tscn` files whole; search by node name. Never edit `.godot/`. Commit `.import` and `.uid` files.
- Self-verify: `uv run tools/guardrails/check.py --all`, a headless import/parse run, and the test command in `docs/engine/build-and-test.md`. Scan logs for `SCRIPT ERROR`, not only exit codes.
