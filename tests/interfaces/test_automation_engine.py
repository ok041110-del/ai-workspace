import pytest

from ai_workspace.interfaces.automation_engine import DuplicateTriggerError

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
