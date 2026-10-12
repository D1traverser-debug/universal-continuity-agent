import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_entrypoint_has_lightweight_three_state_ingress_and_controller_boundary():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")

    assert "## Lightweight ingress triage" in entrypoint
    assert "`NO_DEFECT`" in entrypoint
    assert "`INVESTIGATE`" in entrypoint
    assert "`CONFIRMED_DEFECT`" in entrypoint
    assert "runtime/maintenance_controller.py" in entrypoint
    assert "forbids stage skipping" in entrypoint
    assert "material patching before implementation" in entrypoint
    assert "closure before all canonical stages" in entrypoint


def test_account_router_keeps_preflight_thin_but_routes_systemic_work_to_controller():
    startup = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")

    assert "defect-signal preflight" in startup
    assert "NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT" in startup
    assert "`NO_DEFECT` 正常走业务 owner" in startup
    assert "runtime/maintenance_controller.py" in startup
    assert "不得先 patch 再补大纲/记录" in startup


def test_agent_manifest_declares_controller_as_runtime_and_transition_guard():
    manifest = load("AGENT_MANIFEST.json")

    assert "runtime/maintenance_controller.py" in manifest["runtime"]["entrypoints"]
    assert "runtime/maintenance_controller.py" in manifest["workflow"]["transition_guard_refs"]
    assert "maintenance_controller" in manifest["harness"]["suites"]


def test_unified_ingress_does_not_make_full_maintenance_a_business_hot_path():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    startup = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")

    assert "do not load full maintenance" in entrypoint
    assert "`NO_DEFECT` 正常走业务 owner" in startup
    assert "NO_DEFECT" in entrypoint
