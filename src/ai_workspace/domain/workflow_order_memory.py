from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_MIN_SAMPLE_SIZE_FOR_RECOMMENDATION: Final[int] = 3


@dataclass(frozen=True)
class WorkflowOrderStat:
    """`WorkflowEngine.plan()`(Milestone 2)이 실제로 반환했던 특정 실행
    순서(order)가 성공/실패로 끝난 횟수를 누적하는 값 객체(Milestone 71,
    ADR-0089). `EngineReliabilityStat`(M65)/`EngineExecutionMemoryStat`
    (M69)/`ConsensusAgreementStat`(M70)과 동일한 패턴이다 — 키는
    "동일한 Workflow(같은 task_ids+dependencies)에서 이 특정 순서가
    쓰인 횟수"이며, `WorkflowEngine`이 in-process dict로 관리한다."""

    total: int = 0
    success_count: int = 0
    failure_count: int = 0

    def record(self, success: bool) -> WorkflowOrderStat:
        return WorkflowOrderStat(
            total=self.total + 1,
            success_count=self.success_count + (1 if success else 0),
            failure_count=self.failure_count + (0 if success else 1),
        )

    def success_rate(self) -> float | None:
        if self.total < _MIN_SAMPLE_SIZE_FOR_RECOMMENDATION:
            return None
        return self.success_count / self.total
