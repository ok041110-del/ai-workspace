from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TriggerKind(Enum):
    """Automation Rule을 발동시키는 조건의 종류(M21). "언제 발동해야
    하는가"의 평가 로직은 여기 없다 — 이 계층은 순수 데이터이고,
    평가는 `runtime/automation/`의 Trigger 평가기(M21-T03/T04,
    사용자 승인 조건 1: Scheduler와 Trigger 책임 분리)가 담당한다."""

    TIME = "time"
    INTERVAL = "interval"
    EVENT = "event"
    STARTUP = "startup"


@dataclass(frozen=True)
class Trigger:
    """4종 Trigger를 하나의 데이터 모양으로 표현한다(kind로 태그된
    Flat 구조 — `ExecutionRecord`(M20)와 동일한 스타일). kind별로
    실제 쓰이는 필드만 채워진다.

    - TIME: `time_of_day`(필수, "HH:MM") + `day_of_week`/`day_of_month`
      (둘 다 선택, 둘 다 없으면 매일).
    - INTERVAL: `interval_seconds`(필수).
    - EVENT: `event_type`(필수, `EventBus`의 `Event.event_type`과
      동일한 문자열 — 예: `ENGINE_EXECUTION_COMPLETED`).
    - STARTUP: 추가 필드 없음."""

    kind: TriggerKind
    time_of_day: str | None = None
    day_of_week: str | None = None
    day_of_month: int | None = None
    interval_seconds: int | None = None
    event_type: str | None = None


class ActionKind(Enum):
    """Automation Rule이 발동됐을 때 수행할 동작의 종류(M21)."""

    RUN_TASK = "run_task"
    RUN_WORKFLOW = "run_workflow"
    DASHBOARD_REFRESH = "dashboard_refresh"
    NOTIFICATION = "notification"


@dataclass(frozen=True)
class Action:
    """4종 Action을 하나의 데이터 모양으로 표현한다(Trigger와 동일한
    kind 태그 스타일).

    - RUN_TASK: `project_id`/`task_title`(둘 다 필수) — 새 `Task`를
      만들어 `ExecutionDispatcher`로 실행한다.
    - RUN_WORKFLOW: `workflow_id`(필수).
    - DASHBOARD_REFRESH: 추가 필드 없음 — `ExecutionDispatcher`를
      거치지 않는다(Task를 실행하지 않으므로).
    - NOTIFICATION: `notification_message`(필수) — 실제 알림 전송은
      Out of Scope, 요청 의도만 표현한다."""

    kind: ActionKind
    project_id: str | None = None
    task_title: str | None = None
    workflow_id: str | None = None
    notification_message: str | None = None


@dataclass
class AutomationRule:
    """조건/일정에 따라 Task를 자동 실행하는 규칙(M21). Dashboard와
    독립적인 Domain이다 — `web/`이나 `Dashboard`를 전혀 참조하지
    않는다.

    `last_executed_at`/`next_execution_at`(사용자 승인 조건 6)은
    M23 Mobile Experience가 그대로 재사용할 수 있도록 이 Milestone
    부터 도메인 모델에 포함한다 — 값 자체는 `AutomationScheduler`가
    채운다(이 도메인 계층은 시간을 계산하지 않는다)."""

    rule_id: str
    name: str
    description: str
    trigger: Trigger
    action: Action
    created_at: str
    updated_at: str
    enabled: bool = True
    last_executed_at: str | None = None
    next_execution_at: str | None = None

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False
