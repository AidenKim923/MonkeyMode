# Engine notes: <YourGame>

No MonkeyMode engine adapter is installed (engine: other). The engine-neutral rules in [`docs/ai/`](../ai/README.md) still apply. Fill in these sections so agents know your engine; the adapters for Godot, Unity, Unreal and Bevy show the expected depth.

## Project context

| Item | Value |
|---|---|
| Engine / framework and version | `<...>` |
| Language | `<...>` |
| Folder layout | `<...>` |
| Data and tuning files | `<...>` |

## Architecture

Scene/level structure, scripting model (components, nodes, actors, entities), module boundaries and how they are enforced.

## Guardrails

Add a profile `guardrails/<engine>.json` (format in `docs/ai/12_GUARDRAILS_INSTEAD_OF_COMMENTS.md`) for your engine's tricky APIs, applying the principles in `docs/ai/13_BANNED_APIS.md`.

## Build and test

| Goal | Command | Pass signal |
|---|---|---|
| Compile / parse check | `<...>` | |
| Tests | `<...>` | |
| Build | `<...>` | |
| Run N instances | `pwsh tools/Start-Game.ps1 -Exe <exe> -Instances <n>` | |

## Multiplayer

Networking library, how authority and replication work, how to run several instances.

## Version control

What to ignore, what to commit, LFS patterns, files that cannot be merged.
