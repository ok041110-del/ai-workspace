from __future__ import annotations

from ai_workspace.interfaces.interaction_engine import (
    InteractionEngine,
    NormalizedRequest,
    UnsupportedSurfaceError,
)


class InMemoryInteractionEngine(InteractionEngine):
    """자유 텍스트 기반 UI Surface(Voice/Slack/REST API 등)의 입력을
    `NormalizedRequest`로 정규화하는 최소 구현체(ARCHITECTURE.md §3.2,
    ADR-0013, M4-T03). CLI는 이미 argparse로 구조화된 입력을 제공하므로
    이 계층을 거치지 않는 예외적인 Surface다(`docs/ARCHITECTURE.md` §3.1
    참고) — `cli/main.py`는 계속 `WorkspaceCore`를 직접 호출한다."""

    def __init__(self, surfaces: frozenset[str] = frozenset()) -> None:
        self._surfaces = surfaces

    def normalize(
        self, surface: str, raw_input: str, session_id: str | None = None
    ) -> NormalizedRequest:
        if surface not in self._surfaces:
            raise UnsupportedSurfaceError(surface)
        return NormalizedRequest(surface=surface, text=raw_input.strip(), session_id=session_id)

    def format_response(self, surface: str, message: str) -> str:
        if surface not in self._surfaces:
            raise UnsupportedSurfaceError(surface)
        return message

    def supported_surfaces(self) -> frozenset[str]:
        return self._surfaces
