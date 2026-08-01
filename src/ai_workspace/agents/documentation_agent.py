from __future__ import annotations

import uuid

from ai_workspace.agents.events import DOCUMENTATION_COMPLETED, REVIEW_COMPLETED
from ai_workspace.agents.scheduling import is_agent_selected
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.llm_policy import model_name, required_capabilities
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
from ai_workspace.interfaces.context_manager import ContextManager
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class DocumentationAgent:
    """`ReviewCompleted` Event를 구독해 문서화하고 `DocumentationCompleted`
    Event를 발행하는 Agent(ARCHITECTURE.md §3.6, §5, T2-06). 협업 체인의
    마지막 단계로, 완료 시 Context Manager로 Snapshot을 생성해 Memory를
    갱신한다(ARCHITECTURE.md §5 다이어그램의 마무리 단계).

    **Policy→Execution 라우팅(M6-T02)**: `CodingAgent`와 동일하게
    `AgentSession.llm_policy_decision`을 `required_capabilities()`로
    변환해 `engine_runtime.run()`에 전달한다. **Model 라우팅(M14-T03)**:
    같은 방식으로 `model_name()`도 함께 전달한다.

    **Memory 요약(M7-T02)**: `engine_runtime.run()`의 결과(`output`)를
    그대로 Memory 요약으로 재활용해 `create_snapshot()`에 전달한다 —
    이전에는 이 결과를 그대로 버렸다. 신규 LLM 호출을 추가하지 않는다
    (YAGNI). 성공/실패 여부와 무관하게 `output`을 저장한다 — 실패 시
    출력이 유의미한 요약이 아닐 수 있다는 점은 알려진 단순화다.

    **세션 연속성(M8-T02)**: `create_snapshot()`이 반환하는 snapshot_id를
    `workspace_session.memory_snapshot_id`에 되먹인다 — 이전에는 반환값
    자체가 버려져 다음 Mission이 이번 Snapshot을 전혀 알지 못했다. 같은
    세션에서 이어지는 Mission은 이제 `assemble_context()`가 자동으로
    이 Snapshot을 반영한다.

    **Multi-Agent Collaboration(M56, ADR-0074)**: `CodingAgent`(M13)와
    동일한 패턴 — `agent_registry`/`agent_scheduler`를 둘 다 주입하면,
    같은 DOCUMENTATION Capability의 다른 `DocumentationAgent` 인스턴스가
    함께 등록돼 있어도 `AgentScheduler`가 선택한 인스턴스만 실제로
    처리한다(`is_agent_selected()`). 둘 중 하나라도 주어지지 않으면
    (기본값 `None`) 이 확인을 건너뛰어 기존 동작과 완전히 동일하다."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        engine_runtime: EngineRuntime,
        context_manager: ContextManager,
        workspace_session: WorkspaceSession,
        agent_registry: AgentRegistry | None = None,
        agent_scheduler: AgentScheduler | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._engine_runtime = engine_runtime
        self._context_manager = context_manager
        self._workspace_session = workspace_session
        self._agent_registry = agent_registry
        self._agent_scheduler = agent_scheduler
        self._session = agent_runtime.start_agent(
            AgentRole.DOCUMENTATION, frozenset({AgentCapability.DOCUMENTATION})
        )
        event_bus.subscribe(self._on_review_completed)

    def _on_review_completed(self, event: Event) -> None:
        if event.event_type != REVIEW_COMPLETED:
            return
        if self._agent_registry is not None and self._agent_scheduler is not None:
            if not is_agent_selected(
                self._agent_registry,
                self._agent_scheduler,
                AgentCapability.DOCUMENTATION,
                self._session.agent_id,
            ):
                return
        task_id = event.payload["task_id"]
        task = self._task_engine.get_task(task_id)
        result = self._engine_runtime.run(
            task,
            required_capabilities=required_capabilities(self._session.llm_policy_decision),
            model=model_name(self._session.llm_policy_decision),
        )
        self._task_engine.transition(task, TaskStatus.DONE)
        snapshot_id = self._context_manager.create_snapshot(
            self._workspace_session, summary=result.output
        )
        self._workspace_session.memory_snapshot_id = snapshot_id
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=DOCUMENTATION_COMPLETED,
                payload={"task_id": task_id},
                source_agent_id=self._session.agent_id,
            )
        )
