import pytest
from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.automation import Action, ActionKind, AutomationRule, Trigger, TriggerKind
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.automation.automation_action_executor import (
    AutomationActionExecutor,
    AutomationActionNotSupportedError,
)
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher

_TRIGGER = Trigger(kind=TriggerKind.STARTUP)


def make_rule(action: Action) -> AutomationRule:
    return AutomationRule(
        rule_id="r1",
        name="테스트 Rule",
        description="설명",
        trigger=_TRIGGER,
        action=action,
        created_at="2026-07-27T00:00:00",
        updated_at="2026-07-27T00:00:00",
    )


def make_executor() -> tuple[AutomationActionExecutor, FakeExecutionEnvironment]:
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(returncode=0, stdout="ok", stderr="")
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code",
        ClaudeCodeEngineAdapter(
            execution_environment=execution_environment, subprocess_timeout_seconds=5.0
        ),
    )
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    executor = AutomationActionExecutor(
        engine_registry=registry,
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        execution_dispatcher=dispatcher,
    )
    return executor, execution_environment


def test_run_task_action_executes_via_execution_dispatcher_pipeline() -> None:
    executor, execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.RUN_TASK, project_id="p1", task_title="정리 작업"))

    executor(rule)

    assert len(execution_environment.executed_commands) == 1


def test_dashboard_refresh_action_does_nothing() -> None:
    executor, execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.DASHBOARD_REFRESH))

    executor(rule)

    assert execution_environment.executed_commands == []


def test_notification_action_does_nothing() -> None:
    executor, execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.NOTIFICATION, notification_message="완료"))

    executor(rule)

    assert execution_environment.executed_commands == []


def test_run_workflow_action_raises_not_supported() -> None:
    executor, _execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.RUN_WORKFLOW, workflow_id="w1"))

    with pytest.raises(AutomationActionNotSupportedError):
        executor(rule)
