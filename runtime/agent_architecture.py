from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class ArchitectureStatus(str, Enum):
    PASS = "PASS"
    PASS_WITH_DRIFT = "PASS_WITH_DRIFT"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ArchitectureResult:
    status: ArchitectureStatus
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def _nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(x, str) and x.strip() for x in value)


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_fields(container: Mapping[str, Any], fields: Sequence[str], prefix: str, errors: list[str]) -> None:
    for field in fields:
        value = container.get(field)
        if isinstance(value, list):
            if not _nonempty_list(value):
                errors.append(f"{prefix}.{field} must be a non-empty string list")
        elif not _nonempty_str(value):
            errors.append(f"{prefix}.{field} is required")


def validate_agent_manifest(
    manifest: Mapping[str, Any],
    contract: Mapping[str, Any],
    *,
    repository_paths: set[str] | None = None,
    file_sizes: Mapping[str, int] | None = None,
) -> ArchitectureResult:
    errors: list[str] = []
    warnings: list[str] = []

    if str(manifest.get("architecture_contract_version", "")).strip() != str(contract.get("schema_version", "")).strip():
        errors.append("architecture_contract_version mismatch")
    if not _nonempty_str(manifest.get("owner")):
        errors.append("owner is required")
    if manifest.get("owner_kind") != "BUSINESS":
        errors.append("owner_kind must be BUSINESS")

    required_layers = contract.get("required_layers", {})
    for layer_name in ("skill", "runtime", "workflow", "harness", "references", "continuity"):
        layer = manifest.get(layer_name)
        if not isinstance(layer, Mapping):
            errors.append(f"missing layer: {layer_name}")
            continue
        spec = required_layers.get(layer_name, {}) if isinstance(required_layers, Mapping) else {}
        _require_fields(layer, spec.get("required_fields", ()), layer_name, errors)

    skill = manifest.get("skill", {}) if isinstance(manifest.get("skill"), Mapping) else {}
    if skill and skill.get("role") != "ROUTER":
        errors.append("skill.role must be ROUTER")
    skill_entrypoint = skill.get("entrypoint")
    target_max = int(required_layers.get("skill", {}).get("target_max_bytes", 0) or 0)
    if file_sizes and _nonempty_str(skill_entrypoint) and skill_entrypoint in file_sizes and target_max:
        actual = int(file_sizes[skill_entrypoint])
        if actual > target_max:
            warnings.append(f"skill router exceeds target byte budget: {actual}>{target_max}")

    runtime = manifest.get("runtime", {}) if isinstance(manifest.get("runtime"), Mapping) else {}
    allowed_runtime = set(required_layers.get("runtime", {}).get("allowed_runtime_type", ()))
    if runtime and runtime.get("runtime_type") not in allowed_runtime:
        errors.append("runtime.runtime_type is not allowed")
    judgment = runtime.get("judgment_execution")
    allowed_judgment = set(required_layers.get("runtime", {}).get("judgment_execution_status", ()))
    if runtime and judgment not in allowed_judgment:
        errors.append("runtime.judgment_execution is not allowed")

    harness = manifest.get("harness", {}) if isinstance(manifest.get("harness"), Mapping) else {}
    suites = set(harness.get("suites", ())) if isinstance(harness.get("suites"), list) else set()
    minimum_suites = set(required_layers.get("harness", {}).get("minimum_suites", ()))
    missing_suites = sorted(minimum_suites - suites)
    if missing_suites:
        errors.append(f"harness missing minimum suites: {missing_suites}")

    refs = manifest.get("references", {}) if isinstance(manifest.get("references"), Mapping) else {}
    mirror_policy = refs.get("mirror_policy")
    allowed_mirror = set(required_layers.get("references", {}).get("allowed_mirror_policy", ()))
    if refs and mirror_policy not in allowed_mirror:
        errors.append("references.mirror_policy is not allowed")

    if repository_paths is not None:
        refs_to_check: list[str] = []
        if _nonempty_str(skill_entrypoint):
            refs_to_check.append(str(skill_entrypoint))
        for layer_name, fields in {
            "runtime": ("entrypoints", "tool_surface_refs"),
            "workflow": ("state_authority_refs", "transition_guard_refs"),
            "harness": ("ci_workflow_ref",),
            "references": ("canonical_roots",),
            "continuity": ("task_index_ref", "protocol_adapter_ref", "execution_capability_ref"),
        }.items():
            layer = manifest.get(layer_name, {})
            if not isinstance(layer, Mapping):
                continue
            for field in fields:
                value = layer.get(field)
                if isinstance(value, str) and value.strip():
                    refs_to_check.append(value.strip())
                elif isinstance(value, list):
                    refs_to_check.extend(str(x).strip() for x in value if str(x).strip())
        for ref in refs_to_check:
            normalized = ref.rstrip("/")
            if normalized not in repository_paths and not any(path.startswith(normalized + "/") for path in repository_paths):
                errors.append(f"architecture ref missing from repository snapshot: {ref}")

    status = ArchitectureStatus.FAIL if errors else (ArchitectureStatus.PASS_WITH_DRIFT if warnings else ArchitectureStatus.PASS)
    return ArchitectureResult(status=status, errors=tuple(errors), warnings=tuple(warnings))


def validate_architecture_observation(observation: Mapping[str, Any], *, observed_owner_head: str) -> ArchitectureResult:
    errors: list[str] = []
    warnings: list[str] = []
    required = ("architecture_validation_head", "architecture_validation_result", "architecture_validation_ref")
    _require_fields(observation, required, "architecture_observation", errors)
    validated_head = str(observation.get("architecture_validation_head", "")).strip()
    if validated_head and validated_head != str(observed_owner_head).strip():
        errors.append("architecture validation is stale relative to externally observed owner head")
    result = str(observation.get("architecture_validation_result", "")).strip()
    if result not in {"PASS", "PASS_WITH_DRIFT", "FAIL"}:
        errors.append("architecture_validation_result is invalid")
    if result == "PASS_WITH_DRIFT":
        warnings.append("owner architecture currently has acknowledged drift")
    if result == "FAIL":
        errors.append("owner architecture validation failed")
    status = ArchitectureStatus.FAIL if errors else (ArchitectureStatus.PASS_WITH_DRIFT if warnings else ArchitectureStatus.PASS)
    return ArchitectureResult(status=status, errors=tuple(errors), warnings=tuple(warnings))


def validate_registry_architecture_pointers(owner_registry: Mapping[str, Any]) -> ArchitectureResult:
    errors: list[str] = []
    warnings: list[str] = []
    for owner in owner_registry.get("owners", []):
        if not isinstance(owner, Mapping) or owner.get("owner_kind") != "BUSINESS":
            continue
        name = str(owner.get("name", "<unknown>"))
        ref = owner.get("agent_manifest_ref")
        if not _nonempty_str(ref):
            errors.append(f"BUSINESS owner missing agent_manifest_ref: {name}")
    return ArchitectureResult(
        status=ArchitectureStatus.FAIL if errors else ArchitectureStatus.PASS,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )
