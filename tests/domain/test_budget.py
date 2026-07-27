from ai_workspace.domain.budget import Budget, BudgetDecision


def test_budget_defaults_to_no_limits() -> None:
    budget = Budget()

    assert budget.max_tokens is None
    assert budget.max_cost_usd is None


def test_budget_holds_given_limits() -> None:
    budget = Budget(max_tokens=1000, max_cost_usd=1.5)

    assert budget.max_tokens == 1000
    assert budget.max_cost_usd == 1.5


def test_budget_decision_defaults_to_no_reason() -> None:
    decision = BudgetDecision(allowed=True)

    assert decision.allowed is True
    assert decision.reason is None


def test_budget_decision_can_carry_a_reason() -> None:
    decision = BudgetDecision(allowed=False, reason="over budget")

    assert decision.allowed is False
    assert decision.reason == "over budget"
