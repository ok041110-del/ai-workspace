from __future__ import annotations

import uuid
from datetime import UTC, datetime

from ai_workspace.domain.automation import Action, AutomationRule, Trigger
from ai_workspace.interfaces.automation_repository import AutomationRepository


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class AutomationService:
    """Automation Rule CRUD의 유일한 진입점(M21-T02, 사용자 승인
    조건 3 — Automation CRUD는 Automation API를 통해서만 수행하고,
    API는 이 Service만 사용한다). `AutomationRepository`만 사용하며
    `web/`이나 `Dashboard`를 전혀 모른다 — `DashboardService`(M20)와
    동일하게 UI를 모르는 순수 서비스다.

    **실행은 이 클래스의 책임이 아니다**: `enable_rule`/`disable_rule`
    은 상태만 바꾸고, Rule에 연결된 Action을 실제로 실행하는 것은
    `AutomationScheduler`(M21-T03)와 `ExecutionDispatcher` 연동
    (M21-T04)의 책임이다(사용자 승인 조건 5 — `ExecutionDispatcher`가
    유일한 실행 진입점)."""

    def __init__(self, *, automation_repository: AutomationRepository) -> None:
        self._automation_repository = automation_repository

    def create_rule(
        self,
        *,
        name: str,
        description: str,
        trigger: Trigger,
        action: Action,
        enabled: bool = True,
    ) -> AutomationRule:
        now = _now_iso()
        rule = AutomationRule(
            rule_id=str(uuid.uuid4()),
            name=name,
            description=description,
            trigger=trigger,
            action=action,
            created_at=now,
            updated_at=now,
            enabled=enabled,
        )
        self._automation_repository.save(rule)
        return rule

    def get_rule(self, rule_id: str) -> AutomationRule:
        return self._automation_repository.get(rule_id)

    def list_rules(self) -> list[AutomationRule]:
        return self._automation_repository.list_rules()

    def update_rule(
        self,
        rule_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        trigger: Trigger | None = None,
        action: Action | None = None,
    ) -> AutomationRule:
        rule = self._automation_repository.get(rule_id)
        if name is not None:
            rule.name = name
        if description is not None:
            rule.description = description
        if trigger is not None:
            rule.trigger = trigger
        if action is not None:
            rule.action = action
        rule.updated_at = _now_iso()
        self._automation_repository.save(rule)
        return rule

    def delete_rule(self, rule_id: str) -> None:
        self._automation_repository.delete(rule_id)

    def enable_rule(self, rule_id: str) -> AutomationRule:
        rule = self._automation_repository.get(rule_id)
        rule.enable()
        rule.updated_at = _now_iso()
        self._automation_repository.save(rule)
        return rule

    def disable_rule(self, rule_id: str) -> AutomationRule:
        rule = self._automation_repository.get(rule_id)
        rule.disable()
        rule.updated_at = _now_iso()
        self._automation_repository.save(rule)
        return rule
