import copy
import json
import shutil
from pathlib import Path

from runtime.owner_topology import business_owner_names
from runtime.system_audit import (
    CORE_CHECKS,
    FAULT_INJECTION_SCENARIOS,
    audit_local_control_plane,
    evaluate_owner_protocol_observation,
    plan_audit,
)


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def current_business_owners():
    return business_owner_names(load("OWNER_REGISTRY.json"))


def test_routine_change_does_not_scan_every_business_pipeline():
    plan = plan_audit(["README.md"], "routine_change", owner_registry=load("OWNER_REGISTRY.json"))

    assert plan["modes"] == ["CORE_ALWAYS", "IMPACT_SCOPED"]
    assert plan["run_all_owner_business_pipelines"] is False
    assert plan["owner_metadata_scope"] == []
    assert plan["fault_injection_scenarios"] == []
    assert "maintenance_meta_governance_alignment" in CORE_CHECKS


def test_explicit_global_audit_escalates_to_all_current_business_owner_metadata_and_fault_injection():
    owners = load("OWNER_REGISTRY.json")
    plan = plan_audit([], "explicit_global_audit", owner_registry=owners)

    assert "FULL_CONTROL_PLANE" in plan["modes"]
    assert "SYNTHETIC_FAULT_INJECTION" in plan["modes"]
    assert plan["owner_metadata_scope"] == sorted(business_owner_names(owners))
    assert plan["run_all_owner_business_pipelines"] is False
    assert set(plan["fault_injection_scenarios"]) == set(FAULT_INJECTION_SCENARIOS)


def test_user_challenge_to_maintenance_completeness_is_a_full_fault_injected_audit_trigger():
    owners = load("OWNER_REGISTRY.json")
    plan = plan_audit(
        [],
        "USER_CHALLENGES_MAINTENANCE_METHOD_OR_GLOBAL_COMPLETENESS",
        owner_registry=owners,
    )

    assert plan["trigger"] == "user_challenges_maintenance_method_or_global_completeness"
    assert "FULL_CONTROL_PLANE" in plan["modes"]
    assert "SYNTHETIC_FAULT_INJECTION" in plan["modes"]
    assert plan["owner_metadata_scope"] == sorted(business_owner_names(owners))
    assert "maintenance_meta_governance_alignment" in plan["checks"]


def test_high_risk_control_plane_change_forces_dynamic_full_control_plane_sweep():
    owners = load("OWNER_REGISTRY.json")
    plan = plan_audit(["OWNER_PROTOCOL_ADAPTATION_REGISTRY.json"], "routine_change", owner_registry=owners)

    assert plan["risk"] == "HIGH"
    assert "FULL_CONTROL_PLANE" in plan["modes"]
    assert plan["owner_metadata_scope"] == sorted(business_owner_names(owners))
    assert "owner_protocol_observation_match" in plan["checks"]
    assert "dangling_remote_pointer_check" in plan["checks"]


def test_synthetic_new_business_owner_is_automatically_in_audit_scope():
    owners = copy.deepcopy(load("OWNER_REGISTRY.json"))
    owners["owners"].append(
        {
            "name": "SYNTHETIC_NEW_AGENT",
            "owner_kind": "BUSINESS",
            "domains": ["SYNTHETIC_DOMAIN"],
            "priority": 100,
            "adapter_status": "SYNTHETIC_RECONCILED",
            "bare_inherit_participant": True,
            "bare_inherit_source": "synthetic-owner@main:continuity/TASK_INDEX.json",
            "checkpoint_authority": "synthetic-owner@main:continuity/tasks/<task_id>/TASK_MANIFEST.json",
            "protocol_adapter": "synthetic-owner@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
            "execution_capability_ref": "synthetic-owner@main:continuity/EXECUTION_CAPABILITIES.json",
        }
    )

    plan = plan_audit([], "explicit_global_audit", owner_registry=owners)
    assert "SYNTHETIC_NEW_AGENT" in plan["owner_metadata_scope"]


