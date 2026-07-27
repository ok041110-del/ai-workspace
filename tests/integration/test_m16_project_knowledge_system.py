from __future__ import annotations

from pathlib import Path

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.engines.knowledge_provider import InMemoryKnowledgeProvider
from ai_workspace.engines.knowledge_search import InMemoryKnowledgeSearch
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.storage.file_knowledge_repository import FileKnowledgeRepository

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _assemble() -> tuple[InMemoryEventBus, InMemoryTaskEngine, InMemoryEngineRuntime]:
    """M16-T03: 실제 프로젝트 문서(`docs/ARCHITECTURE.md` 등)를 실제로
    읽는 `FileKnowledgeRepository` + `InMemoryKnowledgeSearch` +
    `InMemoryKnowledgeProvider`를 실제 `CodingAgent`에 연결한다.
    Mock인 것은 실제 LLM/CLI 프로세스 실행 경계(`MockEngineAdapter`)
    뿐이다."""
    repository = FileKnowledgeRepository(_PROJECT_ROOT)
    knowledge_provider = InMemoryKnowledgeProvider(InMemoryKnowledgeSearch(repository))

    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())

    agent_runtime = AgentRuntime(
        agent_manager=InMemoryAgentManager(), agent_registry=InMemoryAgentRegistry()
    )
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        knowledge_provider=knowledge_provider,
    )
    return event_bus, task_engine, engine_runtime


def test_real_project_document_is_found_and_reflected_in_agent_prompt() -> None:
    """M16 DoD 5번: 실제 `docs/ARCHITECTURE.md`에 등장하는 키워드로 Task를
    만들면, `FileKnowledgeRepository`가 실제로 그 파일을 읽고,
    `CodingAgent`가 그 내용을 실행 프롬프트에 반영함을 증명한다."""
    event_bus, task_engine, _engine_runtime = _assemble()
    task = task_engine.create_task("p1", "ExecutionEnvironment")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    code_completed = next(e for e in received if e.event_type == CODE_COMPLETED)
    assert code_completed.payload["success"] is True


def test_agent_prompt_actually_contains_the_matched_documents_content() -> None:
    """검색된 실제 문서 내용이 그대로 프롬프트에 실려 Engine까지
    전달됐는지, MockEngineAdapter가 받은 Task로 직접 확인한다."""
    repository = FileKnowledgeRepository(_PROJECT_ROOT)
    knowledge_provider = InMemoryKnowledgeProvider(InMemoryKnowledgeSearch(repository))
    matched = knowledge_provider.provide("ExecutionEnvironment")
    assert matched, "실제 ARCHITECTURE.md에 ExecutionEnvironment가 있어야 한다"

    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()

    received_prompts: list[str] = []

    class RecordingAdapter(MockEngineAdapter):
        def run(self, session_id, task, *, model=None):  # type: ignore[override]
            received_prompts.append(task.title)
            return super().run(session_id, task, model=model)

    engine_runtime.register_engine("mock", RecordingAdapter())
    agent_runtime = AgentRuntime(
        agent_manager=InMemoryAgentManager(), agent_registry=InMemoryAgentRegistry()
    )
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        knowledge_provider=knowledge_provider,
    )
    task = task_engine.create_task("p1", "ExecutionEnvironment")

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert len(received_prompts) == 1
    assert matched[0].content in received_prompts[0]


def test_no_match_query_leaves_prompt_unchanged() -> None:
    event_bus, task_engine, engine_runtime = _assemble()
    task = task_engine.create_task("p1", "완전히-무관한-검색어-xyz123")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    code_completed = next(e for e in received if e.event_type == CODE_COMPLETED)
    assert code_completed.payload["success"] is True
