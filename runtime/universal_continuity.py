from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Protocol, Sequence
from uuid import uuid4

SCHEMA_VERSION = "3.2"


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


DEFAULT_STATUSES = {TaskStatus.ACTIVE, TaskStatus.WAITING, TaskStatus.BLOCKED}
NON_USER_CLASSES = {
    TaskClass.SYSTEM_INFRA,
    TaskClass.TEST,
    TaskClass.FIXTURE,
    TaskClass.EVAL,
    TaskClass.MIGRATION,
}


@dataclass(frozen=True)
class ResumeLease:
    lease_id: str
    resume_epoch: int
    acquired_at: datetime
    supersedes_lease_id: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None) -> "ResumeLease | None":
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
            resume_epoch=int(raw["resume_epoch"]),
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
        return cls(
            task_id=str(raw["task_id"]),
            domain=str(raw["domain"]),
            title=str(raw["title"]),
            recovery_owner=str(raw["recovery_owner"]),
            status=TaskStatus(str(raw["status"])),
            task_class=TaskClass(str(raw.get("task_class", TaskClass.MIGRATION.value))),
            resume_eligible=bool(raw.get("resume_eligible", False)),
            resume_visibility=ResumeVisibility(str(raw.get("resume_visibility", ResumeVisibility.EXPLICIT_ONLY.value))),
            updated_at=dt,
            current_stage=raw.get("current_stage"),
            next_action=raw.get("next_action"),
            checkpoint_ref=raw.get("checkpoint_ref"),
            contract_version=raw.get("contract_version"),
            skill_version=raw.get("skill_version"),
            runtime_version=raw.get("runtime_version"),
            keywords=tuple(str(x) for x in raw.get("keywords", ()) if str(x).strip()),
            artifact_refs=tuple(str(x) for x in raw.get("artifact_refs", ()) if str(x).strip()),
            manifest_ref=raw.get("manifest_ref"),
            manifest_version=int(raw.get("manifest_version", 1)),
            resume_epoch=int(raw.get("resume_epoch", 0)),
            active_lease=ResumeLease.from_mapping(raw.get("active_lease")),
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


class OwnerAdapter(Protocol):
    owner_name: str

    def list_resumable_tasks(self) -> Sequence[Mapping[str, Any]]: ...
    def get_task_checkpoint(self, task_id: str) -> Mapping[str, Any]: ...
    def compatibility_check(self, task: TaskMetadata, current_contract: Mapping[str, Any]) -> CompatibilityDecision: ...


def bare_inherit_eligible(task: TaskMetadata) -> bool:
    return (
        task.task_class == TaskClass.USER
        and task.resume_eligible
        and task.resume_visibility == ResumeVisibility.DEFAULT
        and task.status in DEFAULT_STATUSES
    )


def explicit_eligible(task: TaskMetadata) -> bool:
    return task.status not in {TaskStatus.ABANDONED}


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


def _tokens(text: str) -> set[str]:
    normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {token for token in normalized.split() if token}


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _score_hint(task: TaskMetadata, hint: str | None, owner_hint: str | None, domain_hint: str | None, now: datetime) -> RecoveryCandidate:
    score = 0.0
    reasons: list[str] = []
    if owner_hint and task.recovery_owner == owner_hint:
        score += 5.0
        reasons.append("owner")
    if domain_hint and task.domain == domain_hint:
        score += 4.0
        reasons.append("domain")
    if hint:
        h = hint.strip().lower()
        title = task.title.lower()
        if h and h in title:
            score += 8.0
            reasons.append("title-substring")
        if _contains_cjk(h):
            for kw in task.keywords:
                if kw and kw.lower() in h:
                    score += 3.0
                    reasons.append(f"keyword:{kw}")
            if task.domain.lower() in h:
                score += 2.0
                reasons.append("domain-text")
        else:
            overlap = _tokens(h) & (_tokens(title) | set().union(*(_tokens(k) for k in task.keywords)) if task.keywords else _tokens(title))
            if overlap:
                score += min(5.0, float(len(overlap) * 2))
                reasons.append("token-overlap")
    age_hours = max(0.0, (now - task.updated_at.astimezone(timezone.utc)).total_seconds() / 3600.0)
    recency_bonus = max(0.0, 3.0 - min(3.0, age_hours / 24.0))
    score += recency_bonus
    if recency_bonus:
        reasons.append("recency")
    if task.status == TaskStatus.BLOCKED:
        score -= 0.25
    return RecoveryCandidate(task=task, score=score, reasons=tuple(reasons))


def resolve_candidates(
    tasks: Iterable[TaskMetadata],
    *,
    hint: str | None = None,
    owner_hint: str | None = None,
    domain_hint: str | None = None,
    explicit: bool = False,
    max_results: int = 5,
    now: datetime | None = None,
) -> list[RecoveryCandidate]:
    now = now or datetime.now(timezone.utc)
    eligible = [t for t in tasks if (explicit_eligible(t) if explicit else bare_inherit_eligible(t))]
    scored = [_score_hint(t, hint, owner_hint, domain_hint, now) for t in eligible]
    scored.sort(key=lambda c: (c.score, c.task.updated_at, c.task.task_id), reverse=True)
    return scored[: max(1, min(max_results, 5))]


def should_autoresume(candidates: Sequence[RecoveryCandidate], *, hint_present: bool) -> bool:
    if len(candidates) != 1:
        return False
    only = candidates[0]
    if not hint_present:
        return True
    semantic_reasons = {"owner", "domain", "title-substring", "token-overlap", "domain-text"}
    return bool(semantic_reasons.intersection(only.reasons) or any(r.startswith("keyword:") for r in only.reasons))


def classify_version_compatibility(
    task: TaskMetadata,
    *,
    current_contract_version: str | None,
    migration_supported_from: set[str] | None = None,
) -> CompatibilityDecision:
    migration_supported_from = migration_supported_from or set()
    old = task.contract_version
    new = current_contract_version
    if not old or old == "legacy-unclassified":
        return CompatibilityDecision(
            Compatibility.MIGRATABLE if "legacy-unclassified" in migration_supported_from else Compatibility.UNKNOWN,
            "persisted task has no classified contract version",
        )
    if not new:
        return CompatibilityDecision(Compatibility.UNKNOWN, "current owner contract version unavailable")
    if old == new:
        return CompatibilityDecision(Compatibility.COMPATIBLE, f"contract versions match: {old}")
    if old in migration_supported_from:
        return CompatibilityDecision(Compatibility.MIGRATABLE, f"owner declares migration path {old} -> {new}")
    return CompatibilityDecision(Compatibility.INCOMPATIBLE, f"no declared migration path {old} -> {new}")


def acquire_resume_lease(task: TaskMetadata, *, lease_id: str | None = None, now: datetime | None = None) -> TaskMetadata:
    """Create a new single-writer epoch for a newly inherited chat.

    Acquiring a lease intentionally supersedes the previous chat. The caller must
    persist the returned task manifest, re-read it, and verify the lease before
    doing substantive work. This is a fail-closed guard, not a transactional DB lock.
    """
    if task.task_class != TaskClass.USER:
        raise ValueError("only USER tasks may acquire a normal resume lease")
    if not explicit_eligible(task):
        raise ValueError(f"task status is not resumable: {task.status.value}")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    previous = task.active_lease.lease_id if task.active_lease else None
    next_epoch = max(task.resume_epoch, task.active_lease.resume_epoch if task.active_lease else 0) + 1
    lease = ResumeLease(
        lease_id=lease_id or str(uuid4()),
        resume_epoch=next_epoch,
        acquired_at=now,
        supersedes_lease_id=previous,
    )
    return replace(
        task,
        resume_epoch=next_epoch,
        active_lease=lease,
        manifest_version=task.manifest_version + 1,
        updated_at=now,
    )


def verify_resume_lease(task: TaskMetadata, lease_id: str, *, resume_epoch: int | None = None) -> bool:
    lease = task.active_lease
    if lease is None or lease.lease_id != lease_id:
        return False
    if resume_epoch is not None and lease.resume_epoch != resume_epoch:
        return False
    return lease.resume_epoch == task.resume_epoch


def assert_checkpoint_writer(task: TaskMetadata, *, lease_id: str, resume_epoch: int) -> None:
    if not verify_resume_lease(task, lease_id, resume_epoch=resume_epoch):
        raise RuntimeError("STALE_WRITER_LEASE: this chat no longer owns the task; re-inherit from the latest checkpoint")


def registry_manifest_drift(index_rows: Iterable[Mapping[str, Any]], manifest_rows: Iterable[Mapping[str, Any]]) -> list[str]:
    """Compare a rebuildable registry cache with authoritative per-task manifests."""
    index = {str(row["task_id"]): row for row in index_rows if row.get("task_id")}
    manifests = {str(row["task_id"]): row for row in manifest_rows if row.get("task_id")}
    problems: list[str] = []
    for task_id in sorted(manifests.keys() - index.keys()):
        problems.append(f"registry-missing:{task_id}")
    for task_id in sorted(index.keys() - manifests.keys()):
        problems.append(f"registry-orphan:{task_id}")
    for task_id in sorted(index.keys() & manifests.keys()):
        idx = index[task_id]
        man = manifests[task_id]
        for field_name in ("status", "current_stage", "next_action", "recovery_owner", "checkpoint_ref"):
            if idx.get(field_name) != man.get(field_name):
                problems.append(f"registry-stale:{task_id}:{field_name}")
    return problems


def validate_checkpoint_quality(raw: Mapping[str, Any]) -> list[str]:
    """Return problems instead of silently accepting weak checkpoints/manifests."""
    problems: list[str] = []
    for field_name in (
        "task_id", "task_class", "domain", "title", "status", "resume_eligible",
        "resume_visibility", "recovery_owner", "updated_at", "current_stage", "next_action",
    ):
        if field_name not in raw:
            problems.append(f"missing:{field_name}")
    if raw.get("task_class") == "USER" and raw.get("resume_eligible") is True and not raw.get("checkpoint_ref"):
        problems.append("resumable-user-without-checkpoint-ref")
    if raw.get("status") in {"COMPLETE", "ARCHIVED", "ABANDONED"} and raw.get("resume_visibility") == "DEFAULT":
        problems.append("terminal-task-default-visible")
    if raw.get("task_class") in {c.value for c in NON_USER_CLASSES} and raw.get("resume_visibility") == "DEFAULT":
        problems.append("non-user-default-visible")
    if raw.get("manifest_ref") and not str(raw.get("manifest_ref")).endswith("TASK_MANIFEST.json"):
        problems.append("invalid-task-manifest-ref")
    active_lease = raw.get("active_lease")
    if active_lease:
        if not active_lease.get("lease_id"):
            problems.append("active-lease-missing-id")
        if int(active_lease.get("resume_epoch", -1)) != int(raw.get("resume_epoch", 0)):
            problems.append("active-lease-epoch-mismatch")
    return problems
