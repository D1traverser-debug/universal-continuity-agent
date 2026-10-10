# Universal Continuity — System Regression Audit — 2026-10-10

Status: **PASS_WITH_LAZY_OWNER_RECONCILIATIONS_AND_PRODUCT_E2E_PENDING**  
Protocol: **v3.7**  
Engineering authority: `D1traverser-debug/universal-continuity-agent@main`

## Audit scope

This regression reviewed the system as an architecture rather than a set of isolated files:

- top-level blueprint and authority order;
- version lifecycle and cleanup;
- new-chat bootstrap and bare-inherit discovery quorum;
- context recovery and progress observability;
- same-chat protocol reconciliation;
- single-writer lease invariants;
- required owner discovery/conformance surfaces;
- CI regression coverage;
- user-responsibility boundary.

The user is not the migration operator. Internal version selection, owner adaptation, checkpoint migration and stale-writer protection remain system responsibilities.

## 1. Core protocol/version consistency

### Finding
Two core policy surfaces still carried historical protocol labels even though their semantics had already evolved:

- `BARE_INHERIT_DISCOVERY.json` declared Continuity 3.4;
- `CONTEXT_RECOVERY_POLICY.json` declared Continuity 3.6.

`OWNER_REGISTRY.json` also lacked a current-protocol marker and still exposed pre-v3.7 adapter status labels. `NEW_CHAT_BOOTSTRAP.json` had no canonical current-protocol marker.

### Repair
All four surfaces were aligned to v3.7. `tests/test_version_consistency.py` was expanded so future CI verifies the current protocol across the contract, discovery, recovery, progress, owner-adapter, bootstrap, registry, lifecycle and live-chat reconciliation surfaces.

Disposition: **FIXED + REGRESSION-GUARDED**.

## 2. Same-chat old-version reconciliation

### Finding
The system had policy and tests describing in-place reconciliation of an already-open task chat, but the core harness lacked an executable protocol-only reconciliation planner. That left a gap between the documented promise and mechanical execution.

### Repair
Added `runtime/protocol_reconciliation.py` with:

- canonical/legacy protocol-version normalization;
- compatibility classification;
- current-lease/current-epoch validation;
- a protocol-only patch planner;
- an adaptation record;
- a guard that forbids protocol reconciliation from mutating `task_id`, `status`, `current_stage`, `next_action`, `resume_epoch`, `active_lease`, `checkpoint_ref` or `artifact_refs`.

The harness plans the patch; the domain owner still performs CAS/version-guarded persistence and authoritative re-read. Unsupported/unknown old protocols fail closed.

Regression coverage includes supported migration, stale writer rejection, current-version no-op, legacy current-marker canonicalization and unsupported-version fail-closed behavior.

Disposition: **FIXED + EXECUTABLE + REGRESSION-GUARDED**.

## 3. Bare `继承` quorum regression

All five required sources were queried successfully:

1. `GENERIC_HANDOFF` — `GENERIC_TASK_REGISTRY.json`;
2. `FINANCIAL_WRITING_AGENT_RUNTIME` — Financial Writing `continuity/TASK_INDEX.md`;
3. `A_SHARE_MARKET_AGENT` — A-share `continuity/TASK_INDEX.md`;
4. `NOVEL_OS` — Library `/NOVEL_OS_小说系统/99_RECOVERY/TASK_INDEX.json`;
5. `VIDEO_GROWTH_AGENT` — Video Growth `continuity/TASK_INDEX.md`.

Current default USER candidates remain exactly four:

- 金融文章写作;
- A股荐股;
- 《凌晨零点，我接到明天的订单》;
- AI视频涨粉与商业化.

The Universal Continuity maintenance task remains SYSTEM_INFRA + EXPLICIT_ONLY and is correctly excluded from bare discovery.

Disposition: **PASS — 5/5 required sources, 4 default USER candidates**.

## 4. Financial Writing owner conformance

### Finding
`financial-writing:main` still has an active writer lease under a v3.3 task-level marker. Its `HANDOFF.md` is too large and duplicates business rules already owned by the current Skill/reference modules. It also contains stale rule wording, including a 12-item Natural Authorial Prose audit while the current style authority uses the consolidated 9-dimension contract.

### Repair staged without stealing the task lease

Created `D1traverser-debug/financial-writing-agent@main:continuity/HANDOFF_COMPACTION_PLAN.json` and wired it into `continuity/UNIVERSAL_PROTOCOL_ADAPTER.json`.

