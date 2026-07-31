"""Intelligence Layer — Recommendation Adjustment Analyzer (ADR-0058, Milestone 42-T02).

Milestone 42(Recommendation Adaptation)의 유일한 판정 로직. "Adaptation"은
새로운 1급 Domain이 아니라 **Behavioral Concept**(§13.3)이다 — 과거
실행 결과(M40 `ExperienceReport`)를 근거로 이미 결정된 판단을 사후
조정(Adjustment)하는 행동 유형을 가리킬 뿐, 새 Recommendation을
생성하지 않는다. `RecommendationRuleAnalyzer`(M35)가 고른
`NextAction`을 그대로 받아, 그 대상이 반복 실패한 기록만 있으면
추천을 보류(`None`)하고, 그 밖의 모든 경우는 그대로 통과시킨다.

**ExperienceReport 생성은 M40의 책임이다(Non-goal)** — 이 모듈은
`ExperienceReport`를 만들지 않고 오직 소비만 한다.

**Deterministic + Immutable Input(M42 DoD, 사용자 조건)**: 같은
`(next_action, experience_report)`가 주어지면 항상 같은 결과를
반환한다 — 현재 시각·난수·외부 상태를 참조하지 않는다. 두 입력
모두 읽기만 하고 수정하지 않는다.

**`experience_report=None`일 때 M35와 100% 동일 동작(M42 DoD, 사용자
조건)**: `experience_report`가 없으면 `next_action`을 그대로
반환한다 — Adjustment는 전혀 개입하지 않는다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.experience_rules import ExperienceReport
from ai_workspace.intelligence.recommendation_rules import NextAction


@dataclass(frozen=True)
class RecommendationAdjustment:
    """Adjustment 결과. `next_action`은 조정 후 최종 추천(보류 시 `None`)."""

    next_action: NextAction | None
    adjusted: bool
    reason: str | None


class RecommendationAdjustmentAnalyzer:
    """`NextAction`(M35) + `ExperienceReport`(M40)를 입력받아, 반복
    실패한 대상의 추천을 보류하는 단일 Rule만 적용하는 순수 Analyzer.
    우선순위 재설계·점수화·가중치 학습은 하지 않는다(Non-goal)."""

    def analyze(
        self,
        next_action: NextAction | None,
        experience_report: ExperienceReport | None,
    ) -> RecommendationAdjustment:
        """
        입력: next_action(M35이 이미 결정한 단일 추천, 없을 수 있음),
              experience_report(M40 `ExperienceReport`, 없을 수 있음)
        출력: `RecommendationAdjustment` — 조정 여부와 최종 추천
        예외: 없음
        보장: side-effect 없음(read-only). `next_action`/
              `experience_report`를 수정하지 않는다.
        """
        if next_action is None or experience_report is None:
            return RecommendationAdjustment(next_action=next_action, adjusted=False, reason=None)

        stat = next(
            (s for s in experience_report.stats if s.task_id == next_action.target),
            None,
        )
        if stat is not None and stat.success_count == 0 and stat.failure_count > 0:
            reason = (
                f"{next_action.target}이(가) 반복 실패(성공 0/실패 "
                f"{stat.failure_count})해 추천을 보류함"
            )
            return RecommendationAdjustment(next_action=None, adjusted=True, reason=reason)

        return RecommendationAdjustment(next_action=next_action, adjusted=False, reason=None)
