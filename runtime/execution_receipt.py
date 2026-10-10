from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ReceiptBindingStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ReceiptBindingResult:
    status: ReceiptBindingStatus
    errors: tuple[str, ...]


REQUIRED_TEXT_FIELDS = (
    "receipt_id",
    "action_id",
    "task_id",
    "stage",
    "capability_id",
    "executor_identity",
    "execution_ref",
    "result",
)

REQUIRED_MAPPING_FIELDS = (
    "subject_bindings",
    "input_bindings",
)

IDENTITY_FIELDS = (
    "task_id",
    "stage",
    "capability_id",
    "action_id",
)


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _validate_required_shape(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TEXT_FIELDS:
        if not _text(receipt.get(field)):
            errors.append(f"missing_or_blank:{field}")

    for field in REQUIRED_MAPPING_FIELDS:
        value = receipt.get(field)
        if not isinstance(value, Mapping):
            errors.append(f"missing_or_invalid_mapping:{field}")

    output_refs = receipt.get("output_refs")
    if not isinstance(output_refs, Sequence) or isinstance(output_refs, (str, bytes)):
        errors.append("missing_or_invalid:output_refs")
    else:
        normalized = [_text(item) for item in output_refs]
        if not normalized or any(not item for item in normalized):
            errors.append("output_refs_must_be_non_empty_strings")

    return errors


def _binding_errors(
    receipt: Mapping[str, Any],
    expectation: Mapping[str, Any],
    *,
    field: str,
) -> list[str]:
    expected = expectation.get(field, {})
    if expected is None:
        expected = {}
    if not isinstance(expected, Mapping):
        return [f"invalid_expectation_mapping:{field}"]

    actual = receipt.get(field)
    if not isinstance(actual, Mapping):
        return []

    errors: list[str] = []
    for key, expected_value in expected.items():
        if key not in actual:
            errors.append(f"binding_missing:{field}:{key}")
            continue
        if actual.get(key) != expected_value:
            errors.append(f"binding_mismatch:{field}:{key}")
    return errors


def validate_execution_receipt_binding(
    receipt: Mapping[str, Any],
    expectation: Mapping[str, Any],
    *,
    prior_receipts: Iterable[Mapping[str, Any]] = (),
    anti_replay_fields: Sequence[str] = ("receipt_id",),
) -> ReceiptBindingResult:
    """Validate that an execution receipt proves the exact claim it is being used for.

    This validator intentionally does not decide whether an executor is trustworthy or
    whether an external provider trace is independently attested. Those are separate
    assurance questions. It closes a narrower but cross-agent gap: a real receipt or
    evidence reference cannot satisfy a different task/stage/capability/action, cannot
    silently swap claim/input bindings, and cannot be replayed when a caller marks an
    identity field as single-use.

    Owners can place domain-specific identities in ``subject_bindings`` (for example a
    candidate id, brief digest, replay-cassette set, or review packet id) and immutable
    input identities/digests in ``input_bindings``. The caller supplies the expected
    subset for the exact gate being advanced.
    """

    errors = _validate_required_shape(receipt)

    for field in IDENTITY_FIELDS:
        expected = _text(expectation.get(field))
        if expected and _text(receipt.get(field)) != expected:
            errors.append(f"identity_mismatch:{field}")

    expected_executor = _text(expectation.get("executor_identity"))
    if expected_executor and _text(receipt.get("executor_identity")) != expected_executor:
        errors.append("identity_mismatch:executor_identity")

    expected_result = _text(expectation.get("result"))
    if expected_result and _text(receipt.get("result")) != expected_result:
        errors.append("result_mismatch")

    errors.extend(_binding_errors(receipt, expectation, field="subject_bindings"))
    errors.extend(_binding_errors(receipt, expectation, field="input_bindings"))

    prior = tuple(item for item in prior_receipts if isinstance(item, Mapping))
    for field in anti_replay_fields:
        field = _text(field)
        if not field:
            continue
        value = receipt.get(field)
        if value is None or value == "":
            errors.append(f"anti_replay_field_missing:{field}")
            continue
        if any(previous.get(field) == value for previous in prior):
            errors.append(f"replayed:{field}")

    return ReceiptBindingResult(
        status=ReceiptBindingStatus.PASS if not errors else ReceiptBindingStatus.FAIL,
        errors=tuple(errors),
    )
