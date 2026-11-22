# Game dev workflow

> The order MonkeyMode runs its `mm-` skills in, from idea to shipped story, and where each output goes. Ask `mm-help` at any point: it reads `_mm/_config/mm-help.csv` and your outputs and recommends the next step.

## Where things go

| Kind | Location | Rule |
|---|---|---|
| Working drafts from skills (brief, GDD, architecture, epics, stories, sprint status) | `_mm-output/planning-artifacts/`, `_mm-output/implementation-artifacts/` | Drafts. Skills read and update them |
| Lasting, approved design decisions | `docs/project/` | Written as current fact: no dates, no change history. Promote only after the user approves |
| Progress, work notes, handoffs | `docs/work/{date}/{topic}.md` + one line in `docs/work/pointer.md` | The only place for dates and history |
| Engine rules | `docs/engine/` | From the engine adapter; edit to match your project |

`AGENTS.md` and `docs/ai/` override any skill instruction they conflict with. Every `mm-` workflow is told so in its defaults (`persistent_facts` in its `customize.toml`).

## Recommended order

| Phase | Skill | Notes |
|---|---|---|
| 1. Pre-production | `mm-brainstorm-game` | Optional. Game-specific techniques on top of `mm-brainstorming` |
| | `mm-research` | Optional. Domain, market, competitive or technical research |
| | `mm-create-game-brief` | Highest-value input for the GDD |
| 2. Design | `mm-gdd` | The design source of truth. Choose Express or Facilitative. Numbers are assumptions until playtested |
| | `mm-create-narrative` | For story-driven games. Run before finalizing the GDD when the story feeds mechanics |
| | `mm-ux` | Camera, controls, HUD and screens are settled here, not in the GDD |
| | `mm-prd` | Optional: formal requirements or an external tool needs a PRD |
| 3. Technical | `mm-game-architecture` | Reads `docs/engine/architecture-addendum.md`. Leaves undecided tech behind interfaces, ends with guardrail proposals, offers an independent review |
| | Guardrail update | The user approves the proposals; then they are added to `guardrails/` |
| | `mm-generate-project-context` | Condenses the rules agents must follow while coding; seed it from `docs/engine/project-context.md` |
| | `mm-create-epics-and-stories` | Each story carries risk, verification level and multiplayer grade |
| | `mm-check-implementation-readiness` | Gate: GDD, UX, architecture and epics agree |
| 4. Production | `mm-sprint-planning` → `mm-create-story` → `mm-dev-story` → `mm-code-review` | Dev runs the [pre-commit procedure](09_PRE_COMMIT_PROCEDURE.md) and the four-part report before "done" |
| | `mm-sprint-status`, `mm-correct-course` | Status and replanning when off track |
| | `mm-retrospective` | After each epic |
| Testing | `mm-test-framework`, `mm-test-design`, `mm-test-automate`, `mm-e2e-scaffold`, `mm-test-review` | Engine knowledge for Unity, Unreal and Godot is built in; Bevy uses the adapter doc |
| | `mm-playtest-plan`, `mm-performance-test` | Feel and visuals need human approval |
| Anytime | `mm-quick-dev` (`mm-quick-dev-auto`) | Small changes without the full chain |
| | `mm-investigate`, `mm-document-project`, `mm-walkthrough`, `mm-review` | Debugging, documenting an existing project, guided review of a change, editorial and adversarial review |
| | `mm-party-mode` (mm-agents pack), `mm-advanced-elicitation` | Multi-agent discussion, deeper critique of the last output |

## Lessons baked into the defaults

- **Finalize late.** It is fine to leave the GDD at a reviewed draft while the narrative is designed; finalize once the story stops moving mechanics.
- **Batch volatile decisions.** Story details that will change (which NPC does what, episode endings) are collected as open items and confirmed together, not one by one.
- **Promote, do not copy.** When a draft decision is approved, write it into `docs/project/` as fact and leave the history in `docs/work/`.
- **Architecture gets a second reader.** A fresh-context reviewer (another model, or a clean sub-agent) reads the draft against the inputs; record each finding and what changed.
- **Undecided stays undecided.** Transport, save format, voice chat, platform services: interface now, decide later, with the user.
- **Guardrails come out of architecture.** Banned patterns and module directions the architecture implies become guardrail proposals, then rules.
