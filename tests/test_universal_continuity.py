from datetime import datetime, timedelta, timezone

import pytest

from runtime.universal_continuity import (
    Compatibility,
    TaskMetadata,
    acquire_resume_lease,
    assign_display_name_zh,
    assert_checkpoint_writer,
    bare_inherit_eligible,
    candidate_display_name,
    classify_version_compatibility,
    needs_display_name_zh,
    registry_manifest_drift,
    resolve_candidates,
    should_autoresume,
    validate_checkpoint_quality,
    verify_resume_lease,
)

NOW = datetime(2026, 10, 9, 6, 0, tzinfo=timezone.utc)


def task(**overrides):
    raw = {
        "task_id": "t1",
        "domain": "WRITING",
        "title": "AI pharma article machine title",
        "display_name_zh": "AI制药文章",
        "recovery_owner": "FINANCIAL_WRITING_AGENT_RUNTIME",
        "status": "ACTIVE",
        "task_class": "USER",
        "resume_eligible": True,
        "resume_visibility": "DEFAULT",
        "updated_at": (NOW - timedelta(hours=2)).isoformat(),
        "current_stage": "EDITORIAL",
        "next_action": "compatibility check",
        "checkpoint_ref": "runtime://t1",
        "contract_version": "2.0",
        "keywords": ["AI制药", "文章", "写作"],
        "manifest_ref": "/tasks/t1/TASK_MANIFEST.json",
        "manifest_version": 1,
        "resume_epoch": 0,
        "active_lease": None,
    }
    raw.update(overrides)
    return TaskMetadata.from_mapping(raw)


def test_non_user_never_enters_bare_inherit():
    assert bare_inherit_eligible(task(task_class="SYSTEM_INFRA")) is False
    assert bare_inherit_eligible(task(task_class="FIXTURE")) is False
    assert bare_inherit_eligible(task(task_class="MIGRATION")) is False


def test_legacy_defaults_fail_closed():
    raw = {
        "task_id": "legacy",
        "domain": "WRITING",
        "title": "old",
        "recovery_owner": "OWNER",
        "status": "ACTIVE",
        "updated_at": NOW.isoformat(),
    }
    assert bare_inherit_eligible(TaskMetadata.from_mapping(raw)) is False


def test_unique_user_task_can_autoresume_on_bare_inherit():
    candidates = resolve_candidates([task()], now=NOW)
    assert len(candidates) == 1
    assert should_autoresume(candidates, hint_present=False) is True


def test_hint_prefers_matching_domain_and_keyword():
    a = task(task_id="a", display_name_zh="AI制药文章", keywords=["AI制药", "文章"])
    b = task(task_id="b", display_name_zh="A股盘前任务", title="market-day task", domain="A_SHARE", recovery_owner="A_SHARE_RECOMMENDATION", keywords=["荐股"])
    candidates = resolve_candidates([a, b], hint="继续荐股", now=NOW)
    assert candidates[0].task.task_id == "b"


def test_display_name_zh_is_used_for_semantic_routing_and_ui():
    a = task(task_id="a", title="opaque-task-a", display_name_zh="湿实验产业链文章", keywords=[])
    b = task(task_id="b", title="opaque-task-b", display_name_zh="视频增长系统", keywords=[])
    candidates = resolve_candidates([a, b], hint="继续湿实验产业链文章", now=NOW)
    assert candidates[0].task.task_id == "a"
    assert candidate_display_name(candidates[0].task) == "湿实验产业链文章"


def test_missing_display_name_zh_requires_one_time_naming():
    unnamed = task(display_name_zh=None)
    assert needs_display_name_zh(unnamed) is True
    raw = {
        "task_id": "x", "task_class": "USER", "domain": "X", "title": "x", "status": "ACTIVE",
        "resume_eligible": True, "resume_visibility": "DEFAULT", "recovery_owner": "GENERIC_HANDOFF",
        "updated_at": NOW.isoformat(), "current_stage": "WORK", "next_action": "continue", "checkpoint_ref": "x",
    }
    assert "user-task-missing-display-name-zh" in validate_checkpoint_quality(raw)


