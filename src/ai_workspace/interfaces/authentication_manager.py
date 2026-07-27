from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class AuthenticationStatus(Enum):
    AUTHENTICATED = "authenticated"
    UNAUTHENTICATED = "unauthenticated"


class AuthenticationRequiredError(Exception):
    """선택된 Engine이 인증되어 있지 않은 상태에서 실행을 시도할 때
    발생한다(`ExecutionDispatcher`가 던진다)."""


class AuthenticationManager(ABC):
    """Engine별 실행 가능한 인증 상태인지 **확인만** 하는 계약
    (M18-T01). 이번 Milestone은 "로그인을 수행"하는 것이 아니라
    "실행 가능한 인증 상태인지 확인"하는 역할만 담당한다 — `login()`/
    `logout()`은 의도적으로 이 계약에 없다(실제 로그인/OAuth/API Key/
    Credential 저장/Token Refresh는 범위 밖). Workspace는 CLI 로그인
    명령을 직접 실행하지 않는다."""

    @abstractmethod
    def is_authenticated(self, engine_name: str) -> bool:
        """
        입력: engine_name (확인할 Engine 식별 이름)
        출력: 실행 가능한 인증 상태이면 True
        예외: 없음
        보장: side-effect 없음(read-only). 등록되지 않은 engine_name에
              대해서도 예외 없이 False를 반환한다(인증 여부와 등록
              여부는 서로 다른 질문 — 등록 여부 확인은 `EngineRegistry`
              의 책임이다).
        """
        raise NotImplementedError

    @abstractmethod
    def authentication_status(self, engine_name: str) -> AuthenticationStatus:
        """
        입력: engine_name
        출력: AuthenticationStatus(AUTHENTICATED 또는 UNAUTHENTICATED)
        예외: 없음
        보장: side-effect 없음(read-only). `is_authenticated(engine_name)`
              이 True이면 이 메서드는 AUTHENTICATED를 반환한다(둘은
              같은 상태를 서로 다른 형태로 노출할 뿐이다).
        """
        raise NotImplementedError
