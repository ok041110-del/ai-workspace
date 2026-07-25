import pytest

from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.automation_engine import InMemoryAutomationEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.interfaces.automation_engine import (
    DuplicateTriggerError,
    TriggerNotBoundError,
    TriggerNotFoundError,
)


def test_register_trigger_appears_in_list() -> None:
    engine = InMemoryAutomationEngine()

    engine.register_trigger("t1", "매일 오전 9시 실행")

    assert engine.list_triggers() == ["t1"]


def test_register_duplicate_trigger_raises_error() -> None:
    engine = InMemoryAutomationEngine()
    engine.register_trigger("t1", "매일 오전 9시 실행")

    with pytest.raises(DuplicateTriggerError):
        engine.register_trigger("t1", "다른 설명")


def test_list_triggers_returns_defensive_copy() -> None:
    engine = InMemoryAutomationEngine()
    engine.register_trigger("t1", "매일 오전 9시 실행")

    triggers = engine.list_triggers()
    triggers.append("t2")

    assert engine.list_triggers() == ["t1"]


def test_bind_workflow_unknown_trigger_raises_error() -> None:
    engine = InMemoryAutomationEngine()
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"])

    with pytest.raises(TriggerNotFoundError):
        engine.bind_workflow("unknown", workflow)


def test_fire_unknown_trigger_raises_error() -> None:
    engine = InMemoryAutomationEngine()

    with pytest.raises(TriggerNotFoundError):
        engine.fire("unknown")


def test_fire_unbound_trigger_raises_error() -> None:
    engine = InMemoryAutomationEngine()
    engine.register_trigger("t1", "매일 오전 9시 실행")

    with pytest.raises(TriggerNotBoundError):
        engine.fire("t1")


def test_fire_returns_bound_workflow() -> None:
    engine = InMemoryAutomationEngine()
    engine.register_trigger("t1", "매일 오전 9시 실행")
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["a", "b"])

    engine.bind_workflow("t1", workflow)

    assert engine.fire("t1") == workflow


def test_automation_scenario_fires_and_executes_real_workflow() -> None:
    """M4 DoD: "자동화 시나리오 1건 이상 동작"을 증명한다. AutomationEngine은
    WorkflowEngine에 의존하지 않으므로(연결 관리만 담당), 호출자가
    fire()로 받은 Workflow를 직접 WorkflowEngine에 넘겨 실행까지
    완료하는 전체 흐름을 검증한다."""
    automation_engine = InMemoryAutomationEngine()
    workflow_engine = InMemoryWorkflowEngine()
    automation_engine.register_trigger("daily-build", "매일 자정 실행")
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=["build", "test"],
        dependencies={"test": {"build"}},
    )
    automation_engine.bind_workflow("daily-build", workflow)

    triggered_workflow = automation_engine.fire("daily-build")
    execution_order = workflow_engine.plan(triggered_workflow)

    assert execution_order == ["build", "test"]
