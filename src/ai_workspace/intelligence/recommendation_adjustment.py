"""Intelligence Layer — Recommendation Adjustment Analyzer (ADR-0058, Milestone 42-T02;
표본 수 조건 정교화는 Milestone 49-T03, ADR-0066; 추세 기반 규칙 추가는
Milestone 51-T03, ADR-0068).

Milestone 42(Recommendation Adaptation)의 유일한 판정 로직. "Adaptation"은
새로운 1급 Domain이 아니라 **Behavioral Concept**(§13.3)이다 — 과거
실행 결과(M40 `ExperienceReport`)를 근거로 이미 결정된 판단을 사후
조정(Adjustment)하는 행동 유형을 가리킬 뿐, 새 Recommendation을
생성하지 않는다. `RecommendationRuleAnalyzer`(M35)가 고른
`NextAction`을 그대로 받아, 아래 두 Rule 중 하나라도 만족하면 추천을
보류(`None`)하고, 그 밖의 모든 경우는 그대로 통과시킨다.

**Rule M49/M50(전체 이력 기반)**: 대상이 실패율 100%(성공 0건)이고
표본이 `_MIN_SAMPLE_SIZE_FOR_WITHHOLD`건 이상 쌓였으면 보류. 표본이
적을 때(예: 실패 1~2건뿐) 성급하게 보류하지 않도록 최소 표본 조건을
Milestone 49에서 추가했다(ADR-0066) — 기존 규칙(표본 1건부터 보류)의
상위 집합이라 회귀는 없다.

**Rule M51(최근 추세 기반, ADR-0068)**: 전체 이력에 성공이 섞여
있더라도, 가장 최근 `_RECENT_FAILURE_STREAK_THRESHOLD`건이 모두
실패(`ExperienceStat.recent_failure_streak`가 그 값 이상)면 보류.
M49/M50 규칙은 전체 이력의 실패율만 보므로 "예전엔 성공했지만 최근
들어 계속 실패하는" 추세 악화를 포착하지 못한다 — M51은 이 규칙을
**대체가 아니라 보완**으로 추가한다(두 규칙 병존, 기존 규칙 무변경).

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
from typing import Final

from ai_workspace.intelligence.experience_rules import ExperienceReport, ExperienceStat
from ai_workspace.intelligence.recommendation_rules import NextAction

_MIN_SAMPLE_SIZE_FOR_WITHHOLD: Final[int] = 3
_RECENT_FAILURE_STREAK_THRESHOLD: Final[int] = 5


@dataclass(frozen=True)
class RecommendationAdjustment:
    """Adjustment 결과. `next_action`은 조정 후 최종 추천(보류 시 `None`)."""

    next_action: NextAction | None
    adjusted: bool
    reason: str | None


class RecommendationAdjustmentAnalyzer:
    """`NextAction`(M35) + `ExperienceReport`(M40)를 입력받아, (1) 표본이
    충분히 쌓인 상태의 전체 실패(M49/M50) 또는 (2) 최근 연속 실패 추세
    (M51) 중 하나라도 만족하는 대상의 추천을 보류하는 순수 Analyzer.
    두 Rule 모두 고정 임계값 기반이며, 우선순위 재설계나 임의의
    점수화·가중치 학습은 하지 않는다(Non-goal 유지)."""

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
        if stat is None:
            return RecommendationAdjustment(next_action=next_action, adjusted=False, reason=None)

        overall_failure_triggered = (
            stat.success_count == 0 and stat.total >= _MIN_SAMPLE_SIZE_FOR_WITHHOLD
        )
        recent_streak_triggered = stat.recent_failure_streak >= _RECENT_FAILURE_STREAK_THRESHOLD

        if overall_failure_triggered or recent_streak_triggered:
            reason = _build_withhold_reason(
                next_action.target, stat, overall_failure_triggered, recent_streak_triggered
            )
            return RecommendationAdjustment(next_action=None, adjusted=True, reason=reason)

        return RecommendationAdjustment(next_action=next_action, adjusted=False, reason=None)


def _build_withhold_reason(
    target: str,
    stat: ExperienceStat,
    overall_failure_triggered: bool,
    recent_streak_triggered: bool,
) -> str:
    overall_text = f"반복 실패(성공 0/실패 {stat.failure_count})"
    recent_text = f"최근 {stat.recent_failure_streak}회 연속 실패"

    if overall_failure_triggered and recent_streak_triggered:
        return f"{target}이(가) {overall_text} 및 {recent_text}해 추천을 보류함(M49+M51 규칙)"
    if recent_streak_triggered:
        return f"{target}이(가) {recent_text}해 추천을 보류함(M51 규칙, 과거 성공 이력 있음)"
    return f"{target}이(가) {overall_text}해 추천을 보류함(M49 규칙)"
