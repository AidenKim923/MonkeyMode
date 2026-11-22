# Version control: Unreal Engine

`mm-setup` appends the adapter's `gitignore` and `gitattributes` lines to your project. Needs community verification.

## Ignore

`Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, `.vs/`, `.idea/`, `*.sln`, `*.VC.db`, and the same folders inside each `Plugins/<Plugin>/`. Keep `Config/` and `Content/`.

## Binary assets

`.uasset` and `.umap` are binary and **cannot be merged**. Two people editing the same asset means one loses their work.

- Track them with Git LFS (`*.uasset`, `*.umap` plus source art) and use **LFS file locking** (`git lfs lock`). The editor's Git source control plugin can show lock state.
- For levels, enable **World Partition with One File Per Actor** so people can edit different actors of the same map.
- Agents never edit `.uasset`/`.umap` files directly and never assign one asset to parallel workers.

## Redirectors

Moving or renaming assets leaves redirectors. Run "Fix Up Redirectors" before committing a move, and commit the redirector removal together with the move. Bulk moves need approval.

## LFS

Unlike other engines, LFS is close to mandatory for Unreal. Set it up before the first content commit.
