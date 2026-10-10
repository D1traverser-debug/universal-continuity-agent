# Universal Continuity — System Blueprint

Status: ACTIVE
Protocol: v3.7
Engineering authority: `D1traverser-debug/universal-continuity-agent@main`

## Purpose

This file is the top-level architecture map for Universal Continuity. Lower-level contracts, policies, Skills and owner adapters implement this blueprint; they must not contradict it.

The user is not the migration operator or the system maintenance operator. Universal Continuity owns protocol evolution, compatibility decisions, owner adaptation, progress observability, version hygiene and maintenance closure for defects inside its authority. Domain owners retain business truth.

## Architecture layers

1. **Account routing layer** — `STARTUP_HOOK.md`. Personalization/Custom Instructions route explicit continuation intent into Continuity. They are an account-level trigger, not task storage.
2. **Discovery and routing layer** — `BARE_INHERIT_DISCOVERY.json`, `OWNER_REGISTRY.json`, executable harness. Finds exact durable tasks without treating chat memory as authority.
3. **Recovery layer** — `CONTEXT_RECOVERY_POLICY.json`. Loads metadata -> short handoff -> exact artifacts -> selective history.
4. **Compatibility and protocol reconciliation layer** — `VERSION_LIFECYCLE_POLICY.json`, `LIVE_CHAT_RECONCILIATION_POLICY.json`. Reconciles old task/chat protocol metadata to the current protocol without making the user migrate anything.
5. **Domain owner layer** — owner runtime/checkpoint. Business rules, business state machines and business artifacts stay with the domain owner.
6. **Writer ownership layer** — `resume_epoch` + `active_lease`. New-chat takeover changes the lease; an in-place protocol upgrade in the same active chat does not.
7. **Progress observability layer** — `PROGRESS_OBSERVABILITY_POLICY.json`. Shows pre-resume durable progress and verified per-turn commit status.
8. **Learning/evolution layer** — `CONTINUOUS_LEARNING_POLICY.md`, `MEDIA_DISTILLATION_PROTOCOL.md`, modular Skills and tests. Learning is distilled into the smallest authoritative surface.
9. **System maintenance layer** — `SYSTEM_MAINTENANCE_POLICY.json`. A detected systemic defect triggers an autonomous diagnose -> patch -> guard -> validation -> record -> authoritative reread loop by default; internal maintenance must not wait for the user to enumerate adjacent follow-ups.
10. **Artifact/context governance layer** — `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`. Separates engineering authority, durable task state, business evidence, learning evidence, rebuildable cache, session scratch, external references and ChatGPT personalization context; defines promotion, invalidation and cleanup rules so stale files or remembered context cannot silently become execution truth.
11. **Lifecycle/cleanup layer** — current executable protocol stays in the working tree; superseded implementations live in Git history. Historical business evidence is never deleted merely because the protocol changed.

## Authority order

1. Compatible authoritative domain business checkpoint/runtime.
2. Authoritative per-task/per-system manifest for routing, lease and protocol metadata.
3. Current GitHub `main` engineering authority for GitHub-backed agent code/contracts/Skills/policies.
4. Explicit owner-referenced business evidence needed by the current action.
5. Universal registry/index cache and other rebuildable mirrors.
6. External reference surfaces such as Library, Drive, Notion or project sources unless the owner contract explicitly promotes/designates them.
7. Chat memory / past chat history as recovery evidence only.

A lower authority may never overwrite fresher higher-authority business truth.

Behavioral instruction precedence is a separate concept from data authority. Account Custom Instructions are a global routing/UX surface; Project instructions may be scope-local and may override global Custom Instructions inside that Project. Neither is durable business checkpoint storage. A current user instruction may change a requirement, but a material durable change must be persisted by the valid owner writer before later chats can treat it as task authority.

## Artifact/context lifecycle invariant

Follow `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`.

Cross-agent minimum rules:

- caches, mirrors, derived summaries and session scratch are rebuildable/non-authoritative;
- material ideas or decisions that exist only in chat are not durable evolution;
- raw learning evidence does not automatically become a rule;
- Library/Drive/Notion/Slack/project sources are reference/evidence by default, not executable checkpoint authority;
- stale caches are rebuilt or deleted rather than migrated as truth;
- duplicate active rules/docs are consolidated to one authority instead of accumulating parallel copies;
- accepted/published business evidence and task checkpoints are preserved according to owner retention and compatibility rules;
- superseded engineering implementations leave the active tree when safe; Git history is the implementation archive.

Universal owns the cross-agent classification/promotion/cleanup contract. Each domain owner owns its business-specific storage schema, retention, artifact invalidation graph and learning promotion decisions.

## Version model

- The active working-tree protocol is singular: v3.7.
- Old executable protocol copies are not kept active for convenience. Git history is the historical implementation archive.
- Historical task/business facts remain durable even if created under an older protocol.
- `continuity_protocol_version` identifies the Universal Continuity protocol.
- `contract_version` remains accepted as a legacy compatibility field until all owners migrate; new manifests should also expose `continuity_protocol_version` so Universal protocol and business/domain contract versions cannot be confused.
- An old chat is not permanently pinned to the protocol version it started with.

## Live-chat upgrade invariant

A chat that already owns a valid task lease may continue after Universal Continuity is upgraded.

Before its next material checkpoint/final durable response, it must reconcile against the current protocol:

1. read current protocol marker/policies;
2. compare persisted task protocol metadata;
3. classify COMPATIBLE / MIGRATABLE / INCOMPATIBLE / UNKNOWN;
4. apply a safe additive migration in place when supported;
5. preserve the existing lease and `resume_epoch` for the same active chat;
6. persist and re-read the adaptation record before claiming it is migrated;
7. then apply current progress-observability rules.

