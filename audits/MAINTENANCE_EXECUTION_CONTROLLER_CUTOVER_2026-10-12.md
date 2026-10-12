# Maintenance Execution Controller Cutover — 2026-10-12

Status: `REGRESSION_VERIFIED__CONTROLLER_NATIVE_LIVE_TRAJECTORY_OPEN`

## Trigger

The user challenged a remaining systemic gap after the V61 failure-class/abstraction work: if a defect has already entered maintenance, why can required steps still be skipped? Historical recall alone is reactive and does not explain execution-path omission.

## Failure class

Primary: `declarative-SOP-without-execution-control`.

Related:
- `posthoc-compliance-record-can-hide-out-of-order-execution`;
- `reliability-hardening-can-bloat-hot-path-router`;
- `tests-that-pin-wording-instead-of-semantics`.

The previous design had a strong maintenance policy and a post-hoc `runtime/meta_maintenance.py` structural verifier, but no deterministic runtime that owned current maintenance stage and action authorization while the work was happening. A model could therefore patch first and reconstruct a structurally complete outline/history record later.

## Parent-system repair

No new Agent, root policy, registry, or failure database was added.

1. Added `runtime/maintenance_controller.py`.
   - canonical stage order is read from `SYSTEM_MAINTENANCE_POLICY.json`; the controller does not own a second stage list;
   - completed receipts must be the exact canonical prefix;
   - `INVESTIGATE` cannot authorize material mutation;
   - `MATERIAL_PATCH` is authorized only for `CONFIRMED_DEFECT` at canonical `M7_IMPLEMENTATION...`;
   - validation/propagation/second-order review are authorized only at their matching stages;
   - reopening an earlier stage truncates downstream receipts;
   - BLOCKED preserves exact stage + evidence;
   - CLOSE is forbidden until all canonical stages complete.
2. Added deterministic controller regressions in `tests/test_maintenance_controller.py`.
3. Wired the controller into `AGENT_MANIFEST.json` as runtime entrypoint and workflow transition guard.
4. Added lightweight three-state ingress to `ENTRYPOINT.md` and canonical `STARTUP_HOOK.md`: `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`.
5. Updated `SYSTEM_BLUEPRINT.md` to separate the during-execution controller from the post-hoc closure verifier.
6. Added `tests/test_unified_ingress_and_controller.py` for routing/wiring boundaries.

## Complexity / hot-path result

The first controller wiring attempt over-expanded the startup prose and CI rejected it. The fix was deletion/compaction, not a budget increase.

Current verified tree at `b3c099ade696f8dbf67998cefa30ecf364f8998e`:
- `ENTRYPOINT.md`: 8,013 bytes / 8,192 target;
- `CURRENT_PROTOCOL.json`: 454 bytes;
- minimal repository bootstrap total: 8,467 bytes / 9,216 budget;
- `STARTUP_HOOK.md`: 3,464 bytes / 4,096 budget.

Detailed SOP remains cold-path in policy/runtime. The hot path retains only trigger/routing and hard boundaries.

## Real regression evidence

GitHub Actions run `38268950814`, job `114878120772`, HEAD `b3c099ade696f8dbf67998cefa30ecf364f8998e`:
- risk-tiered control-plane audit: `PASS`;
- synthetic fault injection selected by the high-risk ENTRYPOINT change: `PASS`, including recurrence-at-same-or-lower-abstraction rejection;
- Agent architecture harness: `PASS` with only previously acknowledged owner drift warnings;
- pytest: `298 passed`.

Earlier iterations were intentionally not treated as success:
- oversized ingress caused hot-path budget failures;
- later compaction removed established progress/takeover invariants and those tests failed;
- stable boundaries were restored while keeping the files under budget;
- a stale exact wording test for the meta verifier was changed to assert role semantics rather than forcing obsolete prose back into the blueprint.

## Assurance boundary

This cutover is `REGRESSION_VERIFIED` for repository structure, controller semantics, ingress wiring, hot-path budgets and current CI.

It is **not** yet proof of a controller-native live maintenance trajectory. This repair began before the controller existed, so no retroactive stage trace is fabricated.

It is also not tool-level hard isolation. The current ChatGPT GitHub connector can issue repository mutations directly; repository runtime code cannot physically intercept that external tool call. Therefore the strongest current guarantee is routing + deterministic action authorization + regression/CI detection, not an unbypassable mutation middleware.

A stronger future assurance layer would require one of:
- all SYSTEM_INFRA mutations routed through an actual controller-aware mutation gateway; or
- repository protection/required-check rules that reject unauthorized direct writes before they become accepted authority.

Do not add that layer merely as prose. Promote it only when the product/tool surface can actually enforce it and after complexity/payoff review.

## Open live gates

1. First real systemic/non-trivial maintenance incident that starts after this cutover must produce a controller-native trajectory without the user having to demand the missing SOP step.
2. The trajectory must demonstrate entry triage, canonical stage order, implementation-stage mutation authorization, validation, second-order review and closure without forward skipping.
3. If a future model can still directly bypass the controller while satisfying post-hoc records, classify that as `execution-controller-not-on-mutation-path` and escalate to tool-level enforcement rather than adding more reminders.
