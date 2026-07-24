from __future__ import annotations

import pytest

from ai_workspace.interfaces.interaction_engine import (
    InteractionRequest,
    InvalidRequestError,
)

from .fakes import FakeInteractionEngine


def test_interaction_engine_success() -> None:
    engine = FakeInteractionEngine()
    request = InteractionRequest(
        user_id="user-1",
        channel="cli",
        message="Hello Workspace",
        payload={"verbose": "true"},
    )
    response = engine.handle_request(request)

    assert response.channel == "cli"
    assert response.message == "수신 완료: Hello Workspace"
    assert response.success is True
    assert response.payload == {"processed": "true"}
    assert request in engine._handled


def test_interaction_engine_invalid_user_id() -> None:
    engine = FakeInteractionEngine()
    request = InteractionRequest(
        user_id="",
        channel="slack",
        message="Failure test",
    )

    with pytest.raises(InvalidRequestError) as exc_info:
        engine.handle_request(request)

    assert "user_id는 비어 있을 수 없습니다." in str(exc_info.value)


def test_interaction_engine_invalid_message() -> None:
    engine = FakeInteractionEngine()
    request = InteractionRequest(
        user_id="user-2",
        channel="api",
        message="fail",
    )

    with pytest.raises(InvalidRequestError) as exc_info:
        engine.handle_request(request)

    assert "유효하지 않은 요청 메시지입니다." in str(exc_info.value)
