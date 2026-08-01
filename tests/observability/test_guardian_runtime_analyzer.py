import json
from pathlib import Path

from ai_workspace.observability.guardian_runtime_analyzer import GuardianRuntimeAnalyzer
from ai_workspace.observability.snapshot import AutomationGateStatus

_REPO_ROOT = Path(__file__).resolve().parents[2]
_EXECUTION_REPORT_DIR = "15 Project Intelligence"
_EXECUTION_REPORT_NAME = "Recommendation Execution.md"


def test_analyze_reads_real_guardian_status() -> None:
    info = GuardianRuntimeAnalyzer().analyze(_REPO_ROOT)

    assert info.guardian_all_passed is True


def test_analyze_returns_none_when_src_missing(tmp_path: Path) -> None:
    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.guardian_all_passed is None
    assert info.pytest_failed_count is None
    assert info.ruff_status is None
    assert info.mypy_status is None
    assert info.coverage_percentage is None
    assert info.last_automation_gate_status is AutomationGateStatus.UNKNOWN
    assert info.last_automation_gate_reason is None


def test_analyze_reports_unknown_gate_status_when_execution_report_missing(
    tmp_path: Path,
) -> None:
    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.last_automation_gate_status is AutomationGateStatus.UNKNOWN
    assert info.last_automation_gate_reason is None


def test_analyze_reports_blocked_gate_status_when_execution_report_has_guardian_reason(
    tmp_path: Path,
) -> None:
    report_dir = tmp_path / _EXECUTION_REPORT_DIR
    report_dir.mkdir(parents=True)
    (report_dir / _EXECUTION_REPORT_NAME).write_text(
        "## Gate 판정\n\n"
        "- 승인 여부: 거부\n"
        "- 이유: Architecture Guardian 위반으로 실행 차단: some_rule\n",
        encoding="utf-8",
    )

    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.last_automation_gate_status is AutomationGateStatus.BLOCKED
    assert info.last_automation_gate_reason is not None
    assert "some_rule" in info.last_automation_gate_reason


def test_analyze_reports_pass_gate_status_when_execution_report_has_no_guardian_reason(
    tmp_path: Path,
) -> None:
    report_dir = tmp_path / _EXECUTION_REPORT_DIR
    report_dir.mkdir(parents=True)
    (report_dir / _EXECUTION_REPORT_NAME).write_text(
        "## Gate 판정\n\n- 승인 여부: 승인\n- 이유: 실행 승인\n", encoding="utf-8"
    )

    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.last_automation_gate_status is AutomationGateStatus.PASS
    assert info.last_automation_gate_reason is None


def test_analyze_reads_pytest_lastfailed_cache(tmp_path: Path) -> None:
    cache_dir = tmp_path / ".pytest_cache" / "v" / "cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "lastfailed").write_text(
        json.dumps({"tests/test_a.py::test_one": True}), encoding="utf-8"
    )

    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.pytest_failed_count == 1


def test_analyze_reads_pytest_lastfailed_empty_means_zero_failures(tmp_path: Path) -> None:
    cache_dir = tmp_path / ".pytest_cache" / "v" / "cache"
    cache_dir.mkdir(parents=True)
    (cache_dir / "lastfailed").write_text("{}", encoding="utf-8")

    info = GuardianRuntimeAnalyzer().analyze(tmp_path)

    assert info.pytest_failed_count == 0
