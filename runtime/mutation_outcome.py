from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MutationOutcome(str, Enum):
    CONFIRMED_SUCCESS = "CONFIRMED_SUCCESS"
    CONFIRMED_FAILURE = "CONFIRMED_FAILURE"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


@dataclass(frozen=True)
class MutationOutcomeDecision:
    outcome: MutationOutcome
    retry_allowed: bool
    reconciliation_required: bool
    reason: str


def classify_mutation_outcome(
    *,
    dispatched: bool | None,
    postcondition_verified: bool | None,
    provider_confirmed_applied: bool | None = None,
    operation_idempotent: bool = False,
    idempotency_key_present: bool = False,
) -> MutationOutcomeDecision:
    """Classify a mutation without converting transport ambiguity into false failure.

    `postcondition_verified=True` means the intended final state was observed.
    `postcondition_verified=False` means the intended mutation was verified *not* to
    have applied. `None` means final state was not verified.

    `dispatched=None` represents an execution boundary where the caller cannot prove
    whether the provider received the mutation. This is materially different from
    `dispatched=False`.
    """

    if postcondition_verified is True or provider_confirmed_applied is True:
        return MutationOutcomeDecision(
            MutationOutcome.CONFIRMED_SUCCESS,
            retry_allowed=False,
            reconciliation_required=False,
            reason="mutation application is verified",
        )

    if postcondition_verified is False:
        return MutationOutcomeDecision(
            MutationOutcome.CONFIRMED_FAILURE,
            retry_allowed=True,
            reconciliation_required=False,
            reason="final state was verified not applied",
        )

    if dispatched is False:
        return MutationOutcomeDecision(
            MutationOutcome.CONFIRMED_FAILURE,
            retry_allowed=True,
            reconciliation_required=False,
            reason="mutation was verified not dispatched",
        )

    safe_retry = operation_idempotent or idempotency_key_present
    return MutationOutcomeDecision(
        MutationOutcome.OUTCOME_UNKNOWN,
        retry_allowed=safe_retry,
        reconciliation_required=True,
        reason=(
            "mutation may have crossed the execution boundary; reconcile final state before treating it as success or failure"
            if not safe_retry
            else "mutation outcome is unknown; retry may be transport-safe because idempotence is available, but final state still requires reconciliation"
        ),
    )
