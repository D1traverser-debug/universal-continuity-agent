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
    assert "USER_CHALLENGES_MAINTENANCE_METHOD_OR_GLOBAL_COMPLETENESS" in policy["triggers"]
    assert "REPEATED_OWNER_FAILURE_OR_REGRESSION" in policy["triggers"]
    assert "PREMATURE_SOLUTION_CANONICALIZATION_OR_USER_CORRECTION_SIGNAL" in policy["triggers"]

    autonomy = policy["default_autonomy"]
    assert autonomy["diagnose_root_cause"] is True
    assert autonomy["assess_reliability_guard_before_feature_expansion"] is True
    assert autonomy["classify_user_feedback_before_adoption"] is True
    assert autonomy["separate_user_goal_from_user_proposed_mechanism"] is True
    assert autonomy["challenge_user_and_assistant_initial_solution"] is True
    assert autonomy["compare_credible_alternatives_for_nontrivial_design"] is True
    assert autonomy["seek_counterexample_or_failure_mode_before_adoption"] is True
    assert autonomy["run_meta_maintenance_outline_before_nontrivial_patch"] is True
    assert autonomy["assess_learning_scout_need"] is True
    assert autonomy["assess_instruction_surface_impact"] is True
    assert autonomy["assess_cross_subsystem_inheritance_and_propagation"] is True
    assert autonomy["assess_complexity_and_efficiency_budget"] is True
    assert autonomy["perform_global_claim_scope_check"] is True
    assert autonomy["apply_smallest_safe_fix"] is True
    assert autonomy["prefer_modify_existing_authority_over_new_parallel_surface"] is True
    assert autonomy["add_or_update_regression_guard_when_testable"] is True
    assert autonomy["run_or_observe_relevant_ci"] is True
    assert autonomy["update_authoritative_status_and_handoff"] is True
    assert autonomy["record_change_and_remaining_risk"] is True
    assert autonomy["reread_authority_before_claiming_committed"] is True
    assert autonomy["ask_user_to_manage_internal_migration_or_recordkeeping"] is False
    assert autonomy["wait_for_user_to_notice_related_internal_followups"] is False
    assert autonomy["claim_global_perfection_or_all_future_failures_preconsidered"] is False


def test_meta_maintenance_outline_is_default_nontrivial_governance_path():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    outline = policy["meta_maintenance_outline"]
    stages = outline["stages"]

    assert stages[0] == "M0_INTAKE_AND_SIGNAL_CLASSIFICATION"
    assert "M2_FULL_SYSTEM_IMPACT_MAP" in stages
    assert "M3_LEARNING_AND_EVIDENCE_SCOUT" in stages
    assert "M5_INSTRUCTION_AND_CONTROL_SURFACE_DECISION" in stages
    assert "M6_DESIGN_AND_COMPLEXITY_EFFICIENCY_BUDGET" in stages
    assert "M9_CROSS_SUBSYSTEM_INHERITANCE_AND_PROPAGATION" in stages
    assert "M10_SECOND_ORDER_REVIEW_AND_GLOBAL_CLAIM_CALIBRATION" in stages
    assert stages[-1] == "M11_DURABLE_LEARNING_AND_CHECKPOINT"
    questions = "\n".join(outline["mandatory_questions"])
    assert "GPT/account/startup instructions" in questions
    assert "child owners/subsystems inherit" in questions
    assert "startup context, tool calls, latency" in questions


def test_user_correction_is_signal_not_direct_implementation_order():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    feedback = policy["user_feedback_assimilation"]

    assert feedback["material_correction_triggers_system_impact_review_after_first_occurrence"] is True
    assert feedback["repetition_required_before_systemic_review"] is False
    assert feedback["goal_or_constraint_is_high_authority"] is True
    assert feedback["proposed_mechanism_is_canonical_by_default"] is False
    assert feedback["testable_correction_should_feed_regression_or_eval"] is True
    assert feedback["do_not_require_user_to_restate_accepted_requirement"] is True
    assert "PROPOSED_MECHANISM" in feedback["classify_each_material_correction_as"]
    assert "COUNTEREXAMPLE_OR_FAILURE_REPORT" in feedback["classify_each_material_correction_as"]


def test_instruction_surface_review_prevents_prompt_patching_every_defect():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    review = policy["instruction_surface_review"]

    assert review["required_for_systemic_behavior_gap"] is True
    assert review["prompt_or_account_instruction_change_is_default_fix"] is False
    assert review["repository_write_proves_account_instruction_propagated"] is False
    assert review["no_instruction_change_requires_reason"] is True
    assert "RUNTIME_OR_SCHEMA" in review["root_cause_layers"]
    assert "ACCOUNT_OR_PRODUCT_INSTRUCTION" in review["root_cause_layers"]
    assert any("runtime/schema/test" in item for item in review["do_not_change_instruction_when"])


