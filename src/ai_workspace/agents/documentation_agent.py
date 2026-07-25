from __future__ import annotations

import uuid

from ai_workspace.agents.events import DOCUMENTATION_COMPLETED, REVIEW_COMPLETED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.interfaces.context_manager import ContextManager
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class DocumentationAgent:
    """`ReviewCompleted` Event를 구독해 문서화하고 `DocumentationCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06). 협업 체인의
    마지막 단계로, 완료 시 Context Manager로 Snapshot을 생성해 Memory를
    갱신한다(ARCHITECTURE.md §5 다이어그램의 마무리 단계)."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        engine_runtime: EngineRuntime,
        context_manager: ContextManager,
        workspace_session: WorkspaceSession,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._engine_runtime = engine_runtime
        self._context_manager = context_manager
        self._workspace_session = workspace_session
        self._session = agent_runtime.start_agent(
            AgentRole.DOCUMENTATION, frozenset({AgentCapability.DOCUMENTATION})
        )
        event_bus.subscribe(self._on_review_completed)

    def _on_review_completed(self, event: Event) -> None:
        if event.event_type != REVIEW_COMPLETED:
            return
        task_id = event.payload["task_id"]
        task = self._task_engine.get_task(task_id)
        self._engine_runtime.run(task)
        self._task_engine.transition(task, TaskStatus.DONE)
        self._context_manager.create_snapshot(self._workspace_session)
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=DOCUMENTATION_COMPLETED,
                payload={"task_id": task_id},
                source_agent_id=self._session.agent_id,
            )
        )
