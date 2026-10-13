# Universal Continuity — Entry Point

Status: ACTIVE  
Contract: v3.7  
Engineering authority: this repository `main`

## Kernel boundary

Chat is ephemeral; the durable object is the task. Universal owns cross-owner control-plane invariants; domain owners keep business rules/state/evidence/artifacts. If required Continuity resources are unavailable, fail closed with `CONTINUITY_BOOTSTRAP_UNAVAILABLE`; never rebuild execution truth from Memory or old chat.

## Minimal bootstrap invariant

Do **not** preload the repository.

Every Continuity bootstrap begins with only:

1. `ENTRYPOINT.md`;
2. `CURRENT_PROTOCOL.json`.

Everything else is event-driven and cold-path unless its event activates it.

## Lightweight ingress triage

Before a material response/action, do only a cheap defect-signal preflight: `NO_DEFECT`, `INVESTIGATE`, or `CONFIRMED_DEFECT`.

- `NO_DEFECT` → continue normal owner/business execution; do not load full maintenance or run global discovery.
- `INVESTIGATE` → inspect only evidence needed to confirm/reject the defect; no suspected-authority mutation.
- `CONFIRMED_DEFECT` → enter current maintenance in the same turn.

For systemic/non-trivial maintenance, `runtime/maintenance_controller.py` enforces `SYSTEM_MAINTENANCE_POLICY.json`. It forbids stage skipping, material patching before implementation, and closure before all canonical stages; re-open invalidates downstream receipts.

## Intent routing

`学习继承，任务不继承` applies to **NEW_TASK**. Explicit `继承 / 继续 / 恢复 / 接着上次` is `CONTINUE` first.

- **Bare CONTINUE** → `BARE_INHERIT_DISCOVERY.json`; derive the complete source quorum from `OWNER_REGISTRY.json`; query every required source before reporting a total.
- **Named CONTINUE** → exact owner/task manifest + short checkpoint first; global discovery only if ambiguous.
- **SYSTEM_INFRA** → explicit-only; never a bare candidate.
- **NEW_TASK** → matching owner, without unfinished task state.

`OWNER_REGISTRY.json` is the sole control-plane owner-membership authority. Parallel copied owner lists are forbidden.

## Continuation invariant

For a selected durable task: read authoritative manifest + short checkpoint; show **继承前进度** before takeover mutation; reconcile protocol only if needed; acquire/verify writer lease; load only next-action artifacts/capabilities; continue from authoritative `current_stage / next_action`.

A real takeover increments `resume_epoch` and supersedes the old lease. Same-writer refresh preserves both. Partial discovery is `INCOMPLETE_DISCOVERY` and never auto-resumes. Bare candidates are resumable USER tasks only; hidden/system/test/eval/migration tasks stay excluded.

## Event-driven authority loading

Load only when activated:

- **Owner admission/topology** → `OWNER_REGISTRY.json` + `AGENT_ARCHITECTURE_CONTRACT.json` + derived conformance surfaces.
- **Protocol mismatch** → `VERSION_LIFECYCLE_POLICY.json` + `LIVE_CHAT_RECONCILIATION_POLICY.json`.
- **Recovery gap** → `CONTEXT_RECOVERY_POLICY.json` → exact artifact refs → selective history only if needed.
- **Material owner execution** → exact owner Skill/entrypoint + `continuity/EXECUTION_CAPABILITIES.json` + `EXECUTION_READINESS_CONTRACT.json`; handshake only required capabilities.
- **Execution/methodology proof used for a gate** → `OWNER_ADAPTER_CONTRACT.json`, `runtime/execution_receipt.py`, `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance`; do not copy their algorithms here.
- **Artifact/file/storage** → `artifact_io@1.0`; load `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` only when activated.
- **Plausible system defect** → `SYSTEM_MAINTENANCE_POLICY.json` + `runtime/maintenance_controller.py`; triage before mutation.
- **Maintenance/repeated failure/drift/material correction** → `operational_hygiene@1.0` + maintenance policy/controller.
- **Durable learning/evolution** → `evolution@1.0` + `CONTINUOUS_LEARNING_POLICY.md`.
- **Media evidence/distillation** → `MEDIA_DISTILLATION_PROTOCOL.md`.
- **Architecture/control-plane review** → `AGENT_ARCHITECTURE_CONTRACT.json` + `SYSTEM_BLUEPRINT.md` + implicated contracts only.

Methodology profiles are conditional contracts loaded only on activation. Owners pin exact versions; Floating `latest` is forbidden.

## Owner execution boundary

Repository declarations are capability ceilings, not current execution proof. Before a material owner action, refresh the exact owner Skill/capability manifest, observe only capabilities needed now, evaluate readiness/methodology, use only an allowed route at its real assurance level, bind receipts to exact task/stage/action/subject/input, and block only the exact unavailable hard gate.

Normal product use is one ChatGPT owner entry. Executor/readiness/assurance selection is system-internal and must not create a second business SOP, alter the owner TaskContract, or silently reduce required outputs.

## Agent product architecture

Every BUSINESS owner exposes the `agent_manifest_ref` declared by `OWNER_REGISTRY.json`:

`Skill/router → Runtime/executor → Workflow/state → Harness/eval → References → Continuity`.

Universal validates structure through `AGENT_ARCHITECTURE_CONTRACT.json` and `runtime/agent_architecture_audit.py`. Static manifests/caches do not certify current runtime quality or external product state.

## Maintenance and learning

Questions, suggestions, analogies, or tentative ideas are candidates, not authority. Do not infer approval; assess independently before acting unless explicitly instructed.

Systemic/non-trivial work follows the controller: parent-system outline before deep diagnosis; failure class/history; recurrence escalation; evidence/alternatives when required; smallest canonical repair; validation; propagation; second-order review; durable checkpoint. `runtime/meta_maintenance.py` verifies closure structure but does not replace during-execution control.

Do not add a permanent supervisory Agent merely to simulate independent review. Prefer deterministic controllers/harnesses and genuinely independent evidence boundaries.

## Progress observability

Checkpoint at verified material safe points; do not wait until the final answer for the first durable write. Pure reads/diagnostics/unchanged state create no heartbeat. Before a final response on an active durable task, persist material change and reread authority.

Exactly one receipt:
- `进度提交：COMMITTED` — material state written + authoritative reread;
- `进度提交：NO_MATERIAL_CHANGE` — durable resume point unchanged;
- `进度提交：COMMIT_FAILED` — intended persistence not verified;
- `进度提交：STALE_WRITER` — writer lease lost.

`COMMITTED` proves durable persistence only; it is not execution, methodology, review, quality or outcome attestation. Truthful OPEN/BLOCKED gates remain checkpointable.

## Performance invariant

Keep Continuity off healthy business hot paths: the global defect preflight is cheap; `NO_DEFECT` loads no maintenance stack or discovery. Continuation bootstrap remains intent-gated. After exact routing, use metadata before content, short checkpoint before deep artifacts, targeted loading, and old history last.

## Authority order

1. compatible authoritative domain runtime/checkpoint;
2. authoritative task/system manifest;
3. current GitHub `main` engineering authority;
4. action-required owner evidence;
5. rebuildable registries/observations/caches;
6. external references unless promoted by owner contract;
7. chat history only as recovery evidence.

Lower authority never overwrites fresher higher-authority truth.
