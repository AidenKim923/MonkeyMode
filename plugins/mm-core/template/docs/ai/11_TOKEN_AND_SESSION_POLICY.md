# Token cost, search cost and sessions

> Avoid needless expensive reasoning and context use. Apply this together with the reading tips in [handoff and context](05_HANDOFF_AND_CONTEXT.md).

## 1. Split work by weight

| Kind | Examples | Handling |
|---|---|---|
| Light | Classification, formatting, rename suggestions, static lookup (finding files and symbols), log summaries, repeated check runs | Cheapest model, low reasoning effort, narrow context. Do not ask a model to do what a script can |
| Heavy | Design, authority-boundary decisions, root-cause analysis, multi-file edits, writing game rules | Stronger model, enough reasoning. Read only the files the decision needs |

- Do not do light work inside a heavy context. Hand search and summaries to a sub-agent (exploration) or a script and bring back **only the conclusion**.
- Claude Code: delegate exploration and summaries to a read-only sub-agent or a cheaper model. Codex: run with lower reasoning effort. Check setting names against your tool's version.
- If unsure, start light and move up when the result is unclear or edits become necessary.

## 2. Several requests, several sessions

When the user gives **several independent requests** at once, do not work through them one after another in a single session. Split them.

- One request = one session. Each session holds only its request's brief and the rule text.
- Avoid write conflicts with a **separate git worktree** per session (`git worktree add`) or another isolated workspace.
- Do not split requests that touch the same file, the same scene/level or a shared data asset, or where one request's output is another's input. Sequence those and say why ([parallel work rules](08_PLANNING_TO_TASKS_AND_PARALLEL_WORK.md), section 8).
- **Do not split the work inside one request into several sessions.** Re-reading context costs more than it saves.
- The parent session checks each session's result against evidence (command output, files) before integrating, then runs the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) once more.

## 3. Narrow scope first

- Do not read the codebase or the docs from start to finish.
- Narrow in this order: **file path → module name → symbol → recent history** (`git log -- <path>`, `git diff`). Read the needed section only once the target is clear.
- Never read scene/level files whole. Search by object or component name.
- Open `docs/project/` by table of contents. Filter CSV/data tables to the rows and columns you need.
- Before reading, ask: "would reading this file change my decision?"

## 4. Incremental work and reuse

- Do not re-read or re-verify unchanged areas. Work from the **delta** (the change-scope output of your engine's tooling, or `git diff`).
- Reuse the scripts in `tools/` for repeatable checks. When a new repeated check appears, make it a script in `tools/` instead of hand-writing it in the conversation each time.
- Do not trust your memory of files you read earlier. Re-read the relevant section right before editing.
- Keep only conclusions and evidence paths in summaries. Do not paste long logs into the conversation; use the `Read-LogErrors` summary and the log path.
