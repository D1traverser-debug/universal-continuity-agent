from runtime.execution_receipt import (
    ReceiptBindingStatus,
    validate_execution_receipt_binding,
)


def receipt(**overrides):
    raw = {
        "receipt_id": "receipt-1",
        "action_id": "action-42",
        "task_id": "task-1",
        "stage": "REVIEW",
        "capability_id": "blind_pairwise_review",
        "executor_identity": "provider-runner-7",
        "execution_ref": "trace://provider/run-7",
        "subject_bindings": {
            "candidate_id": "candidate-v2",
            "candidate_change_ref": "sha256:candidate-v2",
        },
        "input_bindings": {
            "candidate_artifact": "sha256:candidate-artifact-v2",
            "baseline_artifact": "sha256:baseline-v1",
        },
        "output_refs": ["artifact://review/result-42"],
        "result": "PASS",
    }
    raw.update(overrides)
    return raw


def expectation(**overrides):
    raw = {
        "action_id": "action-42",
        "task_id": "task-1",
        "stage": "REVIEW",
        "capability_id": "blind_pairwise_review",
        "executor_identity": "provider-runner-7",
        "subject_bindings": {
            "candidate_id": "candidate-v2",
            "candidate_change_ref": "sha256:candidate-v2",
        },
        "input_bindings": {
            "candidate_artifact": "sha256:candidate-artifact-v2",
            "baseline_artifact": "sha256:baseline-v1",
        },
        "output_refs": ["artifact://review/result-42"],
        "result": "PASS",
    }
    raw.update(overrides)
    return raw


def complete_history(_history):
    return True


def validate(r=None, e=None, **kwargs):
    return validate_execution_receipt_binding(
        r or receipt(),
        e or expectation(),
        replay_history_verifier=kwargs.pop("replay_history_verifier", complete_history),
        **kwargs,
    )


def test_exact_execution_receipt_binding_passes():
    result = validate()
    assert result.status == ReceiptBindingStatus.PASS
    assert result.errors == ()


def test_wrong_task_stage_capability_or_action_cannot_reuse_real_receipt():
    for field, wrong_value in (
        ("task_id", "task-2"),
        ("stage", "FINAL_AUDIT"),
        ("capability_id", "source_audit"),
        ("action_id", "action-99"),
    ):
        result = validate(e=expectation(**{field: wrong_value}))
        assert result.status == ReceiptBindingStatus.FAIL
        assert f"identity_mismatch:{field}" in result.errors


def test_expectation_cannot_omit_exact_identity_or_result():
    for field in ("task_id", "stage", "capability_id", "action_id", "executor_identity", "result"):
        broken = expectation()
        broken.pop(field)
        result = validate(e=broken)
        assert result.status == ReceiptBindingStatus.FAIL
        assert f"expectation_missing_or_blank:{field}" in result.errors


def test_expectation_requires_nonempty_subject_input_and_output_bindings():
    for field, value, error in (
        ("subject_bindings", {}, "expectation_missing_or_invalid_mapping:subject_bindings"),
        ("input_bindings", {}, "expectation_missing_or_invalid_mapping:input_bindings"),
        ("output_refs", [], "expectation_output_refs_must_be_non_empty_strings"),
    ):
        result = validate(e=expectation(**{field: value}))
        assert result.status == ReceiptBindingStatus.FAIL
        assert error in result.errors


def test_old_or_foreign_claim_evidence_cannot_satisfy_current_candidate():
    result = validate(e=expectation(subject_bindings={
        "candidate_id": "candidate-v3",
        "candidate_change_ref": "sha256:candidate-v3",
    }))
    assert result.status == ReceiptBindingStatus.FAIL
    assert "binding_mismatch:subject_bindings:candidate_id" in result.errors
    assert "binding_mismatch:subject_bindings:candidate_change_ref" in result.errors


def test_wrong_input_digest_fails_even_when_receipt_exists():
    result = validate(e=expectation(input_bindings={
        "candidate_artifact": "sha256:candidate-artifact-v3",
        "baseline_artifact": "sha256:baseline-v1",
    }))
    assert result.status == ReceiptBindingStatus.FAIL
    assert "binding_mismatch:input_bindings:candidate_artifact" in result.errors


def test_wrong_or_missing_expected_output_fails():
    result = validate(e=expectation(output_refs=["artifact://review/other-result"]))
    assert result.status == ReceiptBindingStatus.FAIL
    assert "output_ref_missing:artifact://review/other-result" in result.errors


def test_receipt_id_replay_fails_by_default():
    result = validate(prior_receipts=[receipt(result="FAIL")])
    assert result.status == ReceiptBindingStatus.FAIL
    assert "replayed:receipt_id" in result.errors


def test_default_receipt_id_replay_protection_cannot_be_disabled():
    result = validate(prior_receipts=[receipt(result="FAIL")], anti_replay_fields=())
    assert result.status == ReceiptBindingStatus.FAIL
    assert "replayed:receipt_id" in result.errors


def test_replay_history_completeness_requires_verifier():
    result = validate_execution_receipt_binding(receipt(), expectation(), prior_receipts=[])
    assert result.status == ReceiptBindingStatus.FAIL
    assert "replay_history_verifier_required" in result.errors

    result = validate(replay_history_verifier=lambda history: False)
    assert result.status == ReceiptBindingStatus.FAIL
    assert "replay_history_not_verified_complete" in result.errors


def test_owner_can_require_execution_ref_single_use_for_independent_runs():
    previous = receipt(receipt_id="receipt-old")
    result = validate(
        prior_receipts=[previous],
        anti_replay_fields=("receipt_id", "execution_ref"),
    )
    assert result.status == ReceiptBindingStatus.FAIL
    assert "replayed:execution_ref" in result.errors


def test_missing_output_reference_is_not_a_complete_execution_receipt():
    result = validate(r=receipt(output_refs=[]))
    assert result.status == ReceiptBindingStatus.FAIL
    assert "output_refs_must_be_non_empty_strings" in result.errors


def test_extra_owner_specific_binding_does_not_break_expected_subset_matching():
    enriched = receipt(subject_bindings={
        "candidate_id": "candidate-v2",
        "candidate_change_ref": "sha256:candidate-v2",
        "judge_position": "A",
    })
    result = validate(r=enriched)
    assert result.status == ReceiptBindingStatus.PASS
