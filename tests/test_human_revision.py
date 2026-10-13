import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from runtime.human_revision import derive_human_revision, format_human_revision


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_universal_human_revision_is_calendar_plus_existing_manifest_sequence():
    manifest = {
        "updated_at": "2026-10-13T15:10:00+08:00",
        "manifest_version": 86,
    }
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


def test_progress_policy_makes_revision_display_derived_and_non_authoritative():
    policy = load("PROGRESS_OBSERVABILITY_POLICY.json")
    human = policy["human_revision_display"]
    assert human["model"] == "CALVER_PLUS_EXISTING_DURABLE_SEQUENCE"
    assert human["derived_not_stored_as_new_authority"] is True
    assert human["new_counter_forbidden"] is True
    assert human["daily_counter_reset"] is False
    assert human["git_history_scan_required"] is False
    assert human["git_tag_per_checkpoint"] is False
    assert human["universal_pilot"]["scope_code"] == "UC"
    assert human["universal_pilot"]["example"] == "UC-20261013-r86"


def test_version_lifecycle_keeps_git_protocol_and_human_revision_namespaces_separate():
    policy = load("VERSION_LIFECYCLE_POLICY.json")
    layers = policy["version_namespaces"]
    assert layers["git_commit"]["authority"] == "EXACT_IMMUTABLE_ENGINEERING_IDENTITY"
    assert layers["protocol"]["authority"] == "COMPATIBILITY_SEMANTICS"
    assert layers["durable_state_version"]["authority"] == "MONOTONIC_OWNER_OR_TASK_STATE_SEQUENCE"
    assert layers["human_revision"]["authority"] == "DERIVED_PRESENTATION_ONLY"
    assert layers["human_revision"]["global_cross_repo_counter"] is False
    assert layers["human_revision"]["tag_every_checkpoint"] is False
