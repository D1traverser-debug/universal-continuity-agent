import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "research" / "skill-library" / "2026-global-ai-skills-top10"


def load_index():
    return json.loads((LIB / "INDEX.json").read_text(encoding="utf-8"))


def test_top10_library_is_complete_before_final_selection():
    index = load_index()

    assert index["status"] == "COMPLETE_10_OF_10__PHASE_B_SELECTION_COMPLETE"
    assert index["selection_was_frozen_until_complete"] is True
    assert index["production_promotion_is_separate_engineering_change"] is True

    entries = index["entries"]
    assert len(entries) == 10
    assert {item["rank"] for item in entries} == set(range(1, 11))
    assert len({item["name"] for item in entries}) == 10

    for item in entries:
        assert item["status"] == "COMPLETE_SOURCE_NORMALIZATION"
        assert item["selection_status"] != "PENDING_PHASE_B"
        assert (ROOT / item["entry_ref"]).is_file()
        assert item["evidence"]


def test_top10_library_has_pinned_sources_schema_matrix_and_selection():
    index = load_index()

    assert set(index["source_heads"]) == {
        "vercel-labs/skills",
        "mattpocock/skills",
        "vercel-labs/agent-browser",
        "anthropics/skills",
    }
    assert all(len(sha) == 40 for sha in index["source_heads"].values())

    for ref_key in ("common_schema_ref", "cross_skill_matrix_ref", "selection_ref"):
        assert (ROOT / index[ref_key]).is_file()

    readme = (LIB / "README.md").read_text(encoding="utf-8")
    schema = (LIB / "SCHEMA.md").read_text(encoding="utf-8")
    selection = (ROOT / index["selection_ref"]).read_text(encoding="utf-8")

    assert "COMPLETE_10_OF_10__PHASE_B_SELECTION_COMPLETE" in readme
    assert "no final ADOPT / REJECT / MERGE decision" not in readme.lower()
    assert "End-to-end workflow" in schema
    assert "Skill / Agent / Runtime / Harness architecture" in schema
    assert "Hidden assumptions and inferred invariants" in schema
    assert "production_promotion_requires_separate_regression_backed_change" in readme.lower()
    assert "STRONGEST ARCHITECTURE REFERENCE" in selection
    assert "Explicitly rejected mechanisms" in selection


def test_top10_selection_is_primitive_level_not_popularity_copying():
    index = load_index()
    selection = (ROOT / index["selection_ref"]).read_text(encoding="utf-8")

    assert "not choosing the most popular Skills" in selection
    assert "primitive-level" in index["selection_principle"]
    assert "popularity" in index["selection_principle"]
    assert "No selected mechanism justifies a new permanent root Agent" in selection
