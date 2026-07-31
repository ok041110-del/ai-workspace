from pathlib import Path

from ai_workspace.guardian.checker import evaluate
from ai_workspace.guardian.rules import (
    AllowedImportPrefixRule,
    ForbiddenPackageImportRule,
    ServiceRoleGatedImportRule,
)


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_forbidden_package_import_rule_passes_when_no_violation(tmp_path: Path) -> None:
    _write(tmp_path, "domain/task.py", "x = 1\n")
    rule = ForbiddenPackageImportRule(
        name="r1", source_packages=("domain",), forbidden_packages=("vault",)
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is True
    assert report.results[0].violations == ()


def test_forbidden_package_import_rule_detects_violation(tmp_path: Path) -> None:
    _write(tmp_path, "domain/task.py", "from ai_workspace.vault.atomic import atomic_write_text\n")
    rule = ForbiddenPackageImportRule(
        name="r1", source_packages=("domain",), forbidden_packages=("vault",)
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is False
    result = report.results[0]
    assert result.rule_name == "r1"
    assert len(result.violations) == 1
    assert result.violations[0].file == "domain/task.py"


def test_allowed_import_prefix_rule_allows_whitelisted_prefix(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "intelligence/report.py",
        "from ai_workspace.integration.vault_adapter import VaultAdapter\n",
    )
    rule = AllowedImportPrefixRule(
        name="r2",
        source_packages=("intelligence",),
        restricted_package="ai_workspace.integration",
        allowed_prefixes=("ai_workspace.integration.vault_adapter",),
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is True


def test_allowed_import_prefix_rule_rejects_non_whitelisted_prefix(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "intelligence/foo.py",
        "from ai_workspace.integration.workflow_task_link import Something\n",
    )
    rule = AllowedImportPrefixRule(
        name="r2",
        source_packages=("intelligence",),
        restricted_package="ai_workspace.integration",
        allowed_prefixes=("ai_workspace.integration.vault_adapter",),
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is False
    assert "ai_workspace.integration.workflow_task_link" in report.results[0].violations[0].detail


def test_service_role_gated_import_rule_allows_service_module(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "intelligence/foo_service.py",
        "from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore\n\n"
        "class FooService:\n    pass\n",
    )
    rule = ServiceRoleGatedImportRule(
        name="r3", source_packages=("intelligence",), gated_package="ai_workspace.memory"
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is True


def test_service_role_gated_import_rule_rejects_non_service_module(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "intelligence/foo_rules.py",
        "from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore\n\n"
        "class FooAnalyzer:\n    pass\n",
    )
    rule = ServiceRoleGatedImportRule(
        name="r3", source_packages=("intelligence",), gated_package="ai_workspace.memory"
    )

    report = evaluate([rule], tmp_path)

    assert report.all_passed is False
    assert report.results[0].violations[0].file == "intelligence/foo_rules.py"


def test_evaluate_returns_one_result_per_rule_in_order(tmp_path: Path) -> None:
    _write(tmp_path, "domain/task.py", "x = 1\n")
    rule_a = ForbiddenPackageImportRule(
        name="a", source_packages=("domain",), forbidden_packages=("vault",)
    )
    rule_b = ForbiddenPackageImportRule(
        name="b", source_packages=("domain",), forbidden_packages=("engines",)
    )

    report = evaluate([rule_a, rule_b], tmp_path)

    assert [result.rule_name for result in report.results] == ["a", "b"]
