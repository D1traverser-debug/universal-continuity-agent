from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping


CONTROLLER_SCHEMA_VERSION = "1.0"
TRIAGE_OUTCOMES = {"NO_DEFECT", "INVESTIGATE", "CONFIRMED_DEFECT"}
STATE_STATUSES = {"ACTIVE", "BLOCKED", "COMPLETE", "NO_DEFECT_CLOSED"}
ACTION_CLASSES = {
    "INSPECT",
    "CHECKPOINT",
    "MATERIAL_PATCH",
    "VALIDATE",
    "PROPAGATE",
    "SECOND_ORDER_REVIEW",
    "CLOSE",
}


@dataclass(frozen=True)
class ControllerEvaluation:
    status: str
    errors: tuple[str, ...]
    next_required_stage: str | None
    material_patch_allowed: bool


def canonical_stages(policy: Mapping[str, Any]) -> tuple[str, ...]:
    outline = policy.get("meta_maintenance_outline", {})
    stages = outline.get("stages") if isinstance(outline, Mapping) else None
    if not isinstance(stages, list) or not stages or any(not isinstance(stage, str) or not stage.strip() for stage in stages):
        raise ValueError("maintenance policy must define a non-empty ordered stage list")
    normalized = tuple(stage.strip() for stage in stages)
    if len(set(normalized)) != len(normalized):
        raise ValueError("maintenance stage list must not contain duplicates")
    return normalized


