"""M28-T03 DoD: Core Domain <-> vault 직접 의존성이 없는지, Integration
Layer만 양쪽을 참조하는지 소스 트리에서 직접 확인한다(ADR-0035/ADR-0039)."""

from __future__ import annotations

import ast
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_workspace"
_CORE_DOMAIN_PACKAGES = ("domain", "interfaces", "engines")


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_core_domain_does_not_import_vault() -> None:
    offenders = []
    for package in _CORE_DOMAIN_PACKAGES:
        for path in (_SRC_ROOT / package).rglob("*.py"):
            modules = _imported_modules(path)
            if any(module == "ai_workspace.vault" or module.startswith("ai_workspace.vault.")
                   for module in modules):
                offenders.append(path)
    assert offenders == []


def test_vault_does_not_import_core_domain() -> None:
    offenders = []
    for path in (_SRC_ROOT / "vault").rglob("*.py"):
        modules = _imported_modules(path)
        if any(
            module == f"ai_workspace.{package}" or module.startswith(f"ai_workspace.{package}.")
            for module in modules
            for package in _CORE_DOMAIN_PACKAGES
        ):
            offenders.append(path)
    assert offenders == []


def test_only_integration_layer_imports_both_sides() -> None:
    for path in _SRC_ROOT.rglob("*.py"):
        relative = path.relative_to(_SRC_ROOT)
        if relative.parts[0] == "integration":
            continue
        modules = _imported_modules(path)
        imports_vault = any(
            module == "ai_workspace.vault" or module.startswith("ai_workspace.vault.")
            for module in modules
        )
        imports_core_domain = any(
            module == f"ai_workspace.{package}" or module.startswith(f"ai_workspace.{package}.")
            for module in modules
            for package in _CORE_DOMAIN_PACKAGES
        )
        assert not (imports_vault and imports_core_domain), (
            f"{relative}가 vault와 Core Domain을 동시에 import합니다 — "
            "Integration Layer(integration/)만 양쪽을 참조할 수 있습니다."
        )
