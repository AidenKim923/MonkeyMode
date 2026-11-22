# Version control: Godot

`mm-setup` appends the adapter's `gitignore` and `gitattributes` lines to your project. Needs community verification.

## Ignore

`.godot/` (Godot 4 cache and imported resources), `export/` or `build/` output, `*.translation` generated files, `.mono/` and `.godot/mono/` for C# builds, `*.tmp`.

## Commit

- `project.godot`, `export_presets.cfg` (strip any credentials first; Android keystore passwords live there), every `.tscn`, `.tres`, `.gd`.
- `*.import` sidecar files next to assets: they hold import settings and must be committed in Godot 4.
- `*.uid` files (Godot 4.4+) next to scripts and shaders: they hold stable UIDs that references use.

## Merging

`.tscn` and `.tres` are text and merge better than most engines' scenes, but concurrent edits of the same scene still conflict on node order and `load_steps`. One editor per shared scene at a time.

## LFS

Track textures, audio, models (`*.glb`, `*.fbx`, `*.blend`), fonts and video. Decide before the first binary commit; adding patterns needs approval.
