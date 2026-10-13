# 20 — Pass-2 Current Universal Gap Audit

Status: `DIAGNOSIS_ONLY / NO_REFACTOR_AUTHORIZED / PASS2`

Baseline: Universal production/control-plane architecture as of the v69 research reopen. Pass 2 does not replace the first-pass audit; it deepens it using runtime/state/recovery/failure evidence from mature systems and current 2026 agent runtimes.

## Method

The audit now uses two complementary benchmark layers:

1. **Architecture/reliability disciplines** — NASA SE/V&V, evolutionary architecture, Team Topologies, distributed systems, UVM, MAPE-K, Kubernetes, OTP, GitOps, SRE, Operational Excellence, environment parity, public DO-178C/IEC 61508 assurance ideas, TLA+, N-version common-mode research, FDIR, STPA and Chaos Engineering.
2. **Current agent runtimes** — OpenAI Agents API/SDK, Microsoft Agent Framework, Google ADK 2.x/Agents CLI and LangGraph/LangSmith.

A named technology is not a defect criterion. A finding requires a missing capability, invariant, evidence type or explicit boundary relevant to Universal.

## First-pass findings G01–G24

All 24 first-pass findings remain valid as bounded diagnoses. Pass 2 materially strengthens several:

- **G04 environment/substrate architecture fragmented** now includes explicit harness/environment/application-server distinctions and hosted/self-hosted evidence boundaries.
- **G06 requirement→evidence trace matrix absent** now includes runtime/session/checkpoint/eval evidence lineage.
- **G08/G09 supervision/FDIR gaps** now include replay/restart granularity and bounded escalation from current agent runtimes.
- **G11/G12 verification coverage/reference separation** now include offline/online eval and passive-vs-self evidence.
- **G13 common-mode independence** now explicitly covers multi-agent runtimes sharing session history/orchestrators/model/provider/specification.
- **G19 external mutation idempotency/retry** is confirmed by lost-ack, checkpoint-gap, redelivery and node-replay failure cases across several unrelated frameworks.
- **G22 promotion lifecycle** now includes promotion of production trace failures into durable evaluation/regression evidence.
- **G23 multiple-fault analysis** now includes session/checkpoint/tool/external-system combined failures.

## New findings from Pass 2

### G25 — No unified durable execution-lineage model across adapters — HIGH

Universal has excellent task identity (`task_id`, manifest version, lease, resume epoch) and action receipts, but runtime-specific identities are not modeled as one lineage. Current agent runtimes show that correctness can depend on:

`task -> owner action -> runtime/session -> run/turn -> checkpoint -> nested agent/subgraph -> tool call/request -> external operation receipt`.

Without a common lineage vocabulary, two adapters can satisfy the same business contract while disagreeing about what constitutes “the same resumed occurrence.” This becomes material for replay, HITL, nested delegation and external effects.

**Evidence lens:** OpenAI RunState+Session exclusivity; Microsoft AgentSession vs workflow checkpoint/request identity; ADK session/event/workflow resume; LangGraph thread/checkpoint namespace.

### G26 — HITL/approval binding semantics are not shared control-plane invariants — MEDIUM-HIGH

Universal distinguishes user authorization from system inference, but there is no shared machine-readable contract for an approval’s exact subject, action parameters, execution occurrence, expiry/invalidation and restore semantics.

Mature runtimes bind approval to call/request/session identities because pause/resume, handoff, compaction and replay can otherwise apply a valid approval to the wrong occurrence.

**Required future question, not implementation:** when state/version/context changes after approval was requested, what proves the approved action is semantically identical?

### G27 — Context compaction is not governed as an execution-state transformation — MEDIUM-HIGH

Universal correctly keeps Git/durable artifacts above chat memory, but it lacks a general rule for runtimes that compact or summarize conversational/control history. Current harnesses may compact context automatically. Compaction can affect pending obligations, tool/result pairs, approval state, provenance and later model decisions.

The missing capability is not “disable compaction.” It is to declare whether compaction is execution-relevant, what invariant/control items must survive, what provenance/version exists, and what evidence can prove a resumed run is still semantically bound to the authoritative task.

### G28 — Runtime replay granularity and state-class taxonomy are not declared per execution substrate — HIGH

