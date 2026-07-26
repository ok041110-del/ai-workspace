from __future__ import annotations

from ai_workspace.adapters.process_runner import ProcessNotFoundError, ProcessRunner
from ai_workspace.interfaces.execution_environment import (
    ExecutionEnvironment,
    ExecutionNotFoundError,
    ExecutionResult,
)


class LocalExecutionEnvironment(ExecutionEnvironment):
    """`ExecutionEnvironment`의 로컬 프로세스 구현체(Milestone 11). 새
    프로세스 관리 로직을 새로 만들지 않고, 이미 검증된 `ProcessRunner`
    (M3-T03)에 그대로 위임한다 — `ExecutionEnvironment`가 요구하는 계약
    (환경 비종속 명명, 예외 타입)에 맞게 얇게 감싸기만 한다."""

    def __init__(self, *, process_runner: ProcessRunner | None = None) -> None:
        self._process_runner = process_runner if process_runner is not None else ProcessRunner()

    def execute(
        self,
        execution_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ExecutionResult:
        result = self._process_runner.run(execution_id, command, cwd=cwd, timeout=timeout)
        return ExecutionResult(
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            timed_out=result.timed_out,
            cancelled=result.cancelled,
        )

    def cancel(self, execution_id: str) -> None:
        try:
            self._process_runner.cancel(execution_id)
        except ProcessNotFoundError as exc:
            raise ExecutionNotFoundError(execution_id) from exc
