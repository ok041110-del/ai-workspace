from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)
from ai_workspace.runtime.dashboard.dashboard_service import DashboardSnapshot
from ai_workspace.web.dashboard_viewmodel import (
    build_dashboard_view_model,
    build_engine_view_models,
    build_history_view_models,
    build_workspace_view_model,
)


def test_workspace_view_model_translates_status_to_korean() -> None:
    status = WorkspaceStatus(
        project_name="AI Workspace",
        current_task_title="구현하기",
        status="running",
        started_at="2026-07-27T10:00:00Z",
    )

    view_model = build_workspace_view_model(status)

    assert view_model.status_label == "실행 중"
    assert view_model.started_at == "2026-07-27T10:00:00Z"


def test_workspace_view_model_idle_status() -> None:
    status = WorkspaceStatus(
        project_name=None, current_task_title=None, status="idle", started_at=None
    )

    view_model = build_workspace_view_model(status)

    assert view_model.status_label == "대기 중"


def test_engine_view_models_keep_english_name_and_korean_status() -> None:
    view_models = build_engine_view_models(
        {"claude_code": EngineStatus.RUNNING, "codex_cli": EngineStatus.AUTH_REQUIRED}
    )

    by_name = {vm.name: vm.status_label for vm in view_models}
    assert by_name["Claude Code"] == "실행 중"
    assert by_name["Codex CLI"] == "인증 필요"


def test_history_view_model_labels_success_failure_cancelled_timed_out() -> None:
    records = [
        ExecutionRecord("t1", "claude_code", True, False, False, 0, None),
        ExecutionRecord("t2", "claude_code", False, False, False, 0, "boom"),
        ExecutionRecord("t3", "gemini_cli", False, True, False, 0, "cancelled"),
        ExecutionRecord("t4", "claude_code", False, False, True, 2, "timeout"),
    ]

    view_models = build_history_view_models(records)

    assert [vm.result_label for vm in view_models] == ["성공", "실패", "취소", "시간 초과"]
    assert view_models[2].engine == "Gemini CLI"


def test_build_dashboard_view_model_combines_all_areas() -> None:
    snapshot = DashboardSnapshot(
        workspace_status=WorkspaceStatus(None, None, "idle", None),
        engine_statuses={"claude_code": EngineStatus.READY},
        execution_stats=ExecutionStats(total=1, success=1, failure=0, cancelled=0, timed_out=0),
        recent_executions=[ExecutionRecord("t1", "claude_code", True, False, False, 0, None)],
        reliability_stats=ReliabilityStats(0, 0, 0, 0),
    )

    view_model = build_dashboard_view_model(snapshot)

    assert view_model.workspace.status_label == "대기 중"
    assert view_model.engines[0].name == "Claude Code"
    assert view_model.execution_stats.total == 1
    assert view_model.recent_history[0].result_label == "성공"
    assert view_model.reliability_stats.retry_count == 0
