# Handoff and context management

> Record state, evidence, constraints and the next action so the next session can resume without guessing, and avoid working from the wrong context in long sessions and large files.

---

## 1. Handoffs

### Where they go and who reads them

- **Work records**: progress, command results, dead ends and what to resume go to `docs/work/{date}/{topic}.md`. `{date}` is the day first written (`YYYY-MM-DD`), `{topic}` a kebab-case task name. Continuing work updates the original.
- **Pointer**: add or update one line in [`docs/work/pointer.md`](../work/pointer.md) with date, summary, link and status. Do not copy the body.
- **Source-of-truth docs** (`docs/project/`, `docs/ai/`, `docs/engine/`): when a work record's conclusion becomes a rule or a design decision, write the result and its limits into the source doc as current fact. Source docs must make sense without reading work records.
- Work records are committed. No secrets, accounts or personal machine paths.

### When to write one

- The session ends before the work is done
- **Waiting for a multi-client test** (the most common reason to pause)
- Waiting for a human to approve a model or asset
- Only some of several steps are complete
- Uncommitted work remains

### Writing principles

- Keep observed facts apart from guesses.
- Record completion claims with their evidence.
- Do not record dynamic values from memory; write how to re-check them.
- Write the next session's reading order and first actions as imperatives.
- Use the status vocabulary from the [verification playbook](03_VERIFICATION_PLAYBOOK.md).

### Template

```markdown
# Handoff: {{task name}}

Written: YYYY-MM-DD
Branch: {{branch}}

## 1. Goal
- Final state:
- Source docs:

## 2. Done
| Item | Evidence | Status |
|---|---|---|

## 3. Not done
| Item | How far it got | Where it is stuck |
|---|---|---|

## 4. Repository state
- Committed:
- Uncommitted changes:
- Scenes/levels/prefabs edited:
- New data assets:

## 5. Verification
- L1:
- L2:
- L3 / multiplayer grade:
- Unverified items and why:

## 6. Blockers
- [ ] Multi-client test (M2+) needed: checklist of what to check
- [ ] Human approval of an asset or effect needed: preview path
- [ ] Game design decision needed: which options

## 7. First actions for the next session
1.
2.
3.

## 8. Cautions
- Changes that must not be reverted:
- Files being edited in parallel:
```

### Always record

| Item | Why |
|---|---|
| Names of scenes/levels edited | If the next session opens another one, the work seems to be missing |
| Paths of new data assets | They often need values filled in the editor before anything works |
| Multiplayer grade reached | M0 versus M2 decides how much the result can be trusted |
| Asset approval state | Automated checks passing and human approval are different things |
| Whether you stopped with a broken build | Never hand over a broken build |

### Phase boundaries

The project must be **runnable** at the end of every phase. Never hand over with a broken build.

| Good boundary | Bad boundary |
|---|---|
| Player movement synced (grabbing comes next) | Half a class written |
| One character ability finished | Four abilities at 30% each |
| Server logic finished, UI next | Server and UI half-done together |

Stable point check: builds · done definition met · commit status recorded · next first action written.

---

## 2. Context management

### Reading strategy

| Situation | Approach |
|---|---|
| Looking for a feature | Search by symbol or file name, then read only that section |
| Scene/level/prefab files | **Never read them whole.** They are mostly noise (YAML, `.tscn`, binary `.uasset`). Search by object or component name |
| Data assets | Look only at the fields you need |
| Design docs | Use the table of contents; open only the relevant section |
| Logs | New errors first. Classify pre-existing warnings separately. Keep instances apart |
| Large CSV/data tables | Filter to the rows and columns you need |

If you need the structure of a scene, ask for a screenshot of the editor's hierarchy/outliner instead.

### Order of trust

When information conflicts, decide in this order:

1. Current code and configuration: what actually runs
2. `git status` / `git diff`: what changed right now
3. [`AGENTS.md`](../../AGENTS.md) and the collaboration rules: the approved contract
4. `docs/project/` design docs: design intent
5. Earlier handoffs: past state
6. State descriptions in past conversation: re-check against current code

The user's latest explicit instruction is different from a state description: it sets permissions, requirements and priorities, and old code or docs never override it.

When a number in a design doc and the code disagree, **the code wins; report the difference.**

### Long-session warning signs

| Sign | Response |
|---|---|
| You need to re-check a file you read earlier | Read it again. Do not rely on memory |
| You are touching several systems at once | Split the work |
| More than 10 files changed | Review scope and verify |
| The original request feels blurry | Re-read the task brief |
| The conversation was summarized | Summaries lose detail; "do not" constraints and exceptions drop out first. Re-read the brief and the rule text |
| Multi-hour, multi-step work | Keep a checklist in a work record and tick items off |

**Re-read every changed file before reporting.** When editing the same file several times, re-read its current content each time. "It was like this a moment ago, so it still is" is the most common source of errors.

### Search rules

- Search for the exact symbol, file name or config key first
- Too many results: narrow by directory and extension
- Zero results: check for renames, moved paths, or generated code
- Exclude engine metadata and caches from results (see `docs/engine/version-control.md` for the folder list)
