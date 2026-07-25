from __future__ import annotations

import pytest
from tests.interfaces.fakes import FakeEngineRuntime

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task
from ai_workspace.engines.approval_engine import InMemoryApprovalEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalRequestNotFoundError,
)
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.engine.approval_pipeline import (
    EngineApprovalPipeline,
    UnapprovedTaskExecutionError,
)


def make_pipeline() -> tuple[EngineApprovalPipeline, FakeEngineRuntime, InMemoryEventBus]:
    engine_runtime = FakeEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())
    event_bus = InMemoryEventBus()
    pipeline = EngineApprovalPipeline(
        approval_engine=InMemoryApprovalEngine(),
        engine_runtime=engine_runtime,
        event_bus=event_bus,
    )
    return pipeline, engine_runtime, event_bus


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="demo")


def test_request_approval_creates_pending_request() -> None:
    pipeline, _, _ = make_pipeline()

    request = pipeline.request_approval(make_task())

    assert request.action_type == ApprovalActionType.ENGINE_TASK_EXECUTION


def test_request_approval_publishes_event() -> None:
    pipeline, _, event_bus = make_pipeline()
    received: list[Event] = []
    event_bus.subscribe(received.append)

    request = pipeline.request_approval(make_task("t1"))

    assert len(received) == 1
    assert received[0].event_type == "approval_requested"
    assert received[0].payload == {"request_id": request.request_id, "task_id": "t1"}


def test_decide_approved_publishes_granted_event() -> None:
    pipeline, _, event_bus = make_pipeline()
    request = pipeline.request_approval(make_task())
    received: list[Event] = []
    event_bus.subscribe(received.append)

    pipeline.decide(request.request_id, approved=True)

    assert received[0].event_type == "approval_granted"
    assert received[0].payload == {"request_id": request.request_id}


def test_decide_rejected_publishes_rejected_event() -> None:
    pipeline, _, event_bus = make_pipeline()
    request = pipeline.request_approval(make_task())
    received: list[Event] = []
    event_bus.subscribe(received.append)

    pipeline.decide(request.request_id, approved=False)

    assert received[0].event_type == "approval_rejected"


def test_decide_unknown_request_raises_error() -> None:
    pipeline, _, _ = make_pipeline()

    with pytest.raises(ApprovalRequestNotFoundError):
        pipeline.decide("unknown", approved=True)


def test_decide_twice_raises_error() -> None:
    pipeline, _, _ = make_pipeline()
    request = pipeline.request_approval(make_task())
    pipeline.decide(request.request_id, approved=True)

    with pytest.raises(ApprovalAlreadyDecidedError):
        pipeline.decide(request.request_id, approved=False)


def test_run_approved_executes_task_via_engine_runtime() -> None:
    pipeline, engine_runtime, _ = make_pipeline()
    request = pipeline.request_approval(make_task("t1"))
    pipeline.decide(request.request_id, approved=True)

    result = pipeline.run_approved(request.request_id)

    assert result.success is True
    assert engine_runtime.status("t1").name == "COMPLETED"


def test_run_approved_without_decision_raises_error() -> None:
    pipeline, _, _ = make_pipeline()
    request = pipeline.request_approval(make_task())

    with pytest.raises(UnapprovedTaskExecutionError):
        pipeline.run_approved(request.request_id)


def test_run_approved_after_rejection_raises_error() -> None:
    pipeline, _, _ = make_pipeline()
    request = pipeline.request_approval(make_task())
    pipeline.decide(request.request_id, approved=False)

    with pytest.raises(UnapprovedTaskExecutionError):
        pipeline.run_approved(request.request_id)


def test_run_approved_unknown_request_raises_error() -> None:
    pipeline, _, _ = make_pipeline()

    with pytest.raises(UnapprovedTaskExecutionError):
        pipeline.run_approved("unknown")


def test_run_approved_twice_raises_error() -> None:
    pipeline, _, _ = make_pipeline()
    request = pipeline.request_approval(make_task())
    pipeline.decide(request.request_id, approved=True)
    pipeline.run_approved(request.request_id)

    with pytest.raises(UnapprovedTaskExecutionError):
        pipeline.run_approved(request.request_id)
