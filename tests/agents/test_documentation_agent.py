from __future__ import annotations

from tests.agents.test_coding_agent import RecordingEngineRuntime
from tests.interfaces.fakes import (
    FakeAgentManager,
    FakeAgentRegistry,
    FakeAgentScheduler,
    FakeTaskEngine,
)

from ai_workspace.agents.documentation_agent import DocumentationAgent
from ai_workspace.agents.events import DOCUMENTATION_COMPLETED, REVIEW_COMPLETED
from ai_workspace.domain.agent import AgentRole
from ai_workspace.domain.llm_policy import LLMEffort, LLMModel, LLMPolicyDecision, LLMProvider
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.llm_policy_engine import InMemoryLLMPolicyEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.context_manager import ContextManager
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime


class SpyContextManager(ContextManager):
    """실제 `InMemoryContextManager`에 위임하면서 `create_snapshot()`에
    전달된 `summary` 값을 기록하는 테스트 더블(M7-T02) — `DocumentationAgent`
    가 실제로 어떤 summary를 넘겼는지 증명하기 위함."""

    def __init__(self) -> None:
        self._inner = InMemoryContextManager(InMemoryMemoryEngine())
        self.received_summaries: list[str | None] = []

    def assemble_context(self, session: WorkspaceSession) -> dict[str, str]:
        return self._inner.assemble_context(session)

    def create_snapshot(self, session: WorkspaceSession, summary: str | None = None) -> str:
        self.received_summaries.append(summary)
        return self._inner.create_snapshot(session, summary)

    def restore_snapshot(self, snapshot_id: str) -> dict[str, str]:
        return self._inner.restore_snapshot(snapshot_id)

    def find_snapshots(self, query: str) -> list[str]:
        return self._inner.find_snapshots(query)

    def latest_snapshot_id(self, project_id: str) -> str | None:
        return self._inner.latest_snapshot_id(project_id)


def build_documentation_agent(
    engine_runtime: RecordingEngineRuntime,
    *,
    llm_policy_engine: LLMPolicyEngine | None = None,
) -> tuple[
    DocumentationAgent, InMemoryEventBus, FakeTaskEngine, SpyContextManager, WorkspaceSession
]:
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(),
        agent_registry=FakeAgentRegistry(),
        llm_policy_engine=llm_policy_engine,
    )
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    context_manager = SpyContextManager()
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")
    agent = DocumentationAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        context_manager=context_manager,
        workspace_session=workspace_session,
    )
    return agent, event_bus, task_engine, context_manager, workspace_session


def _advance_to_review(task_engine: FakeTaskEngine, task: Task) -> None:
    """DocumentationAgent는 REVIEW_COMPLETED를 받으면 Task를 곧바로 DONE으로
    전이시킨다(domain/task.py의 허용된 전이 규칙상 REVIEW에서만 가능) —
    실제 파이프라인에서는 Coding/Review Agent를 거치며 자연히 REVIEW
    상태가 되므로, 단위 테스트에서도 동일한 선행 상태를 맞춰 준다."""
    task_engine.transition(task, TaskStatus.IN_PROGRESS)
    task_engine.transition(task, TaskStatus.REVIEW)


