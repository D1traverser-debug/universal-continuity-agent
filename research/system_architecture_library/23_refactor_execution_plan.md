# 23 — Universal Refactor Execution Plan

Status: `DESIGN_ONLY / NOT_IMPLEMENTATION_AUTHORIZATION`
Date: 2026-10-13
Trigger: user asked why pytest count keeps increasing and requested the concrete architecture modification plan.

## Test-governance defect triage

Classification: `CONFIRMED_DEFECT` (narrow scope).

The problem is not that `323` tests is intrinsically excessive. The current suite is fast, but parts of the regression portfolio bind exact prose in Markdown/bootstrap documents rather than the behavior or machine-readable invariant itself. Recent ENTRYPOINT compression exposed this mechanically: semantically equivalent prose changes failed successive exact-string assertions.

Root cause:

- maintenance policy correctly encourages regression/eval coverage for material corrections;
- however there is no equally mechanical portfolio rule requiring consolidation/deletion when a new regression is semantically covered by an existing invariant/model;
- exact prose anchors therefore tend to accumulate monotonically;
- test count becomes a weak proxy for quality while coupling and maintenance cost rise.

Required repair before production refactor:

1. Classify tests into behavior/state-machine, contract/schema, integration/trajectory, and text/bootstrap-anchor tests.
2. Exact full-sentence Markdown assertions are allowed only when the literal user-facing token itself is the contract; otherwise test the machine-readable authority/runtime behavior and keep at most a short delegation/token check in bootstrap.
3. Repeated bug examples for the same failure class must become table/property/model cases rather than one new bespoke test function per incident.
4. A new regression must defend a unique invariant or extend an existing case matrix; duplicate semantic coverage must be merged or deleted.
5. Track coverage by invariant/failure-class, not raw pytest count. No arbitrary target test count is adopted.

## Refactor principle

Do not create six new framework subsystems. Reuse the current small kernel and fold the six screened primitive families into existing authorities/runtimes. New executable modules are allowed only where they have a unique responsibility and do not create a second authority root.

## Phase 0 — Test portfolio consolidation

Targets:
- `tests/`
- `runtime/system_audit.py`
- existing policy/contract tests

Actions:
- replace brittle long prose assertions against `ENTRYPOINT.md`, `SYSTEM_BLUEPRINT.md`, Handoff, etc. with semantic/runtime or machine-readable contract assertions;
- retain only minimal bootstrap activation/delegation anchors;
- consolidate repeated examples into parameterized case tables;
- prefer state-machine/property coverage for lease/resume/CAS/replay semantics;
- add a lightweight audit rule that flags new long exact-prose assertions against Markdown control surfaces unless explicitly allowlisted.

Expected effect: test count may fall, but the optimization target is lower semantic duplication and stronger invariant coverage, not a cosmetic number.

## Phase 1 — P1 Derived System / Authority Model

Reuse:
- `OWNER_REGISTRY.json`
- owner manifests
- `runtime/owner_topology.py`
- `runtime/system_audit.py`
- existing task/system manifests and protocol contracts

Change:
- extend `runtime/owner_topology.py` (or a narrow helper beside it) to derive one normalized in-memory system model: owners, authority refs, desired/observed sources, dependencies, reconcilers, state/evidence paths, and interaction modes;
- make `system_audit` consume that derived model rather than repeatedly reconstructing partial topology from scattered surfaces;
- do **not** create a second authoritative topology database.

Payoff: impact analysis, propagation checks and later assurance traces get one derived graph while authority remains in existing source files.

## Phase 2 — P6 Formal Writer / Commit Protocol

Reuse:
- `runtime/universal_continuity.py`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- active lease / `resume_epoch` / observed-HEAD CAS / authoritative reread

Change:
- express the writer protocol as a small explicit state machine with transitions for takeover, same-writer refresh, stale writer, pre-write observation, CAS publish, ambiguous publish outcome, reread verification and terminal receipt;
- exhaustively/property-test legal and illegal transition sequences;
- fold multiple bespoke writer regression examples into the state-machine case space.

Do not add Raft/consensus under the current single-authoritative-writer model.

Payoff: this protects the highest-risk invariant while reducing dependence on accumulated one-off tests.

