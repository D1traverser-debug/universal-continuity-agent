import json
from pathlib import Path

from runtime.universal_continuity import (
    Compatibility,
    TaskMetadata,
    bare_inherit_eligible,
    classify_version_compatibility,
    validate_checkpoint_quality,
    verify_resume_lease,
)


MANIFEST_PATH = Path(__file__).parents[1] / "tasks" / "FQ001_MINGRI_ORDER" / "TASK_MANIFEST.json"


def _load():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_novel_task_manifest_is_v37_and_resumable_after_github_cutover():
    raw = _load()
    assert raw["schema_version"] == "3.7"
    assert raw["continuity_protocol_version"] == "3.7"
    assert raw["task_id"] == "FQ001_MINGRI_ORDER"
    assert raw["display_name_zh"] == "《凌晨零点，我接到明天的订单》"
    assert raw["recovery_owner"] == "NOVEL_WRITING_AGENT"
    assert raw["checkpoint_ref"].endswith("projects/FQ001_MINGRI_ORDER/checkpoints/CURRENT_CHECKPOINT.json")
    assert validate_checkpoint_quality(raw) == []

    task = TaskMetadata.from_mapping(raw)
    assert bare_inherit_eligible(task)


def test_novel_task_manifest_contract_is_compatible_with_current_protocol():
    task = TaskMetadata.from_mapping(_load())
    decision = classify_version_compatibility(task, current_contract_version="3.7")
    assert decision.result is Compatibility.COMPATIBLE


def test_novel_current_writer_lease_is_self_consistent():
    raw = _load()
    task = TaskMetadata.from_mapping(raw)
    lease = raw["active_lease"]
    assert verify_resume_lease(task, lease["lease_id"], resume_epoch=lease["resume_epoch"])


def test_novel_manifest_does_not_duplicate_business_payload():
    raw = _load()
    forbidden = {"canon", "chapter_text", "timeline_entries", "character_state", "publication_log"}
    assert forbidden.isdisjoint(raw)
    assert raw["business_state_authority"] == "D1traverser-debug/novel-writing-agent@main"
    assert raw["lease_authority"] == "THIS_GITHUB_MANIFEST"
    assert raw["compatibility"]["post_migration"] == "COMPATIBLE"
