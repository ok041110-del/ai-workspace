from datetime import datetime

from ai_workspace.domain.automation import Action, ActionKind, AutomationRule, Trigger, TriggerKind
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler

_ACTION = Action(kind=ActionKind.DASHBOARD_REFRESH)


def make_rule(
    rule_id: str,
    trigger: Trigger,
    *,
    enabled: bool = True,
    created_at: str = "2026-07-27T00:00:00",
    last_executed_at: str | None = None,
) -> AutomationRule:
    return AutomationRule(
        rule_id=rule_id,
        name="테스트 Rule",
        description="설명",
        trigger=trigger,
        action=_ACTION,
        created_at=created_at,
        updated_at=created_at,
        enabled=enabled,
        last_executed_at=last_executed_at,
    )


SchedulerFixture = tuple[AutomationScheduler, InMemoryAutomationRepository, list[AutomationRule]]


def make_scheduler() -> SchedulerFixture:
    repository = InMemoryAutomationRepository()
    fired: list[AutomationRule] = []
    scheduler = AutomationScheduler(
        automation_repository=repository, action_executor=fired.append
    )
    return scheduler, repository, fired


def test_start_fires_startup_rule_once() -> None:
    scheduler, repository, fired = make_scheduler()
    rule = make_rule("r1", Trigger(kind=TriggerKind.STARTUP))
    repository.save(rule)

    scheduler.start(now=datetime(2026, 7, 27, 0, 0))

    assert len(fired) == 1
    assert fired[0].rule_id == "r1"
    assert repository.get("r1").last_executed_at is not None


def test_start_does_not_refire_startup_rule_on_second_call() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.STARTUP)))

    scheduler.start(now=datetime(2026, 7, 27, 0, 0))
    scheduler.start(now=datetime(2026, 7, 27, 0, 1))

    assert len(fired) == 1


def test_start_ignores_disabled_startup_rule() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.STARTUP), enabled=False))

    scheduler.start(now=datetime(2026, 7, 27, 0, 0))

    assert fired == []


def test_start_ignores_non_startup_rules() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule("r1", Trigger(kind=TriggerKind.INTERVAL, interval_seconds=60))
    )

    scheduler.start(now=datetime(2026, 7, 27, 0, 0))

    assert fired == []


def test_tick_fires_due_time_rule() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.TIME, time_of_day="09:00")))

    scheduler.tick(now=datetime(2026, 7, 27, 9, 5))

    assert len(fired) == 1
    assert repository.get("r1").last_executed_at is not None


def test_tick_does_not_fire_time_rule_before_target() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.TIME, time_of_day="09:00")))

    scheduler.tick(now=datetime(2026, 7, 27, 8, 0))

    assert fired == []


def test_tick_fires_due_interval_rule() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule(
            "r1",
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
        )
    )

    scheduler.tick(now=datetime(2026, 7, 27, 9, 5, 1))

    assert len(fired) == 1


def test_tick_updates_next_execution_at() -> None:
    scheduler, repository, _fired = make_scheduler()
    repository.save(
        make_rule(
            "r1",
            Trigger(kind=TriggerKind.INTERVAL, interval_seconds=300),
            created_at="2026-07-27T09:00:00",
        )
    )

    scheduler.tick(now=datetime(2026, 7, 27, 9, 1))

    assert repository.get("r1").next_execution_at == datetime(2026, 7, 27, 9, 5).isoformat()


def test_tick_skips_disabled_rules() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule("r1", Trigger(kind=TriggerKind.TIME, time_of_day="09:00"), enabled=False)
    )

    scheduler.tick(now=datetime(2026, 7, 27, 9, 5))

    assert fired == []
    assert repository.get("r1").next_execution_at is None


def test_tick_skips_startup_and_event_rules() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.STARTUP)))
    repository.save(make_rule("r2", Trigger(kind=TriggerKind.EVENT, event_type="x")))

    scheduler.tick(now=datetime(2026, 7, 27, 9, 5))

    assert fired == []


def test_bind_event_bus_fires_rule_on_matching_event() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule("r1", Trigger(kind=TriggerKind.EVENT, event_type="engine_execution_completed"))
    )
    event_bus = InMemoryEventBus()
    scheduler.bind_event_bus(event_bus)

    event_bus.publish(
        Event(event_id="e1", event_type="engine_execution_completed", payload={})
    )

    assert len(fired) == 1
    assert repository.get("r1").last_executed_at is not None


def test_bind_event_bus_ignores_non_matching_event_type() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule("r1", Trigger(kind=TriggerKind.EVENT, event_type="engine_execution_completed"))
    )
    event_bus = InMemoryEventBus()
    scheduler.bind_event_bus(event_bus)

    event_bus.publish(Event(event_id="e1", event_type="other_event", payload={}))

    assert fired == []


def test_bind_event_bus_ignores_disabled_rule() -> None:
    scheduler, repository, fired = make_scheduler()
    repository.save(
        make_rule(
            "r1",
            Trigger(kind=TriggerKind.EVENT, event_type="engine_execution_completed"),
            enabled=False,
        )
    )
    event_bus = InMemoryEventBus()
    scheduler.bind_event_bus(event_bus)

    event_bus.publish(
        Event(event_id="e1", event_type="engine_execution_completed", payload={})
    )

    assert fired == []


def test_action_executor_exception_does_not_break_other_rules() -> None:
    repository = InMemoryAutomationRepository()
    fired: list[str] = []

    def flaky_executor(rule: AutomationRule) -> None:
        if rule.rule_id == "r1":
            raise RuntimeError("boom")
        fired.append(rule.rule_id)

    scheduler = AutomationScheduler(
        automation_repository=repository, action_executor=flaky_executor
    )
    repository.save(make_rule("r1", Trigger(kind=TriggerKind.STARTUP)))
    repository.save(make_rule("r2", Trigger(kind=TriggerKind.STARTUP)))

    scheduler.start(now=datetime(2026, 7, 27, 0, 0))

    assert fired == ["r2"]
    assert repository.get("r1").last_executed_at is not None
