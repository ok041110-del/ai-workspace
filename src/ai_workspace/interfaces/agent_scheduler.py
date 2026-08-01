from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.agent import Agent, AgentCapability


class AgentScheduler(ABC):
    """Capability·가용성·우선순위 기준으로 실행할 Agent를 선택하는
    계약. ARCHITECTURE.md §3.4 Agent Scheduler. Role이 아닌 Capability
    기준으로 선택함으로써, 하나의 Role이 여러 Capability를 가지거나
    여러 Role이 동일한 Capability를 공유하는 경우에도 대응한다.

    **가용성·우선순위(Milestone 57, ADR-0075)**: 구현체는 `agent.
    status`가 가용 상태(구현체가 정의)가 아닌 Agent를 후보에서
    제외하고, 남은 후보를 `agent.priority`(낮을수록 우선)로 정렬해야
    한다. `InMemoryAgentScheduler`는 `AgentStatus.STOPPED`/`ERROR`만
    불가용으로 정의한다 — 이 저장소에 공존하는 두 Agent 생성 경로
    (도메인 기본값 IDLE인 단위 테스트, `AgentRuntime.start_agent()`
    로 RUNNING이 되는 실제 실행 경로) 어느 쪽도 걸러지지 않도록
    "더 이상 일할 수 없는" 상태만 제외한다."""

    @abstractmethod
    def select(
        self, candidates: list[Agent], capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        """
        입력: candidates (선택 대상 Agent 목록), capability (요구되는
              Capability), max_count (최대 선택 개수, 기본값 1)
        출력: capability를 가지고 가용 상태인 Agent 중 우선순위에
              따라 선택된 최대 max_count개(없으면 빈 리스트)
        예외: 없음 (조건에 맞는 Agent가 없으면 빈 리스트를 반환한다)
        보장: 반환된 리스트의 모든 Agent는 candidates에 포함되어 있었고
              capability in agent.capabilities 를 만족한다. 반환된 리스트의
              길이는 max_count를 넘지 않는다.
        """
        raise NotImplementedError
