"""M29-T02: Intelligence Layer 경계 검증(docs/ARCHITECTURE.md §8 규칙 21,
ADR-0043). `intelligence/`의 어떤 모듈도 `domain`/`interfaces`/
`engines`/`vault`를 직접 import하지 않는다 — `integration/`의
Adapter만 참조한다."""

from __future__ import annotations

import ast
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_workspace"
_INTELLIGENCE_DIR = _SRC_ROOT / "intelligence"
_FORBIDDEN_PACKAGES = ("domain", "interfaces", "engines", "vault")


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_intelligence_does_not_import_forbidden_packages() -> None:
    offenders: list[str] = []
    for path in _INTELLIGENCE_DIR.rglob("*.py"):
        modules = _imported_modules(path)
        for module in modules:
            if any(
                module == f"ai_workspace.{package}" or module.startswith(f"ai_workspace.{package}.")
                for package in _FORBIDDEN_PACKAGES
            ):
                offenders.append(f"{path.relative_to(_SRC_ROOT)} -> {module}")
    assert offenders == [], f"intelligence/가 금지된 패키지를 직접 import합니다: {offenders}"


def test_intelligence_only_depends_on_integration_adapters() -> None:
    allowed_prefixes = (
        "ai_workspace.integration.vault_adapter",
        "ai_workspace.integration.agent_adapter",
        "ai_workspace.integration.knowledge_adapter",
    )
    offenders: list[str] = []
    for path in _INTELLIGENCE_DIR.rglob("*.py"):
        modules = _imported_modules(path)
        for module in modules:
            if module.startswith("ai_workspace.integration.") and not module.startswith(
                allowed_prefixes
            ):
                offenders.append(f"{path.relative_to(_SRC_ROOT)} -> {module}")
    assert offenders == [], (
        f"intelligence/가 Adapter가 아닌 integration 모듈을 참조합니다: {offenders}"
    )
