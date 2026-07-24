from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class InteractionRequest:
    """UI Surface(CLI, Slack, API 등)로부터 수신된 표준화된 정규 요청"""
    user_id: str
    channel: str  # 예: "cli", "slack", "api", "voice"
    message: str
    payload: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class InteractionResponse:
    """Workspace Core가 처리 후 UI Surface로 다시 돌려보낼 표준 응답"""
    channel: str
    message: str
    payload: dict[str, str] = field(default_factory=dict)
    success: bool = True


class InteractionError(Exception):
    """Interaction Layer 내부 처리 과정에서 발생하는 기본 예외"""
    pass


class InvalidRequestError(InteractionError):
    """정규화 요청 내용이 유효하지 않거나 검증에 실패했을 때 던져지는 예외"""
    pass


class InteractionEngine(ABC):
    """Interaction Layer를 통칭하는 표준 입력 정규화 및 상호작용 오케스트레이터의 계약"""

    @abstractmethod
    def handle_request(self, request: InteractionRequest) -> InteractionResponse:
        """
        UI Surfaces로부터 온 입력을 처리하여 표준 응답을 반환합니다.

        입력: InteractionRequest (정규화된 사용자 입력)
        출력: InteractionResponse (비즈니스 처리 후 반환될 응답)
        예외:
            - InvalidRequestError: 메시지 내용이나 필수 값이 잘못된 경우
            - InteractionError: 기타 처리 도중 내부 오류가 난 경우
        보장: 이 메소드는 UI 표면의 통신 라이브러리에 독립적이어야 합니다.
        """
        raise NotImplementedError
