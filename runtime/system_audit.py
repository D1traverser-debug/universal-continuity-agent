from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Iterable

from runtime.execution_readiness import Assurance, CapabilityRequirement, RouteStatus, evaluate_execution
from runtime.execution_receipt import ReceiptBindingStatus, validate_execution_receipt_binding
from runtime.meta_maintenance import evaluate_meta_maintenance_run
from runtime.methodology_conformance import evaluate_methodology_conformance, evaluate_operational_methodology_conformance
from runtime.owner_topology import bare_inherit_sources, business_owner_names, validate_owner_registry
from runtime.protocol_reconciliation import apply_protocol_patch, plan_in_place_protocol_reconciliation
from runtime.universal_continuity import (
    CommitStatus,
    TaskMetadata,
    acquire_resume_lease,
    build_turn_commit_receipt,
    registry_manifest_drift,
    resolve_candidates,
    should_autoresume,
    verify_resume_lease,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_CHECKS = (
    "protocol_version_alignment",
    "local_authority_reference_reachability",
    "registry_owner_set_consistency",
    "maintenance_task_cache_alignment",
    "maintenance_meta_governance_alignment",
    "product_e2e_status_alignment",
    "owner_protocol_registry_state_consistency",
    "methodology_declaration_operational_separation",
    "owner_membership_single_source_of_truth",
    "persistence_assurance_separation",
    "harness_status_freshness",
)

# Keep the historical scenarios and add newly distilled failure classes. Removing a
# scenario silently would make the audit itself forget a previously defended boundary.
FAULT_INJECTION_SCENARIOS = (
    "required_discovery_source_unavailable",
    "stale_registry_attempts_to_override_owner_authority",
    "same_chat_protocol_refresh_changes_lease_or_resume_epoch",
    "new_chat_takeover_fails_to_change_writer_lease",
    "new_business_owner_is_added_without_execution_or_adaptation_convergence",
    "bare_discovery_uses_stale_parallel_owner_list",
    "methodology_profile_floats_latest",
    "methodology_profile_missing_required_hook",
    "methodology_profile_overrides_kernel_invariant",
    "methodology_applicable_profile_is_silently_omitted",
    "declared_methodology_is_treated_as_operational_proof",
    "self_reported_methodology_receipt_lacks_independent_evidence_verification",
    "methodology_receipt_is_replayed_for_wrong_action",
    "execution_receipt_omits_exact_expectation",
    "execution_receipt_replay_history_is_unverified",
    "isolated_execution_is_self_attested",
    "incomplete_discovery_attempts_autoresume",
    "terminal_task_attempts_writer_takeover",
    "material_write_reports_committed_without_authoritative_reread",
    "destructive_mutation_has_unknown_identity_or_dependency",
    "external_reference_is_promoted_to_authority_by_presence",
    "declared_executor_is_treated_as_session_execution_proof",
    "meta_maintenance_outline_omitted_after_systemic_correction",
    "hard_coded_stale_methodology_receipt_semantics_survive_contract_upgrade",
)

HIGH_RISK_PATHS = {
    "CURRENT_PROTOCOL.json", "CONTINUITY_CONTRACT.json", "ENTRYPOINT.md", "STARTUP_HOOK.md",
    "NEW_CHAT_BOOTSTRAP.json", "BARE_INHERIT_DISCOVERY.json", "OWNER_ADAPTER_CONTRACT.json",
    "OWNER_REGISTRY.json", "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json", "OWNER_EXECUTION_REGISTRY.json",
    "EXECUTION_READINESS_CONTRACT.json", "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json",
    "SYSTEM_MAINTENANCE_POLICY.json", "VERSION_LIFECYCLE_POLICY.json",
    "LIVE_CHAT_RECONCILIATION_POLICY.json", "PROGRESS_OBSERVABILITY_POLICY.json",
    "CONTINUOUS_LEARNING_POLICY.md", "HARNESS_STATUS.json", ".github/workflows/ci.yml",
    "runtime/system_audit.py", "runtime/execution_receipt.py", "runtime/execution_readiness.py",
    "runtime/methodology_conformance.py", "runtime/universal_continuity.py", "runtime/owner_topology.py",
    "runtime/protocol_reconciliation.py", "runtime/meta_maintenance.py", "runtime/maintenance_decision_eval.py",
}
FULL_SWEEP_TRIGGERS = {
    "explicit_global_audit", "protocol_change", "authority_model_change",
    "storage_or_artifact_authority_change", "startup_or_discovery_change",
    "methodology_contract_change", "execution_contract_change", "cross_owner_migration",
    "systemic_incident", "systemic_reliability_incident", "repeated_material_failure",
    "user_challenges_maintenance_method_or_global_completeness", "release_boundary",
}
FAULT_INJECTION_TRIGGERS = {
    "explicit_global_audit", "systemic_incident", "systemic_reliability_incident",
    "repeated_material_failure", "user_challenges_maintenance_method_or_global_completeness",
    "protocol_change", "authority_model_change", "storage_or_artifact_authority_change",
    "methodology_contract_change", "execution_contract_change", "release_boundary",
}


def _normalize_paths(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(path).strip().replace("\\", "/") for path in paths if str(path).strip()}))


