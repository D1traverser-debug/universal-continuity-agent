from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Protocol, Sequence
from uuid import uuid4

SCHEMA_VERSION = "3.7"


class TaskClass(str, Enum):
    USER = "USER"
    SYSTEM_INFRA = "SYSTEM_INFRA"
    TEST = "TEST"
    FIXTURE = "FIXTURE"
    EVAL = "EVAL"
    MIGRATION = "MIGRATION"


class ResumeVisibility(str, Enum):
    DEFAULT = "DEFAULT"
    EXPLICIT_ONLY = "EXPLICIT_ONLY"
    HIDDEN = "HIDDEN"


class TaskStatus(str, Enum):
    ACTIVE = "ACTIVE"
    WAITING = "WAITING"
    BLOCKED = "BLOCKED"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    ABANDONED = "ABANDONED"
    ARCHIVED = "ARCHIVED"


class Compatibility(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    MIGRATABLE = "MIGRATABLE"
    INCOMPATIBLE = "INCOMPATIBLE"
    UNKNOWN = "UNKNOWN"


class CommitStatus(str, Enum):
    COMMITTED = "COMMITTED"
    NO_MATERIAL_CHANGE = "NO_MATERIAL_CHANGE"
    COMMIT_FAILED = "COMMIT_FAILED"
    STALE_WRITER = "STALE_WRITER"
    NOT_APPLICABLE = "NOT_APPLICABLE"


DEFAULT_STATUSES = {TaskStatus.ACTIVE, TaskStatus.WAITING, TaskStatus.BLOCKED}
NON_USER_CLASSES = {TaskClass.SYSTEM_INFRA, TaskClass.TEST, TaskClass.FIXTURE, TaskClass.EVAL, TaskClass.MIGRATION}


def _strict_bool(raw: Mapping[str, Any], field_name: str, default: bool) -> bool:
    if field_name not in raw:
        return default
    value = raw.get(field_name)
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be boolean")
    return value


@dataclass(frozen=True)
class ResumeLease:
    lease_id: str
    resume_epoch: int
    acquired_at: datetime
    supersedes_lease_id: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None, *, fallback_resume_epoch: int = 0) -> "ResumeLease | None":
        if not raw:
            return None
        acquired = raw.get("acquired_at")
        if isinstance(acquired, str):
            acquired = datetime.fromisoformat(acquired.replace("Z", "+00:00"))
        if acquired is None:
            acquired = datetime.now(timezone.utc)
        if acquired.tzinfo is None:
            acquired = acquired.replace(tzinfo=timezone.utc)
        return cls(
            lease_id=str(raw["lease_id"]),
            resume_epoch=int(raw.get("resume_epoch", fallback_resume_epoch)),
            acquired_at=acquired,
            supersedes_lease_id=raw.get("supersedes_lease_id"),
        )


@dataclass(frozen=True)
class TaskMetadata:
    task_id: str
    domain: str
    title: str
    recovery_owner: str
    status: TaskStatus
    display_name_zh: str | None = None
    task_class: TaskClass = TaskClass.MIGRATION
    resume_eligible: bool = False
    resume_visibility: ResumeVisibility = ResumeVisibility.EXPLICIT_ONLY
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    current_stage: str | None = None
    next_action: str | None = None
    checkpoint_ref: str | None = None
    contract_version: str | None = None
    skill_version: str | None = None
    runtime_version: str | None = None
    keywords: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    manifest_ref: str | None = None
    manifest_version: int = 1
    resume_epoch: int = 0
    active_lease: ResumeLease | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "TaskMetadata":
        missing = [k for k in ("task_id", "domain", "title", "recovery_owner", "status") if not raw.get(k)]
        if missing:
            raise ValueError(f"missing required task metadata: {missing}")
        dt = raw.get("updated_at")
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        if dt is None:
            dt = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        display_name_zh = raw.get("display_name_zh")
        if display_name_zh is not None:
            display_name_zh = " ".join(str(display_name_zh).split()) or None
        resume_epoch = int(raw.get("resume_epoch", 0))
        return cls(
            task_id=str(raw["task_id"]), domain=str(raw["domain"]), title=str(raw["title"]),
            recovery_owner=str(raw["recovery_owner"]), status=TaskStatus(str(raw["status"])),
            display_name_zh=display_name_zh,
            task_class=TaskClass(str(raw.get("task_class", TaskClass.MIGRATION.value))),
            resume_eligible=_strict_bool(raw, "resume_eligible", False),
            resume_visibility=ResumeVisibility(str(raw.get("resume_visibility", ResumeVisibility.EXPLICIT_ONLY.value))),
            updated_at=dt, current_stage=raw.get("current_stage"), next_action=raw.get("next_action"),
            checkpoint_ref=raw.get("checkpoint_ref"), contract_version=raw.get("contract_version"),
            skill_version=raw.get("skill_version"), runtime_version=raw.get("runtime_version"),
            keywords=tuple(str(x) for x in raw.get("keywords", ()) if str(x).strip()),
            artifact_refs=tuple(str(x) for x in raw.get("artifact_refs", ()) if str(x).strip()),
            manifest_ref=raw.get("manifest_ref"), manifest_version=int(raw.get("manifest_version", 1)),
            resume_epoch=resume_epoch,
            active_lease=ResumeLease.from_mapping(raw.get("active_lease"), fallback_resume_epoch=resume_epoch),
        )


