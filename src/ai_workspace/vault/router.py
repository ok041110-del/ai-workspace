"""ADR-0035 Save Flow 1단계: Document Router."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path

from ai_workspace.vault.mapping import VAULT_DIRECTORY_MAP
from ai_workspace.vault.markdown_generator import MissingVaultFieldError
from ai_workspace.vault.models import VaultDocumentKind, VaultDocumentRequest


class UnroutableVaultKindError(ValueError):
    """Vault Directory Mapping에 없는 kind가 들어왔을 때 발생한다."""


@dataclass(frozen=True)
class VaultTarget:
    path: Path
    mode: str


class DocumentRouter:
    """`VaultDocumentRequest.kind`를 Vault Directory Mapping으로 해석해
    실제 파일 경로와 저장 방식(append/create)을 결정한다."""

    def __init__(self, vault_root: Path) -> None:
        self._vault_root = vault_root

    def resolve(self, request: VaultDocumentRequest) -> VaultTarget:
        entry = VAULT_DIRECTORY_MAP.get(request.kind)
        if entry is None:
            raise UnroutableVaultKindError(f"매핑되지 않은 kind입니다: {request.kind}")

        relative_path = entry.relative_path
        if request.kind is VaultDocumentKind.DAILY:
            day = request.date or date_cls.today().isoformat()
            relative_path = relative_path.format(date=day)
        elif request.kind is VaultDocumentKind.TASK:
            try:
                task_id = request.fields["task_id"]
            except KeyError as exc:
                raise MissingVaultFieldError(
                    "task 라우팅에 'task_id' 필드가 필요합니다"
                ) from exc
            relative_path = relative_path.format(task_id=task_id)

        return VaultTarget(path=self._vault_root / relative_path, mode=entry.mode)
