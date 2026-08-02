from pathlib import Path

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.storage.file_learning_state_store import FileLearningStateStore


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


def test_load_on_missing_file_leaves_in_process_state_untouched(tmp_path: Path) -> None:
    """M83(ADR-0101): 저장 파일이 아직 없으면(첫 실행) 조용히 아무 것도
    하지 않는다 — 기존 in-process 기본 상태(빈 상태) 그대로 진행한다."""
    store = FileLearningStateStore(tmp_path)
    engine_runtime = InMemoryEngineRuntime()
    workflow_engine = InMemoryWorkflowEngine()

    store.load(engine_runtime, workflow_engine)

    assert engine_runtime.export_learning_state() == {
        "engine_reliability": {},
        "execution_memory": [],
        "consensus_agreement": [],
        "reflections": {},
    }


def test_save_then_load_round_trips_engine_and_workflow_learning_state(tmp_path: Path) -> None:
    """M83(ADR-0101): 저장 후 새 인스턴스에 복원하면 EngineRuntime/
    WorkflowEngine 학습 상태가 모두 그대로 살아난다."""
    engine_runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    engine_runtime.register_engine("engine-a", MockEngineAdapter())
    for i in range(3):
        engine_runtime.run(make_task(f"t{i}"))

    workflow_engine = InMemoryWorkflowEngine()
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"], dependencies={})
    for _ in range(3):
        workflow_engine.record_run_outcome(workflow, ["t1", "t2"], True)

    store = FileLearningStateStore(tmp_path)
    store.save(engine_runtime, workflow_engine)

    restored_engine_runtime = InMemoryEngineRuntime()
    restored_workflow_engine = InMemoryWorkflowEngine()
    store.load(restored_engine_runtime, restored_workflow_engine)

    assert restored_engine_runtime.benchmark_profile("engine-a").execution_count == 3
    assert restored_workflow_engine.recommended_order(workflow) == ["t1", "t2"]


def test_save_creates_base_dir_if_missing(tmp_path: Path) -> None:
    base_dir = tmp_path / "nested" / ".ai-workspace-data"
    store = FileLearningStateStore(base_dir)
    engine_runtime = InMemoryEngineRuntime()
    workflow_engine = InMemoryWorkflowEngine()

    store.save(engine_runtime, workflow_engine)

    assert (base_dir / "learning_state.json").exists()


def test_load_falls_back_silently_on_corrupted_file(tmp_path: Path) -> None:
    """M83(ADR-0101): 저장 파일이 손상돼 있어도(유효하지 않은 JSON)
    예외 없이 조용히 무시하고 in-process 기본 상태로 진행한다."""
    (tmp_path / "learning_state.json").write_text("{not valid json", encoding="utf-8")
    store = FileLearningStateStore(tmp_path)
    engine_runtime = InMemoryEngineRuntime()
    workflow_engine = InMemoryWorkflowEngine()

    store.load(engine_runtime, workflow_engine)  # 예외를 던지지 않아야 한다

    assert engine_runtime.export_learning_state() == {
        "engine_reliability": {},
        "execution_memory": [],
        "consensus_agreement": [],
        "reflections": {},
    }


def test_save_falls_back_silently_when_base_dir_is_unwritable(tmp_path: Path) -> None:
    """M83(ADR-0101): 저장 대상 디렉터리를 만들 수 없는 경우(예: 같은
    이름의 파일이 이미 존재)도 예외를 던지지 않고 조용히 무시한다."""
    blocking_file = tmp_path / "blocked"
    blocking_file.write_text("i am a file, not a directory", encoding="utf-8")
    store = FileLearningStateStore(blocking_file / "nested")
    engine_runtime = InMemoryEngineRuntime()
    workflow_engine = InMemoryWorkflowEngine()

    store.save(engine_runtime, workflow_engine)  # 예외를 던지지 않아야 한다

    assert not (blocking_file / "nested").exists()
