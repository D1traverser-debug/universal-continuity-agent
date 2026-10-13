# 03 — Distributed Systems, Consensus, Idempotency and Change Authority

## Why this matters

Universal spans ChatGPT sessions, GitHub repositories, owner runtimes, external tools and product state. Even with one intended writer, network/tool ambiguity and stale observations create distributed-systems failure modes: delayed reads, duplicate attempts, uncertain mutation outcomes, stale writers and divergent caches.

## Consensus versus single-writer optimistic concurrency

Raft manages a replicated log under multiple nodes that may fail, partitions leader election into terms, elects a leader through majority voting, and preserves safety through log-replication rules. Its main lesson for Universal is not “implement Raft,” but to be explicit about the assumptions under which a simpler mechanism is sufficient.

Current Universal uses `SINGLE_ACTIVE_CHAT`, an active lease/resume epoch and observed-HEAD compare-and-swap for material `main` writes. Under that threat model, a consensus protocol would add complexity without solving a demonstrated problem. The important boundary is:

- current model: one compliant active writer, stale writers rejected through lease/CAS;
- future multi-writer/replicated control plane: the current scheme would no longer be enough; leader election/quorum/consensus semantics would have to be reconsidered.

A future change in writer model must therefore be treated as an architecture transition, not a configuration tweak.

## Ambiguous mutation outcomes

Distributed calls can time out after the server has applied the effect. Retrying blindly can duplicate irreversible work. AWS's idempotency guidance formalizes the fix: stable client/request identity and semantic equivalence allow repeated delivery without repeated side effects.

Universal already contains `runtime/mutation_outcome.py`, which distinguishes confirmed success, confirmed failure and outcome unknown. That is a strong start. However, idempotency semantics are not yet a universal contract across every external owner/tool mutation.

### Needed questions per mutation

- Is the operation read-only, idempotent, conditionally idempotent, or non-idempotent?
- Is there a stable request/action identity?
- If transport result is ambiguous, can final state be reconciled before retry?
- Which layer owns the retry policy?
- Can a retry amplify load or create duplicate business artifacts?
- What is the timeout/backoff/jitter budget?

## Retry storms and layered retries

AWS reliability guidance warns that retries at multiple layers can multiply load. Backoff, jitter and retry caps prevent a transient failure from becoming overload. Universal currently reasons about unknown outcomes but does not expose a single cross-tool retry/backoff policy or retry-budget model.

For ChatGPT tool execution this is particularly relevant: a model may see a timeout, retry a connector call, and accidentally repeat a side effect unless the connector/provider or owner gateway supplies idempotency and postcondition reconciliation.

## Authority and replication

GitHub `main` is engineering authority, but not every real-world state is Git-owned. External ChatGPT automation/plugin state must be live-read when present-tense truth matters. This resembles distributed state replication: a repository record can be a desired policy or timestamped observation, but must not be treated as the authoritative replica when the external system owns the state.

## Current gaps

- Writer-model boundary is explicit, but there is no machine-readable **transition criterion** for when single-writer assumptions cease to hold.
- Idempotency/retry semantics are not uniformly declared per external mutation capability.
- Timeout/backoff/jitter/retry-budget expectations are not a shared execution contract.
- No formal model explores all lease/CAS/stale-writer/tool-ambiguity interleavings.

## What not to transplant

Do not add distributed consensus to a single-writer system merely because it sounds more robust. Consensus has availability, operational and cognitive costs. Use it only when the topology actually becomes multi-writer/replicated and the safety problem requires it.

## Current assessment

- Single-writer stale-write safety: **STRONG / deliberately scoped**.
- Unknown-outcome classification: **PRESENT**.
- Cross-tool idempotency/retry contract: **CURRENT GAP**.
- Multi-writer consensus: **NOT CURRENTLY REQUIRED; FUTURE THREAT-MODEL TRIGGER**.
- Formal concurrency proof: **CURRENT ASSURANCE GAP**.
