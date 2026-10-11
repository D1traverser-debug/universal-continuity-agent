import json
from pathlib import Path

from runtime.mutation_outcome import MutationOutcome, classify_mutation_outcome


ROOT = Path(__file__).resolve().parents[1]


def test_verified_applied_is_confirmed_success():
    result = classify_mutation_outcome(
        dispatched=True,
        postcondition_verified=True,
        operation_idempotent=False,
    )
    assert result.outcome == MutationOutcome.CONFIRMED_SUCCESS
    assert result.retry_allowed is False
    assert result.reconciliation_required is False


def test_verified_not_applied_is_confirmed_failure_and_retryable():
    result = classify_mutation_outcome(
        dispatched=True,
        postcondition_verified=False,
        operation_idempotent=False,
    )
    assert result.outcome == MutationOutcome.CONFIRMED_FAILURE
    assert result.retry_allowed is True
    assert result.reconciliation_required is False


def test_verified_not_dispatched_is_confirmed_failure():
    result = classify_mutation_outcome(
        dispatched=False,
        postcondition_verified=None,
        operation_idempotent=False,
    )
    assert result.outcome == MutationOutcome.CONFIRMED_FAILURE
    assert result.retry_allowed is True


def test_non_idempotent_possible_dispatch_without_postcondition_is_unknown_and_not_retryable():
    result = classify_mutation_outcome(
        dispatched=True,
        postcondition_verified=None,
        operation_idempotent=False,
        idempotency_key_present=False,
    )
    assert result.outcome == MutationOutcome.OUTCOME_UNKNOWN
    assert result.retry_allowed is False
    assert result.reconciliation_required is True


def test_unknown_dispatch_boundary_is_not_false_failure():
    result = classify_mutation_outcome(
        dispatched=None,
        postcondition_verified=None,
        operation_idempotent=False,
    )
    assert result.outcome == MutationOutcome.OUTCOME_UNKNOWN
    assert result.retry_allowed is False


def test_idempotency_key_allows_retry_but_does_not_upgrade_unknown_to_success():
    result = classify_mutation_outcome(
        dispatched=True,
        postcondition_verified=None,
        operation_idempotent=False,
        idempotency_key_present=True,
    )
    assert result.outcome == MutationOutcome.OUTCOME_UNKNOWN
    assert result.retry_allowed is True
    assert result.reconciliation_required is True


def test_policy_binds_runtime_and_forbids_blind_non_idempotent_retry():
    policy = json.loads((ROOT / "ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json").read_text(encoding="utf-8"))
    semantics = policy["mutation_outcome_semantics"]
    assert policy["schema_version"] == "1.2"
    assert semantics["runtime"] == "runtime/mutation_outcome.py"
    assert semantics["blind_retry_non_idempotent_unknown_allowed"] is False
    assert semantics["outcome_unknown_is_commit_proof"] is False
    assert semantics["outcome_unknown_is_failure_proof"] is False
    assert policy["failure_semantics"]["non_idempotent_mutation_outcome_unknown"] == "BLOCK_BLIND_RETRY_AND_RECONCILE_OR_PERSIST_EXACT_UNKNOWN_STATE"
