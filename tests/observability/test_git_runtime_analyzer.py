import subprocess
from pathlib import Path

from ai_workspace.observability.git_runtime_analyzer import GitRuntimeAnalyzer


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial commit"], cwd=path, check=True)


def test_analyze_returns_none_fields_when_not_a_git_repo(tmp_path: Path) -> None:
    info = GitRuntimeAnalyzer().analyze(tmp_path)

    assert info.current_branch is None
    assert info.working_tree_dirty is None
    assert info.ahead is None
    assert info.behind is None
    assert info.last_commit_summary is None


def test_analyze_reads_branch_and_clean_tree(tmp_path: Path) -> None:
    _init_repo(tmp_path)

    info = GitRuntimeAnalyzer().analyze(tmp_path)

    assert info.current_branch is not None
    assert info.working_tree_dirty is False
    assert info.last_commit_summary is not None
    assert "initial commit" in info.last_commit_summary


def test_analyze_detects_dirty_working_tree(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    (tmp_path / "README.md").write_text("changed\n", encoding="utf-8")

    info = GitRuntimeAnalyzer().analyze(tmp_path)

    assert info.working_tree_dirty is True


def test_analyze_returns_none_ahead_behind_without_upstream(tmp_path: Path) -> None:
    _init_repo(tmp_path)

    info = GitRuntimeAnalyzer().analyze(tmp_path)

    assert info.ahead is None
    assert info.behind is None
