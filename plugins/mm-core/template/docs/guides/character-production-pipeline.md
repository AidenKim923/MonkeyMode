# Character production pipeline

> The standard professional character pipeline, adapted for small and solo teams making stylized characters in Blender. Engine import steps are in `docs/engine/` (Unity: [`asset-import.md`](../engine/asset-import.md)).

## Marks

- **[source]**: from the documents listed at the end.
- **[estimate]**: a recommendation or estimate from research and common practice, not verified in production (`unverified`).
- Items that relied on search summaries were not opened directly; check the original before relying on them.

---

## 1. The standard pipeline

| Step | Work | Typical tools |
|---|---|---|
| 1 Concept and reference | Front/side/back sheets, proportions and silhouette, a reference board | Paper/Procreate/Photoshop/Krita, PureRef, image generators (`mm-concept-art`) |
| 2 Blockout | Proportions and silhouette only, from spheres and boxes. No detail | Blender, ZBrush, Nomad Sculpt |
| 3 High-poly sculpt | Forms, folds, fur and feather clumps; symmetry on | ZBrush, Blender Sculpt, Nomad Sculpt |
| 4 Retopology | Rebuild as a game-ready low-poly quad mesh with loops around joints | Blender (including add-ons such as Quad Remesher), ZBrush ZRemesher, TopoGun, Maya |
| 5 UV | Seams, texel density, shared UVs for symmetric parts | Blender, RizomUV |
| 6 Bake | Bake high-poly detail into normal and AO maps on the low-poly | Marmoset Toolbag, Substance Painter, Blender Bake |
| 7 Texturing | PBR or stylized hand-painted | Substance Painter, Blender Texture Paint, Photoshop, Krita |
| 8 Rigging and skinning | Skeleton, controls, weight painting, face, ears, tails | Blender Rigify, Maya, Mixamo (humanoids only) |
| 9 Animation | Idle/Walk/Jump and other clips | Blender, Maya, the engine's animation tools |
| 10 Engine import and LOD | FBX/glTF export, materials, avatar/skeleton setup, LOD | Your engine |

Why this order **[source]**: setting proportions and silhouette in the blockout before anatomical detail saves time (Gnomon). Sculpt → retopology → UV → bake → texture, with these tools, appears in the Blender Studio Stylized Character Workflow, an 80.lv workflow article and Gnomon workshops. A bad bake sends you back to retopology, so approve the early steps (80.lv, Julien Desroy). Rigging and animation can run in parallel with texturing once the low-poly is final (Kinship Entertainment case study).

For a **low-poly stylized look, you can skip the high-poly sculpt and the bake**: model the low-poly directly and use vertex colors or simple hand-painted textures **[estimate]**. The pipeline then becomes concept → blockout → direct low-poly → UV → texture → rig.

## 2. Stylized creature and character guidelines

### Proportions and silhouette

- A big head, small body and short limbs read as cute (neoteny) **[source: cartooning book excerpt, Creative Bloq]**. Measure the body in head units.
- Silhouette test: filled solid black, each character must still be recognizable at a glance **[source: Creative Bloq]**.
- Heads are often round from the front and bean-shaped from the side (Blender Studio, Sprite Fright article). For animal characters, human-like hands read more easily (Pluralsight).
- Put the whole cast side by side in one image and check size order and silhouette contrast **[estimate]**.

### Shape language

- Round shapes read friendly; angular shapes read threatening or tough **[source: Creative Bloq]**. For a soft, rounded style, give every character the same round base and tell them apart with one or two features (tail, ears, nose) **[estimate]**.

### Topology and edge flow

- Where the mesh deforms (shoulders, elbows, knees, jaw, eyes, mouth), edge loops must follow the deformation to fold cleanly **[source: topology guide summaries]**. Stay mostly quads; triangles and n-gons cause problems in animation **[source: Wacom, Polycount summaries]**.
- Faces need closed loops around eyes and mouth and edge flow along the major muscle directions (Blender Studio facial rigging and retopology course outline). Some animators accept loops that are not fully closed if the overall flow is good (comments on the same course).
- Model symmetric characters as one half with a Mirror modifier **[source: Creative Bloq]**.

### Face, ear and tail rigs

