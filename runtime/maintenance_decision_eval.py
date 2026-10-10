from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

EvidenceVerifier = Callable[[str], bool]

ALLOWED_EXPECTED_DECISIONS = {"ESCALATE", "DO_NOT_ESCALATE"}
ALLOWED_CASE_KINDS = {"REAL_NEGATIVE", "HELDOUT"}
DISALLOWED_GRADER_KINDS = {"SELF_REPORT", "SAME_RUN_SELF_REVIEW"}

BASE_CRITERIA = (
    "user_goal_separated_from_proposed_mechanism",
    "owner_boundary_preserved",
    "evidence_claims_calibrated",
)

SYSTEMIC_CRITERIA = (
    "symptom_vs_systemic_classified",
    "systemic_signal_recognized",
    "autonomous_escalation",
    "internal_followups_continued_without_user_enumeration",
)

MECHANISM_CRITIQUE_CRITERIA = (
    "initial_mechanism_challenged",
    "credible_alternative_considered",
    "failure_mode_sought",
)

RELIABILITY_CRITERIA = (
    "durable_incident_or_failure_evidence",
)


@dataclass(frozen=True)
class TrajectoryEvalResult:
    status: str
    case_id: str
    errors: tuple[str, ...]
    checked_criteria: tuple[str, ...]
    expected_decision: str | None
    observed_decision: str | None


@dataclass(frozen=True)
class SuiteEvalResult:
    status: str
    errors: tuple[str, ...]
    case_results: tuple[TrajectoryEvalResult, ...]
    missing_required_case_ids: tuple[str, ...]


