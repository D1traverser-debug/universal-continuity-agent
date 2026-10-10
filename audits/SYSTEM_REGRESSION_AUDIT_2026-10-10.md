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

All five required owner sources were queried successfully. The authoritative default USER candidate count is **4**. Specific live task labels and live owner state are intentionally not copied into this public harness audit; they remain in their owner/discovery authorities.

The Universal Continuity maintenance task remains SYSTEM_INFRA + EXPLICIT_ONLY and is correctly excluded from bare discovery.

Disposition: **PASS — 5/5 required sources, 4 default USER candidates**.

## 4. Financial Writing owner conformance

### Finding
The active Financial Writing recovery handoff duplicates business rules already owned by the current Skill/reference modules and contains stale protocol/rubric wording.

### Repair staged without stealing the task lease

Created the Financial Writing owner-side handoff compaction plan and wired it into its Universal protocol adapter.

The plan verifies stronger authorities and requires the current valid task writer (or a genuine new-chat takeover) to:

- compact the handoff to execution truth + exact refs;
- reconcile task protocol metadata to v3.7;
- preserve the existing lease/epoch when it is the same chat;
- re-read manifest/handoff before reporting `COMMITTED`.

The maintenance task intentionally does **not** overwrite another active task's manifest or handoff.

Disposition: **REPAIR STAGED — PENDING VALID WRITER TURN**.

## 5. A-share owner conformance

The long-lived recommendation entry had no active writer lease and was safely reconciled to v3.7 without replaying market-day business state. Stable cutover/authority refs are present. Historical market-day tasks remain lazy/explicit-only and do not contaminate new trading days.

Disposition: **PASS**.

## 6. NOVEL_OS owner conformance

The Library owner index is available and structurally sufficient for routing/recovery. Universal protocol adaptation remains a routing overlay; maintenance does not copy or rewrite live novel canon, publication facts or owner checkpoint merely for protocol hygiene.

Disposition: **PASS WITH LAZY PROTOCOL RECONCILIATION**.

## 7. Video Growth owner conformance

### Finding
The active video checkpoint is executable but oversized: it mixes current execution state with duplicated project audit detail, repair-contract detail, reviewer-governance rules and preserved user-requirement prose.

A cross-domain contamination risk was also detected: one preserved tool-routing preference has no matching Video Growth durable rule authority. The user-specific prose is not repeated in this public audit and must not silently become a durable Video Growth rule.

### Repair staged without stealing the task lease

Created the Video Growth owner-side checkpoint compaction plan and wired it into its owner adapter.

The plan maps duplicated material to stronger project/Skill authorities, keeps only execution-critical state in the checkpoint, and requires any unverified cross-domain preference to be removed or reclassified unless video-specific durable provenance exists.

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
2. open a genuinely new chat and send exactly `继承` — expected: complete 5-source discovery and four default USER candidates, without taking over any task yet;
3. for the full takeover receipt test without disturbing a business chat, explicitly resume the dedicated Continuity maintenance task in that fresh chat. Because this is an EXPLICIT_ONLY infrastructure task, it is the safest task for validating `继承前进度 -> compatibility -> takeover -> 进度提交`.

Do not select a live business task merely as a test if its existing chat should remain the active writer; a genuine new-chat takeover would correctly retire the prior writer.

## Overall conclusion

The v3.7 architecture is internally coherent after this regression. The most important defect found was not cosmetic: old-chat protocol reconciliation existed as a policy promise without a dedicated executable planner. That gap is now closed and tested.

Remaining work is intentionally event-driven rather than maintenance-force-written:

- owner handoff/checkpoint compaction and task-level v3.7 reconciliation on each valid writer's next durable turn where staged;
- one fresh-chat product-level acceptance test by the user after the account instruction is present.
