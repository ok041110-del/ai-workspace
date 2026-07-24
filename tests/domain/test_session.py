from ai_workspace.domain.session import WorkspaceSession


def test_session_defaults_to_empty_state() -> None:
    session = WorkspaceSession(session_id="s1")

    assert session.current_project_id is None
    assert session.current_mission_id is None
    assert session.active_workflow_id is None
    assert session.active_agent_ids == []
    assert session.memory_snapshot_id is None
    assert session.engine_session_id is None


def test_session_holds_active_state() -> None:
    session = WorkspaceSession(
        session_id="s1",
        current_project_id="p1",
        current_mission_id="m1",
        active_workflow_id="w1",
        active_agent_ids=["a1", "a2"],
        memory_snapshot_id="snap1",
        engine_session_id="es1",
    )

    assert session.current_project_id == "p1"
    assert session.active_agent_ids == ["a1", "a2"]