@dataclass(frozen=True)
class RecoveryCandidate:
    task: TaskMetadata
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class CompatibilityDecision:
    result: Compatibility
    reason: str
    reusable_refs: tuple[str, ...] = ()
    invalidated_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResumeProgressReceipt:
    task_id: str
    display_name: str
    persisted_at: datetime
    status: TaskStatus
    current_stage: str | None
    next_action: str | None
    blockers_or_waiting_state: tuple[str, ...]
    checkpoint_ref: str | None
    manifest_version: int
    resume_epoch_before_takeover: int


@dataclass(frozen=True)
class TurnCommitReceipt:
    commit_status: CommitStatus
    task_id: str | None
    current_persisted_stage: str | None
    current_persisted_next_action: str | None
    checkpoint_ref: str | None
    manifest_version: int | None
    resume_epoch: int | None
    verified_after_write: bool
    detail: str = ""


class OwnerAdapter(Protocol):
    owner_name: str
    def list_resumable_tasks(self) -> Sequence[Mapping[str, Any]]: ...
    def get_task_checkpoint(self, task_id: str) -> Mapping[str, Any]: ...
    def compatibility_check(self, task: TaskMetadata, current_contract: Mapping[str, Any]) -> CompatibilityDecision: ...


def bare_inherit_eligible(task: TaskMetadata) -> bool:
    return task.task_class == TaskClass.USER and task.resume_eligible and task.resume_visibility == ResumeVisibility.DEFAULT and task.status in DEFAULT_STATUSES


def explicit_eligible(task: TaskMetadata) -> bool:
    """Eligible for immediate writer takeover, not merely selectable for inspection/reopen."""
    return task.resume_eligible and task.status in DEFAULT_STATUSES and task.resume_visibility != ResumeVisibility.HIDDEN


def needs_display_name_zh(task: TaskMetadata) -> bool:
    return task.task_class == TaskClass.USER and not bool(task.display_name_zh)


def candidate_display_name(task: TaskMetadata) -> str:
    return task.display_name_zh or task.title


def assign_display_name_zh(task: TaskMetadata, display_name_zh: str, *, now: datetime | None = None) -> TaskMetadata:
    name = " ".join(str(display_name_zh).split())
    if not name:
        raise ValueError("display_name_zh must not be blank")
    if len(name) > 80:
        raise ValueError("display_name_zh must be 80 characters or fewer")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return replace(task, display_name_zh=name, manifest_version=task.manifest_version + 1, updated_at=now)


def validate_owner_adapter_payload(rows: Iterable[Mapping[str, Any]]) -> list[TaskMetadata]:
    tasks: list[TaskMetadata] = []
    seen: set[str] = set()
    for row in rows:
        task = TaskMetadata.from_mapping(row)
        if task.task_id in seen:
            raise ValueError(f"duplicate task_id from owner adapter: {task.task_id}")
        seen.add(task.task_id)
        tasks.append(task)
    return tasks


