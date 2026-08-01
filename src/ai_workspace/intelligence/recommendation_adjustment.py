"""Intelligence Layer — Recommendation Adjustment Analyzer (ADR-0058, Milestone 42-T02;
표본 수 조건 정교화는 Milestone 49-T03, ADR-0066; 추세 기반 규칙 추가는
Milestone 51-T03, ADR-0068; 가중치 결합은 Milestone 52-T03, ADR-0070;
지수 Decay 실패율 반영은 Milestone 53-T03, ADR-0071; `compute_learning_score`
공개 승격은 Milestone 55-T03, ADR-0073).

Milestone 42(Recommendation Adaptation)의 유일한 판정 로직. "Adaptation"은
새로운 1급 Domain이 아니라 **Behavioral Concept**(§13.3)이다 — 과거
실행 결과(M40 `ExperienceReport`)를 근거로 이미 결정된 판단을 사후
조정(Adjustment)하는 행동 유형을 가리킬 뿐, 새 Recommendation을
생성하지 않는다.

**두 신호를 가중치 점수로 결합(M52, ADR-0070)**: M49/M51까지는 "전체
실패율 100%" 또는 "최근 연속 실패 5회" 중 하나를 만족하면 보류하는
이진(OR) 판정이었다. M52는 두 신호를 연속값으로 바꿔 가중 합산한다:

- `signal_overall = stat.decayed_failure_rate`(단, `total <
  _MIN_SAMPLE_SIZE_FOR_WITHHOLD`이면 0 — 최소 표본 조건 그대로 유지)
- `signal_recent = min(recent_failure_streak /
  _RECENT_FAILURE_STREAK_THRESHOLD, 1.0)`
- `score = _OVERALL_FAILURE_WEIGHT * signal_overall +
  _RECENT_STREAK_WEIGHT * signal_recent`
- `score >= WITHHOLD_SCORE_THRESHOLD`이면 보류

가중치·threshold는 모두 0.6으로 동일(사용자 확정) — 신호 하나가
완전히 1.0(기존 M49/M51 조건 그대로)이면 그 신호만으로 이미
`score = 0.6 >= 0.6`이 성립해 **기존 두 Rule은 그대로 보존된다(회귀
없음, 수학적으로 보장)**. 새로 생기는 능력은 두 신호가 각각은
임계값 미달이지만 합치면 위험한 조합(예: 실패율 60% + 최근 3회
연속 실패)도 잡아내는 것이다.

**지수 Decay 실패율(M53, ADR-0071)**: M52의 `signal_overall`은 원래
`failure_count / total`(단순 평균, 모든 기록을 동등하게 반영)이었다.
M53은 이를 `ExperienceStat.decayed_failure_rate`(M40/M51,
`experience_rules.py`가 계산 — 지수 Decay 가중치로 최근 기록에 더
큰 비중)로 교체한다. 전체 이력이 100% 실패면 `decayed_failure_rate`
는 가중치와 무관하게 항상 정확히 1.0이므로, M49 단일 규칙과 M52의
"신호 1.0이면 score=0.6 성립" 체인이 그대로 보존된다(회귀 없음).

**Non-goal**: 가중치(`_OVERALL_FAILURE_WEIGHT`/`_RECENT_STREAK_WEIGHT`)
와 threshold, 그리고 `decayed_failure_rate`가 사용하는 Decay 계수
(`experience_rules._DECAY_FACTOR`)는 모두 코드에 고정된 상수다 —
데이터로부터 이 값들을 학습하거나 세션 중에 조정하는 온라인 학습은
하지 않는다.

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
_OVERALL_FAILURE_WEIGHT: Final[float] = 0.6
_RECENT_STREAK_WEIGHT: Final[float] = 0.6
WITHHOLD_SCORE_THRESHOLD: Final[float] = 0.6


@dataclass(frozen=True)
class RecommendationAdjustment:
    """Adjustment 결과. `next_action`은 조정 후 최종 추천(보류 시 `None`)."""

    next_action: NextAction | None
    adjusted: bool
    reason: str | None


class RecommendationAdjustmentAnalyzer:
    """`NextAction`(M35) + `ExperienceReport`(M40)를 입력받아, 전체 실패율
    신호(M49/M50)와 최근 연속 실패 신호(M51)를 고정 가중치로 결합한
    점수(M52)가 임계값 이상인 대상의 추천을 보류하는 순수 Analyzer.
    가중치·threshold 모두 고정 상수이며, 데이터 기반 가중치 학습은
    하지 않는다(Non-goal 유지)."""

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
        score = compute_learning_score(stat)

        if score >= WITHHOLD_SCORE_THRESHOLD:
            reason = _build_withhold_reason(
                next_action.target, stat, score, overall_failure_triggered, recent_streak_triggered
            )
            return RecommendationAdjustment(next_action=None, adjusted=True, reason=reason)

        return RecommendationAdjustment(next_action=next_action, adjusted=False, reason=None)


def compute_learning_score(stat: ExperienceStat) -> float:
    """M52/M53의 가중치 결합 점수를 계산한다(M55, ADR-0073에서 공개
    함수로 승격 — 원래 private `_withhold_score`였다). `analyze()`의
    보류 판정뿐 아니라 `recommendation_explanation.py`(M44/M55)가
    보류 여부와 무관하게 학습 신호를 상시 노출하는 데도 재사용해,
    가중치·threshold 공식을 두 곳에 중복 구현하지 않는다."""
    signal_overall = (
        stat.decayed_failure_rate if stat.total >= _MIN_SAMPLE_SIZE_FOR_WITHHOLD else 0.0
    )
    signal_recent = min(stat.recent_failure_streak / _RECENT_FAILURE_STREAK_THRESHOLD, 1.0)
    return _OVERALL_FAILURE_WEIGHT * signal_overall + _RECENT_STREAK_WEIGHT * signal_recent


def _build_withhold_reason(
    target: str,
    stat: ExperienceStat,
    score: float,
    overall_failure_triggered: bool,
    recent_streak_triggered: bool,
) -> str:
    overall_text = (
        f"실패율 {stat.failure_count}/{stat.total}(Decay 반영 {stat.decayed_failure_rate:.2f})"
    )
    recent_text = f"최근 {stat.recent_failure_streak}회 연속 실패"

    if overall_failure_triggered and recent_streak_triggered:
        return f"{target}이(가) {overall_text} 및 {recent_text}해 추천을 보류함(M49+M51 규칙)"
    if overall_failure_triggered:
        return f"{target}이(가) {overall_text}해 추천을 보류함(M49 규칙)"
    if recent_streak_triggered:
        return f"{target}이(가) {recent_text}해 추천을 보류함(M51 규칙, 과거 성공 이력 있음)"
    return (
        f"{target}이(가) {overall_text} + {recent_text} 조합(가중치 점수 "
        f"{score:.2f})해 추천을 보류함(M52 가중치 결합 규칙)"
    )
