import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy():
    return json.loads((ROOT / "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json").read_text(encoding="utf-8"))


def test_artifact_context_governance_policy_core_invariants():
    policy = load_policy()
    assert policy["status"] == "ACTIVE"
    classes = policy["storage_classes"]
    for required in (
        "ENGINEERING_AUTHORITY",
        "DURABLE_TASK_STATE",
        "BUSINESS_EVIDENCE",
        "LEARNING_EVIDENCE",
        "REBUILDABLE_CACHE",
        "SESSION_SCRATCH",
        "EXTERNAL_REFERENCE",
        "CHAT_PERSONALIZATION_CONTEXT",
    ):
        assert required in classes
    assert classes["REBUILDABLE_CACHE"]["may_drive_execution"] is False
    assert classes["SESSION_SCRATCH"]["may_drive_execution"] is False
    assert classes["CHAT_PERSONALIZATION_CONTEXT"]["may_drive_execution"] is False
    assert policy["recovery_rule"]["cache_never_satisfies_authority_read"] is True


def test_chat_only_material_change_cannot_masquerade_as_durable_evolution():
    rule = load_policy()["chat_only_material_change_rule"]
    assert "exists only in chat" in rule["principle"]
    assert "Persist" in rule["before_claiming_committed"]
    assert "NO_MATERIAL_CHANGE" in rule["otherwise"]
    assert "COMMIT_FAILED" in rule["otherwise"]


def test_instruction_precedence_is_not_confused_with_business_authority():
    boundary = load_policy()["authority_rules"]
    assert boundary["instruction_precedence_is_separate_from_business_data_authority"] is True
    assert "override global Custom Instructions" in boundary["project_instructions"]
    assert "not executable checkpoint authority" in boundary["memory_library_connected_apps"]
    assert "Do not silently merge" in boundary["conflict_behavior"]


def test_material_file_mutation_requires_verified_postcondition_and_identity():
    policy = load_policy()
    tx = policy["verified_file_operation_transaction"]
    assert "VERIFY_STABLE_IDENTITY_AND_CURRENT_VERSION_WHEN_MATERIAL" in tx["steps"]
    assert "VERIFY_POSTCONDITION_BY_REREAD_OR_PROVIDER_METADATA" in tx["steps"]
    assert "Tool success alone is not postcondition proof" in tx["write_commit_semantics"]
    assert "do not delete" in tx["delete_semantics"].lower()
    assert policy["failure_semantics"]["write_postcondition_not_verified"] == "COMMIT_FAILED_OR_OWNER_EQUIVALENT"


def test_external_stores_cannot_silently_become_control_plane_authority():
    ext = load_policy()["external_storage"]
    assert ext["chatgpt_library"]["durable_control_plane_dependency_allowed"] is False
    assert ext["notion"]["durable_control_plane_dependency_allowed"] is False
    assert ext["google_drive"]["durable_control_plane_dependency_allowed"] is False
    assert "user-facing Word/PDF/slides/spreadsheets" in ext["google_drive"]["allowed_for"]
    assert "implicit runtime checkpoint" in ext["google_drive"]["not_allowed_as"]


def test_owner_contract_requires_file_operation_conformance():
    contract = json.loads((ROOT / "OWNER_ADAPTER_CONTRACT.json").read_text(encoding="utf-8"))
    gov = contract["artifact_context_governance"]
    required = set(gov["owner_must_expose"])
    assert {
        "canonical_artifact_or_file_stores",
        "stable_identity_strategy",
        "read_freshness_requirements",
        "mutation_conflict_strategy",
        "post_write_verification_method",
        "delete_and_retention_rules",
        "external_artifact_vault_if_any",
    } <= required
    assert gov["tool_success_alone_is_commit_proof"] is False
    assert gov["destructive_mutation_requires_stable_identity_and_dependency_check"] is True


def test_file_operation_rules_are_consolidated_not_parallel_root_policy():
    assert not (ROOT / "FILE_OPERATION_GOVERNANCE_POLICY.json").exists()
