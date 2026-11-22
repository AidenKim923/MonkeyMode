# Verification playbook

> Tie every completion claim to real evidence, and match the depth of verification to the risk of the task.

---

## 1. Principles

- Judge "done" by observed state, not by intent.
- Link every claim to an actual run result, log, artifact or reproduction record.
- Mark what you could not check as `unverified`.
- Never present a failed or skipped step as a success.
- Visual results (models, animation, effects, feel) are unverified without a capture or a human's confirmation.
- Flag pre-existing defects outside the edit scope separately; do not mix them up with failures of the current task.

---

## 2. Evidence grades

| Grade | Name | Accepted when | Rule |
|---:|---|---|---|
| 0 | Claim only | Described with no run result | Never used in a completion report |
| 1 | Static check | Compiles, zero console/compiler errors, guardrails pass | Not enough on its own for a behavior change |
| 2 | Functional check | Target behavior observed at least once in a test scene/level or test | Raise to grade 3 if networking is involved |
| 3 | Integration check | Happy path and regressions pass **with several clients connected (M2 or above)** | Required for networking, scene/level structure and initialization changes |

---

## 3. Status vocabulary

| Status | Meaning |
|---|---|
| `done (verified)` | Required level and evidence grade both met |
| `implemented (unverified)` | The deliverable exists, but the required behavior check has not happened |
| `conditional pass` | No blocking defect, but warnings or unverified items remain |
| `diagnosed, not fixed` | Cause and options known; nothing changed |
| `awaiting verification` | Implementation finished; waiting for an environment or for people |
| `awaiting approval` | An asset or effect is waiting for a human's visual approval |
| `failed` | The required check reproduced a defect |
| `blocked` | Cannot proceed safely without an approval, input or environment |

**`awaiting verification` is common in multiplayer games.** A multi-client test needs several instances or several people. When only one instance is possible, stop at M0/M1 and say `awaiting verification`. That is the honest status.

---

## 4. Test levels

### Automated checks

Do not assume CI checks asset metadata, LFS or builds unless your repository actually has that CI. The scripts in `tools/` do the same work locally ([self-verification tooling](10_SELF_VERIFICATION_TOOLING.md)). Run the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) before committing and record the commands you ran and their results.

Unit and integration test frameworks and their folders are engine-specific: see `docs/engine/build-and-test.md`.

### L1: static checks

Apply to every code change.

- The change matches the task contract
- Zero compile errors and **no new** warnings
- Keep pre-existing warnings apart from new ones

For gameplay runtime code, also check statically:

| Rule | Check | On violation |
|---|---|---|
| `no_comment` | `tools/guardrails/check.py` reports zero comments (when the profile enables it; [guardrails](12_GUARDRAILS_INSTEAD_OF_COMMENTS.md)) | `error` |
| `banned_api` | The same check reports zero banned APIs or patterns ([list](13_BANNED_APIS.md)) | `error` |
| `module_boundary` | Module dependency directions follow the engine adapter's rules | `error` |
| `authority_boundary` | No client finalizes game state, ownership or win conditions; every client request is validated on the server | `error` |
| `state_pipeline` | Condition ID → server validation → state change → sync → presentation, in that order | `error` |
| `reset_safe` | Can the challenge/encounter reset after failure? Is it safe against leaving, rejoining and duplicate input? | `error` (soft-lock risk) |
| `async_lifecycle` | Coroutines/tasks/timers block double starts and clean up and restore state on completion, cancel, disable and destroy | `error` if state can leak |
| `runtime_lookup` | No repeated scene-wide lookups or component fetches inside per-frame loops | `error` if repeated |
| `tick_lifetime` | Is the per-frame update really needed? Does it stop when idle? | `warning` without a reason |
| `balance_constant` | Tuning numbers (distances, times, masses, damage) are not code constants | `warning` |

### L2: functional checks

Apply to behavior changes.

- Run the related automated tests and record the pass count
- Run the target behavior in a test scene/level
- Try the normal input and the main failure inputs (out of range, duplicate, no permission)
- Record the reproduction steps and what you observed

### L3: integration and multiplayer checks

Apply to networking, scene/level, initialization and shared-state changes.

**Follow the test grades in [Network authority and testing](04_NETWORK_AUTHORITY_AND_TESTING.md).**

- M2 at minimum
- Timing- and physics-sensitive features: M3 plus injected latency
- Check from the host's view **and a client-only view** (never the host screen alone)
- Timing bugs are probabilistic: repeat at least 10 times

---

## 5. Minimum verification by risk

| Risk | Typical impact | Minimum |
|---|---|---|
| Low | Docs, UI text, logs | L1 |
| Medium | Logic inside one system, tuning values | L1 + L2 |
| High | Shared state, scene/level structure, initialization order, game state, physics objects | L1 + L2 + L3 |
| Critical | Network authority boundary, shared scenes, `.gitattributes`, bulk delete or move | Full L3 + prior approval |

With several risk signals, apply the highest level.
**Never lower the level because verification is expensive. Shrink the task instead.**

---

## 6. Asset verification

Models and props must pass both the automated checks in the [asset pipeline](../guides/asset-pipeline-blender.md) and a human approval.

| Claim | Evidence needed |
|---|---|
| Meets the spec | validation.json (triangle count, scale/rotation, pivot, missing mesh/material, normals) |
| Shape and style are right | preview.png + **human approval**. Until then: `awaiting approval` |
| Usable in the engine | Zero import warnings (or recorded), prefab/blueprint collider checked, placed in a test scene/level |
| A gameplay prop works | L2 above; L3 for props with synced state |

Generative modeling alone does not guarantee rigging, animation or collision quality. Do not write "done" because automated checks passed.

---

## 7. Recording results

```markdown
| Claim | Level | Grade | Means | Actual result | Status |
|---|---|---:|---|---|---|
| When two players grab the same object at once, only one holds it | L3 | 3 | M2 (host + 3 clients), 20 runs | 20/20 correct | done (verified) |
| Holder state matches at 150 ms latency | L3 | 0 | none | not run | awaiting verification |
```

Before reporting, check:

- Does every completion claim have grade 1 evidence or better?
- Does every behavior change have grade 2 or better?
- Does every networking change have grade 3?
- Are unverified items listed with reasons?
- Are new defects kept apart from pre-existing ones?

---

## 8. Independent review

Do not hand the reviewer the worker's self-assessment. Give only:

- The task contract and edit scope
- The current diff
- The original text of the rules to apply
- The verification procedure

Reviewer contract: modify no files · judge only what was checked · do not guess when an environment is missing · mark pre-existing defects `legacy: true` · keep each fix suggestion to one sentence.

| Verdict | Meaning | Next |
|---|---|---|
| `PASS` | No blocking defect and no unverified core item | Next step |
| `CONDITIONAL` | Warnings, or items unchecked because of the environment | Fill the gap, re-review only that part |
| `REJECT` | Error, authority violation, scene conflict, scope breach | Stop, fix, re-review |

```json
{
  "verdict": "PASS | CONDITIONAL | REJECT",
  "checked": ["items checked"],
  "findings": [
    {
      "severity": "error | warning | info",
      "rule": "authority_boundary",
      "file": "path/to/NetworkedGrabbable",
      "line": 0,
      "evidence": "what was observed",
      "suggestion": "one-sentence suggestion",
      "legacy": false
    }
  ],
  "unverified": ["item and reason"],
  "multiplayer_grade": "M0 | M1 | M2 | M3"
}
```

Never return `PASS` while `findings` contains an error or warning.
