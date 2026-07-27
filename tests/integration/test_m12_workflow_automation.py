from __future__ import annotations

from typing import Any

from tests.interfaces.fakes import FakeAgentManager, FakeAgentRegistry

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.agents.coding_agent import CodingAgent
from ai_workspace.agents.coordinator_agent import CoordinatorAgent
from ai_workspace.agents.documentation_agent import DocumentationAgent
from ai_workspace.agents.review_agent import ReviewAgent
from ai_workspace.agents.shell_agent import ShellAgent
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.task import TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine
from ai_workspace.runtime.agent.agent_runtime import AgentRuntime
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.runtime.workflow.workflow_runner import WorkflowRunner


class SequencedProcessRunner:
    """호출 순서대로 미리 정해진 결과를 반환하는 테스트 더블 — 목록의
    마지막 결과는 그 이후 모든 호출에 반복 사용된다(재작업으로 여러 번
    호출돼도 마지막 결과가 계속 반환됨). `ShellAgent`가 실제 `pytest`를
    재귀 호출하지 않도록 실제 프로세스 대신 주입한다."""

    def __init__(self, results: list[ProcessResult]) -> None:
        self._results = results
        self.call_count = 0

    def run(self, process_id: str, command: list[str], *, cwd=None, timeout=None) -> ProcessResult:
        index = min(self.call_count, len(self._results) - 1)
        result = self._results[index]
        self.call_count += 1
        return result

    def cancel(self, process_id: str) -> None:
        pass


def _success_shell_result() -> ProcessResult:
    return ProcessResult(returncode=0, stdout="1 passed", stderr="")


def _failure_shell_result() -> ProcessResult:
    return ProcessResult(returncode=1, stdout="1 failed", stderr="")


def build_pipeline(*, shell_results: list[ProcessResult]) -> dict[str, Any]:
    """M12: `WorkflowRunner`가 실제 Coding→Shell→Coordinator→Review→
    Documentation 파이프라인(M5-T06) 위에서 여러 Task를 순차 실행함을
    검증하기 위한 조립. `PlanningAgent`는 쓰지 않는다 — Task는
    `WorkflowRunner`가 직접 `TaskEngine.create_task()`로 만든 것을
    재사용하고, `MissionPlanned`도 `WorkflowRunner`가 발행한다."""
    agent_runtime = AgentRuntime(
        agent_manager=FakeAgentManager(), agent_registry=FakeAgentRegistry()
    )
    event_bus = InMemoryEventBus()
    task_engine = InMemoryTaskEngine()
    engine_runtime = InMemoryEngineRuntime()
    engine_runtime.register_engine("mock", MockEngineAdapter())
    context_manager = InMemoryContextManager(InMemoryMemoryEngine())
    workspace_session = WorkspaceSession(session_id="s1", current_project_id="p1")

    CodingAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    ShellAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        command_kind="test",
        process_runner=SequencedProcessRunner(shell_results),
    )
    CoordinatorAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        max_rework_attempts=1,
    )
    ReviewAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
    )
    DocumentationAgent(
        agent_runtime=agent_runtime,
        event_bus=event_bus,
        task_engine=task_engine,
        engine_runtime=engine_runtime,
        context_manager=context_manager,
        workspace_session=workspace_session,
    )

    return {
        "event_bus": event_bus,
        "task_engine": task_engine,
        "runner": WorkflowRunner(
            workflow_engine=InMemoryWorkflowEngine(), event_bus=event_bus, task_engine=task_engine
        ),
    }


def test_workflow_with_two_tasks_completes_without_human_intervention() -> None:
    """DoD 3번(성공 시나리오): Task 2개 + 의존관계가 있는 Workflow가
    사람이 각 Task마다 개별 호출을 하지 않아도 plan() 순서대로 전부
    완주한다."""
    pipeline = build_pipeline(shell_results=[_success_shell_result()])
    task1 = pipeline["task_engine"].create_task("p1", "첫 번째 Task")
    task2 = pipeline["task_engine"].create_task("p1", "두 번째 Task")
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=[task1.task_id, task2.task_id],
        dependencies={task2.task_id: {task1.task_id}},
    )

    result = pipeline["runner"].run(workflow)

    assert result.success is True
    assert result.completed_task_ids == [task1.task_id, task2.task_id]
    assert pipeline["task_engine"].get_task(task1.task_id).status == TaskStatus.DONE
    assert pipeline["task_engine"].get_task(task2.task_id).status == TaskStatus.DONE


def test_workflow_stops_when_a_task_fails_and_later_tasks_never_run() -> None:
    """DoD 2번/3번(중단 시나리오): 두 번째 Task의 테스트가 계속
    실패해(재작업 소진, `ReworkExhausted`) DONE에 도달하지 못하면 세
    번째 Task는 실행조차 되지 않는다."""
    pipeline = build_pipeline(
        shell_results=[_success_shell_result(), _failure_shell_result()]
    )
    task1 = pipeline["task_engine"].create_task("p1", "첫 번째 Task")
    task2 = pipeline["task_engine"].create_task("p1", "두 번째 Task(계속 실패)")
    task3 = pipeline["task_engine"].create_task("p1", "세 번째 Task(실행되면 안 됨)")
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=[task1.task_id, task2.task_id, task3.task_id],
        dependencies={
            task2.task_id: {task1.task_id},
            task3.task_id: {task2.task_id},
        },
    )

    result = pipeline["runner"].run(workflow)

    assert result.success is False
    assert result.completed_task_ids == [task1.task_id]
    assert result.failed_task_id == task2.task_id
    assert pipeline["task_engine"].get_task(task1.task_id).status == TaskStatus.DONE
    assert pipeline["task_engine"].get_task(task2.task_id).status != TaskStatus.DONE
    # task3는 create_task()로 만들어졌을 뿐 파이프라인이 실행되지 않아
    # TODO 상태 그대로여야 한다.
    assert pipeline["task_engine"].get_task(task3.task_id).status == TaskStatus.TODO
