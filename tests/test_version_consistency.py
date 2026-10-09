import json
import re
from pathlib import Path

from runtime.universal_continuity import SCHEMA_VERSION

ROOT = Path(__file__).resolve().parents[1]


def test_contract_runtime_package_and_entrypoint_versions_stay_aligned():
    contract = json.loads((ROOT / "CONTINUITY_CONTRACT.json").read_text(encoding="utf-8"))
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")

    version = contract["schema_version"]
    assert version == SCHEMA_VERSION
    assert f'version = "{version}.0"' in pyproject
    assert f"Contract: v{version}" in entrypoint
    assert re.search(rf"Protocol v{re.escape(version)}\b", protocol)
