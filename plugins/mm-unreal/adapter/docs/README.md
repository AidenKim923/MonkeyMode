# Engine adapter: Unreal Engine

> Installed by `mm-setup` into `docs/engine/`. The engine-neutral half of the rules is in [`docs/ai/`](../ai/README.md).

**Verification status: partly checked against the official Unreal Engine 5.9 docs** (RPCs, property replication, object handling, Iris, automation tests, BuildCookRun, UBT target reference, One File Per Actor). Items marked *needs verification* could not be confirmed there. Not yet field-tested in a MonkeyMode project.

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
