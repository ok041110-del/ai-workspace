from pathlib import Path

from ai_workspace.guardian.service import ArchitectureGuardianService, render_markdown
from ai_workspace.integration.vault_adapter import VaultAdapter

_REAL_SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_workspace"


def test_generate_evaluates_guardian_rules_against_real_source_tree(tmp_path: Path) -> None:
    service = ArchitectureGuardianService(VaultAdapter(tmp_path), _REAL_SRC_ROOT)

    report = service.generate()

    # 저장소 자체가 이미 모든 Guardian 규칙을 통과해야 한다(회귀 없음
    # 검증) — GUARDIAN_RULES는 기존 통과하던 규칙만 이전했다.
    assert report.all_passed is True
    assert len(report.results) > 0


def test_publish_writes_architecture_guardian_file(tmp_path: Path) -> None:
    service = ArchitectureGuardianService(VaultAdapter(tmp_path), _REAL_SRC_ROOT)

    report, path = service.publish()

    assert path == tmp_path / "15 Project Intelligence" / "Architecture Guardian.md"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Architecture Guardian" in content
    assert report.all_passed is True


def test_render_markdown_shows_status_for_passing_report() -> None:
    from ai_workspace.guardian.models import ArchitectureCheckResult, ArchitectureHealthReport

    report = ArchitectureHealthReport(
        results=(ArchitectureCheckResult(rule_name="r1", passed=True, violations=()),)
    )

    markdown = render_markdown(report)

    assert "정상(위반 0건)" in markdown
    assert "r1" in markdown
