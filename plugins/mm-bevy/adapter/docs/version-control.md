# Version control: Bevy

`mm-setup` appends the adapter's `gitignore` and `gitattributes` lines to your project.

## Ignore

`/target/` and debug symbols (`*.pdb`). Keep `Cargo.lock` committed for games (binaries).

## Commit

`Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `clippy.toml`, `.cargo/config.toml` (linker settings), `assets/`.

## Merging

Rust source and RON/TOML data merge like ordinary text. Scenes saved as `.scn.ron` are text too, but concurrent edits of the same scene file still conflict; one editor at a time.

## LFS

Track large binary assets under `assets/` (textures, models, audio) with Git LFS once they appear; decide before the first binary commit.
