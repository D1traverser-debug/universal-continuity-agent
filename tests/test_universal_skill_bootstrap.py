from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_universal_skill_delegates_to_two_file_bootstrap_and_event_driven_authority():
    text = (ROOT / "skills/universal-continuity/SKILL.md").read_text(encoding="utf-8")
    assert "ENTRYPOINT.md" in text
    assert "CURRENT_PROTOCOL.json" in text
    assert "event-driven" in text.lower()

    authority_section = text.split("## Authority bootstrap", 1)[1].split("## Core execution", 1)[0]
    assert "CONTINUITY_CONTRACT.json" not in authority_section
    assert "PROGRESS_OBSERVABILITY_POLICY.json" not in authority_section
    assert "OWNER_REGISTRY.json" not in authority_section
    assert "Do **not** maintain or preload a second fixed list" in authority_section
