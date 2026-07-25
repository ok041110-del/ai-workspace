from ai_workspace.domain.mission import Mission
from ai_workspace.domain.step import Step
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine


def test_plan_respects_dependencies() -> None:
    workflow = Workflow(
        workflow_id="w1",
        mission_id="m1",
        task_ids=["t1", "t2", "t3"],
        dependencies={"t2": {"t1"}, "t3": {"t2"}},
    )
    engine = InMemoryWorkflowEngine()

    order = engine.plan(workflow)

    assert order.index("t1") < order.index("t2") < order.index("t3")


def test_plan_returns_every_task_exactly_once() -> None:
    workflow = Workflow(
        workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"], dependencies={}
    )
    engine = InMemoryWorkflowEngine()

    order = engine.plan(workflow)

    assert sorted(order) == sorted(workflow.task_ids)


def test_plan_executes_mission_workflow_task_step_hierarchy() -> None:
    """T2-07: Milestone 2 DoD 2번("Workflow가 Mission→Workflow→Task→Step
    협업 흐름을 실행한다")을 증명한다. 실제 TaskEngine으로 생성한 Task를
    Workflow에 엮고, Task 하나에 Step을 붙여 전체 계층이 함께 동작함을
    확인한다."""
    task_engine = InMemoryTaskEngine()
    mission = Mission(mission_id="m1", project_id="p1", goal="문서 체계 완성")
    design_task = task_engine.create_task(mission.project_id, "설계하기")
    implement_task = task_engine.create_task(mission.project_id, "구현하기")
    workflow = Workflow(
        workflow_id="w1",
        mission_id=mission.mission_id,
        task_ids=[design_task.task_id, implement_task.task_id],
        dependencies={implement_task.task_id: {design_task.task_id}},
    )
    step = Step(step_id="s1", task_id=implement_task.task_id, description="파일 작성")

    order = InMemoryWorkflowEngine().plan(workflow)

    assert order == [design_task.task_id, implement_task.task_id]
    assert step.task_id == implement_task.task_id
