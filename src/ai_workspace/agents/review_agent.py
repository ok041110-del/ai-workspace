from __future__ import annotations

import uuid
from dataclasses import replace

from ai_workspace.agents.events import CODE_COMPLETED, REVIEW_COMPLETED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.development_context import DevelopmentContext
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class ReviewAgent:
    """`CodeCompleted` Event를 구독해 Task를 검토하고 `ReviewCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06).

    `CodeCompleted` payload의 `output`을 `DevelopmentContext.prior_output`
    으로 받아 실제로 무엇을 검토해야 하는지 알고 실행한다(M5-T03) — 이전에는
    `CodingAgent`의 산출물을 전혀 모른 채 같은 Task 제목만 다시 실행했다."""

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
            AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW})
        )
        event_bus.subscribe(self._on_code_completed)

    def _on_code_completed(self, event: Event) -> None:
        if event.event_type != CODE_COMPLETED:
            return
        task_id = event.payload["task_id"]
        task = self._task_engine.get_task(task_id)
        context = DevelopmentContext(
            task_id=task_id,
            instructions=task.title,
            prior_output=event.payload.get("output"),
        )
        result = self._engine_runtime.run(replace(task, title=context.to_prompt()))
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=REVIEW_COMPLETED,
                payload={"task_id": task_id, "output": result.output, "success": result.success},
                source_agent_id=self._session.agent_id,
            )
        )
