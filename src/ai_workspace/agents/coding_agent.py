from __future__ import annotations

import uuid

from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.task import TaskStatus
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class CodingAgent:
    """`MissionPlanned` Event를 구독해 Task를 구현하고 `CodeCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06). 실제 실행은
    Engine Runtime(Mock EngineAdapter)에 위임한다."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        engine_runtime: EngineRuntime,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._engine_runtime = engine_runtime
        self._session = agent_runtime.start_agent(
            AgentRole.CODING, frozenset({AgentCapability.CODING})
        )
        event_bus.subscribe(self._on_mission_planned)

    def _on_mission_planned(self, event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        task_id = event.payload["task_id"]
        task = self._task_engine.get_task(task_id)
        self._task_engine.transition(task, TaskStatus.IN_PROGRESS)
        self._engine_runtime.run(task)
        self._task_engine.transition(task, TaskStatus.REVIEW)
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=CODE_COMPLETED,
                payload={"task_id": task_id},
                source_agent_id=self._session.agent_id,
            )
        )
