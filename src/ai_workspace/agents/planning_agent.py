from __future__ import annotations

import uuid

from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.agent import AgentCapability, AgentRole
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.context_manager import ContextManager
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class PlanningAgent:
    """Mission을 Task로 계획하고 `MissionPlanned` Event를 발행하는 Agent
    (ARCHITECTURE.md §3.6, §5, T2-06). 파이프라인의 진입점 — 외부에서
    `plan_mission()`을 호출해 협업 체인을 시작시킨다.

    **세션 연속성(M8-T03)**: Mission을 시작하기 전에 `workspace_session.
    memory_snapshot_id`가 비어 있으면(예: 새로 만든 세션) `context_manager
    .latest_snapshot_id(project_id)`로 그 프로젝트의 최신 Snapshot을
    자동 복원한다 — Workspace Core가 아니라 Agent 계층에서 해결한다
    (ARCHITECTURE.md §8 규칙 5·7, Workspace Core는 Context Manager를
    전혀 모른다). 이미 값이 있으면(같은 세션에서 이어지는 Mission)
    덮어쓰지 않는다.

    **세션 리셋 옵션(M9-T03)**: `plan_mission(..., reset=True)`면 위
    자동 복원을 건너뛴다 — 사용자가 이전 프로젝트 요약을 이어받지 않고
    완전히 새로 시작하고 싶을 때 쓴다. 이미 `memory_snapshot_id`가 있는
    세션(같은 세션의 후속 Mission)에는 영향을 주지 않는다 — 그 값을
    지우는 것은 이번 갭(M8 Review가 지적한 "새 세션 자동 복원을 원치
    않는 경우")과는 다른 문제라 범위에 포함하지 않는다."""

    def __init__(
        self,
        *,
        agent_runtime: AgentRuntime,
        event_bus: EventBus,
        task_engine: TaskEngine,
        context_manager: ContextManager,
        workspace_session: WorkspaceSession,
    ) -> None:
        self._event_bus = event_bus
        self._task_engine = task_engine
        self._context_manager = context_manager
        self._workspace_session = workspace_session
        self._session = agent_runtime.start_agent(
            AgentRole.PLANNER, frozenset({AgentCapability.PLANNING})
        )

    def plan_mission(self, project_id: str, title: str, *, reset: bool = False) -> Task:
        if not reset and self._workspace_session.memory_snapshot_id is None:
            self._workspace_session.memory_snapshot_id = self._context_manager.latest_snapshot_id(
                project_id
            )
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
