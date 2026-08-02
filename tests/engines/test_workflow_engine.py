from __future__ import annotations

from tests.interfaces.fakes import FakeEngineAdapter

from ai_workspace.domain.engine_selection import EngineCandidate, EngineSelectionDecision
from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.domain.mission import Mission
from ai_workspace.domain.step import Step
from ai_workspace.domain.task import Task
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry


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


class _SpyEngineSelectionPolicy(InMemoryEngineSelectionPolicy):
    """M73(ADR-0091) 테스트용 — `select()`가 실제로 호출됐는지(=비용
    계산 경로가 실행됐는지) 확인하기 위해 호출 횟수만 센다."""

    def __init__(self) -> None:
        self.call_count = 0

    def select(
        self,
        task: Task,
        candidates: list[EngineCandidate],
        *,
        budget_policy_engine: BudgetPolicyEngine | None = None,
        knowledge: list[KnowledgeDocument] | None = None,
    ) -> EngineSelectionDecision | None:
        self.call_count += 1
        return super().select(
            task, candidates, budget_policy_engine=budget_policy_engine, knowledge=knowledge
        )


def _registry_with_one_engine() -> InMemoryEngineRegistry:
    registry = InMemoryEngineRegistry()
    registry.register("engine-a", FakeEngineAdapter())
    return registry


def test_recommended_order_first_recorded_wins_on_full_tie_without_cost_deps() -> None:
    """M73 이전과 100% 동일 동작(회귀 확인): 비용 의존성을 주입하지 않으면
    성공률·표본 수까지 완전히 동률인 두 순서 중 먼저 기록된 순서가
    그대로 이긴다(기존 tie-break)."""
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])

    for _ in range(3):
        engine.record_run_outcome(workflow, ["t1", "t2"], True)
    for _ in range(3):
        engine.record_run_outcome(workflow, ["t2", "t1"], True)

    assert engine.recommended_order(workflow) == ["t1", "t2"]


def test_recommended_order_exercises_cost_tie_break_without_changing_full_tie() -> None:
    """M73(ADR-0091): task_engine/engine_registry/engine_selection_policy가
    모두 주입되면 성공률 동률 후보의 비용 계산 경로(`EngineSelectionPolicy.
    select()`)가 실제로 실행된다. 같은 task_id 집합의 순열은 비용 합이
    항상 동일하므로(EngineSelectionPolicy는 순서를 모르는 순수함수) 비용
    비교는 후보를 좁히지 못하고, 최종 결과는 기존 tie-break(먼저 기록된
    순서)와 동일하다."""
    task_engine = InMemoryTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task")
    spy = _SpyEngineSelectionPolicy()
    engine = InMemoryWorkflowEngine(
        task_engine=task_engine,
        engine_registry=_registry_with_one_engine(),
        engine_selection_policy=spy,
    )
    workflow = _workflow([task1.task_id, task2.task_id])
    order_a = [task1.task_id, task2.task_id]
    order_b = [task2.task_id, task1.task_id]
    for _ in range(3):
        engine.record_run_outcome(workflow, order_a, True)
    for _ in range(3):
        engine.record_run_outcome(workflow, order_b, True)

    result = engine.recommended_order(workflow)

    assert result == order_a
    assert spy.call_count > 0


def test_recommended_order_falls_back_when_cost_cannot_be_computed() -> None:
    """M73(ADR-0091): 비용 의존성은 모두 주입됐지만 Task 조회가 실패하면
    (예: Workflow의 task_id가 TaskEngine에 없음) 비용 계산을 포기하고
    기존 tie-break(먼저 기록된 순서)로 즉시 fallback한다."""
    task_engine = InMemoryTaskEngine()  # task_id를 하나도 만들지 않음 → 조회 실패
    engine = InMemoryWorkflowEngine(
        task_engine=task_engine,
        engine_registry=_registry_with_one_engine(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    workflow = _workflow(["t1", "t2"])

    for _ in range(3):
        engine.record_run_outcome(workflow, ["t1", "t2"], True)
    for _ in range(3):
        engine.record_run_outcome(workflow, ["t2", "t1"], True)

    assert engine.recommended_order(workflow) == ["t1", "t2"]


def test_recommended_order_falls_back_when_engine_registry_has_no_candidates() -> None:
    """M73(ADR-0091): Engine이 하나도 등록돼 있지 않아 후보가 없으면(비용
    계산 불가) 기존 tie-break로 즉시 fallback한다."""
    task_engine = InMemoryTaskEngine()
    task1 = task_engine.create_task("p1", "첫 번째 Task")
    task2 = task_engine.create_task("p1", "두 번째 Task")
    engine = InMemoryWorkflowEngine(
        task_engine=task_engine,
        engine_registry=InMemoryEngineRegistry(),
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
    )
    workflow = _workflow([task1.task_id, task2.task_id])
    order_a = [task1.task_id, task2.task_id]
    order_b = [task2.task_id, task1.task_id]

    for _ in range(3):
        engine.record_run_outcome(workflow, order_a, True)
    for _ in range(3):
        engine.record_run_outcome(workflow, order_b, True)

    assert engine.recommended_order(workflow) == order_a


def test_export_learning_state_empty_when_no_history() -> None:
    """M83(ADR-0101): 기록이 없으면 `order_stats`가 빈 리스트다."""
    engine = InMemoryWorkflowEngine()

    assert engine.export_learning_state() == {"order_stats": []}


def test_export_then_import_round_trips_recommended_order() -> None:
    """M83(ADR-0101): `export_learning_state()`가 만든 스냅샷을 새
    인스턴스에 `import_learning_state()`하면 학습 상태(추천 순서)가
    그대로 복원된다."""
    original = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])
    for _ in range(3):
        original.record_run_outcome(workflow, ["t2", "t1"], False)
    for _ in range(3):
        original.record_run_outcome(workflow, ["t1", "t2"], True)

    state = original.export_learning_state()

    restored = InMemoryWorkflowEngine()
    assert restored.recommended_order(workflow) is None

    restored.import_learning_state(state)

    assert restored.recommended_order(workflow) == ["t1", "t2"]
    assert restored.export_learning_state() == state


def test_import_learning_state_replaces_not_merges_existing_state() -> None:
    """M83(ADR-0101): `import_learning_state()`는 기존에 누적된 학습
    상태를 대체한다 — 병합이 아니다."""
    engine = InMemoryWorkflowEngine()
    workflow = _workflow(["t1", "t2"])
    for _ in range(3):
        engine.record_run_outcome(workflow, ["t1", "t2"], True)
    assert engine.recommended_order(workflow) == ["t1", "t2"]

    engine.import_learning_state({"order_stats": []})

    assert engine.recommended_order(workflow) is None
