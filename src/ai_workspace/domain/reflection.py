from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReflectionReport:
    """Workspace Reflection & Continuous Improvement(Milestone 81,
    ADR-0099)가 `EngineRuntime.run()` 실행 하나가 끝날 때마다 생성하는
    사후 평가 기록. `EngineRecommendation`(M79)이 실행 *전* 근거를
    설명하는 것과 대칭적으로, 이 타입은 그 근거(`expected_*`)가 실행
    *후* 실제 결과(`actual_*`)와 얼마나 맞았는지만 기록한다 — Routing
    정책을 바꾸지 않고(`_select()`/`_build_candidates()` 무관여), 예상과
    실제의 차이만 관찰한다.

    `expected_evidence`는 이번 실행이 시작되기 *직전*(이번 실행 자체가
    통계에 반영되기 전) 스냅샷한 `EngineRecommendation.evidence`와 동일한
    구조(`reliability_success_rate`/`execution_memory_success_rate`/
    `latency_seconds`/`benchmark_success_rate`/`benchmark_average_latency_
    seconds`)다. `expected_success_rate`/`expected_latency_seconds`는 그
    스냅샷에서 Routing tie-break와 같은 우선순위(execution_memory >
    benchmark > reliability)로 대표값 하나를 뽑은 파생값이며, 둘 다
    표본이 전혀 없으면 `None`이다.

    `expectation_matched`는 `expected_success_rate >= 0.5`(성공이 더
    유력하다는 예상)와 실제 `actual_success`가 일치하는지를 비교한
    결과다 — 예상 자체가 없으면(`expected_success_rate is None`)
    판정할 수 없으므로 `None`이다. `latency_gap_seconds`는 `actual_
    latency_seconds - expected_latency_seconds`(예상 latency가 없으면
    `None`)로, 양수면 예상보다 느렸다는 뜻이다."""

    engine_name: str
    expected_evidence: dict[str, float | None]
    expected_confident: bool
    expected_success_rate: float | None
    expected_latency_seconds: float | None
    actual_success: bool
    actual_latency_seconds: float
    expectation_matched: bool | None
    latency_gap_seconds: float | None