def _stage_for_prefix(stages: tuple[str, ...], prefix: str) -> str:
    matches = [stage for stage in stages if stage.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one maintenance stage with prefix {prefix!r}")
    return matches[0]


def new_maintenance_state(*, run_id: str, triage_outcome: str, policy: Mapping[str, Any]) -> dict[str, Any]:
    outcome = str(triage_outcome).strip().upper()
    if outcome not in TRIAGE_OUTCOMES:
        raise ValueError("unsupported triage outcome")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id is required")

    stages = canonical_stages(policy)
    if outcome == "NO_DEFECT":
        return {
            "schema_version": CONTROLLER_SCHEMA_VERSION,
            "run_id": run_id.strip(),
            "triage_outcome": outcome,
            "status": "NO_DEFECT_CLOSED",
            "revision": 0,
            "current_stage": None,
            "completed_stage_receipts": [],
            "reopen_history": [],
            "blocker": None,
        }

    return {
        "schema_version": CONTROLLER_SCHEMA_VERSION,
        "run_id": run_id.strip(),
        "triage_outcome": outcome,
        "status": "ACTIVE",
        "revision": 0,
        "current_stage": stages[0],
        "completed_stage_receipts": [],
        "reopen_history": [],
        "blocker": None,
    }


def evaluate_maintenance_state(
    state: Mapping[str, Any] | None,
    policy: Mapping[str, Any],
    *,
    require_complete: bool = False,
) -> ControllerEvaluation:
    errors: list[str] = []
    stages = canonical_stages(policy)
    if not isinstance(state, Mapping):
        return ControllerEvaluation("FAIL", ("controller_state_required",), stages[0], False)

    if state.get("schema_version") != CONTROLLER_SCHEMA_VERSION:
        errors.append("unsupported_controller_schema")
    run_id = state.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        errors.append("controller_run_id_required")

    outcome = str(state.get("triage_outcome", ""))
    if outcome not in TRIAGE_OUTCOMES:
        errors.append("controller_triage_outcome_invalid")
    status = str(state.get("status", ""))
    if status not in STATE_STATUSES:
        errors.append("controller_status_invalid")

    revision = state.get("revision")
    if not isinstance(revision, int) or revision < 0:
        errors.append("controller_revision_invalid")

    receipts = state.get("completed_stage_receipts")
    if not isinstance(receipts, list):
        errors.append("completed_stage_receipts_must_be_list")
        receipts = []

    completed: list[str] = []
    expected_revision = 0
    for index, receipt in enumerate(receipts):
        if not isinstance(receipt, Mapping):
            errors.append(f"stage_receipt_{index}_invalid")
            continue
        stage = receipt.get("stage")
        if not isinstance(stage, str):
            errors.append(f"stage_receipt_{index}_stage_required")
            continue
        completed.append(stage)
        evidence_refs = receipt.get("evidence_refs")
        if not isinstance(evidence_refs, list) or not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
            errors.append(f"stage_receipt_{index}_evidence_required")
        summary = receipt.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            errors.append(f"stage_receipt_{index}_summary_required")
        receipt_revision = receipt.get("revision")
        expected_revision += 1
        if receipt_revision != expected_revision:
            errors.append(f"stage_receipt_{index}_revision_not_contiguous")

    if completed != list(stages[: len(completed)]):
        errors.append("completed_stages_must_be_exact_canonical_prefix")

    next_stage = stages[len(completed)] if len(completed) < len(stages) else None
    current_stage = state.get("current_stage")

    if outcome == "NO_DEFECT":
        if status != "NO_DEFECT_CLOSED":
            errors.append("no_defect_must_close_without_maintenance")
        if receipts:
            errors.append("no_defect_must_not_have_maintenance_stage_receipts")
        if current_stage is not None:
            errors.append("no_defect_must_not_have_current_stage")
        next_stage = None
    else:
        if status == "COMPLETE":
            if len(completed) != len(stages):
                errors.append("complete_requires_all_canonical_stages")
            if current_stage is not None:
                errors.append("complete_requires_null_current_stage")
            next_stage = None
        elif status in {"ACTIVE", "BLOCKED"}:
            if current_stage != next_stage:
                errors.append("current_stage_must_equal_next_unfinished_stage")
        elif status == "NO_DEFECT_CLOSED":
            errors.append("non_no_defect_cannot_use_no_defect_closed")

    reopen_history = state.get("reopen_history")
    if not isinstance(reopen_history, list):
        errors.append("reopen_history_must_be_list")
    else:
        for index, item in enumerate(reopen_history):
            if not isinstance(item, Mapping):
                errors.append(f"reopen_history_{index}_invalid")
                continue
            target = item.get("target_stage")
            if target not in stages:
                errors.append(f"reopen_history_{index}_target_invalid")
            reason = item.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"reopen_history_{index}_reason_required")
            refs = item.get("evidence_refs")
            if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
                errors.append(f"reopen_history_{index}_evidence_required")

    if status == "BLOCKED":
        blocker = state.get("blocker")
        if not isinstance(blocker, Mapping):
            errors.append("blocked_state_requires_blocker")
        else:
            if not isinstance(blocker.get("reason"), str) or not blocker["reason"].strip():
                errors.append("blocked_state_requires_reason")
            refs = blocker.get("evidence_refs")
            if not isinstance(refs, list) or not refs:
                errors.append("blocked_state_requires_evidence")
    elif state.get("blocker") is not None:
        errors.append("nonblocked_state_must_clear_blocker")

    if isinstance(revision, int):
        minimum_revision = len(receipts) + len(reopen_history)
        if revision < minimum_revision:
            errors.append("controller_revision_behind_recorded_transitions")

    if require_complete and status != "COMPLETE":
        errors.append("controller_state_not_complete")

    material_patch_allowed = False
    try:
        implementation_stage = _stage_for_prefix(stages, "M7_")
        material_patch_allowed = (
            status == "ACTIVE"
            and outcome == "CONFIRMED_DEFECT"
            and current_stage == implementation_stage
        )
    except ValueError:
        errors.append("implementation_stage_not_uniquely_defined")

    return ControllerEvaluation(
        status="PASS" if not errors else "FAIL",
        errors=tuple(errors),
        next_required_stage=next_stage,
        material_patch_allowed=material_patch_allowed,
    )


def complete_current_stage(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    stage: str,
    evidence_refs: list[str],
    summary: str,
) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    if state.get("status") != "ACTIVE":
        raise ValueError("only ACTIVE maintenance can complete a stage")
    if stage != state.get("current_stage"):
        raise ValueError("cannot skip or reorder maintenance stages")
    if not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        raise ValueError("stage evidence_refs are required")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("stage summary is required")

    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    updated["completed_stage_receipts"].append(
        {
            "stage": stage,
            "revision": updated["revision"],
            "evidence_refs": list(evidence_refs),
            "summary": summary.strip(),
        }
    )
    stages = canonical_stages(policy)
    completed_count = len(updated["completed_stage_receipts"])
    if completed_count == len(stages):
        updated["status"] = "COMPLETE"
        updated["current_stage"] = None
    else:
        updated["current_stage"] = stages[completed_count]
    return updated


