import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from runtime.human_revision import derive_human_revision, format_human_revision


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_universal_human_revision_is_calendar_plus_existing_manifest_sequence():
    manifest = {"updated_at": "2026-10-13T15:10:00+08:00", "manifest_version": 86}
    assert derive_human_revision(manifest, scope_code="UC") == "UC-20261013-r86"


def test_label_uses_authoritative_timestamp_calendar_date_without_timezone_conversion():
    persisted = datetime(2026, 10, 14, 0, 15, tzinfo=timezone(timedelta(hours=9)))
    assert format_human_revision(scope_code="UC", persisted_at=persisted, durable_version=87) == "UC-20261014-r87"


def test_same_day_multiple_checkpoints_need_no_new_daily_counter():
    first = format_human_revision(scope_code="UC", persisted_at="2026-10-13T10:00:00+08:00", durable_version=86)
    second = format_human_revision(scope_code="UC", persisted_at="2026-10-13T10:01:00+08:00", durable_version=87)
    assert first == "UC-20261013-r86"
    assert second == "UC-20261013-r87"
    assert first != second


def test_revision_sequence_does_not_reset_when_date_changes():
    assert format_human_revision(scope_code="UC", persisted_at="2026-10-13T23:59:00+08:00", durable_version=87) == "UC-20261013-r87"
    assert format_human_revision(scope_code="UC", persisted_at="2026-10-14T00:01:00+08:00", durable_version=88) == "UC-20261014-r88"


def test_invalid_scope_or_nonpositive_version_fails_closed():
    with pytest.raises(ValueError):
        format_human_revision(scope_code="u", persisted_at="2026-10-13T00:00:00Z", durable_version=1)
    with pytest.raises(ValueError):
        format_human_revision(scope_code="UC", persisted_at="2026-10-13T00:00:00Z", durable_version=0)


def test_current_universal_manifest_derives_revision_without_storing_duplicate_label():
    manifest = load("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    label = derive_human_revision(manifest, scope_code="UC")
    assert label.startswith("UC-")
    assert label.endswith(f"-r{manifest['manifest_version']}")
    assert "human_revision" not in manifest
    assert "human_revision_latest_expected" not in manifest


def test_progress_policy_makes_revision_display_derived_scope_local_and_non_authoritative():
    policy = load("PROGRESS_OBSERVABILITY_POLICY.json")
    human = policy["human_revision_display"]
    assert human["model"] == "CALVER_PLUS_EXISTING_DURABLE_SEQUENCE"
    assert human["derived_not_stored_as_new_authority"] is True
    assert human["do_not_store_derived_label_in_task_manifest"] is True
    assert human["new_counter_forbidden"] is True
    assert human["daily_counter_reset"] is False
    assert human["git_history_scan_required"] is False
    assert human["git_tag_per_checkpoint"] is False
    assert human["scope_local_not_global_unique"] is True
    assert human["gaps_allowed"] is True
    assert human["core_task_state_schema_expansion_required"] is False
    assert human["adoption_gate"]["existing_monotonic_durable_version_required"] is True
    assert human["adoption_gate"]["cross_scope_numeric_comparison_allowed"] is False
    assert human["universal_pilot"]["scope_code"] == "UC"
    assert human["universal_pilot"]["example"] == "UC-20261013-r86"


def test_version_lifecycle_keeps_git_protocol_state_controller_and_human_namespaces_separate():
    policy = load("VERSION_LIFECYCLE_POLICY.json")
    layers = policy["version_namespaces"]
    assert layers["git_commit"]["authority"] == "EXACT_IMMUTABLE_ENGINEERING_IDENTITY"
    assert layers["protocol"]["authority"] == "COMPATIBILITY_SEMANTICS"
    assert layers["durable_state_version"]["authority"] == "MONOTONIC_OWNER_OR_TASK_STATE_SEQUENCE"
    assert layers["controller_revision"]["authority"] == "RUN_LOCAL_MAINTENANCE_TRACE"
    assert layers["human_revision"]["authority"] == "DERIVED_PRESENTATION_ONLY"
    assert layers["human_revision"]["global_cross_repo_counter"] is False
    assert layers["human_revision"]["tag_every_checkpoint"] is False
    assert layers["human_revision"]["stored_duplicate_label_forbidden"] is True
    assert policy["metadata"]["human_revision_storage_field_allowed"] is False


def test_human_revision_is_not_a_global_release_or_cross_owner_ordering_key():
    policy = load("PROGRESS_OBSERVABILITY_POLICY.json")["human_revision_display"]
    assert policy["ordering_rule"].startswith("Within one revision scope")
    assert "not globally comparable" in load("VERSION_LIFECYCLE_POLICY.json")["version_namespaces"]["human_revision"]["cross_owner_rule"]
    assert policy["adoption_gate"]["if_owner_has_no_suitable_monotonic_version"].startswith("OMIT_HUMAN_REVISION")


def test_human_revision_rendering_adds_no_hot_path_remote_or_history_work():
    performance = load("PROGRESS_OBSERVABILITY_POLICY.json")["performance"]
    assert performance["human_revision_requires_no_history_scan_or_new_remote_read"] is True
    assert load("PROGRESS_OBSERVABILITY_POLICY.json")["human_revision_display"]["performance_rule"].startswith("Derivation is O(1)")
