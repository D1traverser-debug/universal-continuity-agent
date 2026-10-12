from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping, Sequence


SOP_VERSION = "1.0"
INVESTIGATE_STEP = "INVESTIGATE_EVIDENCE"
CLOSED_STEP = "CLOSED"
PATCH_STEP = "PATCH_MINIMUM_AUTHORITY_SURFACE"
VALIDATION_STEP = "RUN_OR_OBSERVE_VALIDATION"
SYSTEM_REFRAME_STEP = "BUILD_FULL_SYSTEM_IMPACT_MAP"


class TriageDecision(str, Enum):
    NO_DEFECT = "NO_DEFECT"
    INVESTIGATE = "INVESTIGATE"
    CONFIRMED_DEFECT = "CONFIRMED_DEFECT"


@dataclass(frozen=True)
class SOPReceipt:
    step: str
    evidence_refs: tuple[str, ...]
    durable_checkpoint_ref: str | None = None
    outcome: str = "PASS"


@dataclass(frozen=True)
class MaintenanceSOPState:
    run_id: str
    triage_decision: TriageDecision
    current_step: str
    receipts: tuple[SOPReceipt, ...] = ()
    terminal_reason: str | None = None
    repair_cycle: int = 0

    @property
    def terminal(self) -> bool:
        return self.current_step == CLOSED_STEP


def _nonempty_refs(refs: Sequence[str]) -> tuple[str, ...]:
    normalized = tuple(str(item).strip() for item in refs if str(item).strip())
    if not normalized:
        raise ValueError("evidence_refs_required")
    return normalized


def canonical_loop(policy: Mapping[str, Any]) -> tuple[str, ...]:
    raw = policy.get("maintenance_loop")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) and item.strip() for item in raw):
        raise ValueError("maintenance_loop_missing_or_invalid")
    loop = tuple(item.strip() for item in raw)
    if len(set(loop)) != len(loop):
        raise ValueError("maintenance_loop_contains_duplicate_steps")
    for required in ("DETECT", SYSTEM_REFRAME_STEP, PATCH_STEP, VALIDATION_STEP, "REREAD_AUTHORITATIVE_STATE"):
        if required not in loop:
            raise ValueError(f"maintenance_loop_missing_required_step:{required}")
    if loop.index(SYSTEM_REFRAME_STEP) > loop.index(PATCH_STEP):
        raise ValueError("parent_system_outline_must_precede_patch")
    if loop.index(VALIDATION_STEP) < loop.index(PATCH_STEP):
        raise ValueError("validation_must_follow_patch")
    return loop


def start_triage(*, run_id: str, decision: TriageDecision | str, policy: Mapping[str, Any]) -> MaintenanceSOPState:
    if not str(run_id).strip():
        raise ValueError("run_id_required")
    decision = TriageDecision(str(decision))
    if decision is TriageDecision.NO_DEFECT:
        return MaintenanceSOPState(run_id=run_id, triage_decision=decision, current_step=CLOSED_STEP, terminal_reason="NO_DEFECT")
    if decision is TriageDecision.INVESTIGATE:
        return MaintenanceSOPState(run_id=run_id, triage_decision=decision, current_step=INVESTIGATE_STEP)
    return MaintenanceSOPState(run_id=run_id, triage_decision=decision, current_step=canonical_loop(policy)[0])


def resolve_investigation(
    state: MaintenanceSOPState,
    *,
    decision: TriageDecision | str,
    evidence_refs: Sequence[str],
    policy: Mapping[str, Any],
) -> MaintenanceSOPState:
    if state.current_step != INVESTIGATE_STEP or state.terminal:
        raise ValueError("investigation_resolution_requires_investigate_state")
    refs = _nonempty_refs(evidence_refs)
    decision = TriageDecision(str(decision))
    if decision is TriageDecision.INVESTIGATE:
        return replace(
            state,
            receipts=state.receipts + (SOPReceipt(INVESTIGATE_STEP, refs, outcome="MORE_EVIDENCE_REQUIRED"),),
        )
    receipt = SOPReceipt(INVESTIGATE_STEP, refs, outcome=decision.value)
    if decision is TriageDecision.NO_DEFECT:
        return replace(
            state,
            triage_decision=decision,
            current_step=CLOSED_STEP,
            receipts=state.receipts + (receipt,),
            terminal_reason="NO_DEFECT_AFTER_INVESTIGATION",
        )
    return replace(
        state,
        triage_decision=decision,
        current_step=canonical_loop(policy)[0],
        receipts=state.receipts + (receipt,),
    )


def prepatch_checkpoint_ref(state: MaintenanceSOPState) -> str | None:
    for receipt in reversed(state.receipts):
        if receipt.durable_checkpoint_ref:
            return receipt.durable_checkpoint_ref
    return None


def mutation_admitted(state: MaintenanceSOPState, policy: Mapping[str, Any]) -> bool:
    if state.terminal or state.current_step == INVESTIGATE_STEP:
        return False
    loop = canonical_loop(policy)
    if state.current_step not in loop:
        return False
    return loop.index(state.current_step) >= loop.index(PATCH_STEP) and bool(prepatch_checkpoint_ref(state))


