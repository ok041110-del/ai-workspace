from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.interfaces.authentication_manager import AuthenticationStatus


def test_registered_engine_is_authenticated() -> None:
    manager = InMemoryAuthenticationManager(frozenset({"claude_code"}))

    assert manager.is_authenticated("claude_code") is True
    assert manager.authentication_status("claude_code") == AuthenticationStatus.AUTHENTICATED


def test_unregistered_engine_is_not_authenticated() -> None:
    manager = InMemoryAuthenticationManager(frozenset({"claude_code"}))

    assert manager.is_authenticated("codex") is False
    assert manager.authentication_status("codex") == AuthenticationStatus.UNAUTHENTICATED


def test_no_authenticated_engines_by_default() -> None:
    manager = InMemoryAuthenticationManager()

    assert manager.is_authenticated("claude_code") is False