- Ears, tails and long noses or trunks are bone chains; add spring or delayed motion in the engine if needed **[estimate]**.
- Facial expressions: bones or shape keys (blend shapes). For low-poly styles, swapping eye textures or eyelid bones is simplest **[estimate]**. Shape keys usually export to engines as blend shapes; check your engine's docs (`unverified`).
- Rigify ships metarigs for quadrupeds and animals (Basic Quadruped, Cat, Wolf, Horse, Shark) **[source: Blender manual summary]**. Upright, anthropomorphic characters can start from the Basic Human or Human metarig **[estimate]**. Rigify does not skin for you (weights are manual), assumes 1 unit = 1 m, and keeps the metarig for regeneration **[source]**.

### Fur and feathers

- For low-poly stylized characters, **do not build real fur**. Express it with form clumps, textures and shaders **[estimate]**.
- Options: (1) flat or gradient toon shading with outlines; (2) shell fur shaders; (3) hair cards. Shell fur gets expensive with several characters on screen and on mobile **[estimate, not measured]**.
- Toon shader packages support different engine and render pipeline versions; check compatibility first **[source: search summaries, versions unchecked]**.

### Polygon budgets

- 3,000-8,000 triangles per stylized character is the usual order of magnitude **[estimate; public numbers not checked directly]**.
- With only a handful of characters on screen, 8,000 is comfortable. **Exceeding a budget is rarely why a model looks cheap**: shape, shading and texture are **[estimate]** (section 3).
- Skinning: keep at most 4 bone influences per vertex; most engines default to 4 and charge for more **[source: Unity scripting reference; check your engine]**.

## 3. Why beginner Blender characters look cheap, and the fixes

| Common cause | Fix |
|---|---|
| Too little reference | Put front/side images in the background and match them; use finished works and wireframes as the quality bar [source: Polycount, Creative Bloq] |
| Wrong proportions, detail too early | Approve proportions and silhouette in the blockout before adding detail [source: beginner guides] |
| Models assembled from scripted primitives | Joined spheres and cylinders show seams and no organic flow. Sculpt, or box-model with subdivision [estimate] |
| Bad topology | Mostly quads, loops at joints, no n-gons, manage poles [source] |
| Flat shading or wrong smoothing | Shade Smooth for soft surfaces; bevel + weighted normals for hard edges; check normal direction [estimate] |
| No texture, flat colors | At least a base color plus hand-painted shadows/highlights or a gradient ramp. Eye design changes the impression most [estimate] |
| Bad UVs | Check stretching with a checker texture, hide seams, give resolution to what matters [source: Blender Studio artist guide] |
| Judging under the wrong lights | Judge in the engine under game lighting, not in Blender's viewport [estimate] |
| The face | Eye size, spacing and position decide appeal; highlights, brows and ears carry expression [estimate] |
| Unapplied scale, pivot, transforms | Apply scale/rotation; origin at the feet [source: asset pipeline guide] |

### Checklist

1. Silhouette overlaid as solid black matches the reference.
2. Proportions match the concept from the front, side and 3/4 views.
3. Every joint has edge loops; no triangles or n-gons in deforming areas.
4. Triangle count is within budget (or the reason is recorded).
5. Smoothing and normals look as intended; no dark faces.
6. UVs do not overlap and a checker texture is even.
7. Textures exist, with eye, nose and ear detail.
8. Extreme poses do not tear the mesh (weights checked).
9. In the engine: scale 1, rotation 0, correct size.
10. Engine screenshots (per window) under game lighting are compared side by side with the concept.

## 4. Realistic options for small teams

| Approach | Upsides | Downsides |
|---|---|---|
| Model it yourself (Blender) | No cost, full style control | Learning time, uneven quality |
| Base meshes and kitbashing | Start from proven topology and rigs | Licensing; characters can look alike |
| Asset store character packs | Fast; rigs and animations may be included | Style mismatch, consistency across the cast, licensing, price |
| AI generation + cleanup | Fast first drafts | Poor topology, unsuitable for character rigs; reports of hours of cleanup; more usable for props and backgrounds **[source: Polycount threads, vendor blogs (possible marketing)]**. Generators that cost money or credits need user approval |
| Outsourcing | Quality, saves time | Cost, communication, cast consistency |

