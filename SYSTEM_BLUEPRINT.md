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

Both bootstrap surfaces have explicit byte budgets. A thin `SKILL.md` does not count as a thin product if the mandatory bootstrap immediately reloads a giant duplicated prompt.

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

### 3. Agent product architecture

`AGENT_ARCHITECTURE_CONTRACT.json` defines the product boundary shared by BUSINESS owners and the Universal SYSTEM_INFRA control plane:

`Skill/router -> Runtime/executor -> Workflow/state -> Harness/eval -> References -> Continuity`.

The layers are responsibilities, not mandatory framework brands:
- **Skill/router**: trigger, authority pointer, progressive loading map and hard boundaries; not the executable business system.
- **Runtime/executor**: real executable code/tool/judgment surface. OpenAI Agents SDK, deterministic, hybrid and external runtimes are all valid when declared truthfully.
- **Workflow/state**: durable stage/state authority and transition guards outside chat prose.
- **Harness/eval**: contract/trajectory/domain evals locally; shared architecture validation centrally in Universal.
- **References**: canonical progressive domain knowledge; large rules are not duplicated into the hot-path Skill.
- **Continuity**: task/recovery/capability pointers, not a replacement for domain runtime state.

Every BUSINESS owner declares `continuity/AGENT_MANIFEST.json` through its `OWNER_REGISTRY.json.agent_manifest_ref`. Universal declares root `AGENT_MANIFEST.json` for itself. Static manifests describe architecture; they do not self-certify the repository HEAD or live quality.

`runtime/agent_architecture_audit.py` is the shared architecture harness. It validates Universal locally, requires all current BUSINESS owners to have architecture pointers, and checks the recorded observation topology. An oversized Skill/bootstrap is `PASS_WITH_DRIFT`, while a missing runtime/workflow/harness layer is a structural failure.

### 4. Execution kernel

`ORCHESTRATION_BLUEPRINT.md`, `EXECUTION_READINESS_CONTRACT.json`, `OWNER_EXECUTION_REGISTRY.json` and `runtime/execution_readiness.py` determine whether a required owner capability is merely declared, wired, executable in this session, or independently attested.

Repository declarations are an assurance ceiling, not current execution proof. A missing hard capability blocks the exact affected gate rather than every unrelated owner capability.

### 5. Methodology composition

`OWNER_ADAPTER_CONTRACT.json` is the composition interface. Shared cross-agent methods are referenced as narrow versioned profiles and implemented through owner-local hook bindings:

- `artifact_io@1.0` -> semantics owned by `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`;
- `operational_hygiene@1.0` -> semantics owned by `SYSTEM_MAINTENANCE_POLICY.json`;
- `evolution@1.0` -> semantics owned by `CONTINUOUS_LEARNING_POLICY.md`.

`runtime/methodology_conformance.py` mechanically checks exact profile versions, required owner hooks and forbidden overrides.

Owners may specialize implementation, domain taxonomy, thresholds, artifact locations, evaluator choice and safe domain retention. They may not override kernel authority precedence, single-writer semantics, verified commit, candidate-vs-production separation, evidence-gated promotion, or destructive-mutation safety.

This is composition/extension, not an OO inheritance tree. A profile version changes when its hook/invariant contract changes; compatible improvements inside its semantics owner do not require every domain owner to copy new prose.

### 6. Domain owner boundary

Each business owner owns:
- business state machine and stage semantics;
- business evidence and accepted/published outputs;
- domain-specific invalidation/retention;
- domain-specific learning/evaluation method;
- local executors/gateways and artifacts.

Universal may validate conformance and route execution. It may not steal another active owner lease or rewrite domain business truth from a system-maintenance task.

### 7. State Plane vs Signal Plane

Authoritative mutation and observation transport are separate systems.

**State Plane**:
- task manifests, leases, business runtime/checkpoints and accepted business truth;
- only the current valid writer may mutate the relevant authority;
- a stale chat/CI/monitor cannot bypass the lease.

**Signal Plane**:
- `CONTROL_SIGNAL_CONTRACT.json`, `SIGNAL_PLANE.md`, GitHub Issue transport and remote-monitor observations;
- may be emitted by a stale chat, owner CI, remote monitor or active writer;
- signals are non-authoritative and only report evidence requiring re-observation;
- the active Universal maintenance writer consumes/rejects a signal before any authoritative mutation.

