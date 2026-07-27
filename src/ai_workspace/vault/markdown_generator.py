"""ADR-0035 Save Flow 2단계: Markdown Generator.

append 대상 kind(adr/decision/기타)는 `render_section()`으로 "## 제목" +
본문 튜플을 만든다 — 실제 파일 전체가 아니라 Vault Writer가 끼워 넣을
섹션 하나만 렌더링한다(File Strategy, 대상 섹션만 치환). create 대상인
daily만 `render_daily_file()`로 전체 파일을 만든다([[Template - Daily]]
형식)."""

from __future__ import annotations

from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest


class MissingVaultFieldError(ValueError):
    """kind별로 필요한 `request.fields` 값이 빠졌을 때 발생한다."""


def _require(request: VaultDocumentRequest, key: str) -> str:
    try:
        return request.fields[key]
    except KeyError as exc:
        raise MissingVaultFieldError(
            f"{request.kind.value} 렌더링에 '{key}' 필드가 필요합니다"
        ) from exc


def _render_related_docs(related_docs: tuple[str, ...]) -> str:
    if not related_docs:
        return ""
    links = " ".join(f"[[{doc}]]" for doc in related_docs)
    return f"\n관련: {links}\n"


def render_section(request: VaultDocumentRequest) -> tuple[str, str]:
    """(heading, body)를 돌려준다. heading은 "## " 없이 텍스트만 담는다
    (Vault Writer가 섹션 경계를 식별하는 데 이 값을 그대로 쓴다)."""
    if request.kind is VaultDocumentKind.ADR:
        heading = f"ADR-{_require(request, 'number')}: {request.title}"
        body = (
            f"- 목적: {_require(request, 'purpose')}\n"
            f"- 결정: {_require(request, 'decision')}\n"
            f"- 영향: {_require(request, 'impact')}\n"
        )
        return heading, body

    if request.kind is VaultDocumentKind.DECISION:
        heading = request.title
        body = (
            f"- Status: {_require(request, 'status')}\n"
            f"- 질문: {_require(request, 'question')}\n"
            f"- 답: {_require(request, 'answer')}\n"
        )
        return heading, body

    # 나머지 append 대상 kind(backend/api/dashboard/automation/
    # production/ios/android/milestone/architecture)는 공통 Summary
    # 형식(제목 + 요약 + 관련 문서)을 쓴다. kind별 전용 형식이 실제로
    # 필요해지면 그때 위처럼 분기를 추가한다(YAGNI).
    heading = request.title
    body = f"{request.summary}\n" + _render_related_docs(request.related_docs)
    return heading, body


def render_daily_file(date: str) -> str:
    """[[Template - Daily]] 형식 그대로 전체 파일 내용을 만든다."""
    return (
        "---\n"
        "tags: [daily]\n"
        "---\n"
        "\n"
        f"# {date}\n"
        "\n"
        "## 오늘 작업\n"
        "\n"
        "-\n"
        "\n"
        "## 오늘 결정\n"
        "\n"
        "-\n"
        "\n"
        "## 발견한 문제\n"
        "\n"
        "-\n"
        "\n"
        "## 내일 계획\n"
        "\n"
        "-\n"
        "\n"
        "## 관련 문서\n"
        "\n"
        "- [[Overview]]\n"
    )