def reopen_stage(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    target_stage: str,
    reason: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    stages = canonical_stages(policy)
    if target_stage not in stages:
        raise ValueError("unknown target stage")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reopen reason is required")
    if not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        raise ValueError("reopen evidence_refs are required")

    target_index = stages.index(target_stage)
    receipts = list(state.get("completed_stage_receipts", []))
    completed_count = len(receipts)
    if target_index > completed_count:
        raise ValueError("cannot reopen to a future stage")

    updated = deepcopy(dict(state))
    updated["completed_stage_receipts"] = receipts[:target_index]
    updated["revision"] = int(updated["revision"]) + 1
    updated.setdefault("reopen_history", []).append(
        {
            "target_stage": target_stage,
            "revision": updated["revision"],
            "reason": reason.strip(),
            "evidence_refs": list(evidence_refs),
        }
    )
    updated["status"] = "ACTIVE"
    updated["current_stage"] = target_stage
    updated["blocker"] = None
    return updated


def block_current_stage(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    reason: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    if state.get("status") != "ACTIVE":
        raise ValueError("only ACTIVE maintenance can be blocked")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("block reason is required")
    if not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        raise ValueError("block evidence_refs are required")

    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    updated["status"] = "BLOCKED"
    updated["blocker"] = {"reason": reason.strip(), "evidence_refs": list(evidence_refs)}
    return updated


def resume_blocked_state(state: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    if state.get("status") != "BLOCKED":
        raise ValueError("state is not BLOCKED")
    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    updated["status"] = "ACTIVE"
    updated["blocker"] = None
    return updated


def resolve_investigation(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    outcome: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    if state.get("triage_outcome") != "INVESTIGATE":
        raise ValueError("only INVESTIGATE may be resolved")
    resolved = str(outcome).strip().upper()
    if resolved not in {"NO_DEFECT", "CONFIRMED_DEFECT"}:
        raise ValueError("investigation must resolve to NO_DEFECT or CONFIRMED_DEFECT")
    if not evidence_refs or any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        raise ValueError("investigation resolution evidence is required")

    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    if resolved == "CONFIRMED_DEFECT":
        updated["triage_outcome"] = resolved
        return updated

    updated["triage_outcome"] = "NO_DEFECT"
    updated["status"] = "NO_DEFECT_CLOSED"
    updated["current_stage"] = None
    updated["completed_stage_receipts"] = []
    updated["blocker"] = None
    return updated


def authorize_action(state: Mapping[str, Any], policy: Mapping[str, Any], action_class: str) -> ControllerEvaluation:
    action = str(action_class).strip().upper()
    if action not in ACTION_CLASSES:
        raise ValueError("unsupported maintenance action class")
    evaluation = evaluate_maintenance_state(state, policy)
    errors = list(evaluation.errors)
    if evaluation.status != "PASS":
        return ControllerEvaluation("FAIL", tuple(errors), evaluation.next_required_stage, False)

    status = state.get("status")
    outcome = state.get("triage_outcome")
    stages = canonical_stages(policy)
    current = state.get("current_stage")

    if action in {"INSPECT", "CHECKPOINT"}:
        allowed = status in {"ACTIVE", "BLOCKED"}
    elif action == "MATERIAL_PATCH":
        allowed = evaluation.material_patch_allowed
    elif action == "VALIDATE":
        allowed = status == "ACTIVE" and outcome == "CONFIRMED_DEFECT" and current == _stage_for_prefix(stages, "M8_")
    elif action == "PROPAGATE":
        allowed = status == "ACTIVE" and outcome == "CONFIRMED_DEFECT" and current == _stage_for_prefix(stages, "M9_")
    elif action == "SECOND_ORDER_REVIEW":
        allowed = status == "ACTIVE" and outcome == "CONFIRMED_DEFECT" and current == _stage_for_prefix(stages, "M10_")
    else:  # CLOSE
        allowed = status == "COMPLETE" and outcome == "CONFIRMED_DEFECT"

    if not allowed:
        errors.append(f"action_not_authorized_at_current_stage:{action}")
    return ControllerEvaluation(
        status="PASS" if not errors else "FAIL",
        errors=tuple(errors),
        next_required_stage=evaluation.next_required_stage,
        material_patch_allowed=evaluation.material_patch_allowed,
    )
