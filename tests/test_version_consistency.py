import json
import re
from pathlib import Path

from runtime.universal_continuity import SCHEMA_VERSION

ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_contract_runtime_package_and_entrypoint_versions_stay_aligned():
    contract = load_json("CONTINUITY_CONTRACT.json")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")

    version = contract["schema_version"]
    assert version == SCHEMA_VERSION
    assert f'version = "{version}.0"' in pyproject
    assert f"Contract: v{version}" in entrypoint
    assert re.search(rf"Protocol v{re.escape(version)}\b", protocol)


def test_core_bootstrap_and_recovery_surfaces_use_current_protocol():
    version = load_json("CURRENT_PROTOCOL.json")["continuity_protocol_version"]
    assert version == SCHEMA_VERSION

    assert load_json("BARE_INHERIT_DISCOVERY.json")["continuity_contract"] == version
    assert load_json("BARE_INHERIT_DISCOVERY.json")["continuity_protocol_version"] == version
    assert load_json("CONTEXT_RECOVERY_POLICY.json")["continuity_contract"] == version
    assert load_json("CONTEXT_RECOVERY_POLICY.json")["continuity_protocol_version"] == version
    assert load_json("PROGRESS_OBSERVABILITY_POLICY.json")["continuity_contract"] == version
    assert load_json("OWNER_ADAPTER_CONTRACT.json")["continuity_contract"] == version
    assert load_json("NEW_CHAT_BOOTSTRAP.json")["continuity_protocol_version"] == version
    assert load_json("OWNER_REGISTRY.json")["continuity_protocol_version"] == version
    assert load_json("VERSION_LIFECYCLE_POLICY.json")["continuity_protocol"] == version
    assert load_json("LIVE_CHAT_RECONCILIATION_POLICY.json")["continuity_protocol"] == version


def test_owner_registry_points_to_current_protocol_adaptation_surfaces():
    registry = load_json("OWNER_REGISTRY.json")
    adaptation = load_json("OWNER_PROTOCOL_ADAPTATION_REGISTRY.json")

    assert registry["resolver"]["protocol_adaptation_registry"] == "OWNER_PROTOCOL_ADAPTATION_REGISTRY.json"
    statuses = {row["name"]: row["adapter_status"] for row in registry["owners"]}
    assert statuses["GENERIC_HANDOFF"] == "READY_V37_NATIVE"
    assert "V37" in statuses["FINANCIAL_WRITING_AGENT_RUNTIME"]
    assert "V37" in statuses["A_SHARE_MARKET_AGENT"]
    assert "V37" in statuses["NOVEL_OS"]
    assert "V37" in statuses["VIDEO_GROWTH_AGENT"]

    adaptation_owners = {row["owner"] for row in adaptation["owners"]}
    assert {
        "FINANCIAL_WRITING_AGENT_RUNTIME",
        "A_SHARE_MARKET_AGENT",
        "NOVEL_OS",
        "VIDEO_GROWTH_AGENT",
    }.issubset(adaptation_owners)
