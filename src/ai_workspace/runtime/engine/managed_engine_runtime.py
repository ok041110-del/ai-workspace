from __future__ import annotations

import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

from ai_workspace.domain.engine_selection import EngineCandidate
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
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
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy
from ai_workspace.interfaces.event_bus import Event, EventBus

_DEFAULT_TIMEOUT_SECONDS = 30.0


class ManagedEngineRuntime(EngineRuntime):
    """EngineAdapter의 Task 실행을 생명주기(Running/Completed/Failed/
    Cancelled) 관리·Timeout·Event 발행과 함께 운영하는 프로덕션 Engine
    Runtime(ARCHITECTURE.md §3.9, ADR-0016, M3-T01/M6-T01). 여러 개의
    EngineAdapter를 이름별로 등록할 수 있으며(M6-T01), `run()`/
    `run_parallel()`은 `required_capabilities`를 만족하는 등록된 어댑터 중
    하나를 선택해 실행한다(등록 순서상 첫 매칭 — 복수 매칭 시 우선순위
    정책은 필요성이 증명되지 않아 도입하지 않음, YAGNI). 이 선택 방식은
    `tests/interfaces/fakes.py`의 `FakeEngineRuntime`이 이미 계약 검증용으로
    구현해 둔 것과 동일하다.

    기존 `EngineAdapter`/`EngineRuntime` 계약은 동기(synchronous)이므로,
    Timeout은 `adapter.run()` 호출을 별도 스레드에서 실행하고
    `Thread.join(timeout)`으로 감시하는 최소 구조로 구현한다. Python은
    실행 중인 스레드를 강제 종료할 수 없으므로, 시간 초과 시 이 Runtime은
    실패로 처리하고 `adapter.cancel()`을 호출해 어댑터에 취소를
    알릴 뿐이다(진짜 실행 엔진이 이를 어떻게 받아들일지는 M3-T02 이후
    실제 Adapter 구현에 달려 있다 — 지금은 구조만 제공한다).

    `run_parallel()`은 `ThreadPoolExecutor`로 각 Task의 `run()`을 실제로
    동시에 실행한다(ADR-0023, M4-T06 — 이전에는 순차 반복 호출이었음).
    반환 목록은 `EngineRuntime.run_parallel()` 계약대로 입력 순서·길이를
    보장한다.

    **개별 Task 실패 격리(M10-T02)**: `required_capabilities`를 만족하는
    엔진이 아예 없으면(Runtime 자체의 치명적 오류) 어떤 Task도 제출하기
    전에 `NoSuitableEngineError`가 즉시 전파된다. 반면 제출된 개별
    Task의 실행이 예외를 던지면(예: `EngineExecutionError`) 그 Task의
    `future.result()`만 개별적으로 캐치해 `EngineResult(success=False)`로
    변환한다 — 이전에는 `[future.result() for future in futures]` 리스트
    컴프리헨션이 첫 예외에서 즉시 전파되어 이미 완료된 다른 Task의 결과까지
    전부 유실됐다(M10 이전 버그, `.ai/TASKS.md` M10-T02 참고). `with` 블록이
    끝날 때 `ThreadPoolExecutor.shutdown(wait=True)`가 호출되므로, 예외
    캐치 시점에는 제출된 모든 Task가 이미 완료된 상태임이 보장된다.

    `engine_selection_policy`(Milestone 64, ADR-0082)를 생성자로 주입하면
    `_require_adapter()`가 "등록 순서상 첫 매칭" 대신 `EngineSelectionPolicy`
    (M17)로 비용 기반 선택을 한다 — 이미 Automation 파이프라인이 쓰는 것과
    같은 선택 규칙을 이 경로에도 적용한다. 생략(기본값 `None`)하면 이전
    동작과 100% 동일하다.
    """

    def __init__(
        self,
        *,
        event_bus: EventBus,
        default_timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS,
        engine_selection_policy: EngineSelectionPolicy | None = None,
        budget_policy_engine: BudgetPolicyEngine | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._default_timeout_seconds = default_timeout_seconds
        self._engines: dict[str, EngineAdapter] = {}
        self._task_status: dict[str, EngineSessionStatus] = {}
        self._task_sessions: dict[str, str] = {}
        self._task_adapters: dict[str, EngineAdapter] = {}
        self._engine_selection_policy = engine_selection_policy
        self._budget_policy_engine = budget_policy_engine

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        if name in self._engines:
            raise DuplicateEngineError(name)
        self._engines[name] = adapter

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        timeout_seconds: float | None = None,
        *,
        model: str | None = None,
    ) -> EngineResult:
        adapter = self._require_adapter(required_capabilities, task)
        session_id = adapter.create_session()
        self._task_sessions[task.task_id] = session_id
        self._task_adapters[task.task_id] = adapter
        self._task_status[task.task_id] = EngineSessionStatus.RUNNING
        self._publish("engine_task_started", task.task_id, session_id)

        result_box: dict[str, EngineResult] = {}
        error_box: dict[str, BaseException] = {}

        def _execute() -> None:
            try:
                result_box["result"] = adapter.run(session_id, task, model=model)
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
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> list[EngineResult]:
        if not tasks:
            return []
        self._require_adapter(required_capabilities, tasks[0])
        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            futures = [
                executor.submit(self.run, task, required_capabilities, model=model)
                for task in tasks
            ]
            results: list[EngineResult] = []
            for future in futures:
                try:
                    results.append(future.result())
                except BaseException as exc:
                    results.append(EngineResult(success=False, output="", error=str(exc)))
            return results

    def run_ensemble(
        self,
        task: Task,
        engine_names: list[str],
        *,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        """등록된 이름별 어댑터에 `run_parallel()`과 같은 `ThreadPoolExecutor`
        메커니즘으로 동시에 같은 Task를 돌린다. `run()`/`_task_status` 등
        task_id 단위 상태 추적은 여기서 쓰지 않는다 — 같은 task.task_id가
        여러 엔진에서 동시에 실행되면 그 상태 저장소(1개 task_id당 1개
        상태만 갖는 구조)와 의미가 충돌하기 때문에, status()/cancel()
        연동 없이 세션 생성→실행→정리만 독립적으로 수행한다."""
        if not engine_names:
            return {}
        with ThreadPoolExecutor(max_workers=len(engine_names)) as executor:
            futures = {
                name: executor.submit(self._run_named, name, task, model)
                for name in engine_names
            }
            return {name: future.result() for name, future in futures.items()}

    def _run_named(self, name: str, task: Task, model: str | None) -> EngineResult:
        adapter = self._engines.get(name)
        if adapter is None:
            return EngineResult(success=False, output="", error=f"engine '{name}' not registered")
        try:
            session_id = adapter.create_session()
            result = adapter.run(session_id, task, model=model)
            adapter.destroy_session(session_id)
            return result
        except BaseException as exc:
            return EngineResult(success=False, output="", error=str(exc))

    def estimate_cost(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> CostEstimate:
        adapter = self._require_adapter(required_capabilities, task)
        return adapter.estimate_cost(task)

    def cancel(self, task_id: str) -> None:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        self._task_status[task_id] = EngineSessionStatus.CANCELLED
        session_id = self._task_sessions.get(task_id)
        adapter = self._task_adapters.get(task_id)
        if session_id is not None and adapter is not None:
            try:
                adapter.cancel(session_id)
            except SessionNotFoundError:
                pass

    def status(self, task_id: str) -> EngineSessionStatus:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        return self._task_status[task_id]

    def _require_adapter(self, required_capabilities: frozenset[str], task: Task) -> EngineAdapter:
        if self._engine_selection_policy is None:
            for adapter in self._engines.values():
                if required_capabilities.issubset(adapter.capabilities()):
                    return adapter
            raise NoSuitableEngineError(required_capabilities)

        candidates: list[EngineCandidate] = []
        for name, adapter in self._engines.items():
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            estimate = adapter.estimate_cost(task)
            candidates.append(
                EngineCandidate(
                    engine_name=name,
                    capabilities=adapter.capabilities(),
                    estimated_tokens=estimate.estimated_tokens,
                    estimated_cost_usd=estimate.estimated_cost_usd,
                    supports_parallel=adapter.supports_parallel(),
                )
            )
        decision = self._engine_selection_policy.select(
            task, candidates, budget_policy_engine=self._budget_policy_engine
        )
        if decision is None:
            raise NoSuitableEngineError(required_capabilities)
        return self._engines[decision.engine_name]

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
