# 14 — Refactor Candidate Map — FROZEN PENDING USER COMMAND

Status: `CANDIDATE_ONLY`  
Authority effect: none  
Implementation authorization: **NOT GRANTED**

This document preserves design options so the next turn can reason from evidence instead of restarting from chat. It is not a roadmap, decision, or instruction to modify production authority.

## Design principle

The likely goal is **not** to bolt UVM + MAPE-K + Kubernetes + OTP + GitOps + SRE + STPA + TLA+ onto Universal as named modules. That would create a framework zoo and exactly the bloat the system is meant to avoid.

A better refactor, if later authorized, should extract the smallest number of missing primitives that cover multiple findings.

## Candidate primitive A — Derived System Model / Architecture Graph

Could unify visibility across G02/G03/G04/G08/G15/G16/G23 without becoming authority.

Candidate content:

- owners/components;
- authority/state sources;
- desired/observed state pointers;
- environments;
- control-loop edges;
- interaction/dependency edges;
- effectors/mutations;
- monitors/evidence sources;
- supervision/recovery edges;
- verification obligations.

Constraint: derive from existing authorities where possible. New annotations must be explicitly non-authoritative. Do not create a second owner registry.

Alternatives:

1. generated graph/view from existing JSON + small annotations;
2. extend one existing architecture manifest contract;
3. no graph; add only focused environment/interaction inventories.

Do not choose until complexity/payoff comparison is rerun at M7.

## Candidate primitive B — Architecture Assurance Matrix

Could address G06/G11/G12/G14/G18.

Concept:

`requirement/invariant -> implementation/guard -> test/fault/model evidence -> coverage dimension -> live validation -> assurance ceiling`

This can serve NASA/V-model traceability, UVM scoreboard/coverage, evolutionary fitness functions and operational-readiness evidence without separate frameworks.

Constraint: generate as much as possible from existing tests/contracts; avoid manually duplicated matrices that go stale.

## Candidate primitive C — Reliability Objectives / Error Budget

Could address G05/G20/G21.

Candidate SLI families:

- continuity correctness;
- false-commit / stale-write prevention;
- routing correctness;
- recovery success/time;
- tool ambiguity reconciliation;
- bootstrap latency/tool cost;
- user durable-requirement restatement incidents;
- owner-isolation/blast-radius violations.

Open questions:

- Which measurements are actually observable without adding surveillance/toil?
- Are targets hard SLOs, engineering budgets, or regression thresholds?
- What change-freeze actions are justified when a budget is depleted?

## Candidate primitive D — Environment & Capability Matrix

Could address G04 and part of G12/G13/G17/G18.

Potential dimensions:

`environment -> tools -> credentials -> persistence -> isolation -> authoritative claims -> permitted mutations -> destructive-test policy -> evidence promotion path`

Likely environments:

ChatGPT, GitHub connector, GitHub Actions, owner runtime, plugin/MCP, external product state, sandbox/test runtime, independent verifier.

The matrix should complement `EXECUTION_READINESS_CONTRACT`, not duplicate it.

## Candidate primitive E — Recovery / Supervision / FDIR Contract

Could address G08/G09/G19/G23.

Candidate responsibilities:

- fault class;
- detection evidence;
- isolation boundary;
- affected dependencies;
- safe retry/reconcile strategy;
- retry/restart intensity/budget;
- degraded/safe-hold state;
- escalation owner;
- recovery success condition;
- concurrent-fault considerations.

This should probably be a reusable runtime/schema concept, not prose copies inside every owner.

## Candidate primitive F — Hazard / Unsafe-Control-Action Analysis

Could address G10 and improve high-impact action design.

Scope should remain narrow: Universal control plane and high-impact owner/external mutations, not ordinary text-generation stages.

Potential first control actions:

- takeover/lease change;
- authoritative commit;
- external mutation/retry;
- owner delegation;
- promotion to production authority;
- invalidation/deletion;
- recovery/re-enable;
- assurance upgrade / `COMMITTED` declaration.

Output candidates: loss/hazard catalog, unsafe-control-action table, derived constraints, tests/evidence links.

## Candidate primitive G — Formal Model for Writer/Commit Protocol

Could address G07/G24.

Initial bounded TLA+/equivalent model candidate:

- active writer lease;
- resume epoch;
- task version;
- observed Git HEAD;
- prepare/publish CAS;
- external HEAD movement;
- unknown transport outcome;
- authoritative reread;
- signal/state separation.

Decision criteria: implementation effort vs ability to find previously untested interleavings. Do not formalize low-risk business workflows.

## Candidate primitive H — Common-Mode Independence Record

Could address G13.

For high-assurance reviews only, record which independence axes are actually distinct:

- model/provider;
- execution context;
- evidence source;
- specification/prompt derivation;
- tool/runtime;
- reference checker;
- provenance/trace.

Avoid raw reviewer count as an assurance metric.

## Candidate primitive I — Progressive Rollout / Canary Contract

Could address G17 and reduce cross-owner blast radius.

Candidate states:

`LAB -> UNIVERSAL_PILOT -> OWNER_OPT_IN/PILOT -> OBSERVE -> PROMOTE / ROLLBACK / HOLD`

Each promotion would require entry criteria, time/evidence window, rollback plan, affected owners and assurance ceiling.

This is inspired by release engineering/GitOps but must preserve owner authority.

## Candidate primitive J — Chaos / Resilience Experiment Contract

Could address G18 and expand current synthetic fault tests.

Fields:

- steady-state hypothesis;
- experimental fault;
- environment;
- blast radius;
- abort condition;
- expected isolation/recovery;
- measured result;
- cleanup/rollback;
- promotion decision.

Default live-production BUSINESS mutation experiments remain prohibited unless separately justified/authorized.

## Candidate primitive K — Writer-Model Transition Guard

Could address G24 without implementing consensus prematurely.

The system could explicitly declare conditions that invalidate `SINGLE_ACTIVE_CHAT`, such as multiple autonomous authoritative reconcilers or replicated writer state. Crossing the condition would block continued reliance on current lease/CAS assumptions until a new consistency design is reviewed.

## Consolidation hypothesis

If later authorized, the highest-payoff design may be **5–7 cross-cutting primitives**, not 20 framework modules:

1. derived system model;
2. assurance/coverage matrix;
3. reliability objectives;
4. environment matrix;
5. supervision/FDIR contract;
6. hazard/control analysis for high-impact actions;
7. formal model + independence/rollout extensions where justified.

This hypothesis must be challenged at M7. A smaller repair may be better.

## Explicit hold

No current policy/runtime/test/owner/business behavior is modified by this file. The maintenance run must remain blocked at `M7_IMPLEMENTATION_AND_SUPERSESSION` until the user explicitly instructs the system to adjust/refactor.
