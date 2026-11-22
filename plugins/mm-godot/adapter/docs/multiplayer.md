# Multiplayer: Godot

> Engine-neutral rules and test grades: [`docs/ai/04`](../ai/04_NETWORK_AUTHORITY_AND_TESTING.md). Needs community verification.

## High-level multiplayer (Godot 4)

| Concept | Godot |
|---|---|
| Peer | `ENetMultiplayerPeer` (UDP), `WebSocketMultiplayerPeer`, `WebRTCMultiplayerPeer`; assigned to `multiplayer.multiplayer_peer` |
| Server check | `multiplayer.is_server()`; the server's peer ID is 1 |
| Authority over a node | `set_multiplayer_authority(peer_id)` / `is_multiplayer_authority()`; default authority is the server (1) |
| Client → server request | `@rpc("any_peer", "call_remote", "reliable")` function called with `.rpc_id(1, args)`; on the server read `multiplayer.get_remote_sender_id()` and validate |
| Server → clients effect | `@rpc("authority", "call_local")` |
| Replicated state | `MultiplayerSynchronizer` with a `SceneReplicationConfig` (spawn + sync properties, on-change or always) |
| Spawning | `MultiplayerSpawner` with a spawn path and allowed scenes; spawn on the server only |

## Common mistakes

| Mistake | Result |
|---|---|
| `any_peer` RPC without checking the sender | Any client can change game state |
| Moving a node on a peer that is not its authority | Overwritten by the synchronizer next update; jitter |
| Spawning outside a `MultiplayerSpawner` path, or on a client | Node exists on one peer only |
| Node path or name differs between peers | RPCs and synchronizers fail to resolve the node |
| Physics bodies simulated on every peer | Divergence; freeze them on non-authority peers |
| State sent only as RPCs | Late joiners never see it |

## Listen server vs dedicated

Listen server: `create_server` on the host, which also plays. Dedicated: export a headless build (`--headless`, or the dedicated server export option) and run without rendering. All the listen-server traps in `docs/ai/04` apply.

## Alternatives

Steam networking (GodotSteam with its multiplayer peer), Nakama, or a custom transport. Choose with the user; keep the transport behind the session/network autoload.
