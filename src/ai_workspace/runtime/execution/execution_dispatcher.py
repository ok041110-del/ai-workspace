from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime

from ai_workspace.domain.engine_selection import EngineSelectionDecision
from ai_workspace.domain.execution_result import EngineExecutionResult
from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.authentication_manager import (
    AuthenticationManager,
    AuthenticationRequiredError,
)
from ai_workspace.interfaces.engine_adapter import EngineExecutionError, EngineResult
from ai_workspace.interfaces.engine_registry import EngineNotRegisteredError, EngineRegistry
from ai_workspace.interfaces.engine_runtime import NoSuitableEngineError
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)
from ai_workspace.runtime.execution.retry_executor import RetryExecutor

_DEFAULT_NON_RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
    AuthenticationRequiredError,
    EngineNotRegisteredError,
    NoSuitableEngineError,
)

# M19 기술 부채(ADR-0031): ClaudeCodeEngineAdapter.run()은 Timeout과 다른 실행
# 오류를 모두 같은 EngineExecutionError로 던지고, 메시지 텍스트로만 구분된다.
# EngineAdapter 인터페이스를 이번 Milestone에서 바꾸지 않기로 했기 때문에
# 완전한 구분은 불가능하다 — 이 마커 문자열 매칭은 알려진 한계가 있는 휴리스틱이다.
_TIMEOUT_MESSAGE_MARKER = "응답하지 않았습니다"


def _looks_like_timeout(exception: BaseException) -> bool:
    return _TIMEOUT_MESSAGE_MARKER in str(exception)


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
    `EngineAdapter.run()`만 호출한다.

    **Reliability는 `RetryExecutor`에 위임한다(M19)**: 이 클래스는
    재시도 로직을 직접 구현하지 않는다 — 인증 확인→Registry 조회→
    Adapter 실행 전체를 한 번의 시도로 묶어 `RetryExecutor`에 넘긴다.
    `AuthenticationRequiredError`/`EngineNotRegisteredError`/
    `NoSuitableEngineError`는 기본적으로 재시도하지 않도록 구성된
    `RetryPolicy`를 쓴다(재정의하려면 `retry_policy`를 주입한다).
    취소는 `EngineAdapter`가 이미 쓰는 sentinel(`EngineResult.error
    == "cancelled"`)을 그대로 이어받아 판정한다 — 새 문자열 규칙을
    만들지 않는다.

    **Dashboard를 위한 Event 발행(M20)**: `event_bus`를 선택적으로
    주입하면 실행 시작/완료/인증 실패 시점에
    `runtime/execution/events.py`의 Event를 발행한다. 이 클래스는
    누가 구독하는지 전혀 알지 못한다 — `DashboardRepository`(M20)를
    직접 참조하지 않는다(Event만 발행, CQRS). 미주입 시(기본값
    `None`) Event 발행 자체를 건너뛰어 M19 이전과 완전히 동일하게
    동작한다."""

    def __init__(
        self,
        *,
        engine_registry: EngineRegistry,
        authentication_manager: AuthenticationManager,
        retry_policy: RetryPolicy | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self._engine_registry = engine_registry
        self._authentication_manager = authentication_manager
        self._retry_policy = (
            retry_policy
            if retry_policy is not None
            else RetryPolicy(non_retryable_exceptions=_DEFAULT_NON_RETRYABLE_EXCEPTIONS)
        )
        self._retry_executor = RetryExecutor(retry_policy=self._retry_policy)
        self._event_bus = event_bus

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

        self._publish(
            ENGINE_EXECUTION_STARTED,
            {
                "engine": decision.engine_name,
                "task_title": task.title,
                "started_at": _now_iso(),
            },
        )

        attempts = 0

        def attempt() -> EngineResult:
            nonlocal attempts
            attempts += 1
            if not self._authentication_manager.is_authenticated(decision.engine_name):
                raise AuthenticationRequiredError(decision.engine_name)
            adapter = self._engine_registry.get(decision.engine_name)
            session_id = adapter.create_session()
            try:
                return adapter.run(session_id, task, model=decision.model)
            finally:
                adapter.destroy_session(session_id)

        start = time.monotonic()
        try:
            result = self._retry_executor.execute(attempt)
        except AuthenticationRequiredError:
            self._publish(
                ENGINE_AUTHENTICATION_FAILED, {"engine": decision.engine_name}
            )
            raise
        except EngineExecutionError as exc:
            execution_time = time.monotonic() - start
            engine_result = EngineExecutionResult(
                success=False,
                output="",
                error=str(exc),
                engine=decision.engine_name,
                execution_time=execution_time,
                retry_count=attempts - 1,
                timed_out=_looks_like_timeout(exc),
            )
            self._publish_completed(engine_result)
            return engine_result
        execution_time = time.monotonic() - start

        engine_result = EngineExecutionResult(
            success=result.success,
            output=result.output,
            error=result.error,
            engine=decision.engine_name,
            execution_time=execution_time,
            retry_count=attempts - 1,
            cancelled=(result.error == "cancelled"),
        )
        self._publish_completed(engine_result)
        return engine_result

    def _publish_completed(self, result: EngineExecutionResult) -> None:
        self._publish(
            ENGINE_EXECUTION_COMPLETED,
            {
                "engine": result.engine,
                "success": result.success,
                "cancelled": result.cancelled,
                "timed_out": result.timed_out,
                "retry_count": result.retry_count,
                "error": result.error,
                "completed_at": _now_iso(),
            },
        )

    def _publish(self, event_type: str, payload: dict[str, object]) -> None:
        if self._event_bus is None:
            return
        self._event_bus.publish(
            Event(event_id=str(uuid.uuid4()), event_type=event_type, payload=payload)
        )


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()
