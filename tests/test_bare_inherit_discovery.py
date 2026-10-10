import copy
import json
from pathlib import Path

from runtime.owner_topology import bare_inherit_sources, validate_owner_registry


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_bare_inherit_sources_are_derived_from_owner_registry_not_parallel_list():
    policy = load("BARE_INHERIT_DISCOVERY.json")
    owners = load("OWNER_REGISTRY.json")

    assert validate_owner_registry(owners) == ()
    assert "required_sources" not in policy
    authority = policy["participant_authority"]
    assert authority["source"] == "OWNER_REGISTRY.json"
    assert authority["selector"] == "owners[*].bare_inherit_participant == true"
    assert authority["source_field"] == "bare_inherit_source"
    assert authority["hard_coded_owner_list_allowed"] is False

    derived = {row["owner"]: row["source"] for row in bare_inherit_sources(owners)}
    participants = {
        row["name"]: row["bare_inherit_source"]
        for row in owners["owners"]
        if row.get("bare_inherit_participant") is True
    }
    assert derived == participants


def test_synthetic_new_owner_joins_bare_quorum_without_policy_or_code_name_change():
    policy = load("BARE_INHERIT_DISCOVERY.json")
    owners = copy.deepcopy(load("OWNER_REGISTRY.json"))
    before_policy = json.dumps(policy, sort_keys=True)

    owners["owners"].append(
        {
            "name": "SYNTHETIC_NEW_AGENT",
            "owner_kind": "BUSINESS",
            "domains": ["SYNTHETIC_DOMAIN"],
            "priority": 100,
            "adapter_status": "SYNTHETIC_FIXTURE",
            "bare_inherit_participant": True,
            "bare_inherit_source": "synthetic-owner@main:continuity/TASK_INDEX.json",
            "checkpoint_authority": "synthetic-owner@main:continuity/tasks/<task_id>/TASK_MANIFEST.json",
            "protocol_adapter": "synthetic-owner@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json",
            "execution_capability_ref": "synthetic-owner@main:continuity/EXECUTION_CAPABILITIES.json",
        }
    )

    assert validate_owner_registry(owners) == ()
    derived = {row["owner"]: row["source"] for row in bare_inherit_sources(owners)}
    assert derived["SYNTHETIC_NEW_AGENT"] == "synthetic-owner@main:continuity/TASK_INDEX.json"
    assert json.dumps(policy, sort_keys=True) == before_policy


def test_bare_inherit_never_claims_total_from_partial_discovery():
    policy = load("BARE_INHERIT_DISCOVERY.json")
    contract = load("CONTINUITY_CONTRACT.json")
    bootstrap = load("NEW_CHAT_BOOTSTRAP.json")

    assert policy["completion_rule"] == "ALL_DERIVED_REQUIRED_SOURCES_MUST_BE_QUERIED"
    assert policy["on_source_failure"] == "INCOMPLETE_DISCOVERY"
    assert policy["count_rule"] == "DO_NOT_REPORT_TOTAL_CANDIDATE_COUNT_UNLESS_DISCOVERY_COMPLETE"
    assert policy["partial_results_rule"].startswith("MAY_SHOW_PARTIAL_RESULTS_ONLY_IF_EXPLICITLY_LABELED_INCOMPLETE")

    assert contract["schema_version"] == "3.7"
    assert contract["bare_inherit_discovery"]["count_requires_complete_discovery"] is True
    assert contract["rules"]["bare_inherit_requires_complete_owner_discovery_before_reporting_count"] is True

    assert bootstrap["bare_inherit_discovery"]["must_query_all_required_sources"] is True
    assert bootstrap["bare_inherit_discovery"]["report_count_only_when_complete"] is True
    assert bootstrap["degraded_mode"]["bare_inherit_partial_owner_failure"].startswith("INCOMPLETE_DISCOVERY")


def test_non_default_owner_kinds_do_not_pollute_bare_inherit_unless_explicitly_opted_in():
    owners = load("OWNER_REGISTRY.json")
    by_name = {row["name"]: row for row in owners["owners"]}

    assert by_name["FINANCIAL_WRITING_AGENT_ENGINEERING"]["owner_kind"] == "ENGINEERING"
    assert by_name["FINANCIAL_WRITING_AGENT_ENGINEERING"]["bare_inherit_participant"] is False
    assert by_name["FINANCIAL_WRITING_AGENT_STANDALONE"]["owner_kind"] == "STANDALONE"
    assert by_name["FINANCIAL_WRITING_AGENT_STANDALONE"]["bare_inherit_participant"] is False


def test_novel_legacy_alias_does_not_replace_canonical_owner_name():
    owners = load("OWNER_REGISTRY.json")
    by_name = {row["name"]: row for row in owners["owners"]}
    novel = by_name["NOVEL_WRITING_AGENT"]
    assert "NOVEL_OS" in novel.get("aliases", [])
    assert novel["owner_kind"] == "BUSINESS"
    assert novel["bare_inherit_participant"] is True