This prevents discoveries made by a stale writer or unattended CI from disappearing while preserving single-writer authority.

### 8. Remote architecture monitoring

`OWNER_ARCHITECTURE_OBSERVATIONS.json` is a rebuildable observation cache containing externally observed owner HEADs and architecture-validation receipts. It is not owner membership or business-state authority.

Local Universal CI can validate that this cache is structurally complete and internally consistent, but it cannot discover a newer private owner HEAD without a connected remote execution surface. A remote architecture watch therefore reads every current BUSINESS owner from `OWNER_REGISTRY.json`, compares current HEAD / Agent manifest / Skill shape / CI with the recorded observation, and emits a non-authoritative control signal when meaningful drift appears.

Remote monitoring never takes a business lease or writes business state.

### 9. Artifact/context boundary

Cross-agent artifact authority classes, stable identity, freshness/conflict handling, verified mutation, cache/reference treatment and cleanup safety are owned by `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`.

Library/Drive/Notion/connected apps are reference/evidence by default unless an owner explicitly designates a role. Rebuildable cache is never checkpoint authority. Google Drive may be an explicit artifact vault but not an implicit runtime checkpoint or engineering rule source.

### 10. Maintenance, learning and meta-governance boundary

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
5. rebuildable registries/observations/indexes/caches;
6. external references unless explicitly designated by owner contract;
7. past chat/history as recovery evidence only.

Instruction precedence is separate from data authority. Custom Instructions/Project instructions may affect routing/behavior but are not durable business checkpoint storage.

## Live-chat upgrade invariant

A valid active writer may reconcile a supported protocol/profile change in place. Same-chat control-plane refresh preserves the current lease and `resume_epoch`; only a legal takeover changes them.

Before the next affected material action, refresh the exact current owner Skill/capability/profile surfaces required by that action. Do not replay business state merely because the control plane changed.

## Autonomous maintenance invariant

A systemic defect, drift, propagation gap, repeated owner failure, stale artifact/context problem, execution-evidence defect, architecture signal, or material challenge to the maintenance method itself must follow `SYSTEM_MAINTENANCE_POLICY.json` rather than waiting for the user to enumerate follow-ups.

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
- protocol mismatch -> version/reconciliation authority;
- durable progress receipt/commit verification -> progress authority when needed;
- business execution -> execution contract + exact owner capability/Skill;
- owner admission/architecture drift -> Agent architecture contract + observations;
- artifact/file action -> `artifact_io` profile;
- local maintenance/drift/reliability incident -> `operational_hygiene` profile and scope-appropriate maintenance path;
- systemic/non-trivial maintenance or a challenge to maintenance completeness -> full meta-maintenance path, learning/impact review and `runtime/meta_maintenance.py` closure verification;
- durable learning/evolution -> `evolution` profile;
- media evidence -> media distillation authority;
- recovery gap -> recovery authority + selective history.

Audits, external research, Meta-Governance Harness records, unrelated owners, old conversations and inactive methodology profiles are cold-path evidence. Full global research/audit is not a business-turn primitive.

## Version model

Continuity protocol, methodology profiles and Agent architecture contracts are separate version axes. Compatible internal hardening does not require a Continuity protocol bump. A profile/architecture contract version bumps only when its interface/invariant contract changes; owners pin exact supported versions rather than floating `latest`.

A semantics-owner improvement may remain compatible with the existing profile version when its owner hook/invariant contract is unchanged. New verifier/runtime versions are recorded separately and must not silently imply owner business-state migration.

## Required final-response behavior

Every active durable task follows `PROGRESS_OBSERVABILITY_POLICY.json`: `COMMITTED` is valid only after authoritative reread verification. A chat-only insight, cache write, tool-success response, control signal or unpromoted learning candidate cannot justify durable `COMMITTED`.

No maintenance pass may claim that the entire evolving system is globally error-free, that every future failure class has already been anticipated, or that all child systems/outcomes are proven merely because the scoped meta-governance/regression checks passed. Report the actual assurance ceiling and open-world boundary.
