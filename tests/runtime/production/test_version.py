from ai_workspace.runtime.production.version import (
    WORKSPACE_VERSION,
    get_git_commit_hash,
    get_version_info,
)


def test_workspace_version_is_a_nonempty_string() -> None:
    assert isinstance(WORKSPACE_VERSION, str)
    assert WORKSPACE_VERSION


def test_get_git_commit_hash_returns_none_for_missing_repo(tmp_path) -> None:
    assert get_git_commit_hash(cwd=tmp_path) is None


def test_get_version_info_always_includes_version() -> None:
    info = get_version_info(repo_path="/nonexistent/path")

    assert info.version == WORKSPACE_VERSION
    assert info.commit_hash is None
