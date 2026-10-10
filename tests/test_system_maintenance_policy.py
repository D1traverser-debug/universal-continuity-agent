import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_system_maintenance_policy_requires_autonomous_closure():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")

    assert policy["status"] == "ACTIVE"
    assert "ASSISTANT_DETECTS_SYSTEMIC_GAP" in policy["triggers"]
    assert "USER_REPORT_REVEALS_SYSTEMIC_GAP" in policy["triggers"]

    autonomy = policy["default_autonomy"]
    assert autonomy["diagnose_root_cause"] is True
    assert autonomy["apply_smallest_safe_fix"] is True
    assert autonomy["add_or_update_regression_guard_when_testable"] is True
    assert autonomy["run_or_observe_relevant_ci"] is True
    assert autonomy["update_authoritative_status_and_handoff"] is True
    assert autonomy["record_change_and_remaining_risk"] is True
    assert autonomy["reread_authority_before_claiming_committed"] is True
    assert autonomy["ask_user_to_manage_internal_migration_or_recordkeeping"] is False
    assert autonomy["wait_for_user_to_notice_related_internal_followups"] is False


def test_system_maintenance_policy_preserves_owner_boundaries():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    boundaries = policy["scope_boundaries"]

    assert boundaries["do_not_steal_other_active_owner_lease"] is True
    assert boundaries["do_not_rewrite_domain_business_truth_from_maintenance_task"] is True
    assert boundaries["do_not_add_permanent_agent_without_invocation_executor_evidence_contract"] is True
    assert boundaries["do_not_treat_repo_write_as_proof_old_chats_received_update"] is True


def test_blueprint_and_learning_policy_wire_maintenance_policy():
    blueprint = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "SYSTEM_MAINTENANCE_POLICY.json" in blueprint
    assert "Autonomous maintenance invariant" in blueprint
    assert "SYSTEM_MAINTENANCE_POLICY.json" in learning
    assert "do not stop at diagnosis" in learning


def test_material_maintenance_change_requires_durable_record():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    record = policy["required_durable_record"]

    assert record["when_material_change_occurs"] is True
    required_fields = set(record["fields"])
    assert {
        "problem",
        "root_cause",
        "changed_authority_surfaces",
        "validation_or_ci_result",
        "behavioral_effect",
        "remaining_risks_or_external_dependencies",
        "current_stage",
        "next_action",
    }.issubset(required_fields)
