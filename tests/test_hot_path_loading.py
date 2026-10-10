from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_entrypoint_is_small_event_driven_kernel():
    path = ROOT / "ENTRYPOINT.md"
    text = path.read_text(encoding="utf-8")

    assert path.stat().st_size <= 8192
    assert "## Minimal bootstrap invariant" in text
    assert "Every Continuity bootstrap begins with only" in text
    assert "`ENTRYPOINT.md`;" in text
    assert "`CURRENT_PROTOCOL.json`." in text
    assert "## Event-driven authority loading" in text
    assert "Methodology profiles are conditional contracts" in text
    assert "Read next:" not in text


def test_startup_hook_is_routing_only_and_budgeted():
    path = ROOT / "STARTUP_HOOK.md"
    text = path.read_text(encoding="utf-8")

    assert path.stat().st_size <= 8192
    assert "启动时不要机械预读整个仓库" in text
    assert "`ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`" in text
    assert "Event-driven authority loading" in text
    assert "SYSTEM_BLUEPRINT.md" in text
    assert "cold-path" in text
    assert "只先读取" in text
    assert "先读取并严格遵循该仓库当前 `ENTRYPOINT.md`、`SYSTEM_BLUEPRINT.md`、`CURRENT_PROTOCOL.json`、`STARTUP_HOOK.md`" not in text


def test_methodology_profiles_are_conditional_not_fixed_bootstrap_payload():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    startup = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")

    for profile in ("artifact_io@1.0", "operational_hygiene@1.0", "evolution@1.0"):
        assert profile in entrypoint

    assert "只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时" in startup
    assert "Floating `latest` is forbidden" in entrypoint


def test_bootstrap_does_not_embed_detailed_methodology_receipt_algorithm():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "receipt-contract-1.3" not in entrypoint
    assert "independent hook-assessment verifier" not in entrypoint
    assert "runtime/methodology_conformance.py:evaluate_operational_methodology_conformance" in entrypoint
    assert "OWNER_ADAPTER_CONTRACT.json" in entrypoint
