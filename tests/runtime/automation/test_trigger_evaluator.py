from datetime import datetime

from ai_workspace.domain.automation import Action, ActionKind, AutomationRule, Trigger, TriggerKind
from ai_workspace.runtime.automation.trigger_evaluator import (
    IntervalTriggerEvaluator,
    StartupTriggerEvaluator,
    TimeTriggerEvaluator,
)

_ACTION = Action(kind=ActionKind.DASHBOARD_REFRESH)


def make_rule(
    trigger: Trigger,
    *,
    created_at: str = "2026-07-27T00:00:00",
    last_executed_at: str | None = None,
) -> AutomationRule:
    return AutomationRule(
        rule_id="r1",
        name="테스트 Rule",
        description="설명",
        trigger=trigger,
        action=_ACTION,
        created_at=created_at,
        updated_at=created_at,
        last_executed_at=last_executed_at,
    )


class TestTimeTriggerEvaluator:
    def test_fires_after_target_time_when_never_executed(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.TIME, time_of_day="09:00"))

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 5)) is True

    def test_does_not_fire_before_target_time(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.TIME, time_of_day="09:00"))

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 8, 59)) is False

    def test_does_not_refire_same_day(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.TIME, time_of_day="09:00"),
            last_executed_at="2026-07-27T09:00:00",
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 30)) is False

    def test_fires_again_next_day(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.TIME, time_of_day="09:00"),
            last_executed_at="2026-07-27T09:00:00",
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 28, 9, 5)) is True

    def test_day_of_week_constraint(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.TIME, time_of_day="09:00", day_of_week="monday")
        )

        # 2026-07-27 is a Monday
        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 5)) is True
        # 2026-07-28 is a Tuesday
        assert evaluator.should_fire(rule, now=datetime(2026, 7, 28, 9, 5)) is False

    def test_day_of_month_constraint(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.TIME, time_of_day="09:00", day_of_month=1))

        assert evaluator.should_fire(rule, now=datetime(2026, 8, 1, 9, 5)) is True
        assert evaluator.should_fire(rule, now=datetime(2026, 8, 2, 9, 5)) is False

    def test_compute_next_execution_at_today_when_not_yet_passed(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.TIME, time_of_day="09:00"))

        next_at = evaluator.compute_next_execution_at(rule, now=datetime(2026, 7, 27, 8, 0))

        assert next_at == datetime(2026, 7, 27, 9, 0).isoformat()

    def test_compute_next_execution_at_tomorrow_when_already_passed(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.TIME, time_of_day="09:00"))

        next_at = evaluator.compute_next_execution_at(rule, now=datetime(2026, 7, 27, 10, 0))

        assert next_at == datetime(2026, 7, 28, 9, 0).isoformat()

    def test_compute_next_execution_at_respects_day_of_week(self) -> None:
        evaluator = TimeTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.TIME, time_of_day="09:00", day_of_week="monday")
        )

        # 2026-07-27 is Monday 10:00 (already passed today) -> next Monday
        next_at = evaluator.compute_next_execution_at(rule, now=datetime(2026, 7, 27, 10, 0))

        assert next_at == datetime(2026, 8, 3, 9, 0).isoformat()


class TestIntervalTriggerEvaluator:
    def test_fires_after_interval_elapsed_since_creation(self) -> None:
        evaluator = IntervalTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 5, 1)) is True

    def test_does_not_fire_before_interval_elapsed(self) -> None:
        evaluator = IntervalTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 2)) is False

    def test_uses_last_executed_at_when_present(self) -> None:
        evaluator = IntervalTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
            last_executed_at="2026-07-27T09:10:00",
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 12)) is False
        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 9, 16)) is True

    def test_compute_next_execution_at(self) -> None:
        evaluator = IntervalTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
        )

        next_at = evaluator.compute_next_execution_at(rule, now=datetime(2026, 7, 27, 9, 1))

        assert next_at == datetime(2026, 7, 27, 9, 5).isoformat()


class TestStartupTriggerEvaluator:
    def test_fires_when_never_executed(self) -> None:
        evaluator = StartupTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.STARTUP))

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 0, 0)) is True

    def test_does_not_refire_once_executed(self) -> None:
        evaluator = StartupTriggerEvaluator()
        rule = make_rule(
            Trigger(kind=TriggerKind.STARTUP), last_executed_at="2026-07-27T00:00:00"
        )

        assert evaluator.should_fire(rule, now=datetime(2026, 7, 27, 0, 1)) is False

    def test_next_execution_at_is_always_none(self) -> None:
        evaluator = StartupTriggerEvaluator()
        rule = make_rule(Trigger(kind=TriggerKind.STARTUP))

        assert evaluator.compute_next_execution_at(rule, now=datetime(2026, 7, 27, 0, 0)) is None
