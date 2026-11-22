# From design docs to tasks, and parallel work

> Turn design documents into implementable tasks, and keep several tasks running at once from colliding.

---

## 1. Structure the source

Pull these apart from the design doc:

| Item | What to record |
|---|---|
| Goal | The experience the player should get |
| Actors | Player characters, systems, NPCs |
| Inputs and outputs | Controls, events, UI, collectibles |
| Rules | Conditions, priorities, exceptions, numbers |
| State changes | What is created or modified, and who owns it |
| **Networking** | Server authority or client local |
| Verification criteria | Observable success and failure conditions |

**Design docs do not say what is networked; the implementer decides** ([the rule](04_NETWORK_AUTHORITY_AND_TESTING.md)). Keep facts from the source, facts confirmed in code, and the analyst's guesses in separate columns.

Design docs mix in assumptions (for example "a 3-second glide (initial assumption)"). Do not promote assumptions to fixed values. Put them in data assets so they stay tunable.

## 2. Trace the current implementation

Do not settle which code is responsible from a keyword search alone.

1. Find the entry event or public API
2. Trace call relationships and the owner of the data
3. Check data assets and initialization order
4. Record anything not found as `not found in the searched scope`, not `none`

## 3. Gap analysis table

```markdown
| ID | Requirement | Current implementation evidence | Status | Change needed | Network | Verification |
|---|---|---|---|---|---|---|
| R-01 | A large character can lift a small one | (none / attachment component) | Not implemented | Socket attachment + server validation | Server authority | L3 after M2 |
```

Judge `Status` by **whether the required behavior is met**, not by whether code exists. Similar-looking code does not make it `met`.

## 4. Impact decisions

Apply to every candidate change:

- Does it handle values that affect the outcome? → server authority
- Which scene/level must change? → shared ones need approval
- Are there numbers? → move them to a data asset
- Is it on the out-of-scope list? → needs approval
- Is it hard to undo? → needs approval
- Does it settle an undecided item? → report options

## 5. Narrow the open questions

Use questions only for **decisions local research cannot answer**. Each question includes: confirmed facts and their evidence · what is blocked until it is decided · mutually exclusive options · cost and risk of each · a recommendation with reasons. Never send back to the user a question that code search or reading docs would answer.

## 6. Implementation plan

Split the work into independently verifiable phases.

```markdown
### Phase N: {{result}}

- Targets:
- Preconditions:
- Work:
- Done definition: (observable)
- Verification: L? / M?
- Rollback boundary:
- Approval needed: none / {{what}}
```

**The project must run at the end of every phase.** A plan where everything only works together weeks later is risky.

Use the milestone roadmap's order as phase boundaries, but expect it to be ambitious. **Validate networked physics and game feel before expanding content.**

## 7. Review the output

- [ ] Every requirement is traced to a row in the gap table
- [ ] Current implementation evidence is at file and symbol level
- [ ] No guess or unconfirmed item is written as fact
- [ ] Network authority and scene ownership are decided
- [ ] Numbers are moved to data assets
- [ ] Only real decisions are left as questions
- [ ] Every phase has an observable done definition
- [ ] Unimplemented analysis is not reported as `done`

---

## 8. Parallel work

When the user hands over several independent requests at once, use one session per request ([token and session policy](11_TOKEN_AND_SESSION_POLICY.md), section 2). This section covers how to avoid write conflicts inside that.

### When to split

| Worth splitting | Do not split |
|---|---|
| Independent systems (a character ability vs. prop production) | Work that touches the same scene/level |
| Read-only research from several angles | Work whose interfaces are not settled yet |
| Several props in Blender (each item independent) | Sequential work where one output feeds the next |
| Several separate docs | Shared data assets edited together |

**Two tasks touching the same scene/level must not run in parallel.** Scenes do not merge; do them in sequence.

Splitting has a cost. Do not split ordinary coding that one context can finish. Splitting pays when it prevents these failures:

| Failure when one context works too long | How splitting prevents it |
|---|---|
| Handles part of the list and believes it is finished (35 of 58 props) | One worker per item; the parent reconciles the total count |
| Grades its own work generously | A reviewer in a fresh context, separate from the worker, judges |
| Goal and constraints blur over a long run | Each worker gets the rule text and a narrow goal directly |

### Roles

- **Parent**: fixes the brief and the split, assigns each worker **exclusive** read/write scopes, owns shared state, integration and final verification, and checks the evidence behind each worker's report (files, lines, command output).
- **Worker**: researches and edits only its assigned scope. When blocked, report the blocker instead of widening scope to get around it.
- **Reviewer**: judges read-only in a fresh context, separate from the workers ([verification playbook](03_VERIFICATION_PLAYBOOK.md), section 8).

### Avoiding write conflicts

1. Assign each file to exactly one worker
2. **Never assign scene/level files to parallel workers**
3. The parent alone edits shared data assets, global settings and manifests
4. Items being moved or renamed are excluded from parallel writes
5. Items the user is editing are excluded from write scopes
6. After completion, the parent integrates once and runs the static checks

### Work contract (given to each worker)

```text
Goal:
Read scope:
Write scope:
Forbidden scope:
Scenes/levels to edit: (none / test scene name)
Network impact: (none / server authority)
Deliverable:
Done criteria:
How to verify:
What to report when blocked:
```

Do not pass only the parent's summary; important constraints get lost. Give workers the rule text itself.

### Standard pipeline

```
[parent] fix brief → assign exclusive scopes → [workers] run independently
  → [parent] integrate + static checks → [reviewer] read-only verdict → [parent] fill gaps or final report
```

### Before finishing

- Did write targets stay disjoint?
- Were no scene/level files edited in parallel?
- Did only the parent change shared state?
- Did every worker use the same done criteria?
- Did the reviewer avoid relying on the workers' self-assessment?
- Did final verification cover the integrated result?
