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


def _manifest_version(manifest: Mapping[str, Any]) -> str:
    return str(manifest.get("architecture_contract_version", "")).strip()


def _normalize_shared_value(contract: Mapping[str, Any], manifest_version: str, category: str, value: Any) -> Any:
    compatibility = contract.get("compatibility", {})
    if not isinstance(compatibility, Mapping):
        return value
    aliases_by_version = compatibility.get("aliases_by_manifest_version", {})
    if not isinstance(aliases_by_version, Mapping):
        return value
    aliases = aliases_by_version.get(manifest_version, {})
    if not isinstance(aliases, Mapping):
        return value
    category_aliases = aliases.get(category, {})
    if not isinstance(category_aliases, Mapping):
        return value
    return category_aliases.get(value, value)


def _normalized_layer(manifest: Mapping[str, Any], manifest_version: str, layer_name: str) -> dict[str, Any]:
    raw = manifest.get(layer_name, {})
    if not isinstance(raw, Mapping):
        return {}
    layer = dict(raw)
    if manifest_version == "1.1" and layer_name == "runtime" and not _nonempty_list(layer.get("entrypoints")):
        combined: list[str] = []
        public_entrypoint = layer.get("public_entrypoint")
        if _nonempty_str(public_entrypoint):
            combined.append(str(public_entrypoint).strip())
        internal = layer.get("internal_components")
        if isinstance(internal, list):
            combined.extend(str(item).strip() for item in internal if _nonempty_str(item))
        if combined:
            layer["entrypoints"] = combined
    if manifest_version == "1.1" and layer_name == "references" and not _nonempty_list(layer.get("canonical_roots")):
        canonical_root = layer.get("canonical_root")
        if _nonempty_str(canonical_root):
            layer["canonical_roots"] = [str(canonical_root).strip()]
    return layer


def validate_agent_manifest(
    manifest: Mapping[str, Any],
    contract: Mapping[str, Any],
    *,
    repository_paths: set[str] | None = None,
    file_sizes: Mapping[str, int] | None = None,
) -> ArchitectureResult:
    errors: list[str] = []
    warnings: list[str] = []

    manifest_version = _manifest_version(manifest)
    compatibility = contract.get("compatibility", {})
    supported_versions = set(compatibility.get("supported_manifest_versions", ())) if isinstance(compatibility, Mapping) else set()
    if not supported_versions:
        supported_versions = {str(contract.get("schema_version", "")).strip()}
    if manifest_version not in supported_versions:
        errors.append("architecture_contract_version unsupported")

    if not _nonempty_str(manifest.get("owner")):
        errors.append("owner is required")
    owner_kind = manifest.get("owner_kind")
    allowed_owner_kinds = set(contract.get("applies_to_owner_kind", ()))
    if owner_kind not in allowed_owner_kinds:
        errors.append("owner_kind is outside AGENT_ARCHITECTURE_CONTRACT scope")

    required_layers = contract.get("required_layers", {})
    layers: dict[str, dict[str, Any]] = {}
    for layer_name in ("skill", "runtime", "workflow", "harness", "references", "continuity"):
        raw = manifest.get(layer_name)
        if not isinstance(raw, Mapping):
            errors.append(f"missing layer: {layer_name}")
            layers[layer_name] = {}
            continue
        layer = _normalized_layer(manifest, manifest_version, layer_name)
        layers[layer_name] = layer
        spec = required_layers.get(layer_name, {}) if isinstance(required_layers, Mapping) else {}
        fields = spec.get("required_fields", ())
        if layer_name == "continuity":
            fields = spec.get(
                "system_infra_required_fields" if owner_kind == "SYSTEM_INFRA" else "business_required_fields",
                (),
            )
        _require_fields(layer, fields, layer_name, errors)

    skill = layers.get("skill", {})
    skill_role = _normalize_shared_value(contract, manifest_version, "skill_role", skill.get("role"))
    allowed_skill_roles = set(required_layers.get("skill", {}).get("canonical_roles", ("ROUTER",)))
    if skill and skill_role not in allowed_skill_roles:
        errors.append("skill.role is not a supported router role")
    skill_entrypoint = skill.get("entrypoint")
    target_max = int(required_layers.get("skill", {}).get("target_max_bytes", 0) or 0)
    if file_sizes and _nonempty_str(skill_entrypoint) and skill_entrypoint in file_sizes and target_max:
        actual = int(file_sizes[skill_entrypoint])
        if actual > target_max:
            warnings.append(f"skill router exceeds target byte budget: {actual}>{target_max}")

    runtime = layers.get("runtime", {})
    allowed_runtime = set(required_layers.get("runtime", {}).get("allowed_runtime_type", ()))
    if runtime and runtime.get("runtime_type") not in allowed_runtime:
        errors.append("runtime.runtime_type is not allowed")
    judgment = _normalize_shared_value(contract, manifest_version, "judgment_execution", runtime.get("judgment_execution"))
    allowed_judgment = set(required_layers.get("runtime", {}).get("judgment_execution_status", ()))
    if runtime and judgment not in allowed_judgment:
        errors.append("runtime.judgment_execution is not allowed")

    harness = layers.get("harness", {})
    suites = set(harness.get("suites", ())) if isinstance(harness.get("suites"), list) else set()
    minimum_suites = set(required_layers.get("harness", {}).get("minimum_owner_local_suites", ()))
    missing_suites = sorted(minimum_suites - suites)
    if missing_suites:
        errors.append(f"harness missing minimum owner-local suites: {missing_suites}")

    refs = layers.get("references", {})
    mirror_policy = _normalize_shared_value(contract, manifest_version, "mirror_policy", refs.get("mirror_policy"))
    allowed_mirror = set(required_layers.get("references", {}).get("allowed_mirror_policy", ()))
    if refs and mirror_policy not in allowed_mirror:
        errors.append("references.mirror_policy is not allowed")

    if repository_paths is not None:
        refs_to_check: list[str] = []
        if _nonempty_str(skill_entrypoint):
            refs_to_check.append(str(skill_entrypoint))
        reference_fields = {
            "runtime": ("entrypoints", "tool_surface_refs"),
            "workflow": ("state_authority_refs", "transition_guard_refs"),
            "harness": ("ci_workflow_ref",),
            "references": ("canonical_roots",),
            "continuity": (
                ("task_manifest_ref", "owner_registry_ref", "current_protocol_ref")
                if owner_kind == "SYSTEM_INFRA"
                else ("task_index_ref", "protocol_adapter_ref", "execution_capability_ref")
            ),
        }
        for layer_name, fields in reference_fields.items():
            layer = layers.get(layer_name, {})
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
