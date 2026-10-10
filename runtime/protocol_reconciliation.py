from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any, Mapping

from runtime.universal_continuity import Compatibility, CompatibilityDecision, TaskMetadata, assert_checkpoint_writer


@dataclass(frozen=True)
class ProtocolReconciliationPlan:
    decision: CompatibilityDecision
    changed: bool
    patch: Mapping[str, Any]
    adaptation_record: Mapping[str, Any] | None = None


def normalize_protocol_version(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    upper = text.upper()
    if upper.startswith("CONTINUITY_V"):
        return upper.removeprefix("CONTINUITY_V").replace("_", ".")
    if upper.startswith("V") and re.fullmatch(r"V\d+(?:[._]\d+)+", upper):
        return upper[1:].replace("_", ".")
    return text


def _legacy_continuity_marker(value: Any) -> str | None:
    """Accept only legacy values that are recognizably Continuity protocol markers.

    Domain contracts such as ``2.1-github`` are not evidence of the persisted
    Continuity protocol and therefore resolve to UNKNOWN rather than INCOMPATIBLE.
    """
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    upper = text.upper()
    if upper.startswith("CONTINUITY_V"):
        return normalize_protocol_version(text)
    if re.fullmatch(r"V?\d+(?:[._]\d+)+", upper):
        return normalize_protocol_version(text)
    return None


def persisted_protocol_version(raw_manifest: Mapping[str, Any]) -> str | None:
    canonical = normalize_protocol_version(raw_manifest.get("continuity_protocol_version"))
    if canonical:
        return canonical
    return _legacy_continuity_marker(raw_manifest.get("contract_version"))


def classify_protocol_compatibility(raw_manifest: Mapping[str, Any], *, current_protocol_version: str, migration_supported_from: set[str] | None = None) -> CompatibilityDecision:
    supported = {normalize_protocol_version(v) for v in (migration_supported_from or set())}
    supported.discard(None)
    old = persisted_protocol_version(raw_manifest)
    new = normalize_protocol_version(current_protocol_version)
    if not old:
        return CompatibilityDecision(Compatibility.UNKNOWN, "persisted Continuity protocol version unavailable")
    if not new:
        return CompatibilityDecision(Compatibility.UNKNOWN, "current Continuity protocol version unavailable")
    if old == new:
        return CompatibilityDecision(Compatibility.COMPATIBLE, f"Continuity protocol already compatible: {old}")
    if old in supported:
        return CompatibilityDecision(Compatibility.MIGRATABLE, f"declared Continuity migration path {old} -> {new}")
    return CompatibilityDecision(Compatibility.INCOMPATIBLE, f"no declared Continuity migration path {old} -> {new}")


def plan_in_place_protocol_reconciliation(raw_manifest: Mapping[str, Any], *, current_protocol_version: str, migration_supported_from: set[str] | None, lease_id: str, resume_epoch: int, applied_by: str, now: datetime | None = None) -> ProtocolReconciliationPlan:
    decision = classify_protocol_compatibility(raw_manifest, current_protocol_version=current_protocol_version, migration_supported_from=migration_supported_from)
    if decision.result in {Compatibility.UNKNOWN, Compatibility.INCOMPATIBLE}:
        return ProtocolReconciliationPlan(decision=decision, changed=False, patch={})
    current = normalize_protocol_version(current_protocol_version)
    old = persisted_protocol_version(raw_manifest)
    canonical = normalize_protocol_version(raw_manifest.get("continuity_protocol_version"))
    if decision.result == Compatibility.COMPATIBLE and canonical == current:
        return ProtocolReconciliationPlan(decision=decision, changed=False, patch={})
    task = TaskMetadata.from_mapping(raw_manifest)
    assert_checkpoint_writer(task, lease_id=lease_id, resume_epoch=resume_epoch)
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    reconciled_at = now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    classification = decision.result.value
    strategy = "CANONICAL_PROTOCOL_STAMP" if old == current else "ADDITIVE_PROTOCOL_OVERLAY"
    record = {
        "from_protocol": old, "to_protocol": current, "classification": classification,
        "strategy": strategy, "business_state_rewritten": False, "lease_changed": False,
        "applied_by": applied_by, "reconciled_at": reconciled_at,
    }
    patch = {
        "continuity_protocol_version": current, "last_protocol_reconciled_at": reconciled_at,
        "protocol_migration": record, "manifest_version": int(raw_manifest.get("manifest_version", 1)) + 1,
        "updated_at": reconciled_at,
    }
    return ProtocolReconciliationPlan(decision=decision, changed=True, patch=patch, adaptation_record=record)


def apply_protocol_patch(raw_manifest: Mapping[str, Any], plan: ProtocolReconciliationPlan) -> dict[str, Any]:
    if not plan.changed:
        return dict(raw_manifest)
    forbidden = {"task_id","current_stage","next_action","status","resume_epoch","active_lease","checkpoint_ref","artifact_refs"}
    overlap = forbidden.intersection(plan.patch)
    if overlap:
        raise ValueError(f"protocol reconciliation attempted business/lease mutation: {sorted(overlap)}")
    merged = dict(raw_manifest)
    merged.update(plan.patch)
    return merged
