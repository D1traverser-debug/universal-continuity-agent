# Universal Continuity — System Blueprint

Status: ACTIVE
Protocol: v3.7
Engineering authority: `D1traverser-debug/universal-continuity-agent@main`

## Purpose

This is the architecture map, not a second copy of every policy. Lower contracts, runtime code and owner adapters implement the map; they must not contradict it. Domain owners retain business truth.

The user is not the migration operator, internal maintenance operator, cache janitor, regression manager, cross-agent methodology integrator, or the person responsible for enumerating every missing review dimension after each repair.

## Architecture shape

Universal is intentionally a **small control kernel plus composable methodology profiles plus narrow verification harnesses**, not a giant parent Agent and not a repository that owns every domain method.

### 1. Bootstrap / routing edge

`STARTUP_HOOK.md` routes explicit continuation intent. `ENTRYPOINT.md + CURRENT_PROTOCOL.json` are the minimal repository bootstrap. Bare discovery, named routing and deeper authorities are loaded only when their event occurs.

### 2. Continuity kernel

Stable cross-agent invariants:
- durable task identity and current checkpoint;
- exact owner routing;
- protocol compatibility/reconciliation;
- single active writer lease / resume epoch;
- authoritative reread before `COMMITTED`;
- lower-authority cache/chat context never silently overriding durable truth.

Responsibility pointers remain explicit even though they are not fixed bootstrap input:
- protocol lifecycle/version compatibility -> `VERSION_LIFECYCLE_POLICY.json`;
- same-chat reconciliation / lease-preserving upgrades -> `LIVE_CHAT_RECONCILIATION_POLICY.json`;
- durable progress receipts / verified commit semantics -> `PROGRESS_OBSERVABILITY_POLICY.json`;
- progressive recovery / selective history -> `CONTEXT_RECOVERY_POLICY.json`.

The blueprint points to those authorities; it does not duplicate their detailed rules and does not require loading all of them on every turn.

### 3. Execution kernel

`ORCHESTRATION_BLUEPRINT.md`, `EXECUTION_READINESS_CONTRACT.json`, `OWNER_EXECUTION_REGISTRY.json` and `runtime/execution_readiness.py` determine whether a required owner capability is merely declared, wired, executable in this session, or independently attested.

Repository declarations are an assurance ceiling, not current execution proof. A missing hard capability blocks the exact affected gate rather than every unrelated owner capability.

### 4. Methodology composition

`OWNER_ADAPTER_CONTRACT.json` is the composition interface. Shared cross-agent methods are referenced as narrow versioned profiles and implemented through owner-local hook bindings:

- `artifact_io@1.0` -> semantics owned by `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`;
- `operational_hygiene@1.0` -> semantics owned by `SYSTEM_MAINTENANCE_POLICY.json`;
- `evolution@1.0` -> semantics owned by `CONTINUOUS_LEARNING_POLICY.md`.

`runtime/methodology_conformance.py` mechanically checks exact profile versions, required owner hooks and forbidden overrides.

Owners may specialize implementation, domain taxonomy, thresholds, artifact locations, evaluator choice and safe domain retention. They may not override kernel authority precedence, single-writer semantics, verified commit, candidate-vs-production separation, evidence-gated promotion, or destructive-mutation safety.

This is composition/extension, not an OO inheritance tree. A profile version changes when its hook/invariant contract changes; compatible improvements inside its semantics owner do not require every domain owner to copy new prose.

### 5. Domain owner boundary

Each business owner owns:
- business state machine and stage semantics;
- business evidence and accepted/published outputs;
- domain-specific invalidation/retention;
- domain-specific learning/evaluation method;
- local executors/gateways and artifacts.

Universal may validate conformance and route execution. It may not steal another active owner lease or rewrite domain business truth from a system-maintenance task.

### 6. Artifact/context boundary

Cross-agent artifact authority classes, stable identity, freshness/conflict handling, verified mutation, cache/reference treatment and cleanup safety are owned by `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`.

Library/Drive/Notion/connected apps are reference/evidence by default unless an owner explicitly designates a role. Rebuildable cache is never checkpoint authority. Google Drive may be an explicit artifact vault but not an implicit runtime checkpoint or engineering rule source.

### 7. Maintenance, learning and meta-governance boundary

`SYSTEM_MAINTENANCE_POLICY.json` owns autonomous maintenance semantics and the default meta-maintenance outline. `CONTINUOUS_LEARNING_POLICY.md` owns evidence-gated learning/evolution. `runtime/meta_maintenance.py` is a **narrow deterministic verifier**, not a second root authority and not an independent LLM reviewer.

For systemic/non-trivial maintenance, the normative path includes:
`SIGNAL CLASSIFICATION -> FAILURE/IMPACT MODEL -> LEARNING DECISION -> ALTERNATIVES/FALSIFICATION -> INSTRUCTION-SURFACE DECISION -> COMPLEXITY/EFFICIENCY BUDGET -> MINIMUM IMPLEMENTATION -> MULTI-LAYER VALIDATION -> CROSS-SUBSYSTEM PROPAGATION -> SECOND-ORDER CHALLENGE -> DURABLE LEARNING/CHECKPOINT`.

