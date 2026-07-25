import pytest

from ai_workspace.engines.automation_engine import InMemoryAutomationEngine
from ai_workspace.interfaces.automation_engine import DuplicateTriggerError


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
