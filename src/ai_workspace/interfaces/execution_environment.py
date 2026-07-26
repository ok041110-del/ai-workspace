from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class ExecutionNotFoundError(Exception):
    """관리 중이지 않은 execution_id를 취소하려 할 때 발생한다."""


@dataclass
class ExecutionResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    cancelled: bool = False


class ExecutionEnvironment(ABC):
    """`EngineAdapter`가 명령을 실제로 실행할 장소를 추상화하는 하위(내부)
    계약(Milestone 11). `EngineAdapter`(예: `ClaudeCodeEngineAdapter`,
    `CLIEngineAdapter`)가 조립한 명령을 "어디서" 실행할지만 담당하며,
    "무엇을" 실행할지(명령 조립·결과 파싱)는 여전히 `EngineAdapter`의
    책임이다. `execution_id`는 특정 실행 방식(OS 프로세스 등)을 가정하지
    않는 이름이다 — 로컬 프로세스든, 향후 원격 컨테이너 세션이든 모두 이
    식별자로 다뤄진다.

    `EngineAdapter`는 이 인터페이스를 생성자 주입(Dependency Injection)으로
    받아 사용하며, 구체 구현체를 직접 생성하지 않는다. Agent/Engine Runtime은
    이 인터페이스의 존재를 알지 못한다 — `EngineAdapter` 내부에만 위치한다."""

    @abstractmethod
    def execute(
        self,
        execution_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ExecutionResult:
        """
        입력: execution_id (호출자가 지정하는 고유 식별자), command (실행할
              명령과 인자 목록), cwd (작업 디렉터리, 생략 시 환경 기본값),
              timeout (초 단위 제한 시간, 생략 시 무제한)
        출력: ExecutionResult(returncode, stdout, stderr, timed_out, cancelled)
        예외: 명령을 실행할 수 없으면(예: 실행 파일을 찾을 수 없음)
              FileNotFoundError
        보장: timeout을 넘기면 예외 대신 timed_out=True로 반환한다. 같은
              execute() 호출이 실행되는 동안 같은 execution_id로 cancel()이
              호출되면 cancelled=True로 반환한다. 두 경우 모두 예외를 던지지
              않는다 — 실행 파일 자체를 찾지 못한 경우만 예외로 구분한다.
        """
        raise NotImplementedError

    @abstractmethod
    def cancel(self, execution_id: str) -> None:
        """
        입력: 실행 중인 execute() 호출에 사용된 execution_id
        출력: 없음
        예외: 해당 execution_id로 실행 중인 작업이 없으면
              ExecutionNotFoundError
        보장: 실행 중인 명령을 즉시 종료 요청한다. 그 execute() 호출은
              ExecutionResult(cancelled=True)로 반환된다.
        """
        raise NotImplementedError
