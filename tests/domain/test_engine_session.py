from ai_workspace.domain.engine_session import EngineSession


def test_engine_session_holds_session_and_task_id() -> None:
    session = EngineSession(session_id="es1", task_id="t1")

    assert session.session_id == "es1"
    assert session.task_id == "t1"
