from __future__ import annotations

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineResult,
    EngineSessionStatus,
)
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineRuntime,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)


class InMemoryEngineRuntime(EngineRuntime):
    """엔진 선택·세션 풀 관리·병렬 실행을 담당하는 최소 구현체
    (ARCHITECTURE.md §3.9, ADR-0016, T2-05). 세션(create_session/
    destroy_session)은 이 안에서만 관리되며 호출자에게 노출되지 않는다."""

    def __init__(self) -> None:
        self._engines: dict[str, EngineAdapter] = {}
        self._task_status: dict[str, EngineSessionStatus] = {}

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        if name in self._engines:
            raise DuplicateEngineError(name)
        self._engines[name] = adapter

    def _select(
        self, required_capabilities: frozenset[str], require_parallel: bool = False
    ) -> EngineAdapter:
        for adapter in self._engines.values():
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            if require_parallel and not adapter.supports_parallel():
                continue
            return adapter
        raise NoSuitableEngineError(required_capabilities)

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> EngineResult:
        adapter = self._select(required_capabilities)
        session_id = adapter.create_session()
        result = adapter.run(session_id, task, model=model)
        adapter.destroy_session(session_id)
        self._task_status[task.task_id] = (
            EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
        )
        return result

    def run_parallel(
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> list[EngineResult]:
        adapter = self._select(required_capabilities, require_parallel=True)
        results: list[EngineResult] = []
        for task in tasks:
            session_id = adapter.create_session()
            result = adapter.run(session_id, task, model=model)
            adapter.destroy_session(session_id)
            self._task_status[task.task_id] = (
                EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
            )
            results.append(result)
        return results

    def estimate_cost(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> CostEstimate:
        adapter = self._select(required_capabilities)
        return adapter.estimate_cost(task)

    def cancel(self, task_id: str) -> None:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        self._task_status[task_id] = EngineSessionStatus.CANCELLED

    def status(self, task_id: str) -> EngineSessionStatus:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        return self._task_status[task_id]
