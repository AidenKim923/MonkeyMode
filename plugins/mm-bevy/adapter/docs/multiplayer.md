# Multiplayer: Bevy

> Engine-neutral rules and test grades: [`docs/ai/04`](../ai/04_NETWORK_AUTHORITY_AND_TESTING.md). Bevy has no built-in networking. Crate versions below were checked on docs.rs for Bevy 0.20; crate APIs change with every Bevy release, so check each crate's compatibility table first.

## Options

| Crate | Model | Notes |
|---|---|---|
| **lightyear** (0.31 for Bevy 0.20) | Server-authoritative, with client-side prediction and rollback and snapshot interpolation; uses bevy_replicon for world replication | Most complete for action games; heavier to learn |
| **bevy_replicon** (0.45 for Bevy 0.20) | Server-authoritative: "replication happens only from server to clients"; needs a messaging backend such as `bevy_replicon_renet` | Simple mental model: mark components replicated, send client messages |
| **bevy_renet** (6.0 for Bevy 0.20, renet 2) | Client/server channels with authentication and connection management; you write replication yourself | Lowest level; most control |
| **bevy_matchbox** (0.15, still on Bevy 0.19 when checked) | Peer-to-peer WebRTC for native and wasm | For P2P and browser games; check its Bevy support first |
| naia | Various | *Needs verification* (docs were unavailable) |

Choose with the user and keep the crate behind your `net` plugin.

## Rules that apply whichever crate you pick

- The server owns simulation. Run it in `FixedUpdate`; clients send inputs or requests as events/messages, which the server validates (sender ID, distance, ownership, game stage) before applying.
- Replicate state as components on server entities. One-off messages are for effects only; late joiners must receive state through replication.
- Map entities between peers through the crate's entity mapping; raw `Entity` IDs differ between server and clients.
- Split systems into server, client and shared sets with run conditions (replicon exposes its client and server state as Bevy `States`, usable with `in_state`/`run_if`; lightyear has equivalents), and test each in a headless `App` per role where the crate allows it.

## Testing

- Same machine: one server/host process plus clients via `tools/Start-Game.ps1` or a shell script. Some crates provide in-process test harnesses or link conditioners for simulated latency and loss; use them for M1/M2, and real separate machines for M3.
- Log connect, spawn, ownership and state transitions with targets (`target: "game::net"`) so runs can be judged from logs.
