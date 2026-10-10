from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

import pytest

from runtime.owner_topology import business_owner_names, validate_owner_registry
from runtime.universal_continuity import (
    Compatibility, TaskMetadata, acquire_resume_lease, assign_display_name_zh,
    assert_checkpoint_writer, bare_inherit_eligible, build_resume_progress_receipt,
    candidate_display_name, classify_version_compatibility, merge_owner_discovery_payloads,
    needs_display_name_zh, registry_manifest_drift, resolve_candidates, should_autoresume,
    validate_checkpoint_quality, verify_resume_lease,
)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 9, 6, 0, tzinfo=timezone.utc)


def raw_task(**overrides):
    raw = {
        "task_id":"t1","domain":"WRITING","title":"AI pharma article machine title","display_name_zh":"AI制药文章",
        "recovery_owner":"FINANCIAL_WRITING_AGENT_RUNTIME","status":"ACTIVE","task_class":"USER",
        "resume_eligible":True,"resume_visibility":"DEFAULT","updated_at":(NOW-timedelta(hours=2)).isoformat(),
        "current_stage":"EDITORIAL","next_action":"compatibility check","checkpoint_ref":"runtime://t1",
        "contract_version":"2.0","keywords":["AI制药","文章","写作"],"manifest_ref":"/tasks/t1/TASK_MANIFEST.json",
        "manifest_version":1,"resume_epoch":0,"active_lease":None,
    }
    raw.update(overrides)
    return raw


def task(**overrides): return TaskMetadata.from_mapping(raw_task(**overrides))


def test_non_user_and_legacy_never_enter_bare_inherit():
    assert not bare_inherit_eligible(task(task_class="SYSTEM_INFRA"))
    assert not bare_inherit_eligible(task(task_class="FIXTURE"))
    legacy = {"task_id":"legacy","domain":"WRITING","title":"old","recovery_owner":"OWNER","status":"ACTIVE","updated_at":NOW.isoformat()}
    assert not bare_inherit_eligible(TaskMetadata.from_mapping(legacy))


def test_resume_eligible_is_strict_boolean_not_truthy_string():
    with pytest.raises(ValueError, match="resume_eligible must be boolean"):
        task(resume_eligible="false")
    raw = raw_task(resume_eligible="false")
    assert "resume_eligible-not-boolean" in validate_checkpoint_quality(raw)


def test_bare_discovery_does_not_silently_truncate_and_partial_set_never_autoresumes():
    tasks = [task(task_id=f"t{i}", display_name_zh=f"任务{i}") for i in range(8)]
    full = resolve_candidates(tasks, now=NOW)
    assert len(full) == 8
    assert should_autoresume(full, hint_present=False, discovery_complete=True) is False

    truncated = resolve_candidates(tasks, now=NOW, max_results=1)
    assert len(truncated) == 1
    assert should_autoresume(truncated, hint_present=False, discovery_complete=False) is False


def test_unique_complete_user_task_can_autoresume():
    candidates = resolve_candidates([task()], now=NOW)
    assert should_autoresume(candidates, hint_present=False, discovery_complete=True) is True


def test_hint_prefers_matching_domain_and_keyword():
    a = task(task_id="a", display_name_zh="AI制药文章", keywords=["AI制药", "文章"])
    b = task(task_id="b", display_name_zh="A股盘前任务", title="market-day task", domain="A_SHARE", recovery_owner="A_SHARE_RECOMMENDATION", keywords=["荐股"])
    assert resolve_candidates([a,b], hint="继续荐股", now=NOW)[0].task.task_id == "b"


def test_display_name_assignment_preserves_machine_identity():
    original = task(display_name_zh=None)
    assert needs_display_name_zh(original)
    renamed = assign_display_name_zh(original, "  AI 制药 A股深度文章  ", now=NOW)
    assert renamed.task_id == original.task_id
    assert renamed.display_name_zh == "AI 制药 A股深度文章"
    assert candidate_display_name(renamed) == "AI 制药 A股深度文章"
    with pytest.raises(ValueError): assign_display_name_zh(original, "   ")


def test_terminal_or_paused_task_cannot_acquire_writer_lease_without_reactivation():
    for status in ("PAUSED", "COMPLETE", "ARCHIVED", "ABANDONED"):
        with pytest.raises(ValueError, match="not directly resumable"):
            acquire_resume_lease(task(status=status), lease_id="x", now=NOW)


def test_explicit_system_infra_active_task_can_take_lease_but_terminal_cannot():
    active = task(task_id="infra", task_class="SYSTEM_INFRA", resume_visibility="EXPLICIT_ONLY", status="ACTIVE")
    resumed = acquire_resume_lease(active, lease_id="infra-chat", now=NOW)
    assert resumed.resume_epoch == 1
    terminal = task(task_id="infra", task_class="SYSTEM_INFRA", resume_visibility="EXPLICIT_ONLY", status="COMPLETE")
    with pytest.raises(ValueError, match="not directly resumable"):
        acquire_resume_lease(terminal, lease_id="infra-chat", now=NOW)


