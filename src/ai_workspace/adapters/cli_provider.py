from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.adapters.process_runner import ProcessResult
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineResult


class CLIProvider(ABC):
    """CLI 기반 구현 엔진(Codex/Gemini CLI 등)마다 다른 명령 조립·결과
    파싱 방식을 캡슐화하는 전략 객체(M5-T05). `CLIEngineAdapter`가 이
    계약을 통해 실제 CLI 프로세스를 실행한다.

    `EngineAdapter`(interfaces/)처럼 상위 계층이 직접 의존하는 보호
    자산이 아니라, `adapters/` 내부에서만 쓰이는 협력자다 — Agent나
    WorkspaceCore는 이 계약을 알지 못하고 `CLIEngineAdapter`(EngineAdapter
    구현체)만 상대한다."""

    @abstractmethod
    def build_command(self, session_id: str, task: Task) -> list[str]:
        """
        입력: session_id, task
        출력: 실행할 커맨드라인 인자 목록
        예외: 없음
        보장: side-effect 없음(read-only) — 이 메서드는 명령을 조립만
              하고 실행하지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def parse_result(self, process_result: ProcessResult) -> EngineResult:
        """
        입력: 프로세스 실행이 끝난 뒤의 ProcessResult
        출력: EngineResult(success, output, error)
        예외: 없음(파싱 실패는 예외가 아니라 success=False로 표현)
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> frozenset[str]:
        """이 CLI가 지원하는 능력 태그 집합(정적 정보)."""
        raise NotImplementedError

    @abstractmethod
    def supports_parallel(self) -> bool:
        """이 CLI가 여러 세션 동시 실행을 지원하면 True(정적 정보)."""
        raise NotImplementedError