def merge_owner_discovery_payloads(payloads: Mapping[str, Iterable[Mapping[str, Any]]]) -> list[TaskMetadata]:
    """Merge complete owner discovery payloads and fail on cross-owner task identity collision."""
    merged: list[TaskMetadata] = []
    identities: dict[str, str] = {}
    for source_owner, rows in payloads.items():
        for task in validate_owner_adapter_payload(rows):
            previous = identities.get(task.task_id)
            if previous is not None and previous != source_owner:
                raise ValueError(f"cross_owner_task_id_collision:{task.task_id}:{previous}:{source_owner}")
            identities[task.task_id] = source_owner
            merged.append(task)
    return merged


def _tokens(text: str) -> set[str]:
    normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {token for token in normalized.split() if token}


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _score_hint(task: TaskMetadata, hint: str | None, owner_hint: str | None, domain_hint: str | None, now: datetime) -> RecoveryCandidate:
    score = 0.0
    reasons: list[str] = []
    if owner_hint and task.recovery_owner == owner_hint:
        score += 5.0; reasons.append("owner")
    if domain_hint and task.domain == domain_hint:
        score += 4.0; reasons.append("domain")
    if hint:
        h = hint.strip().lower()
        labels = [str(x).strip().lower() for x in (task.display_name_zh, task.title) if x and str(x).strip()]
        display_text = " ".join(labels)
        if h and any(h in label or label in h for label in labels):
            score += 8.0; reasons.append("title-substring")
        if _contains_cjk(h):
            for kw in task.keywords:
                if kw and kw.lower() in h:
                    score += 3.0; reasons.append(f"keyword:{kw}")
            if task.domain.lower() in h:
                score += 2.0; reasons.append("domain-text")
        else:
            label_tokens = _tokens(display_text)
            keyword_tokens = set().union(*(_tokens(k) for k in task.keywords)) if task.keywords else set()
            overlap = _tokens(h) & (label_tokens | keyword_tokens)
            if overlap:
                score += min(5.0, float(len(overlap) * 2)); reasons.append("token-overlap")
    age_hours = max(0.0, (now - task.updated_at.astimezone(timezone.utc)).total_seconds() / 3600.0)
    recency_bonus = max(0.0, 3.0 - min(3.0, age_hours / 24.0))
    score += recency_bonus
    if recency_bonus: reasons.append("recency")
    if task.status == TaskStatus.BLOCKED: score -= 0.25
    return RecoveryCandidate(task=task, score=score, reasons=tuple(reasons))


def resolve_candidates(tasks: Iterable[TaskMetadata], *, hint: str | None = None, owner_hint: str | None = None, domain_hint: str | None = None, explicit: bool = False, max_results: int | None = None, now: datetime | None = None) -> list[RecoveryCandidate]:
    now = now or datetime.now(timezone.utc)
    eligible = [t for t in tasks if (explicit_eligible(t) if explicit else bare_inherit_eligible(t))]
    scored = [_score_hint(t, hint, owner_hint, domain_hint, now) for t in eligible]
    scored.sort(key=lambda c: (c.score, c.task.updated_at, c.task.task_id), reverse=True)
    if max_results is None:
        return scored
    if max_results < 1:
        raise ValueError("max_results must be >= 1 when provided")
    return scored[:max_results]


def should_autoresume(candidates: Sequence[RecoveryCandidate], *, hint_present: bool, discovery_complete: bool) -> bool:
    if not discovery_complete or len(candidates) != 1:
        return False
    only = candidates[0]
    if not hint_present:
        return True
    semantic_reasons = {"owner", "domain", "title-substring", "token-overlap", "domain-text"}
    return bool(semantic_reasons.intersection(only.reasons) or any(r.startswith("keyword:") for r in only.reasons))


