import json
from pathlib import Path

from runtime.meta_maintenance import CURRENT_META_MAINTENANCE_SCHEMA, evaluate_meta_maintenance_run


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def latest_meta_run_ref() -> str:
    return load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")["latest_meta_maintenance_run_ref"]


def valid_systemic_run():
    owners = [
        item["name"]
        for item in load_json("OWNER_REGISTRY.json")["owners"]
        if item.get("owner_kind") == "BUSINESS"
    ]
    return {
        "schema_version": CURRENT_META_MAINTENANCE_SCHEMA,
        "run_id": "meta-test-1",
        "scope": "FULL_CONTROL_PLANE",
        "trigger": "USER_CHALLENGES_MAINTENANCE_METHOD_OR_GLOBAL_COMPLETENESS",
        "user_signal": {
            "classifications": ["GOAL_OR_CONSTRAINT", "COUNTEREXAMPLE_OR_FAILURE_REPORT", "PROPOSED_MECHANISM"],
            "goal_or_constraint": "Systemic maintenance must learn, challenge, propagate and validate without repeated user reminders.",
            "proposed_mechanism": "Maybe add an upper system or agent.",
            "counterexample": "A prior green maintenance pass can still omit a required review dimension.",
        },
        "authority_inspection": {
            "refs": ["ENTRYPOINT.md", "SYSTEM_MAINTENANCE_POLICY.json", "CONTINUOUS_LEARNING_POLICY.md"]
        },
        "failure_model": {
            "root_cause_layers": ["REPOSITORY_POLICY", "TEST_OR_EVAL", "EVIDENCE_OR_PROPAGATION"],
            "failure_classes": ["repair-first-governance", "self-review-without-process-verifier"],
            "system_impact_map": ["maintenance", "learning", "startup", "owners"],
            "falsification_checks": [
                "Try a structurally incomplete systemic run and require fail-closed behavior.",
                "Try a no-change conclusion and verify the harness does not force a mutation.",
            ],
        },
        "failure_history": {
            "searched_failure_classes": ["repair-first-governance", "self-review-without-process-verifier"],
            "matched_prior_refs": [],
            "recurrence_status": "FIRST_OBSERVED",
            "current_abstraction_level": "FAILURE_CLASS",
            "prior_repair_abstraction_level": None,
            "escalation_decision": "HOLD_FIRST_OBSERVATION",
            "escalation_reason": "No prior accepted repair for this exact classified failure set is assumed by the fixture.",
            "class_level_prevention": "Encode the reusable failure class in the existing deterministic maintenance harness.",
            "instance_fix": "Repair the concrete maintenance run and its affected authority surfaces.",
            "considered_or_reused_mechanism_refs": [
                "SYSTEM_MAINTENANCE_POLICY.json",
                "runtime/meta_maintenance.py",
            ],
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
        "capability_reuse": {
            "decision": "EXTEND_EXISTING",
            "inspected_existing_capabilities": [
                "SYSTEM_MAINTENANCE_POLICY meta-maintenance outline",
                "runtime/meta_maintenance.py structural harness",
            ],
            "rejected_existing_candidates": [],
            "rationale": "The existing meta-maintenance path can own the behavior without a new root agent or policy.",
        },
        "decision_frontier": {
            "verified_facts": [
                "Current startup routing already loads repository maintenance authority.",
                "The existing meta harness can enforce additional structured gates.",
            ],
            "unresolved_facts": [],
            "user_decisions_required": [],
            "autonomous_next_steps": [
                "Extend the current harness rather than ask the user to choose internal architecture details.",
            ],
            "facts_resolved_before_user_decision": True,
        },
        "alternatives": [
            {"id": "policy-only", "decision": "REJECTED", "rationale": "Self-enforcement remains weak."},
            {"id": "deterministic-harness", "decision": "ACCEPTED", "rationale": "Adds process verification without a fake agent identity."},
        ],
        "architecture_payoff": {
            "current_failure_cost": "Repeated operator correction and incomplete systemic reviews.",
            "change_cost": "A compatible meta-harness schema increment and bounded tests.",
            "expected_payoff": "Fewer unnecessary new surfaces and fewer user questions for retrievable facts.",
            "deletion_or_simplification_considered": True,
            "deletion_or_simplification_result": "Extend the existing harness; do not create a new supervisory agent or root policy.",
            "net_complexity_decision": "NET_NEUTRAL",
        },
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
            "decision": "CHANGE_APPLIED",
            "inspected_paths": ["SYSTEM_MAINTENANCE_POLICY.json", "runtime/meta_maintenance.py"],
            "changed_paths": ["SYSTEM_MAINTENANCE_POLICY.json", "runtime/meta_maintenance.py"],
            "superseded_or_demoted_surfaces": [],
        },
        "validation": {
            "regression_or_eval_refs": ["pytest://test_meta_maintenance"],
            "second_order_challenge": "PASS",
            "second_order_findings": [
                "Structural conformance does not establish semantic independence.",
                "No-change conclusions must remain legal so the harness does not reward needless mutation.",
            ],
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


def test_v1_3_failure_report_requires_counterexample():
    run = valid_systemic_run()
    run["user_signal"].pop("counterexample")
    result = evaluate(run)
    assert "counterexample_required_when_failure_report_classified" in result.errors


def test_v1_3_systemic_run_requires_falsification_checks():
    run = valid_systemic_run()
    run["failure_model"].pop("falsification_checks")
    result = evaluate(run)
    assert "systemic_falsification_checks_required" in result.errors


def test_v1_3_learning_source_disposition_is_bounded():
    run = valid_systemic_run()
    run["learning_scout"]["sources"][0]["disposition"] = "TRUST_ME"
    result = evaluate(run)
    assert "learning_source_0_disposition_invalid" in result.errors


def test_systemic_run_requires_failure_history_search():
    run = valid_systemic_run()
    run.pop("failure_history")
    result = evaluate(run)
    assert "failure_history_search_required" in result.errors
    assert "recurrence_status_required" in result.errors
    assert "current_abstraction_level_required" in result.errors


def test_failure_history_search_must_cover_every_classified_failure():
    run = valid_systemic_run()
    run["failure_history"]["searched_failure_classes"] = ["repair-first-governance"]
    result = evaluate(run)
    assert "failure_history_must_cover_all_failure_classes" in result.errors


def test_known_failure_class_requires_prior_incident_refs():
    run = valid_systemic_run()
    run["failure_history"].update(
        {
            "recurrence_status": "KNOWN_CLASS_NEW_INSTANCE",
            "matched_prior_refs": [],
            "escalation_decision": "ESCALATE",
            "current_abstraction_level": "OWNER_OR_COMPONENT_MECHANISM",
        }
    )
    result = evaluate(run)
    assert "known_failure_class_requires_prior_refs" in result.errors


def test_recurrence_after_fix_must_move_up_the_abstraction_ladder():
    run = valid_systemic_run()
    run["failure_history"].update(
        {
            "recurrence_status": "RECURRED_AFTER_FIX",
            "matched_prior_refs": ["audits/prior-repair.json"],
            "prior_repair_abstraction_level": "OWNER_OR_COMPONENT_MECHANISM",
            "current_abstraction_level": "OWNER_OR_COMPONENT_MECHANISM",
            "escalation_decision": "ESCALATE",
            "escalation_reason": "The same class recurred after the owner-level repair.",
        }
    )
    result = evaluate(run)
    assert "recurring_failure_must_escalate_abstraction_level" in result.errors


def test_recurrence_after_fix_can_close_structurally_only_after_escalation_and_return_to_instance():
    run = valid_systemic_run()
    run["failure_history"].update(
        {
            "recurrence_status": "RECURRED_AFTER_FIX",
            "matched_prior_refs": ["audits/prior-repair.json"],
            "prior_repair_abstraction_level": "OWNER_OR_COMPONENT_MECHANISM",
            "current_abstraction_level": "SYSTEM_ARCHITECTURE",
            "escalation_decision": "ESCALATE",
            "escalation_reason": "The owner-level mechanism already failed, so the system architecture must be challenged before another local patch.",
            "class_level_prevention": "Repair the shared architecture condition that permitted the class to recur.",
            "instance_fix": "Then repair and revalidate the triggering concrete defect under the new architecture.",
        }
    )
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_meta_method_recurrence_requires_explicit_max_level_redesign():
    run = valid_systemic_run()
    run["failure_history"].update(
        {
            "recurrence_status": "RECURRED_AFTER_FIX",
            "matched_prior_refs": ["audits/prior-meta-method-repair.json"],
            "prior_repair_abstraction_level": "META_METHOD",
            "current_abstraction_level": "META_METHOD",
            "escalation_decision": "ESCALATE",
        }
    )
    result = evaluate(run)
    assert "meta_method_recurrence_requires_max_level_redesign" in result.errors


def test_systemic_run_requires_reuse_before_build_scan():
    run = valid_systemic_run()
    run.pop("capability_reuse")
    result = evaluate(run)
    assert "capability_reuse_decision_required" in result.errors
    assert "capability_reuse_rationale_required" in result.errors


def test_build_new_requires_rejected_existing_candidates():
    run = valid_systemic_run()
    run["capability_reuse"] = {
        "decision": "BUILD_NEW",
        "inspected_existing_capabilities": ["existing-harness"],
        "rejected_existing_candidates": [],
        "rationale": "Need a new mechanism.",
    }
    result = evaluate(run)
    assert "build_new_requires_rejected_existing_candidates" in result.errors


def test_systemic_run_requires_facts_decisions_frontier():
    run = valid_systemic_run()
    run.pop("decision_frontier")
    result = evaluate(run)
    assert "decision_frontier_verified_facts_required" in result.errors
    assert "decision_frontier_autonomous_next_steps_required" in result.errors
    assert "decision_frontier_requires_fact_resolution_before_user_decision" in result.errors


def test_decision_frontier_must_not_skip_fact_resolution():
    run = valid_systemic_run()
    run["decision_frontier"]["facts_resolved_before_user_decision"] = False
    result = evaluate(run)
    assert "decision_frontier_requires_fact_resolution_before_user_decision" in result.errors


def test_systemic_run_requires_architecture_payoff_and_deletion_test():
    run = valid_systemic_run()
    run.pop("architecture_payoff")
    result = evaluate(run)
    assert "architecture_payoff_deletion_or_simplification_must_be_considered" in result.errors
    assert "architecture_payoff_net_complexity_decision_required" in result.errors


def test_more_complex_architecture_requires_justification():
    run = valid_systemic_run()
    run["architecture_payoff"]["net_complexity_decision"] = "NET_MORE_COMPLEX_WITH_JUSTIFICATION"
    result = evaluate(run)
    assert "net_more_complex_requires_justification" in result.errors


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


def test_no_change_systemic_audit_can_close_without_inventing_a_mutation():
    run = valid_systemic_run()
    run["implementation"] = {
        "decision": "NO_CHANGE_REQUIRED",
        "inspected_paths": ["ENTRYPOINT.md", "SYSTEM_MAINTENANCE_POLICY.json", "runtime/system_audit.py"],
        "changed_paths": [],
        "no_change_reason": "The inspected mechanism already satisfies the invariant and the falsification checks did not expose a repairable defect.",
        "superseded_or_demoted_surfaces": [],
    }
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_no_change_requires_reason_and_cannot_hide_changed_paths():
    run = valid_systemic_run()
    run["implementation"] = {
        "decision": "NO_CHANGE_REQUIRED",
        "inspected_paths": ["ENTRYPOINT.md"],
        "changed_paths": ["ENTRYPOINT.md"],
        "superseded_or_demoted_surfaces": [],
    }
    result = evaluate(run)
    assert "no_change_required_forbids_changed_paths" in result.errors
    assert "no_change_required_reason_required" in result.errors


def test_systemic_second_order_challenge_requires_findings_not_only_pass_label():
    run = valid_systemic_run()
    run["validation"].pop("second_order_findings")
    result = evaluate(run)
    assert "systemic_second_order_findings_required" in result.errors


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
    run.pop("capability_reuse")
    run.pop("decision_frontier")
    run.pop("architecture_payoff")
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


def test_legacy_v1_2_run_remains_readable_as_historical_evidence():
    run = valid_systemic_run()
    run["schema_version"] = "1.2"
    run.pop("failure_history")
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_legacy_v1_1_run_remains_readable_as_historical_evidence():
    run = valid_systemic_run()
    run["schema_version"] = "1.1"
    run.pop("failure_history")
    run.pop("capability_reuse")
    run.pop("decision_frontier")
    run.pop("architecture_payoff")
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_legacy_v1_0_run_remains_readable_as_historical_evidence():
    run = valid_systemic_run()
    run["schema_version"] = "1.0"
    run["user_signal"].pop("counterexample")
    run["failure_model"].pop("falsification_checks")
    run.pop("failure_history")
    run.pop("capability_reuse")
    run.pop("decision_frontier")
    run.pop("architecture_payoff")
    run["implementation"].pop("decision")
    run["implementation"].pop("inspected_paths")
    run["validation"].pop("second_order_findings")
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_recorded_meta_maintenance_run_is_structurally_conformant_and_propagation_consistent():
    run = load_json(latest_meta_run_ref())
    result = evaluate(run)
    assert result.status == "PASS", result.errors
    assert result.assurance_ceiling == "STRUCTURED_PROCESS_CONFORMANCE_ONLY"

    expected_owners = {
        item["name"]
        for item in load_json("OWNER_REGISTRY.json")["owners"]
        if item.get("owner_kind") == "BUSINESS"
    }
    propagation = run["propagation"]
    impacted = set(propagation["impacted_business_owners"])
    scope = propagation["scope"]

    if scope == "ALL_BUSINESS_OWNERS":
        assert impacted == expected_owners
    elif scope == "SUBSET_WITH_REASON":
        assert impacted
        assert impacted.issubset(expected_owners)
        assert propagation.get("reason")
    else:
        assert scope == "NOT_APPLICABLE_WITH_REASON"
        assert impacted == set()
        assert propagation.get("reason")


def test_meta_governance_hardening_cannot_close_with_stale_or_missing_run_record():
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    stage = str(manifest.get("current_stage", ""))
    if "SELF_AUDIT_IN_PROGRESS" in stage or "PRODUCTION_PROMOTION_IN_PROGRESS" in stage:
        return

    assert manifest.get("meta_maintenance_harness_version") == CURRENT_META_MAINTENANCE_SCHEMA
    run_ref = manifest.get("latest_meta_maintenance_run_ref")
    assert isinstance(run_ref, str) and run_ref
    run = load_json(run_ref)
    assert run.get("schema_version") == CURRENT_META_MAINTENANCE_SCHEMA
    assert run.get("target_manifest_version") == manifest.get("manifest_version")
    result = evaluate(run)
    assert result.status == "PASS", result.errors


def test_entrypoint_delegates_current_methodology_contract_without_version_duplication():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    adapter = load_json("OWNER_ADAPTER_CONTRACT.json")
    current = str(adapter["methodology_composition"]["operational_profile_run_contract_version"])

    assert "OWNER_ADAPTER_CONTRACT.json" in entrypoint
    assert "runtime/methodology_conformance.py" in entrypoint
    assert f"receipt-contract-{current}" not in entrypoint
    assert f"Under receipt contract {current}" not in entrypoint
    assert "apply the current receipt/action-binding contract there rather than copying it into this bootstrap" in entrypoint