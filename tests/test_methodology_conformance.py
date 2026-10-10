import json
from pathlib import Path

from runtime.methodology_conformance import (
    evaluate_methodology_conformance,
    evaluate_operational_methodology_conformance,
)


ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    return json.loads((ROOT / "OWNER_ADAPTER_CONTRACT.json").read_text(encoding="utf-8"))


def make_binding_contract(profile_ids):
    contract = load_contract()
    composition = contract["methodology_composition"]
    requested = set(profile_ids)
    profile_refs = {}
    profile_applicability = {}
    hook_bindings = {}
    for profile_id, profile in composition["profiles"].items():
        applies = profile_id in requested
        profile_applicability[profile_id] = {
            "status": "APPLIES" if applies else "NOT_APPLICABLE",
            "reason": (
                f"synthetic fixture exposes {profile_id} activation surface"
                if applies
                else f"synthetic fixture intentionally omits {profile_id} activation surface"
            ),
            "evidence_refs": [f"owner://surface/{profile_id}"],
        }
        if not applies:
            continue
        profile_refs[profile_id] = profile["version"]
        hook_set_name = profile["required_hooks_from"].split(".")[-1]
        for hook in composition["hook_sets"][hook_set_name]:
            hook_bindings[hook] = f"owner://hooks/{hook}"
    return contract, {
        "methodology": {
            "profile_refs": profile_refs,
            "profile_applicability": profile_applicability,
            "hook_bindings": hook_bindings,
            "overrides": {"domain_taxonomy": "owner://taxonomy"},
        }
    }


def profile_run(contract, profile_id, *, evidence_refs=None, invoked_hooks=None):
    """Legacy receipt fixture: absence of hook_assessments means every hook must be invoked."""
    composition = contract["methodology_composition"]
    profile = composition["profiles"][profile_id]
    hook_set_name = profile["required_hooks_from"].split(".")[-1]
    return {
        "profile_id": profile_id,
        "profile_version": profile["version"],
        "activation_id": f"activation-{profile_id}",
        "trigger": "test-trigger",
        "invoked_hooks": invoked_hooks if invoked_hooks is not None else list(composition["hook_sets"][hook_set_name]),
        "evidence_refs": evidence_refs if evidence_refs is not None else [f"evidence://{profile_id}/1"],
    }


def action_scoped_profile_run(contract, profile_id, invoked_hooks, *, evidence_refs=None):
    composition = contract["methodology_composition"]
    profile = composition["profiles"][profile_id]
    hook_set_name = profile["required_hooks_from"].split(".")[-1]
    hooks = list(composition["hook_sets"][hook_set_name])
    invoked = set(invoked_hooks)
    return {
        "profile_id": profile_id,
        "profile_version": profile["version"],
        "activation_id": f"action-activation-{profile_id}",
        "trigger": "action-scoped-test-trigger",
        "invoked_hooks": sorted(invoked),
        "hook_assessments": {
            hook: {
                "status": "INVOKED" if hook in invoked else "NOT_APPLICABLE_FOR_ACTION",
                "reason": (
                    f"{hook} executed for this synthetic action"
                    if hook in invoked
                    else f"{hook} is outside this synthetic action's scope"
                ),
                "evidence_refs": [f"evidence://{profile_id}/{hook}"],
            }
            for hook in hooks
        },
        "evidence_refs": evidence_refs if evidence_refs is not None else [f"evidence://{profile_id}/action"],
    }


def test_composable_profiles_accept_thin_owner_bindings():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "PASS"
    assert result.errors == ()
    assert set(result.active_profiles) == {
        "artifact_io@1.0",
        "operational_hygiene@1.0",
        "evolution@1.0",
    }


def test_profile_version_is_pinned_not_floating_latest():
    contract, owner = make_binding_contract(["evolution"])
    owner["methodology"]["profile_refs"]["evolution"] = "latest"

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert any(error.startswith("profile_version_mismatch:evolution") for error in result.errors)


def test_missing_domain_hook_fails_closed():
    contract, owner = make_binding_contract(["artifact_io"])
    owner["methodology"]["hook_bindings"].pop("post_write_verification_method")

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "missing_hook_binding:artifact_io:post_write_verification_method" in result.errors


def test_owner_cannot_override_kernel_invariant():
    contract, owner = make_binding_contract(["operational_hygiene"])
    owner["methodology"]["overrides"] = {
        "candidate_is_not_production_authority": False,
    }

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "forbidden_override:candidate_is_not_production_authority" in result.errors


