"""M28-T03 DoD: Core Domain <-> vault 직접 의존성이 없는지, Integration
Layer만 양쪽을 참조하는지 소스 트리에서 직접 확인한다(ADR-0035/ADR-0039).

처음 두 검사(Core Domain↔vault 개별 금지)는 Milestone 41(Architecture
Guardian, ADR-0056)에서 `guardian/rules.py`의 `GUARDIAN_RULES`로
이전됐다 — 여기서는 그 결과를 `assert`만 한다(평가 로직은 `guardian/
checker.py`). 세 번째 검사("Integration Layer만 양쪽을 동시에
참조할 수 있다")는 Guardian의 3개 Rule 형태로 자연스럽게 표현되지
않아(무리한 일반화를 피하기 위해, 사용자 조건) 이전하지 않고 기존
방식 그대로 유지한다."""

from __future__ import annotations

import ast
from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.rules import GUARDIAN_RULES

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
    rules = [rule for rule in GUARDIAN_RULES if rule.name == "core_domain_does_not_import_vault"]
    report = evaluate(rules, _SRC_ROOT)
    result = report.results[0]
    assert result.passed, result.violations


def test_vault_does_not_import_core_domain() -> None:
    rules = [rule for rule in GUARDIAN_RULES if rule.name == "vault_does_not_import_core_domain"]
    report = evaluate(rules, _SRC_ROOT)
    result = report.results[0]
    assert result.passed, result.violations


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
