import pytest

from ai_workspace.domain.automation import Action, ActionKind, AutomationRule, Trigger, TriggerKind
from ai_workspace.interfaces.automation_repository import AutomationRuleNotFoundError
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository


def make_rule(rule_id: str = "r1") -> AutomationRule:
    return AutomationRule(
        rule_id=rule_id,
        name="매일 정리",
        description="매일 09:00에 정리 작업 실행",
        trigger=Trigger(kind=TriggerKind.TIME, time_of_day="09:00"),
        action=Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="정리 작업"),
        created_at="2026-07-27T00:00:00Z",
        updated_at="2026-07-27T00:00:00Z",
    )


def test_save_then_get_returns_same_rule() -> None:
    repository = InMemoryAutomationRepository()
    rule = make_rule()

    repository.save(rule)

    assert repository.get("r1") == rule


def test_save_is_idempotent_upsert() -> None:
    repository = InMemoryAutomationRepository()
    rule = make_rule()
    repository.save(rule)

    rule.disable()
    repository.save(rule)

    assert repository.get("r1").enabled is False


def test_get_unknown_rule_raises() -> None:
    repository = InMemoryAutomationRepository()

    with pytest.raises(AutomationRuleNotFoundError):
        repository.get("missing")


def test_delete_removes_rule() -> None:
    repository = InMemoryAutomationRepository()
    repository.save(make_rule())

    repository.delete("r1")

    with pytest.raises(AutomationRuleNotFoundError):
        repository.get("r1")


def test_delete_unknown_rule_raises() -> None:
    repository = InMemoryAutomationRepository()

    with pytest.raises(AutomationRuleNotFoundError):
        repository.delete("missing")


def test_list_rules_returns_all_saved_rules() -> None:
    repository = InMemoryAutomationRepository()
    repository.save(make_rule("r1"))
    repository.save(make_rule("r2"))

    rules = repository.list_rules()

    assert {rule.rule_id for rule in rules} == {"r1", "r2"}


def test_list_rules_returns_defensive_copy() -> None:
    repository = InMemoryAutomationRepository()
    repository.save(make_rule())

    rules = repository.list_rules()
    rules.clear()

    assert len(repository.list_rules()) == 1
