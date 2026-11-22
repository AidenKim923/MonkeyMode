# Version control: Godot

`mm-setup` appends the adapter's `gitignore` and `gitattributes` lines to your project. The ignore list follows the github/gitignore `Godot.gitignore` template.

## Ignore

`.godot/` (Godot 4 project cache), `.nomedia`, `export.cfg`, `export_credentials.cfg`, `*.tmp`, `*.translation` (generated from CSV), C# build output (`.mono/`, `data_*/`, `mono_crash.*.json`, `~*.dll`), and your export output (`build/`, `*.exe`).

## Commit

- `project.godot`, `export_presets.cfg` (credentials such as keystore passwords belong in `export_credentials.cfg`, which is ignored), every `.tscn`, `.tres`, `.gd`.
- `*.import` sidecar files next to assets: they hold import settings; the official template does not ignore them, so commit them.
- `*.uid` files (Godot 4.4+) next to scripts and shaders: they hold the stable UIDs that references use. Commit them together with the file they belong to (*needs verification*: the docs show the files but do not say it in so many words).

## Merging

`.tscn` and `.tres` are text and merge better than most engines' scenes, but concurrent edits of the same scene still conflict on node order and `load_steps`. One editor per shared scene at a time.

## LFS

Track textures, audio, models (`*.glb`, `*.fbx`, `*.blend`), fonts and video. Decide before the first binary commit; adding patterns needs approval.
