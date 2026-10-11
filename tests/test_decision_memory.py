import json
from pathlib import Path

from runtime.decision_memory import (
    RejectionHorizon,
    extract_negative_decisions,
    search_negative_decisions,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_2026-10-11.json"


def test_current_meta_run_exposes_searchable_negative_decision_memory():
    run = json.loads(AUDIT.read_text(encoding="utf-8"))
    result = extract_negative_decisions(run, source_ref=AUDIT.relative_to(ROOT).as_posix())
    assert result.status == "PASS", result.errors
    assert len(result.records) >= 2
    assert all(record.concept_key for record in result.records)
    assert all(record.reconsider_when for record in result.records)


def test_rejected_mechanism_requires_concept_horizon_and_reconsider_condition():
    run = {
        "run_id": "x",
        "alternatives": [
            {
                "id": "new-agent",
                "decision": "REJECTED",
                "rationale": "Duplicates current runtime.",
            }
        ],
    }
    result = extract_negative_decisions(run, source_ref="audit://x")
    assert result.status == "FAIL"
    assert "alternative_0_concept_key_required" in result.errors
    assert "alternative_0_rejection_horizon_invalid" in result.errors


def test_scope_local_rejection_requires_scope_boundary():
    run = {
        "run_id": "x",
        "alternatives": [
            {
                "id": "visual-method-globalization",
                "concept_key": "frontend-design/globalize-to-universal",
                "decision": "REJECTED",
                "rationale": "Useful only in visual owners.",
                "rejection_horizon": "SCOPE_LOCAL",
                "reconsider_when": "Reconsider only if cross-owner evidence demonstrates general value.",
            }
        ],
    }
    result = extract_negative_decisions(run, source_ref="audit://x")
    assert result.status == "FAIL"
    assert "alternative_0_scope_boundary_required" in result.errors


def test_negative_decisions_are_searchable_by_concept_not_chat_memory():
    run = json.loads(AUDIT.read_text(encoding="utf-8"))
    extracted = extract_negative_decisions(run, source_ref=AUDIT.relative_to(ROOT).as_posix())
    matches = search_negative_decisions(extracted.records, concept_query="supervisory")
    assert matches
    assert any("supervisory" in record.concept_key for record in matches)
    assert all(record.rejection_horizon == RejectionHorizon.PERMANENT_UNTIL_EVIDENCE_CHANGE for record in matches)
