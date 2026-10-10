import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_artifact_context_governance_policy_core_invariants():
    policy = json.loads((ROOT / "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json").read_text(encoding="utf-8"))

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
    policy = json.loads((ROOT / "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json").read_text(encoding="utf-8"))
    rule = policy["chat_only_material_change_rule"]

    assert "exists only in chat" in rule["principle"]
    assert "Persist" in rule["before_claiming_committed"]
    assert "NO_MATERIAL_CHANGE" in rule["otherwise"]
    assert "COMMIT_FAILED" in rule["otherwise"]


def test_instruction_precedence_is_not_confused_with_business_authority():
    policy = json.loads((ROOT / "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json").read_text(encoding="utf-8"))
    boundary = policy["behavioral_instruction_vs_data_authority"]

    assert "separate concepts" in boundary["rule"]
    assert "override global Custom Instructions" in boundary["project_instructions"]
    assert "not executable checkpoint authority" in boundary["memory_library_connected_apps"]
    assert "do not silently merge" in boundary["conflict_behavior"]
