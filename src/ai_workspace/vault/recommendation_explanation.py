"""Milestone 44, T03: Recommendation Explanation 결과를 Vault에 노출.

`intelligence/recommendation_explanation_service.py`가 계산한
`RecommendationExplanationReport`를 Markdown 문자열로 이미 렌더링해
넘기면, 이 모듈은 그 문자열을 `15 Project Intelligence/Recommendation
Explanation.md`에 원자적으로 덮어쓸 뿐이다 —
`vault/experience_intelligence.py`(M40)와 같은 패턴이다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text

_REPORT_PATH = ("15 Project Intelligence", "Recommendation Explanation.md")


def write_recommendation_explanation_report(vault_root: Path, markdown: str) -> Path:
    """`markdown`을 `15 Project Intelligence/Recommendation
    Explanation.md`에 원자적으로 덮어쓴다.

    입력: vault_root, markdown(렌더링된 전체 문서 내용)
    출력: 실제로 쓰여진 파일의 절대 경로
    예외: 없음
    보장: 같은 vault_root에 다시 호출하면 파일 내용이 최신 markdown
          으로 완전히 교체된다(append 아님).
    """
    path = vault_root.joinpath(*_REPORT_PATH)
    atomic_write_text(path, markdown)
    return path
