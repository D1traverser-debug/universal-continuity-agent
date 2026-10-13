from runtime.control_signal import (
    SignalLifecycleState,
    WorkAdmissionState,
    assess_signal_admission,
    current_remediation_allowed,
    validate_agent_ready_brief,
    validate_control_signal,
)


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


def brief() -> dict:
    return {
        "behavior": "Owner router exceeds the shared hot-path budget.",
        "current_state": "Detailed business rules are duplicated in the Skill.",
        "desired_state": "Skill routes to canonical runtime/references while hard boundaries remain compact.",
        "stable_interfaces": ["continuity/AGENT_MANIFEST.json", "skills/financial-writing-agent/SKILL.md"],
        "acceptance_criteria": ["Skill is within the shared byte budget", "owner CI remains green"],
        "out_of_scope": ["business article state", "writer lease"],
        "evidence_refs": ["repo://financial/SKILL.md", "ci://owner"],
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


def test_signal_lifecycle_accepts_active_historical_open_and_resolved_only():
    for state in ("ACTIVE", "HISTORICAL_OPEN", "RESOLVED"):
        payload = signal()
        payload["lifecycle_state"] = state
        assert validate_control_signal(payload).valid is True

    payload = signal()
    payload["lifecycle_state"] = "OPEN"
    result = validate_control_signal(payload)
    assert result.valid is False
    assert "lifecycle_state is invalid" in result.errors


def test_historical_open_and_resolved_cannot_drive_current_remediation():
    assert current_remediation_allowed(
        lifecycle_state=SignalLifecycleState.HISTORICAL_OPEN,
        reobserved_current_condition=True,
        current_authorization=True,
    ) is False
    assert current_remediation_allowed(
        lifecycle_state=SignalLifecycleState.RESOLVED,
        reobserved_current_condition=True,
        current_authorization=True,
    ) is False
    assert current_remediation_allowed(
        lifecycle_state=SignalLifecycleState.ACTIVE,
        reobserved_current_condition=False,
        current_authorization=True,
    ) is False
    assert current_remediation_allowed(
        lifecycle_state=SignalLifecycleState.ACTIVE,
        reobserved_current_condition=True,
        current_authorization=False,
    ) is False
    assert current_remediation_allowed(
        lifecycle_state=SignalLifecycleState.ACTIVE,
        reobserved_current_condition=True,
        current_authorization=True,
    ) is True


def test_signal_must_be_reobserved_before_clarification_or_delegation():
    decision = assess_signal_admission(reobserved=False, actionable=True, agent_ready_brief=brief())
    assert decision.state == WorkAdmissionState.VERIFY_REQUIRED
    assert decision.user_interruption_required is False


def test_retrievable_fact_gap_is_system_work_not_user_question():
    decision = assess_signal_admission(
        reobserved=True,
        actionable=None,
        retrievable_fact_gaps=["current owner HEAD", "latest CI status"],
    )
    assert decision.state == WorkAdmissionState.FACT_GATHERING
    assert decision.user_interruption_required is False


def test_only_unavailable_information_or_human_judgment_interrupts_user():
    info = assess_signal_admission(
        reobserved=True,
        actionable=None,
        unavailable_fact_gaps=["private business constraint not recorded anywhere"],
    )
    judgment = assess_signal_admission(
        reobserved=True,
        actionable=True,
        human_judgment_required=True,
    )
    assert info.state == WorkAdmissionState.NEEDS_USER_INFORMATION
    assert info.user_interruption_required is True
    assert judgment.state == WorkAdmissionState.NEEDS_HUMAN_JUDGMENT
    assert judgment.user_interruption_required is True


def test_actionable_signal_requires_stable_agent_ready_brief_before_delegation():
    missing = assess_signal_admission(reobserved=True, actionable=True, agent_ready_brief=None)
    assert missing.state == WorkAdmissionState.BRIEF_REQUIRED
    assert missing.user_interruption_required is False

    ready = assess_signal_admission(reobserved=True, actionable=True, agent_ready_brief=brief())
    assert ready.state == WorkAdmissionState.READY_TO_DELEGATE
    assert ready.user_interruption_required is False


def test_agent_ready_brief_requires_behavior_state_interfaces_acceptance_and_evidence():
    payload = brief()
    payload["acceptance_criteria"] = []
    result = validate_agent_ready_brief(payload)
    assert result.valid is False
    assert "agent_ready_brief.acceptance_criteria must be a non-empty string list" in result.errors


def test_non_actionable_signal_can_close_without_user_interruption():
    decision = assess_signal_admission(reobserved=True, actionable=False)
    assert decision.state == WorkAdmissionState.NOT_ACTIONABLE
    assert decision.user_interruption_required is False
