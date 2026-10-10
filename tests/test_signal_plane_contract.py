import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_signal_plane_is_non_authoritative_and_monitorable():
    contract = json.loads((ROOT / "CONTROL_SIGNAL_CONTRACT.json").read_text(encoding="utf-8"))
    doc = (ROOT / "SIGNAL_PLANE.md").read_text(encoding="utf-8")

    assert contract["transport"]["issue_is_authority"] is False
    assert contract["writers"]["stale_chat_may_emit_signal"] is True
    assert contract["writers"]["signal_emitter_may_mutate_authoritative_task_state_without_lease"] is False
    assert "[CONTROL_SIGNAL]" in doc
    assert "does not mutate authoritative task or business state" in doc
    assert "OWNER_ARCHITECTURE_OBSERVATIONS.json" in doc
