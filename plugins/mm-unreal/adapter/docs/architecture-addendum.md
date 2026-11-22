# Architecture addendum: Unreal Engine

> Read by `mm-game-architecture`. Needs community verification.

## Gameplay framework

| Class | Lives on | Use for |
|---|---|---|
| `AGameModeBase` | Server only | Rules, spawning, match flow. Clients never see it |
| `AGameStateBase` | Server + all clients (replicated) | Shared match state everyone reads |
| `APlayerController` | Server + owning client | Input routing, per-player UI, client→server RPCs |
| `APlayerState` | Server + all clients | Per-player replicated data (score, team, selection) |
| `APawn` / `ACharacter` | Server + relevant clients | The controllable body |
| `UGameInstance` / subsystems | Per process | Session, save, services that outlive maps |
| `UWorldSubsystem` | Per world | Registries ("all interactables in this level") instead of actor iteration |

Put rules in GameMode (server), shared facts in GameState, per-player facts in PlayerState. That split is the authority boundary.

## Modules

Each module has a `.Build.cs` with `PublicDependencyModuleNames` / `PrivateDependencyModuleNames`; UBT enforces them. Keep dependencies one-way (Core → gameplay → UI), editor code in an `Editor`-type module, and make cross-module calls go through interfaces (`UINTERFACE`) or delegates.

## UObject lifetime

- UObjects are garbage-collected. A pointer keeps an object alive only if the GC can see it: a `UPROPERTY()` member (use `TObjectPtr<>` in headers), an `AddReferencedObjects` override, or a `TStrongObjectPtr`. Use `TWeakObjectPtr` for non-owning references and check `IsValid()` before use.
- Create with `NewObject`, `CreateDefaultSubobject` (constructor only) or `SpawnActor`. Destroy actors with `Destroy()`. Never `new`/`delete` UObjects.
- Tuning lives in `UDataAsset` / `UPrimaryDataAsset`, DataTables or `UDeveloperSettings`, not in code constants.

## Assets and loading

Hard `UPROPERTY` references load everything they point to. Use `TSoftObjectPtr`/`TSoftClassPtr` plus async loading (`UAssetManager`, `FStreamableManager`) for optional or large content.

## Threads

Gameplay code and UObject access stay on the game thread. Background work uses `UE::Tasks`, `Async` or `FRunnable`, then returns results with `AsyncTask(ENamedThreads::GameThread, ...)`.

## Blueprints

Expose tuning and composition to Blueprints (`BlueprintReadWrite`, `BlueprintCallable`, `BlueprintImplementableEvent`); keep authority checks and networking in C++ where guardrails and reviews can see them.
