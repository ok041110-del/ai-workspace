import pytest

from ai_workspace.engines.approval_engine import InMemoryApprovalEngine
from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalDecision,
    ApprovalRequestNotFoundError,
)


def test_submit_starts_as_pending() -> None:
    engine = InMemoryApprovalEngine()

    request = engine.submit(ApprovalActionType.NEW_FEATURE, "새 기능 추가")

    assert request.decision == ApprovalDecision.PENDING
    assert engine.is_approved(request.request_id) is False


def test_decide_approved_reflected_in_is_approved() -> None:
    engine = InMemoryApprovalEngine()
    request = engine.submit(ApprovalActionType.MILESTONE_COMPLETION, "Milestone 2 완료")

    engine.decide(request.request_id, approved=True)

    assert engine.is_approved(request.request_id) is True


def test_decide_rejected_keeps_is_approved_false() -> None:
    engine = InMemoryApprovalEngine()
    request = engine.submit(ApprovalActionType.ARCHITECTURE_CHANGE, "아키텍처 변경")

    engine.decide(request.request_id, approved=False)

    assert engine.is_approved(request.request_id) is False


def test_decide_twice_raises_already_decided() -> None:
    engine = InMemoryApprovalEngine()
    request = engine.submit(ApprovalActionType.REFACTORING, "리팩토링")
    engine.decide(request.request_id, approved=False)

    with pytest.raises(ApprovalAlreadyDecidedError):
        engine.decide(request.request_id, approved=True)


def test_unknown_request_raises_not_found() -> None:
    engine = InMemoryApprovalEngine()

    with pytest.raises(ApprovalRequestNotFoundError):
        engine.is_approved("unknown")


def test_approval_action_type_covers_exactly_four_gated_actions() -> None:
    """RULES.md §1.4의 승인 대상 4대 행위(아키텍처 변경/신규 기능/리팩토링/
    Milestone 완료)가 빠짐없이 판별·차단 가능함을 확인한다(T2-03 DoD)."""
    action_types = list(ApprovalActionType)

    assert len(action_types) == 4
    for action_type in action_types:
        engine = InMemoryApprovalEngine()
        request = engine.submit(action_type, f"{action_type.value} 승인 요청")

        assert engine.is_approved(request.request_id) is False

        engine.decide(request.request_id, approved=True)

        assert engine.is_approved(request.request_id) is True
