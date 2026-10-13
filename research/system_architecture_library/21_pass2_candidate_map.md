# 21 — Pass-2 Candidate Map — FROZEN

Status: `CANDIDATE_ONLY / NON_AUTHORITY / USER_REFACTOR_COMMAND_REQUIRED`

Pass 2 does not authorize implementation. It narrows candidate design so later refactor work does not become a framework zoo.

## Consolidation principle

The new agent-runtime research reinforces the earlier hypothesis: the highest-payoff architecture is likely a small set of **cross-cutting primitives**, not separate UVM/MAPE-K/Kubernetes/OTP/SRE/OpenAI/Microsoft/ADK/LangGraph modules.

### Candidate A — Derived System Model
Cover owners, authorities, environments, interaction/dependency edges, desired/observed sources, reconcilers, supervision edges, effectors and evidence paths. Must be derived/non-authoritative where possible.

### Candidate B — Assurance / Coverage Trace
`requirement/invariant -> guard/implementation -> verifier/reference model -> tests/fault/model coverage -> live evidence -> assurance ceiling`.

Add explicit coverage dimensions for state transitions, runtime substrate, owner interaction, replay/resume and recovery paths.

### Candidate C — Reliability Objectives
Only where observable: correctness incidents, false commit/stale write, wrong owner routing, recovery success/time, external observation freshness, user restatement incidents, toil and hot-path/tool cost. Avoid invented SLO percentages without measurement.

### Candidate D — Environment + Runtime Semantics Matrix
Extend—not duplicate—execution readiness with:

`environment/runtime -> persistence -> session/workflow/memory/artifact state -> credentials/isolation -> protocol versions -> replay unit -> permitted effects -> evidence ceiling`.

This candidate absorbs G04/G28/G29 and part of G27.

### Candidate E — Execution Lineage + Effect Contract
Potential shared vocabulary:

`task -> action -> runtime session -> run/turn -> checkpoint -> nested execution -> tool/request -> external operation`.

Effectful capability declaration could include idempotency identity, semantic subject/parameters, timeout/retry ownership, ambiguous-outcome reconciliation, post-effect receipt and HITL binding.

This candidate consolidates G19/G25/G26 and prevents separate “approval subsystem” and “retry subsystem” duplication.

### Candidate F — Supervision / FDIR
Fault classification, detection evidence, isolation boundary, affected dependencies, retry/restart budget, degraded/safe-hold state, escalation owner, recovery success criteria and concurrent-fault behavior.

### Candidate G — Hazard / Unsafe-Control-Action Analysis
Scope only high-impact control-plane/external mutations: takeover, commit, retry, delete/invalidate, promote, re-enable/recover, delegate and assurance upgrade.

### Candidate H — Formal Writer/Commit Model
A bounded TLA+/equivalent model for lease/resume_epoch, observed HEAD/CAS, ambiguous outcomes, authoritative reread and state/signal separation. Do not formalize ordinary BUSINESS prose workflows.

### Candidate I — Independence + Evaluation Promotion
For high-assurance review: independence axes (model/provider/spec/evidence/runtime/reference checker) plus a promotion loop from live failure/user correction to reproducible eval, regression, measured improvement and online observation.

### Candidate J — Progressive Rollout / Chaos Contract
Potential common lifecycle for risky cross-owner changes and resilience tests:
`LAB -> UNIVERSAL_PILOT -> OWNER_OPT_IN -> OBSERVE -> PROMOTE/ROLLBACK/HOLD` with steady-state, blast radius, abort, rollback and evidence criteria.

## New anti-bloat constraints from Pass 2

1. Do not create a generic “Agent Runtime Abstraction” that erases real replay/state differences between OpenAI, Microsoft, ADK, LangGraph or owner-native runtimes.
2. Prefer typed declarations and derived views over copying framework state into Universal.
3. Do not place current framework versions in hot-path startup. Re-observe version-specific facts only when the capability is selected.
4. Do not persist trace/eval telemetry as task authority; link evidence by reference.
5. Do not equate checkpoint support with exactly-once external effects.
6. Do not create permanent LLM supervisor/reviewer roles when a deterministic guard or passive monitor suffices.
7. Do not centralize BUSINESS workflow semantics into Universal.

## Decision hold

At M7, if the user later authorizes refactor, these candidates must be re-compared against current authority, implementation cost and deletion/payoff criteria. This file is not a roadmap and none of A–J is pre-approved.