from ai_workspace.guardian.models import (
    GUARDIAN_BLOCK_REASON_PREFIX,
    ArchitectureCheckResult,
    ArchitectureHealthReport,
)
from ai_workspace.intelligence.recommendation_rules import (
    ACTION_CONTINUE_CURRENT_WORK,
    ACTION_START_NEXT_TASK,
    SOURCE_CURRENT_WORK,
    SOURCE_NEXT_TASK,
    NextAction,
)
from ai_workspace.runtime.execution.recommendation_execution_gate import ExecutionGate

_PASSING_GUARDIAN_REPORT = ArchitectureHealthReport(
    results=(ArchitectureCheckResult(rule_name="r1", passed=True, violations=()),)
)
_FAILING_GUARDIAN_REPORT = ArchitectureHealthReport(
    results=(ArchitectureCheckResult(rule_name="r1", passed=False, violations=()),)
)

_NEXT_TASK_ACTION = NextAction(
    source=SOURCE_NEXT_TASK, action=ACTION_START_NEXT_TASK, target="M36-T02", reason="r"
)
_CURRENT_WORK_ACTION = NextAction(
    source=SOURCE_CURRENT_WORK, action=ACTION_CONTINUE_CURRENT_WORK, target="M36-T01", reason="r"
)


def test_approves_next_task_with_manual_trigger() -> None:
    gate = ExecutionGate()

    decision = gate.check(_NEXT_TASK_ACTION, manual_trigger=True)

    assert decision.approved is True


def test_rejects_when_manual_trigger_is_false() -> None:
    gate = ExecutionGate()

    decision = gate.check(_NEXT_TASK_ACTION, manual_trigger=False)

    assert decision.approved is False
    assert "manual_trigger" in decision.reason


def test_rejects_when_next_action_is_none() -> None:
    gate = ExecutionGate()

    decision = gate.check(None, manual_trigger=True)

    assert decision.approved is False


def test_rejects_unsupported_source_as_not_supported() -> None:
    gate = ExecutionGate()

    decision = gate.check(_CURRENT_WORK_ACTION, manual_trigger=True)

    assert decision.approved is False
    assert "지원하지 않음" in decision.reason
    assert SOURCE_CURRENT_WORK in decision.reason


def test_approves_next_task_when_guardian_report_passes() -> None:
    gate = ExecutionGate()

    decision = gate.check(
        _NEXT_TASK_ACTION, manual_trigger=True, guardian_report=_PASSING_GUARDIAN_REPORT
    )

    assert decision.approved is True


def test_rejects_when_guardian_report_fails_even_with_manual_trigger_and_next_task() -> None:
    gate = ExecutionGate()

    decision = gate.check(
        _NEXT_TASK_ACTION, manual_trigger=True, guardian_report=_FAILING_GUARDIAN_REPORT
    )

    assert decision.approved is False
    assert decision.reason.startswith(GUARDIAN_BLOCK_REASON_PREFIX)
    assert "r1" in decision.reason


def test_guardian_violation_is_checked_before_manual_trigger() -> None:
    gate = ExecutionGate()

    decision = gate.check(
        _NEXT_TASK_ACTION, manual_trigger=False, guardian_report=_FAILING_GUARDIAN_REPORT
    )

    assert decision.approved is False
    assert decision.reason.startswith(GUARDIAN_BLOCK_REASON_PREFIX)
