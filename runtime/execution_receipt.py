from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
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


ReplayHistoryVerifier = Callable[[tuple[Mapping[str, Any], ...]], bool]

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
REQUIRED_MAPPING_FIELDS = ("subject_bindings", "input_bindings")
IDENTITY_FIELDS = ("task_id", "stage", "capability_id", "action_id")
REQUIRED_EXPECTATION_TEXT_FIELDS = (*IDENTITY_FIELDS, "executor_identity", "result")
DEFAULT_ANTI_REPLAY_FIELDS = ("receipt_id",)


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _string_sequence(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return None
    normalized = tuple(_text(item) for item in value)
    if not normalized or any(not item for item in normalized):
        return None
    return normalized


def _validate_required_shape(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TEXT_FIELDS:
        if not _text(receipt.get(field)):
            errors.append(f"missing_or_blank:{field}")
    for field in REQUIRED_MAPPING_FIELDS:
        if not isinstance(receipt.get(field), Mapping):
            errors.append(f"missing_or_invalid_mapping:{field}")
    if _string_sequence(receipt.get("output_refs")) is None:
        errors.append("output_refs_must_be_non_empty_strings")
    return errors


def _validate_expectation_shape(expectation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_EXPECTATION_TEXT_FIELDS:
        if not _text(expectation.get(field)):
            errors.append(f"expectation_missing_or_blank:{field}")
    for field in REQUIRED_MAPPING_FIELDS:
        value = expectation.get(field)
        if not isinstance(value, Mapping) or not value:
            errors.append(f"expectation_missing_or_invalid_mapping:{field}")
    if _string_sequence(expectation.get("output_refs")) is None:
        errors.append("expectation_output_refs_must_be_non_empty_strings")
    return errors


def _binding_errors(
    receipt: Mapping[str, Any],
    expectation: Mapping[str, Any],
    *,
    field: str,
) -> list[str]:
    expected = expectation.get(field)
    if not isinstance(expected, Mapping):
        return []
    actual = receipt.get(field)
    if not isinstance(actual, Mapping):
        return []
    errors: list[str] = []
    for key, expected_value in expected.items():
        if key not in actual:
            errors.append(f"binding_missing:{field}:{key}")
        elif actual.get(key) != expected_value:
            errors.append(f"binding_mismatch:{field}:{key}")
    return errors


def validate_execution_receipt_binding(
    receipt: Mapping[str, Any],
    expectation: Mapping[str, Any],
    *,
    prior_receipts: Iterable[Mapping[str, Any]] = (),
    anti_replay_fields: Sequence[str] = DEFAULT_ANTI_REPLAY_FIELDS,
    replay_history_verifier: ReplayHistoryVerifier | None = None,
) -> ReceiptBindingResult:
    """Validate that an execution receipt proves the exact claim it is used for.

    Contract 1.1 treats the *expectation* and replay-history completeness as security
    inputs, not trusted caller conveniences. An exact gate must provide all core
    identities, non-empty subject/input bindings, expected result, and expected output
    refs. ``receipt_id`` replay protection is mandatory and cannot be disabled by an
    empty caller-supplied anti-replay list. A verifier must attest that the supplied
    prior-receipt set is the history relevant to the gate before a PASS can be issued.

    This validator still does not establish executor trust, provider issuance,
    chronology, reviewer independence, or semantic quality. Those are higher-assurance
    questions owned by the relevant execution/review contract.
    """

    errors = _validate_required_shape(receipt)
    errors.extend(_validate_expectation_shape(expectation))

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

    actual_outputs = _string_sequence(receipt.get("output_refs")) or ()
    expected_outputs = _string_sequence(expectation.get("output_refs")) or ()
    for ref in expected_outputs:
        if ref not in actual_outputs:
            errors.append(f"output_ref_missing:{ref}")

    prior = tuple(item for item in prior_receipts if isinstance(item, Mapping))
    if replay_history_verifier is None:
        errors.append("replay_history_verifier_required")
    else:
        try:
            history_verified = bool(replay_history_verifier(prior))
        except Exception:
            history_verified = False
        if not history_verified:
            errors.append("replay_history_not_verified_complete")

    effective_anti_replay_fields = list(DEFAULT_ANTI_REPLAY_FIELDS)
    for raw_field in anti_replay_fields:
        field = _text(raw_field)
        if field and field not in effective_anti_replay_fields:
            effective_anti_replay_fields.append(field)

    for field in effective_anti_replay_fields:
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
