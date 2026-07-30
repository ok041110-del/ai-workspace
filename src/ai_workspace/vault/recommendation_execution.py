"""Milestone 36, T04: Recommendation Execution 결과를 Vault에 노출.

`runtime/execution/recommendation_execution_service.py`(Recommendation
Execution Service)가 계산한 `RecommendationExecutionOutcome`을
Markdown 문자열로 이미 렌더링해 넘기면, 이 모듈은 그 문자열을 `15
Project Intelligence/Recommendation Execution.md`에 원자적으로
덮어쓸 뿐이다 — `vault/recommendation_intelligence.py`(M35-T04)와
같은 패턴이다. Core Domain을 모르고 Markdown 렌더링 로직도 갖지
않는다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.atomic import atomic_write_text

_REPORT_PATH = ("15 Project Intelligence", "Recommendation Execution.md")


def write_recommendation_execution_report(vault_root: Path, markdown: str) -> Path:
    """`markdown`을 `15 Project Intelligence/Recommendation
    Execution.md`에 원자적으로 덮어쓴다.

    입력: vault_root, markdown(렌더링된 전체 문서 내용)
    출력: 실제로 쓰여진 파일의 절대 경로
    예외: 없음
    보장: 같은 vault_root에 다시 호출하면 파일 내용이 최신 markdown
          으로 완전히 교체된다(append 아님).
    """
    path = vault_root.joinpath(*_REPORT_PATH)
    atomic_write_text(path, markdown)
    return path
