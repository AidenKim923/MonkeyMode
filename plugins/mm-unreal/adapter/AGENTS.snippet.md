## Engine: Unreal Engine

Engine rules live in [`docs/engine/`](docs/engine/README.md) (adapter status: needs community verification). The short version:

- UObjects are garbage-collected: no raw `new`/`delete`; members are `UPROPERTY() TObjectPtr<>`; non-owning references are `TWeakObjectPtr` checked with `IsValid()`.
- Server authority: rules in GameMode, shared state in replicated properties on GameState/PlayerState/actors, client requests via `Server` RPCs on owned actors with validation. Multicast RPCs are for effects only.
- No world-wide actor searches or synchronous loads at runtime; use subsystems and soft references with async loading. Log with a per-module category, not `LogTemp`.
- `.uasset`/`.umap` are binary: never edit them as text, never assign the same asset to parallel workers, use LFS locks.
- Self-verify: `uv run tools/guardrails/check.py --all`, then the build and automation-test commands in `docs/engine/build-and-test.md`.
