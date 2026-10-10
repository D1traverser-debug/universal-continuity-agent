import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_maintenance_policy_version_is_aligned_across_authority_and_status_surfaces():
    policy = load_json("SYSTEM_MAINTENANCE_POLICY.json")
    manifest = load_json("tasks/universal-continuity-maintenance/TASK_MANIFEST.json")
    harness = load_json("HARNESS_STATUS.json")

    expected = policy["schema_version"]
    assert manifest["system_maintenance_policy_version"] == expected
    assert harness["system_maintenance"]["policy_version"] == expected


def test_blueprint_exposes_meta_governance_as_narrow_verifier_not_independent_agent():
    blueprint = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")

    assert "runtime/meta_maintenance.py" in blueprint
    assert "narrow deterministic verifier" in blueprint
    assert "structured process conformance" in blueprint
    assert "does not prove the diagnosis" in blueprint
    assert "A new supervisory LLM Agent is not implied by meta-governance" in blueprint


def test_harness_records_meta_governance_assurance_ceiling_and_hot_path_boundary():
    harness = load_json("HARNESS_STATUS.json")
    meta = harness["meta_governance"]

    assert meta["runtime"] == "runtime/meta_maintenance.py"
    assert meta["authority"] == "SYSTEM_MAINTENANCE_POLICY.json"
    assert meta["assurance_ceiling"] == "STRUCTURED_PROCESS_CONFORMANCE_ONLY"
    assert meta["independent_semantic_review_proven"] is False
    assert meta["business_hot_path_preload_added"] is False
    assert meta["external_account_instruction_expansion_required"] is False
