import json
from pathlib import Path

from runtime.context_footprint import (
    approximate_tokens_from_utf8_bytes,
    footprint_within_budget,
    measure_context_footprint,
)


ROOT = Path(__file__).resolve().parents[1]


def contract():
    return json.loads((ROOT / "AGENT_ARCHITECTURE_CONTRACT.json").read_text(encoding="utf-8"))


def test_approximate_token_estimate_is_explicitly_byte_based():
    assert approximate_tokens_from_utf8_bytes(0) == 0
    assert approximate_tokens_from_utf8_bytes(1) == 1
    assert approximate_tokens_from_utf8_bytes(4) == 1
    assert approximate_tokens_from_utf8_bytes(5) == 2


def test_universal_minimal_repo_bootstrap_has_measured_budget():
    budget = contract()["context_footprint"]["universal_hot_path_budgets"]["minimal_repo_bootstrap_max_bytes"]
    footprint = measure_context_footprint(ROOT, ["ENTRYPOINT.md", "CURRENT_PROTOCOL.json"])

    assert footprint.paths == ("ENTRYPOINT.md", "CURRENT_PROTOCOL.json")
    assert footprint.file_count == 2
    assert footprint.utf8_bytes > 0
    assert footprint.approximate_tokens > 0
    assert footprint_within_budget(footprint, max_utf8_bytes=budget)


def test_account_routing_hook_and_universal_skill_have_measured_budgets():
    architecture = contract()
    footprint_contract = architecture["context_footprint"]
    skill_budget = architecture["required_layers"]["skill"]["target_max_bytes"]

    startup = measure_context_footprint(ROOT, ["STARTUP_HOOK.md"])
    skill = measure_context_footprint(ROOT, ["skills/universal-continuity/SKILL.md"])

    assert footprint_within_budget(
        startup,
        max_utf8_bytes=footprint_contract["universal_hot_path_budgets"]["startup_hook_max_bytes"],
    )
    assert footprint_within_budget(skill, max_utf8_bytes=skill_budget)


def test_context_measurement_contract_does_not_claim_exact_tokenization():
    footprint_contract = contract()["context_footprint"]
    assert footprint_contract["runtime"] == "runtime/context_footprint.py"
    assert footprint_contract["token_measurement"] == "APPROXIMATE_ONLY__UTF8_BYTES_DIVIDED_BY_4"
    assert footprint_contract["exact_model_token_count_claimed"] is False
    assert footprint_contract["efficiency_claim_requires_measurement"] is True
