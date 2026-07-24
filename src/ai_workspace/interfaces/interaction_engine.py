from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class UnsupportedSurfaceError(Exception):
    """지원하지 않는 surface(예: 등록되지 않은 UI 표면)를 사용하려 할 때
    발생한다."""


@dataclass
class NormalizedRequest:
    surface: str
    text: str
    session_id: str | None = None


class InteractionEngine(ABC):
    """다양한 UI Surfaces(CLI/Dashboard/Mobile/Voice/REST API/Slack/Discord/
    Webhook)의 입력을 표준 요청으로 정규화하고, Workspace Core의 응답을 다시
    표면에 맞게 변환하는 계약(ARCHITECTURE.md §3.2, ADR-0013). 기존
    `ConversationEngine` 명칭을 대체한다. Agent Runtime/Engine Runtime/Memory
    어느 것에도 의존하지 않는 독립 계층이며, 오직 UI Surfaces와 Workspace Core
    사이에만 위치한다(ARCHITECTURE.md §8 의존성 규칙 1~2)."""

    @abstractmethod
    def normalize(
        self, surface: str, raw_input: str, session_id: str | None = None
    ) -> NormalizedRequest:
        """
        입력: surface (입력이 들어온 표면 식별자, 예: "cli"/"voice"/"slack"),
              raw_input (표면에서 받은 원본 입력), session_id (기존
              WorkspaceSession과 연결할 경우 선택적으로 전달)
        출력: 표준화된 NormalizedRequest
        예외: supported_surfaces()에 없는 surface면 UnsupportedSurfaceError
        보장: 반환된 NormalizedRequest.surface는 입력받은 surface와 동일하다.
        """
        raise NotImplementedError

    @abstractmethod
    def format_response(self, surface: str, message: str) -> str:
        """
        입력: surface, message (Workspace Core가 반환한 표면 비종속 응답 텍스트)
        출력: surface에 맞게 변환된 응답 문자열
        예외: supported_surfaces()에 없는 surface면 UnsupportedSurfaceError
        보장: 없음(표면별 변환 규칙은 구현체마다 다르다).
        """
        raise NotImplementedError

    @abstractmethod
    def supported_surfaces(self) -> frozenset[str]:
        """
        입력: 없음
        출력: 이 InteractionEngine이 지원하는 surface 식별자 집합
        예외: 없음
        보장: 항상 동일한 결과를 반환한다(정적 정보).
        """
        raise NotImplementedError
