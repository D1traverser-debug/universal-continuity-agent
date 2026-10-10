import json
from pathlib import Path

from runtime.methodology_conformance import evaluate_methodology_conformance


ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    return json.loads((ROOT / "OWNER_ADAPTER_CONTRACT.json").read_text(encoding="utf-8"))


def make_binding_contract(profile_ids):
    contract = load_contract()
    composition = contract["methodology_composition"]
    profile_refs = {}
    hook_bindings = {}
    for profile_id in profile_ids:
        profile = composition["profiles"][profile_id]
        profile_refs[profile_id] = profile["version"]
        hook_set_name = profile["required_hooks_from"].split(".")[-1]
        for hook in composition["hook_sets"][hook_set_name]:
            hook_bindings[hook] = f"owner://hooks/{hook}"
    return contract, {
        "methodology": {
            "profile_refs": profile_refs,
            "hook_bindings": hook_bindings,
            "overrides": {"domain_taxonomy": "owner://taxonomy"},
        }
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


def test_methodology_composition_does_not_create_parallel_root_policy():
    contract = load_contract()
    composition = contract["methodology_composition"]

    assert composition["model"] == "SMALL_STABLE_KERNEL_PLUS_COMPOSABLE_PROFILES_PLUS_OWNER_LOCAL_BINDINGS"
    assert composition["owner_declaration_contract"]["copy_shared_profile_prose_into_owner_required"] is False
    assert composition["owner_declaration_contract"]["load_only_profiles_required_by_current_action"] is True
    assert composition["executable_validator"] == "runtime/methodology_conformance.py"
    assert not (ROOT / "METHODOLOGY_POLICY.json").exists()
    assert not (ROOT / "METHODOLOGY_PROFILE_POLICY.json").exists()
