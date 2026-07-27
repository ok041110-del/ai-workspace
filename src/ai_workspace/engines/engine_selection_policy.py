from __future__ import annotations

from ai_workspace.domain.engine_selection import EngineCandidate, EngineSelectionDecision
from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine
from ai_workspace.interfaces.engine_adapter import CostEstimate
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy


class InMemoryEngineSelectionPolicy(EngineSelectionPolicy):
    """예산 내 후보 중 예상 비용(`estimated_cost_usd`, 동률이면
    `estimated_tokens`)이 가장 낮은 후보를 선택하는 최소 규칙 기반
    구현체(M17-T02). `budget_policy_engine`이 주어지면 각 후보의
    `estimated_tokens`/`estimated_cost_usd`로 `CostEstimate`를 만들어
    `BudgetPolicyEngine.check()`에 그대로 위임한다 — 예산 비교 로직을
    중복 구현하지 않는다(M15 재사용, DRY)."""

    def select(
        self,
        task: Task,
        candidates: list[EngineCandidate],
        *,
        budget_policy_engine: BudgetPolicyEngine | None = None,
        knowledge: list[KnowledgeDocument] | None = None,
    ) -> EngineSelectionDecision | None:
        allowed = candidates
        if budget_policy_engine is not None:
            allowed = [
                candidate
                for candidate in candidates
                if budget_policy_engine.check(
                    CostEstimate(candidate.estimated_tokens, candidate.estimated_cost_usd)
                ).allowed
            ]
        if not allowed:
            return None

        def _rank(candidate: EngineCandidate) -> tuple[float, int]:
            return (candidate.estimated_cost_usd, candidate.estimated_tokens)

        best = min(allowed, key=_rank)
        reason = (
            f"예산 내 후보 중 예상 비용이 가장 낮음"
            f"(estimated_cost_usd={best.estimated_cost_usd}, "
            f"estimated_tokens={best.estimated_tokens})"
        )
        if knowledge:
            reason = f"{reason}, 관련 Knowledge {len(knowledge)}건 참고"
        return EngineSelectionDecision(engine_name=best.engine_name, model=None, reason=reason)
