from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping


CONTROLLER_SCHEMA_VERSION = "1.0"
TRIAGE_OUTCOMES = {"NO_DEFECT", "INVESTIGATE", "CONFIRMED_DEFECT"}
STATE_STATUSES = {"ACTIVE", "BLOCKED", "COMPLETE", "NO_DEFECT_CLOSED"}
INVESTIGATION_STAGE = "INVESTIGATE_EVIDENCE"
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


def _valid_refs(refs: Any) -> bool:
    return isinstance(refs, list) and bool(refs) and all(isinstance(ref, str) and bool(ref.strip()) for ref in refs)


def _strictly_increasing(values: list[int]) -> bool:
    return all(left < right for left, right in zip(values, values[1:]))


def new_maintenance_state(*, run_id: str, triage_outcome: str, policy: Mapping[str, Any]) -> dict[str, Any]:
    outcome = str(triage_outcome).strip().upper()
    if outcome not in TRIAGE_OUTCOMES:
        raise ValueError("unsupported triage outcome")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id is required")

    stages = canonical_stages(policy)
    common = {
        "schema_version": CONTROLLER_SCHEMA_VERSION,
        "run_id": run_id.strip(),
        "triage_outcome": outcome,
        "revision": 0,
        "completed_stage_receipts": [],
        "reopen_history": [],
        "investigation_resolution": None,
        "prepatch_checkpoint": None,
        "blocker": None,
    }
    if outcome == "NO_DEFECT":
        return {**common, "status": "NO_DEFECT_CLOSED", "current_stage": None}
    if outcome == "INVESTIGATE":
        return {**common, "status": "ACTIVE", "current_stage": INVESTIGATION_STAGE}
    return {**common, "status": "ACTIVE", "current_stage": stages[0]}


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
        revision = -1

    receipts = state.get("completed_stage_receipts")
    if not isinstance(receipts, list):
        errors.append("completed_stage_receipts_must_be_list")
        receipts = []

    completed: list[str] = []
    receipt_revisions: list[int] = []
    for index, receipt in enumerate(receipts):
        if not isinstance(receipt, Mapping):
            errors.append(f"stage_receipt_{index}_invalid")
            continue
        stage = receipt.get("stage")
        if not isinstance(stage, str):
            errors.append(f"stage_receipt_{index}_stage_required")
            continue
        completed.append(stage)
        if not _valid_refs(receipt.get("evidence_refs")):
            errors.append(f"stage_receipt_{index}_evidence_required")
        summary = receipt.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            errors.append(f"stage_receipt_{index}_summary_required")
        receipt_revision = receipt.get("revision")
        if not isinstance(receipt_revision, int) or receipt_revision <= 0:
            errors.append(f"stage_receipt_{index}_revision_invalid")
        else:
            receipt_revisions.append(receipt_revision)
    if receipt_revisions and not _strictly_increasing(receipt_revisions):
        errors.append("stage_receipt_revisions_must_be_strictly_increasing")

    if completed != list(stages[: len(completed)]):
        errors.append("completed_stages_must_be_exact_canonical_prefix")

    reopen_history = state.get("reopen_history")
    reopen_revisions: list[int] = []
    if not isinstance(reopen_history, list):
        errors.append("reopen_history_must_be_list")
        reopen_history = []
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
            if not _valid_refs(item.get("evidence_refs")):
                errors.append(f"reopen_history_{index}_evidence_required")
            item_revision = item.get("revision")
            if not isinstance(item_revision, int) or item_revision <= 0:
                errors.append(f"reopen_history_{index}_revision_invalid")
            else:
                reopen_revisions.append(item_revision)
    if reopen_revisions and not _strictly_increasing(reopen_revisions):
        errors.append("reopen_revisions_must_be_strictly_increasing")

    auxiliary_revisions: list[int] = []
    investigation_resolution = state.get("investigation_resolution")
    if investigation_resolution is not None:
        if not isinstance(investigation_resolution, Mapping):
            errors.append("investigation_resolution_invalid")
        else:
            if not _valid_refs(investigation_resolution.get("evidence_refs")):
                errors.append("investigation_resolution_evidence_required")
            inv_revision = investigation_resolution.get("revision")
            if not isinstance(inv_revision, int) or inv_revision <= 0:
                errors.append("investigation_resolution_revision_invalid")
            else:
                auxiliary_revisions.append(inv_revision)

    checkpoint = state.get("prepatch_checkpoint")
    if checkpoint is not None:
        if not isinstance(checkpoint, Mapping):
            errors.append("prepatch_checkpoint_invalid")
        else:
            ref = checkpoint.get("ref")
            if not isinstance(ref, str) or not ref.strip():
                errors.append("prepatch_checkpoint_ref_required")
            if checkpoint.get("authoritative_reread_verified") is not True:
                errors.append("prepatch_checkpoint_requires_authoritative_reread")
            checkpoint_revision = checkpoint.get("revision")
            if not isinstance(checkpoint_revision, int) or checkpoint_revision <= 0:
                errors.append("prepatch_checkpoint_revision_invalid")
            else:
                auxiliary_revisions.append(checkpoint_revision)
            try:
                implementation_index = stages.index(_stage_for_prefix(stages, "M7_"))
            except ValueError:
                implementation_index = -1
                errors.append("implementation_stage_not_uniquely_defined")
            if checkpoint.get("bound_completed_stage_count") != implementation_index:
                errors.append("prepatch_checkpoint_not_bound_to_preimplementation_prefix")

    all_event_revisions = receipt_revisions + reopen_revisions + auxiliary_revisions
    if len(all_event_revisions) != len(set(all_event_revisions)):
        errors.append("controller_event_revisions_must_be_unique")
    if all_event_revisions and isinstance(revision, int) and max(all_event_revisions) > revision:
        errors.append("controller_revision_behind_recorded_events")

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
    elif outcome == "INVESTIGATE":
        if status not in {"ACTIVE", "BLOCKED"}:
            errors.append("investigate_must_be_active_or_blocked")
        if receipts:
            errors.append("investigate_must_not_complete_systemic_stages")
        if current_stage != INVESTIGATION_STAGE:
            errors.append("investigate_current_stage_invalid")
        if checkpoint is not None:
            errors.append("investigate_must_not_have_prepatch_checkpoint")
        next_stage = INVESTIGATION_STAGE
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
            errors.append("confirmed_defect_cannot_use_no_defect_closed")

    if status == "BLOCKED":
        blocker = state.get("blocker")
        if not isinstance(blocker, Mapping):
            errors.append("blocked_state_requires_blocker")
        else:
            if not isinstance(blocker.get("reason"), str) or not blocker["reason"].strip():
                errors.append("blocked_state_requires_reason")
            if not _valid_refs(blocker.get("evidence_refs")):
                errors.append("blocked_state_requires_evidence")
    elif state.get("blocker") is not None:
        errors.append("nonblocked_state_must_clear_blocker")

    if require_complete and status != "COMPLETE":
        errors.append("controller_state_not_complete")

    material_patch_allowed = False
    try:
        implementation_stage = _stage_for_prefix(stages, "M7_")
        material_patch_allowed = (
            status == "ACTIVE"
            and outcome == "CONFIRMED_DEFECT"
            and current_stage == implementation_stage
            and isinstance(checkpoint, Mapping)
            and checkpoint.get("authoritative_reread_verified") is True
            and bool(str(checkpoint.get("ref", "")).strip())
        )
        implementation_index = stages.index(implementation_stage)
        if outcome == "CONFIRMED_DEFECT" and len(completed) > implementation_index and checkpoint is None:
            errors.append("implementation_receipt_requires_prepatch_checkpoint")
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
    if state.get("triage_outcome") != "CONFIRMED_DEFECT":
        raise ValueError("systemic stages require CONFIRMED_DEFECT")
    if stage != state.get("current_stage"):
        raise ValueError("cannot skip or reorder maintenance stages")
    if not _valid_refs(evidence_refs):
        raise ValueError("stage evidence_refs are required")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("stage summary is required")

    stages = canonical_stages(policy)
    implementation_stage = _stage_for_prefix(stages, "M7_")
    if stage == implementation_stage and not evaluation.material_patch_allowed:
        raise ValueError("implementation_stage_requires_verified_prepatch_checkpoint")

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
    completed_count = len(updated["completed_stage_receipts"])
    if completed_count == len(stages):
        updated["status"] = "COMPLETE"
        updated["current_stage"] = None
    else:
        updated["current_stage"] = stages[completed_count]
    return updated


