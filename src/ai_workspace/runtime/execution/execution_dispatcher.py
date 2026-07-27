from __future__ import annotations

import time

from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.execution_result import EngineExecutionResult
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.authentication_manager import (
    AuthenticationManager,
    AuthenticationRequiredError,
)
from ai_workspace.interfaces.engine_registry import EngineRegistry


class ExecutionDispatcher:
    """M17의 `EngineSelectionDecision`을 실제 실행으로 연결하는 구체
    클래스(M18, Interface가 아니다 — `WorkflowRunner`와 동일한 패턴,
    사용자 승인). `EngineRegistry`/`EngineAdapter`/`AuthenticationManager`
    Interface만 사용해 특정 Provider를 직접 분기하지 않는다(OCP —
    새 Engine을 추가해도 이 클래스는 수정하지 않는다).

    **Decision과 Execution의 완전한 분리**: 이 클래스는
    `EngineSelectionPolicy`를 전혀 참조하지 않는다 — 이미 계산된
    `EngineSelectionDecision`만 입력으로 받는다.

    **Authentication은 상태 확인만 담당**: 실제 로그인을 수행하지
    않는다. 인증되어 있지 않으면 `AuthenticationRequiredError`를
    던진다 — Workspace가 CLI 로그인 명령을 대신 실행하지 않는다.

    **`ExecutionEnvironment`는 직접 다루지 않는다**: `EngineAdapter`
    (예: `ClaudeCodeEngineAdapter`)가 이미 생성자 주입으로
    `ExecutionEnvironment`를 갖고 있으므로(M11), 이 클래스는
    `EngineAdapter.run()`만 호출한다."""

    def __init__(
        self, *, engine_registry: EngineRegistry, authentication_manager: AuthenticationManager
    ) -> None:
        self._engine_registry = engine_registry
        self._authentication_manager = authentication_manager

    def dispatch(
        self, decision: EngineSelectionDecision | None, task: Task
    ) -> EngineExecutionResult:
        if decision is None:
            return EngineExecutionResult(
                success=False,
                output="",
                error="no selection decision",
                engine=None,
                execution_time=0.0,
            )

        if not self._authentication_manager.is_authenticated(decision.engine_name):
            raise AuthenticationRequiredError(decision.engine_name)

        adapter = self._engine_registry.get(decision.engine_name)
        start = time.monotonic()
        session_id = adapter.create_session()
        try:
            result = adapter.run(session_id, task, model=decision.model)
        finally:
            adapter.destroy_session(session_id)
        execution_time = time.monotonic() - start

        return EngineExecutionResult(
            success=result.success,
            output=result.output,
            error=result.error,
            engine=decision.engine_name,
            execution_time=execution_time,
        )
