# Universal Continuity Global System Audit — 2026-10-10

## Trigger

The user asked for a global review of the control system, including risks that are easy to enumerate and risks that are not known in advance. The user also explicitly corrected the maintenance process not to treat the user's suggested mechanism (for example, “check every project every time”) as architecture authority.

This audit therefore separated the goal from the proposed mechanism:

- Goal: maximize the probability of detecting real continuity/control-plane failures before they reach business execution.
- Candidate A: run every project/business pipeline on every audit.
- Candidate B: risk-tiered audit with always-on kernel checks, change-impact checks, owner metadata sentinels, event-triggered full control-plane sweeps, and synthetic negative/fault scenarios.

Candidate A was rejected as the default because it is expensive, can require live market/model/provider capabilities, can create false failures, can create unnecessary owner interactions, and risks turning the continuity control plane into a giant business orchestrator. Candidate B was adopted because it preserves failure containment while escalating verification depth when uncertainty or blast radius is actually high.

## Practical external evidence reviewed

The design was checked against practical reliability guidance rather than copied from framework descriptions:

- Google SRE, *Testing for Reliability*: testing reduces uncertainty; verification depth should follow reliability risk, and staged/canary validation complements pre-production tests.
- Google SRE, *Embracing Risk*: reliability effort must balance risk reduction against excessive operational cost and lost velocity.
- Google SRE launch/canary guidance: staged exposure, health verification and rollback boundaries reduce blast radius.
- AWS Fault Injection Service guidance: fault experiments should begin with a hypothesis, use controlled/non-production scope where possible, and define stop conditions/guardrails before disruptive experiments.
- Microsoft safe deployment guidance: health signals and stop/rollback behavior matter more than merely completing a deployment step.

These sources were treated as candidate evidence, not system authority. The accepted architecture was determined by current repository/owner constraints and regression evidence.

## Accepted audit model

The semantic owner is `SYSTEM_MAINTENANCE_POLICY.json`; no parallel `GLOBAL_AUDIT_POLICY.json` or `SYSTEM_AUDIT_POLICY.json` was created.

### 1. CORE_ALWAYS

Runs on every control-plane CI and material maintenance closure:

- protocol/version alignment;
- local authority-reference reachability;
- owner-set consistency across registries;
- maintenance manifest/cache alignment;
- product-E2E status alignment;
- owner protocol-registry state consistency.

Implemented by `runtime/system_audit.py` and invoked before pytest in `.github/workflows/ci.yml`.

### 2. IMPACT_SCOPED

Runs for every material change against the changed authority surface, direct dependents, affected runtime/tests, and owner adapter/capability pointers.

### 3. OWNER_SENTINEL_ROTATION

Reads owner metadata/index/manifest/adapter/capability surfaces when extra cross-owner confidence is useful, but does not execute owner business workflows or steal leases.

### 4. FULL_CONTROL_PLANE

Triggered by explicit global audit, protocol/authority/startup/storage/methodology/execution-contract changes, cross-owner migration, systemic reliability incidents, or major release boundaries.

It may inspect all control-plane authorities and all durable-owner metadata surfaces, but business truth remains owner-local.

### 5. SYNTHETIC_FAULT_INJECTION

Used for explicit global audits and high-risk reliability boundaries. Production mutation is not allowed by default. The initial scenario inventory includes:

- required discovery source unavailable;
- stale registry attempting to override owner authority;
- same-chat refresh changing lease/resume_epoch;
- genuine new-chat takeover failing to change writer lease;
- floating methodology profile version;
- missing methodology hook;
- forbidden kernel-invariant override;
- `COMMITTED` without authoritative reread;
- destructive mutation with unknown identity/dependency;
- external reference promoted to authority merely by presence;
- declared executor treated as current-session execution proof.

Unknown-unknown coverage is therefore pursued with contradiction scans, independent evidence, dangling-reference detection, negative fixtures and boundary failures rather than an unbounded checklist.

## Concrete defects found by this audit

### A. Stale owner protocol adaptation registry

`OWNER_PROTOCOL_ADAPTATION_REGISTRY.json` still reported:

- Financial Writing as observed protocol 3.3 / pending valid-writer reconciliation;
- Video Growth as observed protocol 3.5 / pending valid-writer reconciliation.

Fresh owner authority showed both active entries already reconciled to Continuity 3.7.

Fix: registry schema 1.2 now records historical source protocol separately from current observed protocol and marks current entries compatible.

### B. Dangling Financial conformance reference

The migration registry pointed to:

`financial-writing-agent@main:continuity/HANDOFF_COMPACTION_PLAN.json`

That file does not exist. The current authoritative compact handoff is:

`continuity/tasks/financial-writing-main/HANDOFF.md`

Fix: the dangling reference was replaced with the live handoff reference.

### C. Stale owner-registry reconciliation statuses

`OWNER_REGISTRY.json` still described Financial and Video as lazy/pending reconciliation after their current owner state had reached 3.7.

Fix: status-only refresh to current reconciliation state. An attempted schema bump from 3.0 to 3.1 was rejected by regression because no structural schema change occurred; schema remained 3.0.

### D. README bootstrap/authority drift

README still instructed:

`ENTRYPOINT.md -> PROTOCOL.md`

and described ChatGPT Library as retaining a thin bootstrap pointer. This contradicted the already product-tested minimal bootstrap and current external-store authority model.

Fix: README now states the hot bootstrap as:

`ENTRYPOINT.md + CURRENT_PROTOCOL.json`

and treats `PROTOCOL.md` as a human-readable reference rather than mandatory hot-path input. Library/Notion/Drive are not implicit control-plane authority.

### E. System-maintenance policy/version drift