def test_new_chat_resume_supersedes_old_writer_lease():
    old = acquire_resume_lease(task(), lease_id="old-chat", now=NOW)
    new = acquire_resume_lease(old, lease_id="new-chat", now=NOW+timedelta(minutes=1))
    assert new.resume_epoch == 2
    assert new.active_lease.supersedes_lease_id == "old-chat"
    assert verify_resume_lease(new, "new-chat", resume_epoch=2)
    with pytest.raises(RuntimeError, match="STALE_WRITER_LEASE"):
        assert_checkpoint_writer(new, lease_id="old-chat", resume_epoch=1)


def test_resume_progress_checkpoint_must_bind_same_task_identity():
    t = task()
    good = {"task_id":"t1","status":"ACTIVE","current_stage":"DRAFT","next_action":"finish","updated_at":NOW.isoformat()}
    receipt = build_resume_progress_receipt(t, good)
    assert receipt.current_stage == "DRAFT"
    with pytest.raises(ValueError, match="checkpoint_missing_task_id"):
        build_resume_progress_receipt(t, {"status":"ACTIVE"})
    with pytest.raises(ValueError, match="checkpoint_task_id_mismatch"):
        build_resume_progress_receipt(t, {"task_id":"other","status":"ACTIVE"})


def test_cross_owner_task_id_collision_fails_closed():
    a = [raw_task(task_id="same", recovery_owner="OWNER_A")]
    b = [raw_task(task_id="same", recovery_owner="OWNER_B")]
    with pytest.raises(ValueError, match="cross_owner_task_id_collision"):
        merge_owner_discovery_payloads({"OWNER_A":a, "OWNER_B":b})


def test_contract_compatibility_is_fail_closed():
    assert classify_version_compatibility(task(), current_contract_version="2.0").result == Compatibility.COMPATIBLE
    assert classify_version_compatibility(task(contract_version="1.0"), current_contract_version="2.0").result == Compatibility.INCOMPATIBLE
    assert classify_version_compatibility(task(contract_version="1.0"), current_contract_version="2.0", migration_supported_from={"1.0"}).result == Compatibility.MIGRATABLE


def test_registry_manifest_drift_detects_stale_cache():
    index=[{"task_id":"a","display_name_zh":"旧名","status":"ACTIVE","current_stage":"OLD","next_action":"old","recovery_owner":"X","checkpoint_ref":"x"}]
    manifests=[{"task_id":"a","display_name_zh":"新名","status":"ACTIVE","current_stage":"NEW","next_action":"new","recovery_owner":"X","checkpoint_ref":"x"},{"task_id":"b","display_name_zh":"任务B","status":"ACTIVE","current_stage":"WORK","next_action":"go","recovery_owner":"Y","checkpoint_ref":"y"}]
    drift=registry_manifest_drift(index,manifests)
    assert "registry-stale:a:display_name_zh" in drift
    assert "registry-missing:b" in drift


def test_owner_registry_is_machine_readable_unique_and_topology_authoritative():
    data=json.loads((ROOT/"OWNER_REGISTRY.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "3.1"
    assert data["default_owner"] == "GENERIC_HANDOFF"
    assert data["membership_authority"]["role"] == "SOLE_CONTROL_PLANE_OWNER_MEMBERSHIP_AUTHORITY"
    assert validate_owner_registry(data) == ()
    assert business_owner_names(data)


def test_system_and_task_registries_are_rebuildable_not_authority():
    task_registry=json.loads((ROOT/"GENERIC_TASK_REGISTRY.json").read_text(encoding="utf-8"))
    system_registry=json.loads((ROOT/"SYSTEM_REGISTRY.json").read_text(encoding="utf-8"))
    assert task_registry["role"] == "REBUILDABLE_CACHE_NOT_AUTHORITY"
    assert system_registry["role"] == "REBUILDABLE_CACHE_NOT_AUTHORITY"


def test_new_chat_bootstrap_persists_before_substantive_work_and_has_degraded_mode():
    policy=json.loads((ROOT/"NEW_CHAT_BOOTSTRAP.json").read_text(encoding="utf-8"))
    order=policy["write_order"]
    assert order.index("TASK_MANIFEST authority") < order.index("perform substantive work")
    assert order.index("display_name_zh; ask user once if missing") < order.index("TASK_MANIFEST authority")
    assert policy["degraded_mode"]["simple_one_shot"].startswith("Proceed normally")
    assert policy["single_writer"]["model"] == "NEW_CHAT_TAKEOVER_SUPERSEDES_OLD_CHAT"
