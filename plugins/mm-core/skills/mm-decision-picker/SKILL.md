---
name: mm-decision-picker
description: When the user must pick one of several options - UI mockups, concept art, or any image-based game asset - put the options on a local web page (localhost:5090) so the user chooses there, then read the choice back and apply it. Use for "let me pick", "show me several versions", or any comparison and selection of UI or asset concepts.
---

# Decision picker page (localhost:5090)

Scope: UI mockups and every game asset made from images. Small questions without images are asked in the terminal instead.

The server and its files come from the MonkeyMode project template (`tools/Start-ConceptServer.ps1`, `tools/concept-server/`, needs Node.js 18+ and PowerShell 7). If they are missing, run `mm-setup` first.

## Steps

1. Get the candidate images: from `mm-concept-art` (if the `mm-art-tools` plugin is installed), from the user, or from files already in the project. Images live under `.agent-output/concepts/{date}/{name}.png`.
2. Write `.agent-output/decisions/{id}.json`. `id` uses only ASCII letters, digits, `_` and `-`.
   ```json
   {
     "id": "lobby-ui-layout",
     "title": "Lobby UI layout",
     "question": "Which direction should we take?",
     "created": "2026-01-01T10:00:00Z",
     "options": [
       {"id": "a", "label": "Option A", "summary": "One-line summary", "pros": ["upside"], "cons": ["downside"],
        "image": "concepts/2026-01-01/lobby-a.png", "recommended": true},
       {"id": "b", "label": "Option B", "summary": "...", "pros": [], "cons": []}
     ]
   }
   ```
   `image` is relative to `.agent-output/`; only images under `concepts/` or `decisions/` are served. Mark the recommendation with `recommended: true`. Write pros and cons in the `mm-present-alternatives` frame.
3. Start or check the server: `pwsh tools/Start-ConceptServer.ps1` (prints the URL if it is already running). Tell the user to open `http://localhost:5090/` and choose. Never ask them to copy results or paste anything into the chat.
4. When the user says they chose, read `.agent-output/decisions/{id}.choice.json` (`optionId`, `note`, `chosenAt`) and apply it. If the file does not exist, they have not chosen yet. Do not poll in a loop.
5. Write the confirmed result into `docs/project/` as current fact (no dates or history wording) and log the work in `docs/work/`.

## Rules

- The server listens on `127.0.0.1:5090` only and checks Host and Origin. Stop it with `pwsh tools/Start-ConceptServer.ps1 -Stop`.
- The user can change their mind by choosing another option. Re-read `choice.json` right before applying.
- Never put original purchased-asset files, other people's work, or personal information on the page.
