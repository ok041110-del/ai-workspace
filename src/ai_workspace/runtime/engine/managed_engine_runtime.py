from __future__ import annotations

import threading
import uuid

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    EngineAdapter,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineRuntime,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)
from ai_workspace.interfaces.event_bus import Event, EventBus

_DEFAULT_TIMEOUT_SECONDS = 30.0


class ManagedEngineRuntime(EngineRuntime):
    """단일 EngineAdapter의 Task 실행을 생명주기(Running/Completed/Failed/
    Cancelled) 관리·Timeout·Event 발행과 함께 운영하는 프로덕션 Engine
    Runtime(ARCHITECTURE.md §3.9, ADR-0016, M3-T01). 여러 엔진 등록·
    Capability 기반 선택(Engine Registry, T2-05의 `InMemoryEngineRuntime`이
    이미 담당)은 범위 밖이며, 이 구현은 정확히 하나의 EngineAdapter만
    등록할 수 있다.

    기존 `EngineAdapter`/`EngineRuntime` 계약은 동기(synchronous)이므로,
    Timeout은 `adapter.run()` 호출을 별도 스레드에서 실행하고
    `Thread.join(timeout)`으로 감시하는 최소 구조로 구현한다. Python은
    실행 중인 스레드를 강제 종료할 수 없으므로, 시간 초과 시 이 Runtime은
    실패로 처리하고 `adapter.cancel()`을 호출해 어댑터에 취소를
    알릴 뿐이다(진짜 실행 엔진이 이를 어떻게 받아들일지는 M3-T02 이후
    실제 Adapter 구현에 달려 있다 — 지금은 구조만 제공한다).
    """

    def __init__(
        self, *, event_bus: EventBus, default_timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS
    ) -> None:
        self._event_bus = event_bus
        self._default_timeout_seconds = default_timeout_seconds
        self._adapter: EngineAdapter | None = None
        self._task_status: dict[str, EngineSessionStatus] = {}
        self._task_sessions: dict[str, str] = {}

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        if self._adapter is not None:
            raise DuplicateEngineError(name)
        self._adapter = adapter

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        timeout_seconds: float | None = None,
    ) -> EngineResult:
        adapter = self._require_adapter(required_capabilities)
        session_id = adapter.create_session()
        self._task_sessions[task.task_id] = session_id
        self._task_status[task.task_id] = EngineSessionStatus.RUNNING
        self._publish("engine_task_started", task.task_id, session_id)

        result_box: dict[str, EngineResult] = {}
        error_box: dict[str, BaseException] = {}

        def _execute() -> None:
            try:
                result_box["result"] = adapter.run(session_id, task)
            except BaseException as exc:
                error_box["error"] = exc

        thread = threading.Thread(target=_execute, daemon=True)
        thread.start()
        effective_timeout = (
            timeout_seconds if timeout_seconds is not None else self._default_timeout_seconds
        )
        thread.join(effective_timeout)

        if thread.is_alive():
            return self._finish_as_timeout(task.task_id, session_id, adapter)

        if "error" in error_box:
            adapter.destroy_session(session_id)
            self._task_status[task.task_id] = EngineSessionStatus.FAILED
            raise error_box["error"]

        return self._finish_as_completed(task.task_id, session_id, adapter, result_box["result"])

    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        return [self.run(task, required_capabilities) for task in tasks]

    def cancel(self, task_id: str) -> None:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        self._task_status[task_id] = EngineSessionStatus.CANCELLED
        session_id = self._task_sessions.get(task_id)
        if session_id is not None and self._adapter is not None:
            try:
                self._adapter.cancel(session_id)
            except SessionNotFoundError:
                pass

    def status(self, task_id: str) -> EngineSessionStatus:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        return self._task_status[task_id]

    def _require_adapter(self, required_capabilities: frozenset[str]) -> EngineAdapter:
        if self._adapter is None or not required_capabilities.issubset(
            self._adapter.capabilities()
        ):
            raise NoSuitableEngineError(required_capabilities)
        return self._adapter

    def _finish_as_completed(
        self, task_id: str, session_id: str, adapter: EngineAdapter, result: EngineResult
    ) -> EngineResult:
        adapter.destroy_session(session_id)
        if self._task_status.get(task_id) == EngineSessionStatus.CANCELLED:
            self._publish("engine_task_cancelled", task_id, session_id)
            return EngineResult(success=False, output=result.output, error="cancelled")
        self._task_status[task_id] = (
            EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
        )
        self._publish(
            "engine_task_completed" if result.success else "engine_task_failed", task_id, session_id
        )
        return result

    def _finish_as_timeout(
        self, task_id: str, session_id: str, adapter: EngineAdapter
    ) -> EngineResult:
        self._task_status[task_id] = EngineSessionStatus.FAILED
        try:
            adapter.cancel(session_id)
        except SessionNotFoundError:
            pass
        self._publish("engine_task_timeout", task_id, session_id)
        return EngineResult(success=False, output="", error="timeout")

    def _publish(self, event_type: str, task_id: str, session_id: str) -> None:
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                payload={"task_id": task_id, "session_id": session_id},
            )
        )
