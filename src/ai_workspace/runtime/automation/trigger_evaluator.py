from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta

from ai_workspace.domain.automation import AutomationRule

_WEEKDAY_NAMES = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


class TriggerEvaluator(ABC):
    """Trigger 종류별 "언제 발동해야 하는가" 판단을 전담하는
    계층(M21-T03, 사용자 승인 조건 1 — `AutomationScheduler`와
    Trigger의 책임을 분리한다). `AutomationScheduler`는 이 Interface
    만 통해 평가하고, 각 Trigger 종류가 어떻게 "지금 발동해야 하는지"
    를 계산하는지는 전혀 알지 못한다."""

    @abstractmethod
    def should_fire(self, rule: AutomationRule, *, now: datetime) -> bool:
        """rule의 Trigger가 now 시점에 발동해야 하면 True."""
        raise NotImplementedError

    @abstractmethod
    def compute_next_execution_at(self, rule: AutomationRule, *, now: datetime) -> str | None:
        """rule의 다음 예정 발동 시각(ISO 8601)을 계산한다. 예정할 수
        없으면(예: Startup) None."""
        raise NotImplementedError


class TimeTriggerEvaluator(TriggerEvaluator):
    """지정된 시각(매일/매주/매월)에 발동하는 Time Trigger 평가기.
    같은 날 중복 발동을 막기 위해 `last_executed_at`의 날짜와 오늘
    날짜를 비교한다 — Scheduler의 tick 주기가 정확히 목표 분(minute)
    과 일치하지 않아도(예: 30초마다 tick) 놓치지 않는다."""

    def should_fire(self, rule: AutomationRule, *, now: datetime) -> bool:
        trigger = rule.trigger
        assert trigger.time_of_day is not None
        target_hour, target_minute = _parse_time_of_day(trigger.time_of_day)

        if not _day_matches(rule, now):
            return False
        if (now.hour, now.minute) < (target_hour, target_minute):
            return False
        if rule.last_executed_at is None:
            return True
        last = _parse_iso(rule.last_executed_at)
        return last.date() < now.date()

    def compute_next_execution_at(self, rule: AutomationRule, *, now: datetime) -> str | None:
        trigger = rule.trigger
        assert trigger.time_of_day is not None
        target_hour, target_minute = _parse_time_of_day(trigger.time_of_day)

        candidate = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)

        for _ in range(8):
            if _day_matches(rule, candidate):
                return candidate.isoformat()
            candidate += timedelta(days=1)
        return None


class IntervalTriggerEvaluator(TriggerEvaluator):
    """`interval_seconds`마다 발동하는 Interval Trigger 평가기.
    `last_executed_at`(없으면 `created_at`)을 기준으로 경과 시간을
    계산한다."""

    def should_fire(self, rule: AutomationRule, *, now: datetime) -> bool:
        interval_seconds = rule.trigger.interval_seconds
        assert interval_seconds is not None
        base = _parse_iso(rule.last_executed_at or rule.created_at)
        return now >= base + timedelta(seconds=interval_seconds)

    def compute_next_execution_at(self, rule: AutomationRule, *, now: datetime) -> str | None:
        interval_seconds = rule.trigger.interval_seconds
        assert interval_seconds is not None
        base = _parse_iso(rule.last_executed_at or rule.created_at)
        return (base + timedelta(seconds=interval_seconds)).isoformat()


class StartupTriggerEvaluator(TriggerEvaluator):
    """Workspace(서버) 시작 시 한 번만 발동하는 Startup Trigger
    평가기. 주기적 `tick()`이 아니라 `AutomationScheduler.start()`
    에서 별도로 평가된다 — 아직 한 번도 발동하지 않은
    (`last_executed_at is None`) Rule만 발동 대상이다."""

    def should_fire(self, rule: AutomationRule, *, now: datetime) -> bool:
        return rule.last_executed_at is None

    def compute_next_execution_at(self, rule: AutomationRule, *, now: datetime) -> str | None:
        return None


class EventTriggerEvaluator(TriggerEvaluator):
    """Workspace Event 발생 시 발동하는 Event Trigger 평가기(M21-T04).
    `AutomationScheduler`가 `EventBus`를 구독해 `event_type`이
    일치하는 Rule에 대해서만 이 평가기를 호출하므로(사전 필터링은
    Scheduler 책임), `should_fire`는 항상 True다 — event가 이미
    일치를 확인한 뒤에만 불린다. 일정 기반이 아니므로 다음 예정
    시각은 계산할 수 없다."""

    def should_fire(self, rule: AutomationRule, *, now: datetime) -> bool:
        return True

    def compute_next_execution_at(self, rule: AutomationRule, *, now: datetime) -> str | None:
        return None


def _parse_time_of_day(value: str) -> tuple[int, int]:
    hour_str, minute_str = value.split(":")
    return int(hour_str), int(minute_str)


def _day_matches(rule: AutomationRule, when: datetime) -> bool:
    trigger = rule.trigger
    if trigger.day_of_week is not None:
        return _WEEKDAY_NAMES[when.weekday()] == trigger.day_of_week
    if trigger.day_of_month is not None:
        return when.day == trigger.day_of_month
    return True


def utc_now() -> datetime:
    return datetime.now(UTC)
