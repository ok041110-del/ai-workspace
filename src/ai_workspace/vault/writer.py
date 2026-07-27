"""ADR-0035 Save Flow 3단계: Vault Writer (File Creator + File Updater).

File Strategy(ADR-0035 결정 4)를 그대로 구현한다 — 신규 문서는 전체
생성하고, 기존 Index 문서는 대상 섹션만 치환하거나 말미(관련 문서
절 앞)에 추가한다. 실제 내용이 바뀔 때만 파일을 쓴다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.sync import VaultConflictError, content_hash

_RELATED_DOCS_HEADING = "## 관련 문서"


class VaultWriter:
    def create_file(self, path: Path, content: str) -> bool:
        """새 파일을 만든다. 이미 존재하면 아무것도 하지 않고 False를
        돌려준다 — 덮어쓰지 않는다."""
        if path.exists():
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True

    def upsert_section(
        self, path: Path, heading: str, body: str, *, expected_hash: str | None = None
    ) -> bool:
        """`path` 안에서 "## {heading}" 섹션을 찾아 있으면 본문을 교체하고,
        없으면 "## 관련 문서" 절 바로 앞에 새 섹션을 추가한다. 내용이 실제로
        바뀔 때만 파일을 쓰고 True를 돌려준다.

        `expected_hash`(`sync.content_hash()`로 미리 읽어 둔 값)를 주면,
        그 사이 다른 경로로 파일이 바뀌었을 때 조용히 덮어쓰는 대신
        `VaultConflictError`를 낸다(Conflict Handling, M23-T05)."""
        if expected_hash is not None and content_hash(path) != expected_hash:
            raise VaultConflictError(f"저장 시점 사이에 파일이 변경되었습니다: {path}")

        original = path.read_text(encoding="utf-8")
        updated = _upsert_section_text(original, heading, body)
        if updated == original:
            return False
        path.write_text(updated, encoding="utf-8")
        return True


def _upsert_section_text(content: str, heading: str, body: str) -> str:
    heading_line = f"## {heading}"
    section_lines = [heading_line, "", *body.rstrip("\n").split("\n"), ""]
    lines = content.split("\n")

    start = _find_heading_line(lines, heading_line)
    if start is not None:
        end = _find_section_end(lines, start)
        return "\n".join(lines[:start] + section_lines + lines[end:])

    insert_at = _find_heading_line(lines, _RELATED_DOCS_HEADING)
    if insert_at is not None:
        return "\n".join(lines[:insert_at] + section_lines + lines[insert_at:])

    return content.rstrip("\n") + "\n\n" + "\n".join(section_lines)


def _find_heading_line(lines: list[str], heading_line: str) -> int | None:
    for i, line in enumerate(lines):
        if line == heading_line:
            return i
    return None


def _find_section_end(lines: list[str], start: int) -> int:
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            return i
    return len(lines)
