from datetime import datetime, timezone
import pytest

from runtime.protocol_reconciliation import apply_protocol_patch, classify_protocol_compatibility, plan_in_place_protocol_reconciliation
from runtime.universal_continuity import Compatibility


def manifest(protocol: str = "CONTINUITY_V3_3") -> dict:
    return {
        "task_id":"demo:task","task_class":"USER","domain":"DEMO","title":"Demo task","display_name_zh":"演示任务",
        "status":"ACTIVE","resume_eligible":True,"resume_visibility":"DEFAULT","recovery_owner":"GENERIC_HANDOFF",
        "updated_at":"2026-10-10T00:00:00Z","current_stage":"WORKING","next_action":"continue exact work",
        "checkpoint_ref":"tasks/demo/HANDOFF.md","contract_version":protocol,"manifest_ref":"tasks/demo/TASK_MANIFEST.json",
        "manifest_version":4,"resume_epoch":7,
        "active_lease":{"lease_id":"lease-current","acquired_at":"2026-10-10T00:00:00Z","supersedes_lease_id":"lease-old"},
        "artifact_refs":["artifact-a"],
    }


def plan(raw):
    return plan_in_place_protocol_reconciliation(raw, current_protocol_version="3.7", migration_supported_from={"3.3","3.5","3.6"}, lease_id="lease-current", resume_epoch=7, applied_by="test-writer", now=datetime(2026,10,10,1,0,tzinfo=timezone.utc))


def test_supported_same_chat_migration_preserves_business_state_and_lease():
    raw=manifest(); p=plan(raw)
    assert p.decision.result == Compatibility.MIGRATABLE and p.changed
    updated=apply_protocol_patch(raw,p)
    assert updated["continuity_protocol_version"] == "3.7"
    assert updated["resume_epoch"] == raw["resume_epoch"]
    assert updated["active_lease"] == raw["active_lease"]
    assert updated["current_stage"] == raw["current_stage"]
    assert updated["next_action"] == raw["next_action"]
    assert updated["artifact_refs"] == raw["artifact_refs"]


def test_stale_writer_cannot_apply_migratable_protocol_patch():
    with pytest.raises(RuntimeError, match="STALE_WRITER_LEASE"):
        plan_in_place_protocol_reconciliation(manifest(), current_protocol_version="3.7", migration_supported_from={"3.3"}, lease_id="lease-stale", resume_epoch=7, applied_by="stale")


def test_already_canonical_current_protocol_is_noop():
    raw=manifest("CONTINUITY_V3_7"); raw["continuity_protocol_version"]="3.7"
    p=plan(raw); assert p.decision.result == Compatibility.COMPATIBLE and not p.changed


def test_legacy_current_marker_gets_canonical_stamp_without_takeover():
    raw=manifest("CONTINUITY_V3_7"); p=plan(raw); updated=apply_protocol_patch(raw,p)
    assert p.decision.result == Compatibility.COMPATIBLE and p.changed
    assert updated["resume_epoch"] == 7 and updated["active_lease"]["lease_id"] == "lease-current"


def test_unsupported_continuity_protocol_fails_closed_without_mutation():
    raw=manifest("CONTINUITY_V2_0"); p=plan(raw)
    assert p.decision.result == Compatibility.INCOMPATIBLE and not p.changed and apply_protocol_patch(raw,p)==raw


def test_domain_contract_version_is_not_misclassified_as_legacy_continuity_protocol():
    raw=manifest("2.1-github")
    decision=classify_protocol_compatibility(raw,current_protocol_version="3.7",migration_supported_from={"3.3","3.5","3.6"})
    assert decision.result == Compatibility.UNKNOWN


def test_plain_numeric_legacy_protocol_marker_remains_supported():
    raw=manifest("3.5")
    assert classify_protocol_compatibility(raw,current_protocol_version="3.7",migration_supported_from={"3.5"}).result == Compatibility.MIGRATABLE
