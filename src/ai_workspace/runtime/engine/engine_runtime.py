from __future__ import annotations

import threading
import time

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
)
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineRuntime,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)
from ai_workspace.interfaces.engine_selection_policy import EngineSelectionPolicy

_NEUTRAL_RATE = 0.5


class InMemoryEngineRuntime(EngineRuntime):
    """엔진 선택·세션 풀 관리·병렬 실행을 담당하는 최소 구현체
    (ARCHITECTURE.md §3.9, ADR-0016, T2-05). 세션(create_session/
    destroy_session)은 이 안에서만 관리되며 호출자에게 노출되지 않는다.

    `engine_selection_policy`(Milestone 64, ADR-0082)를 생성자로 주입하면
    `_select()`가 "능력 만족하는 첫 매칭" 대신 `EngineSelectionPolicy`(M17)
    로 비용 기반 선택을 한다 — Automation 파이프라인이 이미 쓰던 것과 같은
    선택 규칙을 Agent가 직접 쓰는 이 경로에도 적용한다. 생략(기본값 `None`)
    하면 이전 동작(Milestone 64 이전)과 100% 동일하다.

    **엔진별 신뢰도 추적 + 적응형 라우팅(Milestone 65, ADR-0083)**: `run()`/
    `run_parallel()`/`run_ensemble()`이 실제로 실행한 엔진의 성공/실패를
    이름별로 in-process 누적한다(`EngineReliabilityStat`). 비용 기반 선택
    경로(`engine_selection_policy` 주입 시)에서만 이 기록을 활용해
    `EngineReliabilityStat.is_unreliable()`(M49와 동일한 "성공 0건 + 표본
    3건 이상" 규칙)에 해당하는 엔진을 후보에서 제외한다 — 비용이 가장
    싸도 계속 실패하는 엔진은 더 이상 선택되지 않는다.

    **제외 엔진 자동 복구(Milestone 66, ADR-0084)**: `is_unreliable()`이
    한번 참이 되면 성공 기록 없이는 다시 후보가 될 수 없었던 M65의 공백을
    메운다 — `_build_candidates()`가 제외된 엔진을 `_PROBE_INTERVAL`번
    연속으로 건너뛰면 다음 선택에서 한 번 더 후보로 포함해(probe) 복구
    여부를 다시 확인할 기회를 준다.

    **Dynamic Ensemble Routing(Milestone 68, ADR-0086)**: `run_ensemble()`
    (M62)은 `engine_names`를 호출자가 직접 나열해야 했다. `run_ensemble_auto()`
    는 `_build_candidates()`(M64/M65/M66과 동일한 비용·신뢰도 기반 후보
    선정)를 재사용해 `EngineSelectionPolicy.select()`를 반복 호출하는
    방식으로 상위 `top_n`개 엔진을 동적으로 고른 뒤 기존 `run_ensemble()`
    에 그대로 위임한다 — 새 병렬 실행 로직을 만들지 않는다(YAGNI).

    **Execution Memory & Context Routing(Milestone 69, ADR-0087)**: `run()`/
    `run_ensemble_auto()`가 실제로 실행한 결과를 `(required_capabilities,
    engine_name)` 조합 키로 `EngineExecutionMemoryStat`에 누적한다(성공/
    실패/latency). `_build_candidates()`가 (기존 신뢰도 제외 이후) 이
    기록을 확인해, 같은 `required_capabilities` 조합에서 표본이 충분한
    엔진을 성공률 내림차순으로 재정렬한다 — `EngineSelectionPolicy`의
    비용 기준 `min()`은 비용이 다르면 항상 진짜 최저 비용을 고르므로,
    이 재정렬은 **비용이 동률인 후보끼리의 tie-break**로만 작동한다(표본
    부족 시 기본값 순서 그대로, 100% 하위 호환). M65/M66의 "복구 즉시
    완전 신뢰" 판정과 충돌하지 않도록 의도적으로 이렇게 범위를 좁혔다.
    신뢰도 제외와 동일하게 `engine_selection_policy` 주입 경로에서만
    적용된다.

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
    중인 세션 수(`run()`/`run_parallel()`이 세션을 만든 시점부터 정리할
    때까지)를 in-process로 카운트한다. `_select()`/`_build_candidates()`가
    한도에 도달한 엔진을 후보에서 제외해 다른 후보로 자동 fallback하고,
    후보 전체가 busy면 기존과 동일하게 `NoSuitableEngineError`를 던진다.
    `run_ensemble()`/`run_ensemble_auto()`는 호출자가 엔진을 직접 지정하거나
    (M62) 비교를 목적으로 여러 엔진을 의도적으로 동시에 쓰는 기능이라
    (M68) 이 범위에서 제외했다(YAGNI) — `max_concurrency`를 지정하지
    않으면 이전 동작과 100% 동일하다.

    **Diversity Routing(Milestone 75, ADR-0093)**: 여러 Agent가 병렬로
    Task를 제출하면, M64(비용)/M69(성공률)가 완전히 동률인 후보 여러 개가
    모두 같은 Provider에 몰려 M74의 capacity 여유를 낭비하는 경우가
    있었다. `_build_candidates()`가 M74 capacity 필터링 **이후**,
    `_reorder_by_execution_memory()`보다 먼저 `_reorder_by_diversity()`
    (안정 정렬)를 적용해 지금 이 순간의 부하가 더 적은 엔진을 완전
    동률 상황에서만 우선한다. 비용·성공률 우선순위는 정렬 순서상 항상
    이 다양성 순서를 덮어쓰므로 절대 바뀌지 않는다 — 순수 tie-break이며
    `engine_selection_policy` 미주입 시(첫 매칭 경로)에는 관여하지
    않는다(100% 하위 호환). `run_ensemble()`/`run_ensemble_auto()`는
    M74와 동일한 이유로 범위 밖(YAGNI).

    **Adaptive Load Balancing(Milestone 76, ADR-0094)**: M75의 부하
    신호를 절대 `_in_flight` 개수에서 `_load_ratio()`(= `_in_flight /
    max_concurrency`, M74 상태를 그대로 재사용 — 새 상태 없음)로
    개선했다 — Provider마다 `max_concurrency`가 다르면 절대 개수만으로는
    "한도 10 중 3개 사용 중"인 엔진과 "한도 2 중 1개 사용 중"인 엔진의
    실제 여유를 구분할 수 없었다. `max_concurrency`를 지정하지 않은
    (무제한) 엔진은 부하율 0.0으로 취급해 유한 엔진보다 항상 먼저
    선택된다 — 실제 동시 실행 상한이 없으므로 병목 위험이 없다는
    사실을 그대로 반영한다. `_reorder_by_diversity()`가 호출되는
    위치·정렬 안정성·tie-break 전용 범위는 M75와 완전히 동일하게
    유지된다."""

    def __init__(
        self,
        *,
        engine_selection_policy: EngineSelectionPolicy | None = None,
        budget_policy_engine: BudgetPolicyEngine | None = None,
    ) -> None:
        self._engines: dict[str, EngineAdapter] = {}
        self._task_status: dict[str, EngineSessionStatus] = {}
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
        """**Adaptive Load Balancing(Milestone 76, ADR-0094)**: 지금 이
        순간의 상대 부하 — `max_concurrency`가 설정된 엔진은 `_in_flight /
        max_concurrency`(0.0~1.0)로, 무제한 엔진은 병목 위험이 없으므로
        0.0으로 취급한다. M74/M75가 이미 관리하는 `_in_flight`/
        `_max_concurrency`만 읽는 read-only 계산이며 새 상태를 만들지
        않는다."""

        limit = self._max_concurrency.get(name)
        if limit is None:
            return 0.0
        return self._in_flight.get(name, 0) / limit

    def _load_rank(self, candidate: EngineCandidate) -> tuple[float, int]:
        """부하율이 동률(예: `max_concurrency`를 지정하지 않은 무제한
        엔진끼리는 항상 0.0)이면 M75의 기존 신호였던 raw `_in_flight`
        개수로 2차 tie-break한다 — M76 도입 이전에 무제한 엔진들 사이에서
        동작하던 분산 동작을 그대로 보존하면서, `max_concurrency`가 서로
        다른 엔진 사이에서는 상대 부하율이 우선한다."""

        return (
            self._load_ratio(candidate.engine_name),
            self._in_flight.get(candidate.engine_name, 0),
        )

    def _reorder_by_diversity(self, candidates: list[EngineCandidate]) -> list[EngineCandidate]:
        """**Diversity Routing(Milestone 75, ADR-0093) / Adaptive Load
        Balancing(Milestone 76, ADR-0094)**: 비용과 성공률이 모두 동률인
        후보끼리는(`_reorder_by_execution_memory()`가 그 동률을 그대로
        통과시킨 뒤, `EngineSelectionPolicy`의 `min()`이 동률일 때 반환하는
        첫 원소를 이 순서로 결정) 지금 이 순간의 상대 부하(`_load_rank()`
        = 부하율 우선, 부하율까지 동률이면 raw `_in_flight`)가 더 낮은
        (=덜 바쁜) 엔진을 앞세운다. `_reorder_by_execution_memory()`보다
        먼저 적용해(안정 정렬) 성공률이 갈리는 순간 이 부하 순서는 곧바로
        덮어써진다 — 비용·신뢰도 우선순위를 전혀 바꾸지 않고 "완전한
        동률"에서만 개입하는 선택적 최적화다."""

        return sorted(candidates, key=self._load_rank)

    def _select(
        self,
        task: Task,
        required_capabilities: frozenset[str],
        require_parallel: bool = False,
        excluded: frozenset[str] = frozenset(),
    ) -> tuple[str, EngineAdapter]:
        if self._engine_selection_policy is None:
            for name, adapter in self._engines.items():
                if name in excluded:
                    continue
                if not required_capabilities.issubset(adapter.capabilities()):
                    continue
                if require_parallel and not adapter.supports_parallel():
                    continue
                if not self._has_capacity(name):
                    continue
                return name, adapter
            raise NoSuitableEngineError(required_capabilities)

        candidates = self._build_candidates(task, required_capabilities, require_parallel, excluded)
        decision = self._engine_selection_policy.select(
            task, candidates, budget_policy_engine=self._budget_policy_engine
        )
        if decision is None:
            raise NoSuitableEngineError(required_capabilities)
        return decision.engine_name, self._engines[decision.engine_name]

    def _select_and_acquire(
        self,
        task: Task,
        required_capabilities: frozenset[str],
        require_parallel: bool = False,
    ) -> tuple[str, EngineAdapter]:
        """`max_concurrency` 필터링(`_has_capacity()`)은 후보를 고를 때
        읽기 전용 스냅샷으로 판단하므로, 여러 호출이 동시에 같은 엔진을
        고른 뒤 이 메서드에서 실제 슬롯 획득(`_try_acquire()`)을 시도할
        때 경쟁이 생길 수 있다. 획득에 실패하면(다른 호출이 먼저
        차지함) 그 엔진을 제외하고 다시 선택해, 남은 후보가 있으면
        안전하게 fallback한다."""
        excluded: set[str] = set()
        while True:
            name, adapter = self._select(
                task, required_capabilities, require_parallel, frozenset(excluded)
            )
            if self._try_acquire(name):
                return name, adapter
            excluded.add(name)

    def _build_candidates(
        self,
        task: Task,
        required_capabilities: frozenset[str],
        require_parallel: bool,
        excluded: frozenset[str] = frozenset(),
    ) -> list[EngineCandidate]:
        candidates: list[EngineCandidate] = []
        for name, adapter in self._engines.items():
            if name in excluded:
                continue
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            if require_parallel and not adapter.supports_parallel():
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

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> EngineResult:
        name, adapter = self._select_and_acquire(task, required_capabilities)
        try:
            session_id = adapter.create_session()
            started = time.monotonic()
            result = adapter.run(session_id, task, model=model)
            latency = time.monotonic() - started
            adapter.destroy_session(session_id)
            self._record_engine_outcome(name, result.success)
            self._record_execution_memory(required_capabilities, name, result.success, latency)
            self._task_status[task.task_id] = (
                EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
            )
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
        name, adapter = self._select_and_acquire(
            tasks[0], required_capabilities, require_parallel=True
        )
        try:
            results: list[EngineResult] = []
            for task in tasks:
                session_id = adapter.create_session()
                result = adapter.run(session_id, task, model=model)
                adapter.destroy_session(session_id)
                self._record_engine_outcome(name, result.success)
                self._task_status[task.task_id] = (
                    EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
                )
                results.append(result)
            return results
        finally:
            self._release(name)

    def run_ensemble(
        self,
        task: Task,
        engine_names: list[str],
        *,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        results: dict[str, EngineResult] = {}
        for name in engine_names:
            adapter = self._engines.get(name)
            if adapter is None:
                results[name] = EngineResult(
                    success=False, output="", error=f"engine '{name}' not registered"
                )
                continue
            try:
                session_id = adapter.create_session()
                results[name] = adapter.run(session_id, task, model=model)
                adapter.destroy_session(session_id)
            except BaseException as exc:
                results[name] = EngineResult(success=False, output="", error=str(exc))
            self._record_engine_outcome(name, results[name].success)
        return results

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

        remaining = self._build_candidates(task, required_capabilities, require_parallel=False)
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
        _name, adapter = self._select(task, required_capabilities)
        return adapter.estimate_cost(task)

    def cancel(self, task_id: str) -> None:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        self._task_status[task_id] = EngineSessionStatus.CANCELLED

    def status(self, task_id: str) -> EngineSessionStatus:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        return self._task_status[task_id]