Universal has task state/evidence/cache categories, but runtime adapters do not share a complete declaration of:

- conversation/session state;
- workflow/checkpoint state;
- long-term memory;
- artifacts/files;
- live observed external state;
- replay unit on resume/failure;
- whether completed nested/tool work may rerun.

OpenAI, Microsoft, ADK and LangGraph all draw these boundaries differently. Treating them all as generic `runtime state` hides real semantic differences.

This refines G04 and G19 but is distinct: G04 asks *where execution happens*; G19 asks *how an effect is safely retried*; G28 asks *what state/replay semantics the runtime itself provides*.

### G29 — Protocol/integration compatibility is not represented as a first-class runtime assurance dimension — MEDIUM

Universal pins methodology profiles and protocol versions internally, but current agent systems integrate MCP, A2A, provider APIs, hosted/self-hosted runtimes and evolving SDK versions. Compatibility can fail even when an owner’s business workflow is unchanged.

A future environment/runtime declaration should be able to state protocol family/version/capability negotiation and whether evidence came from the exact deployed combination. Do not turn this into a global version matrix unless an active capability needs it.

### G30 — Evaluation feedback lifecycle is fragmented — MEDIUM

Universal has tests, audits, synthetic fault injection and owner-specific quality work, but no uniform lifecycle connecting:

`production/live failure or user correction -> trace/evidence capture -> reproducible eval case -> offline regression/fault test -> measured improvement -> promotion -> online monitoring -> retirement/supersession`.

Google Agents CLI and LangSmith make this lifecycle explicit at tooling level; Microsoft/OpenAI tracing/eval ecosystems also separate execution from evaluation. Universal’s evolution system has pieces of the loop but no single derived promotion trace.

## Cross-framework findings that are **not** current defects

- **No Raft/consensus:** current single-authoritative-writer threat model does not require replicated consensus. G24 is a transition guard, not a request to implement Raft.
- **No literal UVM environment:** verification separation/coverage is useful; UVM class/phasing architecture is not required.
- **No Kubernetes control plane:** desired/observed reconciliation is useful for suitable resources; finite tasks should remain workflows.
- **No permanent supervisor Agent:** OTP supervision principles do not justify another LLM role.
- **No blanket multi-agent orchestration:** deterministic workflow remains preferable where routing is known.
- **No certification claim:** public DO-178C/IEC material informs assurance questions only.

## Revised strengths

Pass 2 confirms several Universal choices align with mature systems:

1. Git/durable task authority above conversational memory.
2. Explicit single-writer lease/resume epoch and stale-writer rejection.
3. Observed-HEAD CAS and authoritative reread after mutation.
4. Signal plane separate from authoritative state plane.
5. Action-bound receipts and explicit unknown mutation outcome handling.
6. User suggestions are candidates, not inferred authority.
7. Deterministic controller for maintenance rather than free-form model routing.
8. Hard distinction between repository capability declaration and current session execution proof.
9. Self-attested review not promoted to independent assurance.
10. Cold learning evidence does not automatically become production policy.
11. Bounded closure claims and real reopen on failed validation.

## Priority after Pass 2

Highest architectural blind spots remain:

- G02 derived system model/outline;
- G04 environment/substrate model;
- G05 measurable reliability objectives;
- G06 assurance trace matrix;
- G07 formal model of core writer/commit protocol;
- G08/G09 supervision/FDIR;
- G10 hazard/UCA model;
- G11 coverage closure;
- G13 common-mode independence;
- G19 idempotent external mutation/reconciliation;
- G23 multiple-fault analysis;
- **G25 execution lineage;**
- **G28 runtime state/replay taxonomy.**

G26/G27/G29/G30 are important but should be integrated into those cross-cutting primitives rather than becoming standalone subsystems unless later evidence demands it.

## Assurance statement

Pass 2 is now deep enough for architecture comparison because each studied family has been examined at the level of control/runtime model, state/authority, failure/recovery, verification/observability, lifecycle/change and limitations. That is **not** exhaustive mastery of every API/source file/paid standard clause/future version. Version-sensitive framework facts must be re-observed when they become implementation dependencies.

No production refactor is authorized by this audit.