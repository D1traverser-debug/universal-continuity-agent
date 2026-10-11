import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_owner_contract_defines_one_self_maintenance_evolution_loop():
    adapter = load_json("OWNER_ADAPTER_CONTRACT.json")
    shared = adapter["operational_hygiene_and_learning"]["unified_self_maintenance_evolution_loop"]

    assert shared["required"] is True
    assert shared["single_loop_instance_when_profiles_coactivate"] is True
    assert shared["owner_may_trigger_without_user_report"] is True
    assert shared["pre_patch_system_level_reframe_required"] is True
    assert shared["uncertain_solution_or_knowledge_gap_requires_learning_scout"] is True
    assert shared["post_validation_second_order_reframe_required"] is True
    assert shared["durable_pattern_distillation_required"] is True
    assert shared["propagate_method_and_invariant_not_business_truth"] is True
    assert shared["full_loop_on_every_business_turn"] is False

    signals = set(shared["material_signal_sources"])
    assert {
        "USER_CORRECTION_OR_BUG_REPORT",
        "ASSISTANT_DETECTED_DEFECT_OR_INEFFICIENCY",
        "CI_EVAL_OR_TRACE_REGRESSION",
        "ROUTING_OR_TOOL_NONUSE",
        "CONTEXT_OR_STATE_LOSS",
        "DUPLICATE_OR_SUPERSEDED_MECHANISM",
        "PERFORMANCE_OR_COMPLEXITY_REGRESSION",
    }.issubset(signals)


def test_operational_hygiene_and_evolution_are_profile_slices_not_competing_parent_loops():
    adapter = load_json("OWNER_ADAPTER_CONTRACT.json")
    coordination = adapter["methodology_composition"]["profile_coordination"]
    profiles = adapter["methodology_composition"]["profiles"]

    assert coordination["profiles_are_activation_and_evidence_slices_not_separate_parent_loops"] is True
    assert coordination["operational_hygiene_plus_evolution_coactivation_means_one_self_maintenance_evolution_loop"] is True
    assert coordination["coactivation_should_share_problem_impact_and_closure_context"] is True
    assert coordination["owner_specific_business_evidence_remains_owner_local"] is True

    assert profiles["operational_hygiene"]["semantics_owner"] == "SYSTEM_MAINTENANCE_POLICY.json"
    assert profiles["evolution"]["semantics_owner"] == "CONTINUOUS_LEARNING_POLICY.md"


def test_existing_maintenance_loop_already_contains_the_full_closed_loop_in_order():
    policy = load_json("SYSTEM_MAINTENANCE_POLICY.json")
    steps = policy["maintenance_loop"]

    expected_order = [
        "DETECT",
        "BUILD_FULL_SYSTEM_IMPACT_MAP",
        "DIAGNOSE_ROOT_CAUSE",
        "DECIDE_LEARNING_SCOUT_AND_DISTILL_RELEVANT_EVIDENCE",
        "CHALLENGE_INITIAL_SOLUTION_CANDIDATES",
        "RUN_ARCHITECTURE_PAYOFF_AND_DELETION_TEST",
        "PATCH_MINIMUM_AUTHORITY_SURFACE",
        "REMOVE_OR_DEMOTE_SUPERSEDED_MECHANISM",
        "RUN_OR_OBSERVE_VALIDATION",
        "RUN_CROSS_SUBSYSTEM_PROPAGATION_CHECK",
        "RUN_SECOND_ORDER_CHALLENGE_AND_CLAIM_CALIBRATION",
        "DISTILL_ACCEPTED_LEARNING_AND_USER_CORRECTION",
        "REREAD_AUTHORITATIVE_STATE",
    ]
    positions = [steps.index(item) for item in expected_order]
    assert positions == sorted(positions)


def test_plausible_system_defect_hypothesis_is_triaged_before_ordinary_discussion():
    startup = (ROOT / "STARTUP_HOOK.md").read_text(encoding="utf-8")
    entrypoint = (ROOT / "ENTRYPOINT.md").read_text(encoding="utf-8")
    policy = load_json("SYSTEM_MAINTENANCE_POLICY.json")

    assert "defect triage" in startup
    assert "确认无问题则解释并停止" in startup
    assert "证据不足则继续核查" in startup
    assert "确认有问题则在同一轮进入维护/进化闭环" in startup
    assert "不得只把已确认缺陷描述成“未来风险”后结束" in startup

    assert "Plausible system-defect hypothesis" in entrypoint
    assert "triage before discussion" in entrypoint
    assert "`NO_DEFECT`, `INVESTIGATE`, or `CONFIRMED_DEFECT`" in entrypoint
    assert "Confirmed defects enter maintenance/evolution in the same turn" in entrypoint
    assert "never close them as an unowned “future risk”" in entrypoint

    assert policy["meta_maintenance_outline"]["stages"][0] == "M0_INTAKE_AND_SIGNAL_CLASSIFICATION"
    assert policy["default_autonomy"]["classify_user_feedback_before_adoption"] is True
    assert policy["default_autonomy"]["wait_for_user_to_notice_related_internal_followups"] is False


def test_learning_policy_is_an_input_to_maintenance_not_a_parallel_root_system():
    learning = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")
    assert "Learning is one input to maintenance" in learning
    assert "Raw learning evidence must never silently mutate owner business rules." in learning


def test_unified_loop_does_not_add_a_new_root_policy_or_supervisor_agent():
    assert not (ROOT / "SELF_MAINTENANCE_EVOLUTION_POLICY.json").exists()
    assert not (ROOT / "REFLECTION_AGENT_POLICY.json").exists()
