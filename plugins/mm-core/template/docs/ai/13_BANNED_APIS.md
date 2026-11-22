# Banned APIs and patterns

> Some APIs are easy to call and hard to use safely: they hide lifetime, threading, ordering or networking contexts that agents get wrong. MonkeyMode bans them mechanically instead of hoping the next agent remembers.

## Where the lists live

| Layer | File | Scope |
|---|---|---|
| Core (every engine) | `guardrails/secrets.json` | Secrets, private keys, absolute personal paths in tracked text files |
| Engine | `guardrails/<engine>.json` | The engine's tricky APIs. Reasoning, sources and open questions: [`docs/engine/guardrails.md`](../engine/guardrails.md) |
| Project | Add rules to the engine profile, or a new `guardrails/<name>.json` profile | Your own repeated mistakes |

## Principles behind every list

These are engine-neutral; each adapter maps them onto concrete APIs.

| Principle | Why agents get it wrong | Typical replacement |
|---|---|---|
| No calls by string name (messages, invokes, reflection) | Renames break silently; the receiver is implicit | Interfaces, typed events/signals, registration tables |
| No scene-wide lookups at runtime | Hidden dependency on hierarchy shape and load order; breaks at network spawn time | Serialized references, injection at creation, registries |
| No fire-and-forget async without an owner | Exceptions vanish; work continues after the object is gone | Awaitables/tasks bound to a cancellation owner, coroutines/timers owned by the object |
| No raw threads touching engine state | Engine APIs are main-thread only; stray threads survive shutdown | The engine's job/task system, background-thread APIs |
| No direct engine logging in gameplay code | Agents judge behavior from logs, which needs consistent categories and levels | One project logging wrapper |
| No global time-scale writes in networked games | Server and client clocks drift; physics sync breaks | A server-side pause gate and one session clock |
| Client requests are always validated on the server | A modified client skips game rules | Owner-scoped requests carrying target IDs, validated server-side |

## Deciding new entries

When an agent wants to use an API that is not listed but has a tricky context (lifetime, threading, state), it asks first ([execution policy](01_AGENT_EXECUTION_POLICY.md)). Record the decision in the engine profile or in `docs/engine/guardrails.md` with a verdict column:

| Verdict | Meaning |
|---|---|
| `banned` | Mechanically blocked; the message names the alternative |
| `conditional` | Allowed under a written condition (for example "pure computation only, never touches engine APIs") |
| `allowed` | Reviewed and fine |

Mark the evidence behind each entry: **[source]** for something checked in a referenced document, **[knowledge]** for general engineering knowledge not re-checked, **[judgment]** for a project-specific choice.
