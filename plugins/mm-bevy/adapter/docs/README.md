# Engine adapter: Bevy

> Installed by `mm-setup` into `docs/engine/`. The engine-neutral half of the rules is in [`docs/ai/`](../ai/README.md).

**Verification status: needs community verification.** Written from Bevy documentation knowledge (APIs of the 0.14-0.16 era). Bevy breaks APIs between minor releases: check every name against the version in your `Cargo.toml` and the official migration guides.

| Doc | Content |
|---|---|
| [Project context](project-context.md) | Fill in: Bevy version, crates, features, platforms |
| [Architecture addendum](architecture-addendum.md) | ECS, plugins, schedules and system ordering, states |
| [Guardrails](guardrails.md) | No blocking in systems, ordering rules, Clippy layer |
| [Build and test](build-and-test.md) | cargo commands, headless tests with `MinimalPlugins` |
| [Multiplayer](multiplayer.md) | lightyear, bevy_replicon, renet as options |
| [Version control](version-control.md) | `target/`, assets, LFS |

Files this adapter adds: `guardrails/bevy.json` (Rust rules) and `clippy.toml.example` (symbol-accurate `disallowed-methods`).
