from __future__ import annotations

import pytest
from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeAgentScheduler,
    FakeEventBus,
    FakeProjectRepository,
    FakeWorkflowEngine,
)

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.core.workspace_core import (
    EngineSessionNotFoundError,
    WorkspaceCore,
    WorkspaceSessionNotFoundError,
)
from ai_workspace.domain.project import Project
from ai_workspace.domain.task import Task
from ai_workspace.domain.workflow import Workflow
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import EngineAdapter, EngineResult, EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.project_repository import ProjectNotFoundError
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime


class SpyEngineRuntime(EngineRuntime):
    """Workspace Core가 Task를 직접 실행하지 않음을 증명하기 위한 테스트 더블.
    어떤 메서드가 호출되어도 즉시 실패한다 — Core는 이 인터페이스를 저장하고
    노출할 뿐, 스스로 호출해서는 안 된다."""

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        raise AssertionError("Workspace Core는 엔진을 직접 등록하면 안 된다.")

    def run(self, task: Task, required_capabilities: frozenset[str] = frozenset()) -> EngineResult:
        raise AssertionError("Workspace Core는 Task를 직접 실행하면 안 된다.")

    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        raise AssertionError("Workspace Core는 Task를 직접 실행하면 안 된다.")

    def cancel(self, task_id: str) -> None:
        raise AssertionError("Workspace Core는 Engine Runtime을 직접 제어하면 안 된다.")

    def status(self, task_id: str) -> EngineSessionStatus:
        raise AssertionError("Workspace Core는 Engine Runtime을 직접 제어하면 안 된다.")


def make_core(
    config: dict[str, str] | None = None,
    project_repository: FakeProjectRepository | None = None,
) -> WorkspaceCore:
    return WorkspaceCore(
        project_repository=project_repository or FakeProjectRepository(),
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=FakeAgentRegistry(),
        agent_scheduler=FakeAgentScheduler(),
        agent_manager=FakeAgentManager(),
        event_bus=FakeEventBus(),
        engine_runtime=SpyEngineRuntime(),
        config=config,
    )


def test_load_project_delegates_to_project_repository() -> None:
    project_repository = FakeProjectRepository()
    project = Project(project_id="p1", name="Demo", goal="목표")
    project_repository.save(project)
    core = make_core(project_repository=project_repository)

    loaded = core.load_project("p1")

    assert loaded == project


def test_save_project_delegates_to_project_repository() -> None:
    project_repository = FakeProjectRepository()
    core = make_core(project_repository=project_repository)
    project = Project(project_id="p1", name="Demo", goal="목표")

    core.save_project(project)

    assert project_repository.load("p1") == project


def test_load_project_missing_raises_error() -> None:
    core = make_core()

    with pytest.raises(ProjectNotFoundError):
        core.load_project("unknown")


def test_config_returns_defensive_copy() -> None:
    core = make_core(config={"log_level": "info"})

    returned = core.config
    returned["log_level"] = "debug"

    assert core.config == {"log_level": "info"}


def test_config_defaults_to_empty_dict() -> None:
    core = make_core()

    assert core.config == {}


def test_start_session_creates_session_with_unique_id() -> None:
    core = make_core()

    session1 = core.start_session(project_id="p1")
    session2 = core.start_session(project_id="p1")

    assert session1.session_id != session2.session_id
    assert session1.current_project_id == "p1"


def test_start_session_defaults_project_id_to_none() -> None:
    core = make_core()

    session = core.start_session()

    assert session.current_project_id is None


def test_get_session_unknown_raises_error() -> None:
    core = make_core()

    with pytest.raises(WorkspaceSessionNotFoundError):
        core.get_session("unknown")


def test_update_session_changes_only_provided_fields() -> None:
    core = make_core()
    session = core.start_session(project_id="p1")

    updated = core.update_session(session.session_id, current_mission_id="m1")

    assert updated.current_mission_id == "m1"
    assert updated.current_project_id == "p1"


def test_update_session_updates_active_workflow_id() -> None:
    core = make_core()
    session = core.start_session()

    updated = core.update_session(session.session_id, active_workflow_id="w1")

    assert updated.active_workflow_id == "w1"


