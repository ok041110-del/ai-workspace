from __future__ import annotations

import subprocess
from dataclasses import dataclass

_DEFAULT_TERMINATION_GRACE_SECONDS = 5.0


class ProcessNotFoundError(Exception):
    """관리 중이지 않은 process_id를 취소하려 할 때 발생한다."""


@dataclass
class ProcessResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    cancelled: bool = False


class ProcessRunner:
    """`subprocess.Popen` 기반으로 외부 프로세스를 실행·감시·종료하는 최소
    구현체(M3-T03). `EngineAdapter` 구현체(예: `ClaudeCodeEngineAdapter`)가
    실제 CLI 프로세스를 실행할 때 사용한다. Timeout 시 `terminate()`(SIGTERM)
    후 유예 시간 안에 종료하지 않으면 `kill()`(SIGKILL)한다. 실행 중
    `cancel()`이 호출되면 즉시 `terminate()`한다."""

    def __init__(
        self, *, termination_grace_seconds: float = _DEFAULT_TERMINATION_GRACE_SECONDS
    ) -> None:
        self._termination_grace_seconds = termination_grace_seconds
        self._processes: dict[str, subprocess.Popen[str]] = {}
        self._cancelled_ids: set[str] = set()

    def run(
        self,
        process_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ProcessResult:
        process = subprocess.Popen(
            command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        self._processes[process_id] = process
        try:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                return self._force_stop(process, timed_out=True)
            cancelled = process_id in self._cancelled_ids
            return ProcessResult(
                returncode=process.returncode, stdout=stdout, stderr=stderr, cancelled=cancelled
            )
        finally:
            self._processes.pop(process_id, None)
            self._cancelled_ids.discard(process_id)

    def cancel(self, process_id: str) -> None:
        process = self._processes.get(process_id)
        if process is None:
            raise ProcessNotFoundError(process_id)
        self._cancelled_ids.add(process_id)
        process.terminate()

    def _force_stop(self, process: subprocess.Popen[str], *, timed_out: bool) -> ProcessResult:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=self._termination_grace_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
        return ProcessResult(
            returncode=process.returncode,
            stdout=stdout or "",
            stderr=stderr or "",
            timed_out=timed_out,
        )
