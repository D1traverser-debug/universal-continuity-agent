from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

TRIAGE_OUTCOMES = {"NO_DEFECT", "INVESTIGATE", "CONFIRMED_DEFECT"}
REFERENCE_ASSURANCE = "DETERMINISTIC_REFERENCE_SIMULATION_ONLY"

# The simulator intentionally verifies only the control-flow invariants needed to
# reason about the parent loop. It is not a product-chat or child-owner executor.
_REQUIRED_FULL_LOOP_STEPS = (
    "DETECT",
    "BUILD_FULL_SYSTEM_IMPACT_MAP",
    "DIAGNOSE_ROOT_CAUSE",
    "DECIDE_LEARNING_SCOUT_AND_DISTILL_RELEVANT_EVIDENCE",
    "CHALLENGE_INITIAL_SOLUTION_CANDIDATES",
    "PATCH_MINIMUM_AUTHORITY_SURFACE",
    "RUN_OR_OBSERVE_VALIDATION",
    "RUN_CROSS_SUBSYSTEM_PROPAGATION_CHECK",
    "RUN_SECOND_ORDER_CHALLENGE_AND_CLAIM_CALIBRATION",
    "DISTILL_ACCEPTED_LEARNING_AND_USER_CORRECTION",
    "REREAD_AUTHORITATIVE_STATE",
)

_REQUIRED_SHARED_FLAGS = (
    "required",
    "pre_patch_system_level_reframe_required",
    "post_validation_second_order_reframe_required",
    "durable_pattern_distillation_required",
    "propagate_method_and_invariant_not_business_truth",
)


@dataclass(frozen=True)
class ReferenceTrajectoryResult:
    status: str
    triage_outcome: str
    events: tuple[str, ...]
    errors: tuple[str, ...]
    assurance_ceiling: str
    business_truth_propagated: bool


def _ordered_subset(sequence: list[str], required: tuple[str, ...]) -> bool:
    try:
        positions = [sequence.index(item) for item in required]
    except ValueError:
        return False
    return positions == sorted(positions)


def simulate_self_maintenance_reference(
    *,
    triage_outcome: str,
    material: bool,
    systemic: bool,
    solution_uncertain: bool,
    shared_method_change: bool,
    validation_passed: bool,
    policy: Mapping[str, Any],
    adapter: Mapping[str, Any],
) -> ReferenceTrajectoryResult:
    """Dry-run the intended self-maintenance/evolution control flow.

    This is a deterministic reference simulation. It proves that the current
    repository authorities can compose into the expected route for representative
    inputs. It does not prove that a live ChatGPT conversation or a remote child
    owner will actually take the route; those claims still require product traces.
    """

    outcome = str(triage_outcome).strip().upper()
    events: list[str] = ["DEFECT_TRIAGE"]
    errors: list[str] = []

    if outcome not in TRIAGE_OUTCOMES:
        return ReferenceTrajectoryResult(
            status="FAIL",
            triage_outcome=outcome,
            events=tuple(events),
            errors=("unsupported_triage_outcome",),
            assurance_ceiling=REFERENCE_ASSURANCE,
            business_truth_propagated=False,
        )

    if outcome == "NO_DEFECT":
        events.append("EXPLAIN_AND_STOP")
        return ReferenceTrajectoryResult(
            status="PASS",
            triage_outcome=outcome,
            events=tuple(events),
            errors=(),
            assurance_ceiling=REFERENCE_ASSURANCE,
            business_truth_propagated=False,
        )

    if outcome == "INVESTIGATE":
        events.extend(("READ_CURRENT_AUTHORITY", "GATHER_EVIDENCE", "STOP_PENDING_EVIDENCE"))
        return ReferenceTrajectoryResult(
            status="PASS",
            triage_outcome=outcome,
            events=tuple(events),
            errors=(),
            assurance_ceiling=REFERENCE_ASSURANCE,
            business_truth_propagated=False,
        )

    if not material:
        events.append("LOCAL_REPAIR_ONLY")
        return ReferenceTrajectoryResult(
            status="PASS",
            triage_outcome=outcome,
            events=tuple(events),
            errors=(),
            assurance_ceiling=REFERENCE_ASSURANCE,
            business_truth_propagated=False,
        )

    loop = policy.get("maintenance_loop")
    if not isinstance(loop, list) or not all(isinstance(item, str) for item in loop):
        errors.append("maintenance_loop_missing")
        loop = []
    elif not _ordered_subset(loop, _REQUIRED_FULL_LOOP_STEPS):
        errors.append("maintenance_loop_required_order_missing")

    shared = (
        adapter.get("operational_hygiene_and_learning", {})
        .get("unified_self_maintenance_evolution_loop", {})
    )
    if not isinstance(shared, Mapping):
        errors.append("unified_loop_contract_missing")
        shared = {}
    for flag in _REQUIRED_SHARED_FLAGS:
        if shared.get(flag) is not True:
            errors.append(f"unified_loop_flag_missing:{flag}")

    events.extend(("READ_CURRENT_AUTHORITY", "PARENT_SYSTEM_REFRAME", "DIAGNOSE_ROOT_CAUSE"))

    if systemic or solution_uncertain:
        events.append("LEARNING_SCOUT")

    events.extend(("COMPARE_AND_FALSIFY_CANDIDATES", "PATCH_MINIMUM_AUTHORITY_SURFACE"))

    if not validation_passed:
        events.extend(("VALIDATION_FAIL", "KEEP_ACTIVE_WITH_BLOCKER"))
        return ReferenceTrajectoryResult(
            status="PASS" if not errors else "FAIL",
            triage_outcome=outcome,
            events=tuple(events),
            errors=tuple(errors),
            assurance_ceiling=REFERENCE_ASSURANCE,
            business_truth_propagated=False,
        )

    events.extend(("VALIDATION_PASS", "SECOND_ORDER_REVIEW"))

    business_truth_propagated = False
    if shared_method_change:
        events.append("PROPAGATE_SHARED_METHOD_INVARIANTS_ONLY")

    events.extend(("CLEAN_SUPERSEDED_MECHANISMS", "DISTILL_DURABLE_LEARNING", "REREAD_AUTHORITY"))

    return ReferenceTrajectoryResult(
        status="PASS" if not errors else "FAIL",
        triage_outcome=outcome,
        events=tuple(events),
        errors=tuple(errors),
        assurance_ceiling=REFERENCE_ASSURANCE,
        business_truth_propagated=business_truth_propagated,
    )
