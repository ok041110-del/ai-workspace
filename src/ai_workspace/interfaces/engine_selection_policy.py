from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.engine_selection import EngineCandidate, EngineSelectionDecision
from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine


class EngineSelectionPolicy(ABC):
    """Task + 후보 목록 + Budget(선택) + Project Knowledge(선택)를 종합해
    최적 Engine 후보를 판단하는 계약(M17-T02, "Decision Only" —
    실제 실행과 연결하는 것은 M18의 책임). `LLMPolicyEngine`/
    `BudgetPolicyEngine`과 동일한 설계 원칙을 따른다 — 규칙 기반,
    side-effect 없음, LLM을 호출하지 않는다.

    후보가 어디서 왔는지(`EngineRegistry`)는 이 계약이 알지 못한다 —
    이미 조회된 `EngineCandidate` 목록만 받아 판단만 한다(SRP: 조회는
    `EngineRegistry`, 판단은 `EngineSelectionPolicy`)."""

    @abstractmethod
    def select(
        self,
        task: Task,
        candidates: list[EngineCandidate],
        *,
        budget_policy_engine: BudgetPolicyEngine | None = None,
        knowledge: list[KnowledgeDocument] | None = None,
    ) -> EngineSelectionDecision | None:
        """
        입력: task (선택 대상 Task), candidates (판단 대상 후보 목록),
              budget_policy_engine (선택, 주어지면 각 후보의 예상 비용을
              예산과 대조해 초과 후보를 제외), knowledge (선택, 결정
              사유에 참고 정보로만 반영 — 이번 MVP는 Knowledge로 후보
              자체를 걸러내지 않는다)
        출력: 선택된 EngineSelectionDecision(reason 포함), 후보가
              없거나(candidates가 빈 리스트) 예산 내 후보가 하나도
              없으면 None
        예외: 없음
        보장: side-effect 없음(read-only, LLM을 호출하지 않는다).
        """
        raise NotImplementedError
