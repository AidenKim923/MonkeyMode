# Guardrails: Unity

> Banned APIs and patterns for Unity C#, enforced by `guardrails/unity.json` on `Assets/_Game/**/*.cs`. Evidence marks: **[source]** checked in a listed document · **[knowledge]** general engineering knowledge, not re-checked · **[judgment]** a MonkeyMode default.

## 1. Enforced now

| ID | Target | Why it is tricky | Instead | Evidence |
|---|---|---|---|---|
| BANNED_TWEEN_LIB | DOTween (`DG.Tweening`), LeanTween, iTween | Tweens keep running after the target is destroyed (null access), `SetAutoKill(false)` tweens leak, kill/reset/callback ordering bugs, update-mode confusion (pause, time scale) | Animator, AnimationCurve, state machines. When server state drives it, change only the presentation in the sync callback | [source] ①②③ |
| BANNED_STRING_MESSAGING | `SendMessage`, `SendMessageUpwards`, `BroadcastMessage` | Called by string name: renames break silently; receivers are implicit | Interfaces, C# events/delegates | [knowledge] |
| BANNED_STRING_INVOKE | `Invoke("x")` / `InvokeRepeating` / `CancelInvoke` with strings or `nameof`, `StartCoroutine("x")` | Same as above; cancellation and lifetime owner unclear | `StartCoroutine(IEnumerator)`, one lifetime owner | [knowledge] |
| BANNED_RUNTIME_FIND | `GameObject.Find*`, `FindObjectOfType(s)`, `FindFirst/AnyObjectByType`, `FindObjectsByType` (Editor and Tests excluded) | Hidden dependency on hierarchy, load and spawn order; null at network spawn time; expensive when called in `Update` | Serialized references, injection at creation, registries | [knowledge] |
| BANNED_RESOURCES_LOAD | `Resources.Load*` (Editor excluded) | String paths; everything in Resources ships in the build | Serialized references, ScriptableObject registry, Addressables | [knowledge] |
| BANNED_ASYNC_VOID | `async void` (Tests excluded) | Callers cannot catch exceptions; unlike coroutines, keeps running after the object is destroyed unless given `destroyCancellationToken` | Return `Awaitable`/`Task` and pass `destroyCancellationToken`, or a coroutine | [source] ④⑤ |
| BANNED_RAW_THREAD | `new Thread(...)` | Unity APIs are main-thread only; threads survive shutdown | `Awaitable.BackgroundThreadAsync`, Job System | [knowledge] |
| BANNED_REFLECTION | `System.Reflection`, `Activator.CreateInstance`, `GetMethod/GetField/GetProperty` (Editor and Tests excluded) | Severs static references; breaks silently under IL2CPP stripping and refactors | Interfaces, registration tables | [knowledge] |
| BANNED_DEBUG_LOG | Direct `Debug.Log*` (logging wrapper, Editor and Tests excluded) | Agents judge behavior from logs; categories and levels must be consistent | The project logging wrapper | [judgment] |
| BANNED_MIRROR_NO_AUTHORITY_COMMAND | `requiresAuthority = false` **[Mirror]** | Any client can send commands for objects it does not own; one missing server check skips game rules | Command on a player-owned object passing the target `NetworkIdentity`; server validates distance, ownership, ability | [judgment] (exact semantics: check the docs of your Mirror version) |
| BANNED_TIMESCALE_WRITE | `Time.timeScale =` (Editor and Tests excluded) | Server and client time drift; physics sync breaks | A server-side pause gate and one session clock | [judgment] |

Also enforced: **no comments** in `Assets/_Game/**/*.cs` (generated files excluded). Turn it off with `"noComments": false` if your team prefers comments.

### The biggest call: banning tweens entirely

Without tweens, UI and effects (doors opening, button presses, damage numbers, camera moves) are written by hand.

| Option | Upside | Cost |
|---|---|---|
| A. Ban entirely (default) | Lifetime bugs cannot happen | Effects code by hand; heavy for animation-rich games |
| B. Allow one wrapper | Lifetime rules (for example DOTween `SetLink` to auto-kill on destroy) live in one place | Wrapper design and upkeep |
| C. Allow a different library (PrimeTween and others) | Claimed to have fewer lifetime problems | Not verified [knowledge gap] |

If effects cost becomes the bottleneck, revisit B with the user.

### Coroutines and Awaitable

Default: coroutines for game-object effects, `Awaitable` for I/O and network waits; never both inside one feature.

