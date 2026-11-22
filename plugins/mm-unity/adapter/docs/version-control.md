# Version control: Unity

`mm-setup` appends the lines in the adapter's `gitignore` and `gitattributes` to your project's files.

## Ignore

`Library/`, `Temp/`, `Obj/`, `Build/`, `Builds/`, `Logs/`, `UserSettings/`, `MemoryCaptures/`, `.vs/`, `.idea/`, generated `*.csproj` and `*.sln`/`*.slnx`.

## Always commit

- Every `.meta` file next to its asset. A missing `.meta` file means a new GUID and broken references.
- `ProjectSettings/` and `Packages/manifest.json` + `packages-lock.json`.

## Serialization and merging

- Set **Asset Serialization: Force Text** and **Version Control: Visible Meta Files** (Project Settings → Editor).
- Scenes and prefabs merge badly even as text. Use UnityYAMLMerge ("Smart Merge") as the git merge tool, and still never edit a shared scene in parallel.

## LFS

Track large binaries: textures (`*.png`, `*.psd`, `*.tga`, `*.exr`), audio (`*.wav`, `*.ogg`), models (`*.fbx`, `*.glb`), video, fonts. Decide LFS before the first binary commit: patterns are not applied to history retroactively, and adding them needs approval.
