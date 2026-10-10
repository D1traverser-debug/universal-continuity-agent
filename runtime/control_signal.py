from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


ALLOWED_TYPES = {
    "AGENT_ARCHITECTURE_DRIFT",
    "OWNER_HEAD_FRESHNESS_DRIFT",
    "OWNER_CI_FAILURE",
    "CAPABILITY_OR_CONTRACT_DRIFT",
    "CONTINUITY_RECOVERY_DRIFT",
    "USER_REPORTED_SYSTEMIC_FAILURE",
    "OTHER_CONTROL_PLANE_SIGNAL",
}
ALLOWED_SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
REQUIRED_FIELDS = (
    "signal_id",
    "signal_type",
    "source",
    "observed_at",
    "subject",
    "summary",
    "evidence_refs",
    "severity",
)


@dataclass(frozen=True)
class SignalValidation:
    valid: bool
    errors: tuple[str, ...]


def validate_control_signal(signal: Mapping[str, Any]) -> SignalValidation:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        value = signal.get(field)
        if field == "evidence_refs":
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                errors.append("evidence_refs must be a non-empty string list")
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"{field} is required")
    if signal.get("signal_type") not in ALLOWED_TYPES:
        errors.append("signal_type is invalid")
    if signal.get("severity") not in ALLOWED_SEVERITIES:
        errors.append("severity is invalid")
    if signal.get("authoritative_state_mutation") not in (None, False):
        errors.append("control signal cannot claim authoritative_state_mutation")
    return SignalValidation(valid=not errors, errors=tuple(errors))
