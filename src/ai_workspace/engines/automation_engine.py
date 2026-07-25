from __future__ import annotations

from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.automation_engine import (
    AutomationEngine,
    DuplicateTriggerError,
    TriggerNotBoundError,
    TriggerNotFoundError,
)


class InMemoryAutomationEngine(AutomationEngine):
    """조건/일정 기반 자동 트리거를 메모리에 등록하는 최소 구현체(T2-03,
    Workflow 연결·발동은 M4-T07). `WorkflowEngine`에 의존하지 않는다 —
    연결 관리만 담당하고 실행은 호출자 책임이다(Interface docstring
    참고)."""

    def __init__(self) -> None:
        self._triggers: list[str] = []
        self._workflows: dict[str, Workflow] = {}

    def register_trigger(self, trigger_id: str, description: str) -> None:
        if trigger_id in self._triggers:
            raise DuplicateTriggerError(trigger_id)
        self._triggers.append(trigger_id)

    def list_triggers(self) -> list[str]:
        return list(self._triggers)

    def bind_workflow(self, trigger_id: str, workflow: Workflow) -> None:
        if trigger_id not in self._triggers:
            raise TriggerNotFoundError(trigger_id)
        self._workflows[trigger_id] = workflow

    def fire(self, trigger_id: str) -> Workflow:
        if trigger_id not in self._triggers:
            raise TriggerNotFoundError(trigger_id)
        if trigger_id not in self._workflows:
            raise TriggerNotBoundError(trigger_id)
        return self._workflows[trigger_id]
