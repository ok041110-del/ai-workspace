from __future__ import annotations

import uuid
from dataclasses import replace

from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.agents.scheduling import is_agent_selected
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.development_context import DevelopmentContext
from ai_workspace.domain.llm_policy import model_name, required_capabilities
from ai_workspace.domain.task import TaskStatus
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
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
    빈 집합이 되어 기존 동작(제약 없음)과 하위 호환된다. **Model 라우팅
    (M14-T03)**: 같은 `llm_policy_decision`을 `model_name()`으로 변환해
    함께 전달한다 — `ClaudeCodeEngineAdapter`가 실제 `--model` 실행
    인자에 반영한다(M14-T02). 정책이 없으면 `None`이 되어 각 Adapter의
    기본 모델을 그대로 쓴다.

    **Multi-Agent Collaboration(M13)**: `agent_registry`/`agent_scheduler`
    를 둘 다 주입하면, 같은 CODING Capability를 가진 다른 `CodingAgent`
    인스턴스가 함께 등록돼 있어도 `AgentScheduler`가 선택한 인스턴스만
    실제로 처리한다(`is_agent_selected()`로 자가 확인). 새로운 중앙
    디스패처는 없다 — 선택이 결정적이라는 전제 하에 모든 인스턴스가
    같은 질문에 같은 답을 얻는다. 둘 중 하나라도 주어지지 않으면(기본값
    `None`) 이 확인을 건너뛰어 기존 동작과 완전히 동일하다."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        engine_runtime: EngineRuntime,
        agent_registry: AgentRegistry | None = None,
        agent_scheduler: AgentScheduler | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._engine_runtime = engine_runtime
        self._agent_registry = agent_registry
        self._agent_scheduler = agent_scheduler
        self._session = agent_runtime.start_agent(
            AgentRole.CODING, frozenset({AgentCapability.CODING})
        )
        event_bus.subscribe(self._on_mission_planned)

    def _on_mission_planned(self, event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        if self._agent_registry is not None and self._agent_scheduler is not None:
            if not is_agent_selected(
                self._agent_registry,
                self._agent_scheduler,
                AgentCapability.CODING,
                self._session.agent_id,
            ):
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
            model=model_name(self._session.llm_policy_decision),
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
