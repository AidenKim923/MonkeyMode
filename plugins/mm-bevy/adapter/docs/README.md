# Engine adapter: Bevy

> Installed by `mm-setup` into `docs/engine/`. The engine-neutral half of the rules is in [`docs/ai/`](../ai/README.md).

**Verification status: checked against Bevy 0.20** (docs.rs and the 0.17 and 0.20 migration guides) and the docs of lightyear, bevy_replicon, bevy_renet and bevy_matchbox. Bevy breaks APIs between minor releases: check names against the version in your `Cargo.toml` and the official migration guides. Items marked *needs verification* could not be confirmed.

| Doc | Content |
|---|---|
| [Project context](project-context.md) | Fill in: Bevy version, crates, features, platforms |
| [Architecture addendum](architecture-addendum.md) | ECS, plugins, schedules and system ordering, states |
| [Guardrails](guardrails.md) | No blocking in systems, ordering rules, Clippy layer |
| [Build and test](build-and-test.md) | cargo commands, headless tests with `MinimalPlugins` |
| [Multiplayer](multiplayer.md) | lightyear, bevy_replicon, renet as options |
| [Version control](version-control.md) | `target/`, assets, LFS |

Files this adapter adds: `guardrails/bevy.json` (Rust rules) and `clippy.toml.example` (symbol-accurate `disallowed-methods`).
