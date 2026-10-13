from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


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
ALLOWED_LIFECYCLE_STATES = {"ACTIVE", "HISTORICAL_OPEN", "RESOLVED"}
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
AGENT_READY_BRIEF_FIELDS = (
    "behavior",
    "current_state",
    "desired_state",
    "stable_interfaces",
    "acceptance_criteria",
    "out_of_scope",
    "evidence_refs",
)


class WorkAdmissionState(str, Enum):
    VERIFY_REQUIRED = "VERIFY_REQUIRED"
    FACT_GATHERING = "FACT_GATHERING"
    NEEDS_USER_INFORMATION = "NEEDS_USER_INFORMATION"
    NEEDS_HUMAN_JUDGMENT = "NEEDS_HUMAN_JUDGMENT"
    BRIEF_REQUIRED = "BRIEF_REQUIRED"
    READY_TO_DELEGATE = "READY_TO_DELEGATE"
    NOT_ACTIONABLE = "NOT_ACTIONABLE"


class SignalLifecycleState(str, Enum):
    ACTIVE = "ACTIVE"
    HISTORICAL_OPEN = "HISTORICAL_OPEN"
    RESOLVED = "RESOLVED"


@dataclass(frozen=True)
class SignalValidation:
    valid: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class WorkAdmissionDecision:
    state: WorkAdmissionState
    user_interruption_required: bool
    errors: tuple[str, ...]
    next_action: str


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty_string(item) for item in value)


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
    lifecycle_state = signal.get("lifecycle_state")
    if lifecycle_state is not None and lifecycle_state not in ALLOWED_LIFECYCLE_STATES:
        errors.append("lifecycle_state is invalid")
    if signal.get("authoritative_state_mutation") not in (None, False):
        errors.append("control signal cannot claim authoritative_state_mutation")
    return SignalValidation(valid=not errors, errors=tuple(errors))


def current_remediation_allowed(
    *,
    lifecycle_state: str | SignalLifecycleState,
    reobserved_current_condition: bool,
    current_authorization: bool,
) -> bool:
    """Return whether a signal may drive a present-tense state repair.

    Historical-open and resolved signals may still justify provenance/history work, but
    they cannot by themselves authorize current remediation. ACTIVE signals still need
    a fresh observation and current authority/user authorization.
    """

    try:
        state = SignalLifecycleState(str(lifecycle_state))
    except ValueError:
        return False
    if state is not SignalLifecycleState.ACTIVE:
        return False
    return bool(reobserved_current_condition and current_authorization)


def validate_agent_ready_brief(brief: Mapping[str, Any] | None) -> SignalValidation:
    if not isinstance(brief, Mapping):
        return SignalValidation(False, ("agent_ready_brief_required",))

    errors: list[str] = []
    for field in ("behavior", "current_state", "desired_state"):
        if not _nonempty_string(brief.get(field)):
            errors.append(f"agent_ready_brief.{field} is required")
    for field in ("stable_interfaces", "acceptance_criteria", "evidence_refs"):
        if not _nonempty_string_list(brief.get(field)):
            errors.append(f"agent_ready_brief.{field} must be a non-empty string list")
    out_of_scope = brief.get("out_of_scope")
    if not isinstance(out_of_scope, list) or any(not _nonempty_string(item) for item in out_of_scope):
        errors.append("agent_ready_brief.out_of_scope must be a string list")
    return SignalValidation(valid=not errors, errors=tuple(errors))


def assess_signal_admission(
    *,
    reobserved: bool,
    actionable: bool | None,
    retrievable_fact_gaps: Sequence[str] = (),
    unavailable_fact_gaps: Sequence[str] = (),
    human_judgment_required: bool = False,
    agent_ready_brief: Mapping[str, Any] | None = None,
) -> WorkAdmissionDecision:
    """Apply verify-before-clarify-before-delegate semantics to a control signal.

    Retrievable facts are system work and must not be escalated to the user as choices.
    User interruption is reserved for genuinely unavailable information or human judgment.
    Delegation requires a compact stable brief rather than raw chat/issue history.
    """

    if not reobserved:
        return WorkAdmissionDecision(
            WorkAdmissionState.VERIFY_REQUIRED,
            user_interruption_required=False,
            errors=(),
            next_action="re-observe the reported claim against current authority/environment",
        )

    if retrievable_fact_gaps:
        return WorkAdmissionDecision(
            WorkAdmissionState.FACT_GATHERING,
            user_interruption_required=False,
            errors=(),
            next_action="resolve retrievable facts autonomously before clarification or delegation",
        )

    if unavailable_fact_gaps:
        return WorkAdmissionDecision(
            WorkAdmissionState.NEEDS_USER_INFORMATION,
            user_interruption_required=True,
            errors=(),
            next_action="ask only for facts that cannot be safely retrieved or inferred",
        )

    if human_judgment_required:
        return WorkAdmissionDecision(
            WorkAdmissionState.NEEDS_HUMAN_JUDGMENT,
            user_interruption_required=True,
            errors=(),
            next_action="ask the user only for the genuine judgment or irreversible choice",
        )

    if actionable is False:
        return WorkAdmissionDecision(
            WorkAdmissionState.NOT_ACTIONABLE,
            user_interruption_required=False,
            errors=(),
            next_action="close or retain the signal with a durable not-actionable reason",
        )

    if actionable is not True:
        return WorkAdmissionDecision(
            WorkAdmissionState.FACT_GATHERING,
            user_interruption_required=False,
            errors=("actionability_not_resolved",),
            next_action="resolve actionability from current evidence",
        )

    brief_result = validate_agent_ready_brief(agent_ready_brief)
    if not brief_result.valid:
        return WorkAdmissionDecision(
            WorkAdmissionState.BRIEF_REQUIRED,
            user_interruption_required=False,
            errors=brief_result.errors,
            next_action="construct a stable Agent-ready brief from verified evidence before delegation",
        )

    return WorkAdmissionDecision(
        WorkAdmissionState.READY_TO_DELEGATE,
        user_interruption_required=False,
        errors=(),
        next_action="delegate using the stable brief and acceptance criteria",
    )
