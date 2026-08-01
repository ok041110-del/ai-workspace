from __future__ import annotations

from ai_workspace.domain.agent import Agent, AgentCapability, AgentStatus
from ai_workspace.interfaces.agent_scheduler import AgentScheduler

_UNAVAILABLE_STATUSES = frozenset({AgentStatus.STOPPED, AgentStatus.ERROR})


class InMemoryAgentScheduler(AgentScheduler):
    """Capability·가용성·우선순위 기준으로 실행할 Agent를 선택하는
    구현체(ARCHITECTURE.md §3.4, T2-02; 우선순위/가용성 고도화는
    Milestone 57-T03, ADR-0075).

    **가용성(M57)**: `AgentStatus.STOPPED`/`ERROR`만 제외하고 나머지
    (IDLE/RUNNING/WAITING/PAUSED)는 모두 선택 대상이다. 이 저장소에는
    두 가지 서로 다른 Agent 생성 경로가 공존한다 — 도메인 기본값
    그대로 두는 단위 테스트(IDLE 기본값)와 `AgentRuntime.
    start_agent()`로 등록돼 즉시 RUNNING이 되는 실제 실행 경로(M13/
    M56) — 어느 한쪽만 가용으로 보면 다른 쪽이 전부 걸러져 Scheduler
    가 빈 리스트를 반환하는 회귀가 생긴다. STOPPED/ERROR만 명확히
    "더 이상 일할 수 없는" 상태이므로 그것만 제외한다.

    **우선순위(M57)**: `Agent.priority`(낮을수록 우선)로 안정
    정렬한다 — 동점(기본값 0)이면 `candidates` 원래 순서를 그대로
    보존해 M13/M56이 검증한 "첫 매치" 동작과 100% 동일하다."""

    def select(
        self, candidates: list[Agent], capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        matched = [
            agent
            for agent in candidates
            if capability in agent.capabilities and agent.status not in _UNAVAILABLE_STATUSES
        ]
        ordered = sorted(matched, key=lambda agent: agent.priority)
        return ordered[:max_count]