def classify_version_compatibility(task: TaskMetadata, *, current_contract_version: str | None, migration_supported_from: set[str] | None = None) -> CompatibilityDecision:
    migration_supported_from = migration_supported_from or set()
    old = task.contract_version; new = current_contract_version
    if not old or old == "legacy-unclassified":
        return CompatibilityDecision(Compatibility.MIGRATABLE if "legacy-unclassified" in migration_supported_from else Compatibility.UNKNOWN, "persisted task has no classified contract version")
    if not new: return CompatibilityDecision(Compatibility.UNKNOWN, "current owner contract version unavailable")
    if old == new: return CompatibilityDecision(Compatibility.COMPATIBLE, f"contract versions match: {old}")
    if old in migration_supported_from: return CompatibilityDecision(Compatibility.MIGRATABLE, f"owner declares migration path {old} -> {new}")
    return CompatibilityDecision(Compatibility.INCOMPATIBLE, f"no declared migration path {old} -> {new}")


def acquire_resume_lease(task: TaskMetadata, *, lease_id: str | None = None, now: datetime | None = None) -> TaskMetadata:
    if task.task_class == TaskClass.SYSTEM_INFRA:
        if task.resume_visibility != ResumeVisibility.EXPLICIT_ONLY or not task.resume_eligible:
            raise ValueError("SYSTEM_INFRA takeover requires resume_eligible + EXPLICIT_ONLY")
    elif task.task_class != TaskClass.USER:
        raise ValueError("only USER or explicit SYSTEM_INFRA tasks may acquire a resume lease")
    if not explicit_eligible(task):
        raise ValueError(f"task status is not directly resumable: {task.status.value}; paused/terminal tasks require owner-authoritative reactivation")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None: now = now.replace(tzinfo=timezone.utc)
    previous = task.active_lease.lease_id if task.active_lease else None
    next_epoch = max(task.resume_epoch, task.active_lease.resume_epoch if task.active_lease else 0) + 1
    lease = ResumeLease(lease_id=lease_id or str(uuid4()), resume_epoch=next_epoch, acquired_at=now, supersedes_lease_id=previous)
    return replace(task, resume_epoch=next_epoch, active_lease=lease, manifest_version=task.manifest_version + 1, updated_at=now)


def verify_resume_lease(task: TaskMetadata, lease_id: str, *, resume_epoch: int | None = None) -> bool:
    lease = task.active_lease
    if lease is None or lease.lease_id != lease_id: return False
    if resume_epoch is not None and lease.resume_epoch != resume_epoch: return False
    return lease.resume_epoch == task.resume_epoch


def assert_checkpoint_writer(task: TaskMetadata, *, lease_id: str, resume_epoch: int) -> None:
    if not verify_resume_lease(task, lease_id, resume_epoch=resume_epoch):
        raise RuntimeError("STALE_WRITER_LEASE: this chat no longer owns the task; re-inherit from the latest checkpoint")


def _receipt_state_items(raw: Any) -> tuple[str, ...]:
    if raw is None: return ()
    if not isinstance(raw, (list, tuple)): raw = [raw]
    items: list[str] = []
    for item in raw:
        if isinstance(item, Mapping):
            detail = item.get("detail") or item.get("reason") or item.get("type")
            items.append(str(detail if detail is not None else dict(item)))
        else: items.append(str(item))
    return tuple(x for x in items if x.strip())


def build_resume_progress_receipt(task: TaskMetadata, checkpoint: Mapping[str, Any] | None = None) -> ResumeProgressReceipt:
    checkpoint = checkpoint or {}
    if checkpoint:
        checkpoint_task_id = str(checkpoint.get("task_id") or "").strip()
        if not checkpoint_task_id:
            raise ValueError("checkpoint_missing_task_id")
        if checkpoint_task_id != task.task_id:
            raise ValueError(f"checkpoint_task_id_mismatch:{checkpoint_task_id}:{task.task_id}")
    blockers = _receipt_state_items(checkpoint.get("blockers")); waiting = _receipt_state_items(checkpoint.get("waiting_on"))
    persisted_at = task.updated_at
    raw_updated = checkpoint.get("updated_at")
    if isinstance(raw_updated, str):
        try: persisted_at = datetime.fromisoformat(raw_updated.replace("Z", "+00:00"))
        except ValueError: persisted_at = task.updated_at
    return ResumeProgressReceipt(
        task_id=task.task_id, display_name=candidate_display_name(task), persisted_at=persisted_at,
        status=TaskStatus(str(checkpoint.get("status", task.status.value))), current_stage=checkpoint.get("current_stage") or task.current_stage,
        next_action=checkpoint.get("next_action") or task.next_action, blockers_or_waiting_state=blockers + waiting,
        checkpoint_ref=task.checkpoint_ref, manifest_version=task.manifest_version, resume_epoch_before_takeover=task.resume_epoch,
    )


