from __future__ import annotations

import uuid

from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class PlanningAgent:
    """Mission을 Task로 계획하고 `MissionPlanned` Event를 발행하는 Agent
    (ARCHITECTURE.md §3.6, §5, T2-06). 파이프라인의 진입점 — 외부에서
    `plan_mission()`을 호출해 협업 체인을 시작시킨다."""

    def __init__(
        self, *, agent_runtime: AgentRuntime, event_bus: EventBus, task_engine: TaskEngine
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._session = agent_runtime.start_agent(
            AgentRole.PLANNER, frozenset({AgentCapability.PLANNING})
        )

    def plan_mission(self, project_id: str, title: str) -> Task:
        task = self._task_engine.create_task(project_id, title)
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=MISSION_PLANNED,
                payload={"task_id": task.task_id},
                source_agent_id=self._session.agent_id,
            )
        )
        return task
