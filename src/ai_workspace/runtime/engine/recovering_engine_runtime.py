from __future__ import annotations

from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineAdapter, EngineResult, EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import EngineRuntime


class RecoveringEngineRuntime(EngineRuntime):
    """다른 `EngineRuntime`을 감싸 실행 실패 시 재시도하는 데코레이터
    (M3-T06). 이 클래스 자체는 새 상태 저장소를 두지 않는다 — `status()`/
    `cancel()`/`register_engine()`/`run_parallel()`은 모두 내부 Runtime에
    그대로 위임하며, "Runtime 상태 복원"은 별도 영속화가 아니라 재시도
    과정 내내 내부 Runtime의 상태만을 유일한 진실로 유지하는 것으로
    해석한다. `EngineResult(success=False)`(정상 실패)는 재시도 후에도
    실패하면 마지막 결과를 그대로 반환하고, 예외(비정상 종료)는 재시도
    후에도 실패하면 마지막 예외를 그대로 다시 던진다 — 기존
    `EngineRuntime.run()` 계약("EngineExecutionError가 발생하면 그대로
    전파한다")을 그대로 유지하기 위해 예외를 `EngineResult`로 감싸지
    않는다."""

    def __init__(self, *, inner: EngineRuntime, retry_policy: RetryPolicy) -> None:
        self._inner = inner
        self._retry_policy = retry_policy

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        self._inner.register_engine(name, adapter)

    def run(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> EngineResult:
        last_exception: BaseException | None = None
        last_result: EngineResult | None = None
        for _ in range(self._retry_policy.max_attempts):
            try:
                last_result = self._inner.run(task, required_capabilities)
            except BaseException as exc:
                last_exception = exc
                last_result = None
                continue
            last_exception = None
            if last_result.success:
                return last_result
        if last_exception is not None:
            raise last_exception
        assert last_result is not None
        return last_result

    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        return self._inner.run_parallel(tasks, required_capabilities)

    def cancel(self, task_id: str) -> None:
        self._inner.cancel(task_id)

    def status(self, task_id: str) -> EngineSessionStatus:
        return self._inner.status(task_id)
