import pytest

from ai_workspace.interfaces.interaction_engine import UnsupportedSurfaceError

from .fakes import FakeInteractionEngine


def test_normalize_returns_request_with_same_surface_and_trimmed_text() -> None:
    engine = FakeInteractionEngine(frozenset({"cli"}))

    request = engine.normalize("cli", "  hello  ", session_id="s1")

    assert request.surface == "cli"
    assert request.text == "hello"
    assert request.session_id == "s1"


def test_normalize_unsupported_surface_raises_error() -> None:
    engine = FakeInteractionEngine(frozenset({"cli"}))

    with pytest.raises(UnsupportedSurfaceError):
        engine.normalize("voice", "hello")


def test_format_response_unsupported_surface_raises_error() -> None:
    engine = FakeInteractionEngine(frozenset({"cli"}))

    with pytest.raises(UnsupportedSurfaceError):
        engine.format_response("voice", "완료되었습니다")


def test_supported_surfaces_returns_configured_set() -> None:
    engine = FakeInteractionEngine(frozenset({"cli", "slack"}))

    assert engine.supported_surfaces() == frozenset({"cli", "slack"})
