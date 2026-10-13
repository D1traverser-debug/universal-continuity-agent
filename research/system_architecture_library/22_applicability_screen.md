# 22 — Architecture Knowledge Applicability Screen

Status: `SCREEN_COMPLETE / NON_AUTHORITY / NO_PRODUCTION_REFACTOR`
Date: 2026-10-13

## User-authorized scope

The user explicitly authorized two actions:

1. remove or demote research subjects whose core material is not reliably accessible;
2. use the retained research to determine what is actually applicable to Universal.

This authorization does **not** mean “implement every framework” and does not authorize production architecture mutation in this checkpoint.

## Source-access pruning

### Excluded from the “deep-studied framework” count

- **RTCA DO-178C normative standard** — paid/copyrighted normative text is not available as a complete research corpus here.
- **IEC 61508 normative standard series** — the full normative text is paid and is not available as a complete research corpus here.

They are therefore not treated as fully studied architecture frameworks.

### Public evidence retained, but only as evidence lenses

- FAA AC 20-115D and other public FAA software-assurance material: useful for lifecycle evidence, requirements-based verification, traceability, configuration control and assurance independence.
- IEC public functional-safety overview/material: useful for lifecycle, modification/maintenance, hazard and integrity-oriented questions.

These public sources do not create certification or normative-conformance claims.

### Retained as genuinely studyable

UVM remains retained because Accellera publicly exposes user guides, class references and reference implementations. NASA SE/V&V, Evolutionary Architecture, Team Topologies, distributed-systems literature, MAPE-K, Kubernetes, OTP, OpenGitOps, Google SRE, AWS Operational Excellence, Twelve-Factor, TLA+, N-version/common-mode research, NASA FDIR, STPA, Chaos Engineering, and the current OpenAI/Microsoft/Google/LangGraph agent-runtime families all have sufficient public primary/original material for architecture-level comparison.

## Applicability result

The useful knowledge is broadly applicable, but **not as one module per framework**. The highest-payoff shape is six consolidated primitives.

### P1 — Derived System / Authority Model

Absorbs:
- NASA SE decomposition/traceability;
- Team Topologies ownership/interaction boundaries;
- MAPE-K typed knowledge/control-loop roles;
- Kubernetes desired/observed/reconciler distinctions;
- GitOps declared intent vs live observed state.

Use: derive owners, authorities, dependencies, desired/observed sources, reconcilers, interaction modes and evidence paths from existing authorities.

Do not use: a second authoritative topology database or a central “knowledge store” that competes with owner truth.

### P2 — Runtime Semantics + Execution Lineage + Effect Contract

Absorbs:
- distributed-systems idempotency/retry/ambiguous-outcome lessons;
- OpenAI Agents API/SDK session, RunState, environment and tool boundaries;
- Microsoft Agent Framework session/workflow/checkpoint/request identity;
- Google ADK Session/State/Memory/Event/Artifact and resume semantics;
- LangGraph thread/checkpointer/store/subgraph replay semantics.

Use: a shared lineage vocabulary such as:

`task -> owner action -> runtime/session -> run/turn -> checkpoint -> nested execution -> tool/request -> external operation`

and effect metadata for idempotency identity, approval occurrence, retry owner, ambiguous-outcome reconciliation and post-effect evidence.

Do not use: a generic “Agent Runtime Abstraction” that erases substrate-specific replay/state semantics.

### P3 — Assurance / Coverage / Evaluation Trace

Absorbs:
- NASA V&V and requirement-to-evidence traceability;
- Evolutionary Architecture fitness functions;
- UVM stimulus/driver/monitor/reference-model/coverage separation;
- public FAA assurance guidance;
- agent-runtime tracing/evaluation patterns;
- N-version/common-mode independence lessons.

Use: derive a trace from invariant/requirement through implementation/guard, verifier/reference model, test/fault/model coverage, live evidence and assurance ceiling; record independence axes rather than reviewer counts.

Do not use: UVM class hierarchies/phasing, certification paperwork, or self-attested review as independent assurance.

### P4 — Supervision / FDIR / Hazard Control

Absorbs:
- Erlang/OTP bounded supervision and escalation;
- NASA FDIR detection/isolation/recovery;
- STPA unsafe-control-action analysis;
- public IEC lifecycle/hazard-oriented material.

Use: fault class, isolation boundary, retry/restart budget, degraded/safe-hold state, escalation owner, recovery success criteria and high-impact unsafe-control analysis.

Do not use: permanent LLM “supervisor agents” merely to imitate OTP or safety engineering.

### P5 — Measured Reliability + Progressive Rollout / Resilience

Absorbs:
- Google SRE SLI/SLO/error-budget/toil thinking;
- AWS Operational Excellence reversible changes/readiness;
- Twelve-Factor environment-difference awareness;
- Chaos Engineering experiment contracts;
- Evolutionary Architecture controlled change.

Use only where measurable: correctness incidents, stale/false commits, wrong routing, recovery success/time, observation freshness, user-restatement incidents, tool/startup cost and bounded rollout/fault experiments.

Do not use: invented SLO percentages, destructive production chaos, or blanket canary machinery for low-risk changes.

### P6 — Formal Writer / Commit Protocol

Absorbs:
- TLA+/model-checking state-machine reasoning;
- distributed-systems stale-writer/CAS/ambiguous-outcome lessons;
- current Universal lease/resume_epoch/observed-HEAD/reread model.

Use: bounded formal modeling of the small high-value writer/commit protocol.

Do not use: Raft/consensus under the current single-authoritative-writer threat model, or formalization of ordinary prose/business workflows.

## Disposition of the earlier A–J candidates

- A Derived System Model -> **ADOPT**, folded into P1.
- B Assurance / Coverage Trace -> **ADOPT**, folded into P3.
- C Reliability Objectives -> **ADOPT CONDITIONALLY**, folded into P5.
- D Environment + Runtime Semantics -> **ADOPT**, folded into P2 and P5.
- E Execution Lineage + Effect Contract -> **ADOPT**, core of P2.
- F Supervision / FDIR -> **ADOPT**, core of P4.
- G Hazard / Unsafe-Control-Action Analysis -> **ADOPT FOR HIGH-IMPACT CONTROLS ONLY**, folded into P4.
- H Formal Writer/Commit Model -> **ADOPT BOUNDED**, core of P6.
- I Independence + Evaluation Promotion -> **ADOPT**, folded into P3.
- J Progressive Rollout / Chaos Contract -> **ADOPT CONDITIONALLY**, folded into P5.

## Explicit non-adoptions

The following are useful as negative boundaries but should not be implemented now:

- Raft/consensus without multiple authoritative writers;
- a literal UVM environment/phasing/class hierarchy;
- a Kubernetes-style control plane for finite user tasks;
- one centralized MAPE-K Knowledge database;
- permanent LLM supervisor/reviewer agents;
- a generic runtime layer that hides OpenAI/Microsoft/ADK/LangGraph semantic differences;
- blanket multi-agent orchestration when deterministic workflow is sufficient;
- certification-style DO-178C/IEC 61508 process imitation;
- fabricated SLO targets without observable denominators.

## Answer to “can all the researched knowledge be used?”

**Almost all retained knowledge has a useful role, but most of it should be used as design constraints, invariants, verification questions or failure models—not as separate subsystems.**

After consolidation, the research does not justify a framework zoo. It justifies six shared primitive families, with existing Universal mechanisms reused wherever possible.

Production implementation remains a separate decision and must start from current authority plus a smallest-change design, not from literal framework transplantation.
