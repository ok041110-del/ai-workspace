from __future__ import annotations

from ai_workspace.interfaces.automation_engine import AutomationEngine, DuplicateTriggerError


class InMemoryAutomationEngine(AutomationEngine):
    """조건/일정 기반 자동 트리거를 메모리에 등록하는 최소 구현체(T2-03)."""

    def __init__(self) -> None:
        self._triggers: list[str] = []

    def register_trigger(self, trigger_id: str, description: str) -> None:
        if trigger_id in self._triggers:
            raise DuplicateTriggerError(trigger_id)
        self._triggers.append(trigger_id)

    def list_triggers(self) -> list[str]:
        return list(self._triggers)
