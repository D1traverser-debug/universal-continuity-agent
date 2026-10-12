# Universal Continuity — Entry Point

Status: ACTIVE  
Contract: v3.7  
Engineering authority: this repository `main`

## Kernel boundary

Chat is ephemeral; the durable object is the task. GitHub/Library are storage/discovery surfaces, not automatic event listeners.

Universal owns cross-owner control-plane invariants; domain owners retain business rules, state, evidence and artifacts.

If required Continuity resources cannot be accessed, fail closed with `CONTINUITY_BOOTSTRAP_UNAVAILABLE`; never reconstruct execution truth from Memory or old chat.

## Minimal bootstrap invariant

Do **not** preload the repository.

Every Continuity bootstrap begins with only:

1. `ENTRYPOINT.md`;
2. `CURRENT_PROTOCOL.json`.

Everything else is event-driven; blueprints, audits, methodology details, owner repositories and old transcripts are cold path.

## Lightweight ingress triage

Before a material response or material action under this control plane, do a **cheap defect-signal preflight**, not a full maintenance sweep. Its only job is routing:

- `NO_DEFECT` — no plausible system/control-plane defect signal; continue the normal owner/business route without loading the maintenance stack.
- `INVESTIGATE` — a plausible defect, contradiction, regression, repeated correction, missing output/gate, stale state, routing/tool anomaly, or completion-evidence mismatch exists but is not yet proved; load the exact evidence needed and do not mutate the suspected authority while the defect remains unconfirmed.
- `CONFIRMED_DEFECT` — evidence establishes a material defect; enter the current `SYSTEM_MAINTENANCE_POLICY.json` path in the same turn.

A user does not need to use the word “bug”. A material correction, a comparison showing “last time X / this time Y”, a claim that the system skipped its own path, a CI/state/output contradiction, or an assistant-detected anomaly can all be defect signals. Ordinary healthy business input must stay cheap and must not trigger the full maintenance loop.

Once `INVESTIGATE` or `CONFIRMED_DEFECT` enters systemic/non-trivial maintenance, use `runtime/maintenance_controller.py` as the deterministic stage controller over the stage list owned by `SYSTEM_MAINTENANCE_POLICY.json`. The controller is not a second authority. It enforces execution order and action boundaries:

- the parent-system outline and prerequisite stages cannot be skipped;
- `INVESTIGATE` cannot authorize a material patch until evidence resolves it to `CONFIRMED_DEFECT`;
- material authority mutation is forbidden before the canonical `M7_IMPLEMENTATION...` stage;
- validation, propagation and second-order review actions are authorized only at their corresponding stages;
- a validation/second-order discovery may reopen an earlier stage, which invalidates all downstream stage receipts;
- blocked work preserves the exact stage and blocker evidence;
- closure is illegal until every canonical maintenance stage is completed.

The post-hoc Meta-Governance Harness still validates the closure record, but it is no longer the only process control: the controller governs what may happen **during** the maintenance trajectory.

## Intent routing

`学习继承，任务不继承` applies to **NEW_TASK**. Explicit `继承 / 继续 / 恢复 / 接着上次` intent is `CONTINUE` first.

- **Bare CONTINUE** → load `BARE_INHERIT_DISCOVERY.json`, derive the current source quorum from `OWNER_REGISTRY.json`, complete every required source, then present eligible USER tasks. Never reuse a historical owner count.
- **Named CONTINUE** → route directly to the exact owner/task manifest + short checkpoint. Skip global discovery unless ambiguous.
- **SYSTEM_INFRA** → never appears in bare candidates; it resumes only after explicit selection when eligible.
- **NEW_TASK** → route to the matching owner without inheriting unfinished task state.

`OWNER_REGISTRY.json` is the **sole control-plane owner-membership authority**. Parallel copied owner-name allowlists are forbidden.

## Continuation invariant

For a selected durable task:

1. read authoritative manifest + short checkpoint;
2. show **继承前进度** before takeover mutation;
3. reconcile protocol only when required;
4. acquire/verify the writer lease with owner/CAS protection;
5. load only artifacts/capabilities required by the real `next_action`;
6. continue from authoritative `current_stage / next_action`.

A real takeover increments `resume_epoch` and supersedes the old lease. Same-writer control-plane refresh preserves both. Partial discovery is `INCOMPLETE_DISCOVERY` and never auto-resumes.

Bare candidates are USER tasks with `resume_eligible=true`, `resume_visibility=DEFAULT`, and non-terminal resumable status. Hidden/system/test/eval/migration tasks are excluded.

## Event-driven authority loading

Load only when the event occurs:

