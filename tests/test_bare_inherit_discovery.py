import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_bare_inherit_required_sources_match_owner_registry_participants():
    policy = load("BARE_INHERIT_DISCOVERY.json")
    owners = load("OWNER_REGISTRY.json")

    required = {row["owner"] for row in policy["required_sources"]}
    participants = {
        row["name"]
        for row in owners["owners"]
        if row.get("bare_inherit_participant") is True
    }

    assert required == participants
    assert required == {
        "GENERIC_HANDOFF",
        "FINANCIAL_WRITING_AGENT_RUNTIME",
        "A_SHARE_MARKET_AGENT",
        "NOVEL_OS",
        "VIDEO_GROWTH_AGENT",
    }


def test_bare_inherit_never_claims_total_from_partial_discovery():
    policy = load("BARE_INHERIT_DISCOVERY.json")
    contract = load("CONTINUITY_CONTRACT.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    assert policy["completion_rule"] == "ALL_REQUIRED_SOURCES_MUST_BE_QUERIED"
    assert policy["on_source_failure"] == "INCOMPLETE_DISCOVERY"
    assert policy["count_rule"] == "DO_NOT_REPORT_TOTAL_CANDIDATE_COUNT_UNLESS_DISCOVERY_COMPLETE"
    assert policy["partial_results_rule"].startswith("MAY_SHOW_PARTIAL_RESULTS_ONLY_IF_EXPLICITLY_LABELED_INCOMPLETE")

    assert contract["schema_version"] == "3.7"
    assert contract["bare_inherit_discovery"]["count_requires_complete_discovery"] is True
    assert contract["rules"]["bare_inherit_requires_complete_owner_discovery_before_reporting_count"] is True

    assert bootstrap["bare_inherit_discovery"]["must_query_all_required_sources"] is True
    assert bootstrap["bare_inherit_discovery"]["report_count_only_when_complete"] is True
    assert bootstrap["degraded_mode"]["bare_inherit_partial_owner_failure"].startswith("INCOMPLETE_DISCOVERY")


def test_system_infra_owners_do_not_pollute_bare_inherit():
    owners = load("OWNER_REGISTRY.json")
    by_name = {row["name"]: row for row in owners["owners"]}

    assert by_name["FINANCIAL_WRITING_AGENT_ENGINEERING"]["bare_inherit_participant"] is False
    assert by_name["FINANCIAL_WRITING_AGENT_STANDALONE"]["bare_inherit_participant"] is False
