from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from runtime.agent_architecture import (
    ArchitectureStatus,
    validate_agent_manifest,
    validate_architecture_observation,
    validate_registry_architecture_pointers,
)
from runtime.owner_topology import business_owner_names


def _load_json(root: Path, relative: str) -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _snapshot(root: Path) -> tuple[set[str], dict[str, int]]:
    paths: set[str] = set()
    sizes: dict[str, int] = {}
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        paths.add(relative)
        try:
            sizes[relative] = path.stat().st_size
        except OSError:
            pass
    return paths, sizes


def audit_agent_architecture(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    contract = _load_json(root, "AGENT_ARCHITECTURE_CONTRACT.json")
    registry = _load_json(root, "OWNER_REGISTRY.json")
    universal_manifest = _load_json(root, "AGENT_MANIFEST.json")
    observations = _load_json(root, "OWNER_ARCHITECTURE_OBSERVATIONS.json")
    paths, sizes = _snapshot(root)

    universal = validate_agent_manifest(
        universal_manifest,
        contract,
        repository_paths=paths,
        file_sizes=sizes,
    )
    errors.extend(f"UNIVERSAL:{item}" for item in universal.errors)
    warnings.extend(f"UNIVERSAL:{item}" for item in universal.warnings)

    pointers = validate_registry_architecture_pointers(registry)
    errors.extend(f"REGISTRY:{item}" for item in pointers.errors)
    warnings.extend(f"REGISTRY:{item}" for item in pointers.warnings)

    expected = set(business_owner_names(registry))
    observed_rows = {
        row.get("owner"): row
        for row in observations.get("owners", [])
        if isinstance(row, dict) and row.get("owner")
    }
    if set(observed_rows) != expected:
        errors.append("OBSERVATIONS:owner set does not match current BUSINESS topology")

    for owner in sorted(expected.intersection(observed_rows)):
        row = observed_rows[owner]
        observed_head = str(row.get("observed_owner_head", "")).strip()
        if not observed_head:
            errors.append(f"OBSERVATIONS:{owner}:missing observed_owner_head")
            continue
        result = validate_architecture_observation(row, observed_owner_head=observed_head)
        errors.extend(f"OBSERVATIONS:{owner}:{item}" for item in result.errors)
        warnings.extend(f"OBSERVATIONS:{owner}:{item}" for item in result.warnings)
        manifest_ref = str(row.get("agent_manifest_ref", "")).strip()
        registry_ref = next(
            (
                str(entry.get("agent_manifest_ref", "")).strip()
                for entry in registry.get("owners", [])
                if isinstance(entry, dict) and entry.get("name") == owner
            ),
            "",
        )
        if manifest_ref != registry_ref:
            errors.append(f"OBSERVATIONS:{owner}:agent_manifest_ref differs from OWNER_REGISTRY")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "universal_architecture_status": universal.status.value,
        "checked_business_owners": sorted(expected),
        "assurance_ceiling": "STRUCTURAL_ARCHITECTURE_AND_RECORDED_OBSERVATION_CONFORMANCE_ONLY",
        "remote_freshness_boundary": (
            "Local CI validates the recorded observation set and its internal head binding. "
            "It cannot discover a newer private owner HEAD by itself; the remote monitor/maintenance runner must refresh observations."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = audit_agent_architecture(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
