import json
from pathlib import Path

from runtime.meta_maintenance import (
    ABSTRACTION_LEVELS,
    ESCALATION_DECISIONS,
    RECURRENCE_STATUSES,
)


ROOT = Path(__file__).resolve().parents[1]


def test_failure_abstraction_escalation_policy_is_single_semantic_owner():
    policy = json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))
    escalation = policy["failure_abstraction_escalation"]

    assert escalation["owner"] == "SYSTEM_MAINTENANCE_POLICY.json"
    assert tuple(escalation["abstraction_levels_low_to_high"]) == ABSTRACTION_LEVELS
    assert set(escalation["recurrence_statuses"]) == RECURRENCE_STATUSES
    assert set(escalation["escalation_decisions"]) == ESCALATION_DECISIONS
    assert escalation["rules"]["systemic_run_must_search_every_classified_failure_class"] is True
    assert escalation["rules"]["recurrence_after_accepted_fix_must_move_strictly_above_prior_repair_level"] is True
    assert escalation["rules"]["same_or_lower_level_repeat_patch_is_allowed"] is False
    assert escalation["rules"]["high_level_repair_must_return_to_class_level_prevention"] is True
    assert escalation["rules"]["high_level_repair_must_return_to_concrete_instance_fix"] is True


def test_meta_outline_builds_parent_system_map_before_deep_diagnosis_and_history_escalation():
    policy = json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))
    stages = policy["meta_maintenance_outline"]["stages"]
    loop = policy["maintenance_loop"]

    assert stages.index("M2_FULL_SYSTEM_IMPACT_MAP") < stages.index("M2A_ROOT_CAUSE_FAILURE_HISTORY_AND_ABSTRACTION_ESCALATION")
    assert loop.index("BUILD_FULL_SYSTEM_IMPACT_MAP") < loop.index("DIAGNOSE_ROOT_CAUSE")
    assert loop.index("DIAGNOSE_ROOT_CAUSE") < loop.index("SEARCH_HISTORICAL_FAILURE_CLASS_AND_PRIOR_REPAIRS")
    assert loop.index("SEARCH_HISTORICAL_FAILURE_CLASS_AND_PRIOR_REPAIRS") < loop.index("ESCALATE_ABSTRACTION_IF_RECURRED_AFTER_FIX")
    assert loop.index("ESCALATE_ABSTRACTION_IF_RECURRED_AFTER_FIX") < loop.index("PATCH_MINIMUM_AUTHORITY_SURFACE")
    assert loop.index("PATCH_MINIMUM_AUTHORITY_SURFACE") < loop.index("RETURN_TO_CLASS_PREVENTION_AND_INSTANCE_FIX")
    assert loop.index("RETURN_TO_CLASS_PREVENTION_AND_INSTANCE_FIX") < loop.index("RUN_OR_OBSERVE_VALIDATION")
