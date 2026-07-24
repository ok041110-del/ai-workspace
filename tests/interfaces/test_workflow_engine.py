from ai_workspace.domain.workflow import Workflow

from .fakes import FakeWorkflowEngine


def test_plan_respects_dependencies() -> None:
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=["t1", "t2", "t3"],
        dependencies={"t2": {"t1"}, "t3": {"t2"}},
    )
    engine = FakeWorkflowEngine()

    order = engine.plan(workflow)

    assert order.index("t1") < order.index("t2") < order.index("t3")


def test_plan_returns_every_task_exactly_once() -> None:
    workflow = Workflow(
        workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"], dependencies={}
    )
    engine = FakeWorkflowEngine()

    order = engine.plan(workflow)

    assert sorted(order) == sorted(workflow.task_ids)
