from pathlib import Path

from ai_workspace.domain.execution_memory import ExecutionMemory
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.observability.learning_runtime_analyzer import LearningRuntimeAnalyzer
from ai_workspace.storage.file_memory_engine import FileMemoryEngine


def _record(store: ExecutionMemoryStore, task_id: str, result: str, timestamp: str) -> None:
    store.record(
        ExecutionMemory(task_id=task_id, action="실행", result=result, timestamp=timestamp)
    )


def test_analyze_returns_zero_tracked_tasks_when_no_records(tmp_path: Path) -> None:
    info = LearningRuntimeAnalyzer().analyze(tmp_path)

    assert info.tracked_task_count == 0
    assert info.highest_risk_task_id is None
    assert info.highest_risk_decayed_failure_rate is None
    assert info.highest_risk_recent_failure_streak is None


def test_analyze_reflects_records_persisted_by_file_memory_engine(tmp_path: Path) -> None:
    """M54(ADR-0072) — M50이 영속화한 FileMemoryEngine 데이터를
    별도 프로세스(이 Analyzer)에서 그대로 읽을 수 있음을 확인."""
    store = ExecutionMemoryStore(FileMemoryEngine(tmp_path / ".ai-workspace-data"))
    _record(store, "M42-T01", "failure", "2026-07-30T00:00:00")
    _record(store, "M42-T01", "failure", "2026-07-30T01:00:00")
    _record(store, "M42-T01", "failure", "2026-07-30T02:00:00")
    _record(store, "M42-T02", "success", "2026-07-30T00:00:00")

    info = LearningRuntimeAnalyzer().analyze(tmp_path)

    assert info.tracked_task_count == 2
    assert info.highest_risk_task_id == "M42-T01"
    assert info.highest_risk_decayed_failure_rate == 1.0
    assert info.highest_risk_recent_failure_streak == 3


def test_analyze_breaks_ties_by_task_id_ascending(tmp_path: Path) -> None:
    store = ExecutionMemoryStore(FileMemoryEngine(tmp_path / ".ai-workspace-data"))
    _record(store, "M42-T02", "failure", "2026-07-30T00:00:00")
    _record(store, "M42-T01", "failure", "2026-07-30T00:00:00")

    info = LearningRuntimeAnalyzer().analyze(tmp_path)

    assert info.highest_risk_task_id == "M42-T01"
