from __future__ import annotations

import uuid

from ai_workspace.domain.automation import Action, ActionKind, AutomationRule
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_registry import EngineRegistry
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher


class AutomationActionNotSupportedError(Exception):
    """아직 실제로 실행할 수 없는 Action Kind에 대해 발생한다(예:
    RUN_WORKFLOW — M21은 Task 단위 실행만 다룬다)."""


class AutomationActionExecutor:
    """`AutomationRule.action`을 실제로 실행하는 유일한 통로(M21-T04,
    사용자 승인 조건 5 — `ExecutionDispatcher`를 유일한 실행
    진입점으로 유지한다). `AutomationScheduler`(M21-T03)의
    `action_executor` 콜러블로 주입된다 — Scheduler는 이 클래스의
    내부 구현을 전혀 모른다.

    RUN_TASK는 M17/M18 파이프라인을 그대로 재사용한다: 새 `Task`
    생성 → `EngineRegistry.list_candidates()`로 후보 조회 →
    `EngineSelectionPolicy.select()`로 Decision 판단 →
    `ExecutionDispatcher.dispatch()`로 실행. 이 클래스는 새로운
    실행 경로를 만들지 않는다.

    DASHBOARD_REFRESH/NOTIFICATION은 `ExecutionDispatcher`를 거칠
    Task가 없으므로 아무것도 실행하지 않는다(Dashboard는 이미
    `ExecutionDispatcher`가 발행하는 Event로 갱신되고, 실제 알림
    발송은 Out of Scope). RUN_WORKFLOW는 이번 Milestone이 다루는
    실행 경로가 Task 단위뿐이라 아직 지원하지 않는다
    (`AutomationActionNotSupportedError`)."""

    def __init__(
        self,
        *,
        engine_registry: EngineRegistry,
        engine_selection_policy: EngineSelectionPolicy,
        execution_dispatcher: ExecutionDispatcher,
    ) -> None:
        self._engine_registry = engine_registry
        self._engine_selection_policy = engine_selection_policy
        self._execution_dispatcher = execution_dispatcher

    def __call__(self, rule: AutomationRule) -> None:
        action = rule.action
        if action.kind is ActionKind.RUN_TASK:
            self._run_task(action)
        elif action.kind is ActionKind.RUN_WORKFLOW:
            raise AutomationActionNotSupportedError(action.kind.value)
        elif action.kind in (ActionKind.DASHBOARD_REFRESH, ActionKind.NOTIFICATION):
            return

    def _run_task(self, action: Action) -> None:
        assert action.project_id is not None
        assert action.task_title is not None
        task = Task(
            task_id=str(uuid.uuid4()), project_id=action.project_id, title=action.task_title
        )

        candidates = self._engine_registry.list_candidates(task)
        decision = self._engine_selection_policy.select(task, candidates)
        self._execution_dispatcher.dispatch(decision, task)
