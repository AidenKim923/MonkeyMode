# Multiplayer: Unity

> Engine-neutral authority rules and test grades: [`docs/ai/04`](../ai/04_NETWORK_AUTHORITY_AND_TESTING.md). This page maps them to Unity libraries.

## Options

| Library | Notes | Status of these notes |
|---|---|---|
| **Mirror** | Open source, community-maintained, UNET-style API (`NetworkBehaviour`, `[Command]`, `[ClientRpc]`, `[SyncVar]`, `NetworkIdentity`). Transports are pluggable (KCP default, Steam and relays via add-ons) | Field-tested in a listen-server co-op project |
| **Netcode for GameObjects (NGO)** | Unity's first-party library (`NetworkObject`, `NetworkVariable<T>`, `[Rpc(SendTo.Server)]`, Unity Transport, Relay/Lobby services) | Documentation knowledge; needs community verification |
| Fish-Net, Photon Fusion, others | Different authority models; read their docs | Not covered |

Pick the library and version together with the user; the API names below must be checked against the version you adopt.

## Mirror: common mistakes

| Mistake | Result |
|---|---|
| Trusting `[Command]` arguments without server checks | A modified client skips the challenge |
| Assigning a `[SyncVar]` on a client | Not synced; host and client diverge |
| Network components on an object without `NetworkIdentity` | Never syncs |
| Runtime prefabs not registered for spawning | Visible on the host only |
| Rigidbody simulated on server and clients | Jitter, double forces |
| Forgetting SyncVar hooks and RPCs also run on the host | Logic runs twice on the host |
| Not releasing ownership on disconnect/rejoin | Objects held forever; soft-lock |
| `requiresAuthority = false` commands | Banned by guardrail; see [guardrails](guardrails.md) |

## NGO equivalents (needs verification)

| Concept | NGO |
|---|---|
| Replicated state | `NetworkVariable<T>` with server write permission |
| Client → server request | `[Rpc(SendTo.Server)]` (older: `[ServerRpc]`); validate the sender's client ID on the server |
| One-off effect | `[Rpc(SendTo.ClientsAndHost)]` / `[ClientRpc]` |
| Spawn | `NetworkObject.Spawn()` on the server; prefab in the network prefabs list |
| Authority check | `IsServer`, `IsOwner` |

## Running several instances

- Builds: `pwsh tools/Start-Game.ps1 -Exe <build> -Instances <n>` (host first, then clients; per-instance logs and window screenshots). Host/client arguments are defined once the game has a connect entry point.
- In-editor: Unity's Multiplayer Play Mode package runs extra virtual players from the editor (Unity 6). Mirror and NGO both work with it; ParrelSync is the older community alternative. Treat these as M1/M2 conveniences; M3 still needs separate machines.

## Logging for verification

Make connect, spawn, ownership and game-state changes log through the logging wrapper with a category, so a multi-instance run can be judged from logs alone.
