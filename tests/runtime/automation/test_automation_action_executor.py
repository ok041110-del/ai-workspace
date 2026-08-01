import pytest
from tests.interfaces.fakes import FakeEventBus, FakeExecutionEnvironment, FakeTaskEngine

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.automation import Action, ActionKind, AutomationRule, Trigger, TriggerKind
from ai_workspace.domain.task import TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.automation.automation_action_executor import (
    AutomationActionExecutor,
    AutomationActionNotSupportedError,
)
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.execution.recommendation_execution_service import (
    RecommendationExecutionService,
)
from ai_workspace.runtime.execution.recommendation_orchestration_service import (
    RecommendationOrchestrationService,
)
from ai_workspace.runtime.workflow.workflow_repository import InMemoryWorkflowRepository
from ai_workspace.runtime.workflow.workflow_runner import WorkflowRunner

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


def test_run_workflow_action_raises_not_supported_without_injected_collaborators() -> None:
    executor, _execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.RUN_WORKFLOW, workflow_id="w1"))

    with pytest.raises(AutomationActionNotSupportedError):
        executor(rule)


def test_run_workflow_action_looks_up_workflow_and_runs_it_via_workflow_runner() -> None:
    """M59(ADR-0077): workflow_repository/workflow_runner를 둘 다 주입하면
    workflow_id로 실제 Workflow를 조회해 WorkflowRunner에 위임한다."""
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

    task_engine = FakeTaskEngine()
    task = task_engine.create_task("p1", "Workflow Task")
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=[task.task_id])
    workflow_repository = InMemoryWorkflowRepository()
    workflow_repository.save(workflow)

    event_bus = FakeEventBus()

    def complete_task(event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        completed_task = task_engine.get_task(event.payload["task_id"])
        task_engine.transition(completed_task, TaskStatus.IN_PROGRESS)
        task_engine.transition(completed_task, TaskStatus.REVIEW)
        task_engine.transition(completed_task, TaskStatus.DONE)

    event_bus.subscribe(complete_task)
    workflow_runner = WorkflowRunner(
        workflow_engine=InMemoryWorkflowEngine(), event_bus=event_bus, task_engine=task_engine
    )

    executor = AutomationActionExecutor(
        engine_registry=registry,
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        execution_dispatcher=dispatcher,
        workflow_repository=workflow_repository,
        workflow_runner=workflow_runner,
    )
    rule = make_rule(Action(kind=ActionKind.RUN_WORKFLOW, workflow_id="w1"))

    executor(rule)

    assert task_engine.get_task(task.task_id).status == TaskStatus.DONE


def test_run_recommendation_action_raises_not_supported_without_injected_service() -> None:
    executor, _execution_environment = make_executor()
    rule = make_rule(Action(kind=ActionKind.RUN_RECOMMENDATION))

    with pytest.raises(AutomationActionNotSupportedError):
        executor(rule)


def test_run_recommendation_action_calls_recommendation_execution_service_publish(
    tmp_path,
) -> None:
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

    vault_adapter = VaultAdapter(tmp_path)
    agent_adapter = AgentAdapter(
        InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler()
    )
    recommendation_service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter, agent_adapter),
        CapabilityIntelligenceService(agent_adapter, vault_adapter),
    )
    recommendation_execution_service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    experience_service = ExperienceIntelligenceService(vault_adapter, execution_memory_store)
    recommendation_orchestration_service = RecommendationOrchestrationService(
        experience_service,
        recommendation_service,
        recommendation_execution_service,
    )
    executor = AutomationActionExecutor(
        engine_registry=registry,
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        execution_dispatcher=dispatcher,
        recommendation_orchestration_service=recommendation_orchestration_service,
    )
    rule = make_rule(Action(kind=ActionKind.RUN_RECOMMENDATION))

    executor(rule)

    published_path = tmp_path / "15 Project Intelligence" / "Recommendation Execution.md"
    assert published_path.exists()
