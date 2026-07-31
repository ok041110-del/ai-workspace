"""Intelligence Layer — Recommendation Explanation Service (ADR-0061, Milestone 44-T03).

`RecommendationExplanationAnalyzer`(M44-T02) 호출 + Vault 발행을
조합만 하는 얇은 계층 — `ExperienceIntelligenceService`(M40)와 같은
뼈대. 판정 로직은 전혀 갖지 않는다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.experience_rules import ExperienceReport
from ai_workspace.intelligence.recommendation_explanation import (
    RecommendationExplanationAnalyzer,
    RecommendationExplanationReport,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceReport


class RecommendationExplanationService:
    """`RecommendationExplanationAnalyzer`(M44-T02) + Vault 발행을
    조합한다. Recommendation을 스스로 계산하지 않는다 — 호출자가
    이미 계산한 `RecommendationIntelligenceReport`를 받는다(M43의
    `RecommendationExecutionService`와 동일한 결합도 원칙, ADR-0059)."""

    def __init__(self, vault_adapter: VaultAdapter) -> None:
        self._vault_adapter = vault_adapter
        self._analyzer = RecommendationExplanationAnalyzer()

    def generate(
        self,
        report: RecommendationIntelligenceReport,
        experience_report: ExperienceReport | None = None,
    ) -> RecommendationExplanationReport:
        """
        입력: report(M35/M42가 이미 계산한 `RecommendationIntelligenceReport`),
              experience_report(M40 `ExperienceReport`, 없을 수 있음)
        출력: `RecommendationExplanationReport`
        예외: 없음
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        return self._analyzer.analyze(report, experience_report)

    def publish(
        self,
        report: RecommendationIntelligenceReport,
        experience_report: ExperienceReport | None = None,
    ) -> tuple[RecommendationExplanationReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_recommendation_explanation()`에 위임).

        보장: `15 Project Intelligence/Recommendation Explanation.md`
              가 이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        explanation = self.generate(report, experience_report)
        markdown = render_markdown(explanation)
        path = self._vault_adapter.publish_recommendation_explanation(markdown)
        return explanation, path


def render_markdown(explanation: RecommendationExplanationReport) -> str:
    """`RecommendationExplanationReport`를 Vault 문서 Markdown으로
    렌더링한다. 순수 함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [recommendation-explanation]",
        "type: recommendation-explanation",
        "---",
        "",
        "# Recommendation Explanation",
        "",
        "> Milestone 44(Recommendation Explainability)가 Recommendation"
        "(M35/M42/M43)이 왜 그렇게 결정됐는지를 이미 계산된 값으로부터"
        " 구조적으로 재구성한 읽기 전용 문서다(ADR-0061). Recommendation"
        " 자체를 바꾸지 않는다 — 근거만 보여준다. 매 생성 시 이 문서"
        " 전체가 덮어써진다 — 편집해도 다음 생성 때 사라진다.",
        "",
        "## Next Action",
        "",
    ]
    if explanation.next_action_target is not None:
        lines.append(f"- 대상: {explanation.next_action_target}")
    else:
        lines.append("- 추천할 다음 행동 없음")

    lines.extend(["", "## Reason", ""])
    for step in explanation.trace:
        suffix = " 선택" if step.matched else ""
        marker = f"Priority Rule #{step.rank}{suffix}"
        lines.append(f"- {step.label}: {step.detail} ({marker})")
    if explanation.experience_summary is not None:
        lines.append(f"- Experience {explanation.experience_summary}")
    if explanation.adaptation_applied:
        lines.append(f"- Adaptation 적용됨: {explanation.adaptation_reason}")
    else:
        lines.append("- Adaptation 적용 안 됨")

    lines.append("")
    return "\n".join(lines)
