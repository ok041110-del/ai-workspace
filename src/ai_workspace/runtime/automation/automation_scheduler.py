from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from ai_workspace.domain.automation import AutomationRule, TriggerKind
from ai_workspace.interfaces.automation_repository import AutomationRepository
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.runtime.automation.trigger_evaluator import (
    EventTriggerEvaluator,
    IntervalTriggerEvaluator,
    StartupTriggerEvaluator,
    TimeTriggerEvaluator,
    TriggerEvaluator,
    utc_now,
)

ActionExecutor = Callable[[AutomationRule], None]

_PERIODIC_EVALUATORS: dict[TriggerKind, type[TriggerEvaluator]] = {
    TriggerKind.TIME: TimeTriggerEvaluator,
    TriggerKind.INTERVAL: IntervalTriggerEvaluator,
}


class AutomationScheduler:
    """활성 `AutomationRule`을 평가해 발동시키는 Infrastructure Layer
    컴포넌트(M21-T03, 사용자 DoD — "Scheduler는 Server Runtime과
    함께 실행된다"). Rule을 별도로 등록/보관하지 않는다 — 매
    `tick()`마다 `AutomationRepository`를 다시 조회해 활성 Rule
    목록을 얻는다. 이렇게 하면 "Rule 등록/제거/활성화/비활성화"는
    `AutomationService`(공유하는 동일 Repository를 통해 CRUD를
    수행하는 유일한 진입점, 사용자 승인 조건 3)를 거치기만 하면 이
    Scheduler에 자동으로 반영된다 — 별도 동기화가 필요 없다.

    **Trigger 평가와 완전히 분리**(사용자 승인 조건 1): 이 클래스는
    "지금 발동해야 하는가"를 스스로 판단하지 않고
    `TriggerEvaluator`에게 위임한다. Event Trigger는 `tick()`/
    `start()`가 다루지 않는다 — 주기 평가 대상이 아니라
    `bind_event_bus()`로 별도 구독한다(M21-T04).

    **실행은 `action_executor`에 위임**(사용자 승인 조건 5 —
    `ExecutionDispatcher`가 유일한 실행 진입점): 이 클래스는
    `ExecutionDispatcher`를 알지 못한다. Action을 실제로 실행하는
    방법(M21-T04의 `AutomationActionExecutor` —
    `EngineSelectionPolicy`→`ExecutionDispatcher`로 연결)은 생성자로
    주입된 콜러블이 담당한다."""

    def __init__(
        self, *, automation_repository: AutomationRepository, action_executor: ActionExecutor
    ) -> None:
        self._automation_repository = automation_repository
        self._action_executor = action_executor
        self._startup_evaluator = StartupTriggerEvaluator()
        self._event_evaluator = EventTriggerEvaluator()

    def start(self, *, now: datetime | None = None) -> None:
        """Workspace(서버) 시작 시 한 번 호출한다 — Startup Trigger만
        평가한다."""
        moment = now or utc_now()
        for rule in self._enabled_rules_with_kind(TriggerKind.STARTUP):
            if self._startup_evaluator.should_fire(rule, now=moment):
                self._fire(rule, moment)

    def tick(self, *, now: datetime | None = None) -> None:
        """Time/Interval Trigger를 주기적으로 평가한다. 실제 주기적
        호출(타이머/백그라운드 루프)은 Server Runtime 기동 시
        연결한다(M21-T05) — 이 메서드 자체는 순수하게 한 번의 평가
        Pass만 수행해 고정된 `now`로 결정적으로 테스트할 수 있다."""
        moment = now or utc_now()
        for rule in self._automation_repository.list_rules():
            if not rule.enabled:
                continue
            evaluator_cls = _PERIODIC_EVALUATORS.get(rule.trigger.kind)
            if evaluator_cls is None:
                continue
            evaluator = evaluator_cls()
            if evaluator.should_fire(rule, now=moment):
                self._fire(rule, moment)
            rule.next_execution_at = evaluator.compute_next_execution_at(rule, now=moment)
            self._automation_repository.save(rule)

    def bind_event_bus(self, event_bus: EventBus) -> None:
        """Event Trigger를 위해 `EventBus`를 구독한다(M21-T04).
        `AutomationScheduler`는 이벤트를 받을 뿐 발행하지 않는다 —
        `ExecutionDispatcher`가 Dashboard를 모르는 것과 동일하게,
        이 Scheduler도 Event의 발행처(Dashboard 등)를 알 필요가
        없다."""
        event_bus.subscribe(self._on_event)

    def _on_event(self, event: Event) -> None:
        now = utc_now()
        for rule in self._automation_repository.list_rules():
            if not rule.enabled or rule.trigger.kind is not TriggerKind.EVENT:
                continue
            if rule.trigger.event_type != event.event_type:
                continue
            if self._event_evaluator.should_fire(rule, now=now):
                self._fire(rule, now)

    def _enabled_rules_with_kind(self, kind: TriggerKind) -> list[AutomationRule]:
        return [
            rule
            for rule in self._automation_repository.list_rules()
            if rule.enabled and rule.trigger.kind is kind
        ]

    def _fire(self, rule: AutomationRule, now: datetime) -> None:
        rule.last_executed_at = now.isoformat()
        self._automation_repository.save(rule)
        try:
            self._action_executor(rule)
        except Exception:
            # EventBus.publish()와 동일한 원칙: 한 Rule의 Action 실행
            # 실패가 다른 Rule 평가나 호출자(EventBus 구독 경로 등)에
            # 영향을 주지 않는다. last_executed_at은 "실행을 시도한
            # 시점"을 기록할 뿐, 성공을 보장하지 않는다.
            pass
