# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `89`
- current controller run: `human-readable-durable-revision-v68-2026-10-13`
- controller status: `ACTIVE` revision `16` at `M8_MULTI_LAYER_VALIDATION`

## Human Durable Revision

Universal pilot format remains:

`UC-YYYYMMDD-rN`

This is a user-facing durable-state revision label, not a replacement for Git, SVN, protocol or business versions.

- `Git SHA` = exact immutable engineering identity.
- `protocol 3.7` = compatibility semantics.
- `manifest_version` = monotonic durable task/CAS state sequence.
- controller revision = one maintenance run's internal trace.
- `UC-YYYYMMDD-rN` = derived presentation for the user.

`YYYYMMDD` comes from the authoritative persisted timestamp's encoded calendar date. `rN` reuses the existing monotonic durable version. The sequence does **not** reset daily. Date is context; `rN` is ordering within this revision scope.

## Why not SVN-style global r1234 or R20261013.001

SVN can expose a repository-wide increasing integer because its repository commit model is centralized. These agents live in separate Git repositories and durable owner/task streams. A shared daily/global counter would add a mutable authority, reset/timezone policy, locks, cross-repo contention and failure recovery.

Therefore there is no central revision counter, no `revision registry`, no Git-history scan and no tag for every checkpoint. Git tags remain optional stable-milestone/release markers only.

## Second-order correction

Corrective M8 `38363967497 / 115184549077` passed after the first two regressions were fixed. Before propagation/closure, second-order review found a new boundary problem in our own v68 state:

1. `TASK_MANIFEST.json` carried `human_revision_latest_expected`, which contradicted the core rule that the label is derived, not a second stored truth. It has been removed.
2. Future owner adoption rules were not strict enough: owner/task streams may have independent counters, gaps caused by internal durable checkpoints, and some owners may not have a suitable monotonic sequence for the intended scope. Policy now says:
   - numbers are scope-local, not globally comparable;
   - skipped r values are valid and never backfilled/reused;
   - an owner must already have a suitable monotonic durable version for the intended identity lifetime;
   - if it does not, omit the human revision and fix owner versioning separately—never invent a display-only counter;
   - the scope code must identify the actual revision stream closely enough to avoid ambiguity.
3. The core `TaskMetadata`/receipt state schemas are **not** expanded with a stored human revision field. The label is assembled at the user-facing receipt presentation boundary from already-loaded authoritative metadata. This avoids contaminating persistence/state schemas for a display concern.

This is exactly the anti-bloat decision: one small formatter, existing policy surfaces, focused tests, zero new startup preload, zero new remote read, zero new authority/counter.

## Validation history

- first M8 `38363727516 / 115183763873`: control-plane PASS, architecture PASS, pytest `317 passed / 2 failed`; real reopen.
- second M8 `38363967497 / 115184549077`: all steps PASS, then second-order review deliberately reopened because of the duplicate-label/adoption-boundary issue above.
- current step: re-run M8 against policy schemas 1.2 and the no-stored-label regression.

## Cross-owner boundary

This is **not maintenance-only** conceptually; it is a generic durable progress-receipt presentation convention. But the user's instruction was to use it in Universal first. Financial / A-share / Novel / Video were inspected only to assess future propagation. No BUSINESS lease or state was changed.

Future adoption must be owner-local and explicit: map an existing monotonic durable version + a stable revision-stream scope code. Do not assume every owner currently has identical version semantics.

## v65 direct-main / PR-first regression anchor

当前模型不是 PR-first。

Universal material compliant writes continue to use active lease + observed-HEAD CAS + CI + authoritative reread. PR-first and branch protection are not default requirements under the current `SINGLE_ACTIVE_CHAT` threat model; unprotected `main` alone is not a HIGH defect.

The experimental branch `continuity/pr-first-mutation-gate-v65` is unmerged and non-authoritative.

## Next

Re-run M8. If green: M9 records propagation analysis only, M10 rechecks hidden failure modes (same-day, date change, gap, rollback, failure/stale/no-change, scope collision, missing owner sequence, timestamp anomaly, branch/scratch, tags, protocol/Git namespace confusion, performance), then M11 closure and post-closure CI/reread.
