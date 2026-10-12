import json
from pathlib import Path

import pytest

from runtime.maintenance_controller import (
    authorize_action,
    block_current_stage,
    canonical_stages,
    complete_current_stage,
    evaluate_maintenance_state,
    new_maintenance_state,
    reopen_stage,
    resolve_investigation,
    resume_blocked_state,
)


ROOT = Path(__file__).resolve().parents[1]


def policy():
    return json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))


def advance_until_prefix(state, prefix):
    stages = canonical_stages(policy())
    while state["current_stage"] is not None and not state["current_stage"].startswith(prefix):
        stage = state["current_stage"]
        state = complete_current_stage(
            state,
            policy(),
            stage=stage,
            evidence_refs=[f"evidence://{stage}"],
            summary=f"completed {stage}",
        )
    return state


def test_no_defect_closes_without_starting_maintenance_sop():
    state = new_maintenance_state(run_id="r-no-defect", triage_outcome="NO_DEFECT", policy=policy())
    result = evaluate_maintenance_state(state, policy())
    assert result.status == "PASS", result.errors
    assert state["status"] == "NO_DEFECT_CLOSED"
    assert state["current_stage"] is None
    assert state["completed_stage_receipts"] == []


def test_confirmed_defect_starts_at_first_canonical_stage_and_cannot_skip():
    stages = canonical_stages(policy())
    state = new_maintenance_state(run_id="r-confirmed", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    assert state["current_stage"] == stages[0]

    with pytest.raises(ValueError, match="cannot skip or reorder"):
        complete_current_stage(
            state,
            policy(),
            stage=stages[1],
            evidence_refs=["evidence://skip"],
            summary="try to skip",
        )


def test_material_patch_is_forbidden_until_implementation_stage():
    state = new_maintenance_state(run_id="r-patch-gate", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    blocked = authorize_action(state, policy(), "MATERIAL_PATCH")
    assert blocked.status == "FAIL"
    assert "action_not_authorized_at_current_stage:MATERIAL_PATCH" in blocked.errors

    state = advance_until_prefix(state, "M7_")
    allowed = authorize_action(state, policy(), "MATERIAL_PATCH")
    assert allowed.status == "PASS", allowed.errors
    assert allowed.material_patch_allowed is True


def test_investigate_cannot_patch_until_confirmed():
    state = new_maintenance_state(run_id="r-investigate", triage_outcome="INVESTIGATE", policy=policy())
    state = advance_until_prefix(state, "M7_")
    denied = authorize_action(state, policy(), "MATERIAL_PATCH")
    assert denied.status == "FAIL"

    state = resolve_investigation(
        state,
        policy(),
        outcome="CONFIRMED_DEFECT",
        evidence_refs=["evidence://confirmed"],
    )
    allowed = authorize_action(state, policy(), "MATERIAL_PATCH")
    assert allowed.status == "PASS", allowed.errors


def test_investigation_can_close_no_defect_without_patch_path():
    state = new_maintenance_state(run_id="r-investigate-clean", triage_outcome="INVESTIGATE", policy=policy())
    state = resolve_investigation(
        state,
        policy(),
        outcome="NO_DEFECT",
        evidence_refs=["evidence://no-defect"],
    )
    result = evaluate_maintenance_state(state, policy())
    assert result.status == "PASS", result.errors
    assert state["status"] == "NO_DEFECT_CLOSED"
    assert authorize_action(state, policy(), "MATERIAL_PATCH").status == "FAIL"


def test_validation_failure_can_reopen_implementation_and_invalidates_downstream_receipts():
    state = new_maintenance_state(run_id="r-reopen", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    state = advance_until_prefix(state, "M8_")
    implementation_stage = next(stage for stage in canonical_stages(policy()) if stage.startswith("M7_"))
    assert state["current_stage"].startswith("M8_")

    reopened = reopen_stage(
        state,
        policy(),
        target_stage=implementation_stage,
        reason="validation exposed consumer drift",
        evidence_refs=["ci://failed"],
    )
    assert reopened["current_stage"] == implementation_stage
    assert authorize_action(reopened, policy(), "MATERIAL_PATCH").status == "PASS"
    assert len(reopened["completed_stage_receipts"]) == canonical_stages(policy()).index(implementation_stage)


def test_second_order_review_can_reopen_system_impact_map_and_invalidate_later_work():
    state = new_maintenance_state(run_id="r-second-order", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    state = advance_until_prefix(state, "M10_")
    impact_stage = next(stage for stage in canonical_stages(policy()) if stage.startswith("M2_FULL_SYSTEM_IMPACT_MAP"))
    reopened = reopen_stage(
        state,
        policy(),
        target_stage=impact_stage,
        reason="second-order review found a missed consumer surface",
        evidence_refs=["audit://missed-consumer"],
    )
    assert reopened["current_stage"] == impact_stage
    assert authorize_action(reopened, policy(), "MATERIAL_PATCH").status == "FAIL"


def test_blocked_stage_preserves_exact_resume_point_and_disallows_patch():
    state = new_maintenance_state(run_id="r-blocked", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    stage = state["current_stage"]
    blocked = block_current_stage(
        state,
        policy(),
        reason="required authority unavailable",
        evidence_refs=["tool://unavailable"],
    )
    assert blocked["status"] == "BLOCKED"
    assert blocked["current_stage"] == stage
    assert authorize_action(blocked, policy(), "MATERIAL_PATCH").status == "FAIL"

    resumed = resume_blocked_state(blocked, policy())
    assert resumed["status"] == "ACTIVE"
    assert resumed["current_stage"] == stage


def test_close_is_impossible_until_every_canonical_stage_is_completed():
    state = new_maintenance_state(run_id="r-close", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    assert authorize_action(state, policy(), "CLOSE").status == "FAIL"

    for stage in canonical_stages(policy()):
        state = complete_current_stage(
            state,
            policy(),
            stage=stage,
            evidence_refs=[f"evidence://{stage}"],
            summary=f"completed {stage}",
        )

    result = evaluate_maintenance_state(state, policy(), require_complete=True)
    assert result.status == "PASS", result.errors
    assert state["status"] == "COMPLETE"
    assert authorize_action(state, policy(), "CLOSE").status == "PASS"


def test_completed_receipts_must_be_exact_canonical_prefix():
    state = new_maintenance_state(run_id="r-tamper", triage_outcome="CONFIRMED_DEFECT", policy=policy())
    first = state["current_stage"]
    state = complete_current_stage(
        state,
        policy(),
        stage=first,
        evidence_refs=["evidence://first"],
        summary="first complete",
    )
    state["completed_stage_receipts"][0]["stage"] = canonical_stages(policy())[2]
    result = evaluate_maintenance_state(state, policy())
    assert result.status == "FAIL"
    assert "completed_stages_must_be_exact_canonical_prefix" in result.errors
