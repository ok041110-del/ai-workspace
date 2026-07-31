"""Architecture Guardian — Service(ADR-0056, Milestone 41-T01/T02).

`GUARDIAN_RULES`를 `checker.evaluate()`로 평가하고, 그 결과를 Vault에
발행한다. **Vault 발행은 부가 기능이 아니라 이 Service의 핵심
Output이다**(사용자 조건) — `publish()`가 기본 진입점이고,
`generate()`는 그 전 단계(평가만)를 노출할 뿐이다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.models import ArchitectureHealthReport
from ai_workspace.guardian.rules import GUARDIAN_RULES
from ai_workspace.integration.vault_adapter import VaultAdapter


class ArchitectureGuardianService:
    """`GUARDIAN_RULES`를 소스 트리에 대해 평가하고 Vault에 발행하는
    얇은 조합 계층 — `RecommendationIntelligenceService`(M35)와 같은
    뼈대다. 평가 로직은 전혀 갖지 않는다(`checker`의 책임)."""

    def __init__(self, vault_adapter: VaultAdapter, src_root: Path) -> None:
        self._vault_adapter = vault_adapter
        self._src_root = src_root

    def generate(self) -> ArchitectureHealthReport:
        """
        입력: 없음
        출력: `GUARDIAN_RULES` 전체를 `self._src_root`에 대해 평가한
              `ArchitectureHealthReport`
        예외: 없음
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        return evaluate(GUARDIAN_RULES, self._src_root)

    def publish(self) -> tuple[ArchitectureHealthReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_architecture_guardian()`에 위임). 이
        메서드가 Guardian의 핵심 진입점이다 — 평가만으로는 Guardian의
        목적("공표한다")을 완수하지 못한다.

        보장: `15 Project Intelligence/Architecture Guardian.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate()
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_architecture_guardian(markdown)
        return report, path


def render_markdown(report: ArchitectureHealthReport) -> str:
    """`ArchitectureHealthReport`를 Vault 문서 Markdown으로 렌더링한다.
    순수 함수(입출력 문자열 변환만, I/O 없음)."""
    status = "정상(위반 0건)" if report.all_passed else "위반 발견"
    lines = [
        "---",
        "tags: [architecture-guardian]",
        "type: architecture-guardian",
        "---",
        "",
        "# Architecture Guardian",
        "",
        "> Milestone 41(Architecture Guardian)이 `docs/ARCHITECTURE.md` "
        "§8이 정의한 규칙을 소스 트리에 대해 평가한 결과다(ADR-0056). "
        "Guardian은 규칙을 정의하지 않는다 — 이미 선언된 규칙을 평가하고 "
        "공표할 뿐이다. 매 생성 시 이 문서 전체가 덮어써진다.",
        "",
        f"## 전체 상태: {status}",
        "",
        "## 규칙별 결과",
        "",
    ]
    for result in report.results:
        icon = "✅" if result.passed else "❌"
        lines.append(f"### {icon} {result.rule_name}")
        lines.append("")
        if result.passed:
            lines.append("- 위반 없음")
        else:
            for violation in result.violations:
                lines.append(f"- `{violation.file}` — {violation.detail}")
        lines.append("")
    return "\n".join(lines)
