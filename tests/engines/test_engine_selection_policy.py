from ai_workspace.domain.budget import Budget
from ai_workspace.domain.engine_selection import EngineCandidate
from ai_workspace.domain.knowledge import KnowledgeDocument, KnowledgeKind
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy


def make_task() -> Task:
    return Task(task_id="t1", project_id="p1", title="구현하기", status=TaskStatus.TODO)


def _candidate(name: str, tokens: int, cost: float) -> EngineCandidate:
    return EngineCandidate(
        engine_name=name,
        capabilities=frozenset({"code_generation"}),
        estimated_tokens=tokens,
        estimated_cost_usd=cost,
        supports_parallel=True,
    )


def test_select_returns_none_when_no_candidates() -> None:
    policy = InMemoryEngineSelectionPolicy()

    assert policy.select(make_task(), []) is None


def test_select_picks_lowest_cost_candidate_without_budget() -> None:
    policy = InMemoryEngineSelectionPolicy()
    candidates = [_candidate("expensive", 100, 1.0), _candidate("cheap", 50, 0.1)]

    decision = policy.select(make_task(), candidates)

    assert decision is not None
    assert decision.engine_name == "cheap"
    assert decision.model is None
    assert "cheap" not in decision.reason  # reason은 근거를 담을 뿐 이름을 반복하지 않음


def test_select_excludes_candidates_over_budget() -> None:
    policy = InMemoryEngineSelectionPolicy()
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=0.5))
    candidates = [_candidate("expensive", 100, 1.0), _candidate("cheap", 50, 0.1)]

    decision = policy.select(make_task(), candidates, budget_policy_engine=budget_policy_engine)

    assert decision is not None
    assert decision.engine_name == "cheap"


def test_select_returns_none_when_all_candidates_exceed_budget() -> None:
    policy = InMemoryEngineSelectionPolicy()
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=0.01))
    candidates = [_candidate("expensive", 100, 1.0), _candidate("still-expensive", 50, 0.5)]

    decision = policy.select(make_task(), candidates, budget_policy_engine=budget_policy_engine)

    assert decision is None


def test_select_includes_knowledge_reference_in_reason() -> None:
    policy = InMemoryEngineSelectionPolicy()
    candidates = [_candidate("only", 10, 0.01)]
    knowledge = [
        KnowledgeDocument(
            document_id="architecture",
            kind=KnowledgeKind.ARCHITECTURE,
            title="ARCHITECTURE",
            content="내용",
            source_path="docs/ARCHITECTURE.md",
        )
    ]

    decision = policy.select(make_task(), candidates, knowledge=knowledge)

    assert decision is not None
    assert "Knowledge" in decision.reason


def test_select_ties_prefer_first_registered_order() -> None:
    policy = InMemoryEngineSelectionPolicy()
    candidates = [_candidate("first", 10, 0.1), _candidate("second", 10, 0.1)]

    decision = policy.select(make_task(), candidates)

    assert decision is not None
    assert decision.engine_name == "first"
