from __future__ import annotations

from tests.interfaces.fakes import FakeEventBus, FakeTaskEngine, FakeWorkflowEngine

from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.task import TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.runtime.workflow.workflow_runner import WorkflowRunner


def _complete_task_on_mission_planned(task_engine: FakeTaskEngine) -> object:
    """MissionPlanned를 받으면 해당 Task를 TODO→IN_PROGRESS→REVIEW→DONE
    까지 전이시키는 테스트용 구독자 — 실제 CodingAgent~DocumentationAgent
    6-Agent 파이프라인이 성공적으로 끝났을 때의 최종 상태를 흉내낸다."""

    def handler(event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        task = task_engine.get_task(event.payload["task_id"])
        task_engine.transition(task, TaskStatus.IN_PROGRESS)
        task_engine.transition(task, TaskStatus.REVIEW)
        task_engine.transition(task, TaskStatus.DONE)

    return handler


def _block_task_on_mission_planned(task_engine: FakeTaskEngine) -> object:
    """MissionPlanned를 받아도 Task를 IN_PROGRESS에서 멈춰 두는 테스트용
    구독자 — 재작업이 소진되어(ReworkExhausted) DONE에 도달하지 못하고
    파이프라인이 중간에 멈춘 상황을 흉내낸다."""

    def handler(event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        task = task_engine.get_task(event.payload["task_id"])
        task_engine.transition(task, TaskStatus.IN_PROGRESS)

    return handler


def test_run_executes_all_tasks_in_dependency_order_and_succeeds() -> None:
    task_engine = FakeTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task")
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=[task1.task_id, task2.task_id],
        dependencies={task2.task_id: {task1.task_id}},
    )
    event_bus = FakeEventBus()
    published_task_ids: list[str] = []
    event_bus.subscribe(
        lambda event: published_task_ids.append(event.payload["task_id"])
        if event.event_type == MISSION_PLANNED
        else None
    )
    event_bus.subscribe(_complete_task_on_mission_planned(task_engine))
    runner = WorkflowRunner(
        workflow_engine=FakeWorkflowEngine(), event_bus=event_bus, task_engine=task_engine
    )

    result = runner.run(workflow)

    assert result.success is True
    assert result.completed_task_ids == [task1.task_id, task2.task_id]
    assert result.failed_task_id is None
    assert published_task_ids == [task1.task_id, task2.task_id]


def test_run_stops_after_first_task_that_does_not_reach_done() -> None:
    task_engine = FakeTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task(재작업 소진으로 멈춤)")
    task3 = task_engine.create_task("p1", "세 번째 Task(실행되면 안 됨)")
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=[task1.task_id, task2.task_id, task3.task_id],
        dependencies={
            task2.task_id: {task1.task_id},
            task3.task_id: {task2.task_id},
        },
    )
    event_bus = FakeEventBus()
    published_task_ids: list[str] = []
    event_bus.subscribe(
        lambda event: published_task_ids.append(event.payload["task_id"])
        if event.event_type == MISSION_PLANNED
        else None
    )

    def handler(event: Event) -> None:
        if event.event_type != MISSION_PLANNED:
            return
        task_id = event.payload["task_id"]
        if task_id == task2.task_id:
            _block_task_on_mission_planned(task_engine)(event)
        else:
            _complete_task_on_mission_planned(task_engine)(event)

    event_bus.subscribe(handler)
    runner = WorkflowRunner(
        workflow_engine=FakeWorkflowEngine(), event_bus=event_bus, task_engine=task_engine
    )

    result = runner.run(workflow)

    assert result.success is False
    assert result.completed_task_ids == [task1.task_id]
    assert result.failed_task_id == task2.task_id
    # task3는 task2가 실패한 뒤 실행되면 안 된다.
    assert published_task_ids == [task1.task_id, task2.task_id]


def test_run_single_task_workflow_succeeds() -> None:
    task_engine = FakeTaskEngine()
    task = task_engine.create_task("p1", "단일 Task")
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=[task.task_id])
    event_bus = FakeEventBus()
    event_bus.subscribe(_complete_task_on_mission_planned(task_engine))
    runner = WorkflowRunner(
        workflow_engine=FakeWorkflowEngine(), event_bus=event_bus, task_engine=task_engine
    )

    result = runner.run(workflow)

    assert result.success is True
    assert result.completed_task_ids == [task.task_id]


def test_run_records_outcome_for_workflow_learning() -> None:
    """M71(ADR-0089): run()이 끝나면 실제로 쓰인 순서와 성공 여부가
    자동으로 WorkflowEngine에 기록된다."""
    task_engine = FakeTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task")
    workflow = Workflow(
        workflow_id="w1", mission_id="m1", task_ids=[task1.task_id, task2.task_id]
    )
    event_bus = FakeEventBus()
    event_bus.subscribe(_complete_task_on_mission_planned(task_engine))
    engine = InMemoryWorkflowEngine()
    runner = WorkflowRunner(workflow_engine=engine, event_bus=event_bus, task_engine=task_engine)

    for _ in range(3):
        runner.run(workflow)

    assert engine.recommended_order(workflow) == [task1.task_id, task2.task_id]


def test_run_follows_workflow_engine_recommended_order() -> None:
    """M71(ADR-0089): WorkflowEngine이 학습된 순서를 추천하면
    WorkflowRunner는 그 순서 그대로 Task를 실행한다."""
    task_engine = FakeTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task")
    workflow = Workflow(
        workflow_id="w1", mission_id="m1", task_ids=[task1.task_id, task2.task_id]
    )
    engine = InMemoryWorkflowEngine()
    reversed_order = [task2.task_id, task1.task_id]
    for _ in range(3):
        engine.record_run_outcome(workflow, reversed_order, True)
    event_bus = FakeEventBus()
    event_bus.subscribe(_complete_task_on_mission_planned(task_engine))
    runner = WorkflowRunner(workflow_engine=engine, event_bus=event_bus, task_engine=task_engine)

    result = runner.run(workflow)

    assert result.completed_task_ids == reversed_order