def test_assign_display_name_zh_preserves_machine_identity():
    original = task(display_name_zh=None)
    renamed = assign_display_name_zh(original, "  AI 制药 A股深度文章  ", now=NOW)
    assert renamed.task_id == original.task_id
    assert renamed.display_name_zh == "AI 制药 A股深度文章"
    assert renamed.manifest_version == original.manifest_version + 1
    assert needs_display_name_zh(renamed) is False


def test_assign_display_name_zh_rejects_blank_name():
    with pytest.raises(ValueError, match="must not be blank"):
        assign_display_name_zh(task(), "   ")


def test_multiple_bare_tasks_do_not_autoresume():
    a = task(task_id="a")
    b = task(task_id="b", title="another writing task", display_name_zh="另一个写作任务")
    candidates = resolve_candidates([a, b], now=NOW)
    assert len(candidates) == 2
    assert should_autoresume(candidates, hint_present=False) is False


def test_contract_compatibility_is_fail_closed():
    assert classify_version_compatibility(task(), current_contract_version="2.0").result == Compatibility.COMPATIBLE
    assert classify_version_compatibility(task(contract_version="1.0"), current_contract_version="2.0").result == Compatibility.INCOMPATIBLE
    assert classify_version_compatibility(task(contract_version="1.0"), current_contract_version="2.0", migration_supported_from={"1.0"}).result == Compatibility.MIGRATABLE


def test_checkpoint_quality_catches_false_resumability():
    raw = {
        "task_id": "x", "task_class": "USER", "domain": "X", "title": "x", "display_name_zh": "任务X", "status": "ACTIVE",
        "resume_eligible": True, "resume_visibility": "DEFAULT", "recovery_owner": "GENERIC_HANDOFF",
        "updated_at": NOW.isoformat(), "current_stage": "WORK", "next_action": "continue",
    }
    assert "resumable-user-without-checkpoint-ref" in validate_checkpoint_quality(raw)