def record_prepatch_checkpoint(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    checkpoint_ref: str,
    authoritative_reread_verified: bool,
) -> dict[str, Any]:
    evaluation = evaluate_maintenance_state(state, policy)
    if evaluation.status != "PASS":
        raise ValueError("invalid controller state: " + ",".join(evaluation.errors))
    stages = canonical_stages(policy)
    implementation_stage = _stage_for_prefix(stages, "M7_")
    implementation_index = stages.index(implementation_stage)
    if state.get("status") != "ACTIVE" or state.get("triage_outcome") != "CONFIRMED_DEFECT":
        raise ValueError("prepatch checkpoint requires active confirmed defect")
    if state.get("current_stage") != implementation_stage:
        raise ValueError("prepatch checkpoint is only valid at implementation admission")
    if len(state.get("completed_stage_receipts", [])) != implementation_index:
        raise ValueError("prepatch checkpoint requires complete preimplementation prefix")
    if not isinstance(checkpoint_ref, str) or not checkpoint_ref.strip():
        raise ValueError("prepatch checkpoint_ref is required")
    if authoritative_reread_verified is not True:
        raise ValueError("prepatch checkpoint requires authoritative reread")

    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    updated["prepatch_checkpoint"] = {
        "ref": checkpoint_ref.strip(),
        "revision": updated["revision"],
        "bound_completed_stage_count": implementation_index,
        "authoritative_reread_verified": True,
    }
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
    if not _valid_refs(evidence_refs):
        raise ValueError("reopen evidence_refs are required")

    target_index = stages.index(target_stage)
    receipts = list(state.get("completed_stage_receipts", []))
    completed_count = len(receipts)
    if target_index > completed_count:
        raise ValueError("cannot reopen to a future stage")

    implementation_index = stages.index(_stage_for_prefix(stages, "M7_"))
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
    if target_index < implementation_index:
        updated["prepatch_checkpoint"] = None
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
    if not _valid_refs(evidence_refs):
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
    if state.get("triage_outcome") != "INVESTIGATE" or state.get("current_stage") != INVESTIGATION_STAGE:
        raise ValueError("only active INVESTIGATE may be resolved")
    resolved = str(outcome).strip().upper()
    if resolved not in {"NO_DEFECT", "CONFIRMED_DEFECT"}:
        raise ValueError("investigation must resolve to NO_DEFECT or CONFIRMED_DEFECT")
    if not _valid_refs(evidence_refs):
        raise ValueError("investigation resolution evidence is required")

    updated = deepcopy(dict(state))
    updated["revision"] = int(updated["revision"]) + 1
    updated["investigation_resolution"] = {
        "outcome": resolved,
        "revision": updated["revision"],
        "evidence_refs": list(evidence_refs),
    }
    if resolved == "CONFIRMED_DEFECT":
        updated["triage_outcome"] = resolved
        updated["current_stage"] = canonical_stages(policy)[0]
        return updated

    updated["triage_outcome"] = "NO_DEFECT"
    updated["status"] = "NO_DEFECT_CLOSED"
    updated["current_stage"] = None
    updated["completed_stage_receipts"] = []
    updated["prepatch_checkpoint"] = None
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
    else:
        allowed = status == "COMPLETE" and outcome == "CONFIRMED_DEFECT"

    if not allowed:
        errors.append(f"action_not_authorized_at_current_stage:{action}")
    return ControllerEvaluation(
        status="PASS" if not errors else "FAIL",
        errors=tuple(errors),
        next_required_stage=evaluation.next_required_stage,
        material_patch_allowed=evaluation.material_patch_allowed,
    )
