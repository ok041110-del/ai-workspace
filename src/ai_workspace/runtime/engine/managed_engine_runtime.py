from __future__ import annotations

import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from ai_workspace.domain.consensus_agreement import ConsensusAgreementStat
from ai_workspace.domain.engine_execution_memory import EngineExecutionMemoryStat
from ai_workspace.domain.engine_reliability import EngineReliabilityStat
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
_NEUTRAL_RATE = 0.5


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

    **엔진별 신뢰도 추적 + 적응형 라우팅(Milestone 65, ADR-0083)**: `run()`
    (Cancel된 경우는 제외)/`_finish_as_timeout()`/`run_ensemble()`이 실제로
    실행한 엔진의 성공/실패를 이름별로 in-process 누적한다
    (`EngineReliabilityStat`). 비용 기반 선택 경로(`engine_selection_policy`
    주입 시)에서만 이 기록을 활용해 `is_unreliable()`(M49와 동일한 "성공
    0건 + 표본 3건 이상" 규칙)에 해당하는 엔진을 후보에서 제외한다.

    **제외 엔진 자동 복구(Milestone 66, ADR-0084)**: `_require_adapter()`가
    제외된 엔진을 `_PROBE_INTERVAL`번 연속으로 건너뛰면 다음 선택에서 한
    번 더 후보로 포함해(probe) 복구 여부를 다시 확인한다 — `EngineRuntime`과
    동일한 규칙(`EngineReliabilityStat.is_probe_eligible()`)이다.

    **Dynamic Ensemble Routing(Milestone 68, ADR-0086)**: `run_ensemble()`
    (M62)은 `engine_names`를 호출자가 직접 나열해야 했다. `run_ensemble_auto()`
    는 `_require_adapter()`에서 쓰던 후보 선정 로직을 `_build_candidates()`로
    분리해 재사용하고, `EngineSelectionPolicy.select()`를 반복 호출해(매번
    이미 선택된 후보를 제외) 상위 `top_n`개 엔진을 동적으로 고른 뒤 기존
    `run_ensemble()`에 그대로 위임한다 — 새 병렬 실행 로직을 만들지
    않는다(YAGNI).

    **Execution Memory & Context Routing(Milestone 69, ADR-0087)**: `run()`
    (Cancel된 경우는 제외)/`run_ensemble_auto()`가 실제로 실행한 결과를
    `(required_capabilities, engine_name)` 조합 키로 `EngineExecutionMemoryStat`
    에 누적한다(성공/실패/latency). `_build_candidates()`가 (기존 신뢰도
    제외 이후) 이 기록을 확인해, 같은 `required_capabilities` 조합에서
    표본이 충분한 엔진을 성공률 내림차순으로 재정렬한다 —
    `EngineSelectionPolicy`의 비용 기준 `min()`은 비용이 다르면 항상 진짜
    최저 비용을 고르므로, 이 재정렬은 **비용이 동률인 후보끼리의
    tie-break**로만 작동한다(표본 부족 시 기본값 순서 그대로, 100% 하위
    호환). M65/M66의 "복구 즉시 완전 신뢰" 판정과 충돌하지 않도록
    의도적으로 이렇게 범위를 좁혔다. 신뢰도 제외와 동일하게
    `engine_selection_policy` 주입 경로에서만 적용된다.

    **Adaptive Consensus(Milestone 70, ADR-0088)**: `run_ensemble()`(M62)
    결과를 `ResultAggregator`(M63)로 다수결한 뒤, 호출자(주로
    `AdaptiveConsensusAggregator`)가 `record_consensus_outcome()`으로 어떤
    엔진의 투표가 합의와 일치했는지 알려주면 `(required_capabilities,
    engine_name)` 키로 `ConsensusAgreementStat`에 누적한다.
    `consensus_weight()`는 이 기록을 조회하는 read-only 메서드다 —
    `EngineRuntime`은 `ResultAggregator`를 호출하거나 알지 못하며, 이
    두 메서드로만 연결된다(YAGNI, 기존 ADR-0080/0081의 결합 방지 원칙
    유지).

    **Provider Concurrency Management(Milestone 74, ADR-0092)**:
    `register_engine()`에 `max_concurrency`를 지정한 엔진은 동시에 실행
    중인 세션 수(`run()`이 세션을 만든 시점부터 완료/실패/타임아웃으로
    정리될 때까지 — `ThreadPoolExecutor`로 실제 동시 실행되는
    `run_parallel()`도 각 Task가 내부적으로 `run()`을 호출하므로 그대로
    적용된다)를 in-process로 카운트한다. 한도에 도달한 엔진은 후보에서
    제외되어 다른 후보로 자동 fallback하고, 후보 전체가 busy면 기존과
    동일하게 `NoSuitableEngineError`를 던진다. `run_ensemble()`/
    `run_ensemble_auto()`는 `InMemoryEngineRuntime`과 동일한 이유(M62/M68)
    로 이 범위에서 제외했다(YAGNI). `max_concurrency`를 지정하지 않으면
    이전 동작과 100% 동일하다.

    **Diversity Routing(Milestone 75, ADR-0093)**: `_build_candidates()`가
    M74 capacity 필터링 이후, `_reorder_by_execution_memory()`보다 먼저
    `_reorder_by_diversity()`(안정 정렬)를 적용해 비용·성공률이 완전
    동률인 후보끼리는 지금 이 순간의 부하가 더 적은 엔진을 우선한다.
    `InMemoryEngineRuntime`과 동일한 설계(순수 tie-break, 새 상태 없음,
    `engine_selection_policy` 미주입 시 관여하지 않음).

    **Adaptive Load Balancing(Milestone 76, ADR-0094)**: `_reorder_by_
    diversity()`의 부하 신호를 절대 `_in_flight` 개수에서 `_load_ratio()`
    (= `_in_flight / max_concurrency`, 무제한 엔진은 0.0)로 개선했다 —
    `InMemoryEngineRuntime._load_ratio()`와 완전히 동일한 설계이며, M74
    상태만 읽는 read-only 계산이라 새 상태를 만들지 않는다."""

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
        self._engine_reliability: dict[str, EngineReliabilityStat] = {}
        self._execution_memory: dict[tuple[frozenset[str], str], EngineExecutionMemoryStat] = {}
        self._consensus_agreement: dict[tuple[frozenset[str], str], ConsensusAgreementStat] = {}
        self._max_concurrency: dict[str, int] = {}
        self._in_flight: dict[str, int] = {}
        self._concurrency_lock = threading.Lock()

    def register_engine(
        self, name: str, adapter: EngineAdapter, *, max_concurrency: int | None = None
    ) -> None:
        if name in self._engines:
            raise DuplicateEngineError(name)
        self._engines[name] = adapter
        if max_concurrency is not None:
            self._max_concurrency[name] = max_concurrency

    def _has_capacity(self, name: str) -> bool:
        limit = self._max_concurrency.get(name)
        if limit is None:
            return True
        return self._in_flight.get(name, 0) < limit

    def _try_acquire(self, name: str) -> bool:
        with self._concurrency_lock:
            limit = self._max_concurrency.get(name)
            current = self._in_flight.get(name, 0)
            if limit is not None and current >= limit:
                return False
            self._in_flight[name] = current + 1
            return True

    def _release(self, name: str) -> None:
        with self._concurrency_lock:
            self._in_flight[name] = max(0, self._in_flight.get(name, 0) - 1)

    def _record_engine_outcome(self, name: str, success: bool) -> None:
        stat = self._engine_reliability.get(name, EngineReliabilityStat())
        self._engine_reliability[name] = stat.record(success)

    def _record_execution_memory(
        self,
        required_capabilities: frozenset[str],
        name: str,
        success: bool,
        latency_seconds: float,
    ) -> None:
        key = (required_capabilities, name)
        stat = self._execution_memory.get(key, EngineExecutionMemoryStat())
        self._execution_memory[key] = stat.record(success, latency_seconds)

    def _reorder_by_execution_memory(
        self, candidates: list[EngineCandidate], required_capabilities: frozenset[str]
    ) -> list[EngineCandidate]:
        """비용이 동일한 후보끼리는(`EngineSelectionPolicy`의 `min()`이
        동률일 때 반환하는 첫 원소를 이 순서로 결정) 같은 `required_
        capabilities` 조합에서 성공률이 더 높았던 엔진을 앞세운다. 비용이
        다르면 `min()`이 항상 진짜 최저 비용을 고르므로 순서는 결과에
        영향을 주지 않는다 — M65/M66의 신뢰도 판정(`is_unreliable()`)이
        이미 "복구 즉시 완전 신뢰"를 보장하는 것과 배치되지 않도록,
        의도적으로 비용 동률 상황의 tie-break로만 범위를 좁혔다.

        표본 부족으로 아직 성공률을 모르는 엔진은 `_NEUTRAL_RATE`(0.5)로
        취급한다 — 검증된 고성능 엔진보다는 뒤지지만, 이미 나쁜 것으로
        확인된(성공률이 0.5 미만인) 엔진보다는 앞선다. 표본 부족을
        "가장 나쁨"으로 취급하면 아직 검증되지 않았을 뿐인 엔진이 이미
        확인된 저성능 엔진보다 부당하게 밀리기 때문이다."""

        def _rank(candidate: EngineCandidate) -> float:
            stat = self._execution_memory.get((required_capabilities, candidate.engine_name))
            rate = stat.success_rate() if stat is not None else None
            return -(rate if rate is not None else _NEUTRAL_RATE)

        return sorted(candidates, key=_rank)

    def _load_ratio(self, name: str) -> float:
        """**Adaptive Load Balancing(Milestone 76, ADR-0094)**:
        `InMemoryEngineRuntime._load_ratio()`와 동일 — `max_concurrency`가
        설정된 엔진은 `_in_flight / max_concurrency`, 무제한 엔진은 0.0."""

        limit = self._max_concurrency.get(name)
        if limit is None:
            return 0.0
        return self._in_flight.get(name, 0) / limit

    def _load_rank(self, candidate: EngineCandidate) -> tuple[float, int]:
        """`InMemoryEngineRuntime._load_rank()`와 동일 — 부하율이 동률이면
        (예: 무제한 엔진끼리) raw `_in_flight` 개수로 2차 tie-break해 M75
        의 기존 분산 동작을 보존한다."""

        return (
            self._load_ratio(candidate.engine_name),
            self._in_flight.get(candidate.engine_name, 0),
        )

    def _reorder_by_diversity(self, candidates: list[EngineCandidate]) -> list[EngineCandidate]:
        """**Diversity Routing(Milestone 75, ADR-0093) / Adaptive Load
        Balancing(Milestone 76, ADR-0094)**: `InMemoryEngineRuntime.
        _reorder_by_diversity()`와 동일 — 비용·성공률이 완전 동률인
        후보끼리만 지금 이 순간의 상대 부하(`_load_rank()`)가 더 낮은
        엔진을 앞세운다."""

        return sorted(candidates, key=self._load_rank)

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        timeout_seconds: float | None = None,
        *,
        model: str | None = None,
    ) -> EngineResult:
        name, adapter = self._require_adapter_and_acquire(required_capabilities, task)
        try:
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
            started = time.monotonic()
            thread.start()
            effective_timeout = (
                timeout_seconds if timeout_seconds is not None else self._default_timeout_seconds
            )
            thread.join(effective_timeout)
            latency = time.monotonic() - started

            if thread.is_alive():
                self._record_engine_outcome(name, success=False)
                self._record_execution_memory(required_capabilities, name, False, latency)
                return self._finish_as_timeout(task.task_id, session_id, adapter)

            if "error" in error_box:
                adapter.destroy_session(session_id)
                self._task_status[task.task_id] = EngineSessionStatus.FAILED
                self._record_engine_outcome(name, success=False)
                self._record_execution_memory(required_capabilities, name, False, latency)
                raise error_box["error"]

            result = self._finish_as_completed(
                task.task_id, session_id, adapter, result_box["result"]
            )
            if result.error != "cancelled":
                self._record_engine_outcome(name, result.success)
                self._record_execution_memory(required_capabilities, name, result.success, latency)
            return result
        finally:
            self._release(name)

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
            result = EngineResult(success=False, output="", error=f"engine '{name}' not registered")
            self._record_engine_outcome(name, result.success)
            return result
        try:
            session_id = adapter.create_session()
            result = adapter.run(session_id, task, model=model)
            adapter.destroy_session(session_id)
        except BaseException as exc:
            result = EngineResult(success=False, output="", error=str(exc))
        self._record_engine_outcome(name, result.success)
        return result

    def record_consensus_outcome(
        self,
        required_capabilities: frozenset[str],
        agreeing_engines: tuple[str, ...],
        dissenting_engines: tuple[str, ...],
    ) -> None:
        for name in agreeing_engines:
            key = (required_capabilities, name)
            stat = self._consensus_agreement.get(key, ConsensusAgreementStat())
            self._consensus_agreement[key] = stat.record(True)
        for name in dissenting_engines:
            key = (required_capabilities, name)
            stat = self._consensus_agreement.get(key, ConsensusAgreementStat())
            self._consensus_agreement[key] = stat.record(False)

    def consensus_weight(self, required_capabilities: frozenset[str], engine_name: str) -> float:
        stat = self._consensus_agreement.get((required_capabilities, engine_name))
        rate = stat.agreement_rate() if stat is not None else None
        return rate if rate is not None else _NEUTRAL_RATE

    def estimate_cost(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> CostEstimate:
        _name, adapter = self._require_adapter(required_capabilities, task)
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

    def _require_adapter(
        self,
        required_capabilities: frozenset[str],
        task: Task,
        excluded: frozenset[str] = frozenset(),
    ) -> tuple[str, EngineAdapter]:
        if self._engine_selection_policy is None:
            for name, adapter in self._engines.items():
                if name in excluded:
                    continue
                if not required_capabilities.issubset(adapter.capabilities()):
                    continue
                if not self._has_capacity(name):
                    continue
                return name, adapter
            raise NoSuitableEngineError(required_capabilities)

        candidates = self._build_candidates(task, required_capabilities, excluded)
        decision = self._engine_selection_policy.select(
            task, candidates, budget_policy_engine=self._budget_policy_engine
        )
        if decision is None:
            raise NoSuitableEngineError(required_capabilities)
        return decision.engine_name, self._engines[decision.engine_name]

    def _require_adapter_and_acquire(
        self, required_capabilities: frozenset[str], task: Task
    ) -> tuple[str, EngineAdapter]:
        """`_has_capacity()` 필터링은 읽기 전용 스냅샷이라, 동시에 여러
        호출이 같은 엔진을 고른 뒤 실제 슬롯 획득(`_try_acquire()`)에서
        경쟁할 수 있다. 획득에 실패하면 그 엔진을 제외하고 다시 선택해
        남은 후보로 안전하게 fallback한다(`InMemoryEngineRuntime.
        _select_and_acquire()`와 동일한 패턴)."""
        excluded: set[str] = set()
        while True:
            name, adapter = self._require_adapter(required_capabilities, task, frozenset(excluded))
            if self._try_acquire(name):
                return name, adapter
            excluded.add(name)

    def _build_candidates(
        self,
        task: Task,
        required_capabilities: frozenset[str],
        excluded: frozenset[str] = frozenset(),
    ) -> list[EngineCandidate]:
        candidates: list[EngineCandidate] = []
        for name, adapter in self._engines.items():
            if name in excluded:
                continue
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            if not self._has_capacity(name):
                continue
            stat = self._engine_reliability.get(name, EngineReliabilityStat())
            if stat.is_unreliable() and not stat.is_probe_eligible():
                self._engine_reliability[name] = stat.skip()
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
        candidates = self._reorder_by_diversity(candidates)
        return self._reorder_by_execution_memory(candidates, required_capabilities)

    def run_ensemble_auto(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        top_n: int = 2,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        if top_n < 1:
            return {}
        names = self._select_top_n(task, required_capabilities, top_n)
        if not names:
            raise NoSuitableEngineError(required_capabilities)
        started = time.monotonic()
        results = self.run_ensemble(task, names, model=model)
        latency = time.monotonic() - started
        for name in names:
            result = results.get(name)
            if result is not None:
                self._record_execution_memory(required_capabilities, name, result.success, latency)
        return results

    def _select_top_n(
        self, task: Task, required_capabilities: frozenset[str], top_n: int
    ) -> list[str]:
        if self._engine_selection_policy is None:
            names: list[str] = []
            for name, adapter in self._engines.items():
                if required_capabilities.issubset(adapter.capabilities()):
                    names.append(name)
                if len(names) >= top_n:
                    break
            return names

        remaining = self._build_candidates(task, required_capabilities)
        selected: list[str] = []
        while remaining and len(selected) < top_n:
            decision = self._engine_selection_policy.select(
                task, remaining, budget_policy_engine=self._budget_policy_engine
            )
            if decision is None:
                break
            selected.append(decision.engine_name)
            remaining = [c for c in remaining if c.engine_name != decision.engine_name]
        return selected

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
