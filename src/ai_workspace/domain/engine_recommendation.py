from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineRecommendation:
    """Milestone 79(Adaptive Engine Recommendation, ADR-0097)가 반환하는
    단일 추천 결과. `EngineRuntime.recommend_engine()`은 실행을 강제하지
    않고 이 값만 반환한다 — 호출자가 실제로 그 Engine을 쓸지는 전적으로
    호출자의 판단이다(`EngineSelectionDecision`이 이미 확립한 "Decision
    Only, 실행과 미연결" 원칙을 그대로 따른다).

    `evidence`는 근거가 되는 지표를 이름별로 담은 읽기 전용 스냅샷이다
    (값이 `None`이면 아직 표본이 없거나 부족해 판단할 수 없다는 뜻):
    - `reliability_success_rate`: M65 `EngineReliabilityStat`(모든 실행
      경로 누적) 기반 전체 성공률.
    - `execution_memory_success_rate`: M69 `EngineExecutionMemoryStat`
      (이번 `required_capabilities` 조합 전용, 표본 3건 미만이면 `None`)
      기반 성공률 — 이 Milestone에서 "Workflow Learning" 근거로 재사용
      한다(별도 `WorkflowEngine`을 참조하지 않음, ADR-0080/0081/M70의
      결합 금지 원칙 유지).
    - `latency_seconds`: 같은 M69 통계의 평균 latency.
    - `benchmark_success_rate`/`benchmark_average_latency_seconds`: M77
      `EngineBenchmarkProfile`(Provider 전체 누적, 더 넓은 범위) 기반.

    `confident`는 `execution_memory_success_rate`/`benchmark_success_rate`
    중 하나라도 표본이 충분해(M69/M78과 동일한 "3건 이상" 기준) 값이
    있으면 `True`다. `False`면 비용·원시 신뢰도만으로 고른 것이라
    호출자는 이 추천을 무시하고 기존 Routing 결과(`run()`이 실제로
    선택하는 것과 동일한 엔진)를 그대로 써도 무방하다는 뜻이다."""

    engine_name: str
    reason: str
    evidence: dict[str, float | None]
    confident: bool
