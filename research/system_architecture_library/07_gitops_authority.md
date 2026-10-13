# 07 — GitOps and Change Authority

## OpenGitOps core principles

OpenGitOps defines four principles for systems managed through GitOps:

1. desired state is declarative;
2. desired state is versioned and immutable with history;
3. agents automatically pull desired state;
4. agents continuously reconcile actual state toward desired state.

The useful architectural question is not “is Git present?” but:

> Which resources are actually governed by Git-declared desired state, and which resources merely have Git-held policy or observations?

## Universal's current mixed-authority model

Universal deliberately distinguishes several classes:

- GitHub `main` as engineering/rule authority;
- task/owner checkpoints as durable execution/business state according to owner contract;
- rebuildable observation caches as lower authority;
- external product state (for example ChatGPT automation/plugin state) as live external truth when present-tense decisions depend on it;
- chat/history as non-authoritative recovery evidence.

That is more nuanced than “Git is the source of truth,” and it is correct for the current product topology.

## Main problem: GitOps applicability is resource-specific

A GitOps controller can only safely reconcile a resource when:

- Git is authorized to express the resource's desired state;
- the external system exposes an effectful reconciler path;
- repeated reconciliation is idempotent/safe;
- user intent has not revoked management;
- authority precedence is unambiguous;
- drift is actionable rather than historical evidence.

The prior monitor-deletion incident demonstrates the danger of conflating desired policy and current external state: a stale repository observation or old desired state must not resurrect something the user intentionally disabled.

## Desired-state inventory gap

Current Universal has authority rules, but no single derived inventory of managed resources with fields such as:

- resource identity;
- desired-state authority;
- observed-state authority;
- reconciler identity;
- mutation permission/consent;
- reconciliation mode: continuous / event-driven / manual / forbidden;
- idempotency strategy;
- drift policy;
- rollback/disable semantics;
- last observation generation/time.

Without this, GitOps semantics remain correct in prose but are harder to audit systematically.

## Change promotion

GitOps also intersects with promotion and environment architecture. A versioned change should move through evidence gates and eventually become desired authority only after acceptance. Universal currently has candidate-vs-authority separation and main/CAS mutation rules, but a shared machine-readable promotion chain from research → candidate → prototype → validation → accepted authority → owner rollout is not uniform across all change types.

## What not to transplant

Do not declare every external state “Git-managed.” Do not run continuous reconcilers against user-controlled product settings without explicit authorization. Do not use Git history as proof that the external world matches desired state. GitOps is strongest where Git truly owns desired configuration; elsewhere Git should contain policy, evidence or a pointer, not fabricate live truth.

## Current assessment

- Versioned engineering authority: **STRONG**.
- Authority precedence and cache discipline: **STRONG**.
- Resource-by-resource desired/observed/reconciler inventory: **CURRENT GAP**.
- Continuous reconciliation: **SELECTIVE and intentionally constrained**.
- Uniform promotion-state model: **PARTIAL**.