def build_turn_commit_receipt(task: TaskMetadata | None, *, commit_required: bool, write_succeeded: bool = False, verified_after_write: bool = False, lease_id: str | None = None, resume_epoch: int | None = None, detail: str = "") -> TurnCommitReceipt:
    if task is None:
        return TurnCommitReceipt(CommitStatus.NOT_APPLICABLE, None, None, None, None, None, None, False, detail or "no active durable task")
    if lease_id is not None and not verify_resume_lease(task, lease_id, resume_epoch=resume_epoch): status = CommitStatus.STALE_WRITER
    elif not commit_required: status = CommitStatus.NO_MATERIAL_CHANGE
    elif write_succeeded and verified_after_write: status = CommitStatus.COMMITTED
    else: status = CommitStatus.COMMIT_FAILED
    return TurnCommitReceipt(status, task.task_id, task.current_stage, task.next_action, task.checkpoint_ref, task.manifest_version, task.resume_epoch, bool(verified_after_write and status == CommitStatus.COMMITTED), detail)


def registry_manifest_drift(index_rows: Iterable[Mapping[str, Any]], manifest_rows: Iterable[Mapping[str, Any]]) -> list[str]:
    index = {str(row["task_id"]): row for row in index_rows if row.get("task_id")}
    manifests = {str(row["task_id"]): row for row in manifest_rows if row.get("task_id")}
    problems: list[str] = []
    for task_id in sorted(manifests.keys() - index.keys()): problems.append(f"registry-missing:{task_id}")
    for task_id in sorted(index.keys() - manifests.keys()): problems.append(f"registry-orphan:{task_id}")
    for task_id in sorted(index.keys() & manifests.keys()):
        for field_name in ("display_name_zh", "status", "current_stage", "next_action", "recovery_owner", "checkpoint_ref"):
            if index[task_id].get(field_name) != manifests[task_id].get(field_name): problems.append(f"registry-stale:{task_id}:{field_name}")
    return problems


def validate_checkpoint_quality(raw: Mapping[str, Any]) -> list[str]:
    problems: list[str] = []
    for field_name in ("task_id","task_class","domain","title","status","resume_eligible","resume_visibility","recovery_owner","updated_at","current_stage","next_action"):
        if field_name not in raw: problems.append(f"missing:{field_name}")
    if "resume_eligible" in raw and not isinstance(raw.get("resume_eligible"), bool): problems.append("resume_eligible-not-boolean")
    if raw.get("task_class") == "USER" and not str(raw.get("display_name_zh") or "").strip(): problems.append("user-task-missing-display-name-zh")
    if raw.get("task_class") == "USER" and raw.get("resume_eligible") is True and not raw.get("checkpoint_ref"): problems.append("resumable-user-without-checkpoint-ref")
    if raw.get("status") in {"COMPLETE", "ARCHIVED", "ABANDONED"} and raw.get("resume_visibility") == "DEFAULT": problems.append("terminal-task-default-visible")
    if raw.get("task_class") in {c.value for c in NON_USER_CLASSES} and raw.get("resume_visibility") == "DEFAULT": problems.append("non-user-default-visible")
    if raw.get("manifest_ref") and not str(raw.get("manifest_ref")).endswith("TASK_MANIFEST.json"): problems.append("invalid-task-manifest-ref")
    active_lease = raw.get("active_lease")
    if active_lease:
        if not active_lease.get("lease_id"): problems.append("active-lease-missing-id")
        if "resume_epoch" in active_lease and int(active_lease.get("resume_epoch", -1)) != int(raw.get("resume_epoch", 0)): problems.append("active-lease-epoch-mismatch")
    return problems
