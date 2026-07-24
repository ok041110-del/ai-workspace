import pytest

from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.interfaces.context_manager import SnapshotNotFoundError

from .fakes import FakeContextManager


def test_assemble_context_includes_project_and_mission_ids() -> None:
    manager = FakeContextManager()
    session = WorkspaceSession(
        session_id="s1", current_project_id="p1", current_mission_id="m1"
    )

    context = manager.assemble_context(session)

    assert context == {"project_id": "p1", "mission_id": "m1"}


def test_create_snapshot_then_restore_returns_same_context() -> None:
    manager = FakeContextManager()
    session = WorkspaceSession(session_id="s1", current_project_id="p1")

    snapshot_id = manager.create_snapshot(session)

    assert manager.restore_snapshot(snapshot_id) == manager.assemble_context(session)


def test_restore_unknown_snapshot_raises_not_found() -> None:
    manager = FakeContextManager()

    with pytest.raises(SnapshotNotFoundError):
        manager.restore_snapshot("unknown")


def test_restore_snapshot_returns_defensive_copy() -> None:
    manager = FakeContextManager()
    session = WorkspaceSession(session_id="s1", current_project_id="p1")
    snapshot_id = manager.create_snapshot(session)

    context = manager.restore_snapshot(snapshot_id)
    context["extra"] = "mutated"

    assert "extra" not in manager.restore_snapshot(snapshot_id)
