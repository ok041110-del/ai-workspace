import pytest

from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.automation_engine import (
    DuplicateTriggerError,
    TriggerNotBoundError,
    TriggerNotFoundError,
)

from .fakes import FakeAutomationEngine


def test_register_trigger_appears_in_list() -> None:
    engine = FakeAutomationEngine()

    engine.register_trigger("daily-status-check", "매일 상태 점검")

    assert "daily-status-check" in engine.list_triggers()


def test_duplicate_trigger_raises_error() -> None:
    engine = FakeAutomationEngine()
    engine.register_trigger("trigger-1", "설명")

    with pytest.raises(DuplicateTriggerError):
        engine.register_trigger("trigger-1", "다른 설명")


def test_list_triggers_returns_defensive_copy() -> None:
    engine = FakeAutomationEngine()
    engine.register_trigger("trigger-1", "설명")

    triggers = engine.list_triggers()
    triggers.append("trigger-2")

    assert engine.list_triggers() == ["trigger-1"]


def test_bind_workflow_unknown_trigger_raises_error() -> None:
    engine = FakeAutomationEngine()
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"])

    with pytest.raises(TriggerNotFoundError):
        engine.bind_workflow("unknown", workflow)


def test_fire_unknown_trigger_raises_error() -> None:
    engine = FakeAutomationEngine()

    with pytest.raises(TriggerNotFoundError):
        engine.fire("unknown")


def test_fire_unbound_trigger_raises_error() -> None:
    engine = FakeAutomationEngine()
    engine.register_trigger("trigger-1", "설명")

    with pytest.raises(TriggerNotBoundError):
        engine.fire("trigger-1")


def test_fire_returns_bound_workflow() -> None:
    engine = FakeAutomationEngine()
    engine.register_trigger("trigger-1", "설명")
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"])

    engine.bind_workflow("trigger-1", workflow)

    assert engine.fire("trigger-1") == workflow


def test_bind_workflow_overwrites_previous_binding() -> None:
    engine = FakeAutomationEngine()
    engine.register_trigger("trigger-1", "설명")
    engine.bind_workflow("trigger-1", Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1"]))
    updated = Workflow(workflow_id="w2", mission_id="m1", task_ids=["t2"])

    engine.bind_workflow("trigger-1", updated)

    assert engine.fire("trigger-1") == updated