def _load_json(root: Path, relative: str) -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _business_owner_scope(owner_registry: dict[str, Any] | None = None) -> set[str]:
    registry = owner_registry or _load_json(REPO_ROOT, "OWNER_REGISTRY.json")
    return set(business_owner_names(registry))


def _high_risk_path(path: str) -> bool:
    return path in HIGH_RISK_PATHS or path.startswith("runtime/") or path.startswith(".github/workflows/")


def plan_audit(
    changed_paths: Iterable[str] = (),
    trigger: str | None = None,
    *,
    owner_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    paths = _normalize_paths(changed_paths)
    trigger = (trigger or "routine_change").strip().lower()
    modes = ["CORE_ALWAYS", "IMPACT_SCOPED"]
    checks = set(CORE_CHECKS)
    owner_scope: set[str] = set()
    business_owners = _business_owner_scope(owner_registry)
    high_risk_change = any(_high_risk_path(path) for path in paths)
    owner_surface_change = any(
        path.startswith("OWNER_")
        or path.startswith("runtime/owner_topology.py")
        or path.startswith("runtime/methodology_conformance.py")
        or path.startswith("runtime/execution_")
        for path in paths
    )
    risk = "HIGH" if high_risk_change or owner_surface_change else "LOW"
    if high_risk_change:
        checks.update({"cross_surface_contradiction_scan", "derived_cache_freshness_scan"})
    if owner_surface_change:
        owner_scope.update(business_owners)
        checks.update({"owner_pointer_reachability", "owner_protocol_observation_match"})
    if trigger in FULL_SWEEP_TRIGGERS or high_risk_change:
        modes.append("FULL_CONTROL_PLANE")
        owner_scope.update(business_owners)
        checks.update({
            "all_control_plane_contracts_and_registries",
            "all_owner_metadata_surfaces",
            "dangling_remote_pointer_check",
            "stale_derived_state_check",
            "maintenance_meta_governance_alignment",
        })
        risk = "HIGH"
    if trigger in FAULT_INJECTION_TRIGGERS or high_risk_change:
        modes.append("SYNTHETIC_FAULT_INJECTION")
        checks.add("negative_and_boundary_scenarios")
        risk = "HIGH"
    if trigger == "owner_rotation":
        modes.append("OWNER_SENTINEL_ROTATION")
        checks.add("rotating_owner_metadata_sample")
        if risk == "LOW":
            risk = "MEDIUM"
    full = "FULL_CONTROL_PLANE" in modes
    return {
        "trigger": trigger,
        "risk": risk,
        "modes": list(dict.fromkeys(modes)),
        "checks": sorted(checks),
        "owner_metadata_scope": sorted(owner_scope),
        "run_all_owner_business_pipelines": False,
        "fault_injection_scenarios": list(FAULT_INJECTION_SCENARIOS) if "SYNTHETIC_FAULT_INJECTION" in modes else [],
        "changed_paths": list(paths),
        "remote_evidence_required": full,
        "remote_evidence_boundary": (
            "CI/local runtime cannot prove remote owner pointer reachability or live owner state; "
            "maintenance runner must supply remote owner metadata evidence before claiming a full cross-repository sweep."
        ),
    }


def _local_ref_candidates(manifest: dict[str, Any]) -> list[str]:
    return [
        ref for ref in manifest.get("artifact_refs", [])
        if isinstance(ref, str) and "@" not in ref and not ref.startswith(("http://", "https://"))
    ]


def _entrypoint_receipt_semantic_errors(adapter: dict[str, Any], entrypoint_text: str) -> list[str]:
    errors: list[str] = []
    current = str(adapter.get("methodology_composition", {}).get("operational_profile_run_contract_version", "")).strip()
    if not current:
        return ["OWNER_ADAPTER_CONTRACT missing operational profile run contract version"]
    if f"receipt-contract-{current}" not in entrypoint_text or f"Under receipt contract {current}" not in entrypoint_text:
        errors.append("ENTRYPOINT methodology receipt semantics are stale relative to OWNER_ADAPTER_CONTRACT")
    if current != "1.2" and ("receipt-contract-1.2" in entrypoint_text or "Under receipt contract 1.2" in entrypoint_text):
        errors.append("ENTRYPOINT retains superseded receipt-contract-1.2 semantics")
    return errors


def _meta_governance_alignment_errors(
    root: Path,
    maintenance: dict[str, Any],
    task_manifest: dict[str, Any],
    harness: dict[str, Any],
    adapter: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    runtime_ref = root / "runtime/meta_maintenance.py"
    if not runtime_ref.exists():
        errors.append("meta-maintenance runtime missing")
    meta = harness.get("meta_governance", {})
    manifest_version = str(task_manifest.get("meta_maintenance_harness_version", "")).strip()
    harness_version = str(meta.get("runtime_version", "")).strip()
    if manifest_version and harness_version and manifest_version != harness_version:
        errors.append("maintenance TASK_MANIFEST meta harness version differs from HARNESS_STATUS")
    if meta.get("authority") != "SYSTEM_MAINTENANCE_POLICY.json":
        errors.append("HARNESS_STATUS meta governance authority drift")
    if meta.get("assurance_ceiling") != "STRUCTURED_PROCESS_CONFORMANCE_ONLY":
        errors.append("HARNESS_STATUS meta governance assurance ceiling drift")
    if meta.get("independent_semantic_review_proven") is not False:
        errors.append("HARNESS_STATUS falsely claims independent meta semantic review")
    run_ref = task_manifest.get("latest_meta_maintenance_run_ref")
    if isinstance(run_ref, str) and run_ref:
        run_path = root / run_ref
        if not run_path.exists():
            errors.append("maintenance latest_meta_maintenance_run_ref is missing")
        else:
            result = evaluate_meta_maintenance_run(
                _load_json(root, run_ref), maintenance, owner_registry=_load_json(root, "OWNER_REGISTRY.json")
            )
            if result.status != "PASS":
                errors.append("latest meta-maintenance run is not structurally conformant")
    else:
        errors.append("maintenance latest_meta_maintenance_run_ref missing")
    errors.extend(_entrypoint_receipt_semantic_errors(adapter, (root / "ENTRYPOINT.md").read_text(encoding="utf-8")))
    return errors


def _methodology_fixture(contract: dict[str, Any], active_profile: str) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    composition = contract["methodology_composition"]
    profiles = composition["profiles"]
    profile = profiles[active_profile]
    hook_set = composition["hook_sets"][profile["required_hooks_from"].split(".")[-1]]
    applicability = {
        profile_id: {
            "status": "APPLIES" if profile_id == active_profile else "NOT_APPLICABLE",
            "reason": "synthetic audit applicability",
            "evidence_refs": [f"synthetic://{profile_id}"],
        }
        for profile_id in profiles
    }
    owner = {
        "methodology": {
            "profile_refs": {active_profile: profile["version"]},
            "profile_applicability": applicability,
            "hook_bindings": {str(h): f"owner://{h}" for h in hook_set},
            "overrides": {},
        }
    }
    return owner, profile, list(hook_set)


def _methodology_separation_errors(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        owner, _, _ = _methodology_fixture(contract, "operational_hygiene")
    except Exception:
        return ["methodology separation preflight cannot resolve operational_hygiene"]
    if evaluate_methodology_conformance(owner, contract).status != "PASS":
        errors.append("synthetic declaration-conformant owner did not pass declaration validation")
    omitted = copy.deepcopy(owner)
    omitted["methodology"]["profile_applicability"]["artifact_io"] = {
        "status": "APPLIES", "reason": "persists artifacts", "evidence_refs": ["synthetic://artifact"]
    }
    result = evaluate_methodology_conformance(omitted, contract)
    if result.status != "FAIL" or "applicable_profile_not_declared:artifact_io" not in result.errors:
        errors.append("applicable methodology profile omission was accepted")
    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        None,
        required_profiles=["operational_hygiene"],
        action_expectation={
            "task_id": "t", "stage": "s", "action_id": "a",
            "subject_bindings": {"x": "y"}, "input_bindings": {"i": "j"},
        },
        evidence_verifier=lambda ref: True,
        assessment_verifier=lambda *args: True,
    )
    if operational.status != "FAIL" or "missing_operational_execution_evidence" not in operational.errors:
        errors.append("declaration-only methodology state was accepted as operational proof")
    return errors


def audit_local_control_plane(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    current = _load_json(root, "CURRENT_PROTOCOL.json")
    contract = _load_json(root, "CONTINUITY_CONTRACT.json")
    adapter = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
    owner_registry = _load_json(root, "OWNER_REGISTRY.json")
    discovery = _load_json(root, "BARE_INHERIT_DISCOVERY.json")
    adaptation = _load_json(root, "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json")
    execution = _load_json(root, "OWNER_EXECUTION_REGISTRY.json")
    maintenance = _load_json(root, "SYSTEM_MAINTENANCE_POLICY.json")
    harness = _load_json(root, "HARNESS_STATUS.json")
    task_manifest = _load_json(root, "tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    generic_registry = _load_json(root, "GENERIC_TASK_REGISTRY.json")

    protocol = current.get("continuity_protocol_version")
    for label, value in (
        ("CONTINUITY_CONTRACT.schema_version", contract.get("schema_version")),
        ("OWNER_ADAPTER_CONTRACT.continuity_contract", adapter.get("continuity_contract")),
        ("OWNER_REGISTRY.continuity_protocol_version", owner_registry.get("continuity_protocol_version")),
        ("BARE_INHERIT_DISCOVERY.continuity_protocol_version", discovery.get("continuity_protocol_version")),
        ("OWNER_PROTOCOL_ADAPTATION_REGISTRY.current_continuity_protocol", adaptation.get("current_continuity_protocol")),
        ("maintenance TASK_MANIFEST protocol", task_manifest.get("continuity_protocol_version")),
    ):
        if value != protocol:
            errors.append(f"{label} != current protocol")
    if task_manifest.get("system_maintenance_policy_version") != maintenance.get("schema_version"):
        errors.append("maintenance TASK_MANIFEST system_maintenance_policy_version is stale")
    if str(task_manifest.get("methodology_owner_declaration_contract_version")) != str(
        adapter.get("methodology_composition", {}).get("owner_declaration_contract_version")
    ):
        errors.append("maintenance TASK_MANIFEST methodology owner declaration contract is stale")

    errors.extend(_meta_governance_alignment_errors(root, maintenance, task_manifest, harness, adapter))
    errors.extend(_methodology_separation_errors(adapter))
    errors.extend(validate_owner_registry(owner_registry))

    owner_map = {
        e["name"]: e for e in owner_registry.get("owners", [])
        if isinstance(e, dict) and e.get("name")
    }
    adapt_map = {
        e["owner"]: e for e in adaptation.get("owners", [])
        if isinstance(e, dict) and e.get("owner")
    }
    exec_map = {
        e["owner"]: e for e in execution.get("owners", [])
        if isinstance(e, dict) and e.get("owner")
    }
    expected = set(business_owner_names(owner_registry))
    bare = bare_inherit_sources(owner_registry)
    bare_names = {r["owner"] for r in bare}
    participant = discovery.get("participant_authority", {})
    if not isinstance(participant, dict) or participant.get("source") != "OWNER_REGISTRY.json":
        errors.append("BARE_INHERIT_DISCOVERY participant authority is not OWNER_REGISTRY.json")
    if isinstance(participant, dict) and participant.get("hard_coded_owner_list_allowed") is not False:
        errors.append("BARE_INHERIT_DISCOVERY permits parallel owner list")
    if "required_sources" in discovery:
        errors.append("BARE_INHERIT_DISCOVERY contains legacy hard-coded required_sources")
    if set(adapt_map) != expected:
        errors.append("OWNER_PROTOCOL_ADAPTATION_REGISTRY owner set does not match OWNER_REGISTRY BUSINESS membership")
    if set(exec_map) != expected:
        errors.append("OWNER_EXECUTION_REGISTRY owner set does not match OWNER_REGISTRY BUSINESS membership")

    for owner in sorted(expected.intersection(adapt_map)):
        entry = adapt_map[owner]
        observed = entry.get("observed_protocol")
        target = entry.get("target_protocol")
        classification = entry.get("classification")
        status = str(entry.get("status", ""))
        registry_status = str(owner_map.get(owner, {}).get("adapter_status", ""))
        if observed == target and classification != "COMPATIBLE":
            errors.append(f"{owner}: observed protocol equals target but classification is not COMPATIBLE")
        if observed == target and "PENDING_VALID_WRITER_RECONCILIATION" in status:
            errors.append(f"{owner}: stale pending reconciliation")
        if observed != target and "READY_V37" in registry_status:
            errors.append(f"{owner}: OWNER_REGISTRY advertises v3.7 readiness while adaptation observation is stale")
        if "RECONCILED" in registry_status and observed != target:
            errors.append(f"{owner}: registry claims reconciled while adaptation is stale")

    lower_text = (
        json.dumps(owner_registry, ensure_ascii=False) + json.dumps(adaptation, ensure_ascii=False)
    ).lower()
    if "or committed claim" in lower_text or ("committed claim" in lower_text and "operational" in lower_text):
        errors.append("lower control surface still couples COMMITTED persistence status to operational assurance")

    generic = {
        t["task_id"]: t for t in generic_registry.get("tasks", [])
        if isinstance(t, dict) and t.get("task_id")
    }
    cache = generic.get(task_manifest.get("task_id"))
    if not cache:
        errors.append("GENERIC_TASK_REGISTRY missing maintenance task cache entry")
    else:
        if cache.get("current_stage") != task_manifest.get("current_stage"):
            errors.append("GENERIC_TASK_REGISTRY maintenance current_stage is stale")
        if cache.get("contract_version") != task_manifest.get("contract_version"):
            errors.append("GENERIC_TASK_REGISTRY maintenance contract_version is stale")

    stage = str(task_manifest.get("current_stage", ""))
    product = harness.get("product_e2e", {})
    existing = product.get("existing_chat", {}).get("status")
    fresh = product.get("fresh_chat", {}).get("status")
    if "KNOWN_TOPOLOGY_PRODUCT_E2E_PASS" in stage and (existing != "PASS" or fresh != "PASS"):
        errors.append("known-topology stage claim contradicts HARNESS_STATUS")
    if "OWNER_PROFILE_MIGRATION_IN_PROGRESS" in str(harness.get("status", "")) and "OWNER_PROFILE_APPLICABILITY_GUARD_PASS" in stage:
        errors.append("HARNESS_STATUS still claims owner profile migration in progress")
    financial_mirror = harness.get("owner_operational_hardening", {}).get("financial_writing", {})
    if financial_mirror.get("methodology_profile_refs") and "artifact_io" not in financial_mirror["methodology_profile_refs"]:
        errors.append("HARNESS_STATUS Financial methodology profile mirror is stale")

    for relative in _local_ref_candidates(task_manifest):
        if not (root / relative).exists():
            errors.append(f"maintenance TASK_MANIFEST local artifact_ref missing: {relative}")
    resolver = owner_registry.get("resolver", {})
    for key in (
        "module", "owner_topology", "bare_inherit_policy", "protocol_adaptation_registry",
        "execution_readiness_contract", "execution_registry", "execution_evaluator",
    ):
        relative = resolver.get(key)
        if relative and not (root / relative).exists():
            errors.append(f"OWNER_REGISTRY resolver ref missing: {key}={relative}")
    if harness.get("startup_trigger", {}).get("acceptance_evidence", {}).get("live_candidate_names_persisted_in_public_harness") is not False:
        errors.append("public harness must not persist live candidate names/task ids")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checked_protocol": protocol,
        "checked_business_owners": sorted(expected),
        "checked_bare_inherit_owners": sorted(bare_names),
        "checked_core_invariants": list(CORE_CHECKS),
    }


def _task_raw(**overrides: Any) -> dict[str, Any]:
    raw: dict[str, Any] = {
        "task_id": "synthetic-task",
        "domain": "SYNTHETIC",
        "title": "Synthetic task",
        "display_name_zh": "合成任务",
        "recovery_owner": "GENERIC_HANDOFF",
        "status": "ACTIVE",
        "task_class": "USER",
        "resume_eligible": True,
        "resume_visibility": "DEFAULT",
        "updated_at": "2026-10-10T00:00:00Z",
        "current_stage": "WORK",
        "next_action": "continue",
        "checkpoint_ref": "synthetic://checkpoint",
        "contract_version": "3.7",
        "manifest_ref": "tasks/synthetic/TASK_MANIFEST.json",
        "manifest_version": 1,
        "resume_epoch": 0,
        "active_lease": None,
    }
    raw.update(overrides)
    return raw


def _fault_methodology_omission(root: Path) -> bool:
    contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
    composition = contract["methodology_composition"]
    profiles = composition["profiles"]
    app = {
        p: {"status": "NOT_APPLICABLE", "reason": "synthetic", "evidence_refs": [f"x://{p}"]}
        for p in profiles
    }
    app["artifact_io"] = {"status": "APPLIES", "reason": "writes files", "evidence_refs": ["x://file"]}
    owner = {"methodology": {"profile_refs": {}, "profile_applicability": app, "hook_bindings": {}, "overrides": {}}}
    return "applicable_profile_not_declared:artifact_io" in evaluate_methodology_conformance(owner, contract).errors


def _fault_methodology_wrong_action(root: Path) -> bool:
    contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
    owner, profile, hooks = _methodology_fixture(contract, "evolution")
    run = {
        "receipt_contract_version": contract["methodology_composition"]["operational_profile_run_contract_version"],
        "profile_id": "evolution",
        "profile_version": profile["version"],
        "activation_id": "a1",
        "trigger": "t",
        "action_binding": {
            "task_id": "task-a", "stage": "S", "action_id": "a",
            "subject_bindings": {"s": "1"}, "input_bindings": {"i": "1"},
        },
        "invoked_hooks": [hooks[0]],
        "hook_assessments": {
            h: {
                "status": "INVOKED" if h == hooks[0] else "NOT_APPLICABLE_FOR_ACTION",
                "reason": "synthetic", "evidence_refs": [f"e://{h}"],
            }
            for h in hooks
        },
        "evidence_refs": ["e://run"],
    }
    result = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["evolution"],
        action_expectation={
            "task_id": "task-b", "stage": "S", "action_id": "a",
            "subject_bindings": {"s": "1"}, "input_bindings": {"i": "1"},
        },
        evidence_verifier=lambda r: True,
        assessment_verifier=lambda *args: True,
    )
    return result.status == "FAIL" and "action_binding_mismatch:evolution:task_id" in result.errors


def _full_execution_receipt() -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = {
        "receipt_id": "r", "action_id": "a", "task_id": "t", "stage": "s",
        "capability_id": "c", "executor_identity": "e", "execution_ref": "x",
        "subject_bindings": {"s": "1"}, "input_bindings": {"i": "1"},
        "output_refs": ["o"], "result": "PASS",
    }
    expectation = {
        "action_id": "a", "task_id": "t", "stage": "s", "capability_id": "c",
        "executor_identity": "e", "subject_bindings": {"s": "1"},
        "input_bindings": {"i": "1"}, "output_refs": ["o"], "result": "PASS",
    }
    return receipt, expectation


def run_synthetic_fault_injection(root: str | Path, scenarios: Iterable[str]) -> dict[str, Any]:
    root = Path(root)
    results: dict[str, str] = {}
    for scenario in scenarios:
        passed = False
        try:
            if scenario == "required_discovery_source_unavailable":
                policy = _load_json(root, "BARE_INHERIT_DISCOVERY.json")
                candidate = resolve_candidates([TaskMetadata.from_mapping(_task_raw())])
                passed = (
                    policy.get("on_source_failure") == "INCOMPLETE_DISCOVERY"
                    and not should_autoresume(candidate, hint_present=False, discovery_complete=False)
                )
            elif scenario == "stale_registry_attempts_to_override_owner_authority":
                drift = registry_manifest_drift(
                    [{"task_id": "x", "status": "ACTIVE", "current_stage": "OLD", "next_action": "old", "recovery_owner": "o", "checkpoint_ref": "c", "display_name_zh": "x"}],
                    [{"task_id": "x", "status": "ACTIVE", "current_stage": "NEW", "next_action": "new", "recovery_owner": "o", "checkpoint_ref": "c", "display_name_zh": "x"}],
                )
                passed = "registry-stale:x:current_stage" in drift
            elif scenario == "same_chat_protocol_refresh_changes_lease_or_resume_epoch":
                raw = _task_raw(
                    contract_version="CONTINUITY_V3_3",
                    continuity_protocol_version="3.3",
                    resume_epoch=4,
                    active_lease={"lease_id": "lease-current", "acquired_at": "2026-10-10T00:00:00Z"},
                )
                plan = plan_in_place_protocol_reconciliation(
                    raw,
                    current_protocol_version="3.7",
                    migration_supported_from={"3.3"},
                    lease_id="lease-current",
                    resume_epoch=4,
                    applied_by="synthetic-audit",
                )
                updated = apply_protocol_patch(raw, plan)
                passed = updated["resume_epoch"] == 4 and updated["active_lease"] == raw["active_lease"]
            elif scenario == "new_chat_takeover_fails_to_change_writer_lease":
                first = acquire_resume_lease(TaskMetadata.from_mapping(_task_raw()), lease_id="old")
                second = acquire_resume_lease(first, lease_id="new")
                passed = second.resume_epoch == 2 and verify_resume_lease(second, "new", resume_epoch=2) and not verify_resume_lease(second, "old", resume_epoch=1)
            elif scenario == "new_business_owner_is_added_without_execution_or_adaptation_convergence":
                owners = copy.deepcopy(_load_json(root, "OWNER_REGISTRY.json"))
                owners["owners"].append({
                    "name": "SYNTHETIC_NEW_AGENT", "owner_kind": "BUSINESS", "domains": ["SYNTHETIC"],
                    "priority": 100, "adapter_status": "SYNTHETIC", "bare_inherit_participant": True,
                    "bare_inherit_source": "synthetic@main:continuity/TASK_INDEX.json",
                    "checkpoint_authority": "synthetic@main:continuity/tasks/<task_id>/TASK_MANIFEST.json",
                    "protocol_adapter": "synthetic@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
                    "execution_capability_ref": "synthetic@main:continuity/EXECUTION_CAPABILITIES.json",
                })
                expected = set(business_owner_names(owners))
                adaptation = {e["owner"] for e in _load_json(root, "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json")["owners"]}
                execution = {e["owner"] for e in _load_json(root, "OWNER_EXECUTION_REGISTRY.json")["owners"]}
                passed = expected != adaptation and expected != execution and "SYNTHETIC_NEW_AGENT" in expected
            elif scenario == "bare_discovery_uses_stale_parallel_owner_list":
                policy = _load_json(root, "BARE_INHERIT_DISCOVERY.json")
                authority = policy.get("participant_authority", {})
                passed = (
                    "required_sources" not in policy
                    and authority.get("source") == "OWNER_REGISTRY.json"
                    and authority.get("hard_coded_owner_list_allowed") is False
                )
            elif scenario == "methodology_profile_floats_latest":
                contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
                owner, _, _ = _methodology_fixture(contract, "evolution")
                owner["methodology"]["profile_refs"]["evolution"] = "latest"
                passed = any(e.startswith("profile_version_mismatch:evolution") for e in evaluate_methodology_conformance(owner, contract).errors)
            elif scenario == "methodology_profile_missing_required_hook":
                contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
                owner, _, hooks = _methodology_fixture(contract, "artifact_io")
                owner["methodology"]["hook_bindings"].pop(hooks[0])
                passed = any(e.startswith("missing_hook_binding:artifact_io:") for e in evaluate_methodology_conformance(owner, contract).errors)
            elif scenario == "methodology_profile_overrides_kernel_invariant":
                contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
                owner, _, _ = _methodology_fixture(contract, "operational_hygiene")
                owner["methodology"]["overrides"] = {"single_writer_lease": False}
                passed = "forbidden_override:single_writer_lease" in evaluate_methodology_conformance(owner, contract).errors
            elif scenario == "methodology_applicable_profile_is_silently_omitted":
                passed = _fault_methodology_omission(root)
            elif scenario == "declared_methodology_is_treated_as_operational_proof":
                contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
                owner, _, _ = _methodology_fixture(contract, "operational_hygiene")
                result = evaluate_operational_methodology_conformance(
                    owner, contract, None, required_profiles=["operational_hygiene"],
                    action_expectation={"task_id": "t", "stage": "s", "action_id": "a", "subject_bindings": {"x": "y"}, "input_bindings": {"i": "j"}},
                    evidence_verifier=lambda r: True, assessment_verifier=lambda *args: True,
                )
                passed = result.status == "FAIL" and "missing_operational_execution_evidence" in result.errors
            elif scenario == "self_reported_methodology_receipt_lacks_independent_evidence_verification":
                contract = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
                owner, profile, hooks = _methodology_fixture(contract, "evolution")
                run = {
                    "receipt_contract_version": contract["methodology_composition"]["operational_profile_run_contract_version"],
                    "profile_id": "evolution", "profile_version": profile["version"], "activation_id": "a1", "trigger": "t",
                    "action_binding": {"task_id": "t", "stage": "s", "action_id": "a", "subject_bindings": {"x": "y"}, "input_bindings": {"i": "j"}},
                    "invoked_hooks": [hooks[0]],
                    "hook_assessments": {h: {"status": "INVOKED" if h == hooks[0] else "NOT_APPLICABLE_FOR_ACTION", "reason": "synthetic", "evidence_refs": [f"e://{h}"]} for h in hooks},
                    "evidence_refs": ["e://run"],
                }
                result = evaluate_operational_methodology_conformance(
                    owner, contract, {"profile_runs": [run]}, required_profiles=["evolution"],
                    action_expectation={"task_id": "t", "stage": "s", "action_id": "a", "subject_bindings": {"x": "y"}, "input_bindings": {"i": "j"}},
                )
                passed = result.status == "FAIL" and "independent_evidence_verifier_required" in result.errors
            elif scenario == "methodology_receipt_is_replayed_for_wrong_action":
                passed = _fault_methodology_wrong_action(root)
            elif scenario == "execution_receipt_omits_exact_expectation":
                receipt, _ = _full_execution_receipt()
                result = validate_execution_receipt_binding(receipt, {"task_id": "t"}, replay_history_verifier=lambda history: True)
                passed = result.status == ReceiptBindingStatus.FAIL
            elif scenario == "execution_receipt_replay_history_is_unverified":
                receipt, expectation = _full_execution_receipt()
                passed = validate_execution_receipt_binding(receipt, expectation).status == ReceiptBindingStatus.FAIL
            elif scenario == "isolated_execution_is_self_attested":
                profile = {"owner": "o", "repository": "r", "capabilities": [{
                    "capability_id": "c", "scope": "x", "assurance_ceiling": "ATTESTED_ISOLATED",
                    "invocation_path": "owner:run", "executor_type": "x", "evidence_contract": ["x"],
                    "side_channel_allowed": False,
                }]}
                obs = {
                    "capability_id": "c", "availability": "AVAILABLE", "observed_assurance": "ATTESTED_ISOLATED",
                    "execution_mode": "ISOLATED_EXTERNAL", "executor_identity": "fake", "proof_ref": "fake", "route_ref": "owner:run",
                }
                passed = evaluate_execution(
                    profile, [CapabilityRequirement("c", min_assurance=Assurance.ATTESTED_ISOLATED)], [obs]
                ).status == RouteStatus.BLOCKED
            elif scenario == "incomplete_discovery_attempts_autoresume":
                candidates = resolve_candidates([TaskMetadata.from_mapping(_task_raw())])
                passed = not should_autoresume(candidates, hint_present=False, discovery_complete=False)
            elif scenario == "terminal_task_attempts_writer_takeover":
                task = TaskMetadata.from_mapping(_task_raw(status="COMPLETE", resume_visibility="EXPLICIT_ONLY"))
                try:
                    acquire_resume_lease(task, lease_id="x")
                except ValueError:
                    passed = True
            elif scenario == "material_write_reports_committed_without_authoritative_reread":
                task = acquire_resume_lease(TaskMetadata.from_mapping(_task_raw()), lease_id="x")
                passed = build_turn_commit_receipt(
                    task, commit_required=True, write_succeeded=True, verified_after_write=False,
                    lease_id="x", resume_epoch=1,
                ).commit_status == CommitStatus.COMMIT_FAILED
            elif scenario == "destructive_mutation_has_unknown_identity_or_dependency":
                policy = _load_json(root, "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json")
                failure = policy.get("failure_semantics", {})
                passed = (
                    failure.get("cannot_resolve_stable_identity") == "BLOCK_DESTRUCTIVE_OR_CONFLICT_SENSITIVE_MUTATION"
                    and failure.get("delete_dependency_unknown") == "DO_NOT_DELETE"
                )
            elif scenario == "external_reference_is_promoted_to_authority_by_presence":
                policy = _load_json(root, "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json")
                storage = policy.get("storage_classes", {}).get("EXTERNAL_REFERENCE", {})
                passed = storage.get("may_drive_execution") == "ONLY_WHEN_CURRENT_OWNER_CONTRACT_OR_CURRENT_USER_TASK_EXPLICITLY_DESIGNATES_IT_WITH_PROVENANCE"
            elif scenario == "declared_executor_is_treated_as_session_execution_proof":
                profile = {"owner": "o", "repository": "r", "capabilities": [{
                    "capability_id": "c", "scope": "x", "assurance_ceiling": "SESSION_EXECUTABLE",
                    "invocation_path": "owner:run", "executor_type": "x", "evidence_contract": ["x"],
                    "side_channel_allowed": False,
                }]}
                decision = evaluate_execution(profile, [CapabilityRequirement("c")], [])
                passed = decision.status == RouteStatus.BLOCKED and decision.blockers == ("session_capability_unobserved:c",)
            elif scenario == "meta_maintenance_outline_omitted_after_systemic_correction":
                policy = _load_json(root, "SYSTEM_MAINTENANCE_POLICY.json")
                incomplete = {
                    "schema_version": "1.1",
                    "run_id": "synthetic-meta-omission",
                    "scope": "FULL_CONTROL_PLANE",
                    "trigger": "USER_CHALLENGES_MAINTENANCE_METHOD_OR_GLOBAL_COMPLETENESS",
                    "user_signal": {
                        "classifications": ["GOAL_OR_CONSTRAINT"],
                        "goal_or_constraint": "systemic maintenance must close completely",
                    },
                    "authority_inspection": {"refs": ["SYSTEM_MAINTENANCE_POLICY.json"]},
                }
                result = evaluate_meta_maintenance_run(
                    incomplete, policy, owner_registry=_load_json(root, "OWNER_REGISTRY.json")
                )
                passed = result.status == "FAIL" and "systemic_change_requires_learning_scout" in result.errors and "at_least_two_alternatives_required" in result.errors
            elif scenario == "hard_coded_stale_methodology_receipt_semantics_survive_contract_upgrade":
                adapter = copy.deepcopy(_load_json(root, "OWNER_ADAPTER_CONTRACT.json"))
                adapter["methodology_composition"]["operational_profile_run_contract_version"] = "9.9"
                entrypoint = (root / "ENTRYPOINT.md").read_text(encoding="utf-8")
                passed = bool(_entrypoint_receipt_semantic_errors(adapter, entrypoint))
        except Exception:
            passed = False
        results[scenario] = "PASS" if passed else "FAIL"
    failed = [name for name, status in results.items() if status != "PASS"]
    return {"status": "PASS" if not failed else "FAIL", "results": results, "failed": failed}


def evaluate_owner_protocol_observation(
    adaptation_entry: dict[str, Any],
    *,
    authoritative_protocol: str,
    missing_remote_refs: Iterable[str] = (),
) -> list[str]:
    errors: list[str] = []
    owner = adaptation_entry.get("owner", "UNKNOWN_OWNER")
    target = adaptation_entry.get("target_protocol")
    observed = adaptation_entry.get("observed_protocol")
    if authoritative_protocol != target:
        errors.append(f"{owner}: authoritative owner protocol {authoritative_protocol} != target {target}")
    if authoritative_protocol == target and observed != target:
        errors.append(f"{owner}: adaptation registry observed_protocol is stale")
    if authoritative_protocol == target and adaptation_entry.get("classification") != "COMPATIBLE":
        errors.append(f"{owner}: target protocol reached but classification is not COMPATIBLE")
    for ref in missing_remote_refs:
        errors.append(f"{owner}: dangling remote authority/conformance ref: {ref}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Universal Continuity risk-tiered system audit")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--trigger", default="routine_change")
    parser.add_argument("--changed-path", action="append", default=[])
    args = parser.parse_args()
    root = Path(args.repo_root)
    owner_registry = _load_json(root, "OWNER_REGISTRY.json")
    plan = plan_audit(args.changed_path, args.trigger, owner_registry=owner_registry)
    local = audit_local_control_plane(root)
    faults = (
        run_synthetic_fault_injection(root, plan["fault_injection_scenarios"])
        if plan["fault_injection_scenarios"]
        else {"status": "NOT_SELECTED", "results": {}, "failed": []}
    )
    status = "PASS" if local["status"] == "PASS" and faults["status"] in {"PASS", "NOT_SELECTED"} else "FAIL"
    result = {
        "status": status,
        "plan": plan,
        "local_audit": local,
        "synthetic_fault_injection": faults,
        "assurance_ceiling": (
            "LOCAL_CONTROL_PLANE_AND_DETERMINISTIC_SYNTHETIC_FAULTS_ONLY; remote owner sweep requires "
            "maintenance-runner evidence when plan.remote_evidence_required=true"
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
