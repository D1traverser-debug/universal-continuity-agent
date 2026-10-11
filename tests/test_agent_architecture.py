import json
from pathlib import Path

from runtime.agent_architecture import (
    ArchitectureStatus,
    validate_agent_manifest,
    validate_architecture_observation,
    validate_registry_architecture_pointers,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "AGENT_ARCHITECTURE_CONTRACT.json").read_text(encoding="utf-8"))


def valid_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "architecture_contract_version": "1.0",
        "owner": "SYNTHETIC_AGENT",
        "owner_kind": "BUSINESS",
        "skill": {"role": "ROUTER", "entrypoint": "skills/synthetic/SKILL.md"},
        "runtime": {
            "runtime_type": "HYBRID",
            "entrypoints": ["synthetic/runtime.py"],
            "tool_surface_refs": ["synthetic/tools.py"],
            "judgment_execution": "EXECUTABLE",
        },
        "workflow": {
            "state_authority_refs": ["synthetic/state.py"],
            "transition_guard_refs": ["synthetic/controller.py"],
        },
        "harness": {
            "ci_workflow_ref": ".github/workflows/ci.yml",
            "commands": ["pytest -q"],
            "suites": ["architecture", "contract", "trajectory"],
        },
        "references": {"canonical_roots": ["references"], "mirror_policy": "NONE"},
        "continuity": {
            "task_index_ref": "continuity/TASK_INDEX.json",
            "protocol_adapter_ref": "continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
            "execution_capability_ref": "continuity/EXECUTION_CAPABILITIES.json",
        },
    }


def test_v10_manifest_remains_compatible_under_v11_contract():
    result = validate_agent_manifest(valid_manifest(), CONTRACT)
    assert CONTRACT["schema_version"] == "1.1"
    assert result.status == ArchitectureStatus.PASS


def test_v11_owner_aliases_normalize_to_shared_semantics():
    manifest = valid_manifest()
    manifest["schema_version"] = "1.1"
    manifest["architecture_contract_version"] = "1.1"
    manifest["skill"]["role"] = "ROUTER_AND_PROGRESSIVE_POLICY_ENTRYPOINT"
    manifest["runtime"]["judgment_execution"] = "CHAT_BRIDGED_OWNER_GATED"
    manifest["references"]["mirror_policy"] = "GENERATED_DISTRIBUTION_MIRRORS_ONLY"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.PASS


def test_v11_field_shape_aliases_normalize_to_canonical_layers():
    manifest = valid_manifest()
    manifest["schema_version"] = "1.1"
    manifest["architecture_contract_version"] = "1.1"
    manifest["skill"]["role"] = "ROUTER_AND_PROGRESSIVE_POLICY_ENTRYPOINT"
    manifest["runtime"].pop("entrypoints")
    manifest["runtime"]["public_entrypoint"] = "synthetic/runtime.py"
    manifest["runtime"]["internal_components"] = ["synthetic/controller.py"]
    manifest["runtime"]["judgment_execution"] = "CHAT_BRIDGED_OWNER_GATED"
    manifest["references"].pop("canonical_roots")
    manifest["references"]["canonical_root"] = "references"
    manifest["references"]["mirror_policy"] = "GENERATED_DISTRIBUTION_MIRRORS_ONLY"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.PASS


def test_v11_video_aliases_normalize_to_shared_semantics():
    manifest = valid_manifest()
    manifest["schema_version"] = "1.1"
    manifest["architecture_contract_version"] = "1.1"
    manifest["skill"]["role"] = "ROUTER_AND_OPERATING_CONTRACT"
    manifest["runtime"]["judgment_execution"] = "EXECUTABLE_WITH_ASSURANCE_BOUNDARIES"
    manifest["references"]["mirror_policy"] = "ONLY_REQUIRED_DISTRIBUTION_MIRRORS_WITH_MACHINE_EQUALITY_CHECK"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.PASS


def test_unknown_v11_shared_alias_fails_closed():
    manifest = valid_manifest()
    manifest["architecture_contract_version"] = "1.1"
    manifest["skill"]["role"] = "SUPER_ROUTER"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.FAIL
    assert any("skill.role" in item for item in result.errors)


def test_unknown_future_manifest_version_fails_closed():
    manifest = valid_manifest()
    manifest["architecture_contract_version"] = "9.9"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.FAIL
    assert "architecture_contract_version unsupported" in result.errors


def test_big_skill_is_drift_not_silent_pass():
    manifest = valid_manifest()
    result = validate_agent_manifest(
        manifest,
        CONTRACT,
        file_sizes={manifest["skill"]["entrypoint"]: 20000},
    )
    assert result.status == ArchitectureStatus.PASS_WITH_DRIFT
    assert any("skill router exceeds" in warning for warning in result.warnings)


def test_skill_only_owner_fails():
    manifest = valid_manifest()
    del manifest["runtime"]
    del manifest["harness"]
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.FAIL
    assert "missing layer: runtime" in result.errors
    assert "missing layer: harness" in result.errors


def test_stale_architecture_observation_fails_against_external_head():
    observation = {
        "architecture_validation_head": "old",
        "architecture_validation_result": "PASS",
        "architecture_validation_ref": "ci://123",
    }
    result = validate_architecture_observation(observation, observed_owner_head="new")
    assert result.status == ArchitectureStatus.FAIL
    assert any("stale" in error for error in result.errors)


def test_matching_architecture_observation_passes():
    observation = {
        "architecture_validation_head": "abc",
        "architecture_validation_result": "PASS",
        "architecture_validation_ref": "ci://123",
    }
    result = validate_architecture_observation(observation, observed_owner_head="abc")
    assert result.status == ArchitectureStatus.PASS


def test_missing_repository_ref_fails():
    manifest = valid_manifest()
    paths = {
        "skills/synthetic/SKILL.md",
        "synthetic/runtime.py",
        "synthetic/state.py",
        "synthetic/controller.py",
        "synthetic/tools.py",
        ".github/workflows/ci.yml",
        "references/a.md",
        "continuity/TASK_INDEX.json",
        "continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
    }
    result = validate_agent_manifest(manifest, CONTRACT, repository_paths=paths)
    assert result.status == ArchitectureStatus.FAIL
    assert any("EXECUTION_CAPABILITIES" in error for error in result.errors)


def test_all_business_owners_require_agent_manifest_pointer():
    registry = {
        "owners": [
            {"name": "A", "owner_kind": "BUSINESS", "agent_manifest_ref": "repo@main:continuity/AGENT_MANIFEST.json"},
            {"name": "B", "owner_kind": "BUSINESS"},
            {"name": "F", "owner_kind": "FALLBACK"},
        ]
    }
    result = validate_registry_architecture_pointers(registry)
    assert result.status == ArchitectureStatus.FAIL
    assert result.errors == ("BUSINESS owner missing agent_manifest_ref: B",)
