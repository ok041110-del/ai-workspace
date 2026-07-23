import pytest

from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalDecision,
    ApprovalRequestNotFoundError,
)

from .fakes import FakeApprovalEngine


def test_submit_starts_as_pending() -> None:
    engine = FakeApprovalEngine()

    request = engine.submit(ApprovalActionType.NEW_FEATURE, "새 기능 추가")

    assert request.decision == ApprovalDecision.PENDING
    assert engine.is_approved(request.request_id) is False


def test_decide_approved_reflected_in_is_approved() -> None:
    engine = FakeApprovalEngine()
    request = engine.submit(ApprovalActionType.PHASE_COMPLETION, "Phase 1 완료")

    engine.decide(request.request_id, approved=True)

    assert engine.is_approved(request.request_id) is True


def test_decide_twice_raises_already_decided() -> None:
    engine = FakeApprovalEngine()
    request = engine.submit(ApprovalActionType.REFACTORING, "리팩토링")
    engine.decide(request.request_id, approved=False)

    with pytest.raises(ApprovalAlreadyDecidedError):
        engine.decide(request.request_id, approved=True)


def test_unknown_request_raises_not_found() -> None:
    engine = FakeApprovalEngine()

    with pytest.raises(ApprovalRequestNotFoundError):
        engine.is_approved("unknown")
