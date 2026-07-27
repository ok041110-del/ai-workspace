import pytest

from ai_workspace.domain.automation import Action, ActionKind, Trigger, TriggerKind
from ai_workspace.interfaces.automation_repository import AutomationRuleNotFoundError
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_service import AutomationService


def make_service() -> AutomationService:
    return AutomationService(automation_repository=InMemoryAutomationRepository())


def make_trigger() -> Trigger:
    return Trigger(kind=TriggerKind.TIME, time_of_day="09:00")


def make_action() -> Action:
    return Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="정리 작업")


def test_create_rule_assigns_id_and_timestamps() -> None:
    service = make_service()

    rule = service.create_rule(
        name="매일 정리",
        description="매일 09:00 정리",
        trigger=make_trigger(),
        action=make_action(),
    )

    assert rule.rule_id
    assert rule.created_at == rule.updated_at
    assert rule.enabled is True


def test_create_rule_can_start_disabled() -> None:
    service = make_service()

    rule = service.create_rule(
        name="매일 정리",
        description="매일 09:00 정리",
        trigger=make_trigger(),
        action=make_action(),
        enabled=False,
    )

    assert rule.enabled is False


def test_get_rule_returns_created_rule() -> None:
    service = make_service()
    created = service.create_rule(
        name="매일 정리",
        description="매일 09:00 정리",
        trigger=make_trigger(),
        action=make_action(),
    )

    fetched = service.get_rule(created.rule_id)

    assert fetched == created


def test_get_unknown_rule_raises() -> None:
    service = make_service()

    with pytest.raises(AutomationRuleNotFoundError):
        service.get_rule("missing")


def test_list_rules_returns_all_created_rules() -> None:
    service = make_service()
    service.create_rule(
        name="A", description="A", trigger=make_trigger(), action=make_action()
    )
    service.create_rule(
        name="B", description="B", trigger=make_trigger(), action=make_action()
    )

    rules = service.list_rules()

    assert {rule.name for rule in rules} == {"A", "B"}


def test_update_rule_changes_only_given_fields() -> None:
    service = make_service()
    created = service.create_rule(
        name="매일 정리", description="원래 설명", trigger=make_trigger(), action=make_action()
    )

    updated = service.update_rule(created.rule_id, description="새 설명")

    assert updated.name == "매일 정리"
    assert updated.description == "새 설명"


def test_update_rule_bumps_updated_at() -> None:
    service = make_service()
    created = service.create_rule(
        name="매일 정리", description="원래 설명", trigger=make_trigger(), action=make_action()
    )

    updated = service.update_rule(created.rule_id, name="새 이름")

    assert updated.created_at == created.created_at


def test_update_unknown_rule_raises() -> None:
    service = make_service()

    with pytest.raises(AutomationRuleNotFoundError):
        service.update_rule("missing", name="새 이름")


def test_delete_rule_removes_it() -> None:
    service = make_service()
    created = service.create_rule(
        name="매일 정리", description="설명", trigger=make_trigger(), action=make_action()
    )

    service.delete_rule(created.rule_id)

    with pytest.raises(AutomationRuleNotFoundError):
        service.get_rule(created.rule_id)


def test_enable_and_disable_rule() -> None:
    service = make_service()
    created = service.create_rule(
        name="매일 정리",
        description="설명",
        trigger=make_trigger(),
        action=make_action(),
        enabled=False,
    )

    enabled = service.enable_rule(created.rule_id)
    assert enabled.enabled is True

    disabled = service.disable_rule(created.rule_id)
    assert disabled.enabled is False
