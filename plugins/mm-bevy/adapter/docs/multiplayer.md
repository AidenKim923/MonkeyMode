# Multiplayer: Bevy

> Engine-neutral rules and test grades: [`docs/ai/04`](../ai/04_NETWORK_AUTHORITY_AND_TESTING.md). Bevy has no built-in networking. **Needs community verification**; crate APIs change with Bevy versions, so check compatibility tables first.

## Options

| Crate | Model | Notes |
|---|---|---|
| **lightyear** | Server-authoritative replication with client prediction, rollback and interpolation; input handling built in | Most complete for action games; heavier to learn |
| **bevy_replicon** | Server-authoritative component replication with pluggable transports (for example `bevy_replicon_renet`) | Simple mental model: mark components replicated, send client events |
| **bevy_renet** (renet) | Reliable/unreliable channels over UDP; you write replication yourself | Lowest level; most control |
| Others (naia, matchbox for WebRTC/P2P) | Various | Evaluate case by case |

Choose with the user and keep the crate behind your `net` plugin.

## Rules that apply whichever crate you pick

- The server owns simulation. Run it in `FixedUpdate`; clients send inputs or requests as events/messages, which the server validates (sender ID, distance, ownership, game stage) before applying.
- Replicate state as components on server entities. One-off messages are for effects only; late joiners must receive state through replication.
- Map entities between peers through the crate's entity mapping; raw `Entity` IDs differ between server and clients.
- Split systems into server, client and shared sets with run conditions (`run_if(server_running)`-style helpers in replicon, or lightyear's equivalents), and test each in a headless `App` per role where the crate allows it.

## Testing

- Same machine: one server/host process plus clients via `tools/Start-Game.ps1` or a shell script. Some crates provide in-process test harnesses or link conditioners for simulated latency and loss; use them for M1/M2, and real separate machines for M3.
- Log connect, spawn, ownership and state transitions with targets (`target: "game::net"`) so runs can be judged from logs.
