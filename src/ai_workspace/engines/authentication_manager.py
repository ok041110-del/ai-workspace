from __future__ import annotations

from ai_workspace.interfaces.authentication_manager import (
    AuthenticationManager,
    AuthenticationStatus,
)


class InMemoryAuthenticationManager(AuthenticationManager):
    """생성 시 주어진 인증된 Engine 이름 집합으로 상태를 확인하는 최소
    구현체(M18-T01). 실제 로그인/OAuth/Credential 저장을 전혀 다루지
    않는다 — 이미 인증된 것으로 간주할 Engine 이름을 그대로 전달받을
    뿐이다."""

    def __init__(self, authenticated_engines: frozenset[str] | None = None) -> None:
        self._authenticated_engines = (
            frozenset(authenticated_engines) if authenticated_engines is not None else frozenset()
        )

    def is_authenticated(self, engine_name: str) -> bool:
        return engine_name in self._authenticated_engines

    def authentication_status(self, engine_name: str) -> AuthenticationStatus:
        if self.is_authenticated(engine_name):
            return AuthenticationStatus.AUTHENTICATED
        return AuthenticationStatus.UNAUTHENTICATED
