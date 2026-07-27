from __future__ import annotations

from ai_workspace.domain.budget import Budget, BudgetDecision
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine
from ai_workspace.interfaces.engine_adapter import CostEstimate


class InMemoryBudgetPolicyEngine(BudgetPolicyEngine):
    """생성 시 주어진 단일 `Budget`으로 `CostEstimate`를 검사하는 최소
    구현체(M15-T01). `budget=None`이면 예산이 아예 설정되지 않은 것으로
    보고 항상 허용한다(정책 부재는 정상 상태, `LLMPolicyEngine`과 동일한
    하위 호환 원칙)."""

    def __init__(self, budget: Budget | None = None) -> None:
        self._budget = budget

    def check(self, estimate: CostEstimate) -> BudgetDecision:
        if self._budget is None:
            return BudgetDecision(allowed=True)

        if (
            self._budget.max_tokens is not None
            and estimate.estimated_tokens > self._budget.max_tokens
        ):
            return BudgetDecision(
                allowed=False,
                reason=(
                    f"estimated_tokens({estimate.estimated_tokens}) exceeds "
                    f"max_tokens({self._budget.max_tokens})"
                ),
            )

        if (
            self._budget.max_cost_usd is not None
            and estimate.estimated_cost_usd > self._budget.max_cost_usd
        ):
            return BudgetDecision(
                allowed=False,
                reason=(
                    f"estimated_cost_usd({estimate.estimated_cost_usd}) exceeds "
                    f"max_cost_usd({self._budget.max_cost_usd})"
                ),
            )

        return BudgetDecision(allowed=True)
