from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


CURRENT_META_MAINTENANCE_SCHEMA = "1.3"
SUPPORTED_META_MAINTENANCE_SCHEMAS = {"1.0", "1.1", "1.2", CURRENT_META_MAINTENANCE_SCHEMA}
SYSTEMIC_SCOPES = {"SYSTEMIC", "ARCHITECTURE", "FULL_CONTROL_PLANE"}
USER_SIGNAL_CLASSES = {
    "GOAL_OR_CONSTRAINT",
    "COUNTEREXAMPLE_OR_FAILURE_REPORT",
    "PROPOSED_MECHANISM",
    "STYLE_OR_UX_PREFERENCE",
    "PRODUCT_OR_ACCOUNT_INSTRUCTION_REQUEST",
}
LEARNING_DISPOSITIONS = {"SCOUT_DONE", "NOT_REQUIRED_WITH_REASON"}
LEARNING_SOURCE_DISPOSITIONS = {"ADOPT", "NARROW", "REJECT"}
INSTRUCTION_DECISIONS = {"CHANGE", "NO_CHANGE", "EXTERNAL_ACTION_REQUIRED"}
PROPAGATION_SCOPES = {"ALL_BUSINESS_OWNERS", "SUBSET_WITH_REASON", "NOT_APPLICABLE_WITH_REASON"}
IMPLEMENTATION_DECISIONS = {"CHANGE_APPLIED", "NO_CHANGE_REQUIRED"}
CAPABILITY_REUSE_DECISIONS = {"REUSE_EXISTING", "EXTEND_EXISTING", "BUILD_NEW", "NOT_APPLICABLE_WITH_REASON"}
NET_COMPLEXITY_DECISIONS = {"NET_SIMPLER", "NET_NEUTRAL", "NET_MORE_COMPLEX_WITH_JUSTIFICATION"}
# Executable mirrors of SYSTEM_MAINTENANCE_POLICY.failure_abstraction_escalation.
# Current-schema evaluation fails closed if the policy and runtime mirrors drift.
RECURRENCE_STATUSES = {
    "FIRST_OBSERVED",
    "KNOWN_CLASS_NEW_INSTANCE",
    "RECURRED_AFTER_FIX",
    "CROSS_OWNER_RECURRENT",
}
ABSTRACTION_LEVELS = (
    "INSTANCE",
    "FAILURE_CLASS",
    "OWNER_OR_COMPONENT_MECHANISM",
    "SYSTEM_ARCHITECTURE",
    "META_METHOD",
)
ABSTRACTION_INDEX = {name: index for index, name in enumerate(ABSTRACTION_LEVELS)}
ESCALATION_DECISIONS = {
    "HOLD_FIRST_OBSERVATION",
    "ESCALATE",
    "MAX_LEVEL_REDESIGN",
}
ASSURANCE_ORDER = {
    "DECLARED": 1,
    "WIRED": 2,
    "REGRESSION_VERIFIED": 3,
    "ACTION_LEVEL_SELF_ATTESTED": 4,
    "ACTION_LEVEL_INDEPENDENTLY_VERIFIED": 5,
    "LIVE_OUTCOME_VERIFIED": 6,
}


@dataclass(frozen=True)
class MetaMaintenanceResult:
    status: str
    errors: tuple[str, ...]
    checked_sections: tuple[str, ...]
    assurance_ceiling: str


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty(item) for item in value)


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty(item) for item in value)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _business_owner_names(owner_registry: Mapping[str, Any] | None) -> set[str]:
    if not owner_registry:
        return set()
    return {
        str(item.get("name"))
        for item in owner_registry.get("owners", [])
        if isinstance(item, Mapping) and item.get("owner_kind") == "BUSINESS" and _nonempty(item.get("name"))
    }


