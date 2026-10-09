import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_progressive_resume_load_order_is_narrow_to_deep():
    policy = load("CONTEXT_RECOVERY_POLICY.json")
    contract = load("CONTINUITY_CONTRACT.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    expected = [
        "metadata",
        "short_handoff",
        "exact_artifact_refs",
        "selective_search",
        "old_chat_history_last_resort",
    ]

    assert policy["schema_version"] == "1.0"
    assert contract["schema_version"] == "3.7"
    assert contract["context_recovery"]["resume_load_order"] == expected
    assert bootstrap["context_recovery"]["load_order"] == expected
    assert bootstrap["context_recovery"]["preload_entire_old_chat"] is False


def test_handoff_is_execution_truth_and_prefers_references():
    policy = load("CONTEXT_RECOVERY_POLICY.json")
    handoff = policy["handoff_contract"]

    assert policy["principles"]["checkpoint_is_execution_truth_not_transcript"] is True
    assert policy["principles"]["reference_existing_artifacts_instead_of_copying_them"] is True
    assert "current_stage" in handoff["must_include"]
    assert "next_action" in handoff["must_include"]
    assert "artifact_refs needed to verify next_action" in handoff["must_include"]
    assert "chat transcript" in handoff["must_not_duplicate"]


def test_task_topology_keeps_same_goal_and_splits_material_branches():
    policy = load("CONTEXT_RECOVERY_POLICY.json")
    topology = policy["task_topology"]

    assert "same task_id" in topology["CONTINUE_SAME_GOAL"]
    assert "same task_id" in topology["FRESH_HANDOFF_SAME_GOAL"]
    assert "do not mutate current_stage/next_action" in topology["SIDE_QUERY"]
    assert "parent_task_id" in topology["FORK_CHILD_TASK"]
    assert "new task_id" in topology["NEW_TASK"]


def test_no_fixed_context_token_threshold_becomes_system_invariant():
    policy = load("CONTEXT_RECOVERY_POLICY.json")
    contract = load("CONTINUITY_CONTRACT.json")

    assert policy["context_health"]["no_fixed_token_threshold"] is True
    assert contract["context_recovery"]["fixed_context_token_threshold_forbidden"] is True
    assert any("150K" in item for item in policy["context_health"]["signals_not_sufficient_alone"])


def test_verification_is_risk_matched_not_always_full_suite():
    policy = load("CONTEXT_RECOVERY_POLICY.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    assert policy["verification"]["low_risk_reversible_change"] == "targeted checks only"
    assert bootstrap["verification"]["broad_unrelated_tests_by_default"] is False