def test_new_business_owner_fails_closed_until_derived_caches_converge(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo)

    owner_registry_path = repo / "OWNER_REGISTRY.json"
    owner_registry = json.loads(owner_registry_path.read_text(encoding="utf-8"))
    owner_registry["owners"].append(
        {
            "name": "SYNTHETIC_NEW_AGENT",
            "owner_kind": "BUSINESS",
            "domains": ["SYNTHETIC_DOMAIN"],
            "priority": 100,
            "adapter_status": "SYNTHETIC_RECONCILED",
            "bare_inherit_participant": True,
            "bare_inherit_source": "synthetic-owner@main:continuity/TASK_INDEX.json",
            "checkpoint_authority": "synthetic-owner@main:continuity/tasks/<task_id>/TASK_MANIFEST.json",
            "protocol_adapter": "synthetic-owner@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
            "execution_capability_ref": "synthetic-owner@main:continuity/EXECUTION_CAPABILITIES.json",
        }
    )
    owner_registry_path.write_text(json.dumps(owner_registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    incomplete = audit_local_control_plane(repo)
    assert incomplete["status"] == "FAIL"
    assert any("OWNER_PROTOCOL_ADAPTATION_REGISTRY owner set" in error for error in incomplete["errors"])
    assert any("OWNER_EXECUTION_REGISTRY owner set" in error for error in incomplete["errors"])

    adaptation_path = repo / "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json"
    adaptation = json.loads(adaptation_path.read_text(encoding="utf-8"))
    adaptation["owners"].append(
        {
            "owner": "SYNTHETIC_NEW_AGENT",
            "repository": "synthetic-owner",
            "historical_from_protocol": "3.7",
            "observed_protocol": "3.7",
            "target_protocol": "3.7",
            "classification": "COMPATIBLE",
            "strategy": "SYNTHETIC_ADMISSION_FIXTURE",
            "business_state_rewrite": False,
            "force_lease_takeover": False,
            "adapter_ref": "synthetic-owner@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
            "status": "SYNTHETIC_READY",
        }
    )
    adaptation_path.write_text(json.dumps(adaptation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    execution_path = repo / "OWNER_EXECUTION_REGISTRY.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["owners"].append(
        {
            "owner": "SYNTHETIC_NEW_AGENT",
            "repository": "synthetic-owner@main",
            "capability_ref": "continuity/EXECUTION_CAPABILITIES.json",
            "summary": "Synthetic new-owner admission fixture.",
            "known_ceiling": "DECLARED_ONLY",
            "strict_isolated_execution_claimed": False,
        }
    )
    execution_path.write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    converged = audit_local_control_plane(repo)
    assert converged["status"] == "PASS", converged["errors"]
    assert "SYNTHETIC_NEW_AGENT" in converged["checked_business_owners"]
    assert "SYNTHETIC_NEW_AGENT" in converged["checked_bare_inherit_owners"]


def test_policy_owns_risk_tiered_audit_without_creating_parallel_root_policy():
    policy = json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))
    audit = policy["system_audit_strategy"]

    assert policy["schema_version"] == "1.6"
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
    assert result["checked_business_owners"] == sorted(current_business_owners())


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


def test_local_audit_detects_missing_or_invalid_meta_governance_record(tmp_path):
    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo)

    manifest_path = repo / "tasks/universal-continuity-maintenance/TASK_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["latest_meta_maintenance_run_ref"] = "audits/DOES_NOT_EXIST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = audit_local_control_plane(repo)
    assert result["status"] == "FAIL"
    assert "maintenance latest_meta_maintenance_run_ref is missing" in result["errors"]


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
    assert "new_business_owner_is_added_without_execution_or_adaptation_convergence" in scenarios
    assert "bare_discovery_uses_stale_parallel_owner_list" in scenarios
    assert "methodology_applicable_profile_is_silently_omitted" in scenarios
    assert "material_write_reports_committed_without_authoritative_reread" in scenarios
    assert "destructive_mutation_has_unknown_identity_or_dependency" in scenarios
    assert "external_reference_is_promoted_to_authority_by_presence" in scenarios
    assert "declared_executor_is_treated_as_session_execution_proof" in scenarios
    assert "meta_maintenance_outline_omitted_after_systemic_correction" in scenarios
    assert "hard_coded_stale_methodology_receipt_semantics_survive_contract_upgrade" in scenarios
