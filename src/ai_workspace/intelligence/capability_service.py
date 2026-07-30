"""Intelligence Layer — Capability Intelligence Service (ADR-0045, Milestone 31-T04/T05).

`capability.CapabilitySnapshotAnalyzer`(M31-T02)와 `capability_gap.
CapabilityGapAnalyzer`(M31-T03)를 순서대로 실행해 하나의
`CapabilityIntelligenceReport`로 묶는다(T04). `render_markdown()`/
`publish()`(T05)는 그 결과를 Markdown으로 렌더링해 Vault에 노출한다
— 여기서도 새 판단 기준을 만들지 않는다(이미 만든 두 Analyzer를
호출 순서대로 배열하고 결과를 묶을 뿐, `report.py`(M29-T05)/
`context_service.py`(M30-T04/T05)와 같은 조합 방식)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability import AgentCapabilitySnapshot, CapabilitySnapshotAnalyzer
from ai_workspace.intelligence.capability_gap import CapabilityGapAnalyzer, CapabilityGapReport

_COVERAGE_LABELS = {"none": "None", "partial": "Partial", "full": "Full"}


@dataclass(frozen=True)
class CapabilityIntelligenceReport:
    snapshot: AgentCapabilitySnapshot
    gap_report: CapabilityGapReport


class CapabilityIntelligenceService:
    """Snapshot → Coverage/Gap을 순서대로 실행해
    `CapabilityIntelligenceReport`를 만든다(`generate()`).
    `VaultAdapter`가 주입돼 있으면 Markdown으로 렌더링해 Vault에
    노출한다(`publish()`). `AgentAdapter`(필수)/`VaultAdapter`(선택,
    미주입 시 `publish()` 호출 불가)만 생성자로 주입받는다."""

    def __init__(
        self,
        agent_adapter: AgentAdapter,
        vault_adapter: VaultAdapter | None = None,
    ) -> None:
        self._snapshot_analyzer = CapabilitySnapshotAnalyzer(agent_adapter)
        self._gap_analyzer = CapabilityGapAnalyzer()
        self._vault_adapter = vault_adapter

    def generate(self) -> CapabilityIntelligenceReport:
        """
        입력: 없음
        출력: `CapabilityIntelligenceReport`(Snapshot + Coverage/Gap)
        예외: 없음
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        snapshot = self._snapshot_analyzer.analyze()
        gap_report = self._gap_analyzer.analyze(snapshot)
        return CapabilityIntelligenceReport(snapshot=snapshot, gap_report=gap_report)

    def publish(self) -> tuple[CapabilityIntelligenceReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_capability_report()`에 위임).

        예외: 생성자에 `vault_adapter`를 주입하지 않았으면
              `ValueError`.
        보장: `15 Project Intelligence/Capability Intelligence.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        if self._vault_adapter is None:
            raise ValueError("publish()를 쓰려면 생성자에 vault_adapter를 주입해야 합니다")
        report = self.generate()
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_capability_report(markdown)
        return report, path


def render_markdown(report: CapabilityIntelligenceReport) -> str:
    """`CapabilityIntelligenceReport`를 Vault 문서 Markdown으로
    렌더링한다. 순수 함수(입출력 문자열 변환만, I/O 없음)."""
    snapshot = report.snapshot
    coverage = report.gap_report.coverage

    lines = [
        "---",
        "tags: [capability-intelligence]",
        "type: capability-intelligence",
        "---",
        "",
        "# Capability Intelligence",
        "",
        "> Milestone 31(Capability Intelligence)이 계산한 읽기 전용 "
        "리포트다(ADR-0045). 매 생성 시 이 문서 전체가 덮어써진다 — "
        "편집해도 다음 생성 때 사라진다.",
        "",
        "## Snapshot",
        "",
        f"- 활성 Agent 수: {snapshot.total_active_agents}",
        "",
        "### Role별",
        "",
    ]
    if snapshot.by_role:
        lines.extend(f"- {role}: {count}건" for role, count in snapshot.by_role.items())
    else:
        lines.append("- (없음)")

    lines.extend(["", "### Capability별", ""])
    if snapshot.by_capability:
        lines.extend(
            f"- {capability}: {count}건"
            for capability, count in sorted(snapshot.by_capability.items())
        )
    else:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## Coverage",
            "",
            f"**{_COVERAGE_LABELS.get(coverage.level, coverage.level)}** "
            f"({coverage.ratio:.0%})",
            "",
            "## Gap",
            "",
        ]
    )
    if report.gap_report.gaps:
        lines.extend(f"- {gap.capability}: {gap.detail}" for gap in report.gap_report.gaps)
    else:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## 관련 문서",
            "",
            "- [[Milestones Index]]",
            "- [[Project Intelligence]]",
            "",
            "## 원문",
            "",
            "- `.ai/TASKS.md`의 \"Milestone 31 — Capability Intelligence\" 절",
            "- `src/ai_workspace/intelligence/`",
            "",
        ]
    )
    return "\n".join(lines)
