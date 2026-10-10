from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_entrypoint_uses_minimal_bootstrap_and_event_driven_loading():
    text = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")

    assert "## Minimal bootstrap invariant" in text
    assert "Every Continuity bootstrap begins with only" in text
    assert "`ENTRYPOINT.md`;" in text
    assert "`CURRENT_PROTOCOL.json`." in text
    assert "## Event-driven authority loading matrix" in text
    assert "methodology profiles loaded only when their activation event occurs" in text
    assert "Read next:" not in text


def test_startup_hook_routes_without_preloading_control_plane():
    text = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")

    assert "启动时不要机械预读整个仓库" in text
    assert "`ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`" in text
    assert "Event-driven authority loading" in text
    assert "SYSTEM_BLUEPRINT.md" in text
    assert "cold-path" in text
    assert "先读取并严格遵循该仓库当前 `ENTRYPOINT.md`、`SYSTEM_BLUEPRINT.md`、`CURRENT_PROTOCOL.json`、`STARTUP_HOOK.md`" not in text


def test_methodology_profiles_are_conditional_not_fixed_bootstrap_payload():
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    startup = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")

    for profile in ("artifact_io@1.0", "operational_hygiene@1.0", "evolution@1.0"):
        assert profile in entrypoint

    assert "只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时" in startup
    assert "Floating `latest` is forbidden" in entrypoint
