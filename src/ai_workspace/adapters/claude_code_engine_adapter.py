from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from ai_workspace.adapters.process_runner import ProcessNotFoundError, ProcessResult, ProcessRunner
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)

_DEFAULT_SUBPROCESS_TIMEOUT_SECONDS = 600.0
_NON_MANUAL_PERMISSION_MODE = "acceptEdits"
_TERMINAL_STATUSES = frozenset({EngineSessionStatus.COMPLETED, EngineSessionStatus.FAILED})


class ClaudeCodeEngineAdapter(EngineAdapter):
    """Claude Code CLI(`claude`)를 서브프로세스로 호출하는 EngineAdapter
    (ARCHITECTURE.md §3.10, ADR-0009/0015, M3-T02/M3-T03).

    `claude -p "<prompt>" --output-format json --session-id <id>`로
    비대화형 실행하고 JSON 결과를 파싱한다. 실제 `--help`로 확인한 플래그만
    사용하며, `--permission-mode`는 헤드리스 환경에서 영원히 대기하는
    `manual`을 절대 쓰지 않는다(기본값 `acceptEdits`).

    실제 프로세스 실행·Timeout 강제 종료·Cancel은 `ProcessRunner`
    (M3-T03)에 위임한다 — `cancel()`이 실제 OS 프로세스를 종료할 수 있다.
    """

    def __init__(
        self,
        *,
        model: str | None = None,
        permission_mode: str = _NON_MANUAL_PERMISSION_MODE,
        cwd: str | Path | None = None,
        subprocess_timeout_seconds: float = _DEFAULT_SUBPROCESS_TIMEOUT_SECONDS,
        process_runner: ProcessRunner | None = None,
    ) -> None:
        if permission_mode == "manual":
            raise ValueError("permission_mode='manual'은 헤드리스 실행에서 영원히 대기한다.")
        self._model = model
        self._permission_mode = permission_mode
        self._cwd = str(cwd) if cwd is not None else None
        self._subprocess_timeout_seconds = subprocess_timeout_seconds
        self._process_runner = process_runner if process_runner is not None else ProcessRunner()
        self._sessions: dict[str, EngineSessionStatus] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task) -> EngineResult:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)

        command = self._build_command(session_id, task)
        try:
            process_result = self._process_runner.run(
                session_id, command, cwd=self._cwd, timeout=self._subprocess_timeout_seconds
            )
        except FileNotFoundError as exc:
            self._sessions[session_id] = EngineSessionStatus.FAILED
            raise EngineExecutionError("claude CLI 실행 파일을 찾을 수 없습니다.") from exc

        if process_result.timed_out:
            self._sessions[session_id] = EngineSessionStatus.FAILED
            raise EngineExecutionError(
                f"claude CLI가 {self._subprocess_timeout_seconds}초 내에 응답하지 않았습니다."
            )

        if process_result.cancelled:
            self._sessions[session_id] = EngineSessionStatus.CANCELLED
            return EngineResult(success=False, output=process_result.stdout, error="cancelled")

        result = self._parse_result(process_result)
        if self._sessions.get(session_id) != EngineSessionStatus.CANCELLED:
            self._sessions[session_id] = (
                EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
            )
        return result

    def cancel(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        if self._sessions[session_id] in _TERMINAL_STATUSES:
            return
        self._sessions[session_id] = EngineSessionStatus.CANCELLED
        try:
            self._process_runner.cancel(session_id)
        except ProcessNotFoundError:
            pass

    def status(self, session_id: str) -> EngineSessionStatus:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return frozenset({"code_generation", "claude_code"})

    def supports_parallel(self) -> bool:
        return True

    def estimate_cost(self, task: Task) -> CostEstimate:
        estimated_tokens = max(1, len(task.title) // 4)
        return CostEstimate(estimated_tokens=estimated_tokens, estimated_cost_usd=0.0)

    def _build_command(self, session_id: str, task: Task) -> list[str]:
        command = [
            "claude",
            "-p",
            task.title,
            "--output-format",
            "json",
            "--session-id",
            session_id,
            "--permission-mode",
            self._permission_mode,
        ]
        if self._model is not None:
            command.extend(["--model", self._model])
        return command

    def _parse_result(self, process_result: ProcessResult) -> EngineResult:
        data = self._parse_json(process_result.stdout)
        if data is not None:
            is_error = bool(data.get("is_error", process_result.returncode != 0))
            output = str(data.get("result", process_result.stdout))
            if is_error:
                return EngineResult(success=False, output=output, error=output)
            return EngineResult(success=True, output=output)

        if process_result.returncode == 0:
            return EngineResult(success=True, output=process_result.stdout)
        return EngineResult(
            success=False,
            output=process_result.stdout,
            error=process_result.stderr or process_result.stdout,
        )

    @staticmethod
    def _parse_json(stdout: str) -> dict[str, Any] | None:
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
