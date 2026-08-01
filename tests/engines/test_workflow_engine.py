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


def _workflow(task_ids: list[str], dependencies: dict[str, set[str]] | None = None) -> Workflow:
    return Workflow(
        workflow_id="w1", mission_id="m1", task_ids=task_ids, dependencies=dependencies or {}
    )


def test_recommended_order_none_when_no_history() -> None:
    engine = InMemoryWorkflowEngine()

    assert engine.recommended_order(_workflow(["t1", "t2"])) is None


def test_recommended_order_none_when_sample_size_insufficient() -> None:
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])

    for _ in range(2):
        engine.record_run_outcome(workflow, ["t1", "t2"], True)

    assert engine.recommended_order(workflow) is None


def test_recommended_order_returns_highest_success_rate_order() -> None:
    """M71(ADR-0089): 표본이 3건 이상이 되면, 성공률이 더 높았던 순서를
    추천한다."""
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])

    for _ in range(3):
        engine.record_run_outcome(workflow, ["t2", "t1"], False)
    for _ in range(3):
        engine.record_run_outcome(workflow, ["t1", "t2"], True)

    assert engine.recommended_order(workflow) == ["t1", "t2"]


def test_plan_returns_recommended_order_once_learned() -> None:
    """M71(ADR-0089): 학습된 순서가 있으면 `plan()`이 기존 위상정렬 대신
    그 순서를 그대로 반환한다."""
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])

    for _ in range(3):
        engine.record_run_outcome(workflow, ["t2", "t1"], True)

    assert engine.plan(workflow) == ["t2", "t1"]


def test_plan_falls_back_to_dependency_order_without_history() -> None:
    """M71 이전과 100% 동일 동작(회귀 확인): 학습 이력이 없으면 기존
    위상정렬 그대로 동작한다."""
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2", "t3"], {"t2": {"t1"}, "t3": {"t2"}})

    order = engine.plan(workflow)

    assert order.index("t1") < order.index("t2") < order.index("t3")


def test_learning_is_scoped_to_exact_task_ids_and_dependencies() -> None:
    """M71(ADR-0089): task_ids 조합이 다르면(=다른 Workflow로 간주) 학습이
    섞이지 않는다."""
    engine = InMemoryWorkflowEngine()
    workflow_a = _workflow(["t1", "t2"])
    workflow_b = _workflow(["t1", "t2", "t3"])

    for _ in range(3):
        engine.record_run_outcome(workflow_a, ["t2", "t1"], True)

    assert engine.recommended_order(workflow_b) is None


def test_plan_falls_back_when_recommended_order_violates_current_dependencies() -> None:
    """M72(ADR-0090): task_ids는 같지만 이후 dependency가 추가되어 과거
    추천 순서가 더 이상 유효하지 않으면(t1이 t2보다 먼저여야 하는데 추천은
    반대), plan()은 그 추천을 버리고 기존 위상 정렬로 fallback한다."""
    engine = InMemoryWorkflowEngine()
    workflow_without_dependency = _workflow(["t1", "t2"])
    for _ in range(3):
        engine.record_run_outcome(workflow_without_dependency, ["t2", "t1"], True)
    workflow_with_new_dependency = _workflow(["t1", "t2"], {"t2": {"t1"}})

    order = engine.plan(workflow_with_new_dependency)

    assert order == ["t1", "t2"]


def test_recommended_order_survives_dependency_change_when_still_valid() -> None:
    """M72(ADR-0090): dependency가 바뀌어도 학습된 순서가 여전히 그
    dependency를 만족하면(적응형 계획), plan()은 그 순서를 그대로 채택한다."""
    engine = InMemoryWorkflowEngine()
    workflow_without_dependency = _workflow(["t1", "t2", "t3"])
    for _ in range(3):
        engine.record_run_outcome(workflow_without_dependency, ["t1", "t3", "t2"], True)
    workflow_with_compatible_dependency = _workflow(["t1", "t2", "t3"], {"t2": {"t1"}})

    order = engine.plan(workflow_with_compatible_dependency)

    assert order == ["t1", "t3", "t2"]
