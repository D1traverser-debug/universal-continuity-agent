from datetime import datetime, timezone
import json
from pathlib import Path

from runtime.universal_continuity import (
    CommitStatus,
    SCHEMA_VERSION,
    TaskMetadata,
    acquire_resume_lease,
    build_resume_progress_receipt,
    build_turn_commit_receipt,
    verify_resume_lease,
)

NOW = datetime(2026, 10, 10, 0, 0, tzinfo=timezone.utc)


def make_task(**overrides):
    raw = {
        "task_id": "continuity:test",
        "task_class": "USER",
        "domain": "TEST_DOMAIN",
        "title": "test task",
        "display_name_zh": "测试任务",
        "status": "ACTIVE",
        "resume_eligible": True,
        "resume_visibility": "DEFAULT",
        "recovery_owner": "GENERIC_HANDOFF",
        "updated_at": NOW.isoformat(),
        "current_stage": "STAGE_A",
        "next_action": "do B",
        "checkpoint_ref": "tasks/test/HANDOFF.md",
        "contract_version": "3.7",
        "manifest_ref": "tasks/test/TASK_MANIFEST.json",
        "manifest_version": 4,
        "resume_epoch": 2,
        "active_lease": None,
    }
    raw.update(overrides)
    return TaskMetadata.from_mapping(raw)


def test_runtime_schema_is_v37():
    assert SCHEMA_VERSION == "3.7"


def test_real_manifest_style_lease_can_inherit_top_level_epoch():
    task = make_task(
        resume_epoch=3,
        active_lease={
            "lease_id": "lease-3",
            "acquired_at": NOW.isoformat(),
            "supersedes_lease_id": "lease-2",
        },
    )
    assert task.active_lease is not None
    assert task.active_lease.resume_epoch == 3
    assert verify_resume_lease(task, "lease-3", resume_epoch=3)


def test_explicit_system_infra_can_take_over_but_stays_non_bare():
    task = make_task(
        task_class="SYSTEM_INFRA",
        resume_visibility="EXPLICIT_ONLY",
        task_id="continuity:maintenance",
        display_name_zh="跨对话继承系统建设与维护",
    )
    resumed = acquire_resume_lease(task, lease_id="infra-chat", now=NOW)
    assert resumed.resume_epoch == 3
    assert verify_resume_lease(resumed, "infra-chat", resume_epoch=3)


def test_resume_progress_receipt_captures_pre_takeover_state_and_waiting():
    task = make_task(status="WAITING", resume_epoch=7, manifest_version=11)
    checkpoint = {
        "updated_at": "2026-10-09T23:30:00Z",
        "status": "WAITING",
        "current_stage": "AWAITING_EXTERNAL_CONFIRMATION",
        "next_action": "continue after confirmation",
        "blockers": [],
        "waiting_on": [{"type": "USER_EXTERNAL_ACTION", "detail": "confirm publication"}],
    }
    receipt = build_resume_progress_receipt(task, checkpoint)
    assert receipt.resume_epoch_before_takeover == 7
    assert receipt.manifest_version == 11
    assert receipt.current_stage == "AWAITING_EXTERNAL_CONFIRMATION"
    assert receipt.next_action == "continue after confirmation"
    assert "confirm publication" in receipt.blockers_or_waiting_state


def test_turn_commit_receipt_requires_verified_write_for_committed():
    task = acquire_resume_lease(make_task(resume_epoch=0), lease_id="writer", now=NOW)
    failed = build_turn_commit_receipt(
        task,
        commit_required=True,
        write_succeeded=True,
        verified_after_write=False,
        lease_id="writer",
        resume_epoch=1,
    )
    assert failed.commit_status == CommitStatus.COMMIT_FAILED

    committed = build_turn_commit_receipt(
        task,
        commit_required=True,
        write_succeeded=True,
        verified_after_write=True,
        lease_id="writer",
        resume_epoch=1,
    )
    assert committed.commit_status == CommitStatus.COMMITTED
    assert committed.verified_after_write is True


def test_turn_commit_receipt_distinguishes_no_change_and_stale_writer():
    task = acquire_resume_lease(make_task(resume_epoch=0), lease_id="new", now=NOW)
    no_change = build_turn_commit_receipt(task, commit_required=False, lease_id="new", resume_epoch=1)
    assert no_change.commit_status == CommitStatus.NO_MATERIAL_CHANGE

    stale = build_turn_commit_receipt(
        task,
        commit_required=True,
        write_succeeded=True,
        verified_after_write=True,
        lease_id="old",
        resume_epoch=0,
    )
    assert stale.commit_status == CommitStatus.STALE_WRITER
    assert stale.verified_after_write is False


def test_progress_policy_requires_both_user_receipts():
    policy = json.loads((Path(__file__).resolve().parents[1] / "PROGRESS_OBSERVABILITY_POLICY.json").read_text(encoding="utf-8"))
    assert policy["continuity_contract"] == "3.7"
    assert policy["resume_progress_receipt"]["user_label_zh"] == "继承前进度"
    assert policy["turn_commit_receipt"]["user_label_zh"] == "进度提交"
    assert "COMMITTED" in policy["turn_commit_receipt"]["statuses"]
    assert "NO_MATERIAL_CHANGE" in policy["turn_commit_receipt"]["statuses"]
    assert policy["anti_false_positive"]["assistant_self_report_is_not_proof"] is True
