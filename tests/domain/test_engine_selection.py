from ai_workspace.domain.engine_selection import EngineCandidate, EngineSelectionDecision


def test_engine_candidate_holds_given_fields() -> None:
    candidate = EngineCandidate(
        engine_name="claude_code",
        capabilities=frozenset({"code_generation"}),
        estimated_tokens=100,
        estimated_cost_usd=0.01,
        supports_parallel=True,
    )

    assert candidate.engine_name == "claude_code"
    assert candidate.capabilities == frozenset({"code_generation"})
    assert candidate.estimated_tokens == 100
    assert candidate.estimated_cost_usd == 0.01
    assert candidate.supports_parallel is True


def test_engine_selection_decision_holds_given_fields() -> None:
    decision = EngineSelectionDecision(
        engine_name="claude_code", model=None, reason="예산 내 최저 비용"
    )

    assert decision.engine_name == "claude_code"
    assert decision.model is None
    assert decision.reason == "예산 내 최저 비용"
