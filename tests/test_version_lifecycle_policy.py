import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_current_protocol_is_single_and_user_does_not_migrate():
    current = load("CURRENT_PROTOCOL.json")
    lifecycle = load("VERSION_LIFECYCLE_POLICY.json")
    assert current["continuity_protocol_version"] == "3.7"
    assert current["user_migration_required"] is False
    assert current["chat_protocol_version_pinned_at_creation"] is False
    assert lifecycle["active_working_tree"]["active_protocol_count"] == 1
    assert lifecycle["active_working_tree"]["active_protocol"] == "3.7"
    assert lifecycle["chat_behavior"]["user_migration_required"] is False
    assert lifecycle["chat_behavior"]["protocol_version_pinned_at_chat_creation"] is False


def test_same_chat_reconciliation_does_not_steal_lease():
    policy = load("LIVE_CHAT_RECONCILIATION_POLICY.json")
    lease = policy["lease_rules"]
    assert lease["same_chat_protocol_upgrade_increments_resume_epoch"] is False
    assert lease["same_chat_protocol_upgrade_replaces_active_lease"] is False
    assert lease["new_chat_takeover_increments_resume_epoch"] is True
    assert lease["new_chat_takeover_replaces_active_lease"] is True
    assert policy["user_responsibility"]["manual_old_chat_restart"] is False


def test_task_manifest_template_uses_current_protocol_and_separates_contracts():
    template = load("tasks/_TASK_MANIFEST_TEMPLATE.json")
    assert template["schema_version"] == "3.7"
    assert template["continuity_protocol_version"] == "3.7"
    assert "domain_contract_version" in template
    assert "last_protocol_reconciled_at" in template


def test_completed_cutover_files_are_not_active_root_authority():
    for name in (
        "MIGRATION_MANIFEST.json",
        "MIGRATION_STATUS.json",
        "MIGRATION_CHECKPOINT.md",
        "ENGINEERING_HOME_STATUS.json",
    ):
        assert not (ROOT / name).exists()
    assert (ROOT / "archive/migrations/2026-10-09-library-to-github.md").exists()


def test_system_blueprint_wires_lifecycle_and_progress_layers():
    text = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")
    assert "VERSION_LIFECYCLE_POLICY.json" in text
    assert "LIVE_CHAT_RECONCILIATION_POLICY.json" in text
    assert "PROGRESS_OBSERVABILITY_POLICY.json" in text
    assert "The user is not the migration operator" in text


def test_supported_old_protocols_have_additive_migration_edges():
    lifecycle = load("VERSION_LIFECYCLE_POLICY.json")
    edges = {(row["from"], row["to"]): row for row in lifecycle["supported_migration_edges"]}
    for old in ("3.3", "3.5", "3.6"):
        edge = edges[(old, "3.7")]
        assert edge["classification"] == "MIGRATABLE"
        assert edge["business_state_rewrite"] is False
        assert edge["lease_takeover_required"] is False
