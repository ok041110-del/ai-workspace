import pytest

from ai_workspace.vault.markdown_generator import (
    MissingVaultFieldError,
    render_daily_file,
    render_section,
)
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest


def test_render_section_adr_uses_purpose_decision_impact() -> None:
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR,
        title="Vault Integration Layer 도입",
        summary="",
        fields={"number": "0035", "purpose": "목적", "decision": "결정", "impact": "영향"},
    )

    heading, body = render_section(request)

    assert heading == "ADR-0035: Vault Integration Layer 도입"
    assert "- 목적: 목적" in body
    assert "- 결정: 결정" in body
    assert "- 영향: 영향" in body


def test_render_section_adr_missing_field_raises() -> None:
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.ADR, title="X", summary="", fields={"number": "1"}
    )

    with pytest.raises(MissingVaultFieldError):
        render_section(request)


def test_render_section_decision_uses_status_question_answer() -> None:
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.DECISION,
        title="왜 X인가",
        summary="",
        fields={"status": "확정", "question": "질문", "answer": "답"},
    )

    heading, body = render_section(request)

    assert heading == "왜 X인가"
    assert "- Status: 확정" in body
    assert "- 질문: 질문" in body
    assert "- 답: 답" in body


def test_render_section_generic_kind_includes_summary_and_related_docs() -> None:
    request = VaultDocumentRequest(
        kind=VaultDocumentKind.BACKEND,
        title="새 컴포넌트",
        summary="한 줄 요약",
        related_docs=("Architecture Overview",),
    )

    heading, body = render_section(request)

    assert heading == "새 컴포넌트"
    assert "한 줄 요약" in body
    assert "[[Architecture Overview]]" in body


def test_render_daily_file_matches_template_daily_structure() -> None:
    content = render_daily_file("2026-07-27")

    assert content.startswith("---\ntags: [daily]\n---\n")
    assert "# 2026-07-27" in content
    assert "## 오늘 작업" in content
    assert "## 관련 문서" in content
    assert "[[Overview]]" in content
