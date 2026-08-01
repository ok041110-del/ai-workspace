"""Intelligence Layer — Recommendation Explanation Analyzer (ADR-0061, Milestone 44-T02;
학습 신호 상시 노출은 Milestone 55-T03, ADR-0073).

**책임(Responsibility)**: Recommendation은 "무엇을 할 것인가"를
결정하고(M35/M42/M43), Explanation은 "왜 그렇게 결정했는가"를 이미
계산된 값들로부터 **구조적으로 재구성**한다 — 새 판단 로직이 아니다.
`RecommendationIntelligenceReport`(M35, Adaptation 반영 시 M42)와
`ExperienceReport`(M40)를 그대로 읽어, 5단계 Priority Rule 중 어느
단계가 왜 통과/실패했는지, Adaptation이 왜 적용/미적용됐는지를
사람이 읽을 수 있는 근거(Evidence)로 펼쳐 보일 뿐이다.

**학습 신호 상시 노출(M55, ADR-0073)**: M49~M53까지 쌓인 학습 신호
(`decayed_failure_rate`/`recent_failure_streak`/가중치 결합 score)
는 M52까지 Adaptation이 실제로 보류를 발동했을 때만(`adaptation_
reason` 프로즈 문자열 안에) 보였다 — 아직 보류되지 않았지만 값이
임계값에 가까운 "near-miss" 케이스는 전혀 드러나지 않았다.
`experience_summary`는 이제 보류 여부와 무관하게 이 신호들을 항상
포함한다. `RecommendationAdjustmentAnalyzer.compute_learning_score()`
(M52/M53이 이미 계산하는 공식, M55에서 공개 함수로 승격)를 그대로
재사용해 가중치·threshold 공식을 중복 구현하지 않는다.

Recommendation 자체를 바꾸지 않는다 — `next_action`은
`RecommendationIntelligenceReport`가 이미 결정한 값을 그대로
옮긴다. Deterministic + Immutable Input(M40/M42와 동일 조건):
같은 `(report, experience_report)`가 주어지면 항상 같은
`RecommendationExplanationReport`를 반환하고, 두 입력 모두 읽기만
한다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.experience_rules import ExperienceReport
from ai_workspace.intelligence.recommendation_adjustment import (
    WITHHOLD_SCORE_THRESHOLD,
    compute_learning_score,
)
from ai_workspace.intelligence.recommendation_rules import (
    SOURCE_BLOCKED_TASK,
    SOURCE_CAPABILITY_GAP,
    SOURCE_CURRENT_WORK,
    SOURCE_NEXT_TASK,
    SOURCE_PROJECT_RECOMMENDATION,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceReport

#: 5단계 Priority Rule의 평가 순서와 표시 라벨(M35, `RecommendationRuleAnalyzer`
#: 와 100% 동일한 순서 — 새 순서를 만들지 않는다).
_PRIORITY_STEPS: tuple[tuple[str, str], ...] = (
    (SOURCE_CURRENT_WORK, "현재 작업"),
    (SOURCE_NEXT_TASK, "다음 Task"),
    (SOURCE_BLOCKED_TASK, "Blocked Task"),
    (SOURCE_CAPABILITY_GAP, "Capability Gap"),
    (SOURCE_PROJECT_RECOMMENDATION, "Project Recommendation"),
)


@dataclass(frozen=True)
class PriorityStepTrace:
    """5단계 Priority Rule 중 한 단계의 평가 결과(순서대로)."""

    rank: int
    source: str
    label: str
    matched: bool
    detail: str


@dataclass(frozen=True)
class RecommendationExplanationReport:
    """`RecommendationExplanationAnalyzer.analyze()`의 결과 —
    Recommendation의 근거(Evidence)를 구조적으로 담는다."""

    next_action_target: str | None
    trace: list[PriorityStepTrace]
    experience_summary: str | None
    adaptation_applied: bool
    adaptation_reason: str | None


class RecommendationExplanationAnalyzer:
    """`RecommendationIntelligenceReport`(M35/M42) + `ExperienceReport`
    (M40, 선택)를 읽어 근거를 재구성하는 순수 Analyzer. 새 AI 판단·
    새 지표 없음 — 이미 계산된 값을 사람이 읽을 수 있는 형태로 펼칠
    뿐이다."""

    def analyze(
        self,
        report: RecommendationIntelligenceReport,
        experience_report: ExperienceReport | None = None,
    ) -> RecommendationExplanationReport:
        """
        입력: report(M35/M42가 이미 계산한 `RecommendationIntelligenceReport`),
              experience_report(M40 `ExperienceReport`, 없을 수 있음)
        출력: `RecommendationExplanationReport`
        예외: 없음
        보장: side-effect 없음(read-only), 두 입력 모두 수정하지
              않는다. `report.next_action`을 바꾸지 않는다 — 그대로
              옮길 뿐이다.
        """
        trace = self._build_trace(report)
        experience_summary = self._build_experience_summary(report, experience_report)

        return RecommendationExplanationReport(
            next_action_target=report.next_action.target if report.next_action else None,
            trace=trace,
            experience_summary=experience_summary,
            adaptation_applied=report.adjusted,
            adaptation_reason=report.adjustment_reason,
        )

    def _build_trace(self, report: RecommendationIntelligenceReport) -> list[PriorityStepTrace]:
        presence = {
            SOURCE_CURRENT_WORK: report.current_work is not None,
            SOURCE_NEXT_TASK: any(
                m.next_task_ids for m in report.workflow_report.milestones
            ),
            SOURCE_BLOCKED_TASK: any(
                m.blocked_count > 0 for m in report.workflow_report.milestones
            ),
            SOURCE_CAPABILITY_GAP: bool(report.capability_gap_report.gaps),
            SOURCE_PROJECT_RECOMMENDATION: bool(report.project_recommendations),
        }
        selected_source = report.next_action.source if report.next_action else None

        trace: list[PriorityStepTrace] = []
        for rank, (source, label) in enumerate(_PRIORITY_STEPS, start=1):
            matched = source == selected_source
            detail = "존재(선택됨)" if matched else ("존재" if presence[source] else "없음")
            trace.append(
                PriorityStepTrace(
                    rank=rank, source=source, label=label, matched=matched, detail=detail
                )
            )
        return trace

    def _build_experience_summary(
        self,
        report: RecommendationIntelligenceReport,
        experience_report: ExperienceReport | None,
    ) -> str | None:
        if experience_report is None or report.next_action is None:
            return None
        stat = next(
            (s for s in experience_report.stats if s.task_id == report.next_action.target), None
        )
        if stat is None:
            return None
        success_rate = round((stat.success_count / stat.total) * 100)
        score = compute_learning_score(stat)
        return (
            f"성공률 {success_rate}%({stat.total}건 중 {stat.success_count}건 성공) · "
            f"Decay실패율 {stat.decayed_failure_rate:.2f} · "
            f"연속실패 {stat.recent_failure_streak} · "
            f"학습 Score {score:.2f}/{WITHHOLD_SCORE_THRESHOLD:.2f}"
        )
