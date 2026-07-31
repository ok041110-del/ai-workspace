from ai_workspace.guardian.models import (
    ArchitectureCheckResult,
    ArchitectureHealthReport,
    ArchitectureViolation,
)


def test_all_passed_is_true_when_every_result_passed() -> None:
    report = ArchitectureHealthReport(
        results=(
            ArchitectureCheckResult(rule_name="a", passed=True, violations=()),
            ArchitectureCheckResult(rule_name="b", passed=True, violations=()),
        )
    )

    assert report.all_passed is True


def test_all_passed_is_false_when_any_result_failed() -> None:
    report = ArchitectureHealthReport(
        results=(
            ArchitectureCheckResult(rule_name="a", passed=True, violations=()),
            ArchitectureCheckResult(
                rule_name="b",
                passed=False,
                violations=(ArchitectureViolation(file="x.py", detail="imports y"),),
            ),
        )
    )

    assert report.all_passed is False


def test_all_passed_is_true_for_empty_report() -> None:
    assert ArchitectureHealthReport(results=()).all_passed is True
