import pytest

from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.interfaces.context_manager import SnapshotNotFoundError
from ai_workspace.memory.context_manager import InMemoryContextManager
from ai_workspace.memory.memory_engine import InMemoryMemoryEngine


def test_assemble_context_includes_project_and_mission() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())
    session = WorkspaceSession(session_id="s1", current_project_id="p1", current_mission_id="m1")

    context = manager.assemble_context(session)

    assert context == {"project_id": "p1", "mission_id": "m1"}


def test_assemble_context_empty_when_session_has_no_state() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())
    session = WorkspaceSession(session_id="s1")

    assert manager.assemble_context(session) == {}


def test_create_snapshot_then_restore_round_trips() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())
    session = WorkspaceSession(session_id="s1", current_project_id="p1", current_mission_id="m1")

    snapshot_id = manager.create_snapshot(session)

    assert manager.restore_snapshot(snapshot_id) == manager.assemble_context(session)


def test_create_snapshot_stores_via_memory_engine() -> None:
    """ContextManager가 자체 dict가 아니라 MemoryEngine을 거쳐 저장함을
    증명한다(ARCHITECTURE.md §8 규칙 7, T2-04 DoD)."""
    memory_engine = InMemoryMemoryEngine()
    manager = InMemoryContextManager(memory_engine)
    session = WorkspaceSession(session_id="s1", current_project_id="p1")

    snapshot_id = manager.create_snapshot(session)

    assert memory_engine.recall(snapshot_id) is not None


def test_restore_snapshot_unknown_raises_error() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())

    with pytest.raises(SnapshotNotFoundError):
        manager.restore_snapshot("unknown")


def test_restore_snapshot_returns_defensive_copy() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())
    session = WorkspaceSession(session_id="s1", current_project_id="p1")
    snapshot_id = manager.create_snapshot(session)

    restored = manager.restore_snapshot(snapshot_id)
    restored["project_id"] = "tampered"

    assert manager.restore_snapshot(snapshot_id)["project_id"] == "p1"


def test_assemble_context_reflects_restored_snapshot() -> None:
    memory_engine = InMemoryMemoryEngine()
    manager = InMemoryContextManager(memory_engine)
    session = WorkspaceSession(session_id="s1", current_project_id="p1")
    snapshot_id = manager.create_snapshot(session)

    later_session = WorkspaceSession(session_id="s2", memory_snapshot_id=snapshot_id)

    assert manager.assemble_context(later_session) == {"project_id": "p1"}


def test_find_snapshots_returns_matching_snapshot_ids() -> None:
    manager = InMemoryContextManager(InMemoryMemoryEngine())
    snapshot_id = manager.create_snapshot(
        WorkspaceSession(session_id="s1", current_project_id="p1")
    )
    manager.create_snapshot(WorkspaceSession(session_id="s2", current_project_id="p2"))

    assert manager.find_snapshots("p1") == [snapshot_id]


def test_find_snapshots_delegates_to_memory_engine_search() -> None:
    """M4-T08: 검색은 MemoryEngine.search()에 위임됨을 증명한다(§8 규칙 7
    — Agent는 ContextManager를 통해서만 검색하고 MemoryEngine을 직접
    호출하지 않는다)."""
    memory_engine = InMemoryMemoryEngine()
    manager = InMemoryContextManager(memory_engine)
    snapshot_id = manager.create_snapshot(
        WorkspaceSession(session_id="s1", current_project_id="p1")
    )

    assert manager.find_snapshots("p1") == memory_engine.search("p1") == [snapshot_id]
