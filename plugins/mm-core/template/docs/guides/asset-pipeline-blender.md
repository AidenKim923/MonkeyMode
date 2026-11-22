# Asset pipeline (Blender)

> How agents produce models and props with Blender, and the gates that keep them honest. Engine import specifics are in `docs/engine/` (Unity: [`asset-import.md`](../engine/asset-import.md)).

## Flow

Design data → model → preview render → automated checks → **human approval** → export (FBX/glTF) → engine import → prefab/blueprint/scene → test scene/level check.

## Tool order

Use the Blender command line first (`mm-cli-blender` from the `mm-art-tools` plugin, or `blender -b --python <script>`). Use a Blender MCP bridge only for what the CLI cannot do; how it is called depends on the connected server. Generative modeling alone does not guarantee rigging, animation or collision quality, so verification and approval gates are mandatory.

## Specs (starting points; record your own in `docs/project/`)

- Units: 1 Blender unit = 1 m, scale applied, a clearly defined pivot (characters: center of the feet).
- Triangle budgets: characters 3,000-8,000; small props 100-1,000. Initial budgets, not hard limits; record the reason when you exceed them.
- Deliverables per asset: source `.blend`, export `.fbx` or `.glb`, `preview.png`, `manifest.json`, `validation.json`.
- Naming: `<category>_<name>_<variant>` (`char_<name>`, `prop_crate_small`, `interact_power_lever`, `env_wall_a`).
- Rigging: a shared set of animations for every character (for example Idle/Walk/Jump/Interact) plus character-specific ones.
- Collision: simple box/capsule/convex colliders; review whether dynamic objects need physics bodies.

## Automated checks

Files exist, no missing mesh or material, normals, triangle count, scale/rotation applied, pivot, export succeeded, engine import warnings, collider and network components on the prefab/blueprint.

## Production order

P0: props the first playable milestone needs to function → P1: core devices of later content → P2: decoration and polish.

## Keep sources out of the repository

`.blend` files and texture sources live outside the engine project and are not committed (`docs/ai/07_ASSET_AND_DATA_POLICY.md`, section 4). Imported results inside the project are committed (with LFS where configured).
