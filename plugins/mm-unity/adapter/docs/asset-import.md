# Asset import: Unity

> The Unity half of [`docs/guides/character-production-pipeline.md`](../guides/character-production-pipeline.md) and [`asset-pipeline-blender.md`](../guides/asset-pipeline-blender.md).

## Export format

- Unity imports FBX natively. glTF/GLB needs an extra package (`com.unity.cloud.gltfast`), which conflicts with other `.glb` importers **[source: glTFast docs summary; details for 6.x unchecked]**. Installing it is the user's decision. For rigs and animation clips, FBX is the safer choice **[estimate]**.
- Blender's glTF exporter triangulates quads and n-gons; split UVs and flat-shaded edges increase vertex counts **[source: Blender glTF manual]**.

## Checklist

1. Blender: 1 unit = 1 m, model at real game size, Apply All Transforms.
2. Origin at the center of the feet; one armature root.
3. Model tab: Scale Factor 1, check Convert Units (match the Blender FBX export scale) **[source: Unity FBX Importer Model]**. Verify Blender's FBX options (Apply Scalings, Forward/Up) in its manual (`unverified`).
4. Rig tab, Animation Type: **Generic** for non-human characters; Humanoid needs a human bone mapping **[source: Unity FBX Importer Rig]**. Upright characters with tails or big ears are simpler as Generic. Humanoid allows retargeting (for example Mixamo clips) but distorts non-human proportions **[estimate]**. To share clips across characters, use the same bone names and structure and share a Generic avatar (Copy From Other Avatar) **[source: Unity Rig docs summary]**.
5. Skin weights: at most 4 bones per vertex (`QualitySettings.skinWeights`) **[source: Unity scripting reference]**.
6. Optimize Game Objects hides unmapped bones; expose bones that code needs (ears, tails) under Extra Transforms to Expose **[source: Unity Rig docs summary]**.
7. Materials: remap to URP Lit or your toon shader; extract materials into `Assets/` so the FBX's embedded materials are not a dependency **[estimate]**.
8. Normals and tangents: Import or Calculate; check the smoothing angle.
9. Colliders: simple capsule/box; no mesh colliders on characters **[estimate]**.
10. LOD: with few characters on screen, often unnecessary; decide after measuring **[estimate]**.
11. Verify: no import warnings, prefab created, window screenshot under game lighting, network components verified separately (M2) for networked characters.

## Sources

- Unity 6, FBX Importer Rig: https://docs.unity3d.com/6000.0/Documentation/Manual/FBXImporter-Rig.html
- Unity 6, FBX Importer Model: https://docs.unity3d.com/6000.0/Documentation/Manual/FBXImporter-Model.html
- Unity, QualitySettings.skinWeights: https://docs.unity3d.com/ScriptReference/QualitySettings-skinWeights.html
- Unity glTFast: https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.10/manual
- Blender manual, glTF 2.0: https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
- Unity Toon Shader manual: https://docs.unity3d.com/Packages/com.unity.toonshader@0.15/manual/index.html
