import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_entrypoint_does_not_infer_a_tentative_user_proposal_as_a_decision():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")

    assert "Questions, suggestions, analogies, or tentative ideas are candidates, not authority." in entrypoint
    assert "Do not infer approval" in entrypoint
    assert "assess independently before acting unless explicitly instructed" in entrypoint


def test_material_universal_main_mutation_uses_head_level_cas_not_pr_first_by_default():
    policy = load_json("PROGRESS_OBSERVABILITY_POLICY.json")
    mutation = policy["authoritative_git_main_mutation"]

    assert mutation["default_workflow"] == "DIRECT_MAIN_WITH_HEAD_CAS"
    assert mutation["branch_protection_required_by_default"] is False
    assert mutation["pr_first_required_by_default"] is False

    preconditions = "\n".join(mutation["preconditions"])
    assert "current main HEAD" in preconditions
    assert "lease_id and resume_epoch" in preconditions
    assert "exact authority surfaces" in preconditions
    assert "MATERIAL_PATCH" in preconditions

    assert "parent is exactly the observed current main HEAD" in mutation["commit_model"]
    publish = mutation["publish_model"]
    assert publish["operation"] == "UPDATE_MAIN_REF_WITH_COMPARE_AND_SWAP"
    assert publish["force"] is False
    assert publish["expected_sha"] == "OBSERVED_CURRENT_MAIN_HEAD"

    mismatch = mutation["head_mismatch_behavior"]
    assert "Abort" in mismatch
    assert "reread current main HEAD" in mismatch
    assert "Never replay or force" in mismatch
    assert mutation["direct_contents_write_for_material_control_plane_change_when_head_cas_primitives_are_available"] is False

    postconditions = "\n".join(mutation["postconditions"])
    assert "reread main" in postconditions
    assert "CI/validation" in postconditions
    assert "before reporting COMMITTED" in postconditions
    assert "does not physically block an authorized external writer" in mutation["assurance_ceiling"]


def test_entrypoint_bootstrap_forbids_contents_api_for_material_main_when_head_cas_exists():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")

    assert "Material Universal `main`: when HEAD-CAS is available, Contents API material mutation is forbidden" in entrypoint
    assert "active lease + reread HEAD + commit-on-HEAD" in entrypoint
    assert "`expected_sha=HEAD`" in entrypoint
    assert "reread authority" in entrypoint
    assert "Details: `PROGRESS_OBSERVABILITY_POLICY.json`." in entrypoint


def test_blueprint_and_handoff_bind_the_single_writer_threat_model_without_stale_high_claim():
    blueprint = (ROOT / "SYSTEM_BLUEPRINT.md").read_text(encoding="utf-8")
    handoff = (ROOT / "tasks/universal-continuity-maintenance/HANDOFF.md").read_text(encoding="utf-8")

    assert "`SINGLE_ACTIVE_CHAT` writer model" in blueprint
    assert "observed-HEAD compare-and-swap" in blueprint
    assert "PR-first and branch protection are not default requirements" in blueprint
    assert "not evidence that unprotected `main` is itself a HIGH defect" in blueprint

    assert "Tool-level unbypassable enforcement — HIGH / OPEN" not in handoff
    assert "当前模型不是 PR-first" in handoff
    assert "active lease + observed-HEAD CAS + CI + authoritative reread" in handoff
    assert "没有 merge，也不是 authoritative implementation" in handoff
