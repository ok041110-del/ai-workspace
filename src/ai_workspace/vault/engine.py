"""ADR-0035 Save Flow 전체를 잇는 진입점: Document Router → Markdown
Generator → Vault Writer. Auto Save Workflow(M23-T04)가 이 클래스 하나만
호출하면 되도록 한다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.vault.markdown_generator import render_daily_file, render_section
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest
from ai_workspace.vault.router import DocumentRouter
from ai_workspace.vault.writer import VaultWriter


class VaultSaveEngine:
    def __init__(self, vault_root: Path) -> None:
        self._router = DocumentRouter(vault_root)
        self._writer = VaultWriter()

    def save(self, request: VaultDocumentRequest) -> bool:
        """`request`를 Vault에 저장한다. 실제로 파일이 바뀌었으면 True."""
        target = self._router.resolve(request)

        if target.mode == "create":
            if request.kind is VaultDocumentKind.DAILY:
                day = request.date or target.path.stem
                content = render_daily_file(day)
            else:
                heading, body = render_section(request)
                content = f"# {heading}\n\n{body}"
            return self._writer.create_file(target.path, content)

        heading, body = render_section(request)
        return self._writer.upsert_section(target.path, heading, body)
