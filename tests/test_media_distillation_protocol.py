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


def test_reference_case_does_not_overclaim_visual_review():
    text = (ROOT / "MEDIA_DISTILLATION_PROTOCOL.md").read_text(encoding="utf-8")

    assert "full YouTube transcript obtained for the complete 20:14 timeline" in text
    assert "same-author companion article fully read" in text
    assert "full visual stream review not yet claimed" in text