- **Owner admission/topology** → `OWNER_REGISTRY.json`, `AGENT_ARCHITECTURE_CONTRACT.json`, and only derived adaptation/execution/architecture conformance surfaces needed now.
- **Protocol mismatch** → `VERSION_LIFECYCLE_POLICY.json` + `LIVE_CHAT_RECONCILIATION_POLICY.json`.
- **Recovery gap** → `CONTEXT_RECOVERY_POLICY.json`, then exact artifact refs, then selective history only if needed.
- **Material owner execution** → exact owner Skill/entrypoint + `continuity/EXECUTION_CAPABILITIES.json` + `EXECUTION_READINESS_CONTRACT.json`; handshake only the exact next-action capabilities.
- **Execution/methodology proof used for a gate** → `OWNER_ADAPTER_CONTRACT.json`, `runtime/execution_receipt.py`, `runtime/methodology_conformance.py`; apply the current receipt/action-binding contract there rather than copying it into this bootstrap.
- **Artifact/file/storage** → `artifact_io@1.0`; load `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` only when activated.
- **Plausible system-defect hypothesis** → `SYSTEM_MAINTENANCE_POLICY.json` + `runtime/maintenance_controller.py`; triage before discussion as `NO_DEFECT`, `INVESTIGATE`, or `CONFIRMED_DEFECT`. Confirmed defects enter maintenance/evolution in the same turn; never close them as an unowned “future risk”.
- **Maintenance/repeated failure/drift/material user correction** → `operational_hygiene@1.0` + `SYSTEM_MAINTENANCE_POLICY.json` + `runtime/maintenance_controller.py`.
- **Durable learning/evolution** → `evolution@1.0` + `CONTINUOUS_LEARNING_POLICY.md`.
- **Media evidence/distillation** → `MEDIA_DISTILLATION_PROTOCOL.md`.
- **Architecture/control-plane review** → `AGENT_ARCHITECTURE_CONTRACT.json` + `SYSTEM_BLUEPRINT.md` + implicated contracts only.

Methodology profiles are conditional contracts loaded only on activation. Owners pin exact versions; Floating `latest` is forbidden.

## Owner execution boundary

Repository declarations are capability ceilings, not current execution proof.

Before a material owner action:

1. refresh the exact owner Skill and execution capability manifest;
2. observe only capabilities needed now;
3. evaluate execution readiness and applicable methodology using current contracts;
4. use only an allowed owner-native / deterministic / CHAT_BRIDGED / attested route at its real assurance level;
5. validate any receipt against exact task/stage/action/subject/input before using it as proof;
6. block only the exact unavailable hard gate.

Operational methodology proof uses `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance`; declaration conformance, owner regression or CI must not substitute for current-action operational proof. `DECLARED_ONLY` is not execution; proof for another action is not proof for this action.

## Agent product architecture

Every BUSINESS owner exposes the `agent_manifest_ref` declared by `OWNER_REGISTRY.json`:

`Skill/router → Runtime/executor → Workflow/state → Harness/eval → References → Continuity`.

Universal validates this through `AGENT_ARCHITECTURE_CONTRACT.json` and `runtime/agent_architecture_audit.py`. Large Skills/bootstrap surfaces are architecture drift. A static manifest cannot certify freshness.

## Maintenance and learning

User goals/corrections are high-value signals, not automatic implementation commands. For systemic/non-trivial maintenance, follow `SYSTEM_MAINTENANCE_POLICY.json` through `runtime/maintenance_controller.py`: build the parent-system impact outline before deep diagnosis, classify the failure, search historical same-class repairs, escalate abstraction on recurrence, learn/compare when required, test counterexamples, review instruction/propagation/complexity impact, implement only after the controller reaches the implementation stage, validate, reopen/invalidate downstream work when new evidence requires it, attack the accepted fix again, and persist.

Do not create another permanent Agent merely to simulate independent review. Deterministic controllers/harnesses, distinct execution identities and real graders keep separate assurance boundaries.

## Progress observability

Work must checkpoint **during the turn** at verified material safe points; do not intentionally wait until the final answer for the first durable write. Pure reads, transient diagnostics and unchanged state do not create heartbeat writes. Resume from the latest verified safe checkpoint.

Every final response on an active durable task emits exactly one:

- `进度提交：COMMITTED` — material state was written and authoritative state reread;
- `进度提交：NO_MATERIAL_CHANGE` — durable resume point unchanged;
- `进度提交：COMMIT_FAILED` — intended persistence failed or could not be verified;
- `进度提交：STALE_WRITER` — this chat lost its lease.

`COMMITTED` is a **durable-persistence receipt**. It means durable persistence only. It is not an execution, methodology, review, quality or outcome attestation. A truthful OPEN/BLOCKED gate must itself be checkpointable; missing gate evidence does not forbid persisting that blocker. Report assurance/gate state separately from commit status.

## Performance invariant

Keep Continuity off the steady-state business hot path: metadata before content, short checkpoint before deep artifacts, targeted capability/profile loading, no global discovery for exact routing, old history last, and no heartbeat write when nothing material changed.

## Authority order

1. compatible authoritative domain runtime/checkpoint;
2. authoritative task/system manifest;
3. current GitHub `main` engineering authority, including `OWNER_REGISTRY.json` for membership;
4. owner-referenced evidence required by the current action;
5. rebuildable registries/observations/caches;
6. external references unless explicitly promoted by owner contract;
7. chat history only as recovery evidence.

A lower authority cannot overwrite fresher higher-authority truth.