The plan verifies stronger authorities and requires the current valid task writer (or a genuine new-chat takeover) to:

- compact the handoff to execution truth + exact refs;
- reconcile task protocol metadata to v3.7;
- preserve the existing lease/epoch when it is the same chat;
- re-read manifest/handoff before reporting `COMMITTED`.

The maintenance task intentionally does **not** overwrite another active task's manifest or handoff.

Disposition: **REPAIR STAGED — PENDING VALID WRITER TURN**.

## 5. A-share owner conformance

The long-lived `ashare:recommendation` entry has no active lease and was safely reconciled to v3.7 without replaying market-day business state. Stable cutover/authority refs are present. Historical market-day tasks remain lazy/explicit-only and do not contaminate new trading days.

Disposition: **PASS**.

## 6. NOVEL_OS owner conformance

The Library owner index remains on its domain-era schema/version and correctly exposes the current WAITING story state. Universal protocol adaptation is a routing overlay; maintenance does not rewrite NOVEL_OS canon, publication facts or owner checkpoint merely for protocol hygiene.

Disposition: **PASS WITH LAZY PROTOCOL RECONCILIATION**.

## 7. Video Growth owner conformance

### Finding
The active video checkpoint is executable but oversized: it mixes current state with duplicated H3 failure details, Sample V3 repair rules, reviewer-governance rules and preserved user-requirement prose.

A cross-domain contamination risk was also found: the checkpoint preserved a `TinyFish`-avoidance rule, but no Video Growth rule authority contains that requirement. That preference originated outside the current Video Growth authority surface and must not silently become a durable video rule.

### Repair staged without stealing the task lease

Created `D1traverser-debug/video-growth-agent@main:continuity/CHECKPOINT_COMPACTION_PLAN.json` and wired it into `continuity/OWNER_ADAPTER.json`.

The plan maps duplicated material to stronger authorities:

- H3 diagnostic detail -> `projects/pilot-002/H3_TRANSITION_V1_AUDIT.md`;
- Sample V3 shot/routing detail -> `projects/pilot-002/SAMPLE_V3_SHOT_REPAIR_MATRIX.md`;
- reviewer isolation/receipt rules -> `skills/video-growth-agent/references/agent-studio.md`;
- general production rules -> `skills/video-growth-agent/SKILL.md`.

The TinyFish requirement is marked `DO_NOT_PROMOTE_AS_VIDEO_DURABLE_RULE` unless the valid video writer finds video-specific durable provenance.

Disposition: **REPAIR STAGED — PENDING VALID WRITER TURN**.

## 8. CI/result

GitHub Actions run `38014845513`, job `114102722190`, head `f785db3e0828190f9a8f53422bbe0548760708a2`:

- editable install: PASS;
- package: `universal-continuity-agent==3.7.0`;
- pytest: **66 passed**;
- conclusion: **success**.

This includes the new executable reconciliation tests and expanded core-version consistency checks.

## 9. Remaining non-automatable acceptance boundary

One product-level boundary cannot be proven by repository CI: a genuinely fresh ChatGPT conversation must receive the account-level startup instruction and invoke the system from the user command.

Low-risk acceptance sequence:

1. ensure the account-level Personalization/Custom Instructions contains the current Continuity startup/backstop rule;
2. open a genuinely new chat and send exactly `继承` — expected: complete 5-source discovery and the four default USER candidates, without taking over any task yet;
3. for the full takeover receipt test without disturbing a business chat, explicitly resume `跨对话继承系统建设与维护` in that fresh chat. Because this is the dedicated EXPLICIT_ONLY infrastructure task, it is the safest task for validating `继承前进度 -> compatibility -> takeover -> 进度提交`.

Do not select Financial Writing, Video Growth or NOVEL_OS merely as a test if the user wants their existing task chat to remain the active writer; a genuine new-chat takeover would correctly retire the prior writer.

## Overall conclusion

The v3.7 architecture is internally coherent after this regression. The most important defect found was not cosmetic: old-chat protocol reconciliation existed as a policy promise without a dedicated executable planner. That gap is now closed and tested.

Remaining work is intentionally event-driven rather than maintenance-force-written:

- Financial Writing handoff compaction + task-level v3.7 reconcile on its next valid writer turn;
- Video Growth checkpoint compaction + task-level v3.7 reconcile on its next valid writer turn;
- NOVEL_OS protocol metadata reconcile on the next legal owner/task write;
- one fresh-chat product-level acceptance test by the user after the account instruction is present.
