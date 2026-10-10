import json
import shutil
from pathlib import Path

from runtime.system_audit import (
    BUSINESS_OWNERS,
    FAULT_INJECTION_SCENARIOS,
    audit_local_control_plane,
    evaluate_owner_protocol_observation,
    plan_audit,
)


ROOT = Path(__file__).resolve().parents[1]


def test_routine_change_does_not_scan_every_business_pipeline():
    plan = plan_audit(["README.md"], "routine_change")

    assert plan["modes"] == ["CORE_ALWAYS", "IMPACT_SCOPED"]
    assert plan["run_all_owner_business_pipelines"] is False
    assert plan["owner_metadata_scope"] == []
    assert plan["fault_injection_scenarios"] == []


def test_explicit_global_audit_escalates_to_all_owner_metadata_and_fault_injection():
    plan = plan_audit([], "explicit_global_audit")

    assert "FULL_CONTROL_PLANE" in plan["modes"]
    assert "SYNTHETIC_FAULT_INJECTION" in plan["modes"]
    assert plan["owner_metadata_scope"] == sorted(BUSINESS_OWNERS)
    assert plan["run_all_owner_business_pipelines"] is False
    assert set(plan["fault_injection_scenarios"]) == set(FAULT_INJECTION_SCENARIOS)


def test_high_risk_control_plane_change_forces_full_control_plane_sweep():
    plan = plan_audit(["OWNER_PROTOCOL_ADAPTATION_REGISTRY.json"], "routine_change")

    assert plan["risk"] == "HIGH"
    assert "FULL_CONTROL_PLANE" in plan["modes"]
    assert plan["owner_metadata_scope"] == sorted(BUSINESS_OWNERS)
    assert "owner_protocol_observation_match" in plan["checks"]
    assert "dangling_remote_pointer_check" in plan["checks"]


def test_policy_owns_risk_tiered_audit_without_creating_parallel_root_policy():
    policy = json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))
    audit = policy["system_audit_strategy"]

    assert policy["schema_version"] == "1.5"
    assert audit["runtime"] == "runtime/system_audit.py"
    assert audit["full_business_pipeline_every_audit"] is False
    assert set(audit["layers"]) == {
        "CORE_ALWAYS",
        "IMPACT_SCOPED",
        "OWNER_SENTINEL_ROTATION",
        "FULL_CONTROL_PLANE",
        "SYNTHETIC_FAULT_INJECTION",
    }
    assert audit["layers"]["SYNTHETIC_FAULT_INJECTION"]["production_mutation_allowed_by_default"] is False
    assert not (ROOT / "GLOBAL_AUDIT_POLICY.json").exists()
    assert not (ROOT / "SYSTEM_AUDIT_POLICY.json").exists()


def test_current_repository_passes_local_cross_surface_audit():
    result = audit_local_control_plane(ROOT)

    assert result["status"] == "PASS", result["errors"]
    assert result["checked_business_owners"] == sorted(BUSINESS_OWNERS)


def test_local_audit_detects_stale_protocol_registry_and_owner_cache(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo)

    adaptation_path = repo / "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json"
    adaptation = json.loads(adaptation_path.read_text(encoding="utf-8"))
    video = next(item for item in adaptation["owners"] if item["owner"] == "VIDEO_GROWTH_AGENT")
    video["observed_protocol"] = "3.5"
    video["classification"] = "MIGRATABLE"
    video["status"] = "ACTIVE_TASK_PENDING_VALID_WRITER_RECONCILIATION"
    adaptation_path.write_text(json.dumps(adaptation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    owner_registry_path = repo / "OWNER_REGISTRY.json"
    owner_registry = json.loads(owner_registry_path.read_text(encoding="utf-8"))
    video_owner = next(item for item in owner_registry["owners"] if item["name"] == "VIDEO_GROWTH_AGENT")
    video_owner["adapter_status"] = "READY_V37_PROTOCOL_ADAPTER__ACTIVE_TASK_LAZY_RECONCILIATION"
    owner_registry_path.write_text(json.dumps(owner_registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = audit_local_control_plane(repo)

    assert result["status"] == "FAIL"
    assert any("VIDEO_GROWTH_AGENT" in error for error in result["errors"])


def test_live_owner_observation_detects_stale_registry_and_dangling_remote_ref():
    entry = {
        "owner": "FINANCIAL_WRITING_AGENT_RUNTIME",
        "observed_protocol": "3.3",
        "target_protocol": "3.7",
        "classification": "MIGRATABLE",
    }

    errors = evaluate_owner_protocol_observation(
        entry,
        authoritative_protocol="3.7",
        missing_remote_refs=["continuity/HANDOFF_COMPACTION_PLAN.json"],
    )

    assert any("observed_protocol is stale" in error for error in errors)
    assert any("dangling remote" in error for error in errors)


def test_fault_injection_suite_targets_unknown_unknown_boundaries():
    scenarios = set(FAULT_INJECTION_SCENARIOS)

    assert "required_discovery_source_unavailable" in scenarios
    assert "stale_registry_attempts_to_override_owner_authority" in scenarios
    assert "material_write_reports_committed_without_authoritative_reread" in scenarios
    assert "destructive_mutation_has_unknown_identity_or_dependency" in scenarios
    assert "external_reference_is_promoted_to_authority_by_presence" in scenarios
    assert "declared_executor_is_treated_as_session_execution_proof" in scenarios
