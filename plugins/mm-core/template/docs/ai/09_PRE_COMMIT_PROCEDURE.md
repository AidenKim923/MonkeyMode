# Pre-commit procedure

> Before **applying** code (commit, merge, hand back), follow steps 1-4 below in order. Do not skip or reorder them.
> Commit and push still happen only on the user's explicit request ([execution policy](01_AGENT_EXECUTION_POLICY.md)). Run this procedure after receiving that request, and before telling the user something is done.

The one-shot command for your engine (static parts of 1-3 plus tests for the affected scope) is listed in `docs/engine/build-and-test.md`. Tool details: [self-verification tooling](10_SELF_VERIFICATION_TOOLING.md).

---

## 1. Understand the diff

- Check changed files with `git status` and `git diff`, including untracked files.
- Do not stop at the file list. **Read the changed functions, classes and modules, and the core logic added or removed**, and summarize them.
- Confirm the whole change belongs to this task. If changes from other workers or the user are mixed in, handle them separately.

## 2. Trace the impact

Do not look only at the edit points. Trace **all** of these:

| Trace | How |
|---|---|
| Callers and references | Search for the names of changed types and methods |
| Dependency paths | Follow module dependency directions (assemblies, crates, modules) to find dependents |
| Serialized references | Do scenes, prefabs/blueprints or data assets use the changed type or field? Renaming a serialized field silently breaks saved data |
| State transitions | Effects on game state, ownership, and session (join, leave, rejoin, reset) |
| Networking | Do request/replication contracts or the authority boundary change? If yes, M2 from [authority and testing](04_NETWORK_AUTHORITY_AND_TESTING.md) is mandatory |

What tools cannot find (editor wiring, string references) goes down as `not found in the searched scope`. Never conclude `no impact`.

## 3. Selective regression first

- **Do not rerun the full test suite and full build blindly.** Run the tests and checks directly related to the impact from step 2 first.
- Order: static guardrails (`uv run tools/guardrails/check.py --all`, engine module rules) → unit tests of affected modules → integration/play tests of affected modules → build and run only when needed.
- **For core changes with thin test coverage, add a verification scenario or test and run it.**
- For changes where UI, state or runtime behavior is the point, **secure verifiable results**: build/run logs, test result files, execution traces, screenshots. Summarize logs with `tools/Read-LogErrors.ps1` or your engine's equivalent.
- Run the full regression only when the impact is wide (core modules, network contracts, shared scenes) or a failure appears that selective regression cannot explain.

## 4. Self-fix loop

```
run check → failed? ── no → pass, report
               │
              yes → isolate the first cause from logs and messages → fix one thing → run the same check again
```

- On failure, do not hand it back to the user. **Fix it yourself from the failure cause and logs**, then verify again.
- Fix one thing at a time. With several fixes at once you cannot tell which one worked.
- **Do not work around symptoms.** Never pass a guardrail violation by editing rule files, adding allowlist entries or bypassing hooks (`--no-verify`). Fix the root cause the message points to. If you believe the rule itself is wrong, stop and ask the user with your reasoning.
- **Stop when the same failure repeats 3 times, or after 5 fixes in total without passing.** Report the fixes tried, the failure logs and your current hypothesis. Do not keep going and widening scope.
- Checks the environment cannot run (the editor holding a project lock, not enough instances for a multi-client test, ...) are not passes. Record them as `unverified` / `awaiting verification`.

---

## Final check before applying

- [ ] Ran 1-4 in this order (wrote down skipped steps and why)
- [ ] Read every changed file; nothing outside this task's scope changed
- [ ] Directly related tests for the affected scope pass; added them if missing
- [ ] Guardrails and module rules pass (no hook bypass)
- [ ] Screenshots and logs secured where there is a visible result
- [ ] The four items of the [completion report](06_RESPONSE_STYLE_GUIDE.md) can be filled in
