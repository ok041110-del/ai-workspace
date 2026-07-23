from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ai_workspace.domain.task import Task


class EngineExecutionError(Exception):
    """구현 엔진 호출 자체가 불가능했을 때(프로세스 실행 실패 등) 발생한다.
    Task 자체의 실패는 예외가 아니라 EngineResult(success=False)로 표현한다."""


@dataclass
class EngineResult:
    success: bool
    output: str
    error: str | None = None


class EngineAdapter(ABC):
    """구현 엔진(Claude Code/Codex/Gemini CLI 등)을 호출하는 공통 계약.
    ClaudeCodeAdapter, CodexAdapter, GeminiCliAdapter가 이 계약을 구현한다
    (구체 구현은 Phase 3)."""

    @abstractmethod
    def run_task(self, task: Task) -> EngineResult:
        """
        입력: 구현 엔진에 위임할 Task
        출력: EngineResult(success, output, error)
        예외: 구현 엔진을 호출하는 과정 자체가 실패하면(예: 실행 파일을 찾을
              수 없음, 타임아웃) EngineExecutionError. Task 처리 자체가
              실패한 경우는 예외를 던지지 않고 EngineResult(success=False,
              error=...)로 반환한다.
        보장: 예외 없이 반환되었다면 EngineResult.success로 성공/실패를
              항상 판별할 수 있으며, success=False일 때 error는 None이 아니다.
        """
        raise NotImplementedError
