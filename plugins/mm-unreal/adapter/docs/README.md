# Engine adapter: Unreal Engine

> Installed by `mm-setup` into `docs/engine/`. The engine-neutral half of the rules is in [`docs/ai/`](../ai/README.md).

**Verification status: needs community verification.** Written for Unreal Engine 5.x (C++ with Blueprints) from engine documentation knowledge. It has not yet been field-tested in a MonkeyMode project.

| Doc | Content |
|---|---|
| [Project context](project-context.md) | Fill in: engine version, modules, C++/Blueprint split, platforms |
| [Architecture addendum](architecture-addendum.md) | Modules, gameplay framework classes, UObject lifetime, assets |
| [Guardrails](guardrails.md) | UObject/GC rules, banned patterns |
| [Build and test](build-and-test.md) | UBT/UAT command lines, automation tests, Gauntlet |
| [Multiplayer](multiplayer.md) | Replication, RPCs, roles, PIE multi-client |
| [Version control](version-control.md) | Ignore list, LFS for `.uasset`/`.umap`, file locking |

Files this adapter adds: `guardrails/unreal.json` (C++ rules under `Source/`).

**Blueprints** are binary assets; regex guardrails cannot read them. Agents can review Blueprint logic only through the editor or exported text. Keep rules that matter in C++ (or enforce them with Data Validation / `UEditorValidatorBase` validators).
