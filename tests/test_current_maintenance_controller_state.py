import json
from pathlib import Path

from runtime.maintenance_controller import evaluate_maintenance_state


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_current_controller_state_is_declared_reachable_and_structurally_valid():
    agent_manifest = load("AGENT_MANIFEST.json")
    state_ref = agent_manifest["continuity"]["maintenance_controller_state_ref"]

    assert state_ref in agent_manifest["workflow"]["state_authority_refs"]
    assert (ROOT / state_ref).exists()

    state = load(state_ref)
    policy = load("SYSTEM_MAINTENANCE_POLICY.json")
    result = evaluate_maintenance_state(state, policy)

    assert result.status == "PASS", result.errors
    assert state["triage_outcome"] in {"NO_DEFECT", "INVESTIGATE", "CONFIRMED_DEFECT"}
    assert state["status"] in {"ACTIVE", "BLOCKED", "COMPLETE", "NO_DEFECT_CLOSED"}


def test_current_controller_state_cannot_silently_claim_complete_without_complete_trace():
    agent_manifest = load("AGENT_MANIFEST.json")
    state = load(agent_manifest["continuity"]["maintenance_controller_state_ref"])
    policy = load("SYSTEM_MAINTENANCE_POLICY.json")

    if state["status"] == "COMPLETE":
        result = evaluate_maintenance_state(state, policy, require_complete=True)
        assert result.status == "PASS", result.errors
        assert state["current_stage"] is None