Recommendation: **model low-poly directly and reuse one base body inside Blender** (the cast shares a body structure); skip the full sculpt and bake. If quality falls short, decide outsourcing or buying assets with the user **[estimate]**.

## 5. Step-by-step workflow with gates

All estimates are **[estimate, one person of medium skill, per character, unverified]**.

| Step | Output | Approval gate | Estimate |
|---|---|---|---|
| 0 Concept | Front/side/back sheets, reference board | User approves the concepts | 0.5 day |
| 1 Blockout | Proportion/silhouette model over the concept | User checks the cast side by side | 0.5-1 day |
| 2 Low-poly model | Quad mesh, joint loops, within budget | Wireframe + smooth render | 1-2 days |
| 3 UV | Non-overlapping UVs, checker check | Checker render | 0.5 day |
| 4 Texture | Base color + hand paint or gradient ramp, eyes | Engine screenshot | 1-2 days |
| 5 Rig and skin | Rigify-based rig, weights, ear and tail chains | Extreme pose test | 1-2 days |
| 6 Animation | Shared clips plus character-specific ones | Plays in the engine | 0.5-1 day per clip |
| 7 Engine import and check | Prefab/blueprint, materials, skeleton/avatar, LOD if needed | Multiplayer build check if networked | 0.5 day |

Run the first character through steps 1-7 end to end to prove the pipeline, then repeat it for the rest. Sharing a base body and UV layout across the cast shortens the work.

When starting from an existing rough model, first compare it with the concept (proportions, detail, surfaces, missing textures). If the shape itself is wrong, restart from step 2.

## 6. Decisions to make with the user

- Keep modeling in-house, or mix in assets or outsourcing
- Export format (FBX or glTF) and whether the engine needs an extra importer
- Target height per character (meters)
- Fur approach (toon shading only, shell fur, cards)

## Sources

- Blender Studio, Stylized Character Workflow: https://studio.blender.org/training/stylized-character-workflow/
- Blender Studio, Facial Rigging (modeling adjustments): https://studio.blender.org/training/facial-rigging/modeling-adjustments/
- Blender Studio, Artist guide, modeling: https://studio.blender.org/tools/artist-guide/asset-creation/modeling
- Blender Studio, Sprite Fright: The illusion of simplicity: https://studio.blender.org/blog/sprite-fright-the-illusion-of-simplicity
- 80.lv, Stylized Character Art Workflow from Blockout to Render: https://80.lv/articles/001agt-stylized-character-art-workflow-from-blockout-to-render
- 80.lv, Julien Desroy Mononoke Warcraft Crossover: https://80.lv/articles/julien-desroy-mononoke-warcraft-crossover/
- 80.lv, Making Stylized 3D Characters Cute and Awesome: https://80.lv/articles/making-stylized-3d-characters-cute-and-awesome
- Gnomon, Modeling a Stylized Character for Games: https://gnomon.thegnomonworkshop.com/tutorials/modeling-a-stylized-character-for-games
- Sketchfab, Kinship Entertainment spotlight: https://sketchfab.com/blogs/community/game-studio-spotlight-kinship-entertainment/
- Creative Bloq, 18 tips for game character models: https://www.creativebloq.com/how-create-character-models-games-18-top-tips-9113050
- Creative Bloq, How shape can make or break your character art: https://www.creativebloq.com/art/digital-art/how-shape-can-make-or-break-your-character-art
- Wacom, Common 3D modeling mistakes: https://wacom.com/en-au/discover/3d-game/common-3d-modeling-mistakes
- Polycount threads: https://polycount.com/discussion/comment/2618768 , https://polycount.com/discussion/comment/2809121/
- Pluralsight, Drawing animals: increasing appeal: https://pluralsight.com/blog/creative-professional/drawing-animals-tips-increasing-appeal-animal-characters
- Blender manual, Rigify: https://docs.blender.org/manual/en/dev/addons/rigify/basics.html
- Blender manual, glTF 2.0: https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
- Unity, QualitySettings.skinWeights: https://docs.unity3d.com/ScriptReference/QualitySettings-skinWeights.html
- hecomi UnityFurURP (shell fur example): https://github.com/hecomi/UnityFurURP
- Tripo, Game-Ready Checklist for AI-Generated Assets (vendor article): https://www.tripo3d.ai/blog/explore/game-ready-checklist-for-ai-generated-assets
