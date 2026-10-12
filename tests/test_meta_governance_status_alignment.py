import json
from pathlib import Path

from runtime.maintenance_controller import evaluate_maintenance_state
from runtime.meta_maintenance import CURRENT_META_MAINTENANCE_SCHEMA


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_maintenance_policy_version_is_aligned_across_authority_and_status_surfaces():
    policy = load_json("SYSTEM_MAINTENANCE_POLICY.json")
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    harness = load_json("HARNESS_STATUS.json")

    expected = policy["schema_version"]
    assert manifest["system_maintenance_policy_version"] == expected
    assert harness["system_maintenance"]["policy_version"] == expected


def test_meta_harness_version_is_aligned_across_runtime_manifest_and_status_cache():
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    harness = load_json("HARNESS_STATUS.json")

    assert manifest["meta_maintenance_harness_version"] == CURRENT_META_MAINTENANCE_SCHEMA
    assert harness["meta_governance"]["runtime_version"] == CURRENT_META_MAINTENANCE_SCHEMA
    assert harness["latest_meta_maintenance_run"] == manifest["latest_meta_maintenance_run_ref"]


def test_blueprint_exposes_meta_governance_as_posthoc_structural_verifier_not_independent_agent():
    blueprint = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")

    assert "runtime/meta_maintenance.py" in blueprint
    assert "post-hoc closure verifier" in blueprint
    assert "closure record is structurally conformant" in blueprint
    assert "Neither proves semantic diagnosis quality" in blueprint
    assert "not an independent LLM reviewer" in blueprint
    assert "A new supervisory LLM Agent is not implied" in blueprint


def test_harness_records_meta_governance_assurance_ceiling_and_hot_path_boundary():
    harness = load_json("HARNESS_STATUS.json")
    meta = harness["meta_governance"]

    assert meta["runtime"] == "runtime/meta_maintenance.py"
    assert meta["runtime_version"] == CURRENT_META_MAINTENANCE_SCHEMA
    assert meta["authority"] == "SYSTEM_MAINTENANCE_POLICY.json"
    assert meta["assurance_ceiling"] == "STRUCTURED_PROCESS_CONFORMANCE_ONLY"
    assert meta["independent_semantic_review_proven"] is False
    assert meta["business_hot_path_preload_added"] is False
    assert meta["external_account_instruction_expansion_required"] is False
    assert meta["no_change_required_is_legal_with_inspection_reason_and_validation"] is True
    assert meta["new_business_owner_global_closure_requires_current_topology_bound_meta_propagation"] is True
    assert meta["systemic_run_requires_capability_reuse_scan"] is True
    assert meta["systemic_run_requires_fact_decision_frontier"] is True
    assert meta["systemic_run_requires_architecture_payoff_deletion_test"] is True
    assert meta["systemic_run_requires_parent_system_outline_before_deep_diagnosis"] is True
    assert meta["systemic_run_requires_failure_history_search"] is True
    assert meta["recurrent_failure_requires_higher_abstraction"] is True
    assert meta["high_level_repair_returns_to_class_and_instance"] is True
    assert meta["high_level_repair_returns_to_class_and_instance_before_validation"] is True


def test_latest_meta_run_is_bound_to_complete_controller_trace_once_contract_is_enabled():
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    controller_contract = manifest.get("maintenance_controller_contract_version")
    if not controller_contract:
        return

    assert controller_contract == "1.0"
    policy = load_json("SYSTEM_MAINTENANCE_POLICY.json")
    run = load_json(manifest["latest_meta_maintenance_run_ref"])
    binding = run.get("maintenance_controller")
    assert isinstance(binding, dict)
    assert binding.get("contract_version") == controller_contract
    assert binding.get("state_ref") == manifest.get("last_completed_maintenance_controller_state_ref")

    state = binding.get("final_state")
    assert isinstance(state, dict)
    result = evaluate_maintenance_state(state, policy, require_complete=True)
    assert result.status == "PASS", result.errors
    assert state["triage_outcome"] == "CONFIRMED_DEFECT"
    assert state["status"] == "COMPLETE"
    assert state["prepatch_checkpoint"]["authoritative_reread_verified"] is True
    assert binding.get("prepatch_checkpoint_ref") == state["prepatch_checkpoint"]["ref"]
    assert binding.get("run_id") == state["run_id"]


def test_controller_state_is_not_a_second_policy_or_business_authority():
    blueprint = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")
    assert "runtime/maintenance_controller.py" in blueprint
    assert "SYSTEM_MAINTENANCE_POLICY.json" in blueprint
    assert "during-execution transition controller" in blueprint
    assert "Domain owners retain business truth" in blueprint
