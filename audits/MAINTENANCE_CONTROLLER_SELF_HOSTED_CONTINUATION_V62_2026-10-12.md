# Maintenance Controller Self-Hosted Continuation V62 — 2026-10-12

## Scope

This record closes the controller-enforcement repair only to the assurance actually observed. It does not retroactively claim that the triggering incident entered through a controller that did not yet exist.

## Root cause

The prior maintenance architecture had a strong policy and a post-hoc meta verifier, but execution order was still largely model-followed. A systemic run could theoretically patch first and reconstruct required outline/history fields later. Historical recall helped diagnosis but did not enforce execution.

## Canonical repair

- Thin ingress triage remains `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`.
- `runtime/maintenance_controller.py` is the single during-execution controller.
- `SYSTEM_MAINTENANCE_POLICY.json` remains the sole canonical stage/semantic owner; the controller derives stages from it rather than owning a shadow list.
- `runtime/meta_maintenance.py` remains a post-hoc closure/conformance verifier, not a replacement controller or independent semantic reviewer.
- Material patch is denied until the controller reaches implementation and has a durable prepatch checkpoint with authoritative reread.
- Reopen truncates stale downstream receipts and preserves explicit reopen evidence.
- `NO_DEFECT` stays off the maintenance path; `INVESTIGATE` cannot material-patch before confirmation.
- Duplicate `runtime/maintenance_sop.py` and its duplicate tests were removed rather than retained as a second authority.
- `AGENT_MANIFEST.json` declares the durable controller state as a workflow/continuity state surface.
- `tests/test_current_maintenance_controller_state.py` loads the actual state ref from `AGENT_MANIFEST.json` and validates the persisted current state against the current policy on every full pytest run.

## Self-hosted continuation evidence

Durable controller run:

`maintenance-execution-sop-v62-selfhost-2026-10-12`

State authority:

`tasks/universal-continuity-maintenance/MAINTENANCE_CONTROLLER_STATE.json`

The repair began before the controller existed, so M0-M6A are evidence-backed historical receipts rather than a claim of controller-native pre-action enforcement. A verified prepatch checkpoint was then persisted before the self-hosted implementation continuation.

Observed controller-driven continuation:

1. M7 implementation/supersession executed under the persisted controller state.
2. M8 bound real hosted CI evidence.
3. M9 verified shared-method propagation without BUSINESS lease/state mutation.
4. M10 second-order review found a real negative-space defect: controller logic was tested, but CI did not directly validate the persisted current controller state.
5. The controller reopened to M7 rather than closing through the defect.
6. A current-state conformance regression was added.
7. M8 was rerun with hosted CI, then M9 and M10 were re-executed.
8. M11 persisted the execution lesson and the controller state reached COMPLETE revision 21.

The second-order reopen is evidence that the controller was used as execution state rather than only as a final checklist.

## Validation

Second-cycle hosted run:

- GitHub Actions run: `38271641398`
- job: `114887058655`
- risk-tiered local control-plane audit: PASS
- Agent architecture harness: PASS with pre-existing acknowledged owner drift warnings only
- pytest: `295 passed`
- the new current-state conformance test was included in that full suite

Earlier controller cutover validation remains historical evidence, not the latest proof.

## Propagation and authority

All current BUSINESS owners continue to inherit the shared maintenance/evolution method through Universal contracts/routing. The controller is not copied into owner repositories and no BUSINESS lease or business truth was modified by this maintenance run.

## Assurance boundary

Achieved:

`REGRESSION_VERIFIED + SELF_HOSTED_CONTROLLER_CONTINUATION_M7_TO_M11`

Not proven:

- a fresh real systemic incident routed from the original material input through triage and every controller stage from M0 to M11 without user SOP reminders;
- independent semantic correctness of diagnosis/classification;
- semantic completeness of historical analogue matching;
- physically unbypassable mutation enforcement.

The current GitHub main branch is unprotected and an external ChatGPT GitHub connector can directly perform repository mutations. Repository Python cannot physically intercept such a tool call. If a future fresh trajectory bypasses controller authorization, the next repair level is a controller-aware mutation gateway or repository protection/required-check enforcement—not more reminder prose or another supervisor Agent.

## Durable lesson

`recall/history` is diagnostic input. It does not guarantee execution. The stable architecture is:

`thin ingress triage -> persisted deterministic maintenance controller -> stage/action authorization -> validation/reopen -> post-hoc meta/CI closure`

This distinction is the reusable failure-class lesson from this incident.
