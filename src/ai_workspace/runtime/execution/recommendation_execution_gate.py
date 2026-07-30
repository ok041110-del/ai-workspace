"""Execution Layer — Recommendation Execution Gate (ADR-0050, Milestone 36-T02).

M35 `NextAction`(`intelligence/recommendation_rules.py`) 중 실제로
실행해도 안전한 것인지만 판정한다 — 변환·실행은 이 클래스의 책임이
아니다(`ActionBuilder`/`RecommendationExecutionService`가 담당,
ADR-0050 결정 3). `source=next_task`만, `manual_trigger=True`를
호출자가 명시적으로 전달했을 때만 승인한다. 나머지는 오류가 아니라
"지원하지 않음(Not Supported)"으로 표현한다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.recommendation_rules import SOURCE_NEXT_TASK, NextAction


@dataclass(frozen=True)
class GateDecision:
    """`ExecutionGate.check()`의 판정 결과."""

    approved: bool
    reason: str


class ExecutionGate:
    """실행 승인 여부만 판정하는 순수 Rule 기반 Gate. source/
    manual_trigger/next_task 여부 3가지만 확인한다."""

    def check(self, next_action: NextAction | None, *, manual_trigger: bool) -> GateDecision:
        """
        입력: M35 `NextAction`(또는 없음), manual_trigger(호출자가
              수동 트리거임을 명시적으로 전달해야 함 — 기본값 없음,
              자동/주기적 트리거로 실수로 승인되는 것을 막는다)
        출력: `GateDecision(approved, reason)`
        예외: 없음
        보장: side-effect 없음(read-only), 실행하지 않는다.
        """
        if not manual_trigger:
            return GateDecision(approved=False, reason="수동 트리거가 아님(manual_trigger=False)")
        if next_action is None:
            return GateDecision(approved=False, reason="추천할 다음 행동 없음")
        if next_action.source != SOURCE_NEXT_TASK:
            return GateDecision(
                approved=False,
                reason=f"지원하지 않음(Not Supported): source={next_action.source}",
            )
        return GateDecision(approved=True, reason="실행 승인")
