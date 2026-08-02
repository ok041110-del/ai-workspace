from __future__ import annotations

import math
import threading
import time
from collections import deque

from ai_workspace.domain.consensus_agreement import ConsensusAgreementStat
from ai_workspace.domain.engine_benchmark import EngineBenchmarkProfile
from ai_workspace.domain.engine_execution_memory import EngineExecutionMemoryStat
from ai_workspace.domain.engine_recommendation import EngineRecommendation
from ai_workspace.domain.engine_reliability import EngineReliabilityStat
from ai_workspace.domain.engine_selection import EngineCandidate, EngineSelectionDecision
from ai_workspace.domain.reflection import ReflectionReport
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
_MIN_BENCHMARK_SAMPLES = 3
_REFLECTION_HISTORY_LIMIT = 20


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
    유지된다.

    **Engine Benchmark & Capability Profiling(Milestone 77, ADR-0095)**:
    `benchmark_profile(engine_name)`은 M65 `_engine_reliability`(모든
    실행 경로의 성공/실패 누적)와 M69 `_execution_memory`(latency 기록
    경로만 반영)를 새 측정 없이 읽기 전용으로 조합해 `EngineBenchmarkProfile`
    (execution_count/success_rate()/failure_rate()/average_latency_
    seconds())로 반환한다. Routing 로직(`_select()`/`_build_candidates()`/
    `_reorder_by_diversity()`/`_reorder_by_execution_memory()`)은 전혀
    수정하지 않는다 — 순수 조회 전용 신규 public 메서드 하나만 추가했다.

    **Adaptive Engine Benchmark Routing(Milestone 78, ADR-0096)**:
    `_build_candidates()`가 `_reorder_by_diversity()`(부하) 이후,
    `_reorder_by_execution_memory()`(특정 `required_capabilities` 조합
    성공률) 이전에 `_reorder_by_benchmark()`를 적용해 M77
    `benchmark_profile()`(Provider 전체 누적 성공률·평균 레이턴시)로 한
    번 더 tie-break한다. 안정 정렬 순서상 최종 우선순위는 cost >
    execution_memory(좁지만 정밀) > benchmark(넓지만 표본 큼) >
    diversity(부하, 최후순위)이며, 표본이 `_MIN_BENCHMARK_SAMPLES`(3)
    미만이면 중립값으로 대체해 즉시 기존 순서로 fallback한다 — 새 상태를
    만들지 않고 M77이 이미 읽기 전용으로 조합해 둔 값만 재사용하며,
    `engine_selection_policy` 미주입 시(첫 매칭 경로)에는 관여하지
    않는다(100% 하위 호환).

    **Adaptive Engine Recommendation(Milestone 79, ADR-0097)**:
    `recommend_engine(task, required_capabilities, top_n=1)`은 `_build_
    candidates()`/`EngineSelectionPolicy.select()`를 실행 없이 조회만 해
    `EngineRecommendation` 목록(engine_name/reason/evidence/confident)을
    반환한다 — `run()`을 호출하지 않으므로 추천이 실행을 강제하지 않는다.
    근거(`evidence`)는 M65(신뢰도)·M69(이번 capability 조합 실행 메모리,
    "Workflow Learning" 근거로 재사용)·M77(Benchmark Profile)을 새 상태
    없이 조합한다. `execution_memory_success_rate`/`benchmark_success_
    rate`가 모두 표본 부족(3건 미만)이면 `confident=False`로 표시해,
    호출자가 근거 부족 시 기존 Routing 결과를 그대로 쓸 수 있게 한다.
    Routing 로직 자체(`_select()`/`_build_candidates()`/재정렬 메서드들)
    는 전혀 수정하지 않는다.

    **Autonomous Decision Engine(Milestone 80, ADR-0098)**: `decide_engine
    (task, required_capabilities)`은 M65~M79를 하나의 최종 실행 결정으로
    통합하는 오케스트레이션 계층이다 — 새 알고리즘 없이 `recommend_
    engine()`의 1순위를 M17 `EngineSelectionDecision`(새 domain 타입
    없음)에 그대로 담아 반환한다. `recommend_engine()`의 1순위는 항상
    `_build_candidates()`/`EngineSelectionPolicy.select()`와 같은
    파이프라인 결과이므로, confident가 낮아도 실제 선택되는 엔진은
    `run()`이 고를 엔진과 동일하다(reason에 confident 여부만 반영). 추천
    자체가 없으면(후보 없음) `_select()`를 그대로 호출해 `run()`과 동일한
    예외를 낸다 — "Recommendation 부족 시 기존 EngineSelectionPolicy로
    즉시 fallback"을 예외 정책까지 일치시켜 만족한다.

    **Workspace Reflection & Continuous Improvement(Milestone 81,
    ADR-0099)**: `run()`이 실행을 마칠 때마다, 그 실행이 시작되기
    직전(이번 실행 자체가 통계에 반영되기 전) M65/M69/M77 상태의
    스냅샷(`_evidence_snapshot()` — `_build_recommendation()`과 완전히
    같은 계산을 공유)을 "예상"으로 남기고, 실제 결과(성공 여부·latency)
    와 비교해 `ReflectionReport`를 엔진별 최근
    `_REFLECTION_HISTORY_LIMIT`(20)건만 in-process로 쌓는다(영속화 없음,
    `reflection_reports()`로 조회). Reflection은 이 실행이 예상과 얼마나
    맞았는지만 기록할 뿐 `_select()`/`_build_candidates()`/재정렬
    메서드는 전혀 건드리지 않는다 — `_build_recommendation()`의 `reason`
    텍스트에 참고 문구를 덧붙이는 것으로만 다음 Recommendation에
    반영되며, `evidence`/순위/`confident` 판정은 그대로다."""

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
        self._reflections: dict[str, deque[ReflectionReport]] = {}

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
        Balancing(Milestone 76, ADR-0094)**: 비용·성공률·Benchmark가 모두
        동률인 후보끼리는(`_reorder_by_benchmark()`와
        `_reorder_by_execution_memory()`가 그 동률을 그대로 통과시킨 뒤,
        `EngineSelectionPolicy`의 `min()`이 동률일 때 반환하는 첫 원소를
        이 순서로 결정) 지금 이 순간의 상대 부하(`_load_rank()` = 부하율
        우선, 부하율까지 동률이면 raw `_in_flight`)가 더 낮은(=덜 바쁜)
        엔진을 앞세운다. 세 재정렬 중 가장 먼저 적용해(안정 정렬) 뒤이은
        재정렬이 조금이라도 갈리면 이 부하 순서는 곧바로 덮어써진다 —
        비용·신뢰도 우선순위를 전혀 바꾸지 않고 "완전한 동률"에서만
        개입하는 최후순위 선택적 최적화다."""

        return sorted(candidates, key=self._load_rank)

    def _benchmark_rank(self, candidate: EngineCandidate) -> tuple[float, float]:
        """**Adaptive Engine Benchmark Routing(Milestone 78, ADR-0096)**:
        M77 `benchmark_profile()`(M65 전체 실행 경로 성공/실패 + M69
        latency를 읽기 전용 조합한 Provider 단위 리포트)을 재사용해 순위
        키 `(-success_rate, average_latency_seconds)`를 만든다 — 성공률
        내림차순이 1순위, 완전히 같은 성공률일 때만 평균 레이턴시
        오름차순(더 빠른 쪽 우선)으로 2차 tie-break한다. `failure_rate()`
        는 `success_count`/`failure_count`가 같은 `execution_count`에서
        나온 보완값이라 별도 정렬 기준으로 쓰지 않는다.

        표본이 `_MIN_BENCHMARK_SAMPLES`(3) 미만이면 아직 신뢰할 수 없는
        수치이므로 `_NEUTRAL_RATE`(0.5, M69와 동일한 상수)와 `math.inf`
        (레이턴시 비교에서 유리하지도 불리하지도 않도록 제외)로 대체해
        기존 재정렬(diversity) 순서를 그대로 보존한다 — 페널티도 우대도
        주지 않는 순수 fallback이다. 표본은 충분하지만 latency만 기록되지
        않은 경우(`run_parallel()`/`run_ensemble()`만 거친 엔진, M69 참고)
        도 동일하게 `math.inf`로 제외한다."""

        profile = self.benchmark_profile(candidate.engine_name)
        if profile.execution_count < _MIN_BENCHMARK_SAMPLES:
            return (-_NEUTRAL_RATE, math.inf)
        rate = profile.success_rate()
        latency = profile.average_latency_seconds()
        return (
            -(rate if rate is not None else _NEUTRAL_RATE),
            latency if latency is not None else math.inf,
        )

    def _reorder_by_benchmark(self, candidates: list[EngineCandidate]) -> list[EngineCandidate]:
        """**Adaptive Engine Benchmark Routing(Milestone 78, ADR-0096)**:
        비용이 동률인 후보끼리(`_reorder_by_execution_memory()`가 처리하는
        특정 `required_capabilities` 조합 성공률까지 동률일 때만) M77
        Benchmark Profile(Provider 전체 누적, `_reorder_by_execution_
        memory()`보다 넓은 범위·큰 표본)로 한 번 더 tie-break한다.
        `_reorder_by_diversity()`(부하, 최후순위)보다 먼저·`_reorder_by_
        execution_memory()`(특정 capability 조합 성공률, 최우선)보다
        나중에 적용해(안정 정렬) 최종 우선순위는 cost > execution_memory
        > benchmark > diversity가 된다 — 이미 확립된 M64/M69 우선순위는
        전혀 바꾸지 않고, 그보다 좁은 신호가 갈리지 않을 때만 개입하는
        추가 tie-break다."""

        return sorted(candidates, key=self._benchmark_rank)

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
        candidates = self._reorder_by_benchmark(candidates)
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
            expected_evidence, expected_confident = self._evidence_snapshot(
                name, required_capabilities
            )
            session_id = adapter.create_session()
            started = time.monotonic()
            result = adapter.run(session_id, task, model=model)
            latency = time.monotonic() - started
            adapter.destroy_session(session_id)
            self._record_engine_outcome(name, result.success)
            self._record_execution_memory(required_capabilities, name, result.success, latency)
            self._record_reflection(
                name, expected_evidence, expected_confident, result.success, latency
            )
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

    def benchmark_profile(self, engine_name: str) -> EngineBenchmarkProfile:
        """**Engine Benchmark & Capability Profiling(Milestone 77,
        ADR-0095)**: M65 `_engine_reliability`(전체 실행 경로 반영)와
        M69 `_execution_memory`(latency 기록 경로만 반영, `(required_
        capabilities, engine_name)` 키를 `engine_name`으로 필터링해
        합산)를 새 상태 없이 읽기 전용으로 조합한다."""

        reliability = self._engine_reliability.get(engine_name, EngineReliabilityStat())
        latency_sample_count = 0
        total_latency_seconds = 0.0
        for (_required_capabilities, name), stat in self._execution_memory.items():
            if name != engine_name:
                continue
            latency_sample_count += stat.total
            total_latency_seconds += stat.total_latency_seconds
        return EngineBenchmarkProfile(
            engine_name=engine_name,
            execution_count=reliability.total,
            success_count=reliability.success_count,
            failure_count=reliability.failure_count,
            latency_sample_count=latency_sample_count,
            total_latency_seconds=total_latency_seconds,
        )

    def _evidence_snapshot(
        self, name: str, required_capabilities: frozenset[str]
    ) -> tuple[dict[str, float | None], bool]:
        """M65(`_engine_reliability`)/M69(`_execution_memory`)/M77
        (`benchmark_profile()`)을 새 측정 없이 읽기 전용으로 조합해
        `EngineRecommendation.evidence`와 동일한 구조의 dict를 만든다.
        `_build_recommendation()`(M79)과 `_record_reflection()`(M81) 양쪽이
        이 계산을 공유해, "예상"이 실행 전 추천의 근거와 항상 같은
        방식으로 계산됨을 구조적으로 보장한다."""

        reliability = self._engine_reliability.get(name, EngineReliabilityStat())
        memory = self._execution_memory.get((required_capabilities, name))
        profile = self.benchmark_profile(name)
        evidence: dict[str, float | None] = {
            "reliability_success_rate": (
                reliability.success_count / reliability.total if reliability.total > 0 else None
            ),
            "execution_memory_success_rate": memory.success_rate() if memory is not None else None,
            "latency_seconds": memory.average_latency_seconds() if memory is not None else None,
            "benchmark_success_rate": profile.success_rate(),
            "benchmark_average_latency_seconds": profile.average_latency_seconds(),
        }
        confident = (
            evidence["execution_memory_success_rate"] is not None
            or profile.execution_count >= _MIN_BENCHMARK_SAMPLES
        )
        return evidence, confident

    def _reflection_note(self, name: str) -> str:
        """**Workspace Reflection & Continuous Improvement(Milestone 81,
        ADR-0099)**: `reflection_reports(name)`에 쌓인 최근 기록 중
        `expectation_matched is False`(예상과 실제가 어긋났던 실행)인
        개수를 세어, 있으면 사람이 읽을 수 있는 문구로만 반환한다. 이
        문구는 `_build_recommendation()`의 `reason`에 덧붙는 참고 정보일
        뿐, `evidence`/`confident`/순위에는 전혀 영향을 주지 않는다."""

        history = self._reflections.get(name)
        if not history:
            return ""
        mismatches = sum(1 for report in history if report.expectation_matched is False)
        if mismatches == 0:
            return ""
        return f" (최근 회고: 예측-실제 불일치 {mismatches}회)"

    def _record_reflection(
        self,
        name: str,
        expected_evidence: dict[str, float | None],
        expected_confident: bool,
        actual_success: bool,
        actual_latency_seconds: float,
    ) -> None:
        """**Workspace Reflection & Continuous Improvement(Milestone 81,
        ADR-0099)**: `run()` 실행 하나가 끝날 때마다 실행 직전 스냅샷
        (`expected_evidence`)과 실제 결과를 비교해 `ReflectionReport`를
        엔진별 `deque(maxlen=_REFLECTION_HISTORY_LIMIT)`에 추가한다 —
        Routing 상태(`_engine_reliability`/`_execution_memory`)는 이
        메서드가 호출되기 전에 이미 `_record_engine_outcome()`/`_record_
        execution_memory()`로 갱신되어 있으므로, `expected_evidence`는
        반드시 그 갱신 이전에 캡처된 스냅샷이어야 "예상"이라는 의미가
        성립한다(호출자 책임).

        `expected_success_rate`는 `execution_memory_success_rate` >
        `benchmark_success_rate` > `reliability_success_rate` 순서로
        (Routing tie-break 우선순위, M78/M69와 동일) 첫 값을 채택한다.
        `expectation_matched`는 `expected_success_rate >= 0.5`와 `actual_
        success`가 같은지 비교한다 — 예상 성공률 자체가 없으면 `None`."""

        expected_success_rate = (
            expected_evidence["execution_memory_success_rate"]
            if expected_evidence["execution_memory_success_rate"] is not None
            else expected_evidence["benchmark_success_rate"]
            if expected_evidence["benchmark_success_rate"] is not None
            else expected_evidence["reliability_success_rate"]
        )
        expected_latency_seconds = (
            expected_evidence["latency_seconds"]
            if expected_evidence["latency_seconds"] is not None
            else expected_evidence["benchmark_average_latency_seconds"]
        )
        expectation_matched = (
            None
            if expected_success_rate is None
            else (expected_success_rate >= _NEUTRAL_RATE) == actual_success
        )
        latency_gap_seconds = (
            None
            if expected_latency_seconds is None
            else actual_latency_seconds - expected_latency_seconds
        )
        report = ReflectionReport(
            engine_name=name,
            expected_evidence=expected_evidence,
            expected_confident=expected_confident,
            expected_success_rate=expected_success_rate,
            expected_latency_seconds=expected_latency_seconds,
            actual_success=actual_success,
            actual_latency_seconds=actual_latency_seconds,
            expectation_matched=expectation_matched,
            latency_gap_seconds=latency_gap_seconds,
        )
        history = self._reflections.setdefault(name, deque(maxlen=_REFLECTION_HISTORY_LIMIT))
        history.append(report)

    def reflection_reports(self, engine_name: str | None = None) -> list[ReflectionReport]:
        """`_reflections`(엔진별 최근 `_REFLECTION_HISTORY_LIMIT`건 ring
        buffer)를 읽기 전용으로 조회한다. `engine_name`을 생략하면 등록
        순서상 딕셔너리 순서로 모든 엔진의 기록을 이어 붙여 반환한다."""

        if engine_name is not None:
            return list(self._reflections.get(engine_name, ()))
        reports: list[ReflectionReport] = []
        for history in self._reflections.values():
            reports.extend(history)
        return reports

    def _build_recommendation(
        self, decision: EngineSelectionDecision, required_capabilities: frozenset[str]
    ) -> EngineRecommendation:
        """**Adaptive Engine Recommendation(Milestone 79, ADR-0097)**:
        `EngineSelectionPolicy.select()`가 이미 내린 결정(`decision`)에,
        M65/M69/M77이 읽기 전용으로 관리하는 데이터를 근거로 덧붙인다.
        `execution_memory_success_rate`(M69, 이번 `required_capabilities`
        조합 전용 — "Workflow Learning" 근거로 재사용)와 `benchmark_
        success_rate`(M77, Provider 전체 누적) 중 하나라도 표본이
        충분하면(M69/M78과 동일한 "3건 이상" 기준) `confident=True`다.

        **Workspace Reflection(Milestone 81, ADR-0099)**: `reason`에
        `_reflection_note()`가 반환하는 참고 문구(예: "최근 회고:
        예측-실제 불일치 N회")를 덧붙인다 — `evidence`/`confident`/순위는
        전혀 바뀌지 않는다(참고 정보로만 활용)."""

        name = decision.engine_name
        evidence, confident = self._evidence_snapshot(name, required_capabilities)
        reason = (
            f"{decision.reason} (Benchmark/Execution Memory 근거 반영)"
            if confident
            else f"{decision.reason} (표본 부족 — 기존 Routing 결과와 동일)"
        )
        reason = f"{reason}{self._reflection_note(name)}"
        return EngineRecommendation(
            engine_name=name, reason=reason, evidence=evidence, confident=confident
        )

    def recommend_engine(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        top_n: int = 1,
    ) -> list[EngineRecommendation]:
        """**Adaptive Engine Recommendation(Milestone 79, ADR-0097)**:
        `_build_candidates()`(M64/M65/M66/M75/M76/M78이 이미 조합해 둔
        후보 순서)와 `EngineSelectionPolicy.select()`를 실행 없이 조회만
        해(`estimate_cost()`와 동일한 read-only 경로) 추천 목록을 만든다.
        `engine_selection_policy` 미주입 시(첫 매칭 경로)에는 `run()`이
        고를 엔진과 같은 엔진을 `confident=False`로 반환한다(근거 데이터
        자체가 없음)."""

        if top_n < 1:
            return []
        if self._engine_selection_policy is None:
            recommendations: list[EngineRecommendation] = []
            for name, adapter in self._engines.items():
                if not required_capabilities.issubset(adapter.capabilities()):
                    continue
                if not self._has_capacity(name):
                    continue
                recommendations.append(
                    EngineRecommendation(
                        engine_name=name,
                        reason="engine_selection_policy 미주입(첫 매칭 경로) — 근거 데이터 없음",
                        evidence={},
                        confident=False,
                    )
                )
                if len(recommendations) >= top_n:
                    break
            return recommendations

        remaining = self._build_candidates(task, required_capabilities, require_parallel=False)
        results: list[EngineRecommendation] = []
        while remaining and len(results) < top_n:
            decision = self._engine_selection_policy.select(
                task, remaining, budget_policy_engine=self._budget_policy_engine
            )
            if decision is None:
                break
            results.append(self._build_recommendation(decision, required_capabilities))
            remaining = [c for c in remaining if c.engine_name != decision.engine_name]
        return results

    def decide_engine(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> EngineSelectionDecision:
        """**Autonomous Decision Engine(Milestone 80, ADR-0098)**: 새
        알고리즘 없이 `recommend_engine()`(M79)의 1순위를 그대로 채택한다
        — 그 1순위는 이미 `_build_candidates()`/`EngineSelectionPolicy.
        select()`와 동일한 파이프라인 결과이므로, confident 여부와 무관
        하게 이 메서드가 반환하는 engine_name은 항상 `run()`이 실제로
        선택할 엔진과 같다. 추천이 아예 없으면(후보 없음) `_select()`를
        그대로 호출해 `run()`과 동일한 예외(`NoSuitableEngineError`)를
        낸다 — "Recommendation이 없으면 기존 EngineSelectionPolicy로 즉시
        fallback"을 예외 정책까지 포함해 만족한다."""

        recommendations = self.recommend_engine(task, required_capabilities, top_n=1)
        if recommendations:
            top = recommendations[0]
            return EngineSelectionDecision(
                engine_name=top.engine_name, model=None, reason=top.reason
            )
        name, _adapter = self._select(task, required_capabilities)
        return EngineSelectionDecision(
            engine_name=name,
            model=None,
            reason="추천 근거 없음 — 기존 EngineSelectionPolicy로 fallback",
        )

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
