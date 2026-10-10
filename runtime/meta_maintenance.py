from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


CURRENT_META_MAINTENANCE_SCHEMA = "1.1"
SUPPORTED_META_MAINTENANCE_SCHEMAS = {"1.0", CURRENT_META_MAINTENANCE_SCHEMA}
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
        "learning",
        "alternatives_and_falsification",
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
    if current_schema and "COUNTEREXAMPLE_OR_FAILURE_REPORT" in (classes or []) and not _nonempty(signal.get("counterexample")):
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
    if not _nonempty_str_list(failure.get("failure_classes")):
        errors.append("failure_classes_required")
    if not isinstance(failure.get("system_impact_map"), list) or not failure.get("system_impact_map"):
        errors.append("system_impact_map_required")
    if current_schema and scope in SYSTEMIC_SCOPES and not _nonempty_str_list(failure.get("falsification_checks")):
        errors.append("systemic_falsification_checks_required")

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
                if current_schema and source.get("disposition") not in LEARNING_SOURCE_DISPOSITIONS:
                    errors.append(f"learning_source_{idx}_disposition_invalid")
    elif disposition == "NOT_REQUIRED_WITH_REASON" and not _nonempty(learning.get("reason")):
        errors.append("learning_not_required_reason_required")

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
    if current_schema:
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
    if current_schema and scope in SYSTEMIC_SCOPES and not _nonempty_str_list(validation.get("second_order_findings")):
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
