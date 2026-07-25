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
