from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionMemory:
    """Milestone 39(Memory Engine)가 다루는 최소 기록 단위 — "Execution
    결과 하나"를 표현한다. Learning(과거 기록으로 판단·추천을 바꾸는 것)
    에 필요한 embedding/score/vector/confidence는 의도적으로 포함하지
    않는다 — 그 책임은 향후 Learning Engine(M40 이후, 별도 승인 대상)
    에 남겨둔다(ADR-0053)."""

    task_id: str
    action: str
    result: str  # "success" 또는 "failure"
    timestamp: str
    reason: str | None = None
