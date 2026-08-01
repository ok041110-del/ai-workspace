import pytest

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler


def make_agent(
    agent_id: str,
    capabilities: frozenset[AgentCapability] = frozenset(),
    *,
    status: AgentStatus = AgentStatus.IDLE,
    priority: int = 0,
) -> Agent:
    return Agent(
        agent_id=agent_id,
        role=AgentRole.CODING,
        capabilities=capabilities,
        status=status,
        priority=priority,
    )


def test_select_returns_agents_with_matching_capability() -> None:
    scheduler = InMemoryAgentScheduler()
    matching = make_agent("a1", frozenset({AgentCapability.CODING}))
    other = make_agent("a2", frozenset({AgentCapability.REVIEW}))

    selected = scheduler.select([matching, other], AgentCapability.CODING)

    assert selected == [matching]


def test_select_respects_max_count() -> None:
    scheduler = InMemoryAgentScheduler()
    agents = [
        make_agent("a1", frozenset({AgentCapability.CODING})),
        make_agent("a2", frozenset({AgentCapability.CODING})),
        make_agent("a3", frozenset({AgentCapability.CODING})),
    ]

    selected = scheduler.select(agents, AgentCapability.CODING, max_count=2)

    assert selected == agents[:2]


def test_select_returns_empty_list_when_no_match() -> None:
    scheduler = InMemoryAgentScheduler()
    agent = make_agent("a1", frozenset({AgentCapability.REVIEW}))

    selected = scheduler.select([agent], AgentCapability.CODING)

    assert selected == []


def test_select_prefers_lower_priority_number() -> None:
    """M57(ADR-0075) — priority는 낮을수록 우선."""
    scheduler = InMemoryAgentScheduler()
    low_priority = make_agent("a1", frozenset({AgentCapability.CODING}), priority=5)
    high_priority = make_agent("a2", frozenset({AgentCapability.CODING}), priority=1)

    selected = scheduler.select([low_priority, high_priority], AgentCapability.CODING)

    assert selected == [high_priority]


def test_select_is_stable_sort_when_priorities_tie() -> None:
    """M57(ADR-0075) — 동점(기본값 0)이면 candidates 원래 순서를
    그대로 보존해 M13/M56의 "첫 매치" 동작과 100% 동일해야 한다."""
    scheduler = InMemoryAgentScheduler()
    first = make_agent("a1", frozenset({AgentCapability.CODING}))
    second = make_agent("a2", frozenset({AgentCapability.CODING}))

    selected = scheduler.select([first, second], AgentCapability.CODING)

    assert selected == [first]


@pytest.mark.parametrize("status", [AgentStatus.STOPPED, AgentStatus.ERROR])
def test_select_excludes_stopped_and_error_agents(status: AgentStatus) -> None:
    """M57(ADR-0075) — STOPPED/ERROR만 불가용으로 제외."""
    scheduler = InMemoryAgentScheduler()
    unavailable = make_agent("a1", frozenset({AgentCapability.CODING}), status=status)

    selected = scheduler.select([unavailable], AgentCapability.CODING)

    assert selected == []


@pytest.mark.parametrize(
    "status", [AgentStatus.IDLE, AgentStatus.RUNNING, AgentStatus.WAITING, AgentStatus.PAUSED]
)
def test_select_includes_all_non_terminal_statuses(status: AgentStatus) -> None:
    """M57(ADR-0075) — IDLE(도메인 기본값 단위 테스트 경로)과
    RUNNING(AgentRuntime.start_agent() 실제 실행 경로) 둘 다 가용
    해야 회귀가 없다. WAITING/PAUSED도 명확히 종료/오류 상태가
    아니므로 가용으로 취급한다."""
    scheduler = InMemoryAgentScheduler()
    agent = make_agent("a1", frozenset({AgentCapability.CODING}), status=status)

    selected = scheduler.select([agent], AgentCapability.CODING)

    assert selected == [agent]
