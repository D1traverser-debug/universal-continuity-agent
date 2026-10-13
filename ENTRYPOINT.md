# Universal Continuity — Entry Point

Status: ACTIVE  
Contract: v3.7  
Engineering authority: this repository `main`

## Kernel boundary

Chat is ephemeral; the durable object is the task. Universal owns cross-owner control-plane invariants; domain owners own business truth. If Continuity authority is unavailable, fail closed with `CONTINUITY_BOOTSTRAP_UNAVAILABLE`; never rebuild execution truth from Memory or old chat.

## Minimal bootstrap invariant

Do **not** preload the repository.

Every Continuity bootstrap begins with only:

1. `ENTRYPOINT.md`;
2. `CURRENT_PROTOCOL.json`.

Everything else is event-driven and cold-path unless activated.

## Lightweight ingress triage

Before material response/action classify only: `NO_DEFECT`, `INVESTIGATE`, or `CONFIRMED_DEFECT`.

- `NO_DEFECT` → normal execution; do not load full maintenance or global discovery.
- `INVESTIGATE` → inspect only evidence needed to confirm/reject; do not mutate suspected authority.
- `CONFIRMED_DEFECT` → enter maintenance in the same turn.

Systemic/non-trivial maintenance uses `runtime/maintenance_controller.py` + `SYSTEM_MAINTENANCE_POLICY.json`; it forbids stage skipping, material patching before implementation, and closure before all canonical stages.

## Intent routing

`学习继承，任务不继承` applies to **NEW_TASK**. Explicit `继承 / 继续 / 恢复 / 接着上次` is `CONTINUE` first.

- **Bare CONTINUE** → `BARE_INHERIT_DISCOVERY.json`; derive quorum from `OWNER_REGISTRY.json` and query every required source before totals.
- **Named CONTINUE** → exact owner/task manifest + short checkpoint first; global discovery only if ambiguous.
- **SYSTEM_INFRA** → explicit-only; never a bare candidate.
- **NEW_TASK** → matching owner, without unfinished task state.

`OWNER_REGISTRY.json` is the sole control-plane owner-membership authority; copied owner lists are forbidden.

## Continuation invariant

For a selected durable task: read manifest + short checkpoint; show **继承前进度** before takeover; reconcile protocol if needed; acquire/verify writer lease; load only next-action evidence/capabilities; continue from authoritative `current_stage / next_action`.

Real takeover increments `resume_epoch` and supersedes the old lease; same-writer refresh preserves both. `INCOMPLETE_DISCOVERY` never auto-resumes. Bare candidates are resumable USER tasks only.

## Event-driven authority loading

Load only when activated:

- **Owner admission/topology** → `OWNER_REGISTRY.json` + `AGENT_ARCHITECTURE_CONTRACT.json`.
- **Protocol mismatch** → `VERSION_LIFECYCLE_POLICY.json` + `LIVE_CHAT_RECONCILIATION_POLICY.json`.
- **Recovery gap** → `CONTEXT_RECOVERY_POLICY.json` → exact refs → selective history.
- **Material owner execution** → owner Skill + `continuity/EXECUTION_CAPABILITIES.json` + `EXECUTION_READINESS_CONTRACT.json`; handshake required capabilities only.
- **Execution/methodology proof** → `OWNER_ADAPTER_CONTRACT.json`, `runtime/execution_receipt.py`, `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance`; apply the current receipt/action-binding contract there rather than copying it into this bootstrap.
- **Artifact/file/storage** → `artifact_io@1.0`; `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` only when activated.
- **Plausible system-defect hypothesis** → `SYSTEM_MAINTENANCE_POLICY.json` + maintenance controller; triage before discussion. Confirmed defects enter maintenance/evolution in the same turn; never close them as an unowned “future risk”.
- **Maintenance/repeated failure/drift/material correction** → `operational_hygiene@1.0` + maintenance controller.
- **Durable learning/evolution** → `evolution@1.0` + `CONTINUOUS_LEARNING_POLICY.md`.
- **Media evidence/distillation** → `MEDIA_DISTILLATION_PROTOCOL.md`.
- **Architecture review** → `AGENT_ARCHITECTURE_CONTRACT.json` + `SYSTEM_BLUEPRINT.md`.

Methodology profiles are conditional contracts loaded only on activation. Owners pin exact versions; Floating `latest` is forbidden.

## Owner execution boundary

Declarations are capability ceilings, not execution proof. Before material owner action, refresh exact owner Skill/capability, observe only needed capabilities, evaluate readiness/methodology, use a real allowed route, bind receipts to exact action/input, and block only unavailable hard gates.

Operational proof uses `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance`; declaration conformance, owner regression or CI must not substitute for current-action proof. Normal product use remains one ChatGPT owner entry; internal executor/readiness/assurance selection must not create a second business SOP or alter the TaskContract.

## Agent product architecture

Every BUSINESS owner exposes the `agent_manifest_ref` from `OWNER_REGISTRY.json`:

`Skill/router → Runtime/executor → Workflow/state → Harness/eval → References → Continuity`.

`AGENT_ARCHITECTURE_CONTRACT.json` + `runtime/agent_architecture_audit.py` validate structure; static manifests/caches do not certify live quality.

## Maintenance and learning

Questions, suggestions, analogies, or tentative ideas are candidates, not authority. Do not infer approval; assess independently before acting unless explicitly instructed.

Systemic/non-trivial work follows the controller: outline → failure class/history → recurrence escalation → evidence/alternatives → smallest repair → validation → propagation → second-order review → durable checkpoint. `runtime/meta_maintenance.py` verifies closure structure, not during-execution control.

Do not add a permanent supervisory Agent merely to simulate independent review.

## Progress observability

Work must checkpoint **during the turn** at verified material safe points; do not intentionally wait until the final answer for the first durable write. Pure reads, transient diagnostics and unchanged state do not create heartbeat writes. Resume from the latest verified safe checkpoint. Before final response on an active durable task, persist material change and reread authority.

Material Universal `main`: when HEAD-CAS is available, Contents API material mutation is forbidden; require active lease + reread HEAD + commit-on-HEAD + `expected_sha=HEAD` + reread authority. Details: `PROGRESS_OBSERVABILITY_POLICY.json`.

Exactly one receipt:
- `进度提交：COMMITTED`
- `进度提交：NO_MATERIAL_CHANGE`
- `进度提交：COMMIT_FAILED`
- `进度提交：STALE_WRITER`

`COMMITTED` is a **durable-persistence receipt**; it is not an execution, methodology, review, quality or outcome attestation. A truthful OPEN/BLOCKED gate must itself be checkpointable; missing gate evidence does not forbid persisting that blocker. Report assurance/gate state separately from commit status.

## Performance invariant

Keep Continuity off healthy business hot paths: cheap preflight, intent-gated continuation, metadata before content, short checkpoint before deep artifacts, old history last.

## Authority order

1. compatible authoritative domain runtime/checkpoint;
2. authoritative task/system manifest;
3. current GitHub `main`;
4. action-required owner evidence;
5. rebuildable registries/observations/caches;
6. external references unless promoted;
7. chat history only as recovery evidence.

Lower authority never overwrites fresher higher-authority truth.
