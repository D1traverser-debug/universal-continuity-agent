from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_account_hook_covers_existing_durable_chats_and_progress_receipts():
    text = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")
    assert "包括升级前已经打开/继承的旧对话" in text
    assert "每次最终答复末尾必须报告“进度提交”" in text
    assert "不要求我手动迁移旧对话" in text
    assert "只有真正的新聊天 takeover" in text


def test_live_chat_policy_preserves_lease_for_protocol_only_upgrade():
    policy = json.loads((ROOT / "LIVE_CHAT_RECONCILIATION_POLICY.json").read_text(encoding="utf-8"))
    assert policy["user_responsibility"]["manual_version_selection"] is False
    assert policy["user_responsibility"]["manual_checkpoint_rewrite"] is False
    assert policy["lease_rules"]["same_chat_protocol_upgrade_increments_resume_epoch"] is False
    assert policy["lease_rules"]["same_chat_protocol_upgrade_replaces_active_lease"] is False
    assert policy["progress_receipt_in_existing_chats"]["turn_commit_receipt_required"] is True
