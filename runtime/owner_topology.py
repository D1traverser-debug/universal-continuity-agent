from __future__ import annotations

from collections.abc import Mapping
from typing import Any

ALLOWED_OWNER_KINDS = {"BUSINESS", "FALLBACK", "ENGINEERING", "STANDALONE", "INFRA"}
MEMBERSHIP_AUTHORITY_ROLE = "SOLE_CONTROL_PLANE_OWNER_MEMBERSHIP_AUTHORITY"


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def owner_entries(registry: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    raw = registry.get("owners", [])
    if not isinstance(raw, list):
        return ()
    return tuple(entry for entry in raw if isinstance(entry, Mapping))


def business_owner_names(registry: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(_text(entry.get("name")) for entry in owner_entries(registry) if _text(entry.get("owner_kind")) == "BUSINESS" and _text(entry.get("name"))))


def bare_inherit_sources(registry: Mapping[str, Any]) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for entry in owner_entries(registry):
        if entry.get("bare_inherit_participant") is not True:
            continue
        name = _text(entry.get("name")); source = _text(entry.get("bare_inherit_source"))
        if name and source:
            rows.append({"owner": name, "source": source})
    rows.sort(key=lambda row: row["owner"])
    return tuple(rows)


def validate_owner_registry(registry: Mapping[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    owners_raw = registry.get("owners")
    if not isinstance(owners_raw, list) or not owners_raw:
        return ("OWNER_REGISTRY owners must be a non-empty list",)

    membership = registry.get("membership_authority")
    if not isinstance(membership, Mapping):
        errors.append("OWNER_REGISTRY missing membership_authority")
    else:
        if _text(membership.get("role")) != MEMBERSHIP_AUTHORITY_ROLE:
            errors.append("OWNER_REGISTRY membership_authority role is invalid")
        if membership.get("parallel_hard_coded_owner_lists_allowed") is not False:
            errors.append("OWNER_REGISTRY must forbid parallel hard-coded owner lists")

    names: set[str] = set(); namespace: dict[str, str] = {}; bare_sources: dict[str, str] = {}; kind_by_name: dict[str, str] = {}
    default_owner = _text(registry.get("default_owner"))

    for index, raw in enumerate(owners_raw):
        if not isinstance(raw, Mapping):
            errors.append(f"OWNER_REGISTRY owners[{index}] is not an object"); continue
        name = _text(raw.get("name"))
        if not name:
            errors.append(f"OWNER_REGISTRY owners[{index}] missing name"); continue
        if name in names: errors.append(f"duplicate owner name:{name}")
        names.add(name)
        kind = _text(raw.get("owner_kind")); kind_by_name[name] = kind
        if kind not in ALLOWED_OWNER_KINDS: errors.append(f"{name}: invalid or missing owner_kind:{kind or 'MISSING'}")
        domains = raw.get("domains")
        if not isinstance(domains, list) or not any(_text(item) for item in domains): errors.append(f"{name}: domains must be a non-empty list")
        participant = raw.get("bare_inherit_participant")
        if not isinstance(participant, bool): errors.append(f"{name}: bare_inherit_participant must be boolean")
        source = _text(raw.get("bare_inherit_source"))
        if participant is True:
            if not source:
                errors.append(f"{name}: bare participant missing bare_inherit_source")
            else:
                previous = bare_sources.get(source)
                if previous is not None and previous != name:
                    errors.append(f"duplicate bare_inherit_source:{source}:{previous}:{name}")
                bare_sources[source] = name
        if kind == "BUSINESS":
            for field in ("checkpoint_authority", "protocol_adapter", "execution_capability_ref"):
                if not _text(raw.get(field)): errors.append(f"{name}: BUSINESS owner missing {field}")
        aliases = raw.get("aliases", [])
        for token in (name, *aliases) if isinstance(aliases, list) else (name,):
            token_text = _text(token)
            if not token_text: continue
            previous = namespace.get(token_text)
            if previous is not None and previous != name: errors.append(f"owner name/alias collision:{token_text}:{previous}:{name}")
            namespace[token_text] = name

    if not default_owner or default_owner not in names:
        errors.append("OWNER_REGISTRY default_owner does not resolve to a canonical owner")
    elif kind_by_name.get(default_owner) != "FALLBACK":
        errors.append("OWNER_REGISTRY default_owner must be owner_kind=FALLBACK")
    return tuple(errors)
