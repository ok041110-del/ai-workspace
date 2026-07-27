from ai_workspace.domain.budget import Budget
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.interfaces.engine_adapter import CostEstimate


def test_no_budget_always_allows() -> None:
    engine = InMemoryBudgetPolicyEngine(None)

    decision = engine.check(CostEstimate(estimated_tokens=1_000_000, estimated_cost_usd=1000.0))

    assert decision.allowed is True
    assert decision.reason is None


def test_within_budget_is_allowed() -> None:
    engine = InMemoryBudgetPolicyEngine(Budget(max_tokens=1000, max_cost_usd=1.0))

    decision = engine.check(CostEstimate(estimated_tokens=500, estimated_cost_usd=0.5))

    assert decision.allowed is True


def test_exceeding_max_tokens_is_denied_with_a_reason() -> None:
    engine = InMemoryBudgetPolicyEngine(Budget(max_tokens=100))

    decision = engine.check(CostEstimate(estimated_tokens=101, estimated_cost_usd=0.0))

    assert decision.allowed is False
    assert decision.reason is not None


def test_exceeding_max_cost_usd_is_denied_with_a_reason() -> None:
    engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=1.0))

    decision = engine.check(CostEstimate(estimated_tokens=0, estimated_cost_usd=1.01))

    assert decision.allowed is False
    assert decision.reason is not None


def test_partial_budget_only_checks_the_given_field() -> None:
    engine = InMemoryBudgetPolicyEngine(Budget(max_tokens=100))

    decision = engine.check(CostEstimate(estimated_tokens=50, estimated_cost_usd=999.0))

    assert decision.allowed is True
