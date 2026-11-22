# <YourGame>: design source of truth

This folder holds the approved, lasting design of the game, written as current fact (no dates, no change history; that goes to `docs/work/`).

MonkeyMode skills write drafts to `_mm-output/`. When the user approves a decision there, promote it here. Suggested files:

| File | Content | Usually promoted from |
|---|---|---|
| `00_OVERVIEW.md` | Pitch, pillars, decided and undecided items, design principles | game brief, GDD |
| `01_STORY.md` | World, characters, story beats (story-driven games) | narrative design |
| `02_MECHANICS.md` | Core loop, mechanics with their numbers, controls | GDD |
| `03_ARCHITECTURE.md` | The architecture summary agents must follow | game architecture |
| `04_ROADMAP.md` | Milestones, done criteria, out-of-scope list | epics, sprint plan |

Numbers that have not been playtested are marked as assumptions. Implemented values live in data assets; when the two disagree, the code wins and the difference is reported.
