from __future__ import annotations

import uuid

from ai_workspace.adapters.cli_provider import CLIProvider
from ai_workspace.adapters.local_execution_environment import LocalExecutionEnvironment
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)
from ai_workspace.interfaces.execution_environment import (
    ExecutionEnvironment,
    ExecutionNotFoundError,
)

_DEFAULT_SUBPROCESS_TIMEOUT_SECONDS = 600.0
_TERMINAL_STATUSES = frozenset({EngineSessionStatus.COMPLETED, EngineSessionStatus.FAILED})


class CLIEngineAdapter(EngineAdapter):
    """`CLIProvider`(Codex/Gemini CLI 등)를 감싸 `EngineAdapter` 계약을
    만족시키는 범용 어댑터(M5-T05). 명령 조립·결과 파싱만 Provider에
    위임하고, 세션 생명주기·프로세스 실행·Timeout·Cancel 처리는
    `ClaudeCodeEngineAdapter`(M3-T02/T03)와 동일한 검증된 로직을
    그대로 따른다.

    **`ClaudeCodeEngineAdapter`는 이 프레임워크로 아직 옮기지 않았다**
    (사용자 지시 — 기존 안정성 유지, 두 어댑터 사이에 일부 중복 로직이
    존재함을 의도적으로 감수함). 충분히 검증된 뒤 M6+에서 통합을
    재검토한다. 실제 명령을 어디서 실행할지는 `ExecutionEnvironment`
    (Milestone 11)에 위임하며, 이 Adapter는 구체 구현체를 직접 생성하지
    않고 생성자로 주입받는다(Dependency Injection)."""

    def __init__(
        self,
        *,
        provider: CLIProvider,
        cwd: str | None = None,
        subprocess_timeout_seconds: float = _DEFAULT_SUBPROCESS_TIMEOUT_SECONDS,
        execution_environment: ExecutionEnvironment | None = None,
    ) -> None:
        self._provider = provider
        self._cwd = cwd
        self._subprocess_timeout_seconds = subprocess_timeout_seconds
        self._execution_environment = (
            execution_environment
            if execution_environment is not None
            else LocalExecutionEnvironment()
        )
        self._sessions: dict[str, EngineSessionStatus] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)

        command = self._provider.build_command(session_id, task)
        try:
            execution_result = self._execution_environment.execute(
                session_id, command, cwd=self._cwd, timeout=self._subprocess_timeout_seconds
            )
        except FileNotFoundError as exc:
            self._sessions[session_id] = EngineSessionStatus.FAILED
            raise EngineExecutionError(
                f"{command[0]} 실행 파일을 찾을 수 없습니다."
            ) from exc

        if execution_result.timed_out:
            self._sessions[session_id] = EngineSessionStatus.FAILED
            raise EngineExecutionError(
                f"{command[0]}가 {self._subprocess_timeout_seconds}초 내에 응답하지 않았습니다."
            )

        if execution_result.cancelled:
            self._sessions[session_id] = EngineSessionStatus.CANCELLED
            return EngineResult(success=False, output=execution_result.stdout, error="cancelled")

        result = self._provider.parse_result(execution_result)
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
            self._execution_environment.cancel(session_id)
        except ExecutionNotFoundError:
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
        return self._provider.capabilities()

    def supports_parallel(self) -> bool:
        return self._provider.supports_parallel()

    def estimate_cost(self, task: Task) -> CostEstimate:
        estimated_tokens = max(1, len(task.title) // 4)
        return CostEstimate(estimated_tokens=estimated_tokens, estimated_cost_usd=0.0)
