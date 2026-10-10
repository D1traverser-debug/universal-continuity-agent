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
    return {
        "owner": "TEST_OWNER",
        "repository": "example/test-agent",
        "capabilities": list(capabilities),
    }


def _cap(
    capability_id: str,
    assurance: str,
    *,
    invocation_path: str = "runtime.executor:run",
    side_channel_allowed: bool = False,
    safe_degraded_modes=(),
):
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


def test_contract_file_declares_role_without_invocation_is_not_execution():
    contract = json.loads((ROOT / "EXECUTION_READINESS_CONTRACT.json").read_text(encoding="utf-8"))
    assert contract["schema_version"] == "1.0"
    assert contract["execution_receipt_binding_contract_version"] == "1.0"
    assert contract["execution_receipt_binding"]["validator"] == "runtime/execution_receipt.py"
    assert any("declared agent without an invocation path" in item for item in contract["hard_invariants"])
    assert any("Current-session availability" in item for item in contract["hard_invariants"])
    assert any("Receipt existence is not enough" in item for item in contract["hard_invariants"])
    assert any("shadow allowlist" in item for item in contract["hard_invariants"])


def test_owner_profile_rejects_fake_non_declared_prompt_only_path():
    profile = _profile(_cap("review", "HARNESS_WIRED", invocation_path="prompt only"))
    problems = validate_owner_profile(profile)
    assert "review:non_declared_assurance_without_real_invocation" in problems


def test_repository_wiring_without_session_handshake_is_blocked():
    profile = _profile(_cap("draft", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("draft")],
        [],
    )
    assert decision.status == RouteStatus.BLOCKED
    assert decision.blockers == ("session_capability_unobserved:draft",)


def test_declared_only_never_satisfies_execution_even_if_session_claims_available():
    profile = _profile(_cap("review", "DECLARED_ONLY"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("review")],
        [
            {
                "capability_id": "review",
                "availability": "AVAILABLE",
                "observed_assurance": "SESSION_EXECUTABLE",
                "execution_mode": "CHAT_BRIDGED",
            }
        ],
    )
    assert decision.status == RouteStatus.BLOCKED
    assert decision.blockers == ("declared_only:review",)


def test_chat_bridge_can_satisfy_normal_execution_when_owner_allows_that_assurance():
    profile = _profile(_cap("draft", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("draft", accepted_modes=("OWNER_NATIVE", "CHAT_BRIDGED"))],
        [
            {
                "capability_id": "draft",
                "availability": "AVAILABLE",
                "observed_assurance": "SESSION_EXECUTABLE",
                "execution_mode": "CHAT_BRIDGED",
                "executor_identity": "chat-session",
            }
        ],
    )
    assert decision.status == RouteStatus.READY
    assert decision.ready_capabilities == ("draft",)
    assert decision.execution_modes == ("CHAT_BRIDGED",)


def test_isolated_gate_cannot_be_satisfied_by_single_context_roleplay():
    profile = _profile(_cap("blind_multimodal_review", "ATTESTED_ISOLATED"))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("blind_multimodal_review", min_assurance=Assurance.ATTESTED_ISOLATED)],
        [
            {
                "capability_id": "blind_multimodal_review",
                "availability": "AVAILABLE",
                "observed_assurance": "SESSION_EXECUTABLE",
                "execution_mode": "CHAT_BRIDGED",
                "executor_identity": "same-chat-roleplay",
            }
        ],
    )
    assert decision.status == RouteStatus.BLOCKED
    assert "insufficient_assurance:blind_multimodal_review" in decision.blockers[0]


def test_isolated_gate_requires_attestation_identity_and_proof():
    profile = _profile(_cap("blind_multimodal_review", "ATTESTED_ISOLATED"))
    no_proof = evaluate_execution(
        profile,
        [CapabilityRequirement("blind_multimodal_review", min_assurance=Assurance.ATTESTED_ISOLATED)],
        [
            {
                "capability_id": "blind_multimodal_review",
                "availability": "AVAILABLE",
                "observed_assurance": "ATTESTED_ISOLATED",
                "execution_mode": "ISOLATED_EXTERNAL",
                "executor_identity": "provider-run-1",
            }
        ],
    )
    assert no_proof.status == RouteStatus.BLOCKED
    assert no_proof.blockers == ("isolated_execution_missing_attestation:blind_multimodal_review",)

    passed = evaluate_execution(
        profile,
        [CapabilityRequirement("blind_multimodal_review", min_assurance=Assurance.ATTESTED_ISOLATED)],
        [
            {
                "capability_id": "blind_multimodal_review",
                "availability": "AVAILABLE",
                "observed_assurance": "ATTESTED_ISOLATED",
                "execution_mode": "ISOLATED_EXTERNAL",
                "executor_identity": "provider-run-1",
                "proof_ref": "trace://provider/run-1",
            }
        ],
    )
    assert passed.status == RouteStatus.READY


def test_optional_missing_capability_degrades_without_blocking_hard_ready_work():
    profile = _profile(_cap("core", "SESSION_EXECUTABLE"))
    decision = evaluate_execution(
        profile,
        [
            CapabilityRequirement("core"),
            CapabilityRequirement("nice_to_have", hard=False),
        ],
        [
            {
                "capability_id": "core",
                "availability": "AVAILABLE",
                "observed_assurance": "SESSION_EXECUTABLE",
                "execution_mode": "OWNER_NATIVE",
            }
        ],
    )
    assert decision.status == RouteStatus.DEGRADED
    assert decision.ready_capabilities == ("core",)
    assert decision.degraded_capabilities == ("missing_owner_capability:nice_to_have",)


def test_partial_capability_requires_explicit_safe_degraded_mode():
    profile = _profile(_cap("research", "SESSION_EXECUTABLE", safe_degraded_modes=("CHAT_BRIDGED",)))
    decision = evaluate_execution(
        profile,
        [CapabilityRequirement("research")],
        [
            {
                "capability_id": "research",
                "availability": "PARTIAL",
                "observed_assurance": "SESSION_EXECUTABLE",
                "execution_mode": "CHAT_BRIDGED",
            }
        ],
    )
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
    github_owners = {
        item["name"]: item
        for item in registry["owners"]
        if item["name"] in expected_business
    }
    assert set(github_owners) == expected_business
    assert all(item.get("execution_capability_ref", "").endswith("continuity/EXECUTION_CAPABILITIES.json") for item in github_owners.values())
