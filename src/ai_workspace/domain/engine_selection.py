from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineCandidate:
    """`EngineRegistry`가 나열하는, 실행 가능한 Engine 후보 하나를
    표현하는 순수 domain 객체(M17-T01). `CostEstimate`(interfaces
    계층)를 그대로 재사용하지 않고 값만 옮겨 담아, domain 계층이
    interfaces에 의존하지 않는 기존 원칙을 유지한다."""

    engine_name: str
    capabilities: frozenset[str]
    estimated_tokens: int
    estimated_cost_usd: float
    supports_parallel: bool


@dataclass(frozen=True)
class EngineSelectionDecision:
    """`EngineSelectionPolicy.select()`의 결과(M17-T01). `reason`은
    사람이 읽을 수 있는 선택 근거를 담는다(사용자 승인 조건). 이
    결정은 실제 실행과 연결되지 않는다 — M17은 Decision Only
    Milestone이고, 실행 연결은 M18의 책임이다. `model`은 이번
    Milestone의 판단 대상이 아니다(M14의 정적 정책이 계속 담당) —
    항상 `None`을 반환하되, 향후 Model 수준 결정이 필요해지면 이
    필드를 그대로 채우면 된다."""

    engine_name: str
    model: str | None
    reason: str
