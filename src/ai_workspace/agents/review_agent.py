from __future__ import annotations

import uuid
from dataclasses import replace

from ai_workspace.agents.events import CODE_VERIFIED, REVIEW_COMPLETED
from ai_workspace.agents.scheduling import is_agent_selected
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.development_context import DevelopmentContext
from ai_workspace.domain.llm_policy import model_name, required_capabilities
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class ReviewAgent:
    """`CodeVerified` Event를 구독해 Task를 검토하고 `ReviewCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06).

    `CodeVerified` payload의 `output`을 `DevelopmentContext.prior_output`
    으로 받아 실제로 무엇을 검토해야 하는지 알고 실행한다(M5-T03) — 이전에는
    `CodingAgent`의 산출물을 전혀 모른 채 같은 Task 제목만 다시 실행했다.

    **트리거 변경(M5-T06)**: 이전에는 `CodeCompleted`를 직접 구독했지만,
    이제 `CoordinatorAgent`가 `ShellAgent`의 테스트 결과를 확인한 뒤
    발행하는 `CodeVerified`를 구독한다 — 테스트를 통과한 코드만 검토
    대상이 되도록 조건부 게이트를 통과시킨다.

    **Policy→Execution 라우팅(M6-T02)**: `CodingAgent`와 동일하게
    `AgentSession.llm_policy_decision`을 `required_capabilities()`로
    변환해 `engine_runtime.run()`에 전달한다. **Model 라우팅(M14-T03)**:
    같은 방식으로 `model_name()`도 함께 전달한다.

    **Multi-Agent Collaboration(M56, ADR-0074)**: `CodingAgent`(M13)와
    동일한 패턴 — `agent_registry`/`agent_scheduler`를 둘 다 주입하면,
    같은 REVIEW Capability의 다른 `ReviewAgent` 인스턴스가 함께
    등록돼 있어도 `AgentScheduler`가 선택한 인스턴스만 실제로
    처리한다(`is_agent_selected()`). 둘 중 하나라도 주어지지 않으면
    (기본값 `None`) 이 확인을 건너뛰어 기존 동작과 완전히 동일하다.

    **병렬 실행(M58, ADR-0076)**: `max_parallel_agents`(기본값 1)를
    `is_agent_selected()`의 `max_parallel`로 전달한다 — `CodingAgent`와
    동일한 패턴(상세 설명은 `coding_agent.py` 참고)."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        engine_runtime: EngineRuntime,
        agent_registry: AgentRegistry | None = None,
        agent_scheduler: AgentScheduler | None = None,
        max_parallel_agents: int = 1,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._engine_runtime = engine_runtime
        self._agent_registry = agent_registry
        self._agent_scheduler = agent_scheduler
        self._max_parallel_agents = max_parallel_agents
        self._session = agent_runtime.start_agent(
            AgentRole.REVIEWER, frozenset({AgentCapability.REVIEW})
        )
        event_bus.subscribe(self._on_code_verified)

    def _on_code_verified(self, event: Event) -> None:
        if event.event_type != CODE_VERIFIED:
            return
        if self._agent_registry is not None and self._agent_scheduler is not None:
            if not is_agent_selected(
                self._agent_registry,
                self._agent_scheduler,
                AgentCapability.REVIEW,
                self._session.agent_id,
                max_parallel=self._max_parallel_agents,
            ):
                return
        task_id = event.payload["task_id"]
        task = self._task_engine.get_task(task_id)
        context = DevelopmentContext(
            task_id=task_id,
            instructions=task.title,
            prior_output=event.payload.get("output"),
        )
        result = self._engine_runtime.run(
            replace(task, title=context.to_prompt()),
            required_capabilities=required_capabilities(self._session.llm_policy_decision),
            model=model_name(self._session.llm_policy_decision),
        )
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=REVIEW_COMPLETED,
                payload={"task_id": task_id, "output": result.output, "success": result.success},
                source_agent_id=self._session.agent_id,
            )
        )
