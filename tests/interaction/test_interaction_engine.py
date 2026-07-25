import pytest

from ai_workspace.interaction.interaction_engine import InMemoryInteractionEngine
from ai_workspace.interfaces.interaction_engine import UnsupportedSurfaceError


def test_normalize_returns_request_with_same_surface_and_trimmed_text() -> None:
    engine = InMemoryInteractionEngine(frozenset({"voice"}))

    request = engine.normalize("voice", "  hello  ", session_id="s1")

    assert request.surface == "voice"
    assert request.text == "hello"
    assert request.session_id == "s1"


def test_normalize_unsupported_surface_raises_error() -> None:
    engine = InMemoryInteractionEngine(frozenset({"voice"}))

    with pytest.raises(UnsupportedSurfaceError):
        engine.normalize("slack", "hello")


def test_format_response_unsupported_surface_raises_error() -> None:
    engine = InMemoryInteractionEngine(frozenset({"voice"}))

    with pytest.raises(UnsupportedSurfaceError):
        engine.format_response("slack", "완료되었습니다")


def test_supported_surfaces_returns_configured_set() -> None:
    engine = InMemoryInteractionEngine(frozenset({"voice", "slack"}))

    assert engine.supported_surfaces() == frozenset({"voice", "slack"})


def test_supported_surfaces_defaults_to_empty() -> None:
    engine = InMemoryInteractionEngine()

    assert engine.supported_surfaces() == frozenset()