The Meta-Governance Harness may reject a closure record that omits required process evidence. A harness PASS proves only **structured process conformance**. It does not prove the diagnosis, external learning, architecture decision, chronology or result is semantically correct; those claims require appropriate independent trajectory/evidence/outcome verification.

User goals/constraints and material corrections are first-class inputs. A user-proposed mechanism, assistant first idea, another Agent/framework or optimizer output is a candidate rather than architecture authority. Nontrivial architecture adoption requires alternative comparison, failure-mode search and evidence proportional to the promoted claim.

A new supervisory LLM Agent is not implied by meta-governance. Add one only if it has a distinct execution/trace boundary and held-out evidence that the added coordination cost produces a measurable verification benefit. Otherwise prefer deterministic harnesses and existing independent graders.

## Authority order

1. compatible authoritative domain runtime/checkpoint;
2. authoritative task/system manifest for routing, lease and protocol metadata;
3. current GitHub `main` engineering authority;
4. explicit owner-referenced business evidence required by the current action;
5. rebuildable registries/indexes/caches;
6. external references unless explicitly designated by owner contract;
7. past chat/history as recovery evidence only.

Instruction precedence is separate from data authority. Custom Instructions/Project instructions may affect routing/behavior but are not durable business checkpoint storage.

## Live-chat upgrade invariant

A valid active writer may reconcile a supported protocol/profile change in place. Same-chat control-plane refresh preserves the current lease and `resume_epoch`; only a genuine new-chat takeover changes them.

Before the next affected material action, refresh the exact current owner Skill/capability/profile surfaces required by that action. Do not replay business state merely because the control plane changed.

## Autonomous maintenance invariant

A systemic defect, drift, propagation gap, repeated owner failure, stale artifact/context problem, execution-evidence defect, or material challenge to the maintenance method itself must follow `SYSTEM_MAINTENANCE_POLICY.json` rather than waiting for the user to enumerate follow-ups.

A material correction is classified into the user goal/constraint, counterexample/failure evidence and any proposed mechanism before implementation. Autonomous maintenance does not mean blindly executing the user's suggested fix; it means owning the full evidence-backed repair/evolution process.

A material maintenance change requires durable problem/root-cause/impact/learning/instruction/propagation/complexity/validation/remaining-risk evidence appropriate to its scope and an authoritative reread before `COMMITTED`.

## Lifecycle / cleanup invariant

One active engineering implementation is preferred. Superseded implementation belongs in Git history once no supported migration edge depends on it.

Owner/dependency/retention-aware GC may delete or rebuild stale caches, mirrors and superseded active mechanisms. It must not delete current checkpoints, accepted/published evidence, active-next-action dependencies or required migration/audit evidence merely because they are old.

## Hot path vs cold path

The hot path is deliberately small:

`ENTRYPOINT.md -> CURRENT_PROTOCOL.json -> event-specific authority -> exact owner state`

Do **not** use this architecture document as a command to preload all referenced files.

Conditional loads:
- bare discovery -> discovery/owner metadata only;
- protocol mismatch -> `VERSION_LIFECYCLE_POLICY.json` + `LIVE_CHAT_RECONCILIATION_POLICY.json`;
- durable progress receipt/commit verification -> `PROGRESS_OBSERVABILITY_POLICY.json` when not already satisfied by current runtime contract;
- business execution -> execution contract + exact owner capability/Skill;
- artifact/file action -> `artifact_io` profile;
- local maintenance/drift/reliability incident -> `operational_hygiene` profile and scope-appropriate maintenance path;
- systemic/non-trivial maintenance or a challenge to maintenance completeness -> full meta-maintenance path, learning/impact review and `runtime/meta_maintenance.py` closure verification;
- durable learning/evolution -> `evolution` profile;
- media evidence -> media distillation authority;
- recovery gap -> `CONTEXT_RECOVERY_POLICY.json` + selective history.

Audits, external research, Meta-Governance Harness records, unrelated owners, old conversations and inactive methodology profiles are cold-path evidence. Full global research/audit is not a business-turn primitive.

## Version model

Continuity protocol and methodology profile contracts are separate version axes. Compatible internal hardening does not require a Continuity protocol bump. A profile version bumps only when its hook/invariant contract changes; owners pin exact supported profile versions rather than floating `latest`.

A semantics-owner improvement such as maintenance governance hardening may remain compatible with the existing profile version when its owner hook/invariant contract is unchanged. New verifier/runtime versions are recorded separately and must not silently imply owner business-state migration.

## Required final-response behavior

Every active durable task follows `PROGRESS_OBSERVABILITY_POLICY.json`: `COMMITTED` is valid only after authoritative reread verification. A chat-only insight, cache write, tool-success response or unpromoted learning candidate cannot justify durable `COMMITTED`.

No maintenance pass may claim that the entire evolving system is globally error-free, that every future failure class has already been anticipated, or that all child systems/outcomes are proven merely because the scoped meta-governance/regression checks passed. Report the actual assurance ceiling and open-world boundary.