After adding risk-tiered audit semantics to `SYSTEM_MAINTENANCE_POLICY.json` v1.5, the maintenance task manifest still declared policy v1.4.

The new CI audit preflight failed before pytest with:

`maintenance TASK_MANIFEST system_maintenance_policy_version is stale`

Fix: maintenance manifest was advanced and cache synchronized. The audit was not weakened.

### F. Circular cache validation exposed by a negative fixture

A synthetic test changed both the Video protocol adaptation registry and owner registry back to stale values. The first local audit implementation incorrectly passed because two derived/cache surfaces agreed with each other.

Fix: local audit now uses already-verified existing-chat product E2E evidence as an independent witness for the Video 3.7 reconciliation. Two stale caches can no longer mutually certify each other.

This was an important design correction: cross-surface consistency must use at least one stronger/independent evidence source where available, not only compare peer caches.

## Regression evidence

### Intermediate failure 1 — useful audit catch

Run `38039484874`, job `114176702308`, head `00781136f9d729efbd07b0171d09ae90ddb7be10`:

- system-audit preflight failed before pytest;
- exact defect: maintenance manifest still declared system-maintenance policy 1.4 after policy moved to 1.5.

The check was preserved and the state was repaired.

### Intermediate failure 2 — useful counterevidence

Run `38039596056`, job `114177014133`, head `cb503dc17133ee6a8c01fd7c7ca03034ce2b934c`:

- audit preflight passed;
- pytest failed 2 tests;
- one failure showed an unnecessary OWNER_REGISTRY schema bump;
- one failure showed the local audit could be fooled when two stale cache surfaces agreed.

The tests were preserved. Schema bump was reverted and the audit gained an independent product-evidence cross-check.

### Current behavioral validation

Run `38039769573`, job `114177507423`, head `fc6de3b4d43b81b68a3df43974fd7c3ba4019204`:

- `python -m runtime.system_audit --repo-root . --trigger routine_change` = PASS;
- pytest = `110 passed in 0.18s`.

A final current-main CI is still required after this audit/status/handoff closure metadata is committed before the maintenance turn may report `COMMITTED`.

## Full owner metadata sweep performed

This explicit global audit read current metadata/authority pointers for all four durable business owners without executing their business pipelines or stealing leases.

### Financial Writing

Verified current:

- active task manifest at Continuity 3.7;
- compact task handoff at 3.7;
- `continuity/UNIVERSAL_PROTOCOL_ADAPTER.json`;
- `continuity/EXECUTION_CAPABILITIES.json`.

The old `HANDOFF_COMPACTION_PLAN.json` reference was confirmed missing and repaired centrally.

### A-share

Verified current:

- recommendation entry manifest at Continuity 3.7;
- task index;
- Universal protocol adapter;
- execution capabilities.

No market-day business execution was run. Live market data/runtime readiness still requires a current-session handshake when a material market action occurs.

### Novel Writing

Verified current:

- active project manifest at Continuity 3.7;
- task index;
- Universal protocol adapter;
- artifact-context governance surface;
- execution capabilities.

No novel business state was mutated.

### Video Growth

Verified current:

- active task canonical Continuity protocol 3.7, with legacy 3.5 marker retained only for compatibility;
- owner adapter;
- execution capabilities;
- checkpoint compaction plan;
- current methodology binding `artifact_io@1.0 + operational_hygiene@1.0`, `overrides={}`.

Checkpoint compaction remains deferred to valid owner scope. Central methodology conformance is still pending and must not be reported complete.

## Synthetic-fault coverage assessment

Not every scenario has the same enforcement layer. This is intentional and is recorded so the system does not confuse a policy assertion with runtime proof.

### Executable negative/runtime evidence already present

- same-chat migration preserves lease/business state;
- stale writer cannot apply protocol patch;
- unsupported protocol fails closed;
- floating methodology profile fails;
- missing methodology hook fails;
- forbidden kernel override fails;
- `COMMITTED` without verified reread becomes `COMMIT_FAILED`;
- stale writer becomes `STALE_WRITER`;
- repository wiring without session handshake is blocked;
- declared-only execution cannot masquerade as executable;
- isolated review cannot be simulated by same-chat roleplay;
- stale cross-registry protocol state is now caught by synthetic fixture plus independent product evidence.

### Contract/owner-boundary guards rather than central business-operation execution

- a required discovery source failure is fail-closed by the discovery contract/product hook, but Universal does not own external source availability itself;
- destructive file mutation identity/dependency enforcement is a shared `artifact_io` invariant, while the concrete file operation remains owner/provider-specific;
- external-store authority promotion is prohibited centrally, while concrete provider/store use remains owner-specific.

These boundaries must be tested in the relevant owner rollout rather than by making Universal execute every business/storage path.

## Architecture decision

The durable decision is:

**Do not run every project/business pipeline on every global-control check.**

Use:

`CORE_ALWAYS -> IMPACT_SCOPED -> OWNER_SENTINEL_ROTATION -> FULL_CONTROL_PLANE when triggered -> SYNTHETIC_FAULT_INJECTION when risk justifies it`

This keeps routine checks cheap enough to run continuously in CI while preserving a deterministic escalation path for large blast-radius changes and systemic incidents.

## Remaining boundaries / next work

1. Video Growth central `runtime/methodology_conformance.py` execution remains pending.
2. Financial Writing, A-share and Novel methodology profile bindings remain pending valid owner turns.
3. Artifact-operation invariants need owner-local runtime/eval evidence during owner profile rollout; Universal should not centralize the actual business file operations.
4. No scheduler/event-watch infrastructure exists, so no claim is made that this audit runs offline after the chat closes.
5. A final current-main CI after audit/status/handoff closure is required before this maintenance turn can be marked committed.
