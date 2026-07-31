from pathlib import Path

from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.domain.execution_memory import ExecutionMemory
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.intelligence.recommendation_explanation_service import (
    RecommendationExplanationService,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.execution.recommendation_execution_service import (
    RecommendationExecutionService,
)
from ai_workspace.runtime.execution.recommendation_orchestration_service import (
    RecommendationOrchestrationService,
)


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def _make_orchestration_service(
    vault_root: Path,
    execution_memory_store: ExecutionMemoryStore,
    explanation_service: RecommendationExplanationService | None = None,
) -> tuple[RecommendationOrchestrationService, FakeExecutionEnvironment]:
    vault_adapter = VaultAdapter(vault_root)
    recommendation_service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )
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
    execution_service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
        execution_memory_store,
    )
    experience_service = ExperienceIntelligenceService(vault_adapter, execution_memory_store)
    service = RecommendationOrchestrationService(
        experience_service, recommendation_service, execution_service, explanation_service
    )
    return service, execution_environment


def test_execute_runs_next_task_when_no_experience_recorded(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M43-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M43",
        owner="AI",
        created="2026-07-31",
        updated="2026-07-31",
    )
    vault_adapter.create_task(
        "M43-T02",
        "Gate",
        status="todo",
        priority="high",
        milestone="M43",
        owner="AI",
        created="2026-07-31",
        updated="2026-07-31",
    )
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    service, execution_environment = _make_orchestration_service(tmp_path, execution_memory_store)

    outcome = service.execute(manual_trigger=True)

    assert outcome.gate_decision.approved is True
    assert outcome.action is not None
    assert outcome.action.task_title == "Gate"
    assert len(execution_environment.executed_commands) == 1


def test_execute_withholds_recommendation_when_target_has_only_failed_before(
    tmp_path: Path,
) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M43-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M43",
        owner="AI",
        created="2026-07-31",
        updated="2026-07-31",
    )
    vault_adapter.create_task(
        "M43-T02",
        "Gate",
        status="todo",
        priority="high",
        milestone="M43",
        owner="AI",
        created="2026-07-31",
        updated="2026-07-31",
    )
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    execution_memory_store.record(
        ExecutionMemory(
            task_id="M43-T02",
            action="Gate",
            result="failure",
            timestamp="2026-07-31T00:00:00",
            reason="boom",
        )
    )
    service, execution_environment = _make_orchestration_service(tmp_path, execution_memory_store)

    outcome = service.execute(manual_trigger=True)

    assert outcome.gate_decision.approved is False
    assert outcome.action is None
    assert execution_environment.executed_commands == []


def test_publish_writes_recommendation_execution_file(tmp_path: Path) -> None:
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    service, _execution_environment = _make_orchestration_service(tmp_path, execution_memory_store)

    outcome, path = service.publish(manual_trigger=False)

    assert path == tmp_path / "15 Project Intelligence" / "Recommendation Execution.md"
    assert path.exists()
    assert outcome.gate_decision.approved is False


def test_publish_without_explanation_service_does_not_write_explanation_file(
    tmp_path: Path,
) -> None:
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    service, _execution_environment = _make_orchestration_service(tmp_path, execution_memory_store)

    service.publish(manual_trigger=False)

    assert not (tmp_path / "15 Project Intelligence" / "Recommendation Explanation.md").exists()


def test_publish_with_explanation_service_writes_explanation_file(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    execution_memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    explanation_service = RecommendationExplanationService(vault_adapter)
    service, _execution_environment = _make_orchestration_service(
        tmp_path, execution_memory_store, explanation_service
    )

    service.publish(manual_trigger=False)

    path = tmp_path / "15 Project Intelligence" / "Recommendation Explanation.md"
    assert path.exists()
    assert "Recommendation Explanation" in path.read_text(encoding="utf-8")
