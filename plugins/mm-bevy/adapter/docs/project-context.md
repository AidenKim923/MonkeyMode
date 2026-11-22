# Project context: Bevy

> Fill this in once; `mm-generate-project-context` uses it as a seed. Blank values are undecided.

| Item | Value |
|---|---|
| Bevy version | `<0.x>` (from `Cargo.toml`; these docs were checked against 0.20) |
| Rust toolchain | `<stable 1.xx>` (pin with `rust-toolchain.toml`) |
| Workspace crates | `<game>`, `<game_core>`, `<game_net>`, ... |
| Key third-party crates | `<physics: avian / rapier>`, `<input: leafwing-input-manager>`, `<ui>`, `<networking>` (check each against your Bevy version) |
| Networking | `<none / lightyear / bevy_replicon (+ transport) / bevy_renet / other>`; topology `<listen / dedicated>`; players `<n>` |
| Target platforms | `<desktop, wasm, mobile>` |
| Dev features | `<e.g. bevy/dynamic_linking in dev only>` |
| Log targets | `<game::net, game::gameplay, ...>` |

## Layout (suggested)

```
Cargo.toml                 workspace
crates/<game>/src/main.rs  App setup only: adds plugins
crates/<game>_core/        components, resources, events, pure rules (no rendering)
crates/<game>_gameplay/    gameplay plugins (one per feature)
crates/<game>_net/         networking plugin (client/server sets)
crates/<game>_ui/          UI plugin; reads state, sends events
assets/                    loaded by AssetServer
```

Crate dependencies are one-way (core ← gameplay ← net/ui ← game); Cargo enforces them.