def evaluate_meta_maintenance_run(
    run: Mapping[str, Any] | None,
    policy: Mapping[str, Any],
    *,
    owner_registry: Mapping[str, Any] | None = None,
) -> MetaMaintenanceResult:
    """Validate maintenance-process completeness, not semantic correctness.

    A PASS means the run supplied the control/evidence fields required by the current
    maintenance policy. It does not prove that the diagnosis, research, alternative
    comparison, falsification, or final architecture judgment is semantically correct.
    That higher claim still requires independent trajectory/grader evidence when applicable.
    """

    errors: list[str] = []
    checked = (
        "signal",
        "authority_and_failure_model",
        "failure_history_and_abstraction_escalation",
        "learning",
        "capability_reuse",
        "decision_frontier",
        "alternatives_and_falsification",
        "architecture_payoff",
        "instruction_surface",
        "propagation",
        "complexity_efficiency",
        "implementation_and_validation",
        "closure",
    )
    if not isinstance(run, Mapping):
        return MetaMaintenanceResult("FAIL", ("maintenance_run_required",), checked, "STRUCTURED_PROCESS_CONFORMANCE_ONLY")

    schema_version = str(run.get("schema_version", ""))
    if schema_version not in SUPPORTED_META_MAINTENANCE_SCHEMAS:
        errors.append("unsupported_meta_maintenance_schema")
    current_schema = schema_version == CURRENT_META_MAINTENANCE_SCHEMA

    if current_schema:
        escalation_policy = _mapping(policy.get("failure_abstraction_escalation"))
        if set(escalation_policy.get("recurrence_statuses", [])) != RECURRENCE_STATUSES:
            errors.append("policy_runtime_recurrence_status_mismatch")
        if tuple(escalation_policy.get("abstraction_levels_low_to_high", [])) != ABSTRACTION_LEVELS:
            errors.append("policy_runtime_abstraction_ladder_mismatch")
        if set(escalation_policy.get("escalation_decisions", [])) != ESCALATION_DECISIONS:
            errors.append("policy_runtime_escalation_decision_mismatch")
        escalation_rules = _mapping(escalation_policy.get("rules"))
        required_true_rules = {
            "systemic_run_must_search_every_classified_failure_class",
            "known_or_recurrent_class_must_bind_prior_incident_or_repair_refs",
            "recurrence_after_accepted_fix_must_move_strictly_above_prior_repair_level",
            "meta_method_recurrence_requires_explicit_max_level_redesign",
            "high_level_repair_must_return_to_class_level_prevention",
            "high_level_repair_must_return_to_concrete_instance_fix",
            "historical_search_and_escalation_record_is_required_before_systemic_closure",
        }
        if any(escalation_rules.get(rule) is not True for rule in required_true_rules):
            errors.append("policy_runtime_abstraction_rules_not_enabled")
        if escalation_rules.get("same_or_lower_level_repeat_patch_is_allowed") is not False:
            errors.append("policy_runtime_same_level_repeat_patch_boundary_mismatch")

    if not _nonempty(run.get("run_id")):
        errors.append("run_id_required")
    scope = str(run.get("scope", "")).strip().upper()
    if scope not in {"LOCAL", *SYSTEMIC_SCOPES}:
        errors.append("unsupported_or_missing_scope")
    if not _nonempty(run.get("trigger")):
        errors.append("trigger_required")

    signal = _mapping(run.get("user_signal"))
    classes = signal.get("classifications")
    if not isinstance(classes, list) or not classes:
        errors.append("user_signal_classification_required")
    else:
        unknown = [item for item in classes if item not in USER_SIGNAL_CLASSES]
        if unknown:
            errors.append("unknown_user_signal_classification:" + ",".join(sorted(map(str, unknown))))
    if not _nonempty(signal.get("goal_or_constraint")):
        errors.append("user_goal_or_constraint_required")
    if "PROPOSED_MECHANISM" in (classes or []) and "proposed_mechanism" not in signal:
        errors.append("proposed_mechanism_field_required_when_classified")
    if schema_version in {"1.1", "1.2", "1.3"} and "COUNTEREXAMPLE_OR_FAILURE_REPORT" in (classes or []) and not _nonempty(signal.get("counterexample")):
        errors.append("counterexample_required_when_failure_report_classified")

    authority = _mapping(run.get("authority_inspection"))
    if not _nonempty_str_list(authority.get("refs")):
        errors.append("authority_refs_required")

    failure = _mapping(run.get("failure_model"))
    root_layers = failure.get("root_cause_layers")
    allowed_layers = set(_mapping(policy.get("instruction_surface_review")).get("root_cause_layers", []))
    if not isinstance(root_layers, list) or not root_layers:
        errors.append("root_cause_layers_required")
    elif allowed_layers and any(layer not in allowed_layers for layer in root_layers):
        errors.append("unknown_root_cause_layer")
    failure_classes = failure.get("failure_classes")
    if not _nonempty_str_list(failure_classes):
        errors.append("failure_classes_required")
        failure_classes = []
    if not isinstance(failure.get("system_impact_map"), list) or not failure.get("system_impact_map"):
        errors.append("system_impact_map_required")
    if schema_version in {"1.1", "1.2", "1.3"} and scope in SYSTEMIC_SCOPES and not _nonempty_str_list(failure.get("falsification_checks")):
        errors.append("systemic_falsification_checks_required")

    if current_schema and scope in SYSTEMIC_SCOPES:
        history = _mapping(run.get("failure_history"))
        searched_classes = history.get("searched_failure_classes")
        if not _nonempty_str_list(searched_classes):
            errors.append("failure_history_search_required")
            searched_classes = []
        elif not set(map(str, failure_classes)).issubset(set(map(str, searched_classes))):
            errors.append("failure_history_must_cover_all_failure_classes")

        matched_refs = history.get("matched_prior_refs")
        if not _string_list(matched_refs):
            errors.append("matched_prior_refs_must_be_string_list")
            matched_refs = []

        recurrence_status = str(history.get("recurrence_status", ""))
        if recurrence_status not in RECURRENCE_STATUSES:
            errors.append("recurrence_status_required")

        current_level = str(history.get("current_abstraction_level", ""))
        if current_level not in ABSTRACTION_INDEX:
            errors.append("current_abstraction_level_required")

        prior_level_raw = history.get("prior_repair_abstraction_level")
        prior_level = str(prior_level_raw) if prior_level_raw is not None else ""
        if prior_level and prior_level not in ABSTRACTION_INDEX:
            errors.append("prior_repair_abstraction_level_invalid")

        escalation_decision = str(history.get("escalation_decision", ""))
        if escalation_decision not in ESCALATION_DECISIONS:
            errors.append("escalation_decision_required")
        if not _nonempty(history.get("escalation_reason")):
            errors.append("escalation_reason_required")
        if not _nonempty(history.get("class_level_prevention")):
            errors.append("class_level_prevention_required")
        if not _nonempty(history.get("instance_fix")):
            errors.append("instance_fix_required")
        if not _nonempty_str_list(history.get("considered_or_reused_mechanism_refs")):
            errors.append("considered_or_reused_mechanism_refs_required")

        known_recurrence = recurrence_status in {
            "KNOWN_CLASS_NEW_INSTANCE",
            "RECURRED_AFTER_FIX",
            "CROSS_OWNER_RECURRENT",
        }
        if known_recurrence and not matched_refs:
            errors.append("known_failure_class_requires_prior_refs")

        repaired_recurrence = recurrence_status in {"RECURRED_AFTER_FIX", "CROSS_OWNER_RECURRENT"}
        if repaired_recurrence:
            if not prior_level:
                errors.append("recurrent_after_fix_requires_prior_repair_level")
            elif prior_level in ABSTRACTION_INDEX and current_level in ABSTRACTION_INDEX:
                if prior_level == "META_METHOD":
                    if current_level != "META_METHOD" or escalation_decision != "MAX_LEVEL_REDESIGN":
                        errors.append("meta_method_recurrence_requires_max_level_redesign")
                elif ABSTRACTION_INDEX[current_level] <= ABSTRACTION_INDEX[prior_level]:
                    errors.append("recurring_failure_must_escalate_abstraction_level")
                elif escalation_decision != "ESCALATE":
                    errors.append("recurrent_failure_requires_escalation_decision")
        elif recurrence_status == "FIRST_OBSERVED" and escalation_decision not in {"HOLD_FIRST_OBSERVATION", "ESCALATE"}:
            errors.append("first_observation_escalation_decision_invalid")

    learning = _mapping(run.get("learning_scout"))
    disposition = learning.get("disposition")
    if disposition not in LEARNING_DISPOSITIONS:
        errors.append("learning_scout_disposition_required")
    if scope in SYSTEMIC_SCOPES and disposition != "SCOUT_DONE":
        errors.append("systemic_change_requires_learning_scout")
    if disposition == "SCOUT_DONE":
        sources = learning.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append("learning_sources_required")
        else:
            for idx, source in enumerate(sources):
                source = _mapping(source)
                for field in ("ref", "observation", "disposition", "rationale"):
                    if not _nonempty(source.get(field)):
                        errors.append(f"learning_source_{idx}_{field}_required")
                if schema_version in {"1.1", "1.2", "1.3"} and source.get("disposition") not in LEARNING_SOURCE_DISPOSITIONS:
                    errors.append(f"learning_source_{idx}_disposition_invalid")
    elif disposition == "NOT_REQUIRED_WITH_REASON" and not _nonempty(learning.get("reason")):
        errors.append("learning_not_required_reason_required")

    if current_schema and scope in SYSTEMIC_SCOPES:
        reuse = _mapping(run.get("capability_reuse"))
        reuse_decision = reuse.get("decision")
        if reuse_decision not in CAPABILITY_REUSE_DECISIONS:
            errors.append("capability_reuse_decision_required")
        if not _nonempty(reuse.get("rationale")):
            errors.append("capability_reuse_rationale_required")
        inspected = reuse.get("inspected_existing_capabilities")
        if reuse_decision != "NOT_APPLICABLE_WITH_REASON" and not _nonempty_str_list(inspected):
            errors.append("capability_reuse_existing_capability_scan_required")
        if reuse_decision == "BUILD_NEW" and not _nonempty_str_list(reuse.get("rejected_existing_candidates")):
            errors.append("build_new_requires_rejected_existing_candidates")

        frontier = _mapping(run.get("decision_frontier"))
        if not _nonempty_str_list(frontier.get("verified_facts")):
            errors.append("decision_frontier_verified_facts_required")
        if not _string_list(frontier.get("unresolved_facts")):
            errors.append("decision_frontier_unresolved_facts_must_be_list")
        if not _string_list(frontier.get("user_decisions_required")):
            errors.append("decision_frontier_user_decisions_must_be_list")
        if not _nonempty_str_list(frontier.get("autonomous_next_steps")):
            errors.append("decision_frontier_autonomous_next_steps_required")
        if frontier.get("facts_resolved_before_user_decision") is not True:
            errors.append("decision_frontier_requires_fact_resolution_before_user_decision")

    alternatives = run.get("alternatives")
    if not isinstance(alternatives, list) or len(alternatives) < 2:
        errors.append("at_least_two_alternatives_required")
    else:
        accepted = 0
        for idx, candidate in enumerate(alternatives):
            candidate = _mapping(candidate)
            if not _nonempty(candidate.get("id")) or not _nonempty(candidate.get("rationale")):
                errors.append(f"alternative_{idx}_identity_and_rationale_required")
            decision = str(candidate.get("decision", "")).upper()
            if decision == "ACCEPTED":
                accepted += 1
            elif decision != "REJECTED":
                errors.append(f"alternative_{idx}_decision_invalid")
        if accepted != 1:
            errors.append("exactly_one_alternative_must_be_accepted")

    if current_schema and scope in SYSTEMIC_SCOPES:
        payoff = _mapping(run.get("architecture_payoff"))
        for field in ("current_failure_cost", "change_cost", "expected_payoff", "deletion_or_simplification_result"):
            if not _nonempty(payoff.get(field)):
                errors.append(f"architecture_payoff_{field}_required")
        if payoff.get("deletion_or_simplification_considered") is not True:
            errors.append("architecture_payoff_deletion_or_simplification_must_be_considered")
        net = payoff.get("net_complexity_decision")
        if net not in NET_COMPLEXITY_DECISIONS:
            errors.append("architecture_payoff_net_complexity_decision_required")
        if net == "NET_MORE_COMPLEX_WITH_JUSTIFICATION" and not _nonempty(payoff.get("complexity_justification")):
            errors.append("net_more_complex_requires_justification")

    instruction = _mapping(run.get("instruction_surface"))
    if instruction.get("decision") not in INSTRUCTION_DECISIONS:
        errors.append("instruction_surface_decision_required")
    if not _nonempty(instruction.get("reason")):
        errors.append("instruction_surface_reason_required")

    propagation = _mapping(run.get("propagation"))
    propagation_scope = propagation.get("scope")
    if propagation_scope not in PROPAGATION_SCOPES:
        errors.append("propagation_scope_required")
    if not _nonempty(propagation.get("classification")):
        errors.append("propagation_classification_required")
    if not _nonempty(propagation.get("mechanism")):
        errors.append("propagation_mechanism_required")
    if propagation.get("stale_override_scan") not in {"PASS", "NOT_APPLICABLE"}:
        errors.append("stale_override_scan_required")
    business_owners = _business_owner_names(owner_registry)
    impacted = set(propagation.get("impacted_business_owners", [])) if isinstance(propagation.get("impacted_business_owners"), list) else set()
    if propagation_scope == "ALL_BUSINESS_OWNERS" and business_owners and impacted != business_owners:
        errors.append("all_business_owner_propagation_must_match_registry")
    if propagation_scope == "SUBSET_WITH_REASON":
        if not impacted or not _nonempty(propagation.get("reason")):
            errors.append("subset_propagation_requires_nonempty_subset_and_reason")
        if business_owners and not impacted.issubset(business_owners):
            errors.append("propagation_references_unknown_business_owner")
    if propagation_scope == "NOT_APPLICABLE_WITH_REASON" and not _nonempty(propagation.get("reason")):
        errors.append("non_applicable_propagation_reason_required")

    budget = _mapping(run.get("complexity_efficiency"))
    required_budget = {
        "new_authority_surfaces",
        "mandatory_startup_context_delta",
        "tool_or_remote_read_delta",
        "steady_state_latency_effect",
        "duplicate_rule_effect",
        "cross_owner_touch_count",
        "migration_compatibility_effect",
        "test_observability_effect",
        "decision",
    }
    missing_budget = sorted(field for field in required_budget if field not in budget)
    if missing_budget:
        errors.append("complexity_efficiency_fields_missing:" + ",".join(missing_budget))
    if budget.get("decision") not in {"ACCEPTABLE", "REJECTED"}:
        errors.append("complexity_efficiency_decision_required")
    new_surfaces = budget.get("new_authority_surfaces")
    if isinstance(new_surfaces, int) and new_surfaces > 0 and run.get("authority_surface_admission") != "PASS":
        errors.append("new_authority_surface_requires_admission_gate")

    implementation = _mapping(run.get("implementation"))
    changed_paths = implementation.get("changed_paths")
    if not isinstance(changed_paths, list) or any(not _nonempty(item) for item in changed_paths):
        errors.append("changed_paths_must_be_string_list")
        changed_paths = []
    if schema_version in {"1.1", "1.2", "1.3"}:
        implementation_decision = implementation.get("decision")
        if implementation_decision not in IMPLEMENTATION_DECISIONS:
            errors.append("implementation_decision_required")
        inspected_paths = implementation.get("inspected_paths")
        if not _nonempty_str_list(inspected_paths):
            errors.append("inspected_paths_required")
        if implementation_decision == "CHANGE_APPLIED" and not changed_paths:
            errors.append("change_applied_requires_changed_paths")
        if implementation_decision == "NO_CHANGE_REQUIRED":
            if changed_paths:
                errors.append("no_change_required_forbids_changed_paths")
            if not _nonempty(implementation.get("no_change_reason")):
                errors.append("no_change_required_reason_required")
    elif not changed_paths:
        errors.append("changed_paths_required")
    if not isinstance(implementation.get("superseded_or_demoted_surfaces"), list):
        errors.append("superseded_or_demoted_surfaces_list_required")

    validation = _mapping(run.get("validation"))
    if not _nonempty_str_list(validation.get("regression_or_eval_refs")):
        errors.append("regression_or_eval_refs_required")
    if validation.get("second_order_challenge") != "PASS":
        errors.append("second_order_challenge_required")
    if schema_version in {"1.1", "1.2", "1.3"} and scope in SYSTEMIC_SCOPES and not _nonempty_str_list(validation.get("second_order_findings")):
        errors.append("systemic_second_order_findings_required")
    if scope in SYSTEMIC_SCOPES and validation.get("cross_surface_or_fault_audit") != "PASS":
        errors.append("systemic_change_requires_cross_surface_or_fault_audit")

    closure = _mapping(run.get("closure"))
    ceiling = str(closure.get("assurance_ceiling", "")).strip()
    if ceiling not in ASSURANCE_ORDER:
        errors.append("valid_assurance_ceiling_required")
    if closure.get("global_flawlessness_claimed") is not False:
        errors.append("global_flawlessness_claim_forbidden")
    if not isinstance(closure.get("open_gates"), list):
        errors.append("open_gates_list_required")
    if not _nonempty(closure.get("unknown_or_open_world_boundary")):
        errors.append("unknown_or_open_world_boundary_required")
    if ceiling in {"ACTION_LEVEL_INDEPENDENTLY_VERIFIED", "LIVE_OUTCOME_VERIFIED"} and not _nonempty_str_list(closure.get("independent_evidence_refs")):
        errors.append("high_assurance_claim_requires_independent_evidence_refs")

    return MetaMaintenanceResult(
        status="PASS" if not errors else "FAIL",
        errors=tuple(errors),
        checked_sections=checked,
        assurance_ceiling="STRUCTURED_PROCESS_CONFORMANCE_ONLY",
    )