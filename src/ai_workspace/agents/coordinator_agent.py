from __future__ import annotations

import uuid

from ai_workspace.agents.events import (
    CODE_VERIFIED,
    MISSION_PLANNED,
    REWORK_EXHAUSTED,
    SHELL_COMPLETED,
)
from ai_workspace.agents.scheduling import is_agent_selected
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime

_DEFAULT_MAX_REWORK_ATTEMPTS = 3


class CoordinatorAgent:
    """`ShellCompleted` Event를 구독해 테스트 결과에 따라 Review로
    진행할지 재작업을 시작할지 결정하는 Agent(ARCHITECTURE.md ADR-0019
    Coordination Capability의 최초 구현체, M5-T06).

    테스트가 통과하면 `CodeVerified`를 발행해 `ReviewAgent`를 깨우고,
    실패하면 같은 Task를 `MissionPlanned`로 재발행해 `CodingAgent`로
    되돌린다(재작업). 무한 루프 방지를 위해 `max_rework_attempts`를
    초과하면 재작업을 멈추고 `ReworkExhausted`를 발행한다.

    시도 이력(Step)은 이 Agent가 직접 보관하지 않고
    `TaskEngine.record_step()`을 통해 실행 컨텍스트(TaskEngine)에
    기록한다 — Step의 소유권을 Agent가 아니라 Task 실행 컨텍스트에
    두기 위함(사용자 지시).

    **Multi-Agent Collaboration(M56, ADR-0074)**: `CodingAgent`(M13)와
    동일한 패턴 — `agent_registry`/`agent_scheduler`를 둘 다 주입하면,
    같은 COORDINATION Capability의 다른 `CoordinatorAgent` 인스턴스가
    함께 등록돼 있어도 `AgentScheduler`가 선택한 인스턴스만 실제로
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
        max_rework_attempts: int = _DEFAULT_MAX_REWORK_ATTEMPTS,
        agent_registry: AgentRegistry | None = None,
        agent_scheduler: AgentScheduler | None = None,
        max_parallel_agents: int = 1,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._max_rework_attempts = max_rework_attempts
        self._agent_registry = agent_registry
        self._agent_scheduler = agent_scheduler
        self._max_parallel_agents = max_parallel_agents
        self._session = agent_runtime.start_agent(
            AgentRole.COORDINATOR, frozenset({AgentCapability.COORDINATION})
        )
        event_bus.subscribe(self._on_shell_completed)

    def _on_shell_completed(self, event: Event) -> None:
        if event.event_type != SHELL_COMPLETED:
            return
        if self._agent_registry is not None and self._agent_scheduler is not None:
            if not is_agent_selected(
                self._agent_registry,
                self._agent_scheduler,
                AgentCapability.COORDINATION,
                self._session.agent_id,
                max_parallel=self._max_parallel_agents,
            ):
                return
        task_id = event.payload["task_id"]

        if event.payload["success"]:
            self._publish(
                CODE_VERIFIED,
                {"task_id": task_id, "output": event.payload.get("code_output")},
            )
            return

        step = self._task_engine.record_step(
            task_id, f"테스트 실패 - 재작업 필요: {event.payload.get('stderr', '')}"
        )
        attempt_count = len(self._task_engine.get_steps(task_id))
        if attempt_count > self._max_rework_attempts:
            self._publish(REWORK_EXHAUSTED, {"task_id": task_id, "last_step_id": step.step_id})
            return

        self._publish(
            MISSION_PLANNED,
            {"task_id": task_id, "rework_reason": event.payload.get("stderr", "")},
        )

    def _publish(self, event_type: str, payload: dict[str, object]) -> None:
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                payload=payload,
                source_agent_id=self._session.agent_id,
            )
        )
