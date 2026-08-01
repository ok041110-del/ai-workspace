from __future__ import annotations

from ai_workspace.domain.agent import Agent, AgentCapability
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler


def find_agent_by_capability(
    agent_registry: AgentRegistry, agent_scheduler: AgentScheduler, capability: AgentCapability
) -> Agent | None:
    """현재 활성 Agent 중 주어진 Capability를 가진 Agent를 Scheduler로
    선택한다(ARCHITECTURE.md §3.4, T2-06). 파이프라인 구성 시 해당 능력을
    가진 Agent가 실제로 등록되어 있는지 확인하는 데 쓰인다."""
    candidates = agent_registry.list_active()
    selected = agent_scheduler.select(candidates, capability, max_count=1)
    return selected[0] if selected else None


def is_agent_selected(
    agent_registry: AgentRegistry,
    agent_scheduler: AgentScheduler,
    capability: AgentCapability,
    agent_id: str,
    max_parallel: int = 1,
) -> bool:
    """같은 Capability를 가진 Agent가 여러 개 등록돼 있을 때, `agent_id`가
    이번에 Scheduler에게 선택된 Agent인지 판별한다(Milestone 13). 여러
    Agent 인스턴스가 각자 이 함수를 같은 `agent_registry`/`agent_scheduler`
    로 호출하면, `AgentScheduler.select()`가 결정적이라는 전제 하에 전부
    같은 결론에 도달한다 — 별도의 중앙 디스패처 없이도 "선택되지 않은
    Agent는 개입하지 않는다"를 각 Agent 스스로 보장할 수 있다.

    **병렬 실행(Milestone 58)**: `max_parallel`(기본값 1)을 Scheduler의
    `max_count`로 그대로 전달한다. 기본값 1이면 M13과 완전히 동일하게
    "선택된 것 하나만 True"이지만, 2 이상을 주면 우선순위 상위
    `max_parallel`개 안에 든 Agent는 전부 True를 얻어 같은 Event를
    동시에 처리할 수 있다 — 새로운 조율 메커니즘 없이 각 인스턴스가
    같은 질문("나는 이번에 뽑힌 N개 중 하나인가")에 각자 답하는 것만으로
    충분하다."""
    selected = agent_scheduler.select(agent_registry.list_active(), capability, max_parallel)
    return any(agent.agent_id == agent_id for agent in selected)
