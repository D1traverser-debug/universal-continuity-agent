import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_startup_hook_is_required_for_bare_inherit():
    contract = load("CONTINUITY_CONTRACT.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    assert contract["schema_version"] == "3.7"
    assert contract["startup_trigger"]["required_for_bare_inherit"] is True
    assert contract["startup_trigger"]["automatic_library_event_listener_claim"] is False
    assert contract["startup_trigger"]["automatic_github_event_listener_claim"] is False
    assert contract["startup_trigger"]["missing_trigger_result"] == "CONTINUITY_BOOTSTRAP_NOT_TRIGGERED"

    assert bootstrap["schema_version"] == "1.6"
    assert bootstrap["startup_hook"]["required"] is True
    assert bootstrap["startup_hook"]["github_or_library_files_auto_load"] is False
    assert bootstrap["degraded_mode"]["startup_hook_missing"].startswith("CONTINUITY_BOOTSTRAP_NOT_TRIGGERED")


def test_continue_intent_precedes_learning_only_new_task_rule():
    contract = load("CONTINUITY_CONTRACT.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    assert contract["startup_trigger"]["explicit_continue_intent_precedes_new_task_learning_rule"] is True
    assert contract["rules"]["explicit_continue_command_must_trigger_continuity_before_learning_only_reply"] is True
    assert "Explicit 继承/继续/恢复 intent" in bootstrap["startup_hook"]["continue_intent_precedence"]


def test_harness_records_real_account_hook_end_to_end_acceptance():
    status = load("HARNESS_STATUS.json")
    trigger = status["startup_trigger"]
    evidence = trigger["acceptance_evidence"]

    assert status["schema_version"] == "3.7"
    assert trigger["account_level_hook_required"] is True
    assert trigger["end_to_end_bare_inherit_claim"] is True
    assert evidence["bare_command"] == "继承"
    assert evidence["required_owner_quorum"] == 5
    assert evidence["required_owner_quorum_succeeded"] is True
    assert evidence["authoritative_default_candidate_count"] == 4
    assert evidence["live_candidate_names_persisted_in_public_harness"] is False


def test_startup_hook_document_contains_acceptance_command_and_failure_mode():
    text = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")
    assert "继承" in text
    assert "Custom Instructions" in text
    assert "CONTINUITY_BOOTSTRAP_UNAVAILABLE" in text
    assert "继承前进度" in text
    assert "进度提交" in text
    assert "CONTINUITY_BOOTSTRAP_NOT_TRIGGERED" not in text or "not a Continuity success" in text
