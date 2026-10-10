from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


CORE_CHECKS = (
    "protocol_version_alignment",
    "local_authority_reference_reachability",
    "registry_owner_set_consistency",
    "maintenance_task_cache_alignment",
    "product_e2e_status_alignment",
    "owner_protocol_registry_state_consistency",
)

FAULT_INJECTION_SCENARIOS = (
    "required_discovery_source_unavailable",
    "stale_registry_attempts_to_override_owner_authority",
    "same_chat_protocol_refresh_changes_lease_or_resume_epoch",
    "new_chat_takeover_fails_to_change_writer_lease",
    "methodology_profile_floats_latest",
    "methodology_profile_missing_required_hook",
    "methodology_profile_overrides_kernel_invariant",
    "material_write_reports_committed_without_authoritative_reread",
    "destructive_mutation_has_unknown_identity_or_dependency",
    "external_reference_is_promoted_to_authority_by_presence",
    "declared_executor_is_treated_as_session_execution_proof",
)

BUSINESS_OWNERS = (
    "FINANCIAL_WRITING_AGENT_RUNTIME",
    "A_SHARE_MARKET_AGENT",
    "NOVEL_WRITING_AGENT",
    "VIDEO_GROWTH_AGENT",
)

HIGH_RISK_PATHS = {
    "CURRENT_PROTOCOL.json",
    "CONTINUITY_CONTRACT.json",
    "ENTRYPOINT.md",
    "STARTUP_HOOK.md",
    "BARE_INHERIT_DISCOVERY.json",
    "OWNER_ADAPTER_CONTRACT.json",
    "OWNER_REGISTRY.json",
    "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json",
    "OWNER_EXECUTION_REGISTRY.json",
    "EXECUTION_READINESS_CONTRACT.json",
    "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json",
    "SYSTEM_MAINTENANCE_POLICY.json",
    "VERSION_LIFECYCLE_POLICY.json",
    "LIVE_CHAT_RECONCILIATION_POLICY.json",
    "PROGRESS_OBSERVABILITY_POLICY.json",
}

FULL_SWEEP_TRIGGERS = {
    "explicit_global_audit",
    "protocol_change",
    "authority_model_change",
    "storage_or_artifact_authority_change",
    "startup_or_discovery_change",
    "methodology_contract_change",
    "execution_contract_change",
    "cross_owner_migration",
    "systemic_incident",
    "release_boundary",
}

FAULT_INJECTION_TRIGGERS = {
    "explicit_global_audit",
    "systemic_incident",
    "protocol_change",
    "authority_model_change",
    "storage_or_artifact_authority_change",
    "methodology_contract_change",
    "execution_contract_change",
    "release_boundary",
}


def _normalize_paths(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(path).strip().replace("\\", "/") for path in paths if str(path).strip()}))


def plan_audit(changed_paths: Iterable[str] = (), trigger: str | None = None) -> dict[str, Any]:
    """Return a deterministic risk-tiered audit plan.

    The planner deliberately does not default to running every owner business pipeline.
    It escalates to metadata-wide or fault-injection checks only when the change surface
    or maintenance trigger justifies the additional cost and blast radius.
    """

    paths = _normalize_paths(changed_paths)
    trigger = (trigger or "routine_change").strip()
    modes = ["CORE_ALWAYS", "IMPACT_SCOPED"]
    checks = set(CORE_CHECKS)
    owner_scope: set[str] = set()
    risk = "LOW"

    high_risk_change = any(path in HIGH_RISK_PATHS for path in paths)
    owner_surface_change = any(
        path.startswith("OWNER_")
        or path.startswith("runtime/methodology_conformance.py")
        or path.startswith("runtime/execution_readiness.py")
        for path in paths
    )

    if high_risk_change:
        risk = "HIGH"
        checks.update({"cross_surface_contradiction_scan", "derived_cache_freshness_scan"})

    if owner_surface_change:
        risk = "HIGH"
        owner_scope.update(BUSINESS_OWNERS)
        checks.update({"owner_pointer_reachability", "owner_protocol_observation_match"})

    if trigger in FULL_SWEEP_TRIGGERS or high_risk_change:
        modes.append("FULL_CONTROL_PLANE")
        owner_scope.update(BUSINESS_OWNERS)
        checks.update(
            {
                "all_control_plane_contracts_and_registries",
                "all_owner_metadata_surfaces",
                "dangling_remote_pointer_check",
                "stale_derived_state_check",
            }
        )
        risk = "HIGH"

    if trigger in FAULT_INJECTION_TRIGGERS:
        modes.append("SYNTHETIC_FAULT_INJECTION")
        checks.add("negative_and_boundary_scenarios")
        risk = "HIGH"

    if trigger == "owner_rotation":
        modes.append("OWNER_SENTINEL_ROTATION")
        checks.add("rotating_owner_metadata_sample")
        risk = max(risk, "MEDIUM", key=("LOW", "MEDIUM", "HIGH").index)

    return {
        "trigger": trigger,
        "risk": risk,
        "modes": list(dict.fromkeys(modes)),
        "checks": sorted(checks),
        "owner_metadata_scope": sorted(owner_scope),
        "run_all_owner_business_pipelines": False,
        "fault_injection_scenarios": list(FAULT_INJECTION_SCENARIOS) if "SYNTHETIC_FAULT_INJECTION" in modes else [],
        "changed_paths": list(paths),
    }


