from __future__ import annotations

import itertools

from ai_workspace.domain.engine_session import EngineSession
from ai_workspace.domain.project import Project
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.agent_manager import AgentManager
from ai_workspace.interfaces.agent_registry import AgentRegistry
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import EventBus
from ai_workspace.interfaces.project_repository import ProjectRepository
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


class WorkspaceSessionNotFoundError(Exception):
    """관리 중이지 않은 session_id를 조회/갱신/종료하려 할 때 발생한다."""


class EngineSessionNotFoundError(Exception):
    """관리 중이지 않은 EngineSession session_id를 조회/종료하려 할 때 발생한다."""


class WorkspaceCore:
    """최상위 오케스트레이터(ARCHITECTURE.md §3.3, ADR-0005, ADR-0010).

    프로젝트/설정 로드, 서비스 초기화, WorkspaceSession 관리, Agent Runtime·
    Engine Runtime 초기화, Workflow 시작, 종료만 책임진다. Task를 실행하는
    메서드가 없는 것은 누락이 아니라 의도된 설계다 — Task 실행은 Agent
    Runtime(Milestone 2 이후 구현)의 책임이며, Workspace Core는 Engine
    Runtime/Engine Adapter를 직접 호출하지 않는다(ARCHITECTURE.md §8 규칙
    3, 6). Registry/Scheduler/Manager/EventBus를 하나의 파사드로 묶지 않고
    개별 Interface로 보관한다(T1-22 명세, YAGNI).

    EngineSession(M3-T04)은 실제 Engine 실행(Agent Runtime → Engine Runtime
    경유)을 호출하지 않는 순수 기록용 추적이다 — 위 규칙과 동일하게 Workspace
    Core는 Engine Runtime을 스스로 호출하지 않으며, 어떤 Task가 어떤
    EngineSession으로 실행 중인지만 보관한다. `AgentSession`/`WorkspaceSession`과
    필드 모양은 비슷하지만 공통 추상화(BaseSession)로 묶지 않는다 — 세 종류의
    Session이 실제로 겹치는 동작을 반복적으로 드러내기 전까지는 독립된 개념으로
    유지한다(점진적 확장 원칙, `.ai/RULES.md` §4.2).
    """

    def __init__(
        self,
        *,
        project_repository: ProjectRepository,
        workflow_engine: WorkflowEngine,
        agent_registry: AgentRegistry,
        agent_scheduler: AgentScheduler,
        agent_manager: AgentManager,
        event_bus: EventBus,
        engine_runtime: EngineRuntime,
        config: dict[str, str] | None = None,
    ) -> None:
        self._project_repository = project_repository
        self._workflow_engine = workflow_engine
        self._agent_registry = agent_registry
        self._agent_scheduler = agent_scheduler
        self._agent_manager = agent_manager
        self._event_bus = event_bus
        self._engine_runtime = engine_runtime
        self._config = dict(config) if config is not None else {}
        self._sessions: dict[str, WorkspaceSession] = {}
        self._session_id_generator = itertools.count(1)
        self._engine_sessions: dict[str, EngineSession] = {}
        self._engine_session_id_generator = itertools.count(1)
        self._engine_session_history: list[EngineSession] = []

    @property
    def config(self) -> dict[str, str]:
        return dict(self._config)

    @property
    def agent_registry(self) -> AgentRegistry:
        return self._agent_registry

    @property
    def agent_scheduler(self) -> AgentScheduler:
        return self._agent_scheduler

    @property
    def agent_manager(self) -> AgentManager:
        return self._agent_manager

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus

    @property
    def engine_runtime(self) -> EngineRuntime:
        return self._engine_runtime

    def load_project(self, project_id: str) -> Project:
        return self._project_repository.load(project_id)

    def start_session(self, project_id: str | None = None) -> WorkspaceSession:
        session_id = f"session-{next(self._session_id_generator)}"
        session = WorkspaceSession(session_id=session_id, current_project_id=project_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> WorkspaceSession:
        if session_id not in self._sessions:
            raise WorkspaceSessionNotFoundError(session_id)
        return self._sessions[session_id]

    def update_session(
        self,
        session_id: str,
        *,
        current_project_id: str | None = None,
        current_mission_id: str | None = None,
        active_workflow_id: str | None = None,
        active_agent_ids: list[str] | None = None,
        memory_snapshot_id: str | None = None,
        engine_session_id: str | None = None,
    ) -> WorkspaceSession:
        session = self.get_session(session_id)
        if current_project_id is not None:
            session.current_project_id = current_project_id
        if current_mission_id is not None:
            session.current_mission_id = current_mission_id
        if active_workflow_id is not None:
            session.active_workflow_id = active_workflow_id
        if active_agent_ids is not None:
            session.active_agent_ids = list(active_agent_ids)
        if memory_snapshot_id is not None:
            session.memory_snapshot_id = memory_snapshot_id
        if engine_session_id is not None:
            session.engine_session_id = engine_session_id
        return session

    def end_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise WorkspaceSessionNotFoundError(session_id)
        del self._sessions[session_id]

    def start_workflow(self, workflow: Workflow) -> list[str]:
        return self._workflow_engine.plan(workflow)

    def start_engine_session(self, task_id: str) -> EngineSession:
        session_id = f"engine-session-{next(self._engine_session_id_generator)}"
        session = EngineSession(session_id=session_id, task_id=task_id)
        self._engine_sessions[session_id] = session
        return session

    def get_engine_session(self, session_id: str) -> EngineSession:
        if session_id not in self._engine_sessions:
            raise EngineSessionNotFoundError(session_id)
        return self._engine_sessions[session_id]

    def end_engine_session(self, session_id: str) -> None:
        if session_id not in self._engine_sessions:
            raise EngineSessionNotFoundError(session_id)
        self._engine_session_history.append(self._engine_sessions.pop(session_id))

    def list_engine_session_history(self) -> list[EngineSession]:
        return list(self._engine_session_history)

    def shutdown(self) -> None:
        self._sessions.clear()
        self._engine_sessions.clear()
