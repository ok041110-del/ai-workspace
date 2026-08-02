from __future__ import annotations

from enum import Enum


class DecisionGoal(Enum):
    """Goal-Aware Decision Policy(Milestone 82, ADR-0100)가 `EngineRuntime.
    recommend_engine()`/`decide_engine()`에 도입하는 목표 프로필. 새
    알고리즘이 아니라 이미 존재하는 의사결정 요소(Cost/Quality(신뢰도·
    Benchmark·Workflow Learning 대표값)/Latency)의 **우선순위 정렬
    순서**만 바꾸는 Policy다 — Routing(`_select()`/`_build_candidates()`)
    이나 `EngineSelectionPolicy` 자체는 전혀 수정하지 않는다.

    `BALANCED`(기본값)는 goal을 지정하지 않았을 때와 완전히 동일한 코드
    경로를 타므로(새 분기 자체가 실행되지 않음), 기존 `run()`이 실제로
    선택하는 엔진과 항상 같다는 M80의 보장이 그대로 유지된다. 나머지 세
    프로필(`COST_OPTIMIZED`/`QUALITY_OPTIMIZED`/`LATENCY_OPTIMIZED`)은
    `recommend_engine()`/`decide_engine()`에 명시적으로 `goal`을 전달했을
    때만 적용되는 별도 우선순위 정렬이며, `run()`이 실제로 고를 엔진과
    달라질 수 있다(그 경우 `reason`에 그 사실이 명시된다)."""

    COST_OPTIMIZED = "cost_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    BALANCED = "balanced"