def test_documentation_agent_passes_no_required_capabilities_when_no_policy_engine() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    _agent, event_bus, task_engine, _context_manager, _workspace_session = (
        build_documentation_agent(engine_runtime)
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_required_capabilities == [frozenset()]


def test_documentation_agent_passes_required_capabilities_from_llm_policy_decision() -> None:
    """M6-T02: DOCUMENTATION Role에 GOOGLE 정책이 있으면 실제로
    required_capabilities={"gemini"}가 전달된다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    policy_engine = InMemoryLLMPolicyEngine(
        {
            AgentRole.DOCUMENTATION: LLMPolicyDecision(
                LLMModel(LLMProvider.GOOGLE, "gemini"), LLMEffort.LOW
            )
        }
    )
    _agent, event_bus, task_engine, _context_manager, _workspace_session = (
        build_documentation_agent(engine_runtime, llm_policy_engine=policy_engine)
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_required_capabilities == [frozenset({"gemini"})]


def test_documentation_agent_passes_model_from_llm_policy_decision() -> None:
    """M14-T03: DOCUMENTATION Role에 gemini 모델 정책이 있으면 실제로
    model="gemini"가 전달된다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    policy_engine = InMemoryLLMPolicyEngine(
        {
            AgentRole.DOCUMENTATION: LLMPolicyDecision(
                LLMModel(LLMProvider.GOOGLE, "gemini"), LLMEffort.LOW
            )
        }
    )
    _agent, event_bus, task_engine, _context_manager, _workspace_session = (
        build_documentation_agent(engine_runtime, llm_policy_engine=policy_engine)
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert engine_runtime.received_models == ["gemini"]


def test_documentation_agent_publishes_documentation_completed() -> None:
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    _agent, event_bus, task_engine, _context_manager, _workspace_session = (
        build_documentation_agent(engine_runtime)
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert any(e.event_type == DOCUMENTATION_COMPLETED for e in received)


def test_documentation_agent_passes_engine_result_output_as_summary() -> None:
    """M7-T02: 이전에는 engine_runtime.run()의 결과가 그대로 버려졌지만,
    이제 그 output이 실제로 create_snapshot()의 summary로 전달된다."""
    engine_runtime = RecordingEngineRuntime(
        EngineResult(success=True, output="로그인 기능 구현 및 검토 완료")
    )
    _agent, event_bus, task_engine, context_manager, _workspace_session = build_documentation_agent(
        engine_runtime
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert context_manager.received_summaries == ["로그인 기능 구현 및 검토 완료"]


def test_documentation_agent_summary_is_retrievable_via_context_manager() -> None:
    """summary가 실제로 Memory Snapshot에 저장되어 find_snapshots()로도
    검색됨을 증명한다(PRD 7.4 검색/요약)."""
    engine_runtime = RecordingEngineRuntime(
        EngineResult(success=True, output="로그인 기능 구현 및 검토 완료")
    )
    _agent, event_bus, task_engine, context_manager, _workspace_session = build_documentation_agent(
        engine_runtime
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert context_manager.find_snapshots("로그인 기능 구현 및 검토 완료") != []


def test_documentation_agent_writes_new_snapshot_id_back_to_session() -> None:
    """M8-T02: create_snapshot()의 반환값이 이전에는 버려졌지만, 이제
    workspace_session.memory_snapshot_id에 되먹여진다 — 같은 세션에서
    이어지는 Mission이 이 Snapshot을 자동으로 이어받을 수 있게 된다."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    _agent, event_bus, task_engine, context_manager, workspace_session = build_documentation_agent(
        engine_runtime
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert workspace_session.memory_snapshot_id is not None
    assert context_manager.restore_snapshot(workspace_session.memory_snapshot_id)["summary"] == (
        "문서화 완료"
    )


def test_documentation_agent_second_mission_overwrites_session_snapshot_id() -> None:
    """연속된 두 번째 Mission이 끝나면 세션은 그 두 번째 Snapshot을
    가리킨다(누적이 아니라 최신 하나만 유지 — 사전 Architecture Review에서
    이미 확정된 단순화)."""
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="완료"))
    _agent, event_bus, task_engine, _context_manager, workspace_session = (
        build_documentation_agent(engine_runtime)
    )
    first_task = task_engine.create_task("p1", "첫 번째 작업")
    _advance_to_review(task_engine, first_task)
    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": first_task.task_id})
    )
    first_snapshot_id = workspace_session.memory_snapshot_id

    second_task = task_engine.create_task("p1", "두 번째 작업")
    _advance_to_review(task_engine, second_task)
    event_bus.publish(
        Event(event_id="e2", event_type=REVIEW_COMPLETED, payload={"task_id": second_task.task_id})
    )

    assert workspace_session.memory_snapshot_id != first_snapshot_id


def test_documentation_agent_ignores_review_completed_when_not_selected_by_scheduler() -> None:
    """M56(ADR-0074) — CodingAgent(M13)와 동일한 패턴: 같은 DOCUMENTATION
    Capability를 가진 다른 DocumentationAgent 인스턴스가 Scheduler에게
    선택되면, 선택되지 않은 인스턴스는 아무것도 하지 않는다."""
    shared_registry = FakeAgentRegistry()
    shared_manager = FakeAgentManager()
    shared_scheduler = FakeAgentScheduler()
    event_bus = InMemoryEventBus()
    task_engine = FakeTaskEngine()
    engine_runtime = RecordingEngineRuntime(EngineResult(success=True, output="문서화 완료"))
    context_manager = SpyContextManager()
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")

    selected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    DocumentationAgent(
        agent_runtime=selected_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        context_manager=context_manager,
        workspace_session=workspace_session,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )
    unselected_agent_runtime = AgentRuntime(
        agent_manager=shared_manager, agent_registry=shared_registry
    )
    DocumentationAgent(
        agent_runtime=unselected_agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        context_manager=context_manager,
        workspace_session=workspace_session,
        agent_registry=shared_registry,
        agent_scheduler=shared_scheduler,
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    _advance_to_review(task_engine, task)

    event_bus.publish(
        Event(event_id="e1", event_type=REVIEW_COMPLETED, payload={"task_id": task.task_id})
    )

    assert len(engine_runtime.received_tasks) == 1