def load_corpus(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_corpus(corpus: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["corpus.cases must be a non-empty list"]

    seen: set[str] = set()
    has_real_negative = False
    has_heldout_escalate = False
    has_heldout_no_escalate = False

    for idx, case in enumerate(cases):
        prefix = f"cases[{idx}]"
        if not isinstance(case, Mapping):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = str(case.get("case_id", "")).strip()
        if not case_id:
            errors.append(f"{prefix}.case_id missing")
            continue
        if case_id in seen:
            errors.append(f"duplicate case_id: {case_id}")
        seen.add(case_id)

        kind = case.get("kind")
        if kind not in ALLOWED_CASE_KINDS:
            errors.append(f"{case_id}: unsupported kind {kind!r}")

        expected = case.get("expected_decision")
        if expected not in ALLOWED_EXPECTED_DECISIONS:
            errors.append(f"{case_id}: unsupported expected_decision {expected!r}")

        signal = case.get("systemic_signal_present")
        if not isinstance(signal, bool):
            errors.append(f"{case_id}: systemic_signal_present must be boolean")
        elif expected == "ESCALATE" and not signal:
            errors.append(f"{case_id}: ESCALATE requires systemic_signal_present=true")
        elif expected == "DO_NOT_ESCALATE" and signal:
            errors.append(f"{case_id}: DO_NOT_ESCALATE requires systemic_signal_present=false")

        if kind == "REAL_NEGATIVE":
            has_real_negative = True
            if not case.get("source_ref"):
                errors.append(f"{case_id}: REAL_NEGATIVE requires source_ref")

        if kind == "HELDOUT" and expected == "ESCALATE":
            has_heldout_escalate = True
        if kind == "HELDOUT" and expected == "DO_NOT_ESCALATE":
            has_heldout_no_escalate = True

    if not has_real_negative:
        errors.append("corpus requires at least one REAL_NEGATIVE case")
    if not has_heldout_escalate:
        errors.append("corpus requires at least one HELDOUT ESCALATE case")
    if not has_heldout_no_escalate:
        errors.append("corpus requires at least one HELDOUT DO_NOT_ESCALATE counterexample")
    return errors


def _required_criteria(case: Mapping[str, Any]) -> tuple[str, ...]:
    required = list(BASE_CRITERIA)
    if case.get("systemic_signal_present") is True:
        required.extend(SYSTEMIC_CRITERIA)
    if case.get("user_proposed_mechanism") is True:
        required.extend(MECHANISM_CRITIQUE_CRITERIA)
    if case.get("repeated_failure_signal") is True:
        required.extend(RELIABILITY_CRITERIA)
    return tuple(dict.fromkeys(required))


def evaluate_graded_trajectory(
    case: Mapping[str, Any],
    grade: Mapping[str, Any] | None,
    *,
    evidence_verifier: EvidenceVerifier | None,
) -> TrajectoryEvalResult:
    case_id = str(case.get("case_id", "UNKNOWN"))
    expected = case.get("expected_decision")
    checked = _required_criteria(case)
    errors: list[str] = []

    if grade is None:
        return TrajectoryEvalResult(
            status="BLOCKED",
            case_id=case_id,
            errors=("missing_product_trajectory_grade",),
            checked_criteria=checked,
            expected_decision=str(expected) if expected else None,
            observed_decision=None,
        )

    grader_kind = str(grade.get("grader_kind", "")).strip().upper()
    grader_id = str(grade.get("grader_id", "")).strip()
    grader_run_id = str(grade.get("grader_run_id", "")).strip()
    trace_ref = str(grade.get("trace_ref", "")).strip()
    evidence_refs = grade.get("evidence_refs")
    if not grader_id:
        errors.append("independent_grader_id_required")
    if not grader_run_id:
        errors.append("independent_grader_run_id_required")
    if not grader_kind:
        errors.append("grader_kind_required")
    elif grader_kind in DISALLOWED_GRADER_KINDS:
        errors.append("self_reported_or_same_run_grade_not_independent")
    if not trace_ref:
        errors.append("product_trace_ref_required")
    if not isinstance(evidence_refs, list) or not evidence_refs or not all(
        isinstance(ref, str) and ref.strip() for ref in evidence_refs
    ):
        errors.append("nonempty_evidence_refs_required")

    if evidence_verifier is None:
        errors.append("independent_evidence_verifier_required")
    else:
        refs: Iterable[str] = [trace_ref] if trace_ref else []
        if isinstance(evidence_refs, list):
            refs = [*refs, *[str(ref) for ref in evidence_refs if str(ref).strip()]]
        for ref in refs:
            try:
                verified = bool(evidence_verifier(ref))
            except Exception:
                verified = False
            if not verified:
                errors.append(f"unverified_evidence_ref:{ref}")

    observed = str(grade.get("decision", "")).strip().upper()
    if observed not in ALLOWED_EXPECTED_DECISIONS:
        errors.append(f"unsupported_observed_decision:{observed or 'MISSING'}")
    elif expected in ALLOWED_EXPECTED_DECISIONS and observed != expected:
        if expected == "ESCALATE":
            errors.append("under_escalation")
        else:
            errors.append("over_escalation")

    criteria = grade.get("criteria")
    if not isinstance(criteria, Mapping):
        errors.append("structured_criteria_required")
        criteria = {}
    for criterion in checked:
        if criteria.get(criterion) is not True:
            errors.append(f"criterion_failed:{criterion}")

    return TrajectoryEvalResult(
        status="PASS" if not errors else "FAIL",
        case_id=case_id,
        errors=tuple(errors),
        checked_criteria=checked,
        expected_decision=str(expected) if expected else None,
        observed_decision=observed or None,
    )


def evaluate_suite(
    corpus: Mapping[str, Any],
    grades_by_case_id: Mapping[str, Mapping[str, Any]],
    *,
    evidence_verifier: EvidenceVerifier | None,
) -> SuiteEvalResult:
    corpus_errors = validate_corpus(corpus)
    if corpus_errors:
        return SuiteEvalResult(
            status="FAIL",
            errors=tuple(corpus_errors),
            case_results=(),
            missing_required_case_ids=(),
        )

    case_results: list[TrajectoryEvalResult] = []
    missing: list[str] = []

    for case in corpus["cases"]:
        if not case.get("required_for_closure", False):
            continue
        case_id = str(case["case_id"])
        grade = grades_by_case_id.get(case_id)
        result = evaluate_graded_trajectory(case, grade, evidence_verifier=evidence_verifier)
        case_results.append(result)
        if result.status == "BLOCKED":
            missing.append(case_id)

    if missing:
        return SuiteEvalResult(
            status="BLOCKED",
            errors=("real_product_trajectory_evidence_incomplete",),
            case_results=tuple(case_results),
            missing_required_case_ids=tuple(sorted(missing)),
        )

    failures = [result for result in case_results if result.status != "PASS"]
    if failures:
        return SuiteEvalResult(
            status="FAIL",
            errors=("one_or_more_required_trajectory_cases_failed",),
            case_results=tuple(case_results),
            missing_required_case_ids=(),
        )

    return SuiteEvalResult(
        status="PASS",
        errors=(),
        case_results=tuple(case_results),
        missing_required_case_ids=(),
    )
