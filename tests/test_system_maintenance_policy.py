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
    assert "REPEATED_OWNER_FAILURE_OR_REGRESSION" in policy["triggers"]
    assert "PREMATURE_SOLUTION_CANONICALIZATION_OR_USER_CORRECTION_SIGNAL" in policy["triggers"]

    autonomy = policy["default_autonomy"]
    assert autonomy["diagnose_root_cause"] is True
    assert autonomy["assess_reliability_guard_before_feature_expansion"] is True
    assert autonomy["separate_user_goal_from_user_proposed_mechanism"] is True
    assert autonomy["challenge_user_and_assistant_initial_solution"] is True
    assert autonomy["compare_credible_alternatives_for_nontrivial_design"] is True
    assert autonomy["seek_counterexample_or_failure_mode_before_adoption"] is True
    assert autonomy["apply_smallest_safe_fix"] is True
    assert autonomy["prefer_modify_existing_authority_over_new_parallel_surface"] is True
    assert autonomy["add_or_update_regression_guard_when_testable"] is True
    assert autonomy["run_or_observe_relevant_ci"] is True
    assert autonomy["update_authoritative_status_and_handoff"] is True
    assert autonomy["record_change_and_remaining_risk"] is True
    assert autonomy["reread_authority_before_claiming_committed"] is True
    assert autonomy["ask_user_to_manage_internal_migration_or_recordkeeping"] is False
    assert autonomy["wait_for_user_to_notice_related_internal_followups"] is False


def test_new_authority_surface_requires_architecture_admission_gate():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    gate = policy["authority_surface_admission_gate"]

    assert "CREATE_NEW_ROOT_POLICY" in gate["applies_before"]
    assert "CAN_EXISTING_AUTHORITY_OWN_THIS_WITHOUT_AMBIGUITY" in gate["required_checks"]
    assert "WOULD_THIS_DUPLICATE_OR_SPLIT_AN_EXISTING_INVARIANT" in gate["required_checks"]
    assert gate["default_decision"] == "REJECT_NEW_SURFACE_IF_EXISTING_AUTHORITY_CAN_OWN_IT"
    assert "Consolidate into the existing authority" in gate["failed_admission_behavior"]
    assert policy["failure_semantics"]["new_authority_surface_without_admission"] == "REJECT_AND_CONSOLIDATE"


def test_repeated_owner_failure_activates_scoped_reliability_guard():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    guard = policy["reliability_guard"]

    assert "same defect class materially recurs after an accepted fix" in guard["incident_triggers"]
    assert "the user repeatedly has to restate the same durable requirement" in guard["incident_triggers"]
    assert "the user repeatedly has to correct the system for treating the user's suggested mechanism or analogy as canonical architecture" in guard["incident_triggers"]
    assert "PERSIST_INCIDENT_OR_FAILURE_EVIDENCE" in guard["required_response"]
    assert "SEPARATE_GOAL_FROM_PROPOSED_MECHANISM" in guard["required_response"]
    assert "COMPARE_ALTERNATIVES_AND_FALSIFY_FIRST_IDEA" in guard["required_response"]
    assert "ADD_OR_UPDATE_REGRESSION_OR_EVAL" in guard["required_response"]
    assert guard["affected_owner_non_reliability_expansion"] == "FREEZE_WHILE_CORE_RELIABILITY_IS_UNHEALTHY"
    assert guard["freeze_scope"] == "AFFECTED_OWNER_OR_CAPABILITY_ONLY"
    assert guard["unrelated_healthy_owners_are_frozen"] is False
    assert guard["user_manages_incident_backlog"] is False
    assert guard["chat_only_apology_or_reminder_counts_as_fix"] is False
    assert "ASSESS_RELIABILITY_GUARD" in policy["maintenance_loop"]
    assert "CHALLENGE_INITIAL_SOLUTION_CANDIDATES" in policy["maintenance_loop"]


def test_learning_policy_requires_epistemic_independence_before_nontrivial_adoption():
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")
    adapter = load_json(ROOT / "OWNER_ADAPTER_CONTRACT.json")
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")

    assert "Epistemic independence and candidate-adoption gate" in learning
    assert "not automatically the authority for an implementation pattern" in learning
    assert "assistant's own first idea" in learning
    assert "generate or retrieve at least one credible alternative" in learning
    assert "actively search for a counterexample" in learning
    assert "an analogy never establishes architecture by itself" in learning

    hygiene = adapter["operational_hygiene_and_learning"]
    assert hygiene["solution_proposal_from_user_assistant_or_other_agent_is_candidate_not_authority"] is True
    assert hygiene["user_goal_and_constraint_must_be_separated_from_user_proposed_mechanism"] is True
    assert hygiene["nontrivial_evolution_candidate_requires_alternative_comparison_and_failure_mode_search"] is True
    assert hygiene["domain_specific_evolution_may_specialize_method_but_must_preserve_cross_agent_evidence_reliability_and_authority_invariants"] is True
    assert hygiene["owner_override_may_replace_method_but_not_bypass_required_evidence_or_owner_boundaries"] is True

    assert policy["scope_boundaries"]["do_not_treat_user_solution_proposal_as_architecture_authority_by_default"] is True
    assert policy["scope_boundaries"]["do_not_treat_assistant_first_idea_as_privileged_candidate"] is True
    assert policy["failure_semantics"]["nontrivial_solution_adopted_without_independent_candidate_critique"] == "EVOLUTION_GATE_NOT_SATISFIED"


def test_learning_policy_requires_second_order_challenge_before_nontrivial_closure():
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "Second-order challenge / closure calibration" in learning
    assert "challenge the **accepted fix itself**" in learning
    assert "**Evidence ceiling:**" in learning
    assert "**Negative space:**" in learning
    assert "**Self-reference:**" in learning
    assert "**Post-hoc provenance:**" in learning
    assert "**Test realism:**" in learning
    assert "**Closure boundary:**" in learning
    assert "### Evidence assurance ladder" in learning
    assert "**DECLARED**" in learning
    assert "**WIRED**" in learning
    assert "**REGRESSION_VERIFIED**" in learning
    assert "**ACTION_LEVEL_SELF_ATTESTED**" in learning
    assert "**ACTION_LEVEL_INDEPENDENTLY_VERIFIED**" in learning
    assert "**LIVE_OUTCOME_VERIFIED**" in learning
    assert "A CI PASS cannot be promoted directly to action-level execution proof" in learning
    assert "structured same-session receipt cannot be promoted to independent attestation" in learning


def test_learning_policy_distills_reusable_failure_patterns_not_owner_business_rules():
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "silent applicable-item omission / negative-space blind spot" in learning
    assert "declaration-to-operation gap" in learning
    assert "self-attestation inflation" in learning
    assert "CI-to-product overclaim" in learning
    assert "single-example overfit" in learning
    assert "post-hoc receipt illusion" in learning
    assert "cache/authority circularity" in learning
    assert "patch-without-distillation" in learning
    assert "Do not copy the triggering owner's business rule into Universal" in learning


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
