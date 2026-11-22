# Multiplayer: Unreal Engine

> Engine-neutral rules and test grades: [`docs/ai/04`](../ai/04_NETWORK_AUTHORITY_AND_TESTING.md). Needs community verification.

## Built-in replication

| Concept | Unreal |
|---|---|
| Authority | The server. `HasAuthority()`; roles `ROLE_Authority`, `ROLE_AutonomousProxy` (owning client), `ROLE_SimulatedProxy` |
| Replicated actor | `bReplicates = true` (and `SetReplicateMovement(true)` for movement) |
| Replicated state | `UPROPERTY(Replicated)` / `ReplicatedUsing=OnRep_X`, registered with `DOREPLIFETIME` in `GetLifetimeReplicatedProps` |
| Client → server request | `UFUNCTION(Server, Reliable)` on an actor the client owns (its PlayerController, Pawn, or PlayerState); validate on the server |
| Server → owning client | `UFUNCTION(Client, Reliable)` |
| Server → everyone (one-off effect) | `UFUNCTION(NetMulticast, Unreliable)` |
| Relevancy and frequency | `NetCullDistanceSquared`, `NetUpdateFrequency`, dormancy |
| Newer stack | Iris replication (opt-in in UE 5.x), push-model replication for fewer property comparisons |

## Common mistakes

| Mistake | Result |
|---|---|
| Server RPC on an actor the client does not own | The call is dropped silently |
| State sent with multicast RPCs | Late joiners and relevancy changes miss it; use replicated properties |
| Changing replicated state on a client | Overwritten next update; local mismatch |
| Logic in `OnRep_` that must also run on the server | `OnRep_` does not fire on the server for its own changes (call it manually in C++ when needed) |
| Spawning replicated actors on clients | They exist locally only |
| Trusting movement/physics from clients | Cheating, desync; rely on `UCharacterMovementComponent` prediction or server physics |

## Testing

- PIE: Play → Number of Players `<n>`, Net Mode `Play As Listen Server` or `Play As Client` (dedicated server in background). Turn off **Run Under One Process** to get separate processes, which behaves more like real clients.
- Command line: `UnrealEditor.exe "<Project>" <Map>?listen -game -log` for the host and `UnrealEditor.exe "<Project>" 127.0.0.1 -game -log` for clients; packaged builds take the same map/URL arguments.
- Network emulation: Project Settings or console `NetEmulation.PktLag=150`, `NetEmulation.PktLoss=2` for M3-style latency without a second machine (still verify on real machines before calling M3).

## Online services

Sessions, invites and NAT traversal go through an Online Subsystem (Null for LAN, Steam, EOS). Keep the choice behind the game's session layer and decide it with the user.
