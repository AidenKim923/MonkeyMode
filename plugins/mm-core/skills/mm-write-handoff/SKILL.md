---
name: mm-write-handoff
description: Write a handoff using the template in docs/ai/05_HANDOFF_AND_CONTEXT.md when the user asks for one ("leave a handoff", "wrap up where we are", "let the next session continue") or when a session is about to end with work unfinished. Writes docs/work/{date}/{topic}.md and updates docs/work/pointer.md; updates the existing record instead of creating a new one when the task already has one.
---

# Write a handoff

## When it applies

- The user asks for a handoff.
- The user says they are stopping and work remains ("that's it for today").
- Work paused waiting for a multi-client test (M2), a human approval of an asset or effect, or a game design decision.
- Only some of several steps are done, or uncommitted changes remain.

If the work is completely finished and no risk remains, do not create one.

## Where it goes

The source of these rules is the "Work records" section of `AGENTS.md`. If `AGENTS.md` names a different docs folder, use it instead of `docs/`.

- Write the handoff to `docs/work/{date}/{topic}.md`. `{date}` is the day it was first written (`YYYY-MM-DD`), `{topic}` a kebab-case task name.
- Then add or update one line in `docs/work/pointer.md`: date, summary, link, status. Do not copy the body.
- Records are committed. No secrets, accounts, or personal machine paths.
- If the user does not want a file, print the same template in the chat.

## Steps

1. **Check for an existing record.** If `docs/work/pointer.md` or the date folders already have a document for this task, update it instead of creating a new one. If it is unclear whether this continues an earlier task, ask.
2. **Collect facts; do not write from memory.** `git status`, `git log --oneline -5`, `git branch --show-current`, paths of edited scenes/levels, prefabs/blueprints and data assets, and the checks you actually ran with their results. For values you cannot confirm, write how to re-check them instead of a value.
3. **Fill the template.** Use the template (8 sections) in `docs/ai/05_HANDOFF_AND_CONTEXT.md` as is. Verification vocabulary comes from `docs/ai/03_VERIFICATION_PLAYBOOK.md`, networking from `docs/ai/04_NETWORK_AUTHORITY_AND_TESTING.md`. Separate facts from guesses sentence by sentence. Section 7 is written as ordered imperatives; section 6 says who must do what to unblock.
4. **Never leave out**: names of edited scenes/levels, paths of new data assets, the multiplayer grade reached (say so explicitly when M2 is unverified), the human-approval state of assets, whether you stopped with a broken build, and temporary settings that must be reverted.
5. **Report**: where you wrote it (or that you printed it), and which fields you could not fill and why.

## Never

- Fill unconfirmed values from memory or guesses
- Record unverified items as done
- Create a new document for a task that already has one
- Create the document without updating the pointer
- Change code or settings "while you're at it". This skill only writes the record
