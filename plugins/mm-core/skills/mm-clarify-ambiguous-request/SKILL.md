---
name: mm-clarify-ambiguous-request
description: When a game-dev request is ambiguous or open to several readings, narrow it down with the code and docs first, then ask specific confirmation questions instead of implementing or guessing. Use when the target (file, scene/level, system) is unspecified, the scope is unclear, implementation choices lead to different results, the request leans on an item listed as Undecided in AGENTS.md, or the instruction is abstract ("fix this", "clean this up", "make it better").
---

# Clarify an ambiguous request

## When it applies

Follow this skill before changing code if any of these hold:

- A pointer with no target: "fix this", "make it better", "tidy this up"
- A target but no scope: which scene/level, folder or script, and how far to go
- Implementation choices diverge and change the result: storage location, naming, UI approach, whether something is networked
- The request depends on an item listed under **Undecided** in `AGENTS.md` (for example networking library version, platform services, save format, supported player counts, camera, voice chat)
- The change could affect other code, docs or parallel work and the scope is uncertain

It pairs with the fact/guess/unverified split in `docs/ai/06_RESPONSE_STYLE_GUIDE.md` and with "report options and impact, do not settle them silently" in `docs/ai/01_AGENT_EXECUTION_POLICY.md`. This skill covers the case before that: when it is not even clear what to recommend.

It does **not** apply when the request is concrete and its target and scope are clear, or when `AGENTS.md`, `docs/ai/`, `docs/engine/` or the guardrails already decide the answer. Then just do it. Do not ask every time.

## Who you are talking to

Read `.monkeymode/config.json` (written by `mm-setup`). If `coding_level` is `cannot-read-code`, phrase options in terms of what the player or the user will see, not in terms of code, and keep each option to one plain sentence. If the file is missing, ask in plain language.

## Method

1. **Do not fill gaps with guesses.** Never settle an undecided value with a plausible default and carry on. Leave it undecided and report the options and their impact.
2. **Narrow it with code and docs first.** Do not ask what reading can confirm. Leave only the points only the user can decide.
3. **Offer choices.** For choosing between UI mockups or image-based game assets, use `mm-decision-picker` to put a choice page on the local server. Otherwise use the agent's question tool (AskUserQuestion in Claude Code) or a short numbered list. Give 2-4 alternatives with the evidence you found, not an open question. Mark the recommended one first with "(recommended)". When there is a real technical trade-off, analyze it first with `mm-present-alternatives`.
4. **Ask only what execution needs.** Bundle independent decisions into one round; ask dependent questions in sequence.
5. **Apply the answer and proceed.** Do not ask the same thing again.

## Example

```
User: "Make player movement"

✗ Immediately write rigid-body movement plus network sync on your own
✓ Check first → existing scripts, input action assets, whether networking is installed
   → follow what the rules already decide (folders, modules, logging, banned APIs) without asking
   → ask only where results diverge: networked in this scope or not,
      kinematic controller or physics body, does it depend on the camera model (undecided)
```
