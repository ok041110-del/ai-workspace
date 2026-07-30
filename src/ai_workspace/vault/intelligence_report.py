"""Milestone 29, T05: Project Intelligence 결과를 Vault에 노출.

`intelligence/`(Intelligence Layer)가 계산한 Snapshot/Health/Risk/
Recommendation을 Markdown 문자열로 이미 렌더링해 넘기면, 이 모듈은
그 문자열을 `15 Project Intelligence/Project Intelligence.md`에
원자적으로 덮어쓸 뿐이다 — Core Domain을 모르고(ADR-0035와 동일
원칙), Markdown 렌더링 로직도 갖지 않는다(그건 `intelligence/
report.py`의 책임).

기존 `VaultDocumentKind`(ADR/DECISION/TASK 등) 체계를 쓰지 않는다 —
이 문서는 AI/사용자가 직접 편집하는 원본이 아니라 매번 다시 계산해
덮어쓰는 **생성된 리포트**라서, Index append/Backlink 검증 같은
다른 kind의 관례가 적용되지 않는다(YAGNI, Simplicity First)."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text

_REPORT_PATH = ("15 Project Intelligence", "Project Intelligence.md")


def write_project_intelligence_report(vault_root: Path, markdown: str) -> Path:
    """`markdown`을 `15 Project Intelligence/Project Intelligence.md`에
    원자적으로 덮어쓴다.

    입력: vault_root, markdown(렌더링된 전체 문서 내용)
    출력: 실제로 쓰여진 파일의 절대 경로
    예외: 없음
    보장: 같은 vault_root에 다시 호출하면 파일 내용이 최신 markdown
          으로 완전히 교체된다(append 아님, side-effect는 이 파일
          하나로 한정).
    """
    path = vault_root.joinpath(*_REPORT_PATH)
    atomic_write_text(path, markdown)
    return path