def test_learning_inheritance_and_efficiency_are_first_class_review_dimensions():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")

    learning = policy["learning_evolution_review"]
    assert learning["systemic_or_architecture_change_default"] == "SCOUT_REQUIRED"
    assert learning["citation_without_behavioral_integration_is_learning"] is False
    assert learning["accepted_user_corrections_feed_future_eval_corpus"] is True

    inheritance = policy["cross_subsystem_inheritance_review"]
    assert inheritance["required_for_shared_control_plane_change"] is True
    assert inheritance["kernel_or_profile_change_requires_impacted_owner_derivation_from_registry"] is True
    assert inheritance["shared_invariant_should_propagate_by_contract_profile_or_runtime_not_copied_prose"] is True
    assert inheritance["check_for_stale_owner_override_or_shadow_logic"] is True

    budget = policy["complexity_efficiency_budget"]
    assert budget["required_for_nontrivial_control_plane_change"] is True
    assert budget["prefer_deletion_or_consolidation_over_addition"] is True
    assert budget["increase_in_startup_preload_requires_explicit_justification"] is True
    assert budget["full_global_audit_on_every_business_turn"] is False
    assert "steady_state_latency" in budget["dimensions"]


def test_closure_claims_must_not_assert_global_perfection():
    policy = load_json(ROOT / "SYSTEM_MAINTENANCE_POLICY.json")
    limits = policy["closure_claim_limits"]

    assert limits["claim_global_system_is_error_free"] is False
    assert limits["claim_all_future_problem_classes_have_been_preconsidered"] is False
    assert limits["claim_no_inappropriate_mechanism_remains_without_evidence"] is False
    assert "unknown/open-world boundary" in limits["required_closure_fields"]
    assert policy["scope_boundaries"]["do_not_claim_global_flawlessness"] is True
    assert policy["failure_semantics"]["global_perfection_claim"] == "CLAIM_SCOPE_INVALID"


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
    assert "a single material user correction exposes a plausible shared control-plane failure class" in guard["incident_triggers"]
    assert "the user repeatedly has to correct the system for treating the user's suggested mechanism or analogy as canonical architecture" in guard["incident_triggers"]
    assert "PERSIST_INCIDENT_OR_FAILURE_EVIDENCE" in guard["required_response"]
    assert "SEPARATE_GOAL_FROM_PROPOSED_MECHANISM" in guard["required_response"]
    assert "COMPARE_ALTERNATIVES_AND_FALSIFY_FIRST_IDEA" in guard["required_response"]
    assert "ADD_OR_UPDATE_REGRESSION_OR_EVAL" in guard["required_response"]
    assert "VERIFY_CROSS_SUBSYSTEM_PROPAGATION" in guard["required_response"]
    assert guard["affected_owner_non_reliability_expansion"] == "FREEZE_WHILE_CORE_RELIABILITY_IS_UNHEALTHY"
    assert guard["freeze_scope"] == "AFFECTED_OWNER_OR_CAPABILITY_ONLY"
    assert guard["unrelated_healthy_owners_are_frozen"] is False
    assert guard["user_manages_incident_backlog"] is False
    assert guard["chat_only_apology_or_reminder_counts_as_fix"] is False
    assert "ASSESS_RELIABILITY_GUARD" in policy["maintenance_loop"]
    assert "CHALLENGE_INITIAL_SOLUTION_CANDIDATES" in policy["maintenance_loop"]
    assert "RUN_INSTRUCTION_SURFACE_IMPACT_REVIEW" in policy["maintenance_loop"]
    assert "ASSESS_COMPLEXITY_AND_EFFICIENCY_BUDGET" in policy["maintenance_loop"]
    assert "RUN_SECOND_ORDER_CHALLENGE_AND_CLAIM_CALIBRATION" in policy["maintenance_loop"]


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
    assert "**Exact proof binding:**" in learning
    assert "**Obligation derivation:**" in learning
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
    assert "not bound to the exact claim/action" in learning


def test_learning_policy_distills_reusable_failure_patterns_not_owner_business_rules():
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "silent applicable-item omission / negative-space blind spot" in learning
    assert "declaration-to-operation gap" in learning
    assert "self-attestation inflation" in learning
    assert "CI-to-product overclaim" in learning
    assert "single-example overfit" in learning
    assert "post-hoc receipt illusion" in learning
    assert "unbound-proof replay / wrong-subject evidence" in learning
    assert "shadow obligation list / configured-obligation drift" in learning
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
    assert boundaries["do_not_treat_autonomous_maintenance_as_permission_to_skip_user_signal_analysis"] is True
    assert boundaries["do_not_use_prompt_growth_to_mask_missing_runtime_or_eval_enforcement"] is True


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
        "user_signal_classification",
        "system_impact_map",
        "learning_scout_disposition",
        "instruction_surface_disposition",
        "inheritance_propagation_effect",
        "complexity_efficiency_effect",
        "changed_authority_surfaces",
        "validation_or_ci_result",
        "behavioral_effect",
        "remaining_risks_or_external_dependencies",
        "assurance_ceiling",
        "current_stage",
        "next_action",
    }.issubset(required_fields)
