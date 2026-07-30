"""Intelligence Layer — Context Intelligence Service (ADR-0044, Milestone 30-T04).

`context.ContextAnalyzer`(M30-T02)와 `context_quality.
ContextFreshnessGapAnalyzer`(M30-T03)를 순서대로 실행해 하나의
`ProjectContextReport`로 묶는다. 새 판단 기준을 만들지 않는다 —
이미 만든 두 Analyzer를 순서대로 배열하고 결과를 묶을 뿐이다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter
from ai_workspace.intelligence.context import ContextAnalyzer, ProjectContext
from ai_workspace.intelligence.context_quality import ContextFreshnessGapAnalyzer, ContextQuality


@dataclass(frozen=True)
class ProjectContextReport:
    context: ProjectContext
    quality: ContextQuality


class ContextIntelligenceService:
    """Context → Freshness/Gap을 순서대로 실행해
    `ProjectContextReport`를 만든다. `KnowledgeAdapter`만 생성자로
    주입받는다."""

    def __init__(
        self,
        knowledge_adapter: KnowledgeAdapter,
        *,
        milestone_distance_threshold: int = 3,
    ) -> None:
        self._analyzer = ContextAnalyzer(knowledge_adapter)
        self._quality_analyzer = ContextFreshnessGapAnalyzer(
            milestone_distance_threshold=milestone_distance_threshold
        )

    def generate(
        self, subject: str, *, current_milestone: int | None = None
    ) -> ProjectContextReport:
        """
        입력: subject(Task/Milestone 식별자), current_milestone(선택,
              Freshness 비교 기준)
        출력: `ProjectContextReport`(Context + Quality)
        예외: 없음
        보장: side-effect 없음(read-only) — Vault/Knowledge에 쓰지
              않는다. 쓰기가 필요하면 M30-T05의 publish()를 쓴다.
        """
        context = self._analyzer.analyze(subject)
        quality = self._quality_analyzer.analyze(context, current_milestone=current_milestone)
        return ProjectContextReport(context=context, quality=quality)