def test_update_session_updates_active_agent_ids_defensively() -> None:
    core = make_core()
    session = core.start_session()
    agent_ids = ["a1", "a2"]

    updated = core.update_session(session.session_id, active_agent_ids=agent_ids)
    agent_ids.append("a3")

    assert updated.active_agent_ids == ["a1", "a2"]


def test_update_session_updates_memory_snapshot_id() -> None:
    core = make_core()
    session = core.start_session()

    updated = core.update_session(session.session_id, memory_snapshot_id="snap1")

    assert updated.memory_snapshot_id == "snap1"


def test_update_session_updates_engine_session_id() -> None:
    core = make_core()
    session = core.start_session()

    updated = core.update_session(session.session_id, engine_session_id="es1")

    assert updated.engine_session_id == "es1"


def test_update_session_unknown_raises_error() -> None:
    core = make_core()

    with pytest.raises(WorkspaceSessionNotFoundError):
        core.update_session("unknown", current_mission_id="m1")


def test_end_session_removes_session() -> None:
    core = make_core()
    session = core.start_session()

    core.end_session(session.session_id)

    with pytest.raises(WorkspaceSessionNotFoundError):
        core.get_session(session.session_id)


def test_end_session_unknown_raises_error() -> None:
    core = make_core()

    with pytest.raises(WorkspaceSessionNotFoundError):
        core.end_session("unknown")


def test_start_workflow_delegates_to_workflow_engine() -> None:
    core = make_core()
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"])

    order = core.start_workflow(workflow)

    assert set(order) == {"t1", "t2"}


def test_shutdown_clears_all_sessions() -> None:
    core = make_core()
    session = core.start_session()

    core.shutdown()

    with pytest.raises(WorkspaceSessionNotFoundError):
        core.get_session(session.session_id)


def test_core_exposes_injected_agent_and_engine_runtime_dependencies() -> None:
    agent_registry = FakeAgentRegistry()
    agent_scheduler = FakeAgentScheduler()
    agent_manager = FakeAgentManager()
    event_bus = FakeEventBus()
    engine_runtime = SpyEngineRuntime()
    core = WorkspaceCore(
        project_repository=FakeProjectRepository(),
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=agent_registry,
        agent_scheduler=agent_scheduler,
        agent_manager=agent_manager,
        event_bus=event_bus,
        engine_runtime=engine_runtime,
    )

    assert core.agent_registry is agent_registry
    assert core.agent_scheduler is agent_scheduler
    assert core.agent_manager is agent_manager
    assert core.event_bus is event_bus
    assert core.engine_runtime is engine_runtime


def test_core_never_calls_engine_runtime_when_using_public_api() -> None:
    """T1-22 DoD: Task 실행은 Workspace Core가 하지 않고 Agent Runtime에
    위임한다. SpyEngineRuntime은 어떤 메서드가 호출되어도 AssertionError를
    던지므로, 아래 흐름이 예외 없이 끝나면 Core가 Engine Runtime을 스스로
    호출하지 않았음이 증명된다."""
    project_repository = FakeProjectRepository()
    project_repository.save(Project(project_id="p1", name="Demo", goal="목표"))
    core = make_core(config={"env": "test"}, project_repository=project_repository)

    session = core.start_session(project_id="p1")
    core.update_session(session.session_id, current_mission_id="m1")
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"])
    core.start_workflow(workflow)
    core.end_session(session.session_id)
    core.shutdown()


def test_core_has_no_task_execution_method() -> None:
    """Task 실행 메서드가 없는 것은 누락이 아니라 설계다 — Engine Runtime
    호출은 항상 Agent Runtime(Milestone 2 이후)을 거쳐야 한다."""
    core = make_core()

    assert not hasattr(core, "run_task")
    assert not hasattr(core, "execute_task")


def test_start_engine_session_creates_session_with_unique_id() -> None:
    core = make_core()

    session1 = core.start_engine_session(task_id="t1")
    session2 = core.start_engine_session(task_id="t1")

    assert session1.session_id != session2.session_id
    assert session1.task_id == "t1"


def test_get_engine_session_unknown_raises_error() -> None:
    core = make_core()

    with pytest.raises(EngineSessionNotFoundError):
        core.get_engine_session("unknown")


