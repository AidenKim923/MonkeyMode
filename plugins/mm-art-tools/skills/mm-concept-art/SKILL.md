---
name: mm-concept-art
description: Produce concept art, mockups or image references for a game - characters, props, environments, UI. Several concepts can be requested at once. Depending on the project's setup it either writes ready-to-paste ChatGPT image prompts with an import checklist, or generates images through the Codex CLI, or points to alternatives (Blender blockouts, free asset libraries, other generators). Use for "make a concept", "draw a mockup", "give me reference images".
---

# Concept art

Request: $ARGUMENTS

## Pick the route

1. Read `uses_chatgpt` from `.monkeymode/config.json` (written by `mm-setup` from the project interview and the mm-core plugin setting). If the file or the value is missing, ask: "Do you also use ChatGPT for images? (recommended)" and suggest running `mm-setup` so the answer is kept.
2. Route:
   - `uses_chatgpt: yes` → **ChatGPT prompt route** (below).
   - `uses_chatgpt: no` and the `codex` CLI is on PATH → **Codex CLI route**.
   - Otherwise → **alternatives route**.

Shared first step for every route: split the request into individual concepts, and read the style and world from `docs/project/` (art direction in the GDD or the project overview). Do not invent a style that contradicts it.

## ChatGPT prompt route

For each concept, write one block the user can paste into ChatGPT as is:

```
Prompt for ChatGPT, concept "<name>":
<one paragraph in English: subject, pose/composition, camera angle, style keywords from the art direction,
 background (plain or transparent for assets), aspect ratio, what must be readable at game size>
Then ask: "Give me 3 variations, same style, different <silhouette | palette | composition>."
```

Then give the import checklist:

1. Save each image as `.agent-output/concepts/<YYYY-MM-DD>/<name>.png` (ASCII name, no spaces), and if you like the prompt as `<name>.json` with `{"prompt": "..."}` next to it.
2. Tell me when they are saved; I will open them, check them against the art direction and show them in the gallery (`pwsh tools/Start-ConceptServer.ps1`, then `http://localhost:5090/`).
3. To choose between versions, I will set up `mm-decision-picker`.
4. Record the tool and its terms in `docs/licenses/ASSET_REGISTRY.md` for every image we keep.

## Codex CLI route

1. Write an English prompt per concept (subject, composition, style, background, purpose).
2. One concept: `pwsh "${CLAUDE_PLUGIN_ROOT}/tools/Invoke-CodexImage.ps1" -Prompt "<prompt>" -Name <ascii-name>`. Several: write a JSON spec and run them together (4 in parallel by default):
   ```
   [{"name":"hero-front","prompt":"..."},{"name":"lab-hall","prompt":"..."}]
   pwsh "${CLAUDE_PLUGIN_ROOT}/tools/Invoke-CodexImage.ps1" -SpecFile <json path>
   ```
   Options: `-Model <model>` (default: Codex's configured model), `-Effort <low|medium|high>` (default `medium`), `-ThrottleLimit <n>`, `-Reference <image>` to work from a reference image. If `${CLAUDE_PLUGIN_ROOT}` was not substituted (non-Claude agents), use the path of this plugin's `tools/` folder.
3. Results go to `.agent-output/concepts/<date>/<name>.png` with the prompt in `<name>.json` (same name again becomes `-v2`). The script starts the local gallery if the project has it. Open the images yourself and check them; report `FAIL` lines with their cause.

## Alternatives route

Say plainly that MonkeyMode recommends ChatGPT for images, then offer:

- **Blender blockout** (with `mm-cli-blender`): simple shapes and colors rendered from the angles you need, good for proportions and silhouettes.
- **Free asset libraries** with clear licenses (for example CC0 libraries such as Poly Haven, Kenney, ambientCG). Check every license before use.
- **Other image generators** the user already has. Write the same prompt blocks as the ChatGPT route.

## Rules

- Concepts are not final until a human approves them. Moving a chosen concept into the project (`docs/` or the art source store) happens after the user confirms.
- Never put purchased-asset originals, other people's work, brands, or personal information in prompts or reference images (`docs/ai/07_ASSET_AND_DATA_POLICY.md`).
- Record the generator and its terms in `docs/licenses/ASSET_REGISTRY.md` for every concept that is adopted.
