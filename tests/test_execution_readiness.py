import json
from pathlib import Path

from runtime.execution_readiness import (
    Assurance,
    CapabilityRequirement,
    RouteStatus,
    evaluate_execution,
    validate_owner_profile,
)
from runtime.owner_topology import business_owner_names

ROOT = Path(__file__).resolve().parents[1]


def _profile(*capabilities):
    return {"owner": "TEST_OWNER", "repository": "example/test-agent", "capabilities": list(capabilities)}


def _cap(capability_id: str, assurance: str, *, invocation_path="runtime.executor:run", side_channel_allowed=False, safe_degraded_modes=()):
    return {
        "capability_id": capability_id,
        "scope": "TEST",
        "assurance_ceiling": assurance,
        "invocation_path": invocation_path,
        "executor_type": "PYTHON_RUNTIME",
        "evidence_contract": ["execution_receipt"],
        "side_channel_allowed": side_channel_allowed,
        "safe_degraded_modes": list(safe_degraded_modes),
    }


def _obs(capability_id, assurance="SESSION_EXECUTABLE", mode="OWNER_NATIVE", **extra):
    raw = {
        "capability_id": capability_id,
        "availability": "AVAILABLE",
        "observed_assurance": assurance,
        "execution_mode": mode,
        "route_ref": "runtime.executor:run",
    }
    raw.update(extra)
    return raw


def test_contract_file_declares_role_without_invocation_is_not_execution():
    contract = json.loads((ROOT / "EXECUTION_READINESS_CONTRACT.json").read_text(encoding="utf-8"))
    assert contract["schema_version"] == "1.0"
    assert any("declared agent without an invocation path" in item for item in contract["hard_invariants"])
    assert any("Current-session availability" in item for item in contract["hard_invariants"])
    assert any("Receipt existence is not enough" in item for item in contract["hard_invariants"])
    assert any("shadow allowlist" in item for item in contract["hard_invariants"])


def test_owner_profile_rejects_fake_non_declared_prompt_only_path():
    profile = _profile(_cap("review", "HARNESS_WIRED", invocation_path="prompt only"))
    assert "review:non_declared_assurance_without_real_invocation" in validate_owner_profile(profile)


def test_owner_profile_rejects_string_boolean_side_channel_flag():
    malformed = _cap("review", "SESSION_EXECUTABLE")
    malformed["side_channel_allowed"] = "false"
    problems = validate_owner_profile(_profile(malformed))
    assert any("side_channel_allowed must be boolean" in item for item in problems)


def test_repository_wiring_without_session_handshake_is_blocked():
    decision = evaluate_execution(_profile(_cap("draft", "SESSION_EXECUTABLE")), [CapabilityRequirement("draft")], [])
    assert decision.status == RouteStatus.BLOCKED
    assert decision.blockers == ("session_capability_unobserved:draft",)


def test_declared_only_never_satisfies_execution_even_if_session_claims_available():
    decision = evaluate_execution(
        _profile(_cap("review", "DECLARED_ONLY")),
        [CapabilityRequirement("review")],
        [_obs("review")],
    )
    assert decision.status == RouteStatus.BLOCKED
    assert decision.blockers == ("declared_only:review",)


def test_owner_forbidden_side_channel_requires_exact_owner_route_observation():
    profile = _profile(_cap("draft", "SESSION_EXECUTABLE", invocation_path="owner.gateway:run"))
    missing = _obs("draft")
    missing.pop("route_ref")
    decision = evaluate_execution(profile, [CapabilityRequirement("draft")], [missing])
    assert decision.blockers == ("owner_route_unobserved:draft",)

    wrong = _obs("draft", route_ref="chat->tool")
    decision = evaluate_execution(profile, [CapabilityRequirement("draft")], [wrong])
    assert decision.blockers == ("owner_route_mismatch:draft",)

    ready = _obs("draft", route_ref="owner.gateway:run")
    decision = evaluate_execution(profile, [CapabilityRequirement("draft")], [ready])
    assert decision.status == RouteStatus.READY


def test_chat_bridge_can_satisfy_normal_execution_when_routed_through_owner_path():
    profile = _profile(_cap("draft", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("draft", accepted_modes=("OWNER_NATIVE", "CHAT_BRIDGED"))],
        [_obs("draft", mode="CHAT_BRIDGED", executor_identity="chat-session")],
    )
    assert decision.status == RouteStatus.READY
    assert decision.ready_capabilities == ("draft",)