def test_get_engine_session_returns_tracked_session() -> None:
    core = make_core()
    started = core.start_engine_session(task_id="t1")

    assert core.get_engine_session(started.session_id) == started


def test_end_engine_session_removes_active_session() -> None:
    core = make_core()
    session = core.start_engine_session(task_id="t1")

    core.end_engine_session(session.session_id)

    with pytest.raises(EngineSessionNotFoundError):
        core.get_engine_session(session.session_id)


def test_end_engine_session_unknown_raises_error() -> None:
    core = make_core()

    with pytest.raises(EngineSessionNotFoundError):
        core.end_engine_session("unknown")


def test_end_engine_session_appends_to_history() -> None:
    core = make_core()
    session = core.start_engine_session(task_id="t1")

    core.end_engine_session(session.session_id)

    assert core.list_engine_session_history() == [session]


def test_list_engine_session_history_returns_defensive_copy() -> None:
    core = make_core()
    session = core.start_engine_session(task_id="t1")
    core.end_engine_session(session.session_id)

    history = core.list_engine_session_history()
    history.append(session)

    assert core.list_engine_session_history() == [session]


def test_shutdown_clears_active_engine_sessions() -> None:
    core = make_core()
    session = core.start_engine_session(task_id="t1")

    core.shutdown()

    with pytest.raises(EngineSessionNotFoundError):
        core.get_engine_session(session.session_id)


def test_workspace_core_wires_real_managed_engine_runtime_without_core_changes() -> None:
    """M3-T04: WorkspaceCore가 T2-05의 InMemoryEngineRuntime뿐 아니라
    M3-T01의 ManagedEngineRuntime도 Core 코드 변경 없이 그대로 주입받을 수
    있음을 증명한다(T1-23의 FileProjectRepository 주입 검증과 동일한 패턴)."""
    event_bus = InMemoryEventBus()
    engine_runtime = ManagedEngineRuntime(event_bus=event_bus)
    engine_runtime.register_engine("mock", MockEngineAdapter())
    core = WorkspaceCore(
        project_repository=FakeProjectRepository(),
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=FakeAgentRegistry(),
        agent_scheduler=FakeAgentScheduler(),
        agent_manager=FakeAgentManager(),
        event_bus=event_bus,
        engine_runtime=engine_runtime,
    )

    assert core.engine_runtime is engine_runtime


def test_workspace_core_event_bus_receives_managed_engine_runtime_events() -> None:
    """EventBus 완전 연동: Core에 주입한 EventBus와 ManagedEngineRuntime에
    주입한 EventBus가 같은 인스턴스이면, Runtime이 발행하는
    engine_task_* 이벤트가 Core.event_bus 구독자에게 그대로 도달한다."""
    event_bus = InMemoryEventBus()
    engine_runtime = ManagedEngineRuntime(event_bus=event_bus)
    engine_runtime.register_engine("mock", MockEngineAdapter())
    core = WorkspaceCore(
        project_repository=FakeProjectRepository(),
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=FakeAgentRegistry(),
        agent_scheduler=FakeAgentScheduler(),
        agent_manager=FakeAgentManager(),
        event_bus=event_bus,
        engine_runtime=engine_runtime,
    )
    received: list[Event] = []
    core.event_bus.subscribe(received.append)

    task = Task(task_id="t1", project_id="p1", title="demo")
    core.engine_runtime.run(task)

    event_types = {event.event_type for event in received}
    assert {"engine_task_started", "engine_task_completed"}.issubset(event_types)


def test_workspace_core_links_engine_session_to_workspace_session() -> None:
    """WorkspaceSession.engine_session_id(T1-22부터 존재하던 필드)가 실제
    EngineSession과 연결되는 흐름 — 새 필드 없이 기존 update_session()과
    새 start_engine_session()의 조합만으로 동작함을 증명한다."""
    core = make_core()
    ws_session = core.start_session(project_id="p1")
    engine_session = core.start_engine_session(task_id="t1")

    updated = core.update_session(
        ws_session.session_id, engine_session_id=engine_session.session_id
    )

    assert updated.engine_session_id == engine_session.session_id
    assert core.get_engine_session(engine_session.session_id) == engine_session
