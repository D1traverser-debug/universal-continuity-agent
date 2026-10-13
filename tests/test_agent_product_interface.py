from __future__ import annotations

import json
from pathlib import Path

from runtime.agent_architecture import ArchitectureStatus, validate_agent_manifest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "AGENT_ARCHITECTURE_CONTRACT.json").read_text(encoding="utf-8"))


def _manifest(version: str = "1.2") -> dict:
    value = {
        "architecture_contract_version": version,
        "owner": "TEST_BUSINESS_OWNER",
        "owner_kind": "BUSINESS",
        "skill": {"role": "ROUTER", "entrypoint": "skills/test/SKILL.md"},
        "runtime": {
            "runtime_type": "DETERMINISTIC_WORKFLOW",
            "entrypoints": ["runtime.py"],
            "judgment_execution": "EXECUTABLE",
        },
        "workflow": {
            "state_authority_refs": ["state.json"],
            "transition_guard_refs": ["runtime.py"],
        },
        "harness": {
            "ci_workflow_ref": ".github/workflows/ci.yml",
            "commands": ["pytest -q"],
            "suites": ["contract", "trajectory"],
        },
        "references": {"canonical_roots": ["references"], "mirror_policy": "NONE"},
        "continuity": {
            "task_index_ref": "continuity/TASK_INDEX.md",
            "protocol_adapter_ref": "continuity/OWNER_ADAPTER.json",
            "execution_capability_ref": "continuity/EXECUTION_CAPABILITIES.json",
        },
    }
    if version == "1.2":
        value["product_interface"] = {
            "interaction_surface": "CHATGPT",
            "entry_model": "SINGLE_OWNER_ENTRY",
            "execution_mode_selection": "SYSTEM_INTERNAL",
            "business_contract_model": "SINGLE_CANONICAL_OWNER_WORKFLOW",
        }
    return value


def test_current_business_manifest_requires_single_chatgpt_product_entry() -> None:
    result = validate_agent_manifest(_manifest(), CONTRACT)
    assert result.status is ArchitectureStatus.PASS


def test_current_business_manifest_rejects_missing_product_interface() -> None:
    manifest = _manifest()
    manifest.pop("product_interface")
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status is ArchitectureStatus.FAIL
    assert "business product_interface is required for architecture contract 1.2" in result.errors


def test_current_business_manifest_rejects_user_selected_execution_mode() -> None:
    manifest = _manifest()
    manifest["product_interface"]["execution_mode_selection"] = "USER_CHOICE"
    result = validate_agent_manifest(manifest, CONTRACT)
    assert result.status is ArchitectureStatus.FAIL
    assert any("product_interface.execution_mode_selection" in item for item in result.errors)


def test_legacy_manifest_remains_backward_compatible() -> None:
    result = validate_agent_manifest(_manifest("1.1"), CONTRACT)
    assert result.status is ArchitectureStatus.PASS


def test_readiness_contract_keeps_executor_modes_internal() -> None:
    readiness = json.loads((ROOT / "EXECUTION_READINESS_CONTRACT.json").read_text(encoding="utf-8"))
    boundary = readiness["product_boundary"]
    assert boundary["normal_interaction_surface"] == "CHATGPT_OWNER_SKILL"
    assert boundary["execution_modes_are"] == "INTERNAL_DISPATCH_AND_EVIDENCE_METADATA"
    assert boundary["normal_user_mode_selection"] == "NONE"
    assert any("separate user-selectable products" in item for item in readiness["hard_invariants"])
