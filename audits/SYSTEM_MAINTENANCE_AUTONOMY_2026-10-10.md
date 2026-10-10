# System Maintenance Autonomy Audit — 2026-10-10

Status: ACCEPTED_AND_CI_PASS
Scope: Universal Continuity + sibling cross-agent execution control plane

## Problem

During execution-propagation hardening, a user had to explicitly point out that writing rules into GitHub did not itself guarantee already-open chats would read them. The system then fixed propagation wiring, but the interaction exposed a broader maintenance defect: the active maintenance writer was still behaving too reactively and could stop after the immediate requested change instead of automatically closing adjacent system-maintenance work.

The user should not need to enumerate internal upgrade, migration, regression, recordkeeping, propagation, or maintenance follow-ups one by one.

## Root cause

Existing policies assigned protocol evolution, compatibility, learning, version hygiene and owner adaptation to Universal Continuity, but there was no single machine-readable maintenance contract that made the complete repair loop mandatory when the assistant itself detected a system-level defect.

This left an ambiguity between:

- proactive learning / auditing; and
- proactive repair / validation / durable maintenance recordkeeping.

A second pre-existing drift was exposed by CI during this change: `tests/test_startup_hook.py` required the exact fail-closed marker `CONTINUITY_BOOTSTRAP_UNAVAILABLE`, while the current `STARTUP_HOOK.md` had weakened this into a generic resource-unavailable explanation.

## Changes

1. Added `SYSTEM_MAINTENANCE_POLICY.json` as the machine-readable authority for autonomous system-maintenance closure.
2. Added explicit triggers for assistant-detected gaps, user reports revealing systemic gaps, CI failures, owner/capability drift, authority inconsistencies, duplicate mechanisms and execution/propagation gaps.
3. Required the default maintenance loop:
   `DETECT -> CLASSIFY_SCOPE_AND_AUTHORITY -> READ_CURRENT_AUTHORITY -> DIAGNOSE_ROOT_CAUSE -> PATCH_MINIMUM_AUTHORITY_SURFACE -> ADD_OR_UPDATE_GUARD -> RUN_OR_OBSERVE_VALIDATION -> UPDATE_CHANGE_RECORD_AND_TASK_STATE -> REREAD_AUTHORITATIVE_STATE -> REPORT_EXACT_RESULT_AND_REMAINING_BOUNDARY`.
4. Defined user-interruption boundaries: external account/UI action, new permission/credential, irreversible high-impact choice, unrecoverable missing fact, or product/legal boundary.
5. Required durable maintenance records for material changes, including problem, root cause, changed authority surfaces, validation, behavioral effect, remaining risk, current stage and next action.
6. Updated `SYSTEM_BLUEPRINT.md` so the user is explicitly not the system maintenance operator and added a dedicated system-maintenance architecture layer/invariant.
7. Updated `CONTINUOUS_LEARNING_POLICY.md` so learning or self-detected gaps feed the autonomous repair loop and do not stop at diagnosis.
8. Added `tests/test_system_maintenance_policy.py` to guard the autonomy, owner-boundary and recordkeeping invariants.
9. Restored `CONTINUITY_BOOTSTRAP_UNAVAILABLE` in `STARTUP_HOOK.md` and wired the maintenance policy into the account/startup semantics instead of weakening the existing startup regression test.

## Validation

Initial run:
- GitHub Actions run: `38018174945`
- Head: `44a1dee788a03ca0aa4c261f9f9f31a40cb55151`
- Result: FAIL
- Test result: `1 failed, 80 passed`
- Failure: pre-existing `STARTUP_HOOK.md` drift; exact `CONTINUITY_BOOTSTRAP_UNAVAILABLE` marker was missing.

Repair run:
- GitHub Actions run: `38018225600`
- Job: `114113204158`
- Validated head: `afa7bac8ad0cbe3b02a35955cb60f28dd3f2d6ee`
- Package: `universal-continuity-agent 3.7.0`
- Result: PASS
- Test result: `81 passed in 0.19s`

The old startup test was not weakened. The authority document was repaired to satisfy the existing fail-closed contract.

## Behavioral effect

For future Universal Continuity / cross-agent control-plane maintenance:

- detecting a systemic defect is itself a maintenance trigger;
- the assistant should complete related internal diagnosis, patching, guards, validation, durable records and status updates without requiring the user to enumerate each operation;
- user involvement is reserved for precise external boundaries;
- the maintenance task still may not steal another owner lease or rewrite domain business truth;
- compatible hardening remains protocol v3.7 and does not justify a gratuitous version bump.

## Remaining boundaries

This policy cannot create product-level capabilities that are absent. Account/UI changes, credentials, third-party permissions and genuinely independent executor infrastructure can still require external action or remain blocked.

Owner-level runtime handshakes and fresh-chat product E2E remain separate pending acceptance work. The new maintenance policy changes who owns the maintenance loop; it does not fabricate those external proofs.
