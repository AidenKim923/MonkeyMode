# Agent execution policy

> Carry approved work through to the end without trampling project data or anyone else's changes.

---

## Principles

1. Pin down the request's goal, deliverable, edit scope and done criteria first.
2. If a reasonable default lets you continue, do not stop just to ask. Do not pause with "shall I continue?" at a step that needs no user input, and do not end by only describing the next step. Put progress notes in the same message as the next action. The only reasons to stop are [the stop conditions below](#when-to-stop-and-ask) and the approval table.
3. Do not stop at a plan or an analysis. Finish implementation and verification within the approved scope.
4. Read the current state and apply the smallest change. Prefer the existing structure and conventions.
5. Back every completion claim with tool output, test results or final file contents.
6. Mark anything you could not verify as `unverified`.

---

## Approval boundaries

List your project's folder layout in `docs/engine/project-context.md`.

### Proceed without approval

- Writing or changing in-scope gameplay code
- Tuning in-scope data assets
- Writing or editing docs under `docs/`
- Requested test scenes/levels and prefabs/blueprints (not shared ones)
- Read-only research and analysis

### Needs approval first

| Target | Why |
|---|---|
| Saving a shared scene or level (list them in `AGENTS.md`) | Scenes do not merge. Two concurrent edits lose one of them |
| Changing the network authority boundary, or the public contract of new synced fields, commands or RPCs | Ripples through many systems |
| Adding packages or plugins, changing the engine version | Affects everything. If `AGENTS.md` says the user installs a library, agents never install it |
| Editing original third-party or purchased assets | Changes are lost on update; licensing |
| Deleting files, bulk moves, bulk renames | Hard to undo. Engines that track assets by ID (Unity `.meta` GUIDs, Unreal redirectors, Godot UIDs) break references |
| Adding `.gitattributes` or LFS patterns | Not applied retroactively |
| Git commit or push | Only on an explicit request. When asked, run the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) first |
| Editing `guardrails/`, `.githooks/`, agent hook config, or the checking scripts in `tools/` | Agents must not be able to loosen their own guardrails. Put proposals in item 4 of the completion report |
| Introducing a tricky library not covered by the [banned API list](13_BANNED_APIS.md) | Libraries with hard lifetime, threading or state contexts need user review |
| Expanding scope (content past the current milestone, matchmaking, anything on the out-of-scope list) | Violates the milestone plan |
| Settling an undecided item (camera, platform services, save format, ...) | Game design decision |

### Never

- Revert the user's or another worker's changes without a reason
- Edit generated folders (engine caches, `target/`, build output; see `docs/engine/version-control.md`)
- Rewrite history (`rebase`, force push)
- Put secrets (API keys, tokens, accounts) into code, docs or external services
- Work around a guardrail failure with `--no-verify`, rule edits or allowlist entries ([guardrails](12_GUARDRAILS_INSTEAD_OF_COMMENTS.md))

---

Check what was already approved earlier in the conversation. Do not ask again for the same work just because it appears in the table above.

## Behavior boundaries

- A request for analysis or explanation is not approval to edit.
- Do not add refactors, cleanups or setting changes outside the requested scope.
- Look at the diff before reverting a file. If you cannot confirm the whole change is yours, do not restore the file.
- When several solutions exist and the choice affects game design, do not pick one silently. Report the options and their impact.
- **Do not widen scope "while you're at it".** On a small team, scope control decides whether the milestone ships.

---

## Standard order of work

1. Read the target files, related design docs and `git status` to get a baseline.
2. Check the relevant rules and the existing implementation.
3. **Decide whether the change touches networking** → [Network authority and testing](04_NETWORK_AUTHORITY_AND_TESTING.md)
4. Apply the smallest safe change.
5. Verify with the [verification playbook](03_VERIFICATION_PLAYBOOK.md).
6. On failure, isolate the first cause, fix one thing at a time, and verify again.
7. Report the result, where it changed, the evidence, what is unverified, and the remaining risk.

---

## When to stop and ask

Stop immediately and ask a specific question only when:

- A required permission or input is missing and there is no safe alternative
- Delivering the result would materially widen the approved scope
- A hard-to-undo operation is needed and the intent is unclear
- A game design decision is needed and the options lead to very different results (for example a movement ability's duration, or the camera model)
- A design doc and the code conflict and you cannot tell which is current

Before asking, finish whatever research and verification you can do safely.

**Never ask** what code search, config checks or reading files can answer.

---

## Failure and fallback

1. Do not repeat the same call under the same conditions.
2. Classify the failure: permission, input, tool state, environment, or verification failure.
3. Consider alternatives in this order: narrower scope, read-only check, a different method, manual reproduction.
4. Verify a workaround against the original done criteria.
5. If the work must move to another session, write a [handoff](05_HANDOFF_AND_CONTEXT.md).

### Engine-specific failures

Each engine adapter lists its typical failure symptoms and what to check first in `docs/engine/build-and-test.md` and `docs/engine/multiplayer.md`.

---|---|
| Compile errors will not go away | Is the editor still recompiling, or in Play Mode? |
| References show as Missing | Missing `.meta` file or GUID collision |
| Images or models show up as text | `git lfs install` and `git lfs pull` (once LFS is in use) |
| Scene changes do not appear | Is a different scene open? |
| Works on the host, broken only on clients | Authority boundary violation, missing `NetworkIdentity`, missing spawn registration |
| Commands from a client are ignored | The client has no authority over the object |
| Objects jitter on clients | Server physics fighting client interpolation; a client-side Rigidbody simulating too |

---

## Done criteria

Report done only when all of these hold:

- The requested deliverable actually exists.
- Nothing changed outside the approved scope.
- Required verification passed, or the reason it could not run is written down.
- Temporary settings and debug code are back to their original state.
- You have passed on the results and remaining items needed to decide the next step.

**A networked change is not `done` without a multi-client check at the grade your project requires (M2 by default; see [04](04_NETWORK_AUTHORITY_AND_TESTING.md)).**
