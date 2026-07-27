from ai_workspace.domain.automation import (
    Action,
    ActionKind,
    AutomationRule,
    Trigger,
    TriggerKind,
)


def test_trigger_kind_covers_expected_kinds() -> None:
    assert {kind.value for kind in TriggerKind} == {
        "time",
        "interval",
        "event",
        "startup",
    }


def test_action_kind_covers_expected_kinds() -> None:
    assert {kind.value for kind in ActionKind} == {
        "run_task",
        "run_workflow",
        "dashboard_refresh",
        "notification",
    }


def test_time_trigger_holds_given_fields() -> None:
    trigger = Trigger(kind=TriggerKind.TIME, time_of_day="09:00", day_of_week="monday")

    assert trigger.time_of_day == "09:00"
    assert trigger.day_of_week == "monday"
    assert trigger.interval_seconds is None
    assert trigger.event_type is None


def test_interval_trigger_holds_interval_seconds() -> None:
    trigger = Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300)

    assert trigger.interval_seconds == 300


def test_event_trigger_holds_event_type() -> None:
    trigger = Trigger(kind=TriggerKind.EVENT, event_type="engine_execution_completed")

    assert trigger.event_type == "engine_execution_completed"


def test_startup_trigger_needs_no_extra_fields() -> None:
    trigger = Trigger(kind=TriggerKind.STARTUP)

    assert trigger.time_of_day is None
    assert trigger.interval_seconds is None
    assert trigger.event_type is None


def test_run_task_action_holds_given_fields() -> None:
    action = Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="정리 작업")

    assert action.project_id == "p1"
    assert action.task_title == "정리 작업"


def test_notification_action_holds_message() -> None:
    action = Action(kind=ActionKind.NOTIFICATION, notification_message="작업이 완료됐습니다")

    assert action.notification_message == "작업이 완료됐습니다"


def test_automation_rule_defaults_to_enabled_and_no_execution_history() -> None:
    rule = AutomationRule(
        rule_id="r1",
        name="매일 정리",
        description="매일 09:00에 정리 작업 실행",
        trigger=Trigger(kind=TriggerKind.TIME, time_of_day="09:00"),
        action=Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="정리 작업"),
        created_at="2026-07-27T00:00:00Z",
        updated_at="2026-07-27T00:00:00Z",
    )

    assert rule.enabled is True
    assert rule.last_executed_at is None
    assert rule.next_execution_at is None


def test_automation_rule_enable_and_disable() -> None:
    rule = AutomationRule(
        rule_id="r1",
        name="매일 정리",
        description="매일 09:00에 정리 작업 실행",
        trigger=Trigger(kind=TriggerKind.STARTUP),
        action=Action(kind=ActionKind.DASHBOARD_REFRESH),
        created_at="2026-07-27T00:00:00Z",
        updated_at="2026-07-27T00:00:00Z",
    )

    rule.disable()
    assert rule.enabled is False

    rule.enable()
    assert rule.enabled is True
