from __future__ import annotations

from ai_workspace.domain.retry_policy import RetryPolicy
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineAdapter, EngineResult, EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import EngineRuntime


class RecoveringEngineRuntime(EngineRuntime):
    """다른 `EngineRuntime`을 감싸 실행 실패 시 재시도하는 데코레이터
    (M3-T06). 이 클래스 자체는 새 상태 저장소를 두지 않는다 — `status()`/
    `cancel()`/`register_engine()`은 내부 Runtime에 그대로 위임하며,
    "Runtime 상태 복원"은 별도 영속화가 아니라 재시도 과정 내내 내부
    Runtime의 상태만을 유일한 진실로 유지하는 것으로 해석한다.
    `EngineResult(success=False)`(정상 실패)는 재시도 후에도 실패하면
    마지막 결과를 그대로 반환하고, 예외(비정상 종료)는 재시도 후에도
    실패하면 마지막 예외를 그대로 다시 던진다 — 기존 `EngineRuntime.run()`
    계약("EngineExecutionError가 발생하면 그대로 전파한다")을 그대로
    유지하기 위해 예외를 `EngineResult`로 감싸지 않는다.

    **`run_parallel()`의 개별 Task 재시도(M10-T03)**: 이전에는 내부
    Runtime에 그대로 위임해 병렬 배치 안의 개별 Task 실패에 재시도가
    전혀 적용되지 않았다(알려진 범위로 M4-T06/ADR-0023에서 기록됨).
    이제는 먼저 내부 Runtime의 `run_parallel()`(M10-T01/T02로 개별 Task
    실패를 EngineResult(success=False)로 격리)을 한 번 병렬 실행한 뒤,
    실패한 Task만 골라 기존 `self.run()`의 재시도 루프로 다시 실행한다
    (새 재시도 로직을 만들지 않고 기존 것을 재사용, YAGNI). 재시도
    대상이 여럿이면 이 단계는 순차 처리다 — 실패가 예외적 상황이라는
    전제이며, 재병렬화는 필요성이 증명되면 별도로 검토한다. `self.run()`
    이 재시도 소진 후 예외를 던지는 경우(위 문단 참고)는 그 Task만
    EngineResult(success=False)로 변환해 다른 Task의 결과에 영향을 주지
    않는다 — 단일 `run()`은 호출자에게 직접 예외를 전파해도 되지만,
    `run_parallel()`은 배치 전체를 보호해야 하므로 의도적으로 다르게
    처리한다."""

    def __init__(self, *, inner: EngineRuntime, retry_policy: RetryPolicy) -> None:
        self._inner = inner
        self._retry_policy = retry_policy

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        self._inner.register_engine(name, adapter)

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
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
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> list[EngineResult]:
        first_pass = self._inner.run_parallel(tasks, required_capabilities)
        final: list[EngineResult] = []
        for task, result in zip(tasks, first_pass):
            if result.success:
                final.append(result)
                continue
            try:
                final.append(self.run(task, required_capabilities))
            except BaseException as exc:
                final.append(EngineResult(success=False, output="", error=str(exc)))
        return final

    def cancel(self, task_id: str) -> None:
        self._inner.cancel(task_id)

    def status(self, task_id: str) -> EngineSessionStatus:
        return self._inner.status(task_id)
