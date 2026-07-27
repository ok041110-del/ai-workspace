"""ADR-0035 결정 2: Vault Directory Mapping — kind → 대상 Vault 파일."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.vault.models import VaultDocumentKind


@dataclass(frozen=True)
class VaultMappingEntry:
    relative_path: str
    mode: str  # "append" | "create"


VAULT_DIRECTORY_MAP: dict[VaultDocumentKind, VaultMappingEntry] = {
    VaultDocumentKind.ADR: VaultMappingEntry("03 ADR/ADR Index.md", "append"),
    VaultDocumentKind.DECISION: VaultMappingEntry("12 Decisions/Decisions Index.md", "append"),
    VaultDocumentKind.BACKEND: VaultMappingEntry("04 Backend/Backend Index.md", "append"),
    VaultDocumentKind.API: VaultMappingEntry("05 API/API Catalog.md", "append"),
    VaultDocumentKind.DASHBOARD: VaultMappingEntry("06 Dashboard/Dashboard Index.md", "append"),
    VaultDocumentKind.AUTOMATION: VaultMappingEntry("07 Automation/Automation Index.md", "append"),
    VaultDocumentKind.PRODUCTION: VaultMappingEntry("08 Production/Production Index.md", "append"),
    VaultDocumentKind.IOS: VaultMappingEntry("09 iOS/iOS Design.md", "append"),
    VaultDocumentKind.ANDROID: VaultMappingEntry("10 Android/Android Placeholder.md", "append"),
    VaultDocumentKind.MILESTONE: VaultMappingEntry("11 Milestones/Milestones Index.md", "append"),
    VaultDocumentKind.DAILY: VaultMappingEntry("13 Daily/{date}.md", "create"),
    VaultDocumentKind.ARCHITECTURE: VaultMappingEntry(
        "02 Architecture/Architecture Overview.md", "append"
    ),
}
