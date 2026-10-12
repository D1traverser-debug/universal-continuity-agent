import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_system_maintenance_current_stage_is_stable_lifecycle_not_changelog():
    manifest = json.loads(
        (ROOT / "tasks/universal-continuity-maintenance/TASK_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert manifest["current_stage_semantics"] == "STABLE_LIFECYCLE_STAGE_NOT_CUMULATIVE_CHANGELOG"
    assert manifest["current_stage"] == "SYSTEM_MAINTENANCE_ACTIVE"
    assert len(manifest["current_stage"].encode("utf-8")) <= 128


def test_system_maintenance_discovery_cache_uses_same_stable_stage_but_delegates_detail_to_manifest():
    manifest = json.loads(
        (ROOT / "tasks/universal-continuity-maintenance/TASK_MANIFEST.json").read_text(encoding="utf-8")
    )
    registry = json.loads((ROOT / "GENERIC_TASK_REGISTRY.json").read_text(encoding="utf-8"))
    row = next(item for item in registry["tasks"] if item["task_id"] == manifest["task_id"])
    assert row["current_stage"] == manifest["current_stage"]
    assert row["manifest_ref"] == "tasks/universal-continuity-maintenance/TASK_MANIFEST.json"
    assert "authoritative maintenance TASK_MANIFEST/HANDOFF" in row["next_action"]
