"""Intelligence Layer — Context Freshness & Gap Analyzer (ADR-0044, Milestone 30-T03).

`context.ProjectContext`(M30-T02 산출물)만 입력으로 받는 순수 Rule
기반 판단 계층이다 — Adapter를 직접 호출하지 않는다(이미 Context
단계에서 읽어온 값만 재사용, 새로운 데이터 접근 경로 없음). AI
추론/LLM 호출은 하지 않는다(사용자 지시)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.context import ProjectContext

FRESHNESS_HEALTHY = "healthy"
FRESHNESS_WARNING = "warning"

#: ProjectContext 항목이 최소 하나는 있어야 "정상"으로 보는 Knowledge
#: Kind(ADR-0044). RULE/PROJECT(ROADMAP/PRD)는 특정 Task/Milestone
#: 마다 매번 언급되지 않는 게 자연스러운 범용 문서라 Gap 판정
#: 대상에서 제외한다.
_GAP_CHECK_KINDS = ("adr", "task", "architecture")


@dataclass(frozen=True)
class ContextGap:
    kind: str
    detail: str


@dataclass(frozen=True)
class ContextFreshness:
    level: str
    reasons: list[str]


@dataclass(frozen=True)
class ContextQuality:
    freshness: ContextFreshness
    gaps: list[ContextGap]
    score: float


class ContextFreshnessGapAnalyzer:
    """`ProjectContext`를 입력으로 Freshness/Gap을 계산하는 Rule 기반
    Analyzer. 임계값은 생성자 파라미터로 조정 가능하다."""

    def __init__(self, *, milestone_distance_threshold: int = 3) -> None:
        self._threshold = milestone_distance_threshold

    def analyze(
        self, context: ProjectContext, *, current_milestone: int | None = None
    ) -> ContextQuality:
        """
        입력: `ProjectContext`(M30-T02 산출물), current_milestone(현재
              Milestone 번호, 생략하면 Freshness는 항상 Healthy)
        출력: `ContextQuality`(Freshness 판정 + Gap 목록 + score)
        예외: 없음 — Milestone 번호를 정수로 못 만드는 항목은 조용히
              건너뛴다(방어적, 판단 중단하지 않음).
        보장: side-effect 없음(read-only), Context를 변경하지 않는다.
        """
        gaps = self._find_gaps(context)
        freshness = self._determine_freshness(context, current_milestone)
        score = self._score(gaps, freshness)
        return ContextQuality(freshness=freshness, gaps=gaps, score=score)

    def _find_gaps(self, context: ProjectContext) -> list[ContextGap]:
        gaps: list[ContextGap] = []
        for kind in _GAP_CHECK_KINDS:
            if not context.by_kind(kind):
                gaps.append(
                    ContextGap(
                        kind=kind,
                        detail=f"'{context.subject}'와 연결된 {kind} 문서를 찾지 못함",
                    )
                )
        return gaps

    def _determine_freshness(
        self, context: ProjectContext, current_milestone: int | None
    ) -> ContextFreshness:
        if current_milestone is None:
            return ContextFreshness(level=FRESHNESS_HEALTHY, reasons=[])

        reasons: list[str] = []
        for entry in context.entries:
            if entry.milestone is None:
                continue
            try:
                number = int(entry.milestone.lstrip("Mm"))
            except ValueError:
                continue
            distance = current_milestone - number
            if distance > self._threshold:
                reasons.append(
                    f"{entry.heading}는 {entry.milestone} 기준으로 현재(M{current_milestone})"
                    f"보다 {distance} Milestone 오래됨"
                )
        level = FRESHNESS_WARNING if reasons else FRESHNESS_HEALTHY
        return ContextFreshness(level=level, reasons=reasons)

    def _score(self, gaps: list[ContextGap], freshness: ContextFreshness) -> float:
        total_checks = len(_GAP_CHECK_KINDS)
        base = (total_checks - len(gaps)) / total_checks if total_checks else 1.0
        if freshness.level == FRESHNESS_WARNING:
            base = max(0.0, base - 0.2)
        return base
