# Network authority and multiplayer testing

> Most multiplayer bugs **work fine in single player and only break with several people connected.**
> So "I ran it" is not evidence. What matters is what you checked and how.
>
> This doc is engine-neutral. The networking library, its API names and its pitfalls are in `docs/engine/multiplayer.md`. Skip this doc entirely if `<YourGame>` is single-player.

---

## 1. Server or client: the rule

Values that affect the outcome of the game are decided by the server (or the host acting as server).

| Server authority | Client local |
|---|---|
| Game/challenge state, success and failure conditions | Camera, input collection |
| Ownership of items and objects (who holds what) | UI display, highlights |
| Physics object positions and velocities | Cosmetic effects and sounds (no effect on outcome) |
| Doors, switches, levers | Journal/inventory screens (content read from server state) |
| Pickups and collectibles | Animation playback (the server sets the state) |
| Attachment state (carrying, mounting) | |

When in doubt, make it server-authoritative. Never build a flow where the client computes the result and the server follows.

### Request flow

```
input (client) → request (command/RPC/message) → server validation (condition ID, distance, ownership, permission)
  → server state change → sync (replicated state) → presentation on each client
```

The server must check: can the requester reach this object · distance · is it already held or processed · does the requester have the required ability · is the challenge at the right stage.

### Common mistakes (any library)

| Mistake | Result |
|---|---|
| Trusting request arguments without server validation | A modified client skips the challenge |
| Writing replicated state directly on a client | Not synced; host and client diverge |
| A networked object without its network identity component/registration | Never syncs |
| Spawning runtime prefabs/scenes without registering them for network spawn | Visible on the host only |
| Simulating the same rigid body on server and client | Jitter, forces applied twice |
| Forgetting that state-change callbacks also fire on the host | Logic runs twice on the host |
| Not releasing ownership/attachments on leave or rejoin | Objects held forever; soft-lock |
| Sending state as a one-shot RPC/event | Late joiners and rejoiners never receive it. State goes in replicated variables; RPCs are for one-off effects |

### Typical co-op rules (adapt in `AGENTS.md`)

- Grabbing: the server checks occupancy, distance and ownership; of simultaneous requests, only the first processed succeeds.
- Carrying another player or object: sync an attachment/socket state before reaching for physics joints.
- Player movement: start with server-authoritative movement; add prediction/reconciliation only when the feel demands it (that is a design change and needs approval).
- Every challenge must reset after failure and stay safe against leaving, rejoining and duplicate input mid-interaction.

---

## 2. Test grades

| Grade | Setup | When |
|---|---|---|
| M0 | One instance (host alone in the editor) | Compile checks, local logic |
| M1 | Host + 1 client on the same machine | Basic sync |
| M2 | Host + clients up to the **target player count** on the same machine | Multi-player logic, shared resources, co-op challenges |
| M3 | Host and clients on **different machines** | Real latency |

**A networked change needs M2 at minimum.** Working at M0 is not evidence.
Logic where the player count matters (all-players conditions, simultaneous requests, duplicate character choice) must be checked with every slot filled.

### Listen-server traps

A host runs server and client in one process with zero input latency. Therefore:

1. **Never pass a change by looking at the host screen.** A client-only instance must show the same result.
2. Works on the host but not on a client: almost always an authority violation or missing sync.
3. Test actions performed by the host's character **and** by a client's character. The result must be the same.
4. Latency and correction bugs do not show on one machine (latency ≈ 0). Check movement, physics and timing at M3.
5. Suspect server-only code paths that happen to work on the host by accident.

**Keep the M3 host on the same machine every run.** If the host changes, frame and tick measurements cannot be compared across runs.

---

## 3. Several instances on one machine

Launch several builds (`tools/Start-Game.ps1 -Exe <build> -Instances <n>` on Windows: host + clients, per-instance logs and screenshots). Host/client launch arguments are defined once the game has a connect entry point ([self-verification tooling](10_SELF_VERIFICATION_TOOLING.md)). Some engines can run several clients from the editor; see `docs/engine/multiplayer.md`.

Check before starting. If any item is off, the multi-client check does not count.

| | Why |
|---|---|
| ✅ Every instance runs **the same build / code version** | Version mismatch silently breaks serialization, connecting and sync |
| ✅ It is a development build (launch args and debug logs on) | Release builds may ignore arguments |
| ✅ The minimum start player count matches the test | With 1, the host starts alone and others cannot join |
| ✅ Logs are saved per instance | In one console you cannot tell who did what |
| ✅ Instances are distinguishable (window title, character, color) | You will mix up which screen is the host |

---

## 4. Scenario checklist

Pick what applies to the change.

### Connection and session

- [ ] Host + all clients join
- [ ] Duplicate character/slot choice is blocked (or allowed, per your design); simultaneous picks resolve on the server
- [ ] Movement and interactions match on every instance
- [ ] A client leaving and rejoining mid-session recovers state or is handled safely
- [ ] The session ends safely when the host leaves (mandatory for listen servers)

### Shared resources and concurrency

- [ ] Two players grabbing the same object at once: only one succeeds
- [ ] The carrier disconnecting releases the object
- [ ] Two players using the same switch at once keep state consistent
- [ ] Repeated input (button mashing) does not change game state twice

### Game state

- [ ] Device/challenge state matches on every client
- [ ] Collectibles match on every client
- [ ] Reset after failure returns every instance to the same state
- [ ] In a two-player combo action, one side leaving midway does not soft-lock

### Physics

- [ ] Server-driven objects sit in the same place on clients without jitter
- [ ] Pushing a heavy object: client input shows up as the server's result

---

## 5. Recording results

```markdown
## Multiplayer check: {{feature}}
- Grade: M2 (host + 3 clients, same machine)
- Build/commit: {{identifier}}
- Runs: 20
- Result per scenario: {{scenario: passes / attempts}}
- Mismatches observed: {{none / details}}
- Unverified: {{M3 latency, ...}}
```

Timing bugs are probabilistic. One pass is not a pass. Run at least 10 times and write down the count.