def test_owner_registry_is_machine_readable_and_unique():
    import json
    from pathlib import Path
    data = json.loads((Path(__file__).resolve().parents[1] / "OWNER_REGISTRY.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "3.0"
    assert data["default_owner"] == "GENERIC_HANDOFF"
    names = [row["name"] for row in data["owners"]]
    assert len(names) == len(set(names))
    assert "FINANCIAL_WRITING_AGENT_RUNTIME" in names
    assert "A_SHARE_MARKET_AGENT" in names
    assert data["resolver"]["owner"] == "UNIVERSAL_CONTINUITY_HARNESS"


def test_system_registry_is_machine_readable_and_has_generic_bootstrap():
    import json
    from pathlib import Path
    data = json.loads((Path(__file__).resolve().parents[1] / "SYSTEM_REGISTRY.json").read_text(encoding="utf-8"))
    assert data["new_system_bootstrap"]["default_owner"] == "GENERIC_HANDOFF"
    assert data["new_system_bootstrap"]["continuity_stores_full_business_rules"] is False
    ids = [row["system_id"] for row in data["systems"]]
    assert len(ids) == len(set(ids))
    assert all(isinstance(x, str) and x for x in ids)


def test_new_chat_bootstrap_policy_requires_early_persistence_for_durable_work():
    import json
    from pathlib import Path
    policy = json.loads((Path(__file__).resolve().parents[1] / "NEW_CHAT_BOOTSTRAP.json").read_text(encoding="utf-8"))
    order = policy["write_order"]
    assert order.index("TASK_MANIFEST authority") < order.index("perform substantive work")
    assert order.index("display_name_zh; ask user once if missing") < order.index("TASK_MANIFEST authority")
    assert "event-driven checkpoint updates" in order
    assert policy["performance"]["bootstrap_scope"] == "FIRST_SUBSTANTIVE_MESSAGE_ONLY"


def test_display_name_bootstrap_is_one_time_then_resume():
    import json
    from pathlib import Path
    policy = json.loads((Path(__file__).resolve().parents[1] / "NEW_CHAT_BOOTSTRAP.json").read_text(encoding="utf-8"))
    naming = policy["display_name_zh"]
    assert naming["prompt_if_missing"] is True
    assert naming["prompt_frequency"] == "ONCE_PER_TASK_UNTIL_SET"
    assert naming["resume_original_work_after_answer"] is True
    assert naming["rename_keeps_task_id"] is True


def test_new_chat_resume_supersedes_old_writer_lease():
    original = task()
    old = acquire_resume_lease(original, lease_id="old-chat", now=NOW)
    assert verify_resume_lease(old, "old-chat", resume_epoch=1)
    new = acquire_resume_lease(old, lease_id="new-chat", now=NOW + timedelta(minutes=1))
    assert new.resume_epoch == 2
    assert new.active_lease.supersedes_lease_id == "old-chat"
    assert verify_resume_lease(new, "new-chat", resume_epoch=2)
    assert verify_resume_lease(new, "old-chat", resume_epoch=1) is False
    with pytest.raises(RuntimeError, match="STALE_WRITER_LEASE"):
        assert_checkpoint_writer(new, lease_id="old-chat", resume_epoch=1)


def test_registry_is_cache_and_manifest_is_authority():
    index = [{"task_id": "a", "display_name_zh": "旧名", "status": "ACTIVE", "current_stage": "OLD", "next_action": "old", "recovery_owner": "X", "checkpoint_ref": "x"}]
    manifests = [
        {"task_id": "a", "display_name_zh": "新名", "status": "ACTIVE", "current_stage": "NEW", "next_action": "new", "recovery_owner": "X", "checkpoint_ref": "x"},
        {"task_id": "b", "display_name_zh": "任务B", "status": "ACTIVE", "current_stage": "WORK", "next_action": "go", "recovery_owner": "Y", "checkpoint_ref": "y"},
    ]
    drift = registry_manifest_drift(index, manifests)
    assert "registry-stale:a:display_name_zh" in drift
    assert "registry-stale:a:current_stage" in drift
    assert "registry-missing:b" in drift


def test_registries_are_declared_rebuildable_caches_not_authority():
    import json
    from pathlib import Path
    task_registry = json.loads((Path(__file__).resolve().parents[1] / "GENERIC_TASK_REGISTRY.json").read_text(encoding="utf-8"))
    system_registry = json.loads((Path(__file__).resolve().parents[1] / "SYSTEM_REGISTRY.json").read_text(encoding="utf-8"))
    assert task_registry["role"] == "REBUILDABLE_CACHE_NOT_AUTHORITY"
    assert system_registry["role"] == "REBUILDABLE_CACHE_NOT_AUTHORITY"
    assert "TASK_MANIFEST" in task_registry["authority"]
    assert "SYSTEM_MANIFEST" in system_registry["authority"]


def test_degraded_mode_prevents_continuity_from_blocking_normal_work():
    import json
    from pathlib import Path
    policy = json.loads((Path(__file__).resolve().parents[1] / "NEW_CHAT_BOOTSTRAP.json").read_text(encoding="utf-8"))
    degraded = policy["degraded_mode"]
    assert degraded["simple_one_shot"].startswith("Proceed normally")
    assert "domain owner directly" in degraded["explicit_known_domain_task"]
    assert degraded["resume_unknown_state"].startswith("FAIL_CLOSED")
    assert policy["performance"]["bootstrap_scope"] == "FIRST_SUBSTANTIVE_MESSAGE_ONLY"


def test_single_writer_policy_matches_new_chat_takeover_workflow():
    import json
    from pathlib import Path
    policy = json.loads((Path(__file__).resolve().parents[1] / "NEW_CHAT_BOOTSTRAP.json").read_text(encoding="utf-8"))
    sw = policy["single_writer"]
    assert sw["model"] == "NEW_CHAT_TAKEOVER_SUPERSEDES_OLD_CHAT"
    assert sw["resume_epoch_required"] is True
    assert sw["lease_required"] is True
    assert any("verify own lease" in step for step in sw["acquire_flow"])
