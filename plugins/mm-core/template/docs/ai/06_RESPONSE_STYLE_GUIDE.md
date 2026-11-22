# Response style guide

> One format for agents' reports and how they cite evidence. Keep it short.

## 1. Completion report

When work is finished, report these four items.

```markdown
## 1. Changes
What changed and how

## 2. Impact
Which related features or modules this can affect

## 3. Verification
Which tests, builds and runs were done and what happened. Include failures and re-fixes.
| Claim | Means | Result | Status |
|---|---|---|---|
Absolute paths of screenshots and logs, if any

## 4. Follow-ups / guardrail proposals
Lint rules, tests or structural changes that would stop the same mistake. "None" if none.
```

- Exactly these four items. If the result is blocked or needs a user decision, put one line before them saying so.
- Item 3 uses the [evidence grades and status vocabulary](03_VERIFICATION_PLAYBOOK.md). Write what you could not verify as `unverified` / `awaiting verification`, with the reason.
- Item 4 follows the criteria in the [guardrails doc](12_GUARDRAILS_INSTEAD_OF_COMMENTS.md). Propose only; do not edit rule files without approval.
- If the list of changed files is long, summarize it or use `git diff --stat`.

## 2. Principles

- **Conclusion first.** Do not open with the process.
- Separate facts, guesses and unverified items.
- When you could not find or confirm something, say how far you looked (paths, commands).
- Do not write "it works" about something you did not verify. Never dress up a failure as a success.
- Mark pre-existing defects outside the scope separately.
- Avoid vague pointers like "this one" or "over there". Name the host or client, the file, the object.
- For assets, keep "passed automated checks" apart from "approved by a human".

## 3. Phrases to avoid

| Avoid | Say instead |
|---|---|
| "Implemented perfectly" | "Implemented and verified to L2. L3 is unverified" |
| "This should work" | "I could not confirm it works. It needs a multi-client test" |
| "No problems" | "Within what I checked (host + 1 client, 10 runs), there was no mismatch" |
| "The model turned out great" | "Validation passed; the preview is awaiting human approval" |
| "I tested it" | Grade, player count, number of runs, result |

## 4. Player count and grade

Always state the grade and the player count for multiplayer checks. Example: `M2 (host + 3 clients, same machine), 20 of 20 runs matched`.
