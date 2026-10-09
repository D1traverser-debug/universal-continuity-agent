from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_media_protocol_separates_audio_and_visual_completion_claims():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    assert "AUDIO_TRANSCRIPT_FULL" in text
    assert "VISUAL_FULL_STREAM_REVIEW" in text
    assert "A complete transcript is sufficient to claim the spoken/audio content was fully reviewed" in text
    assert "It is NOT sufficient to claim every visual element" in text


def test_media_protocol_preserves_source_levels_and_same_media_identity_checks():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    for level in ["L1", "L2", "L3", "L4"]:
        assert level in text
    assert "Same-media identity check" in text
    assert "matching duration" in text
    assert "matching chapter sequence/timestamps" in text


def test_media_protocol_requires_distillation_not_copying_external_advice():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    assert "取其精华，去其糟粕" in text
    assert "Verify important OpenAI/product claims against current first-party documentation" in text
    assert "Check scope fit" in text
    assert "Reject brittle numeric heuristics as hard policy" in text


def test_wechat_media_is_no_login_first_and_has_a_dedicated_playbook():
    protocol = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")
    playbook = (ROOT / "WECHAT_MEDIA_EXTRACTION_PLAYBOOK.md").read_text(encoding="utf-8")

    assert "WECHAT_MEDIA_EXTRACTION_PLAYBOOK.md" in protocol
    assert "Do NOT require YouTube, Bilibili, user login or a manual upload by default" in protocol
    assert "must not ask the user to log in simply because login would be easier" in protocol

    assert "Default ladder" in playbook
    assert "public page -> embedded state -> direct media request" in playbook
    assert "authenticated playback -> user file upload" in playbook
    assert "do not ask for WeChat login or file upload first" in playbook
    assert "blob:" in playbook
    assert "direct MP4" in playbook
    assert "HLS" in playbook
    assert "LOGIN_REQUIRED" in playbook


def test_wechat_playbook_keeps_access_control_boundary():
    playbook = (ROOT / "WECHAT_MEDIA_EXTRACTION_PLAYBOOK.md").read_text(encoding="utf-8")

    assert "Do not bypass paywalls" in playbook
    assert "Do not use this as a way to bypass DRM" in playbook
    assert "public/authorized playback" in playbook


def test_reference_case_records_full_audio_and_visual_review_without_collapsing_evidence_types():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    assert "full YouTube transcript obtained for the complete 20:14 timeline" in text
    assert "same-author companion article fully read" in text
    assert "full-duration visual scene analysis completed from 00:00 through 20:14" in text
    assert "AUDIO_TRANSCRIPT_FULL = true" in text
    assert "VISUAL_FULL_STREAM_REVIEW = true" in text
    assert "EVIDENCE_LEVELS_KEPT_DISTINCT = true" in text


def test_reference_case_explicitly_rejects_brittle_or_out_of_scope_advice():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    assert "fixed “smart-zone” token threshold such as 150K" in text
    assert "fixed long-context pricing threshold" in text
    assert "hard-coded Astra/Sol/Luna model-selection ladder" in text
    assert "anecdotal account-ban claims as system policy" in text
    assert "experimental Codex feature availability as a durable dependency" in text
