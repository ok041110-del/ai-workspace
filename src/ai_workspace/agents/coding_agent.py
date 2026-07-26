from __future__ import annotations

import uuid
from dataclasses import replace

from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.development_context import DevelopmentContext
from ai_workspace.domain.llm_policy import required_capabilities
from ai_workspace.domain.task import TaskStatus
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class CodingAgent:
    """`MissionPlanned` Event를 구독해 Task를 구현하고 `CodeCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06). 실제 실행은
    Engine Runtime(Mock EngineAdapter)에 위임한다.

    `DevelopmentContext`(M5-T03)로 실행 지시를 조립해 Engine에 넘긴다 —
    원본 `Task`의 `title`은 그대로 두고, Engine 호출에만 쓰이는 사본의
    `title`을 조립된 프롬프트로 치환한다(`EngineAdapter.run()` 계약은
    그대로 유지). `MissionPlanned` payload에 `rework_reason`이 있으면
    (M5-T06, `CoordinatorAgent`가 테스트 실패 후 재발행한 경우)
    `DevelopmentContext.prior_output`으로 반영해 이전에 무엇이 실패했는지
    알고 재작업한다.

    **Policy→Execution 라우팅(M6-T02)**: `AgentSession.llm_policy_decision`
    (M5-T02)을 `required_capabilities()`로 변환해 `engine_runtime.run()`에
    전달한다 — 여러 `EngineAdapter`가 등록되어 있으면(M6-T01) 실제로 이
    Role에 배정된 Provider의 Adapter가 선택되어 실행된다. 정책이 없으면
    빈 집합이 되어 기존 동작(제약 없음)과 하위 호환된다."""

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
        context = DevelopmentContext(
            task_id=task_id,
            instructions=task.title,
            prior_output=event.payload.get("rework_reason"),
        )
        result = self._engine_runtime.run(
            replace(task, title=context.to_prompt()),
            required_capabilities=required_capabilities(self._session.llm_policy_decision),
        )
        self._task_engine.transition(task, TaskStatus.REVIEW)
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=CODE_COMPLETED,
                payload={"task_id": task_id, "output": result.output, "success": result.success},
                source_agent_id=self._session.agent_id,
            )
        )
