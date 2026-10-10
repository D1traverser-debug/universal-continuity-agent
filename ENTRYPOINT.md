# Universal Continuity — Entry Point

Status: ACTIVE
Contract: v3.7
Engineering authority: this repository `main`

## Critical startup boundary

Chat is an ephemeral execution window; the durable object is the task. GitHub/Library are storage and discovery surfaces, not automatic event listeners. Bare `继承 / 继续 / 恢复` therefore requires the account startup hook in `STARTUP_HOOK.md`.

If required Continuity resources cannot actually be accessed, fail closed with `CONTINUITY_BOOTSTRAP_UNAVAILABLE`; do not reconstruct execution truth from Memory or old chat text.

## Core ownership

Universal Continuity owns discovery, routing, compatibility, takeover lease semantics, progress observability, recovery pointers and cross-agent control-plane invariants. Domain owners retain business rules, business state machines, evidence and business artifacts. The sibling execution plane owns capability handshake/routing evidence, not business state.

## Intent precedence

`学习继承，任务不继承` applies to **NEW_TASK**. Explicit continuation intent (`继承`, `继续`, `恢复`, `接着上次`, or a named continuation) is `CONTINUE` first.

## Minimal bootstrap invariant

Do **not** preload the whole repository.

Every Continuity bootstrap begins with only:

1. `ENTRYPOINT.md`;
2. `CURRENT_PROTOCOL.json`.

Everything else is event-driven. Load an authority only when the current action activates it. `SYSTEM_BLUEPRINT.md`, audits/research, unrelated owner repositories and old transcripts are cold-path references, not mandatory startup context.

## Event-driven authority loading matrix

- **Bare CONTINUE** -> `BARE_INHERIT_DISCOVERY.json` + owner metadata/index sources required for complete discovery.
- **Named CONTINUE** -> exact owner/task manifest + short owner checkpoint first; skip global discovery unless resolution is ambiguous.
- **Protocol mismatch** -> `VERSION_LIFECYCLE_POLICY.json` + `LIVE_CHAT_RECONCILIATION_POLICY.json`.
- **Recovery gap** -> `CONTEXT_RECOVERY_POLICY.json`, then exact artifact refs, then selective history only if still needed.
- **Material GitHub-backed business execution** -> `OWNER_EXECUTION_REGISTRY.json`, `EXECUTION_READINESS_CONTRACT.json`, exact owner Skill/entrypoint, exact owner `continuity/EXECUTION_CAPABILITIES.json`, then current-session handshake only for required capabilities.
- **Artifact/file/storage operation** -> `artifact_io@1.0` profile from `OWNER_ADAPTER_CONTRACT.json`; load `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` only when its semantics are needed.
- **Maintenance/repeated failure/drift/cleanup** -> `operational_hygiene@1.0`; load `SYSTEM_MAINTENANCE_POLICY.json`.
- **Durable learning/evolution claim** -> `evolution@1.0`; load `CONTINUOUS_LEARNING_POLICY.md`.
- **Media evidence/distillation** -> `MEDIA_DISTILLATION_PROTOCOL.md`.
- **Architecture/control-plane review** -> `SYSTEM_BLUEPRINT.md` plus only the implicated contracts/policies.

Methodology profiles are composable interface contracts, not copied parent-agent prose. Owners bind domain-local hooks and may specialize local methods, but cannot override kernel authority/evidence/reliability/destructive-mutation invariants. Declaration conformance is mechanically evaluated by `runtime/methodology_conformance.py`. Every profile defined by the current contract must be explicitly assessed as `APPLIES` or `NOT_APPLICABLE` with owner-local reason/evidence; omission is not a valid negative decision. Declaration/CI alone is never action-level operational proof.

## Task identity and topology

Every durable USER task has:
- stable machine `task_id`;
- user-facing `display_name_zh`.

A rename never changes `task_id`. Same goal/same work keeps the same task. A materially different major branch that must coexist may become a child task. A one-shot side question should not mutate durable progress by default.

## New-chat continuation

After routing to Continuity:

1. classify CONTINUE vs NEW_TASK;
2. resolve exact task or complete bare candidates;
3. read authoritative manifest + short checkpoint;
4. capture and show **继承前进度** before takeover mutation;
5. reconcile compatibility only if needed;
6. for a genuine new-chat takeover, increment `resume_epoch` and acquire/verify a new lease with owner version/CAS guard where available;
7. load only artifacts/capabilities/profiles needed by the real `next_action`;
8. continue from authoritative `current_stage / next_action`.

Same-chat protocol/control-plane refresh preserves the current lease and `resume_epoch`. Only a genuine new-chat takeover changes them.

If a required bare-discovery source fails, return `INCOMPLETE_DISCOVERY`; never present a partial list as authoritative total.

## Bare inherit eligibility

Plain `继承/继续` candidates must have:
- `task_class == USER`;
- `resume_eligible == true`;
- `resume_visibility == DEFAULT`;
- status in `ACTIVE / WAITING / BLOCKED`.

SYSTEM_INFRA/TEST/FIXTURE/EVAL/MIGRATION/terminal/hidden tasks are not bare candidates. An explicit SYSTEM_INFRA task may resume only when its own visibility/eligibility permits it.

## Compatibility

A resumed task is `COMPATIBLE`, `MIGRATABLE`, `INCOMPATIBLE`, or `UNKNOWN`. Supported additive migrations are system work, not user work. Unknown or incompatible execution truth fails closed rather than being guessed from chat memory.

## GitHub-backed owner execution

Repository declarations establish at most a capability ceiling, not current execution proof.

