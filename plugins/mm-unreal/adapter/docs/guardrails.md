# Guardrails: Unreal Engine

> Enforced by `guardrails/unreal.json` on `Source/**/*.{cpp,h}` (generated files skipped). Evidence marks: **[source]** checked in the Unreal Engine 5.9 docs · **[knowledge]** engine knowledge not re-checked (*needs verification*) · **[judgment]** a MonkeyMode default.

## Enforced

| ID | Target | Why it is tricky | Instead | Evidence |
|---|---|---|---|---|
| UE_RAW_NEW_UOBJECT | `new UThing(...)`, `new AThing` | Invisible to the GC and reflection; crashes or leaks | `NewObject<T>`, `CreateDefaultSubobject<T>`, `SpawnActor<T>` | [source] "UObjects should only be constructed using NewObject at runtime, or CreateDefaultSubobject for constructors" |
| UE_DELETE_UOBJECT | `delete` on actors/components/objects | The GC owns UObjects | `Destroy()`, `DestroyComponent()`, drop references | [source] UObjects are garbage collected and never use `new` |
| UE_RAW_UOBJECT_MEMBER | `UThing* Member;` in headers | Without `UPROPERTY` the GC may collect it; dangling pointer | `UPROPERTY() TObjectPtr<UThing> Member;`, `TWeakObjectPtr` for non-owning | [source] "maintain a UPROPERTY reference to any Object you wish to keep alive"; `TWeakObjectPtr` "will not prevent garbage collection" |
| UE_RUNTIME_ACTOR_SEARCH | `UGameplayStatics::GetAllActorsOf*`, `TActorIterator` (Editor/Tests excluded) | O(actors); depends on spawn and streaming order | Register with a `UWorldSubsystem`, pass references | [knowledge] |
| UE_SYNC_LOAD | `StaticLoadObject`, `LoadObject<>`, `LoadSynchronous()` (Editor/Tests excluded) | Game-thread hitches; hidden hard dependencies | Soft pointers + async loading, or hard `UPROPERTY` refs | [knowledge] |
| UE_STD_THREAD | `std::thread`, `std::async` | Bypasses the task graph; unsafe with UObjects | `UE::Tasks::Launch`, `Async`, `FRunnable` | [knowledge] |
| UE_BLOCKING_SLEEP | `FPlatformProcess::Sleep*` | Freezes the game thread and the server | Timers, latent actions, tasks | [knowledge] |
| UE_LOGTEMP | `UE_LOG(LogTemp, ...)` | Agents need a category per module to read logs | `DECLARE_LOG_CATEGORY_EXTERN(Log<Module>, Log, All)` | [judgment] |
| UE_ONSCREEN_DEBUG | `GEngine->AddOnScreenDebugMessage` | Not checkable from logs; leaks into builds | Categorized logs; debug draw behind a console variable | [judgment] |
| UE_GLOBAL_TIME_DILATION | `SetGlobalTimeDilation` | Server/client time drift; movement correction fights it | Server-side pause through game state | [judgment] |

The no-comment rule is **off** for Unreal: comments on `UPROPERTY`/`UFUNCTION` become editor tooltips. The `UE_RAW_UOBJECT_MEMBER` rule is line-based and only checks headers; a raw pointer local inside an inline header function also matches. Move such code into the `.cpp`.

## Review rules (not mechanical)

| Rule | Why |
|---|---|
| Every `UFUNCTION(Server, ...)` validates its arguments (optional `WithValidation` + `_Validate`, which disconnects a client that fails it, or explicit checks that reject and log) | Clients call these; this is where rules get skipped |
| Replicated state uses `UPROPERTY(Replicated / ReplicatedUsing=OnRep_X)` registered in `GetLifetimeReplicatedProps` with `DOREPLIFETIME`; multicast RPCs only for one-off effects | Late joiners miss RPCs |
| Gameplay checks `HasAuthority()` before changing shared state | Clients must not finalize outcomes |
| `IsValid()` before using weak or possibly-destroyed objects | Pending-kill objects crash |
| No `ConstructorHelpers::FObjectFinder` outside constructors | Asserts at runtime |
| Tick disabled by default (`PrimaryActorTick.bCanEverTick = false`) unless needed | Per-frame cost on every instance |

## Semantic layer

- UHT and the compiler already reject many reflection mistakes. `bWarningsAsErrors = true;` in your `.Target.cs` (a TargetRules property: "Whether to enable all warnings as errors") turns the rest into errors.
- Static analysis: TargetRules `StaticAnalyzer` (with `StaticAnalyzerMode` for Clang, PVS-Studio configs) enables it; the UBT command-line form *needs verification*.
- Data Validation plugin validators (`UEditorValidatorBase`) can enforce rules on Blueprints and assets that text guardrails cannot see.
