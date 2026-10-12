import json
from pathlib import Path

import pytest

from runtime.maintenance_sop import (
    CLOSED_STEP,
    INVESTIGATE_STEP,
    PATCH_STEP,
    SYSTEM_REFRAME_STEP,
    TriageDecision,
    advance,
    canonical_loop,
    mutation_admitted,
    reopen_after_validation_failure,
    resolve_investigation,
    start_triage,
    validate_serialized_trace,
)


ROOT = Path(__file__).resolve().parents[1]


def policy():
    return json.loads((ROOT / "SYSTEM_MAINTENANCE_POLICY.json").read_text(encoding="utf-8"))


def walk_to_prepatch_checkpoint(run_id="sop-test"):
    state = start_triage(run_id=run_id, decision="CONFIRMED_DEFECT", policy=policy())
    loop = canonical_loop(policy())
    patch_idx = loop.index(PATCH_STEP)
    for idx, step in enumerate(loop[:patch_idx]):
        next_step = loop[idx + 1]
        checkpoint = "audit://prepatch" if next_step == PATCH_STEP else None
        state = advance(
            state,
            completed_step=step,
            evidence_refs=[f"evidence://{step.lower()}"],
            policy=policy(),
            durable_checkpoint_ref=checkpoint,
        )
    return state


def test_no_defect_stays_off_maintenance_path():
    state = start_triage(run_id="no-defect", decision="NO_DEFECT", policy=policy())
    assert state.terminal is True
    assert state.current_step == CLOSED_STEP
    assert mutation_admitted(state, policy()) is False


def test_investigate_requires_evidence_before_confirmed_defect_path():
    state = start_triage(run_id="investigate", decision="INVESTIGATE", policy=policy())
    assert state.current_step == INVESTIGATE_STEP
    assert mutation_admitted(state, policy()) is False

    with pytest.raises(ValueError, match="investigate_state_must_be_resolved"):
        advance(
            state,
            completed_step="DETECT",
            evidence_refs=["evidence://guess"],
            policy=policy(),
        )

    state = resolve_investigation(
        state,
        decision="CONFIRMED_DEFECT",
        evidence_refs=["evidence://authority-reread"],
        policy=policy(),
    )
    assert state.current_step == canonical_loop(policy())[0]


def test_investigation_can_close_as_no_defect_without_running_maintenance():
    state = start_triage(run_id="investigate-no-defect", decision="INVESTIGATE", policy=policy())
    state = resolve_investigation(
        state,
        decision="NO_DEFECT",
        evidence_refs=["evidence://falsified-hypothesis"],
        policy=policy(),
    )
    assert state.terminal is True
    assert state.terminal_reason == "NO_DEFECT_AFTER_INVESTIGATION"
    assert mutation_admitted(state, policy()) is False


def test_confirmed_defect_cannot_skip_parent_loop_steps():
    state = start_triage(run_id="skip", decision="CONFIRMED_DEFECT", policy=policy())
    assert state.current_step == "DETECT"
    with pytest.raises(ValueError, match="illegal_sop_transition"):
        advance(
            state,
            completed_step=PATCH_STEP,
            evidence_refs=["evidence://patch"],
            policy=policy(),
        )


def test_patch_is_not_admitted_until_all_prepatch_steps_and_durable_checkpoint_exist():
    state = start_triage(run_id="prepatch", decision="CONFIRMED_DEFECT", policy=policy())
    loop = canonical_loop(policy())
    patch_idx = loop.index(PATCH_STEP)

    for idx, step in enumerate(loop[:patch_idx]):
        next_step = loop[idx + 1]
        if next_step == PATCH_STEP:
            with pytest.raises(ValueError, match="durable_prepatch_checkpoint_required"):
                advance(
                    state,
                    completed_step=step,
                    evidence_refs=[f"evidence://{step.lower()}"],
                    policy=policy(),
                )
            state = advance(
                state,
                completed_step=step,
                evidence_refs=[f"evidence://{step.lower()}"],
                policy=policy(),
                durable_checkpoint_ref="audit://prepatch",
            )
        else:
            state = advance(
                state,
                completed_step=step,
                evidence_refs=[f"evidence://{step.lower()}"],
                policy=policy(),
            )

    assert state.current_step == PATCH_STEP
    assert mutation_admitted(state, policy()) is True


def test_validation_failure_reopens_implementation_not_fake_closure():
    state = walk_to_prepatch_checkpoint("validation-loop")
    loop = canonical_loop(policy())
    start = loop.index(PATCH_STEP)
    stop = loop.index("RUN_OR_OBSERVE_VALIDATION")
    for step in loop[start:stop]:
        state = advance(
            state,
            completed_step=step,
            evidence_refs=[f"evidence://{step.lower()}"],
            policy=policy(),
        )

    assert state.current_step == "RUN_OR_OBSERVE_VALIDATION"
    reopened = reopen_after_validation_failure(
        state,
        evidence_refs=["ci://failed-run"],
        policy=policy(),
        new_systemic_failure_class=False,
    )
    assert reopened.current_step == PATCH_STEP
    assert reopened.repair_cycle == 1
    assert reopened.terminal is False


def test_validation_failure_with_new_systemic_class_returns_to_parent_outline():
    state = walk_to_prepatch_checkpoint("validation-systemic-loop")
    loop = canonical_loop(policy())
    start = loop.index(PATCH_STEP)
    stop = loop.index("RUN_OR_OBSERVE_VALIDATION")
    for step in loop[start:stop]:
        state = advance(
            state,
            completed_step=step,
            evidence_refs=[f"evidence://{step.lower()}"],
            policy=policy(),
        )
    reopened = reopen_after_validation_failure(
        state,
        evidence_refs=["ci://new-systemic-failure"],
        policy=policy(),
        new_systemic_failure_class=True,
    )
    assert reopened.current_step == SYSTEM_REFRAME_STEP


def test_serialized_trace_rejects_patch_without_prepatch_checkpoint():
    loop = canonical_loop(policy())
    receipts = []
    for step in loop:
        receipts.append({"step": step, "evidence_refs": [f"evidence://{step.lower()}"]})
    trace = {
        "run_id": "serialized-bad",
        "triage_decision": "CONFIRMED_DEFECT",
        "status": "CLOSED",
        "receipts": receipts,
        "terminal_reason": "SYSTEMIC_SOP_COMPLETE",
    }
    errors = validate_serialized_trace(trace, policy())
    assert "sop_trace_missing_durable_prepatch_checkpoint" in errors
    assert "sop_trace_patch_before_prepatch_checkpoint" in errors


def test_serialized_trace_accepts_complete_ordered_systemic_run():
    loop = canonical_loop(policy())
    receipts = []
    patch_idx = loop.index(PATCH_STEP)
    for idx, step in enumerate(loop):
        item = {"step": step, "evidence_refs": [f"evidence://{step.lower()}"]}
        if idx == patch_idx - 1:
            item["durable_checkpoint_ref"] = "git://prepatch-checkpoint"
        receipts.append(item)
    trace = {
        "run_id": "serialized-good",
        "triage_decision": "CONFIRMED_DEFECT",
        "status": "CLOSED",
        "receipts": receipts,
        "terminal_reason": "SYSTEMIC_SOP_COMPLETE",
    }
    assert validate_serialized_trace(trace, policy()) == ()
