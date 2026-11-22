---
name: mm-present-alternatives
description: When a feature or design has several real implementation options, explain each option's pros and cons against this project's actual constraints (engine, networking model, server authority, banned APIs, guardrails) and recommend one with reasons. Use for decisions that are costly to reverse - architecture, adopting a package or plugin, data structures, sync strategy, save format - or when the user asks "what are the options?" or "which way is better?".
---

# Present alternatives

## When it applies

When there is no single obvious way and at least two options have real trade-offs:

- The user asks "what are my options?", "compare the pros and cons", "how should I build this?"
- A fork appears during implementation and the options differ in performance, complexity or maintainability
- Before a decision that is expensive to undo: architecture, a new package/plugin, sync strategy (server decides vs. client presents), data structures, save format

Not for: decisions with effectively one right answer, or already decided by `AGENTS.md`, `docs/ai/`, `docs/engine/` or the guardrails (just do it); pure taste (ask directly via `mm-clarify-ambiguous-request`); trivial choices where you would have to invent a third option.

## Method

1. **Read the real constraints first.** Judge by this project's conditions, not general theory.
   - `AGENTS.md`: core rules and the Undecided list
   - `docs/ai/04_NETWORK_AUTHORITY_AND_TESTING.md` (multiplayer games): what the server decides, multi-client verification cost
   - `docs/ai/13_BANNED_APIS.md`, `docs/engine/guardrails.md`, `docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md`: APIs and patterns you cannot use
   - `docs/ai/07_ASSET_AND_DATA_POLICY.md`: third-party assets and licenses
   - `docs/engine/project-context.md` and the engine's real manifests (package manifest, `project.godot`, `.uproject`, `Cargo.toml`): what is actually installed
2. **Separate decided from undecided.** Never treat an undecided item as fact.
3. **Keep only real candidates, 2-4 of them.**
4. **Write every option in the same frame**: one or two line summary / upsides / downsides and risks / impact under this project's conditions:
   - Does it conflict with the server-authority boundary (game state, ownership, physics, win conditions are decided by the host/server)?
   - Does it conflict with banned APIs, guardrails, or module dependency directions?
   - For a new package or third-party asset: compatibility with the engine version, license, and the fact that adopting it needs the user's approval
   - The cost of multi-client verification (M2)
5. **Recommend one explicitly.** If the evidence is thin or depends on an undecided value, recommend conditionally and say what must be decided first. Do not invent certainty.
6. **If the final choice is the user's**, hand over to the question step of `mm-clarify-ambiguous-request`. For UI mockups or image-based game assets, use `mm-decision-picker`. Never end with an analysis and nothing to choose.
7. When the choice comes back, proceed and do not ask again.

If `.monkeymode/config.json` says `coding_level: cannot-read-code`, describe each option by what the player and the user experience (feel, cost, risk, time), and keep code names out of the summary lines.

## Example

```
User: "How should a door's open state sync between server and clients?"

✗ List server authority vs client computation like a textbook and stop
✓ Check the authority rules in docs/ai/04 → compare "server decides one open/closed state,
   clients animate it locally" with "server streams animation frames" → recommend the first:
   the second wastes bandwidth and the animation can run locally on each client.
   Either way the host/server decides the state.
```