def advance(
    state: MaintenanceSOPState,
    *,
    completed_step: str,
    evidence_refs: Sequence[str],
    policy: Mapping[str, Any],
    durable_checkpoint_ref: str | None = None,
) -> MaintenanceSOPState:
    if state.terminal:
        raise ValueError("terminal_sop_cannot_advance")
    if state.current_step == INVESTIGATE_STEP:
        raise ValueError("investigate_state_must_be_resolved_before_systemic_sop")
    loop = canonical_loop(policy)
    if completed_step != state.current_step:
        raise ValueError(f"illegal_sop_transition:expected={state.current_step}:got={completed_step}")
    refs = _nonempty_refs(evidence_refs)
    idx = loop.index(completed_step)
    next_step = CLOSED_STEP if idx == len(loop) - 1 else loop[idx + 1]

    checkpoint = str(durable_checkpoint_ref).strip() if durable_checkpoint_ref else None
    if next_step == PATCH_STEP and not checkpoint:
        raise ValueError("durable_prepatch_checkpoint_required_before_mutation")
    if completed_step == PATCH_STEP and not (checkpoint or prepatch_checkpoint_ref(state)):
        raise ValueError("patch_step_requires_prior_durable_checkpoint")

    receipt = SOPReceipt(completed_step, refs, durable_checkpoint_ref=checkpoint)
    return replace(
        state,
        current_step=next_step,
        receipts=state.receipts + (receipt,),
        terminal_reason="SYSTEMIC_SOP_COMPLETE" if next_step == CLOSED_STEP else None,
    )


def reopen_after_validation_failure(
    state: MaintenanceSOPState,
    *,
    evidence_refs: Sequence[str],
    policy: Mapping[str, Any],
    new_systemic_failure_class: bool = False,
) -> MaintenanceSOPState:
    if state.current_step != VALIDATION_STEP:
        raise ValueError("validation_reopen_requires_validation_step")
    refs = _nonempty_refs(evidence_refs)
    if not prepatch_checkpoint_ref(state):
        raise ValueError("validation_reopen_requires_prior_prepatch_checkpoint")
    target = SYSTEM_REFRAME_STEP if new_systemic_failure_class else PATCH_STEP
    receipt = SOPReceipt(VALIDATION_STEP, refs, outcome="FAIL_REOPEN")
    return replace(
        state,
        current_step=target,
        receipts=state.receipts + (receipt,),
        repair_cycle=state.repair_cycle + 1,
    )


def validate_serialized_trace(trace: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    try:
        decision = TriageDecision(str(trace.get("triage_decision", "")))
    except ValueError:
        return ("sop_trace_invalid_triage_decision",)
    run_id = str(trace.get("run_id", "")).strip()
    if not run_id:
        errors.append("sop_trace_run_id_required")
    receipts = trace.get("receipts")
    if not isinstance(receipts, list):
        return tuple(errors + ["sop_trace_receipts_list_required"])

    if decision is TriageDecision.NO_DEFECT:
        if receipts:
            errors.append("no_defect_trace_must_not_execute_systemic_steps")
        if trace.get("terminal_reason") not in {"NO_DEFECT", "NO_DEFECT_AFTER_INVESTIGATION"}:
            errors.append("no_defect_trace_terminal_reason_required")
        return tuple(errors)

    loop = canonical_loop(policy)
    position = 0
    checkpoint_seen = False
    investigate_open = decision is TriageDecision.INVESTIGATE
    for idx, raw in enumerate(receipts):
        if not isinstance(raw, Mapping):
            errors.append(f"sop_receipt_{idx}_must_be_mapping")
            continue
        step = str(raw.get("step", ""))
        evidence = raw.get("evidence_refs")
        if not isinstance(evidence, list) or not evidence or any(not str(item).strip() for item in evidence):
            errors.append(f"sop_receipt_{idx}_evidence_required")
        if investigate_open:
            if step != INVESTIGATE_STEP:
                errors.append(f"sop_receipt_{idx}_investigation_must_resolve_first")
                investigate_open = False
            else:
                outcome = str(raw.get("outcome", ""))
                if outcome == "MORE_EVIDENCE_REQUIRED":
                    continue
                if outcome == TriageDecision.NO_DEFECT.value:
                    if idx != len(receipts) - 1:
                        errors.append("no_defect_after_investigation_must_terminate")
                    return tuple(errors)
                if outcome != TriageDecision.CONFIRMED_DEFECT.value:
                    errors.append("investigation_resolution_outcome_invalid")
                investigate_open = False
                continue
        if step == VALIDATION_STEP and str(raw.get("outcome", "PASS")) == "FAIL_REOPEN":
            position = loop.index(SYSTEM_REFRAME_STEP if raw.get("new_systemic_failure_class") else PATCH_STEP)
            continue
        if position >= len(loop):
            errors.append(f"sop_receipt_{idx}_extra_step_after_completion")
            continue
        expected = loop[position]
        if step != expected:
            errors.append(f"sop_receipt_{idx}_out_of_order:expected={expected}:got={step}")
            if step in loop:
                position = loop.index(step) + 1
            continue
        checkpoint = str(raw.get("durable_checkpoint_ref", "")).strip()
        next_step = CLOSED_STEP if position == len(loop) - 1 else loop[position + 1]
        if checkpoint:
            checkpoint_seen = True
        if next_step == PATCH_STEP and not checkpoint_seen:
            errors.append("sop_trace_missing_durable_prepatch_checkpoint")
        if step == PATCH_STEP and not checkpoint_seen:
            errors.append("sop_trace_patch_before_prepatch_checkpoint")
        position += 1

    if investigate_open:
        errors.append("sop_trace_investigation_unresolved")
    if trace.get("status") == "CLOSED" and position < len(loop):
        errors.append("sop_trace_closed_before_all_required_steps")
    return tuple(errors)
