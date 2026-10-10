from datetime import datetime, timezone

import pytest

from runtime.protocol_reconciliation import (
    apply_protocol_patch,
    plan_in_place_protocol_reconciliation,
)
from runtime.universal_continuity import Compatibility


def manifest(protocol: str = "CONTINUITY_V3_3") -> dict:
    return {
        "task_id": "demo:task",
        "task_class": "USER",
        "domain": "DEMO",
        "title": "Demo task",
        "display_name_zh": "演示任务",
        "status": "ACTIVE",
        "resume_eligible": True,
        "resume_visibility": "DEFAULT",
        "recovery_owner": "GENERIC_HANDOFF",
        "updated_at": "2026-10-10T00:00:00Z",
        "current_stage": "WORKING",
        "next_action": "continue exact work",
        "checkpoint_ref": "tasks/demo/HANDOFF.md",
        "contract_version": protocol,
        "manifest_ref": "tasks/demo/TASK_MANIFEST.json",
        "manifest_version": 4,
        "resume_epoch": 7,
        "active_lease": {
            "lease_id": "lease-current",
            "acquired_at": "2026-10-10T00:00:00Z",
            "supersedes_lease_id": "lease-old",
        },
        "artifact_refs": ["artifact-a"],
    }


def test_supported_same_chat_migration_preserves_business_state_and_lease():
    raw = manifest()
    plan = plan_in_place_protocol_reconciliation(
        raw,
        current_protocol_version="3.7",
        migration_supported_from={"3.3", "3.5", "3.6"},
        lease_id="lease-current",
        resume_epoch=7,
        applied_by="test-writer",
        now=datetime(2026, 10, 10, 1, 0, tzinfo=timezone.utc),
    )
    assert plan.decision.result == Compatibility.MIGRATABLE
    assert plan.changed is True
    assert plan.adaptation_record["lease_changed"] is False
    assert plan.adaptation_record["business_state_rewritten"] is False

    updated = apply_protocol_patch(raw, plan)
    assert updated["continuity_protocol_version"] == "3.7"
    assert updated["resume_epoch"] == raw["resume_epoch"]
    assert updated["active_lease"] == raw["active_lease"]
    assert updated["current_stage"] == raw["current_stage"]
    assert updated["next_action"] == raw["next_action"]
    assert updated["artifact_refs"] == raw["artifact_refs"]
    assert updated["manifest_version"] == raw["manifest_version"] + 1


def test_stale_writer_cannot_apply_migratable_protocol_patch():
    raw = manifest()
    with pytest.raises(RuntimeError, match="STALE_WRITER_LEASE"):
        plan_in_place_protocol_reconciliation(
            raw,
            current_protocol_version="3.7",
            migration_supported_from={"3.3"},
            lease_id="lease-stale",
            resume_epoch=7,
            applied_by="stale-writer",
        )


def test_already_canonical_current_protocol_is_noop():
    raw = manifest("CONTINUITY_V3_7")
    raw["continuity_protocol_version"] = "3.7"
    plan = plan_in_place_protocol_reconciliation(
        raw,
        current_protocol_version="3.7",
        migration_supported_from={"3.3", "3.5", "3.6"},
        lease_id="lease-current",
        resume_epoch=7,
        applied_by="test-writer",
    )
    assert plan.decision.result == Compatibility.COMPATIBLE
    assert plan.changed is False
    assert apply_protocol_patch(raw, plan) == raw


def test_legacy_current_marker_gets_canonical_stamp_without_takeover():
    raw = manifest("CONTINUITY_V3_7")
    plan = plan_in_place_protocol_reconciliation(
        raw,
        current_protocol_version="3.7",
        migration_supported_from={"3.3", "3.5", "3.6"},
        lease_id="lease-current",
        resume_epoch=7,
        applied_by="test-writer",
    )
    assert plan.decision.result == Compatibility.COMPATIBLE
    assert plan.changed is True
    updated = apply_protocol_patch(raw, plan)
    assert updated["continuity_protocol_version"] == "3.7"
    assert updated["resume_epoch"] == 7
    assert updated["active_lease"]["lease_id"] == "lease-current"


def test_unsupported_protocol_fails_closed_without_mutation():
    raw = manifest("CONTINUITY_V2_0")
    plan = plan_in_place_protocol_reconciliation(
        raw,
        current_protocol_version="3.7",
        migration_supported_from={"3.3", "3.5", "3.6"},
        lease_id="lease-current",
        resume_epoch=7,
        applied_by="test-writer",
    )
    assert plan.decision.result == Compatibility.INCOMPATIBLE
    assert plan.changed is False
    assert plan.patch == {}
    assert apply_protocol_patch(raw, plan) == raw
