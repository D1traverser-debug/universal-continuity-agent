import json
from pathlib import Path

from runtime.agent_architecture import ArchitectureStatus, validate_agent_manifest, validate_registry_architecture_pointers

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
        "observed_owner_head": "abc",
        "harness_receipt_head": "abc",
    }


def test_valid_agent_architecture_passes():
    result = validate_agent_manifest(valid_manifest(), CONTRACT)
    assert result.status == ArchitectureStatus.PASS


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


def test_stale_harness_receipt_fails():
    manifest = valid_manifest()
    manifest["harness_receipt_head"] = "old"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status == ArchitectureStatus.FAIL
    assert any("stale" in error for error in result.errors)


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
