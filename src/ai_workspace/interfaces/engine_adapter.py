from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from ai_workspace.domain.task import Task


class EngineExecutionError(Exception):
    """구현 엔진 호출 자체가 불가능했을 때(프로세스 실행 실패 등) 발생한다.
    Task 자체의 실패는 예외가 아니라 EngineResult(success=False)로 표현한다."""


class SessionNotFoundError(Exception):
    """존재하지 않거나 이미 destroy_session()된 session_id를 사용하려 할 때
    발생한다."""


@dataclass
class EngineResult:
    success: bool
    output: str
    error: str | None = None


class EngineSessionStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class CostEstimate:
    estimated_tokens: int
    estimated_cost_usd: float


class EngineAdapter(ABC):
    """구현 엔진(Claude Code/Codex/Gemini CLI 등)을 호출하는 세션 기반 공통
    계약(ADR-0009, ADR-0015). ClaudeCodeAdapter, CodexAdapter, GeminiCliAdapter가
    이 계약을 구현한다(구체 구현은 Milestone 3). Engine Runtime만 이 계약을
    호출하며, Agent는 이 인터페이스를 직접 호출하지 않는다(ARCHITECTURE.md
    §8 의존성 규칙 6)."""

    @abstractmethod
    def create_session(self) -> str:
        """
        입력: 없음
        출력: 새로 생성된 세션을 식별하는 session_id
        예외: 없음
        보장: 반환된 session_id는 이 어댑터가 이미 생성한 다른 어떤 session_id와도
              겹치지 않으며, destroy_session()되기 전까지 run()/cancel()/
              status()에 사용할 수 있다.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        """
        입력: session_id (create_session()이 반환한 값), task (실행할 Task),
              model (선택적, 이번 실행에 쓸 모델 이름 — 예: "opus". 생략
              시 이 Adapter의 기본 모델을 그대로 쓴다. 모델별 실행을
              지원하지 않는 Adapter는 이 값을 무시할 수 있다)
        출력: EngineResult(success, output, error)
        예외: session_id가 유효하지 않으면 SessionNotFoundError. 구현 엔진을
              호출하는 과정 자체가 실패하면(예: 실행 파일을 찾을 수 없음,
              타임아웃) EngineExecutionError. Task 처리 자체가 실패한 경우는
              예외를 던지지 않고 EngineResult(success=False, error=...)로
              반환한다.
        보장: 예외 없이 반환되었다면 EngineResult.success로 성공/실패를 항상
              판별할 수 있으며, success=False일 때 error는 None이 아니다.
              model을 생략하면 이전 계약(Milestone 14 이전)과 동일하게
              동작한다.
        """
        raise NotImplementedError

    @abstractmethod
    def cancel(self, session_id: str) -> None:
        """
        입력: session_id
        출력: 없음
        예외: session_id가 유효하지 않으면 SessionNotFoundError
        보장: cancel(session_id) 이후 status(session_id)는 CANCELLED를
              반환한다(이미 COMPLETED/FAILED로 끝난 세션은 상태가 유지된다).
        """
        raise NotImplementedError

    @abstractmethod
    def status(self, session_id: str) -> EngineSessionStatus:
        """
        입력: session_id
        출력: 해당 세션에서 가장 최근에 실행된 작업의 상태
        예외: session_id가 유효하지 않으면 SessionNotFoundError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def destroy_session(self, session_id: str) -> None:
        """
        입력: session_id
        출력: 없음
        예외: session_id가 유효하지 않으면 SessionNotFoundError
        보장: destroy_session(session_id) 이후 그 session_id로 run()/cancel()/
              status()를 호출하면 SessionNotFoundError가 발생한다.
        """
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> frozenset[str]:
        """
        입력: 없음
        출력: 이 엔진이 지원하는 능력 태그 집합(예: "code_generation", "vision")
        예외: 없음
        보장: 세션 생성 여부와 무관하게 항상 동일한 결과를 반환한다(정적 정보).
        """
        raise NotImplementedError

    @abstractmethod
    def supports_parallel(self) -> bool:
        """
        입력: 없음
        출력: 이 엔진이 여러 세션을 동시에 실행하는 것을 지원하면 True
        예외: 없음
        보장: 세션 생성 여부와 무관하게 항상 동일한 결과를 반환한다(정적 정보).
        """
        raise NotImplementedError

    @abstractmethod
    def estimate_cost(self, task: Task) -> CostEstimate:
        """
        입력: 비용을 추정할 Task (세션 생성 없이 호출 가능)
        출력: CostEstimate(estimated_tokens, estimated_cost_usd)
        예외: 없음
        보장: side-effect 없음(세션을 생성하거나 실제로 실행하지 않는다).
        """
        raise NotImplementedError
