from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping


class RejectionHorizon(str, Enum):
    PERMANENT_UNTIL_EVIDENCE_CHANGE = "PERMANENT_UNTIL_EVIDENCE_CHANGE"
    TEMPORARY_NOT_NOW = "TEMPORARY_NOT_NOW"
    SCOPE_LOCAL = "SCOPE_LOCAL"


@dataclass(frozen=True)
class NegativeDecisionRecord:
    source_ref: str
    run_id: str
    alternative_id: str
    concept_key: str
    rationale: str
    rejection_horizon: RejectionHorizon
    reconsider_when: str
    scope_boundary: str | None


@dataclass(frozen=True)
class DecisionMemoryExtraction:
    status: str
    records: tuple[NegativeDecisionRecord, ...]
    errors: tuple[str, ...]


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def extract_negative_decisions(
    run: Mapping[str, Any],
    *,
    source_ref: str,
) -> DecisionMemoryExtraction:
    """Extract searchable rejected alternatives from a structured maintenance run.

    The audit run remains the durable source. This module creates no new authority
    database; it only makes rejected mechanisms queryable by stable concept key.
    """

    errors: list[str] = []
    records: list[NegativeDecisionRecord] = []
    run_id = str(run.get("run_id", "")).strip()
    if not run_id:
        errors.append("run_id_required")

    alternatives = run.get("alternatives")
    if not isinstance(alternatives, list):
        return DecisionMemoryExtraction("FAIL", (), (*errors, "alternatives_list_required"))

    seen_keys: set[str] = set()
    for index, raw in enumerate(alternatives):
        if not isinstance(raw, Mapping):
            errors.append(f"alternative_{index}_must_be_mapping")
            continue
        if str(raw.get("decision", "")).upper() != "REJECTED":
            continue

        alternative_id = str(raw.get("id", "")).strip()
        concept_key = str(raw.get("concept_key", "")).strip()
        rationale = str(raw.get("rationale", "")).strip()
        horizon_raw = str(raw.get("rejection_horizon", "")).strip()
        reconsider_when = str(raw.get("reconsider_when", "")).strip()
        scope_boundary = str(raw.get("scope_boundary", "")).strip() or None

        if not alternative_id:
            errors.append(f"alternative_{index}_id_required")
        if not concept_key:
            errors.append(f"alternative_{index}_concept_key_required")
        elif concept_key in seen_keys:
            errors.append(f"duplicate_concept_key:{concept_key}")
        else:
            seen_keys.add(concept_key)
        if not rationale:
            errors.append(f"alternative_{index}_rationale_required")

        try:
            horizon = RejectionHorizon(horizon_raw)
        except ValueError:
            errors.append(f"alternative_{index}_rejection_horizon_invalid")
            continue

        if not reconsider_when:
            errors.append(f"alternative_{index}_reconsider_when_required")
        if horizon == RejectionHorizon.SCOPE_LOCAL and not scope_boundary:
            errors.append(f"alternative_{index}_scope_boundary_required")

        if alternative_id and concept_key and rationale and reconsider_when and (
            horizon != RejectionHorizon.SCOPE_LOCAL or scope_boundary
        ):
            records.append(
                NegativeDecisionRecord(
                    source_ref=source_ref,
                    run_id=run_id,
                    alternative_id=alternative_id,
                    concept_key=concept_key,
                    rationale=rationale,
                    rejection_horizon=horizon,
                    reconsider_when=reconsider_when,
                    scope_boundary=scope_boundary,
                )
            )

    return DecisionMemoryExtraction(
        status="PASS" if not errors else "FAIL",
        records=tuple(records),
        errors=tuple(errors),
    )


def search_negative_decisions(
    records: Iterable[NegativeDecisionRecord],
    *,
    concept_query: str,
) -> tuple[NegativeDecisionRecord, ...]:
    query = concept_query.strip().lower()
    if not query:
        return ()
    return tuple(
        record
        for record in records
        if query in record.concept_key.lower()
        or query in record.alternative_id.lower()
        or query in record.rationale.lower()
    )