def test_every_contract_profile_requires_explicit_applicability_assessment():
    contract, owner = make_binding_contract(["operational_hygiene", "evolution"])
    owner["methodology"]["profile_applicability"].pop("artifact_io")

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "missing_profile_applicability:artifact_io" in result.errors


def test_applicable_profile_cannot_be_silently_omitted():
    contract, owner = make_binding_contract(["operational_hygiene", "evolution"])
    owner["methodology"]["profile_applicability"]["artifact_io"] = {
        "status": "APPLIES",
        "reason": "owner creates and renders persistent publication artifacts",
        "evidence_refs": ["owner://runtime/delivery"],
    }

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "applicable_profile_not_declared:artifact_io" in result.errors


def test_not_applicable_profile_requires_reason_and_evidence():
    contract, owner = make_binding_contract(["operational_hygiene"])
    owner["methodology"]["profile_applicability"]["artifact_io"] = {
        "status": "NOT_APPLICABLE",
        "reason": "",
        "evidence_refs": [],
    }

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "missing_profile_applicability_reason:artifact_io" in result.errors
    assert "missing_profile_applicability_evidence_refs:artifact_io" in result.errors


def test_declared_profile_cannot_be_marked_not_applicable():
    contract, owner = make_binding_contract(["artifact_io"])
    owner["methodology"]["profile_applicability"]["artifact_io"]["status"] = "NOT_APPLICABLE"

    result = evaluate_methodology_conformance(owner, contract)

    assert result.status == "FAIL"
    assert "profile_declared_but_marked_not_applicable:artifact_io" in result.errors


def test_declaration_pass_is_not_operational_pass():
    contract, owner = make_binding_contract(["operational_hygiene"])
    declared = evaluate_methodology_conformance(owner, contract)
    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        None,
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: True,
    )

    assert declared.status == "PASS"
    assert operational.status == "FAIL"
    assert operational.errors == ("missing_operational_execution_evidence",)


def test_self_reported_receipt_without_independent_verifier_cannot_pass():
    contract, owner = make_binding_contract(["operational_hygiene"])
    evidence = {"profile_runs": [profile_run(contract, "operational_hygiene")]}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["operational_hygiene"],
    )

    assert operational.status == "FAIL"
    assert operational.errors == ("independent_evidence_verifier_required",)


def test_operational_conformance_rejects_unverified_evidence_ref():
    contract, owner = make_binding_contract(["operational_hygiene"])
    evidence = {"profile_runs": [profile_run(contract, "operational_hygiene", evidence_refs=["trace://missing"])]}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: False,
    )

    assert operational.status == "FAIL"
    assert "unverified_profile_evidence_ref:operational_hygiene:trace://missing" in operational.errors


def test_legacy_operational_receipt_still_requires_all_profile_hooks():
    contract, owner = make_binding_contract(["operational_hygiene"])
    all_hooks = contract["methodology_composition"]["hook_sets"]["operational_hygiene"]
    observed = [hook for hook in all_hooks if hook != "reliability_or_change_freeze_guard"]
    evidence = {"profile_runs": [profile_run(contract, "operational_hygiene", invoked_hooks=observed)]}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert "required_hook_not_observed:operational_hygiene:reliability_or_change_freeze_guard" in operational.errors


def test_action_scoped_receipt_can_pass_with_real_subset_and_explicit_negative_space():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    invoked = ["learning_evidence_location"]
    run = action_scoped_profile_run(contract, "evolution", invoked)
    evidence = {"profile_runs": [run]}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["evolution"],
        evidence_verifier=lambda ref: ref.startswith("evidence://evolution/"),
    )

    assert operational.status == "PASS"
    assert operational.verified_profiles == ("evolution@1.0",)
    assert operational.errors == ()


