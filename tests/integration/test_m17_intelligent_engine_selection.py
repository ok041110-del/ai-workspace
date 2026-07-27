from __future__ import annotations

from pathlib import Path

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.budget import Budget
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.engines.knowledge_provider import InMemoryKnowledgeProvider
from ai_workspace.engines.knowledge_search import InMemoryKnowledgeSearch
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.engine_adapter import CostEstimate, EngineResult
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.storage.file_knowledge_repository import FileKnowledgeRepository

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


class _FixedCostAdapter(MockEngineAdapter):
    def __init__(self, tokens: int, cost_usd: float) -> None:
        super().__init__()
        self._estimate = CostEstimate(estimated_tokens=tokens, estimated_cost_usd=cost_usd)

    def estimate_cost(self, task: Task) -> CostEstimate:
        return self._estimate


def test_selection_picks_cheapest_candidate_within_budget() -> None:
    """M17 DoD 4번: 여러 Engine이 실제로 등록된 상태에서, Budget 내
    최저 비용 후보가 선택된다."""
    registry = InMemoryEngineRegistry()
    registry.register("expensive", _FixedCostAdapter(tokens=1000, cost_usd=1.0))
    registry.register("cheap", _FixedCostAdapter(tokens=10, cost_usd=0.01))
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=5.0))
    policy = InMemoryEngineSelectionPolicy()

    candidates = registry.list_candidates(make_task())
    decision = policy.select(make_task(), candidates, budget_policy_engine=budget_policy_engine)

    assert decision is not None
    assert decision.engine_name == "cheap"


def test_selection_excludes_the_over_budget_engine() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("expensive", _FixedCostAdapter(tokens=1000, cost_usd=1.0))
    registry.register("mid", _FixedCostAdapter(tokens=100, cost_usd=0.3))
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=0.5))
    policy = InMemoryEngineSelectionPolicy()

    candidates = registry.list_candidates(make_task())
    decision = policy.select(make_task(), candidates, budget_policy_engine=budget_policy_engine)

    assert decision is not None
    assert decision.engine_name == "mid"


def test_selection_returns_none_when_every_candidate_exceeds_budget() -> None:
    registry = InMemoryEngineRegistry()
    registry.register("expensive", _FixedCostAdapter(tokens=1000, cost_usd=1.0))
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=0.01))
    policy = InMemoryEngineSelectionPolicy()

    candidates = registry.list_candidates(make_task())
    decision = policy.select(make_task(), candidates, budget_policy_engine=budget_policy_engine)

    assert decision is None


def test_selection_uses_real_project_knowledge_in_reason() -> None:
    """실제 FileKnowledgeRepository로 조회한 Project Knowledge가
    결정 사유에 반영됨을 실제 구성 요소로 증명한다."""
    repository = FileKnowledgeRepository(_PROJECT_ROOT)
    knowledge_provider = InMemoryKnowledgeProvider(InMemoryKnowledgeSearch(repository))
    matched = knowledge_provider.provide("ExecutionEnvironment")
    assert matched

    registry = InMemoryEngineRegistry()
    registry.register("only", _FixedCostAdapter(tokens=10, cost_usd=0.01))
    policy = InMemoryEngineSelectionPolicy()

    task = Task(task_id="t1", project_id="p1", title="ExecutionEnvironment", status=TaskStatus.TODO)
    candidates = registry.list_candidates(task)
    decision = policy.select(task, candidates, knowledge=matched)

    assert decision is not None
    assert "Knowledge" in decision.reason


def test_selection_decision_is_not_wired_into_actual_execution() -> None:
    """M17 DoD 5번(가장 중요한 경계): EngineSelectionPolicy가 다른
    Engine을 추천하더라도, 실제 CodingAgent 실행 경로(EngineRuntime)는
    전혀 영향을 받지 않는다 — 결정과 실행은 이번 Milestone에서
    완전히 분리되어 있다(M18에서 연결 예정)."""
    # EngineRegistry: "cheap"이 더 저렴해 EngineSelectionPolicy가 이걸 추천한다.
    registry = InMemoryEngineRegistry()
    registry.register("expensive", _FixedCostAdapter(tokens=1000, cost_usd=1.0))
    registry.register("cheap", _FixedCostAdapter(tokens=10, cost_usd=0.01))
    policy = InMemoryEngineSelectionPolicy()
    decision = policy.select(make_task(), registry.list_candidates(make_task()))
    assert decision is not None
    assert decision.engine_name == "cheap"

    # 그러나 실제 실행 경로(EngineRuntime)에는 "expensive"만 등록되어 있다.
    # CodingAgent는 EngineSelectionPolicy/EngineRegistry를 전혀 모른다
    # (생성자에 그런 파라미터가 없다) - 실행은 여전히 EngineRuntime의
    # 기존 규칙(첫 매칭)을 그대로 따른다.
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    expensive_adapter = _FixedCostAdapter(tokens=1000, cost_usd=1.0)
    engine_runtime.register_engine("expensive", expensive_adapter)

    agent_runtime = AgentRuntime(
        agent_manager=InMemoryAgentManager(), agent_registry=InMemoryAgentRegistry()
    )
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    task = task_engine.create_task("p1", "구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    # 실행은 EngineRuntime에 등록된(오직) "expensive"로 그대로 이루어졌다 -
    # EngineSelectionPolicy의 "cheap" 추천은 실행에 아무 영향을 주지 않았다.
    assert engine_runtime.status(task.task_id).name == "COMPLETED"


def test_coding_agent_has_no_dependency_on_engine_selection_policy() -> None:
    """CodingAgent 생성자가 EngineSelectionPolicy/EngineRegistry를
    받지 않음을 직접 확인한다 - M17이 실행 경로를 건드리지 않았다는
    설계상 약속이 실제 코드에서도 지켜지고 있음을 증명."""
    import inspect

    parameters = inspect.signature(CodingAgent.__init__).parameters
    assert "engine_selection_policy" not in parameters
    assert "engine_registry" not in parameters


def test_result_success_flag_unaffected_by_selection_policy_existing() -> None:
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())
    result: EngineResult = engine_runtime.run(make_task())

    assert result.success is True
