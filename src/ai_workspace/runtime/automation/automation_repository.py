from __future__ import annotations

from ai_workspace.domain.automation import AutomationRule
from ai_workspace.interfaces.automation_repository import (
    AutomationRepository,
    AutomationRuleNotFoundError,
)


class InMemoryAutomationRepository(AutomationRepository):
    """`AutomationRule`을 메모리에 보관하는 최소 구현체(M21-T01).
    `ProjectRepository`의 파일 구현체(`FileProjectRepository`)와
    달리 아직 영속화하지 않는다 — 향후 `FileAutomationRepository`/
    `DatabaseAutomationRepository`로 확장 가능하도록 이 Interface만
    보고 구현했다(사용자 DoD)."""

    def __init__(self) -> None:
        self._rules: dict[str, AutomationRule] = {}

    def get(self, rule_id: str) -> AutomationRule:
        if rule_id not in self._rules:
            raise AutomationRuleNotFoundError(rule_id)
        return self._rules[rule_id]

    def save(self, rule: AutomationRule) -> None:
        self._rules[rule.rule_id] = rule

    def delete(self, rule_id: str) -> None:
        if rule_id not in self._rules:
            raise AutomationRuleNotFoundError(rule_id)
        del self._rules[rule_id]

    def list_rules(self) -> list[AutomationRule]:
        return list(self._rules.values())