def test_action_scoped_receipt_rejects_missing_hook_assessment():
    contract, owner = make_binding_contract(["artifact_io"])
    run = action_scoped_profile_run(contract, "artifact_io", ["post_write_verification_method"])
    run["hook_assessments"].pop("delete_and_retention_rules")

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["artifact_io"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert "missing_hook_assessment:artifact_io:delete_and_retention_rules" in operational.errors


def test_action_scoped_not_applicable_requires_reason_and_verified_evidence():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    assessment = run["hook_assessments"]["eval_or_regression_promotion_path"]
    assessment["reason"] = ""
    assessment["evidence_refs"] = []

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["evolution"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert "missing_hook_assessment_reason:evolution:eval_or_regression_promotion_path" in operational.errors
    assert "missing_hook_assessment_evidence_refs:evolution:eval_or_regression_promotion_path" in operational.errors


def test_action_scoped_receipt_requires_at_least_one_invoked_hook():
    contract, owner = make_binding_contract(["operational_hygiene"])
    run = action_scoped_profile_run(contract, "operational_hygiene", [])

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert "no_invoked_hooks_for_action:operational_hygiene" in operational.errors


def test_action_scoped_receipt_rejects_invoked_hook_summary_mismatch():
    contract, owner = make_binding_contract(["operational_hygiene"])
    run = action_scoped_profile_run(contract, "operational_hygiene", ["observability_or_incident_evidence_location"])
    run["invoked_hooks"] = ["self_maintenance_trigger_path"]

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert any(error.startswith("invoked_hooks_mismatch:operational_hygiene:") for error in operational.errors)


def test_action_scoped_receipt_rejects_unknown_hook_assessment():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    run["hook_assessments"]["invented_hook"] = {
        "status": "NOT_APPLICABLE_FOR_ACTION",
        "reason": "synthetic",
        "evidence_refs": ["evidence://evolution/invented"],
    }

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": [run]},
        required_profiles=["evolution"],
        evidence_verifier=lambda ref: True,
    )

    assert operational.status == "FAIL"
    assert "unknown_hook_assessment:evolution:invented_hook" in operational.errors


def test_operational_conformance_passes_legacy_all_hooks_receipt_with_verified_evidence():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    evidence = {
        "profile_runs": [
            profile_run(contract, "operational_hygiene", evidence_refs=["trace://incident/1", "eval://regression/1"]),
        ]
    }
    verified = {"trace://incident/1", "eval://regression/1"}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["operational_hygiene"],
        evidence_verifier=lambda ref: ref in verified,
    )

    assert operational.status == "PASS"
    assert operational.required_profiles == ("operational_hygiene",)
    assert operational.verified_profiles == ("operational_hygiene@1.0",)
    assert operational.errors == ()


def test_operational_conformance_does_not_force_unactivated_profiles():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    evidence = {"profile_runs": [profile_run(contract, "artifact_io")]}

    operational = evaluate_operational_methodology_conformance(
        owner,
        contract,
        evidence,
        required_profiles=["artifact_io"],
        evidence_verifier=lambda ref: ref.startswith("evidence://artifact_io/"),
    )

    assert operational.status == "PASS"
    assert operational.required_profiles == ("artifact_io",)
    assert operational.verified_profiles == ("artifact_io@1.0",)


def test_methodology_composition_does_not_create_parallel_root_policy():
    contract = load_contract()
    composition = contract["methodology_composition"]

    assert composition["model"] == "SMALL_STABLE_KERNEL_PLUS_COMPOSABLE_PROFILES_PLUS_OWNER_LOCAL_BINDINGS"
    assert composition["owner_declaration_contract"]["copy_shared_profile_prose_into_owner_required"] is False
    assert composition["owner_declaration_contract"]["load_only_profiles_required_by_current_action"] is True
    assert composition["owner_declaration_contract"]["profile_applicability_required_for_every_contract_profile"] is True
    assert composition["operational_profile_run_contract_version"] == "1.1"
    assert composition["operational_profile_run_contract"]["every_profile_hook_must_be_assessed"] is True
    assert composition["operational_profile_run_contract"]["at_least_one_hook_must_be_invoked"] is True
    assert composition["executable_validator"] == "runtime/methodology_conformance.py"
    assert not (ROOT / "METHODOLOGY_POLICY.json").exists()
    assert not (ROOT / "METHODOLOGY_PROFILE_POLICY.json").exists()


def test_entrypoint_requires_action_level_operational_methodology_evidence():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")

    assert "evaluate_operational_methodology_conformance" in entrypoint
    assert "profile_runs" in entrypoint
    assert "independent" in entrypoint.lower() and "evidence verifier" in entrypoint.lower()
    assert "declaration conformance, owner regression or CI must not substitute" in entrypoint
    assert "COMMITTED" in entrypoint and "operational conformance" in entrypoint
