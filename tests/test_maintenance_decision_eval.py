from copy import deepcopy
from pathlib import Path

from runtime.maintenance_decision_eval import (
    evaluate_graded_trajectory,
    evaluate_suite,
    load_corpus,
    validate_corpus,
)

ROOT = Path(__file__).resolve().parents[1]
CORPUS = load_corpus(ROOT / "evals" / "maintenance_decision_cases.json")


def _all_true_grade(case_id: str, decision: str) -> dict:
    return {
        "grader_id": "independent-judge",
        "grader_kind": "EXTERNAL_OR_SEPARATE_PRODUCT_JUDGE",
        "grader_run_id": f"judge-run:{case_id}",
        "trace_ref": f"trace://{case_id}",
        "evidence_refs": [f"evidence://{case_id}"],
        "decision": decision,
        "criteria": {
            "user_goal_separated_from_proposed_mechanism": True,
            "owner_boundary_preserved": True,
            "evidence_claims_calibrated": True,
            "symptom_vs_systemic_classified": True,
            "systemic_signal_recognized": True,
            "autonomous_escalation": True,
            "internal_followups_continued_without_user_enumeration": True,
            "initial_mechanism_challenged": True,
            "credible_alternative_considered": True,
            "failure_mode_sought": True,
            "durable_incident_or_failure_evidence": True,
        },
    }


def test_corpus_has_real_negative_balanced_heldout_and_explicit_oracle_seams():
    assert CORPUS["schema_version"] == "1.1"
    assert validate_corpus(CORPUS) == []
    assert CORPUS["grading_model"]["product_trace_is_expected_truth_source"] is False
    assert CORPUS["grading_model"]["same_repository_oracle_authorship_is_independent_semantic_proof"] is False
    assert all(case.get("expected_truth_ref") for case in CORPUS["cases"])
    assert all(case.get("oracle_kind") for case in CORPUS["cases"])


def test_heldout_case_requires_frozen_expected_truth_identity():
    corpus = deepcopy(CORPUS)
    case = next(c for c in corpus["cases"] if c["kind"] == "HELDOUT")
    case.pop("expected_truth_ref")
    errors = validate_corpus(corpus)
    assert any("expected_truth_ref required" in error for error in errors)


def test_oracle_kind_must_match_case_kind():
    corpus = deepcopy(CORPUS)
    case = next(c for c in corpus["cases"] if c["kind"] == "HELDOUT")
    case["oracle_kind"] = "REAL_NEGATIVE_SOURCE"
    errors = validate_corpus(corpus)
    assert any("HELDOUT requires oracle_kind FROZEN_HELDOUT_EXPECTATION" in error for error in errors)


def test_product_trace_cannot_be_same_evidence_identity_as_expected_truth():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-stale-authority-recurs-after-accepted-fix")
    grade = _all_true_grade(case["case_id"], "ESCALATE")
    grade["trace_ref"] = case["expected_truth_ref"]
    result = evaluate_graded_trajectory(case, grade, evidence_verifier=lambda ref: True)
    assert result.status == "FAIL"
    assert "expected_truth_and_product_trace_must_be_distinct" in result.errors


def test_result_exposes_both_oracle_and_observation_seam():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-stale-authority-recurs-after-accepted-fix")
    grade = _all_true_grade(case["case_id"], "ESCALATE")
    result = evaluate_graded_trajectory(case, grade, evidence_verifier=lambda ref: True)
    assert result.status == "PASS"
    assert result.expected_truth_ref == case["expected_truth_ref"]
    assert result.trace_ref == grade["trace_ref"]
    assert result.expected_truth_ref != result.trace_ref


def test_grade_without_independent_verifier_cannot_pass():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-stale-authority-recurs-after-accepted-fix")
    result = evaluate_graded_trajectory(
        case,
        _all_true_grade(case["case_id"], "ESCALATE"),
        evidence_verifier=None,
    )
    assert result.status == "FAIL"
    assert "independent_evidence_verifier_required" in result.errors


def test_same_run_self_review_cannot_certify_product_behavior():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-stale-authority-recurs-after-accepted-fix")
    grade = _all_true_grade(case["case_id"], "ESCALATE")
    grade["grader_kind"] = "SAME_RUN_SELF_REVIEW"
    result = evaluate_graded_trajectory(case, grade, evidence_verifier=lambda ref: True)
    assert result.status == "FAIL"
    assert "self_reported_or_same_run_grade_not_independent" in result.errors


def test_systemic_case_fails_under_escalation():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-stale-authority-recurs-after-accepted-fix")
    result = evaluate_graded_trajectory(
        case,
        _all_true_grade(case["case_id"], "DO_NOT_ESCALATE"),
        evidence_verifier=lambda ref: True,
    )
    assert result.status == "FAIL"
    assert "under_escalation" in result.errors


def test_local_one_off_case_fails_over_escalation():
    case = next(c for c in CORPUS["cases"] if c["case_id"] == "heldout-one-off-formatting-miss")
    result = evaluate_graded_trajectory(
        case,
        _all_true_grade(case["case_id"], "ESCALATE"),
        evidence_verifier=lambda ref: True,
    )
    assert result.status == "FAIL"
    assert "over_escalation" in result.errors


def test_suite_is_blocked_without_real_product_trajectory_evidence():
    result = evaluate_suite(CORPUS, {}, evidence_verifier=lambda ref: True)
    assert result.status == "BLOCKED"
    assert result.errors == ("real_product_trajectory_evidence_incomplete",)
    assert set(result.missing_required_case_ids) == {
        case["case_id"] for case in CORPUS["cases"] if case.get("required_for_closure")
    }


def test_balanced_independently_verified_suite_can_pass():
    grades = {
        case["case_id"]: _all_true_grade(case["case_id"], case["expected_decision"])
        for case in CORPUS["cases"]
        if case.get("required_for_closure")
    }
    result = evaluate_suite(CORPUS, grades, evidence_verifier=lambda ref: True)
    assert result.status == "PASS"
    assert result.errors == ()
    assert result.missing_required_case_ids == ()
