from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Iterable

from runtime.execution_readiness import Assurance, CapabilityRequirement, RouteStatus, evaluate_execution
from runtime.execution_receipt import ReceiptBindingStatus, validate_execution_receipt_binding
from runtime.methodology_conformance import evaluate_methodology_conformance, evaluate_operational_methodology_conformance
from runtime.owner_topology import bare_inherit_sources, business_owner_names, validate_owner_registry
from runtime.universal_continuity import (
    TaskMetadata, acquire_resume_lease, resolve_candidates, should_autoresume,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_CHECKS = (
    "protocol_version_alignment", "local_authority_reference_reachability",
    "registry_owner_set_consistency", "maintenance_task_cache_alignment",
    "product_e2e_status_alignment", "owner_protocol_registry_state_consistency",
    "methodology_declaration_operational_separation", "owner_membership_single_source_of_truth",
    "persistence_assurance_separation", "harness_status_freshness",
)

FAULT_INJECTION_SCENARIOS = (
    "methodology_applicable_profile_is_silently_omitted",
    "methodology_receipt_is_replayed_for_wrong_action",
    "execution_receipt_omits_exact_expectation",
    "execution_receipt_replay_history_is_unverified",
    "isolated_execution_is_self_attested",
    "incomplete_discovery_attempts_autoresume",
    "terminal_task_attempts_writer_takeover",
    "material_write_reports_committed_without_authoritative_reread",
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
    "runtime/protocol_reconciliation.py",
}
FULL_SWEEP_TRIGGERS = {
    "explicit_global_audit", "protocol_change", "authority_model_change",
    "storage_or_artifact_authority_change", "startup_or_discovery_change",
    "methodology_contract_change", "execution_contract_change", "cross_owner_migration",
    "systemic_incident", "release_boundary",
}
FAULT_INJECTION_TRIGGERS = {
    "explicit_global_audit", "systemic_incident", "protocol_change", "authority_model_change",
    "storage_or_artifact_authority_change", "methodology_contract_change",
    "execution_contract_change", "release_boundary",
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


def plan_audit(changed_paths: Iterable[str] = (), trigger: str | None = None, *, owner_registry: dict[str, Any] | None = None) -> dict[str, Any]:
    paths = _normalize_paths(changed_paths)
    trigger = (trigger or "routine_change").strip()
    modes = ["CORE_ALWAYS", "IMPACT_SCOPED"]
    checks = set(CORE_CHECKS)
    owner_scope: set[str] = set()
    business_owners = _business_owner_scope(owner_registry)
    high_risk_change = any(_high_risk_path(path) for path in paths)
    owner_surface_change = any(path.startswith("OWNER_") or path.startswith("runtime/owner_topology.py") or path.startswith("runtime/methodology_conformance.py") or path.startswith("runtime/execution_") for path in paths)
    risk = "HIGH" if high_risk_change or owner_surface_change else "LOW"
    if high_risk_change:
        checks.update({"cross_surface_contradiction_scan", "derived_cache_freshness_scan"})
    if owner_surface_change:
        owner_scope.update(business_owners)
        checks.update({"owner_pointer_reachability", "owner_protocol_observation_match"})
    if trigger in FULL_SWEEP_TRIGGERS or high_risk_change:
        modes.append("FULL_CONTROL_PLANE")
        owner_scope.update(business_owners)
        checks.update({"all_control_plane_contracts_and_registries", "all_owner_metadata_surfaces", "dangling_remote_pointer_check", "stale_derived_state_check"})
        risk = "HIGH"
    if trigger in FAULT_INJECTION_TRIGGERS or high_risk_change:
        modes.append("SYNTHETIC_FAULT_INJECTION")
        checks.add("negative_and_boundary_scenarios")
        risk = "HIGH"
    if trigger == "owner_rotation":
        modes.append("OWNER_SENTINEL_ROTATION"); checks.add("rotating_owner_metadata_sample")
        if risk == "LOW": risk = "MEDIUM"
    full = "FULL_CONTROL_PLANE" in modes
    return {
        "trigger": trigger, "risk": risk, "modes": list(dict.fromkeys(modes)), "checks": sorted(checks),
        "owner_metadata_scope": sorted(owner_scope), "run_all_owner_business_pipelines": False,
        "fault_injection_scenarios": list(FAULT_INJECTION_SCENARIOS) if "SYNTHETIC_FAULT_INJECTION" in modes else [],
        "changed_paths": list(paths),
        "remote_evidence_required": full,
        "remote_evidence_boundary": "CI/local runtime cannot prove remote owner pointer reachability or live owner state; maintenance runner must supply remote owner metadata evidence before claiming a full cross-repository sweep.",
    }


def _local_ref_candidates(manifest: dict[str, Any]) -> list[str]:
    return [ref for ref in manifest.get("artifact_refs", []) if isinstance(ref, str) and "@" not in ref and not ref.startswith(("http://", "https://"))]


def _methodology_separation_errors(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    composition = contract.get("methodology_composition", {})
    profiles = composition.get("profiles", {}) if isinstance(composition, dict) else {}
    hygiene = profiles.get("operational_hygiene") if isinstance(profiles, dict) else None
    hooks = composition.get("hook_sets", {}).get("operational_hygiene") if isinstance(composition.get("hook_sets", {}), dict) else None
    if not isinstance(hygiene, dict) or not isinstance(hooks, list):
        return ["methodology separation preflight cannot resolve operational_hygiene"]
    applicability = {}
    for profile_id in profiles:
        applies = profile_id == "operational_hygiene"
        applicability[profile_id] = {"status":"APPLIES" if applies else "NOT_APPLICABLE","reason":"synthetic audit applicability","evidence_refs":[f"synthetic://{profile_id}"]}
    owner = {"methodology":{"profile_refs":{"operational_hygiene":hygiene.get("version")},"profile_applicability":applicability,"hook_bindings":{str(h):f"owner://{h}" for h in hooks},"overrides":{}}}
    if evaluate_methodology_conformance(owner, contract).status != "PASS":
        errors.append("synthetic declaration-conformant owner did not pass declaration validation")
    omitted = copy.deepcopy(owner)
    omitted["methodology"]["profile_applicability"]["artifact_io"]={"status":"APPLIES","reason":"persists artifacts","evidence_refs":["synthetic://artifact"]}
    result = evaluate_methodology_conformance(omitted, contract)
    if result.status != "FAIL" or "applicable_profile_not_declared:artifact_io" not in result.errors:
        errors.append("applicable methodology profile omission was accepted")
    operational = evaluate_operational_methodology_conformance(owner, contract, None, required_profiles=["operational_hygiene"], action_expectation={"task_id":"t","stage":"s","action_id":"a","subject_bindings":{"x":"y"},"input_bindings":{"i":"j"}}, evidence_verifier=lambda ref: True, assessment_verifier=lambda *args: True)
    if operational.status != "FAIL" or "missing_operational_execution_evidence" not in operational.errors:
        errors.append("declaration-only methodology state was accepted as operational proof")
    return errors


def audit_local_control_plane(root: str | Path) -> dict[str, Any]:
    root = Path(root); errors: list[str] = []; warnings: list[str] = []
    current=_load_json(root,"CURRENT_PROTOCOL.json"); contract=_load_json(root,"CONTINUITY_CONTRACT.json"); adapter=_load_json(root,"OWNER_ADAPTER_CONTRACT.json")
    owner_registry=_load_json(root,"OWNER_REGISTRY.json"); discovery=_load_json(root,"BARE_INHERIT_DISCOVERY.json"); adaptation=_load_json(root,"OWNER_PROTOCOL_ADAPTATION_REGISTRY.json")
    execution=_load_json(root,"OWNER_EXECUTION_REGISTRY.json"); maintenance=_load_json(root,"SYSTEM_MAINTENANCE_POLICY.json"); harness=_load_json(root,"HARNESS_STATUS.json")
    task_manifest=_load_json(root,"tasks/universal-continuity-maintenance/TASK_MANIFEST.json"); generic_registry=_load_json(root,"GENERIC_TASK_REGISTRY.json")
    protocol=current.get("continuity_protocol_version")
    for label, value in (
        ("CONTINUITY_CONTRACT.schema_version",contract.get("schema_version")),("OWNER_ADAPTER_CONTRACT.continuity_contract",adapter.get("continuity_contract")),
        ("OWNER_REGISTRY.continuity_protocol_version",owner_registry.get("continuity_protocol_version")),("BARE_INHERIT_DISCOVERY.continuity_protocol_version",discovery.get("continuity_protocol_version")),
        ("OWNER_PROTOCOL_ADAPTATION_REGISTRY.current_continuity_protocol",adaptation.get("current_continuity_protocol")),("maintenance TASK_MANIFEST protocol",task_manifest.get("continuity_protocol_version")),
    ):
        if value != protocol: errors.append(f"{label} != current protocol")
    if task_manifest.get("system_maintenance_policy_version") != maintenance.get("schema_version"): errors.append("maintenance TASK_MANIFEST system_maintenance_policy_version is stale")
    if str(task_manifest.get("methodology_owner_declaration_contract_version")) != str(adapter.get("methodology_composition",{}).get("owner_declaration_contract_version")): errors.append("maintenance TASK_MANIFEST methodology owner declaration contract is stale")
    errors.extend(_methodology_separation_errors(adapter)); errors.extend(validate_owner_registry(owner_registry))

    owner_map={e["name"]:e for e in owner_registry.get("owners",[]) if isinstance(e,dict) and e.get("name")}; adapt_map={e["owner"]:e for e in adaptation.get("owners",[]) if isinstance(e,dict) and e.get("owner")}; exec_map={e["owner"]:e for e in execution.get("owners",[]) if isinstance(e,dict) and e.get("owner")}
    expected=set(business_owner_names(owner_registry)); bare=bare_inherit_sources(owner_registry); bare_names={r["owner"] for r in bare}
    participant=discovery.get("participant_authority",{})
    if not isinstance(participant,dict) or participant.get("source")!="OWNER_REGISTRY.json": errors.append("BARE_INHERIT_DISCOVERY participant authority is not OWNER_REGISTRY.json")
    if isinstance(participant,dict) and participant.get("hard_coded_owner_list_allowed") is not False: errors.append("BARE_INHERIT_DISCOVERY permits parallel owner list")
    if "required_sources" in discovery: errors.append("BARE_INHERIT_DISCOVERY contains legacy hard-coded required_sources")
    if set(adapt_map)!=expected: errors.append("OWNER_PROTOCOL_ADAPTATION_REGISTRY owner set does not match OWNER_REGISTRY BUSINESS membership")
    if set(exec_map)!=expected: errors.append("OWNER_EXECUTION_REGISTRY owner set does not match OWNER_REGISTRY BUSINESS membership")

    for owner in sorted(expected.intersection(adapt_map)):
        entry=adapt_map[owner]; observed=entry.get("observed_protocol"); target=entry.get("target_protocol"); classification=entry.get("classification"); status=str(entry.get("status","")); registry_status=str(owner_map.get(owner,{}).get("adapter_status",""))
        if observed==target and classification!="COMPATIBLE": errors.append(f"{owner}: observed protocol equals target but classification is not COMPATIBLE")
        if observed==target and "PENDING_VALID_WRITER_RECONCILIATION" in status: errors.append(f"{owner}: stale pending reconciliation")
        if "RECONCILED" in registry_status and observed!=target: errors.append(f"{owner}: registry claims reconciled while adaptation is stale")

    lower_text=(json.dumps(owner_registry,ensure_ascii=False)+json.dumps(adaptation,ensure_ascii=False)).lower()
    if "or committed claim" in lower_text or "committed claim" in lower_text and "operational" in lower_text:
        errors.append("lower control surface still couples COMMITTED persistence status to operational assurance")

    generic={t["task_id"]:t for t in generic_registry.get("tasks",[]) if isinstance(t,dict) and t.get("task_id")}; cache=generic.get(task_manifest.get("task_id"))
    if not cache: errors.append("GENERIC_TASK_REGISTRY missing maintenance task cache entry")
    else:
        if cache.get("current_stage")!=task_manifest.get("current_stage"): errors.append("GENERIC_TASK_REGISTRY maintenance current_stage is stale")
        if cache.get("contract_version")!=task_manifest.get("contract_version"): errors.append("GENERIC_TASK_REGISTRY maintenance contract_version is stale")

    stage=str(task_manifest.get("current_stage","")); product=harness.get("product_e2e",{}); existing=product.get("existing_chat",{}).get("status"); fresh=product.get("fresh_chat",{}).get("status")
    if "KNOWN_TOPOLOGY_PRODUCT_E2E_PASS" in stage and (existing!="PASS" or fresh!="PASS"): errors.append("known-topology stage claim contradicts HARNESS_STATUS")
    if "OWNER_PROFILE_MIGRATION_IN_PROGRESS" in str(harness.get("status","")) and "OWNER_PROFILE_APPLICABILITY_GUARD_PASS" in stage: errors.append("HARNESS_STATUS still claims owner profile migration in progress")
    if harness.get("owner_operational_hardening",{}).get("financial_writing",{}).get("methodology_profile_refs") and "artifact_io" not in harness["owner_operational_hardening"]["financial_writing"]["methodology_profile_refs"]: errors.append("HARNESS_STATUS Financial methodology profile mirror is stale")

    for relative in _local_ref_candidates(task_manifest):
        if not (root/relative).exists(): errors.append(f"maintenance TASK_MANIFEST local artifact_ref missing: {relative}")
    resolver=owner_registry.get("resolver",{})
    for key in ("module","owner_topology","bare_inherit_policy","protocol_adaptation_registry","execution_readiness_contract","execution_registry","execution_evaluator"):
        relative=resolver.get(key)
        if relative and not (root/relative).exists(): errors.append(f"OWNER_REGISTRY resolver ref missing: {key}={relative}")
    if harness.get("startup_trigger",{}).get("acceptance_evidence",{}).get("live_candidate_names_persisted_in_public_harness") is not False: errors.append("public harness must not persist live candidate names/task ids")
    return {"status":"PASS" if not errors else "FAIL","errors":errors,"warnings":warnings,"checked_protocol":protocol,"checked_business_owners":sorted(expected),"checked_bare_inherit_owners":sorted(bare_names),"checked_core_invariants":list(CORE_CHECKS)}


def _fault_methodology_omission(root: Path) -> bool:
    contract=_load_json(root,"OWNER_ADAPTER_CONTRACT.json"); composition=contract["methodology_composition"]; profiles=composition["profiles"]
    app={p:{"status":"NOT_APPLICABLE","reason":"synthetic","evidence_refs":[f"x://{p}"]} for p in profiles}; app["artifact_io"]={"status":"APPLIES","reason":"writes files","evidence_refs":["x://file"]}
    owner={"methodology":{"profile_refs":{},"profile_applicability":app,"hook_bindings":{},"overrides":{}}}
    return "applicable_profile_not_declared:artifact_io" in evaluate_methodology_conformance(owner,contract).errors


def _fault_methodology_wrong_action(root: Path) -> bool:
    contract=_load_json(root,"OWNER_ADAPTER_CONTRACT.json"); c=contract["methodology_composition"]; profile=c["profiles"]["evolution"]; hooks=c["hook_sets"]["evolution"]
    app={p:{"status":"NOT_APPLICABLE","reason":"synthetic","evidence_refs":[f"x://{p}"]} for p in c["profiles"]}; app["evolution"]={"status":"APPLIES","reason":"learns","evidence_refs":["x://learn"]}
    owner={"methodology":{"profile_refs":{"evolution":profile["version"]},"profile_applicability":app,"hook_bindings":{h:f"x://{h}" for h in hooks},"overrides":{}}}
    run={"receipt_contract_version":c["operational_profile_run_contract_version"],"profile_id":"evolution","profile_version":"1.0","activation_id":"a1","trigger":"t","action_binding":{"task_id":"task-a","stage":"S","action_id":"a","subject_bindings":{"s":"1"},"input_bindings":{"i":"1"}},"invoked_hooks":[hooks[0]],"hook_assessments":{h:{"status":"INVOKED" if h==hooks[0] else "NOT_APPLICABLE_FOR_ACTION","reason":"synthetic","evidence_refs":[f"e://{h}"]} for h in hooks},"evidence_refs":["e://run"]}
    result=evaluate_operational_methodology_conformance(owner,contract,{"profile_runs":[run]},required_profiles=["evolution"],action_expectation={"task_id":"task-b","stage":"S","action_id":"a","subject_bindings":{"s":"1"},"input_bindings":{"i":"1"}},evidence_verifier=lambda r:True,assessment_verifier=lambda *args:True)
    return result.status=="FAIL" and any("action_binding_mismatch:evolution:task_id"==e for e in result.errors)


def run_synthetic_fault_injection(root: str | Path, scenarios: Iterable[str]) -> dict[str, Any]:
    root=Path(root); results: dict[str,str]={}
    for scenario in scenarios:
        passed=False
        try:
            if scenario=="methodology_applicable_profile_is_silently_omitted": passed=_fault_methodology_omission(root)
            elif scenario=="methodology_receipt_is_replayed_for_wrong_action": passed=_fault_methodology_wrong_action(root)
            elif scenario=="execution_receipt_omits_exact_expectation":
                receipt={"receipt_id":"r","action_id":"a","task_id":"t","stage":"s","capability_id":"c","executor_identity":"e","execution_ref":"x","subject_bindings":{"s":"1"},"input_bindings":{"i":"1"},"output_refs":["o"],"result":"PASS"}
                result=validate_execution_receipt_binding(receipt,{"task_id":"t"},replay_history_verifier=lambda h:True); passed=result.status==ReceiptBindingStatus.FAIL
            elif scenario=="execution_receipt_replay_history_is_unverified":
                receipt={"receipt_id":"r","action_id":"a","task_id":"t","stage":"s","capability_id":"c","executor_identity":"e","execution_ref":"x","subject_bindings":{"s":"1"},"input_bindings":{"i":"1"},"output_refs":["o"],"result":"PASS"}; expectation={"receipt_id":"unused","action_id":"a","task_id":"t","stage":"s","capability_id":"c","executor_identity":"e","subject_bindings":{"s":"1"},"input_bindings":{"i":"1"},"output_refs":["o"],"result":"PASS"}
                passed=validate_execution_receipt_binding(receipt,expectation).status==ReceiptBindingStatus.FAIL
            elif scenario=="isolated_execution_is_self_attested":
                profile={"owner":"o","repository":"r","capabilities":[{"capability_id":"c","scope":"x","assurance_ceiling":"ATTESTED_ISOLATED","invocation_path":"owner:run","executor_type":"x","evidence_contract":["x"],"side_channel_allowed":False}]}; obs={"capability_id":"c","availability":"AVAILABLE","observed_assurance":"ATTESTED_ISOLATED","execution_mode":"ISOLATED_EXTERNAL","executor_identity":"fake","proof_ref":"fake","route_ref":"owner:run"}
                passed=evaluate_execution(profile,[CapabilityRequirement("c",min_assurance=Assurance.ATTESTED_ISOLATED)],[obs]).status==RouteStatus.BLOCKED
            elif scenario=="incomplete_discovery_attempts_autoresume":
                raw={"task_id":"t","domain":"d","title":"t","display_name_zh":"t","recovery_owner":"o","status":"ACTIVE","task_class":"USER","resume_eligible":True,"resume_visibility":"DEFAULT","updated_at":"2026-10-10T00:00:00Z"}; candidates=resolve_candidates([TaskMetadata.from_mapping(raw)]); passed=not should_autoresume(candidates,hint_present=False,discovery_complete=False)
            elif scenario=="terminal_task_attempts_writer_takeover":
                raw={"task_id":"t","domain":"d","title":"t","display_name_zh":"t","recovery_owner":"o","status":"COMPLETE","task_class":"USER","resume_eligible":True,"resume_visibility":"EXPLICIT_ONLY","updated_at":"2026-10-10T00:00:00Z"}; task=TaskMetadata.from_mapping(raw)
                try: acquire_resume_lease(task,lease_id="x"); passed=False
                except ValueError: passed=True
            elif scenario=="material_write_reports_committed_without_authoritative_reread":
                from runtime.universal_continuity import build_turn_commit_receipt, CommitStatus
                raw={"task_id":"t","domain":"d","title":"t","display_name_zh":"t","recovery_owner":"o","status":"ACTIVE","task_class":"USER","resume_eligible":True,"resume_visibility":"DEFAULT","updated_at":"2026-10-10T00:00:00Z"}; task=acquire_resume_lease(TaskMetadata.from_mapping(raw),lease_id="x")
                passed=build_turn_commit_receipt(task,commit_required=True,write_succeeded=True,verified_after_write=False,lease_id="x",resume_epoch=1).commit_status==CommitStatus.COMMIT_FAILED
        except Exception:
            passed=False
        results[scenario]="PASS" if passed else "FAIL"
    failed=[name for name,status in results.items() if status!="PASS"]
    return {"status":"PASS" if not failed else "FAIL","results":results,"failed":failed}


def evaluate_owner_protocol_observation(adaptation_entry: dict[str, Any], *, authoritative_protocol: str, missing_remote_refs: Iterable[str] = ()) -> list[str]:
    errors=[]; owner=adaptation_entry.get("owner","UNKNOWN_OWNER"); target=adaptation_entry.get("target_protocol"); observed=adaptation_entry.get("observed_protocol")
    if authoritative_protocol!=target: errors.append(f"{owner}: authoritative owner protocol {authoritative_protocol} != target {target}")
    if authoritative_protocol==target and observed!=target: errors.append(f"{owner}: adaptation registry observed_protocol is stale")
    if authoritative_protocol==target and adaptation_entry.get("classification")!="COMPATIBLE": errors.append(f"{owner}: target protocol reached but classification is not COMPATIBLE")
    for ref in missing_remote_refs: errors.append(f"{owner}: dangling remote authority/conformance ref: {ref}")
    return errors


def main() -> int:
    parser=argparse.ArgumentParser(description="Universal Continuity risk-tiered system audit")
    parser.add_argument("--repo-root",default="."); parser.add_argument("--trigger",default="routine_change"); parser.add_argument("--changed-path",action="append",default=[])
    args=parser.parse_args(); root=Path(args.repo_root); owner_registry=_load_json(root,"OWNER_REGISTRY.json")
    plan=plan_audit(args.changed_path,args.trigger,owner_registry=owner_registry); local=audit_local_control_plane(root)
    faults=run_synthetic_fault_injection(root,plan["fault_injection_scenarios"]) if plan["fault_injection_scenarios"] else {"status":"NOT_SELECTED","results":{},"failed":[]}
    status="PASS" if local["status"]=="PASS" and faults["status"] in {"PASS","NOT_SELECTED"} else "FAIL"
    result={"status":status,"plan":plan,"local_audit":local,"synthetic_fault_injection":faults,"assurance_ceiling":"LOCAL_CONTROL_PLANE_AND_DETERMINISTIC_SYNTHETIC_FAULTS_ONLY; remote owner sweep requires maintenance-runner evidence when plan.remote_evidence_required=true"}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if status=="PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
