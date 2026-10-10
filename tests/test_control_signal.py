from runtime.control_signal import validate_control_signal


def signal() -> dict:
    return {
        "signal_id": "sig-1",
        "signal_type": "AGENT_ARCHITECTURE_DRIFT",
        "source": "stale-chat",
        "observed_at": "2026-10-11T00:00:00Z",
        "subject": "FINANCIAL_WRITING_AGENT_RUNTIME",
        "summary": "Skill exceeded router budget",
        "evidence_refs": ["repo://financial/SKILL.md"],
        "severity": "MEDIUM",
        "authoritative_state_mutation": False,
    }


def test_valid_signal_is_non_authoritative():
    result = validate_control_signal(signal())
    assert result.valid is True
    assert result.errors == ()


def test_signal_cannot_claim_state_mutation():
    payload = signal()
    payload["authoritative_state_mutation"] = True
    result = validate_control_signal(payload)
    assert result.valid is False
    assert "control signal cannot claim authoritative_state_mutation" in result.errors


def test_signal_requires_real_evidence_refs():
    payload = signal()
    payload["evidence_refs"] = []
    result = validate_control_signal(payload)
    assert result.valid is False
    assert "evidence_refs must be a non-empty string list" in result.errors
