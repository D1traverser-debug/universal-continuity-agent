from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_continuous_learning_requires_operational_proactive_scouting():
    text = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "## Operational scout loop" in text
    assert "not operational evidence" in text
    assert "disabled recurring scout" in text
    assert "stale hard-coded protocol version" in text
    assert "only after the user supplies a candidate" in text

    for lane in (
        "first-party OpenAI Skills/Agents/product documentation",
        "`skills.sh` All Time, Trending and Hot",
        "GitHub Agent Skills",
        "MCP/tool catalogs",
        "ChatGPT Plugin Directory",
        "novelty lane",
    ):
        assert lane in text


def test_learning_candidates_have_deep_dive_and_promotion_boundaries():
    text = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    for status in (
        "REJECT_DUPLICATE",
        "MONITOR",
        "DEEP_DIVE",
        "UNIVERSAL_CANDIDATE",
        "OWNER_LOCAL_CANDIDATE",
    ):
        assert status in text

    assert "README, marketplace description, leaderboard entry" in text
    assert "delegated runtime/implementation" in text
    assert "tests/evals/workflows" in text
    assert "issue/failure evidence" in text
    assert "do not mutate production authority by themselves" in text


def test_learning_stays_bounded_and_inherits_without_prompt_copying():
    text = (ROOT / "CONTINUOUS_LEARNING_POLICY.md").read_text(encoding="utf-8")

    assert "no more than five unresolved deep dives" in text
    assert "Research remains cold-path evidence" in text
    assert "`evolution@1.0` semantics and owner hook bindings" in text
    assert "Owner-local candidates remain owner-local" in text
    assert "Do not copy shared prose into every child owner" in text
