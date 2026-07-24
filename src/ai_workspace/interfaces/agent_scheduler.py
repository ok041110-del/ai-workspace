from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent, AgentCapability


class AgentScheduler(ABC):
    """Capability 기준으로 실행할 Agent를 선택하는 계약. ARCHITECTURE.md §3.4
    Agent Scheduler. Role이 아닌 Capability 기준으로 선택함으로써, 하나의
    Role이 여러 Capability를 가지거나 여러 Role이 동일한 Capability를 공유하는
    경우에도 대응한다."""

    @abstractmethod
    def select(
        self, candidates: list[Agent], capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        """
        입력: candidates (선택 대상 Agent 목록), capability (요구되는
              Capability), max_count (최대 선택 개수, 기본값 1)
        출력: capability를 가진 Agent 중 우선순위에 따라 선택된 최대
              max_count개 (없으면 빈 리스트)
        예외: 없음 (조건에 맞는 Agent가 없으면 빈 리스트를 반환한다)
        보장: 반환된 리스트의 모든 Agent는 candidates에 포함되어 있었고
              capability in agent.capabilities 를 만족한다. 반환된 리스트의
              길이는 max_count를 넘지 않는다.
        """
        raise NotImplementedError