Only a genuine new-chat takeover increments `resume_epoch` and supersedes the old lease.

## User responsibility boundary

The user does **not**:

- choose migration paths;
- rewrite old checkpoints;
- decide which obsolete implementation files to keep;
- manually adapt each old chat;
- reason about owner schema differences;
- verify whether a write really persisted;
- discover related system-maintenance follow-ups one by one;
- maintain upgrade/change records for internal system changes;
- decide which regression guard should be added after an internal defect;
- classify caches, scratch files, learning evidence or external references by hand;
- manually reconcile stale duplicate files across agent repositories.

The user only supplies genuinely external facts/actions, permissions, account/UI operations or decisions that cannot be inferred safely.

## Autonomous maintenance invariant

When the active maintenance writer detects a systemic defect, drift, propagation gap, weak authority boundary, regression, duplicated/superseded mechanism, artifact/context lifecycle defect or execution-evidence gap inside Universal Continuity / the cross-agent control plane, it must follow `SYSTEM_MAINTENANCE_POLICY.json`.

Default behavior is to continue the maintenance closure without waiting for another user prompt:

`DETECT -> CLASSIFY AUTHORITY -> READ CURRENT TRUTH -> ROOT-CAUSE DIAGNOSIS -> MINIMUM SAFE PATCH -> REGRESSION GUARD -> VALIDATION/CI -> CHANGE/STATUS RECORD -> AUTHORITATIVE REREAD -> REPORT`

Stop and require the user only at a precise external boundary such as account/UI action, new permission/credential, irreversible high-impact choice, or an unrecoverable missing fact. A material maintenance change must leave durable evidence of the problem, root cause, changed authority surfaces, validation, behavioral effect, remaining risks, current stage and next action.

This maintenance autonomy does not authorize stealing another active owner lease or rewriting domain business truth.

## Upgrade classification

- **PATCH / hardening**: tests, cleanup, documentation, owner conformance, compatible adapter additions. Keep the same protocol version.
- **MINOR protocol change**: new required semantics that remain migratable from the previous active protocol. Version bump required with an explicit migration edge.
- **BREAKING protocol change**: incompatible task semantics or persistence model. Version bump required; affected state must fail closed or migrate through an explicit audited path.

Do not increment the protocol number for every internal improvement.

## Cleanup invariant

Delete or archive from the active root any completed migration/cutover artifact that is no longer part of runtime/bootstrap authority. Before deletion, consolidate any still-useful audit facts into `archive/` or a current status artifact. Git history preserves the original files.

Do not delete:

- current business checkpoints;
- historical decisions/evidence needed for audit or causality;
- artifacts referenced by active `next_action`;
- compatibility evidence still required by a supported migration edge;
- accepted/published business artifacts that remain owner-retained evidence.

Delete/rebuild when safe:

- stale rebuildable caches/mirrors;
- obsolete duplicate active docs after consolidation;
- superseded executable implementations once no supported migration path depends on them;
- stale external copies that materially risk drift, while preserving the true source/evidence owner.

## Required final-response behavior

For every active durable task, every final response follows `PROGRESS_OBSERVABILITY_POLICY.json`. `COMMITTED` is only valid after authoritative re-read verification. The outer account instruction is a routing/UX backstop; owner persistence remains the proof.

A material system/business learning or decision that exists only in chat cannot justify `COMMITTED` as durable evolution. It must be persisted to the appropriate owner/system authority or explicitly recorded as an unpromoted pending hypothesis.

## Sibling universal execution control plane

Universal Continuity is intentionally **not** the business executor. GitHub-backed business agents use the sibling execution control plane defined by:

- `ORCHESTRATION_BLUEPRINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `OWNER_EXECUTION_REGISTRY.json`
- `runtime/execution_readiness.py`

After Continuity has resolved an exact owner/task, the execution control plane determines whether the next action is merely declared, actually wired, executable in the current session, or requires attested isolated execution.

This separation prevents two opposite failures:

1. treating a repository full of Skills/roles/configuration as if every specialist had actually run;
2. declaring an entire GitHub agent unusable merely because one strict capability (for example isolated multimodal review) is unavailable.

The execution dispatcher should maximize valid work under current capabilities, use CHAT_BRIDGED execution only where owner assurance permits, and fail closed at the exact missing hard capability. It may never rewrite domain business state except through the domain owner's own runtime/checkpoint contract.

The execution-readiness contract has its own version (`1.0`) and does **not** require a Continuity protocol bump merely because execution orchestration hardening changes.

## Read order

`ENTRYPOINT.md` -> `SYSTEM_BLUEPRINT.md` -> `STARTUP_HOOK.md` -> `CONTINUITY_CONTRACT.json` -> `VERSION_LIFECYCLE_POLICY.json` -> `LIVE_CHAT_RECONCILIATION_POLICY.json` -> `SYSTEM_MAINTENANCE_POLICY.json` -> domain-specific policy/artifacts as needed.

Load `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` when the turn involves storage location, cache/scratch promotion, stale files, external sources, duplicate/superseded artifacts, chat-only learning persistence or authority conflict. It is not required on every ordinary business turn.

For GitHub-backed business execution after owner/task resolution, continue with:

`ORCHESTRATION_BLUEPRINT.md` -> `EXECUTION_READINESS_CONTRACT.json` -> owner `continuity/EXECUTION_CAPABILITIES.json` -> current-session capability handshake -> owner runtime/gateway.
