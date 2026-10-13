from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping
import re


_SCOPE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,7}$")


def _parse_timestamp(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        raise ValueError("persisted_at must not be blank")
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def format_human_revision(*, scope_code: str, persisted_at: datetime | str, durable_version: int) -> str:
    """Derive a human-facing revision without creating another source of truth.

    The date uses the calendar date encoded by the authoritative persisted timestamp.
    The revision sequence is an already-authoritative monotonic task/owner version.
    No daily counter, Git-history scan, timezone conversion, or tag mutation occurs.
    """

    code = str(scope_code).strip().upper()
    if not _SCOPE_RE.fullmatch(code):
        raise ValueError("scope_code must be 2-8 uppercase alphanumeric characters and start with a letter")
    version = int(durable_version)
    if version < 1:
        raise ValueError("durable_version must be >= 1")
    dt = _parse_timestamp(persisted_at)
    return f"{code}-{dt:%Y%m%d}-r{version}"


def derive_human_revision(
    manifest: Mapping[str, Any],
    *,
    scope_code: str,
    timestamp_field: str = "updated_at",
    version_field: str = "manifest_version",
) -> str:
    """Derive a display revision from an authoritative manifest/owner state mapping."""

    if timestamp_field not in manifest:
        raise ValueError(f"missing authoritative timestamp field:{timestamp_field}")
    if version_field not in manifest:
        raise ValueError(f"missing authoritative durable version field:{version_field}")
    return format_human_revision(
        scope_code=scope_code,
        persisted_at=manifest[timestamp_field],
        durable_version=int(manifest[version_field]),
    )