def test_duplicate_session_observations_fail_closed_instead_of_last_write_wins():
    profile = _profile(_cap("draft", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(profile, [CapabilityRequirement("draft")], [_obs("draft"), _obs("draft", mode="CHAT_BRIDGED")])
    assert decision.status == RouteStatus.BLOCKED
    assert decision.blockers == ("duplicate_session_observation:draft",)


def test_isolated_gate_cannot_be_satisfied_by_single_context_roleplay():
    profile = _profile(_cap("blind_multimodal_review", "ATTESTED_ISOLATED"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("blind_multimodal_review", min_assurance=Assurance.ATTESTED_ISOLATED)],
        [_obs("blind_multimodal_review", assurance="SESSION_EXECUTABLE", mode="CHAT_BRIDGED", executor_identity="same-chat-roleplay")],
    )
    assert decision.status == RouteStatus.BLOCKED
    assert "insufficient_assurance:blind_multimodal_review" in decision.blockers[0]


def test_isolated_gate_requires_verified_attestation_not_nonempty_strings():
    profile = _profile(_cap("blind_multimodal_review", "ATTESTED_ISOLATED"))
    req = [CapabilityRequirement("blind_multimodal_review", min_assurance=Assurance.ATTESTED_ISOLATED)]
    observation = _obs(
        "blind_multimodal_review",
        assurance="ATTESTED_ISOLATED",
        mode="ISOLATED_EXTERNAL",
        executor_identity="provider-run-1",
        proof_ref="trace://provider/run-1",
    )

    no_verifier = evaluate_execution(profile, req, [observation])
    assert no_verifier.status == RouteStatus.BLOCKED
    assert no_verifier.blockers == ("isolated_execution_attestation_verifier_required:blind_multimodal_review",)

    rejected = evaluate_execution(profile, req, [observation], attestation_verifier=lambda obs: False)
    assert rejected.blockers == ("isolated_execution_attestation_unverified:blind_multimodal_review",)

    passed = evaluate_execution(profile, req, [observation], attestation_verifier=lambda obs: obs.proof_ref == "trace://provider/run-1")
    assert passed.status == RouteStatus.READY


def test_isolated_gate_requires_isolated_external_mode():
    profile = _profile(_cap("review", "ATTESTED_ISOLATED"))
    observation = _obs("review", assurance="ATTESTED_ISOLATED", mode="OWNER_NATIVE", executor_identity="x", proof_ref="trace://x")
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("review", min_assurance=Assurance.ATTESTED_ISOLATED)],
        [observation],
        attestation_verifier=lambda obs: True,
    )
    assert decision.blockers == ("isolated_execution_mode_invalid:review:OWNER_NATIVE",)


def test_optional_missing_capability_degrades_without_blocking_hard_ready_work():
    profile = _profile(_cap("core", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("core"), CapabilityRequirement("nice_to_have", hard=False)],
        [_obs("core")],
    )
    assert decision.status == RouteStatus.DEGRADED
    assert decision.ready_capabilities == ("core",)
    assert decision.degraded_capabilities == ("missing_owner_capability:nice_to_have",)


def test_partial_capability_requires_explicit_safe_degraded_mode():
    profile = _profile(_cap("research", "SESSION_EXECUTABLE", safe_degraded_modes=("CHAT_BRIDGED",)))
    obs = _obs("research", mode="CHAT_BRIDGED")
    obs["availability"] = "PARTIAL"
    decision = evaluate_execution(profile, [CapabilityRequirement("research")], [obs])
    assert decision.status == RouteStatus.DEGRADED
    assert decision.degraded_capabilities == ("safe_degraded:research:CHAT_BRIDGED",)


def test_cross_agent_registry_covers_current_github_business_agents_dynamically():
    registry = json.loads((ROOT / "OWNER_EXECUTION_REGISTRY.json").read_text(encoding="utf-8"))
    owner_registry = json.loads((ROOT / "OWNER_REGISTRY.json").read_text(encoding="utf-8"))
    owners = {item["owner"]: item for item in registry["owners"]}
    expected_business = set(business_owner_names(owner_registry))
    assert registry["execution_readiness_contract"] == "EXECUTION_READINESS_CONTRACT.json"
    assert set(owners) == expected_business
    for item in owners.values():
        assert item["capability_ref"] == "continuity/EXECUTION_CAPABILITIES.json"
        assert "@main" in item["repository"]


def test_continuity_owner_router_points_to_execution_control_plane_without_name_allowlist():
    registry = json.loads((ROOT / "OWNER_REGISTRY.json").read_text(encoding="utf-8"))
    resolver = registry["resolver"]
    assert resolver["execution_readiness_contract"] == "EXECUTION_READINESS_CONTRACT.json"
    assert resolver["execution_registry"] == "OWNER_EXECUTION_REGISTRY.json"
    assert resolver["execution_evaluator"] == "runtime/execution_readiness.py"
    expected_business = set(business_owner_names(registry))
    github_owners = {item["name"]: item for item in registry["owners"] if item["name"] in expected_business}
    assert set(github_owners) == expected_business
    assert all(item.get("execution_capability_ref", "").endswith("continuity/EXECUTION_CAPABILITIES.json") for item in github_owners.values())
