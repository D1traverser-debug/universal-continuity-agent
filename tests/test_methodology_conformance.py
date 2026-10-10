import json
from pathlib import Path

from runtime.methodology_conformance import (
    evaluate_methodology_conformance,
    evaluate_operational_methodology_conformance,
)

ROOT = Path(__file__).resolve().parents[1]
ACTION_EXPECTATION = {
    "task_id": "task-1",
    "stage": "MAINTENANCE",
    "action_id": "action-1",
    "subject_bindings": {"system": "universal"},
    "input_bindings": {"authority_head": "sha256:head-1"},
}


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
            "reason": f"synthetic {'uses' if applies else 'does not use'} {profile_id}",
            "evidence_refs": [f"owner://surface/{profile_id}"],
        }
        if applies:
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


def action_scoped_profile_run(contract, profile_id, invoked_hooks, *, evidence_refs=None, action_binding=None):
    composition = contract["methodology_composition"]
    profile = composition["profiles"][profile_id]
    hook_set_name = profile["required_hooks_from"].split(".")[-1]
    hooks = list(composition["hook_sets"][hook_set_name])
    invoked = set(invoked_hooks)
    return {
        "receipt_contract_version": composition["operational_profile_run_contract_version"],
        "profile_id": profile_id,
        "profile_version": profile["version"],
        "activation_id": f"activation-{profile_id}",
        "trigger": "synthetic-action",
        "action_binding": dict(action_binding or ACTION_EXPECTATION),
        "invoked_hooks": sorted(invoked),
        "hook_assessments": {
            hook: {
                "status": "INVOKED" if hook in invoked else "NOT_APPLICABLE_FOR_ACTION",
                "reason": f"{hook} {'executed' if hook in invoked else 'is outside scope'} for this action",
                "evidence_refs": [f"evidence://{profile_id}/{hook}"],
            }
            for hook in hooks
        },
        "evidence_refs": evidence_refs or [f"evidence://{profile_id}/action"],
    }


def accept_all_assessments(profile_id, hook, status, reason, refs):
    return bool(profile_id and hook and status and reason and refs)


def operational(owner, contract, runs, profiles, *, expectation=ACTION_EXPECTATION, evidence_verifier=lambda ref: True, assessment_verifier=accept_all_assessments):
    return evaluate_operational_methodology_conformance(
        owner,
        contract,
        {"profile_runs": runs},
        required_profiles=profiles,
        action_expectation=expectation,
        evidence_verifier=evidence_verifier,
        assessment_verifier=assessment_verifier,
    )


def test_composable_profiles_accept_thin_owner_bindings():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    result = evaluate_methodology_conformance(owner, contract)
    assert result.status == "PASS"
    assert set(result.active_profiles) == {"artifact_io@1.0", "operational_hygiene@1.0", "evolution@1.0"}


def test_profile_version_is_pinned_not_floating_latest():
    contract, owner = make_binding_contract(["evolution"])
    owner["methodology"]["profile_refs"]["evolution"] = "latest"
    result = evaluate_methodology_conformance(owner, contract)
    assert result.status == "FAIL"
    assert any(x.startswith("profile_version_mismatch:evolution") for x in result.errors)


def test_missing_domain_hook_and_forbidden_override_fail_closed():
    contract, owner = make_binding_contract(["artifact_io"])
    owner["methodology"]["hook_bindings"].pop("post_write_verification_method")
    assert "missing_hook_binding:artifact_io:post_write_verification_method" in evaluate_methodology_conformance(owner, contract).errors
    contract, owner = make_binding_contract(["evolution"])
    owner["methodology"]["overrides"] = {"candidate_is_not_production_authority": False}
    assert "forbidden_override:candidate_is_not_production_authority" in evaluate_methodology_conformance(owner, contract).errors


def test_every_profile_requires_explicit_applicability_and_applicable_profile_cannot_be_omitted():
    contract, owner = make_binding_contract(["operational_hygiene"])
    owner["methodology"]["profile_applicability"].pop("artifact_io")
    assert "missing_profile_applicability:artifact_io" in evaluate_methodology_conformance(owner, contract).errors

    contract, owner = make_binding_contract(["operational_hygiene"])
    owner["methodology"]["profile_applicability"]["artifact_io"] = {
        "status": "APPLIES", "reason": "owner persists artifacts", "evidence_refs": ["owner://delivery"]
    }
    assert "applicable_profile_not_declared:artifact_io" in evaluate_methodology_conformance(owner, contract).errors


def test_declaration_pass_is_not_operational_pass():
    contract, owner = make_binding_contract(["operational_hygiene"])
    assert evaluate_methodology_conformance(owner, contract).status == "PASS"
    result = evaluate_operational_methodology_conformance(
        owner, contract, None,
        required_profiles=["operational_hygiene"],
        action_expectation=ACTION_EXPECTATION,
        evidence_verifier=lambda ref: True,
        assessment_verifier=accept_all_assessments,
    )
    assert result.status == "FAIL"
    assert result.errors == ("missing_operational_execution_evidence",)


def test_operational_pass_requires_both_independent_verifier_inputs():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    no_evidence_verifier = evaluate_operational_methodology_conformance(
        owner, contract, {"profile_runs": [run]}, required_profiles=["evolution"],
        action_expectation=ACTION_EXPECTATION, assessment_verifier=accept_all_assessments,
    )
    assert no_evidence_verifier.errors == ("independent_evidence_verifier_required",)
    no_semantic_verifier = evaluate_operational_methodology_conformance(
        owner, contract, {"profile_runs": [run]}, required_profiles=["evolution"],
        action_expectation=ACTION_EXPECTATION, evidence_verifier=lambda ref: True,
    )
    assert no_semantic_verifier.errors == ("independent_hook_assessment_verifier_required",)


