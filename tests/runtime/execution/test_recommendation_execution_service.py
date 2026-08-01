from pathlib import Path

from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.guardian.models import ArchitectureCheckResult, ArchitectureHealthReport
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.recommendation_service import (
    RecommendationIntelligenceReport,
    RecommendationIntelligenceService,
)
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
    render_markdown,
)


def _make_agent_adapter() -> AgentAdapter:
    return AgentAdapter(InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler())


def _make_recommendation_service(vault_adapter: VaultAdapter) -> RecommendationIntelligenceService:
    return RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter),
        CapabilityIntelligenceService(_make_agent_adapter()),
    )


def _make_service(
    vault_root: Path,
) -> tuple[
    RecommendationExecutionService, RecommendationIntelligenceReport, FakeExecutionEnvironment
]:
    vault_adapter = VaultAdapter(vault_root)
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()

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

    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )
    return service, report, execution_environment


def test_execute_rejects_when_manual_trigger_is_false(tmp_path: Path) -> None:
    service, report, execution_environment = _make_service(tmp_path)

    outcome = service.execute(report, manual_trigger=False)

    assert outcome.gate_decision.approved is False
    assert outcome.result is None
    assert outcome.lifecycle_transitions == []
    assert execution_environment.executed_commands == []


def test_execute_runs_next_task_via_execution_dispatcher(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M36-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M36",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    vault_adapter.create_task(
        "M36-T02",
        "Gate",
        status="todo",
        priority="high",
        milestone="M36",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()
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
    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )

    outcome = service.execute(report, manual_trigger=True)

    assert outcome.gate_decision.approved is True
    assert outcome.action is not None
    assert outcome.action.task_title == "Gate"
    assert outcome.result is not None
    assert outcome.result.success is True
    assert len(execution_environment.executed_commands) == 1
    assert [t.new_status for t in outcome.lifecycle_transitions] == ["in-progress", "review"]
    tasks = {t.task_id: t.status for t in vault_adapter.list_tasks()}
    assert tasks["M36-T02"] == "review"


def test_execute_blocks_ready_task_when_guardian_report_fails(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M48-T01",
        "설계",
        status="done",
        priority="high",
        milestone="M48",
        owner="AI",
        created="2026-08-01",
        updated="2026-08-01",
    )
    vault_adapter.create_task(
        "M48-T02",
        "Gate",
        status="todo",
        priority="high",
        milestone="M48",
        owner="AI",
        created="2026-08-01",
        updated="2026-08-01",
    )
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()
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
    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )
    guardian_report = ArchitectureHealthReport(
        results=(ArchitectureCheckResult(rule_name="r1", passed=False, violations=()),)
    )

    outcome = service.execute(report, manual_trigger=True, guardian_report=guardian_report)

    assert outcome.gate_decision.approved is False
    assert "Architecture Guardian" in outcome.gate_decision.reason
    assert outcome.action is None
    assert outcome.result is None
    assert execution_environment.executed_commands == []
    tasks = {t.task_id: t.status for t in vault_adapter.list_tasks()}
    assert tasks["M48-T02"] == "todo"


def test_execute_reverts_task_to_todo_on_execution_failure(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M37-T01",
        "Gate",
        status="todo",
        priority="high",
        milestone="M37",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(returncode=1, stdout="", stderr="boom")
    registry = InMemoryEngineRegistry()
    registry.register(
        "claude_code",
        ClaudeCodeEngineAdapter(
            execution_environment=execution_environment, subprocess_timeout_seconds=5.0
        ),
    )
    auth = InMemoryAuthenticationManager(frozenset({"claude_code"}))
    dispatcher = ExecutionDispatcher(engine_registry=registry, authentication_manager=auth)
    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )

    outcome = service.execute(report, manual_trigger=True)

    assert outcome.result is not None
    assert outcome.result.success is False
    assert [t.new_status for t in outcome.lifecycle_transitions] == ["in-progress", "todo"]
    tasks = {t.task_id: t.status for t in vault_adapter.list_tasks()}
    assert tasks["M37-T01"] == "todo"


def test_render_markdown_shows_rejected_gate_decision(tmp_path: Path) -> None:
    service, report, _execution_environment = _make_service(tmp_path)

    outcome = service.execute(report, manual_trigger=False)
    markdown = render_markdown(outcome)

    assert "## Gate 판정" in markdown
    assert "거부" in markdown
    assert "## 실행된 Action" not in markdown
    assert "## Task Status 이력" in markdown
    assert "발생한 전이 없음" in markdown


def test_render_markdown_shows_lifecycle_transitions_on_success(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M37-T02",
        "Transitioner",
        status="todo",
        priority="high",
        milestone="M37",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()
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
    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
    )

    markdown = render_markdown(service.execute(report, manual_trigger=True))

    assert "## Task Status 이력" in markdown
    assert "M37-T02: todo → in-progress" in markdown
    assert "M37-T02: in-progress → review" in markdown


def test_publish_writes_recommendation_execution_file(tmp_path: Path) -> None:
    service, report, _execution_environment = _make_service(tmp_path)

    outcome, path = service.publish(report, manual_trigger=False)

    assert path == tmp_path / "15 Project Intelligence" / "Recommendation Execution.md"
    assert path.exists()
    assert outcome.gate_decision.approved is False
    assert "Recommendation Execution" in path.read_text(encoding="utf-8")


def test_execute_records_execution_memory_when_store_injected(tmp_path: Path) -> None:
    vault_adapter = VaultAdapter(tmp_path)
    vault_adapter.create_task(
        "M39-T01",
        "Gate",
        status="todo",
        priority="high",
        milestone="M39",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )
    recommendation_service = _make_recommendation_service(vault_adapter)
    report = recommendation_service.generate()
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
    memory_store = ExecutionMemoryStore(InMemoryMemoryEngine())
    service = RecommendationExecutionService(
        vault_adapter,
        registry,
        InMemoryEngineSelectionPolicy(),
        dispatcher,
        memory_store,
    )

    outcome = service.execute(report, manual_trigger=True)

    records = memory_store.query(task_id="M39-T01")
    assert len(records) == 1
    assert records[0].action == "Gate"
    assert records[0].result == "success"
    assert records[0].reason is None
    assert outcome.result is not None and outcome.result.success is True


def test_execute_skips_memory_recording_when_store_not_injected(tmp_path: Path) -> None:
    service, report, _execution_environment = _make_service(tmp_path)

    outcome = service.execute(report, manual_trigger=False)

    assert outcome.gate_decision.approved is False
