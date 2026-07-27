from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.budget import BudgetDecision
from ai_workspace.interfaces.engine_adapter import CostEstimate


class BudgetPolicyEngine(ABC):
    """`CostEstimate`(Task를 실행하기 전 `EngineAdapter.estimate_cost()`가
    계산한 예상 비용)를 Workspace의 예산 정책과 대조해 실행 허용 여부를
    결정하는 계약(M15-T01). `LLMPolicyEngine`(M5-T01)과 동일한 설계
    원칙을 따른다 — 규칙의 출처(YAML 등)는 이 계약이 알지 못하고, 예산이
    설정되지 않은 경우는 예외가 아니라 "항상 허용"으로 표현해 정책 부재가
    호출자의 실패로 이어지지 않게 한다.

    Provider 독립: 이 계약은 어떤 LLM Provider나 Engine을 다루는지 전혀
    알지 못한다 — `CostEstimate`만 입력으로 받는다."""

    @abstractmethod
    def check(self, estimate: CostEstimate) -> BudgetDecision:
        """
        입력: estimate (실행하려는 Task의 `EngineAdapter.estimate_cost()`
              결과)
        출력: BudgetDecision(allowed, reason) — 예산 내면 allowed=True,
              초과하면 allowed=False와 사람이 읽을 수 있는 reason
        예외: 없음
        보장: side-effect 없음(read-only). 예산 소비를 기록하거나 누적
              추적하지 않는다 — 매 호출은 주어진 estimate 하나만 독립적으로
              평가한다.
        """
        raise NotImplementedError