def test_exact_action_expectation_is_mandatory_and_mismatch_fails():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    missing = evaluate_operational_methodology_conformance(
        owner, contract, {"profile_runs": [run]}, required_profiles=["evolution"],
        evidence_verifier=lambda ref: True, assessment_verifier=accept_all_assessments,
    )
    assert missing.errors == ("action_expectation_required",)

    wrong = dict(ACTION_EXPECTATION)
    wrong["action_id"] = "other-action"
    result = operational(owner, contract, [run], ["evolution"], expectation=wrong)
    assert result.status == "FAIL"
    assert "action_binding_mismatch:evolution:action_id" in result.errors


def test_action_binding_requires_nonempty_subject_and_input_expectations():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    wrong = dict(ACTION_EXPECTATION)
    wrong["subject_bindings"] = {}
    result = operational(owner, contract, [run], ["evolution"], expectation=wrong)
    assert "action_expectation_missing_or_invalid:subject_bindings" in result.errors


def test_duplicate_profile_runs_and_activation_ids_fail_closed():
    contract, owner = make_binding_contract(["evolution"])
    first = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    second = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    result = operational(owner, contract, [first, second], ["evolution"])
    assert result.status == "FAIL"
    assert "duplicate_operational_profile_run:evolution" in result.errors
    assert "duplicate_activation_id:activation-evolution" in result.errors


def test_receipt_contract_1_2_or_missing_action_binding_is_not_admissible_under_1_3():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    run["receipt_contract_version"] = "1.2"
    run.pop("action_binding")
    result = operational(owner, contract, [run], ["evolution"])
    assert result.status == "FAIL"
    assert "missing_action_binding:evolution" in result.errors
    assert any(x.startswith("operational_receipt_contract_version_mismatch:evolution") for x in result.errors)


def test_real_but_irrelevant_ref_cannot_launder_hook_claim():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"])
    def semantic_verifier(profile_id, hook, status, reason, refs):
        return hook != "eval_or_regression_promotion_path"
    result = operational(owner, contract, [run], ["evolution"], assessment_verifier=semantic_verifier)
    assert result.status == "FAIL"
    assert "unsupported_hook_assessment_claim:evolution:eval_or_regression_promotion_path:NOT_APPLICABLE_FOR_ACTION" in result.errors


def test_hook_negative_space_and_invoked_summary_are_enforced():
    contract, owner = make_binding_contract(["artifact_io"])
    run = action_scoped_profile_run(contract, "artifact_io", ["post_write_verification_method"])
    run["hook_assessments"].pop("delete_and_retention_rules")
    result = operational(owner, contract, [run], ["artifact_io"])
    assert "missing_hook_assessment:artifact_io:delete_and_retention_rules" in result.errors

    run = action_scoped_profile_run(contract, "artifact_io", ["post_write_verification_method"])
    run["invoked_hooks"] = ["stable_identity_strategy"]
    result = operational(owner, contract, [run], ["artifact_io"])
    assert any(x.startswith("invoked_hooks_mismatch:artifact_io:") for x in result.errors)


def test_unverified_profile_evidence_ref_fails():
    contract, owner = make_binding_contract(["evolution"])
    run = action_scoped_profile_run(contract, "evolution", ["learning_evidence_location"], evidence_refs=["trace://missing"])
    result = operational(owner, contract, [run], ["evolution"], evidence_verifier=lambda ref: ref != "trace://missing")
    assert "unverified_profile_evidence_ref:evolution:trace://missing" in result.errors


def test_only_activated_profiles_are_required():
    contract, owner = make_binding_contract(["artifact_io", "operational_hygiene", "evolution"])
    run = action_scoped_profile_run(contract, "artifact_io", ["post_write_verification_method"])
    result = operational(owner, contract, [run], ["artifact_io"])
    assert result.status == "PASS"
    assert result.required_profiles == ("artifact_io",)
    assert result.verified_profiles == ("artifact_io@1.0",)


def test_methodology_composition_contract_is_1_3_without_parallel_root_policy():
    contract = load_contract()
    composition = contract["methodology_composition"]
    run_contract = composition["operational_profile_run_contract"]
    assert composition["model"] == "SMALL_STABLE_KERNEL_PLUS_COMPOSABLE_PROFILES_PLUS_OWNER_LOCAL_BINDINGS"
    assert composition["operational_profile_run_contract_version"] == "1.3"
    assert run_contract["receipt_contract_version_required"] == "1.3"
    assert run_contract["action_binding_required"] is True
    assert run_contract["duplicate_profile_runs_fail_closed"] is True
    assert run_contract["independent_hook_assessment_verification_required"] is True
    assert not (ROOT / "METHODOLOGY_POLICY.json").exists()
    assert not (ROOT / "METHODOLOGY_PROFILE_POLICY.json").exists()


def test_entrypoint_preserves_persistence_assurance_separation():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "evaluate_operational_methodology_conformance" in entrypoint
    assert "declaration conformance, owner regression or CI must not substitute" in entrypoint
    assert "durable-persistence receipt" in entrypoint
    assert "Report assurance/gate state separately from commit status" in entrypoint
