from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class MethodologyConformanceResult:
    status: str
    active_profiles: tuple[str, ...]
    errors: tuple[str, ...]


def _resolve_path(root: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = root
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            raise KeyError(dotted_path)
        current = current[part]
    return current


def evaluate_methodology_conformance(
    owner_declaration: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> MethodologyConformanceResult:
    """Validate composable methodology profiles without copying their semantics into owners.

    The central contract owns profile identity/version and hard override boundaries. Owners bind
    profile hooks to domain-local implementations. Domain specialization is allowed, but a local
    override may not replace cross-agent authority/evidence/reliability invariants.
    """

    composition = contract.get("methodology_composition")
    if not isinstance(composition, Mapping):
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_contract_methodology_composition",),
        )

    profiles = composition.get("profiles")
    if not isinstance(profiles, Mapping):
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_contract_profiles",),
        )

    methodology = owner_declaration.get("methodology")
    if not isinstance(methodology, Mapping):
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_owner_methodology",),
        )

    profile_refs = methodology.get("profile_refs")
    hook_bindings = methodology.get("hook_bindings")
    overrides = methodology.get("overrides", {})
    if not isinstance(profile_refs, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("missing_or_invalid_profile_refs",))
    if not isinstance(hook_bindings, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("missing_or_invalid_hook_bindings",))
    if not isinstance(overrides, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("invalid_overrides",))

    errors: list[str] = []
    active_profiles: list[str] = []

    forbidden_overrides = set(str(item) for item in composition.get("forbidden_override_keys", ()))
    for key in overrides:
        if str(key) in forbidden_overrides:
            errors.append(f"forbidden_override:{key}")

    for profile_id, requested_version in profile_refs.items():
        profile = profiles.get(profile_id)
        if not isinstance(profile, Mapping):
            errors.append(f"unknown_profile:{profile_id}")
            continue

        expected_version = str(profile.get("version", ""))
        if str(requested_version) != expected_version:
            errors.append(
                f"profile_version_mismatch:{profile_id}:requested={requested_version}:expected={expected_version}"
            )
            continue

        required_hooks_from = str(profile.get("required_hooks_from", ""))
        try:
            required_hooks = _resolve_path(contract, required_hooks_from)
        except KeyError:
            errors.append(f"invalid_required_hooks_ref:{profile_id}:{required_hooks_from}")
            continue

        if not isinstance(required_hooks, list):
            errors.append(f"required_hooks_not_list:{profile_id}:{required_hooks_from}")
            continue

        for hook in required_hooks:
            binding = hook_bindings.get(hook)
            if not isinstance(binding, str) or not binding.strip():
                errors.append(f"missing_hook_binding:{profile_id}:{hook}")

        active_profiles.append(f"{profile_id}@{expected_version}")

    status = "PASS" if not errors else "FAIL"
    return MethodologyConformanceResult(
        status=status,
        active_profiles=tuple(active_profiles),
        errors=tuple(errors),
    )
