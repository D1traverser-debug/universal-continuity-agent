import copy
import json
from pathlib import Path

from runtime.owner_topology import validate_owner_registry


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_global_preflight_and_continuation_bootstrap_scopes_are_separate():
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")
    contract = load("CONTINUITY_CONTRACT.json")

    assert bootstrap["startup_hook"]["continuation_routing_scope"] == "EXPLICIT_CONTINUATION_INTENT_ONLY"
    assert bootstrap["startup_hook"]["defect_signal_preflight_scope"] == "ALL_MATERIAL_RESPONSE_OR_ACTION_INPUTS"
    assert bootstrap["startup_hook"]["no_defect_loads_full_maintenance"] is False

    trigger = contract["startup_trigger"]
    assert trigger["continuation_routing_scope"] == "EXPLICIT_CONTINUATION_INTENT_ONLY"
    assert trigger["defect_signal_preflight_scope"] == "ALL_MATERIAL_RESPONSE_OR_ACTION_INPUTS"
    assert trigger["defect_signal_preflight_is_lightweight"] is True
    assert trigger["no_defect_loads_full_maintenance"] is False
    assert contract["rules"]["no_defect_preflight_must_not_trigger_full_maintenance_or_global_discovery"] is True


def test_business_membership_adapter_status_is_stable_not_live_assurance():
    registry = load("OWNER_REGISTRY.json")
    assert validate_owner_registry(registry) == ()

    business = [row for row in registry["owners"] if row["owner_kind"] == "BUSINESS"]
    assert business
    for row in business:
        assert row["adapter_status"] == "READY_V37_PROTOCOL_ADAPTER_DECLARED"

    bad = copy.deepcopy(registry)
    bad_row = next(row for row in bad["owners"] if row["owner_kind"] == "BUSINESS")
    bad_row["adapter_status"] = "READY_V37_OWNER_CI_PASS__LIVE_QUALITY_PENDING"
    errors = validate_owner_registry(bad)
    assert any("mutable operational assurance token" in item for item in errors)


def test_control_signal_cache_distinguishes_active_historical_open_and_resolved():
    contract = load("CONTROL_SIGNAL_CONTRACT.json")
    observations = load("OWNER_ARCHITECTURE_OBSERVATIONS.json")
    manifest = load("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    lifecycle = contract["lifecycle"]

    assert lifecycle["states"] == ["ACTIVE", "HISTORICAL_OPEN", "RESOLVED"]
    assert lifecycle["historical_open_reference_field"] == "historical_open_control_signal_ref"
    assert lifecycle["undifferentiated_control_signal_ref_for_current_cache_forbidden"] is True
    assert lifecycle["closed_signal_may_prove_current_drift"] is False
    assert lifecycle["historical_open_signal_may_prove_current_drift"] is False
    assert lifecycle["historical_open_may_authorize_recreation_or_reenable"] is False
    assert lifecycle["open_signal_may_override_fresher_reobservation"] is False

    rows = {row["owner"]: row for row in observations["owners"]}
    assert all("control_signal_ref" not in row for row in rows.values())
    assert rows["FINANCIAL_WRITING_AGENT_RUNTIME"]["resolved_control_signal_ref"].endswith("#7")
    assert rows["A_SHARE_MARKET_AGENT"]["resolved_control_signal_ref"].endswith("#2")
    assert rows["A_SHARE_MARKET_AGENT"]["latest_context_footprint"]["utf8_bytes"] == 6733
    assert rows["A_SHARE_MARKET_AGENT"]["latest_context_footprint"]["result"] == "WITHIN_TARGET"
    assert rows["NOVEL_WRITING_AGENT"]["active_control_signal_ref"].endswith("#3")
    assert rows["VIDEO_GROWTH_AGENT"]["active_control_signal_ref"].endswith("#4")

    assert manifest["open_control_signal_refs"] == [
        "D1traverser-debug/universal-continuity-agent#3",
        "D1traverser-debug/universal-continuity-agent#4",
    ]
    assert manifest["historical_open_control_signal_refs"] == [
        "D1traverser-debug/universal-continuity-agent#12"
    ]
    assert manifest["resolved_control_signal_refs"] == [
        "D1traverser-debug/universal-continuity-agent#2",
        "D1traverser-debug/universal-continuity-agent#7",
    ]
    assert manifest["monitor_recreation_authorized"] is False
    assert "NOT_CURRENT_DRIFT" in manifest["monitor_historical_issue_12_status"]


def test_universal_entrypoint_preserves_reserved_headroom_under_hard_budget():
    size = (ROOT / "ENTRYPOINT.md").stat().st_size
    assert size <= 8192
    assert 8192 - size >= 512


def test_task_manifest_tracks_current_control_signal_contract_version():
    manifest = load("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    contract = load("CONTROL_SIGNAL_CONTRACT.json")
    assert manifest["control_signal_contract_version"] == contract["schema_version"]
