import json
from pathlib import Path

from runtime.meta_maintenance import evaluate_meta_maintenance_run


ROOT = Path(__file__).resolve().parents[1]
META_RUN_REF = "audits/META_MAINTENANCE_GOVERNANCE_RUN_2026-10-11.json"


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def valid_systemic_run():
    owners = [
        item["name"]
        for item in load_json("OWNER_REGISTRY.json")["owners"]
        if item.get("owner_kind") == "BUSINESS"
    ]
    return {
        "schema_version": "1.0",
        "run_id": "meta-test-1",
        "scope": "FULL_CONTROL_PLANE",
        "trigger": "USER_CHALLENGES_MAINTENANCE_METHOD_OR_GLOBAL_COMPLETENESS",
        "user_signal": {
            "classifications": ["GOAL_OR_CONSTRAINT", "COUNTEREXAMPLE_OR_FAILURE_REPORT", "PROPOSED_MECHANISM"],
            "goal_or_constraint": "Systemic maintenance must learn, challenge, propagate and validate without repeated user reminders.",
            "proposed_mechanism": "Maybe add an upper system or agent.",
        },
        "authority_inspection": {
            "refs": ["ENTRYPOINT.md", "SYSTEM_MAINTENANCE_POLICY.json", "CONTINUOUS_LEARNING_POLICY.md"]
        },
        "failure_model": {
            "root_cause_layers": ["REPOSITORY_POLICY", "TEST_OR_EVAL", "EVIDENCE_OR_PROPAGATION"],
            "failure_classes": ["repair-first-governance", "self-review-without-process-verifier"],
            "system_impact_map": ["maintenance", "learning", "startup", "owners"],
        },
        "learning_scout": {
            "disposition": "SCOUT_DONE",
            "sources": [
                {
                    "ref": "https://example.test/evals",
                    "observation": "Separate execution traces from evaluation.",
                    "disposition": "ADOPT",
                    "rationale": "Provides a distinct evidence surface.",
                }
            ],
        },
        "alternatives": [
            {"id": "policy-only", "decision": "REJECTED", "rationale": "Self-enforcement remains weak."},
            {"id": "deterministic-harness", "decision": "ACCEPTED", "rationale": "Adds process verification without a fake agent identity."},
        ],
        "instruction_surface": {
            "decision": "NO_CHANGE",
            "reason": "Existing startup routing already loads the maintenance authority for systemic maintenance.",
        },
        "propagation": {
            "classification": "COMPOSABLE_PROFILE_METHOD",
            "scope": "ALL_BUSINESS_OWNERS",
            "impacted_business_owners": owners,
            "mechanism": "SYSTEM_MAINTENANCE_POLICY semantics owner through operational_hygiene/evolution bindings",
            "stale_override_scan": "PASS",
        },
        "complexity_efficiency": {
            "new_authority_surfaces": 0,
            "mandatory_startup_context_delta": 0,
            "tool_or_remote_read_delta": "maintenance-only",
            "steady_state_latency_effect": "NONE_ON_BUSINESS_HOT_PATH",
            "duplicate_rule_effect": "CONSOLIDATE",
            "cross_owner_touch_count": len(owners),
            "migration_compatibility_effect": "NO_PROTOCOL_BUMP",
            "test_observability_effect": "ADDS_META_HARNESS_TESTS",
            "decision": "ACCEPTABLE",
        },
        "authority_surface_admission": "PASS",
        "implementation": {
            "changed_paths": ["SYSTEM_MAINTENANCE_POLICY.json", "runtime/meta_maintenance.py"],
            "superseded_or_demoted_surfaces": [],
        },
        "validation": {
            "regression_or_eval_refs": ["pytest://test_meta_maintenance"],
            "second_order_challenge": "PASS",
            "cross_surface_or_fault_audit": "PASS",
        },
        "closure": {
            "assurance_ceiling": "REGRESSION_VERIFIED",
            "open_gates": ["independent live trajectory"],
            "unknown_or_open_world_boundary": "Future model/tool/product changes may expose unmodeled failure classes.",
            "global_flawlessness_claimed": False,
        },
    }


def evaluate(run):
    return evaluate_meta_maintenance_run(
        run,
        load_json("SYSTEM_MAINTENANCE_POLICY.json"),
        owner_registry=load_json("OWNER_REGISTRY.json"),
    )


def test_valid_systemic_meta_maintenance_run_passes_structural_harness():
    result = evaluate(valid_systemic_run())
    assert result.status == "PASS", result.errors
    assert result.assurance_ceiling == "STRUCTURED_PROCESS_CONFORMANCE_ONLY"


