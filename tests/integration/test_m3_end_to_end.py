from __future__ import annotations

import pytest
from tests.adapters.test_claude_code_engine_adapter import FakeProcessRunner, success_result
from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeAgentScheduler,
    FakeProjectRepository,
    FakeWorkflowEngine,
)

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.core.workspace_core import WorkspaceCore
from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.engines.approval_engine import InMemoryApprovalEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.engine.approval_pipeline import (
    EngineApprovalPipeline,
    UnapprovedTaskExecutionError,
)
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime
from ai_workspace.runtime.engine.recovering_engine_runtime import RecoveringEngineRuntime


def assemble() -> tuple[WorkspaceCore, EngineApprovalPipeline, InMemoryEventBus, FakeProcessRunner]:
    """M3 전체 계층을 실제 구현으로 조립한다: WorkspaceCore ↔
    RecoveringEngineRuntime(ManagedEngineRuntime(ClaudeCodeEngineAdapter))
    ↔ EngineApprovalPipeline, 모두 같은 EventBus를 공유한다.
    ClaudeCodeEngineAdapter만 실제 `claude` 프로세스 대신
    `FakeProcessRunner`를 주입받는다(비용·비결정성 방지, 명령 조립·JSON
    파싱 등 실제 코드 경로는 그대로 거친다)."""
    event_bus = InMemoryEventBus()
    process_runner = FakeProcessRunner()
    process_runner.result = success_result("완료")
    adapter = ClaudeCodeEngineAdapter(process_runner=process_runner)
    managed_runtime = ManagedEngineRuntime(event_bus=event_bus)
    managed_runtime.register_engine("claude_code", adapter)
    recovering_runtime = RecoveringEngineRuntime(inner=managed_runtime, retry_policy=RetryPolicy())
    pipeline = EngineApprovalPipeline(
        approval_engine=InMemoryApprovalEngine(),
        engine_runtime=recovering_runtime,
        event_bus=event_bus,
    )
    core = WorkspaceCore(
        project_repository=FakeProjectRepository(),
        workflow_engine=FakeWorkflowEngine(),
        agent_registry=FakeAgentRegistry(),
        agent_scheduler=FakeAgentScheduler(),
        agent_manager=FakeAgentManager(),
        event_bus=event_bus,
        engine_runtime=recovering_runtime,
    )
    return core, pipeline, event_bus, process_runner


def test_full_stack_approve_and_execute_publishes_events_in_order() -> None:
    core, pipeline, event_bus, process_runner = assemble()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    task = Task(task_id="t1", project_id="p1", title="문서화하기")

    request = pipeline.request_approval(task)
    pipeline.decide(request.request_id, approved=True)
    result = pipeline.run_approved(request.request_id)

    assert result.success is True
    assert result.output == "완료"
    assert [event.event_type for event in received] == [
        "approval_requested",
        "approval_granted",
        "engine_task_started",
        "engine_task_completed",
    ]
    assert process_runner.received_commands[0][:3] == ["claude", "-p", "문서화하기"]
    assert core.engine_runtime.status("t1").name == "COMPLETED"


def test_full_stack_reject_blocks_execution_and_stops_event_chain() -> None:
    _core, pipeline, event_bus, process_runner = assemble()
    received: list[Event] = []
    event_bus.subscribe(received.append)
    task = Task(task_id="t1", project_id="p1", title="문서화하기")

    request = pipeline.request_approval(task)
    pipeline.decide(request.request_id, approved=False)

    with pytest.raises(UnapprovedTaskExecutionError):
        pipeline.run_approved(request.request_id)
    assert [event.event_type for event in received] == [
        "approval_requested",
        "approval_rejected",
    ]
    assert process_runner.received_commands == []


def test_workspace_core_engine_session_tracks_the_approved_task() -> None:
    """EngineSession 연동은 이번 E2E 테스트의 핵심이 아니므로 부수적으로만
    확인한다 — 정상 실행 흐름 자체는 위 테스트가 이미 검증한다."""
    core, pipeline, _event_bus, _process_runner = assemble()
    ws_session = core.start_session(project_id="p1")
    task = Task(task_id="t1", project_id="p1", title="문서화하기")
    engine_session = core.start_engine_session(task_id=task.task_id)
    core.update_session(ws_session.session_id, engine_session_id=engine_session.session_id)

    request = pipeline.request_approval(task)
    pipeline.decide(request.request_id, approved=True)
    pipeline.run_approved(request.request_id)
    core.end_engine_session(engine_session.session_id)

    assert core.get_session(ws_session.session_id).engine_session_id == engine_session.session_id
    assert core.list_engine_session_history() == [engine_session]
