import json
from pathlib import Path

from ai_workspace.observability.guardian_runtime_analyzer import GuardianRuntimeAnalyzer

_REPO_ROOT = Path(__file__).resolve().parents[2]


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