def test_systemic_run_cannot_skip_learning_scout():
    run = valid_systemic_run()
    run["learning_scout"] = {"disposition": "NOT_REQUIRED_WITH_REASON", "reason": "I already know the answer."}
    result = evaluate(run)
    assert result.status == "FAIL"
    assert "systemic_change_requires_learning_scout" in result.errors


def test_user_proposed_mechanism_does_not_remove_alternative_requirement():
    run = valid_systemic_run()
    run["alternatives"] = [{"id": "user-proposal", "decision": "ACCEPTED", "rationale": "User suggested it."}]
    result = evaluate(run)
    assert "at_least_two_alternatives_required" in result.errors


def test_shared_change_requires_registry_complete_propagation_when_claimed_global():
    run = valid_systemic_run()
    run["propagation"]["impacted_business_owners"] = ["FINANCIAL_WRITING_AGENT_RUNTIME"]
    result = evaluate(run)
    assert "all_business_owner_propagation_must_match_registry" in result.errors


def test_instruction_surface_review_is_mandatory_even_when_no_change_is_correct():
    run = valid_systemic_run()
    run.pop("instruction_surface")
    result = evaluate(run)
    assert "instruction_surface_decision_required" in result.errors
    assert "instruction_surface_reason_required" in result.errors


def test_complexity_budget_cannot_be_skipped_by_reliability_fix():
    run = valid_systemic_run()
    run["complexity_efficiency"].pop("steady_state_latency_effect")
    result = evaluate(run)
    assert any(error.startswith("complexity_efficiency_fields_missing:") for error in result.errors)


def test_new_authority_surface_requires_admission_gate():
    run = valid_systemic_run()
    run["complexity_efficiency"]["new_authority_surfaces"] = 1
    run["authority_surface_admission"] = "NOT_RUN"
    result = evaluate(run)
    assert "new_authority_surface_requires_admission_gate" in result.errors


def test_global_flawlessness_claim_is_rejected():
    run = valid_systemic_run()
    run["closure"]["global_flawlessness_claimed"] = True
    result = evaluate(run)
    assert "global_flawlessness_claim_forbidden" in result.errors


def test_local_mechanical_bug_can_skip_external_scout_with_reason():
    run = valid_systemic_run()
    run["scope"] = "LOCAL"
    run["learning_scout"] = {
        "disposition": "NOT_REQUIRED_WITH_REASON",
        "reason": "Exact deterministic schema typo with an existing regression oracle.",
    }
    run["propagation"] = {
        "classification": "OWNER_LOCAL_BUSINESS_RULE",
        "scope": "NOT_APPLICABLE_WITH_REASON",
        "reason": "Local fixture only.",
        "impacted_business_owners": [],
        "mechanism": "local patch",
        "stale_override_scan": "NOT_APPLICABLE",
    }
    run["validation"]["cross_surface_or_fault_audit"] = "NOT_REQUIRED"
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_recorded_meta_maintenance_run_is_structurally_conformant_and_registry_complete():
    run = load_json(META_RUN_REF)
    result = evaluate(run)
    assert result.status == "PASS", result.errors
    assert result.assurance_ceiling == "STRUCTURED_PROCESS_CONFORMANCE_ONLY"
    expected_owners = {
        item["name"]
        for item in load_json("OWNER_REGISTRY.json")["owners"]
        if item.get("owner_kind") == "BUSINESS"
    }
    assert set(run["propagation"]["impacted_business_owners"]) == expected_owners


def test_meta_governance_hardening_cannot_close_with_stale_or_missing_run_record():
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    stage = str(manifest.get("current_stage", ""))
    if "META_MAINTENANCE_GOVERNANCE_HARDENING_IN_PROGRESS" in stage:
        assert manifest.get("meta_maintenance_harness_version") == "1.0-candidate"
        return

    assert manifest.get("meta_maintenance_harness_version") == "1.0"
    assert manifest.get("latest_meta_maintenance_run_ref") == META_RUN_REF
    run = load_json(META_RUN_REF)
    assert run.get("target_manifest_version") == manifest.get("manifest_version")
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_entrypoint_tracks_current_methodology_receipt_contract_and_does_not_retain_1_2():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    adapter = load_json("OWNER_ADAPTER_CONTRACT.json")
    current = adapter["methodology_composition"]["operational_profile_run_contract_version"]
    assert f"receipt-contract-{current}" in entrypoint
    assert f"Under receipt contract {current}" in entrypoint
    if current != "1.2":
        assert "receipt-contract-1.2" not in entrypoint
        assert "Under receipt contract 1.2" not in entrypoint