## 2. Banned by review, not yet mechanical

| Target | Why | How to enforce | Evidence |
|---|---|---|---|
| Sending state through `[ClientRpc]` **[Mirror]** | RPCs reach only clients connected at call time; late joiners and rejoiners miss the state. State goes in SyncVars/SyncLists; RPCs are one-off effects | Review checklist, rejoin play test | [knowledge] |
| Game logic inside SyncVar hooks **[Mirror]** | Whether hooks fire on host, server or late join has differed between versions (forum reports); re-assigning inside a hook can double-fire | Hooks update presentation only; test host and client-only instances (M2) | [source] ⑥ (version-dependent; re-check on your Mirror version) |
| Mutable static singletons (`static Instance`) | Load/unload order; a host shares one process between server and client | Registered services, assembly direction | [knowledge] |
| `DontDestroyOnLoad` sprawl | Duplicates on scene change and rejoin | Bootstrap scene only | [judgment] |
| `GetComponent`, LINQ, allocations inside `Update`/`FixedUpdate` | Per-frame allocation, GC spikes | Profiling tests, review | [knowledge] |
| Mixing coroutines and `Awaitable` | Different lifetime models; missed cancellation. `Awaitable<T>` cannot be yielded in a coroutine | One model per feature | [source] ④⑤ |

## 3. Conditional

| Target | Condition |
|---|---|
| `Task.Run` | Pure computation only; never touches Unity APIs |
| LINQ | Initialization and editor code only; never in frame loops |

## 4. The semantic layer: Roslyn banned-API analyzer

Regex checks run on every file every time but can false-positive on same-named symbols and miss `using X = ...` aliases. A Roslyn banned-API analyzer checks symbols precisely:

- A Unity-packaged fork of Microsoft's BannedApiAnalyzers (`BannedApiAnalyzers.Unity` on NuGet, MIT) can live under `Assets/_Game/Analyzers/` with a `BannedSymbols.*.additionalfile` listing the symbols [source] ⑦⑧.
- Observed on Unity 6: violations report as `RS0030`. A global `Assets/csc.rsp` with `-warnaserror+:RS0030` makes them errors, **but also fails third-party code** (template samples, Mirror). Per-assembly `.rsp`, asmdef references and `.editorconfig` severity did not scope it. So keep RS0030 as a warning and let `Invoke-UnityTests`/`Invoke-UnityBuild` fail on RS0030 warnings under `Assets/_Game/`.
- Unity does not recompile unchanged assemblies, so analyzer warnings appear only on the first compile after a change. The regex check stays the final gate; the analyzer is a precise second layer.
- Packages that are not installed (DOTween) can only be caught by regex.

## Sources

① [DOTween tween running on destroyed object (bugnet.io)](https://bugnet.io/blog/how-to-fix-dotween-tween-running-on-destroyed-object-null): `SetLink` auto-kills on destroy
② [Unity Performance Tuning Bible: Third Party (CyberAgent)](https://cyberagentgameentertainment.github.io/UnityPerformanceTuningBible/en/tuning_practice_third_party.html): `SetAutoKill(false)` leaks
③ [DOTween support](https://dotween.demigiant.com/support.php): pooling and reuse of killed tweens
④ [On Async/Await with Awaitables as a Coroutine replacement (Unity Discussions)](https://discussions.unity.com/t/on-async-await-with-awaitables-as-a-coroutine-replacement/1554090): coroutines bound to object lifetime; Awaitable needs `destroyCancellationToken`
⑤ [Awaitable introduction (Unity manual)](https://docs.unity.com/en-us/engine/current/manual/scripting/programming-distribute-work-threads/async-await-support/async-awaitable-introduction)
⑥ [Mirror SyncVars docs](https://mirror-networking.gitbook.io/docs/manual/guides/synchronization/syncvars), [Mirror's SyncVar behavior (forum)](https://discussions.unity.com/t/mirrors-syncvar-behavior/825311): hook firing reports
⑦ [BannedApiAnalyzers.Unity (NuGet)](https://www.nuget.org/packages/BannedApiAnalyzers.Unity)
⑧ [RS0030: Do not use banned APIs](https://github.com/dotnet/roslyn-analyzers/blob/main/src/Microsoft.CodeAnalysis.BannedApiAnalyzers/Microsoft.CodeAnalysis.BannedApiAnalyzers.md)

Most sources above are forums and blogs, not official guarantees. Some Mirror material predates Mirror (UNET era); re-check against the docs of the version you adopt.
