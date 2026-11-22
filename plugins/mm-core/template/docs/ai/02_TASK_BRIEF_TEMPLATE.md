# Task brief template

> Give the reason for the task together with its execution contract, to cut scope drift, over-building and unsupported "done" claims.

## How to use it

- Write outcomes and constraints; leave the implementation order to the worker.
- For a quick lookup or a typo fix, fill in only the fields you need.
- Do not guess unclear values. Write `{{undecided}}`.
- For analysis-only requests, say explicitly that nothing may be edited.
- Pick the verification level from the [verification playbook](03_VERIFICATION_PLAYBOOK.md).

---

## Template: feature or bug

```markdown
# {{Task name}}

## Background
- Why this task is needed:
- Source docs: {{docs/project/ doc and section}}

## Deliverable
- Final form:
- Included this time:
- Deferred:

## Impact
- Scenes/levels to edit: {{test scene / none}}  (shared scenes need approval)
- Network impact: none / new server authority / sync change
- Data impact: none / new data asset / existing values change
- Related mechanics or abilities:
- Which milestone done-criterion this serves:

## Scope
- May read:
- May edit:
- Excluded:

## Constraints
- Must keep:
- Needs approval first:
- Touches anything on the out-of-scope list: {{confirm: no}}

## Done criteria
- [ ]
- [ ]
- [ ] Report verified results and unverified items separately

## Verification
- Risk: low / medium / high / critical
- Minimum level: L1 / L1+L2 / L1+L2+L3
- Multiplayer grade: M0 / M1 / M2 / M3
- Success signal to observe:
- Stop or roll back if:
```

## Variant: asset production [Blender]

```markdown
# Produce {{asset ID}} (ID from your asset inventory)

## Input
- Inventory row: {{ID, stage, asset, priority, role, behavior}}
- Reference images / style: {{style keywords from the art direction}}

## Spec (from docs/guides/asset-pipeline-blender.md)
- Name: {{e.g. prop_crate_small}}
- Triangle budget: {{small prop 100-1,000 / character 3,000-8,000}} (initial budget, not a hard limit)
- Units, pivot, collider: {{1 BU = 1 m, pivot location, box/capsule/convex}}
- Animations or states needed: {{none / open, closed, ...}}

## Deliverables
- .blend, .fbx or .glb, preview.png, manifest.json, validation.json
- Location: {{source store outside the engine project / imported folder}}

## Done criteria
- [ ] Automated checks pass, or the reason is recorded (missing mesh/material, normals, triangle count, scale/rotation, pivot, export)
- [ ] A **human approved** preview.png (until then: `implemented (unverified)`)
- [ ] Engine import warnings checked, prefab collider checked
```

## Variant: analysis only

```text
Investigate read-only. Do not modify any file.
Report the cause, the options, their impact and the evidence, then stop.
Any fix is a separate, separately approved task.
```

---

## Example: grabbing objects in a co-op game

```markdown
# Grab objects (networked grabbable)

## Background
- Core co-op interaction: players pick up and carry crates and fuses. Several players may try to grab the same object at once.
- Source docs: docs/project/<architecture doc> "Networking", <mechanics doc> "Shared actions"

## Deliverable
- Final form: a networked grabbable component, a grab request from the player's interaction component, an occupancy check
- Included this time: grab request (client → server), server-side distance/occupancy/ownership check, sync to every client, release
- Deferred: grab animation, carrying other players

## Impact
- Scenes/levels to edit: a dedicated test scene (not a shared scene)
- Network impact: server authority. Only the server changes who holds the object
- Data impact: grab distance and max mass live in a data asset
- Milestone done-criterion: "grab, push and carry states match on every client"

## Done criteria
- [ ] A grab is accepted only within grab distance
- [ ] When two players request at the same time, exactly one holds the object
- [ ] If the holder disconnects, the object is released and can be grabbed again
- [ ] The host and all clients see the same holder
- [ ] No tuning value is a code constant

## Verification
- Risk: high (shared state, networking)
- Minimum level: L1 + L2 + L3, multiplayer grade M2
- Success signal: on every instance the same object sticks to the same player only, and releases on all of them at once
- Stop if: one object is held by two players at once; stop and re-examine the decision path
```

---

## Check before you send

- Is the goal written as an observable result rather than implementation steps?
- Do the editable scope and the excluded scope stay apart?
- Does every done criterion have a way to check it?
- Did you review network impact and scene ownership?
- Does it stay clear of the out-of-scope list?