def _load_json(root: Path, relative: str) -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _local_ref_candidates(manifest: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for ref in manifest.get("artifact_refs", []):
        if isinstance(ref, str) and "@" not in ref and not ref.startswith(("http://", "https://")):
            refs.append(ref)
    return refs


def audit_local_control_plane(root: str | Path) -> dict[str, Any]:
    """Audit local Universal control-plane coherence without touching owner business state."""

    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []

    current = _load_json(root, "CURRENT_PROTOCOL.json")
    contract = _load_json(root, "CONTINUITY_CONTRACT.json")
    adapter = _load_json(root, "OWNER_ADAPTER_CONTRACT.json")
    owner_registry = _load_json(root, "OWNER_REGISTRY.json")
    adaptation = _load_json(root, "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json")
    execution = _load_json(root, "OWNER_EXECUTION_REGISTRY.json")
    maintenance = _load_json(root, "SYSTEM_MAINTENANCE_POLICY.json")
    harness = _load_json(root, "HARNESS_STATUS.json")
    task_manifest = _load_json(root, "tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    generic_registry = _load_json(root, "GENERIC_TASK_REGISTRY.json")

    protocol = current.get("continuity_protocol_version")
    if contract.get("schema_version") != protocol:
        errors.append("CONTINUITY_CONTRACT.schema_version != CURRENT_PROTOCOL.continuity_protocol_version")
    if adapter.get("continuity_contract") != protocol:
        errors.append("OWNER_ADAPTER_CONTRACT.continuity_contract != current protocol")
    if owner_registry.get("continuity_protocol_version") != protocol:
        errors.append("OWNER_REGISTRY.continuity_protocol_version != current protocol")
    if adaptation.get("current_continuity_protocol") != protocol:
        errors.append("OWNER_PROTOCOL_ADAPTATION_REGISTRY.current_continuity_protocol != current protocol")
    if task_manifest.get("continuity_protocol_version") != protocol:
        errors.append("maintenance TASK_MANIFEST protocol != current protocol")

    if task_manifest.get("system_maintenance_policy_version") != maintenance.get("schema_version"):
        errors.append("maintenance TASK_MANIFEST system_maintenance_policy_version is stale")

    owner_entries = {entry["name"]: entry for entry in owner_registry.get("owners", [])}
    adaptation_entries = {entry["owner"]: entry for entry in adaptation.get("owners", [])}
    execution_entries = {entry["owner"]: entry for entry in execution.get("owners", [])}

    expected_business = set(BUSINESS_OWNERS)
    if not expected_business.issubset(owner_entries):
        errors.append("OWNER_REGISTRY is missing one or more durable business owners")
    if set(adaptation_entries) != expected_business:
        errors.append("OWNER_PROTOCOL_ADAPTATION_REGISTRY owner set does not match durable business owners")
    if set(execution_entries) != expected_business:
        errors.append("OWNER_EXECUTION_REGISTRY owner set does not match durable business owners")

    for owner in sorted(expected_business.intersection(adaptation_entries)):
        entry = adaptation_entries[owner]
        observed = entry.get("observed_protocol")
        target = entry.get("target_protocol")
        classification = entry.get("classification")
        status = str(entry.get("status", ""))
        if observed == target and classification != "COMPATIBLE":
            errors.append(f"{owner}: observed protocol equals target but classification is not COMPATIBLE")
        if observed == target and "PENDING_VALID_WRITER_RECONCILIATION" in status:
            errors.append(f"{owner}: stale pending-reconciliation status after reaching target protocol")
        registry_status = str(owner_entries.get(owner, {}).get("adapter_status", ""))
        if observed == target and "LAZY_RECONCILIATION" in registry_status:
            errors.append(f"{owner}: OWNER_REGISTRY still claims lazy reconciliation after target protocol reached")

    generic_tasks = {task["task_id"]: task for task in generic_registry.get("tasks", [])}
    maintenance_cache = generic_tasks.get(task_manifest.get("task_id"))
    if not maintenance_cache:
        errors.append("GENERIC_TASK_REGISTRY missing maintenance task cache entry")
    else:
        if maintenance_cache.get("current_stage") != task_manifest.get("current_stage"):
            errors.append("GENERIC_TASK_REGISTRY maintenance current_stage is stale")
        if maintenance_cache.get("contract_version") != task_manifest.get("contract_version"):
            errors.append("GENERIC_TASK_REGISTRY maintenance contract_version is stale")

    stage = str(task_manifest.get("current_stage", ""))
    product_e2e = harness.get("product_e2e", {})
    existing = product_e2e.get("existing_chat", {}).get("status")
    fresh = product_e2e.get("fresh_chat", {}).get("status")
    if "PRODUCT_E2E_PASS" in stage and (existing != "PASS" or fresh != "PASS"):
        errors.append("maintenance stage claims PRODUCT_E2E_PASS but HARNESS_STATUS product_e2e is not fully PASS")
    if harness.get("execution_propagation", {}).get("fresh_chat_product_e2e") == "PENDING_REAL_CHAT_EVIDENCE" and fresh == "PASS":
        errors.append("HARNESS_STATUS execution_propagation fresh-chat state contradicts product_e2e")

    for relative in _local_ref_candidates(task_manifest):
        if not (root / relative).exists():
            errors.append(f"maintenance TASK_MANIFEST local artifact_ref missing: {relative}")

    resolver = owner_registry.get("resolver", {})
    for key in ("module", "bare_inherit_policy", "protocol_adaptation_registry", "execution_readiness_contract", "execution_registry", "execution_evaluator"):
        relative = resolver.get(key)
        if relative and not (root / relative).exists():
            errors.append(f"OWNER_REGISTRY resolver ref missing: {key}={relative}")

    if harness.get("startup_trigger", {}).get("acceptance_evidence", {}).get("live_candidate_names_persisted_in_public_harness") is not False:
        errors.append("public harness must not persist live candidate names/task ids")

    if not errors and harness.get("source_validation", {}).get("status") != "PASS":
        warnings.append("HARNESS_STATUS source_validation is not PASS even though local coherence passed")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checked_protocol": protocol,
        "checked_business_owners": sorted(expected_business),
        "checked_core_invariants": list(CORE_CHECKS),
    }


def evaluate_owner_protocol_observation(
    adaptation_entry: dict[str, Any],
    *,
    authoritative_protocol: str,
    missing_remote_refs: Iterable[str] = (),
) -> list[str]:
    """Evaluate live owner evidence supplied by a maintenance runner.

    Remote refs are intentionally observations supplied by the caller; this module does
    not reach across repositories by itself and therefore cannot steal an owner lease or
    turn CI into a network-dependent business execution path.
    """

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

    result = {
        "plan": plan_audit(args.changed_path, args.trigger),
        "local_audit": audit_local_control_plane(args.repo_root),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["local_audit"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