## Phase 3 — P2 Runtime Semantics + Execution Lineage + Effect Contract

Reuse:
- `runtime/execution_receipt.py`
- `EXECUTION_READINESS_CONTRACT.json`
- owner capability bindings/adapters

Change:
- extend the existing receipt/expectation model with a shared lineage vocabulary:
  `task -> owner_action -> runtime/session -> run/turn -> checkpoint -> nested_execution -> tool/request -> external_operation`;
- add effect metadata only where side effects exist: idempotency identity, approval binding, retry owner, ambiguous-outcome reconciliation strategy, and post-effect evidence;
- keep substrate-specific replay/state semantics in owner/runtime adapters rather than hiding them behind one generic Agent Runtime abstraction.

Payoff: reliable retries/resume/HITL/external mutations without pretending OpenAI, Microsoft, ADK and LangGraph have identical state semantics.

## Phase 4 — P3 Assurance / Coverage / Evaluation Trace

Reuse:
- `runtime/system_audit.py`
- `runtime/agent_architecture_audit.py`
- existing contracts, tests/evals and recorded observations

Change:
- derive an assurance trace per high-value invariant:
  `requirement/invariant -> implementation/guard -> verifier/reference model -> tests/fault/model coverage -> live evidence -> assurance ceiling`;
- record independence dimensions (different code path, different evidence source, different executor/reviewer boundary) instead of reviewer/agent counts;
- use this trace to identify redundant tests and real coverage gaps.

A narrow executable helper such as `runtime/assurance_trace.py` is acceptable if it remains derived/non-authoritative.

Payoff: replace “we have 323 tests” with “these invariants have these independent evidence paths and these gaps.”

## Phase 5 — P4 Supervision / FDIR / Hazard Control

Reuse:
- `runtime/maintenance_controller.py`
- `CONTROL_SIGNAL_CONTRACT.json`
- existing BLOCKED/reopen/escalation semantics

Change:
- introduce typed fault classes and bounded recovery policy into the existing controller: detection evidence, isolation boundary, retry/restart budget, degraded/safe-hold state, escalation owner and recovery success criteria;
- for high-impact control actions only, add unsafe-control-action/hazard checks before mutation;
- do not create a permanent LLM supervisor Agent.

Payoff: repeated failure becomes controlled recovery behavior rather than another special-case patch path.

## Phase 6 — P5 Measured Reliability + Progressive Rollout / Resilience

Reuse:
- CI/audit outputs
- `HARNESS_STATUS.json` or a derived report
- current change-risk classification

Change:
- measure only observable denominators: wrong routing incidents, stale/false commit incidents, recovery success/time, user-restatement incidents, observation freshness, bootstrap bytes/tool cost, test semantic duplication and regression recurrence;
- collect baseline first; only after enough observations decide whether any SLO/error-budget threshold is justified;
- use reversible/progressive rollout only for changes whose blast radius warrants it; use bounded synthetic fault experiments, not destructive production chaos.

Payoff: architecture evolution becomes evidence-driven rather than “more rules/tests means safer.”

## Implementation order

`Phase 0 test consolidation -> Phase 1 P1 derived model -> Phase 2 P6 writer state machine -> Phase 3 P2 lineage/effects -> Phase 4 P3 assurance trace -> Phase 5 P4 fault control -> Phase 6 P5 measured reliability`

Why this order:
- fix the verification substrate before large refactor;
- establish topology and writer correctness before adding execution lineage;
- build assurance trace after the underlying models exist;
- add recovery/hazard semantics after failures are typed;
- add quantitative reliability last, once denominators are observable.

## Deletion / non-growth budget

The refactor is successful only if it can remove or consolidate active complexity. Expected deletion candidates include brittle prose-anchor tests, duplicate topology reconstruction, duplicate one-off writer regression cases, and status prose that can be derived from normalized runtime evidence.

No new root policy, registry, generic agent-runtime layer, PR-first subsystem, permanent supervisor Agent, or framework-specific module zoo is authorized by this plan.

## Authorization boundary

This document is a concrete implementation plan, not production-refactor authorization. Production mutation starts only after a separate explicit user command; at that point current authority and version-sensitive runtime facts must be reread before implementation.