Before a material owner action:
1. refresh the exact owner Skill/entrypoint and capability manifest;
2. identify only capabilities needed by the current next action;
3. perform current-session observations/handshake;
4. evaluate with `runtime/execution_readiness.py`;
5. evaluate the owner's methodology declaration with `runtime/methodology_conformance.py:evaluate_methodology_conformance`; every contract profile must have explicit applicability evidence, and any `APPLIES` profile must be exact-version bound before execution proceeds;
6. determine which bound methodology profiles are activated by the concrete action/event and load only those profiles;
7. route via owner-native, permitted CHAT_BRIDGED, deterministic, or attested-isolated execution as allowed;
8. for every activated methodology profile that supports or constrains the material action, assemble receipt-contract-1.2 `profile_runs` evidence with profile version, activation id/trigger, explicit `INVOKED`/`NOT_APPLICABLE_FOR_ACTION` assessment for every profile hook, and stable evidence refs;
9. require an independent evidence verifier for referenced evidence **and** a separate independent hook-assessment verifier that judges whether the verified refs and stated reason actually support each hook assessment; a real but irrelevant ref is not proof;
10. evaluate the activated subset with `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance` before claiming the profile-dependent gate, mutation or durable progress is complete;
11. if declaration applicability is missing/inconsistent, fail closed before the action; if an activated profile lacks a current receipt, complete hook assessment, verified evidence ref, semantic assessment verification, or independent verifier, fail closed only for that profile-dependent action/gate; declaration conformance, owner regression or CI must not substitute for missing operational proof;
12. block only the exact hard capability/profile-dependent gate that is unavailable;
13. require execution/artifact/review receipts for gates that claim completion.

`DECLARED_ONLY` is not execution. `HARNESS_WIRED` is not session proof. `ATTESTED_ISOLATED` cannot be simulated by role-switching inside one unverified chat. A methodology declaration marked `BOUND_EXACT_VERSION` or an owner CI PASS proves wiring/regression only; it does not prove the current material action activated and satisfied the profile. Conversely, an omitted profile is not assumed non-applicable: the owner must make that exclusion explicit and evidence-bearing.

## Artifact and methodology invariants

Shared cross-agent methodology is composed rather than inherited as a giant parent behavior bundle:

- `artifact_io@1.0` -> stable identity, freshness/conflict handling, verified mutation, invalidation, retention/cleanup and artifact-vault bindings;
- `operational_hygiene@1.0` -> incident evidence, self-maintenance trigger, owner-aware GC and scoped reliability freeze;
- `evolution@1.0` -> learning evidence, independent candidate critique, eval/regression promotion and superseded-mechanism cleanup.

Owners pin exact profile versions and bind local hooks. Floating `latest` is forbidden. Every current contract profile also has a mandatory applicability assessment. `APPLIES` requires binding; `NOT_APPLICABLE` requires a concrete reason and owner-local evidence refs. Domain specialization may change implementation, taxonomy, thresholds or evaluator selection inside allowed boundaries; it may not weaken authority precedence, single-writer semantics, verified commit, candidate-vs-production separation, evidence-gated promotion, or destructive-mutation safety.

Operational methodology conformance is event/action scoped. It must be evaluated only for profiles activated by the current action, but for those activated profiles it is mandatory before the profile-dependent action can be represented as operationally complete or durably committed. Under receipt contract 1.2, reference verification and semantic hook-claim verification are distinct requirements; evidence existence alone cannot establish that a hook ran or was genuinely inapplicable.

## Learning and maintenance

External advice, user analogies, assistant first ideas and other Agent/framework proposals are candidates, not architecture authority. For nontrivial adoption: inspect current authority, separate goal from proposed mechanism, compare a credible alternative, actively seek a failure mode/counterexample, then require relevant eval/regression evidence before production promotion.

When a systemic defect or repeated owner failure is inside the current maintenance writer's authority, follow the maintenance closure instead of stopping at explanation. The user does not maintain the internal defect backlog.

## Progress observability

For every final response on an active durable task, emit exactly one `进度提交` state:
- `COMMITTED` only after material write + authoritative reread verification;
- `NO_MATERIAL_CHANGE` when the durable resume point did not change;
- `COMMIT_FAILED` when intended durable progress could not be verified;
- `STALE_WRITER` when this chat lost its lease.

If the current material write/action activated a methodology profile, `COMMITTED` also requires operational conformance for that activated profile when the profile governs the write/action. Missing action-level profile evidence is not a reason to fabricate PASS; it is an exact gate blocker.

A tool-success response, cache write or model memory is never commit proof.

## Performance invariant

Continuity stays off the steady-state business hot path:
- global discovery only for bare continuation or unresolved routing;
- metadata before content;
- short checkpoint before deep artifacts;
- targeted execution handshake only for current action;
- methodology declaration/applicability validation at owner-entry boundaries, not as broad repository preload;
- methodology profiles loaded only when their activation event occurs;
- operational methodology validation only for the profiles activated by the current material action;
- maintenance/research/audits are cold path;
- old chat history is last resort;
- no material change means no heartbeat write.

## Authority order

1. compatible authoritative domain runtime/checkpoint;
2. authoritative task/system manifest for routing/lease/protocol metadata;
3. current GitHub `main` engineering authority for code/contracts/profiles;
4. explicitly owner-referenced business evidence required now;
5. rebuildable registries/caches;
6. external references unless explicitly designated by owner contract;
7. chat history only as recovery evidence.

A lower authority may not silently overwrite fresher higher-authority truth.
