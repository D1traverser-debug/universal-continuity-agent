import copy
import json
from pathlib import Path

from runtime.owner_topology import validate_owner_registry

ROOT = Path(__file__).resolve().parents[1]


def _registry() -> dict:
    return json.loads((ROOT / "OWNER_REGISTRY.json").read_text(encoding="utf-8"))


def test_current_owner_registry_contains_no_rebuildable_remote_observation_fields():
    registry = _registry()
    assert validate_owner_registry(registry) == ()
    for owner in registry["owners"]:
        assert not any(
            key.startswith("observed_") or key.startswith("architecture_validation_")
            for key in owner
        ), owner["name"]


def test_owner_registry_fails_closed_when_remote_observation_cache_is_embedded():
    registry = copy.deepcopy(_registry())
    owner = next(item for item in registry["owners"] if item["owner_kind"] == "BUSINESS")
    owner["observed_owner_head"] = "stale-head"
    owner["architecture_validation_result"] = "PASS"

    errors = validate_owner_registry(registry)

    assert any("observed_owner_head" in error for error in errors)
    assert any("architecture_validation_result" in error for error in errors)


def test_membership_authority_points_rebuildable_remote_observations_to_dedicated_cache():
    membership = _registry()["membership_authority"]
    assert membership["rebuildable_remote_observations_allowed"] is False
    assert membership["remote_observation_cache"] == "OWNER_ARCHITECTURE_OBSERVATIONS.json"
