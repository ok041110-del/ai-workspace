from __future__ import annotations

import json

from tests.interfaces.fakes import FakeExecutionEnvironment

from ai_workspace.adapters.claude_code_engine_adapter import ClaudeCodeEngineAdapter
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.events import CODE_COMPLETED, MISSION_PLANNED
from ai_workspace.domain.budget import Budget
from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.execution_environment import ExecutionResult
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.managed_engine_runtime import ManagedEngineRuntime


def _assemble(*, budget: Budget | None):
    """M15 DoD 4번을 검증하기 위한 최소 파이프라인: 실제
    `ManagedEngineRuntime` + 실제 `ClaudeCodeEngineAdapter`(M15가 새로
    만든 로직이 없는 M3/M14의 기존 구현 그대로) + 실제 `CodingAgent`에
    `InMemoryBudgetPolicyEngine`을 주입한다. 프로세스 경계만
    `FakeExecutionEnvironment`로 대체한다(M11-T03과 동일한 경계)."""
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(
        returncode=0,
        stdout=json.dumps({"is_error": False, "result": "claude 실행 결과"}),
        stderr="",
    )

    engine_runtime = ManagedEngineRuntime(event_bus=event_bus)
    engine_runtime.register_engine(
        "claude_code", ClaudeCodeEngineAdapter(execution_environment=execution_environment)
    )

    agent_runtime = AgentRuntime(
        agent_manager=InMemoryAgentManager(), agent_registry=InMemoryAgentRegistry()
    )
    budget_policy_engine = InMemoryBudgetPolicyEngine(budget)
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        budget_policy_engine=budget_policy_engine,
    )

    return event_bus, task_engine, execution_environment


def test_within_budget_task_runs_and_completes() -> None:
    """M15 DoD 4번(허용 경로): 예상 토큰이 Budget 안이면 기존과 동일하게
    ClaudeCodeEngineAdapter가 실제로 실행되고 CodeCompleted가 발행된다."""
    event_bus, task_engine, execution_environment = _assemble(
        budget=Budget(max_tokens=10_000)
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert any(e.event_type == CODE_COMPLETED for e in received)
    assert task_engine.get_task(task.task_id).status == TaskStatus.REVIEW
    assert len(execution_environment.executed_commands) == 1


def test_over_budget_task_is_blocked_and_never_executed() -> None:
    """M15 DoD 4번(차단 경로): 예상 토큰이 Budget을 초과하면
    ClaudeCodeEngineAdapter가 아예 호출되지 않고, Task는 BLOCKED로
    전환되며, Approval/Retry 없이 CodeCompleted도 발행되지 않는다."""
    event_bus, task_engine, execution_environment = _assemble(budget=Budget(max_tokens=1))
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert not any(e.event_type == CODE_COMPLETED for e in received)
    assert task_engine.get_task(task.task_id).status == TaskStatus.BLOCKED
    assert execution_environment.executed_commands == []


def test_no_budget_policy_engine_behaves_exactly_like_before_m15() -> None:
    """M15 DoD 5번: budget_policy_engine을 아예 주입하지 않으면(기존
    모든 조립 코드) estimate_cost() 호출조차 없이 기존과 완전히
    동일하게 동작한다."""
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    execution_environment = FakeExecutionEnvironment()
    execution_environment.result = ExecutionResult(
        returncode=0,
        stdout=json.dumps({"is_error": False, "result": "claude 실행 결과"}),
        stderr="",
    )
    engine_runtime = ManagedEngineRuntime(event_bus=event_bus)
    engine_runtime.register_engine(
        "claude_code", ClaudeCodeEngineAdapter(execution_environment=execution_environment)
    )
    agent_runtime = AgentRuntime(
        agent_manager=InMemoryAgentManager(), agent_registry=InMemoryAgentRegistry()
    )
    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    task = task_engine.create_task("p1", "로그인 기능 구현하기")
    received: list[Event] = []
    event_bus.subscribe(received.append)

    event_bus.publish(
        Event(event_id="e1", event_type=MISSION_PLANNED, payload={"task_id": task.task_id})
    )

    assert any(e.event_type == CODE_COMPLETED for e in received)
    assert task_engine.get_task(task.task_id).status == TaskStatus.REVIEW
