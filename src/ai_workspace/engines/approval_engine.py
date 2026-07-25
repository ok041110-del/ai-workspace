from __future__ import annotations

import itertools

from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalDecision,
    ApprovalEngine,
    ApprovalRequest,
    ApprovalRequestNotFoundError,
)


class InMemoryApprovalEngine(ApprovalEngine):
    """승인 대상 4대 행위(아키텍처 변경/신규 기능/리팩토링/Milestone 완료)를
    판별·차단하는 최소 구현체(RULES.md §1.4, ADR-0003, T2-03)."""

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._id_generator = itertools.count(1)

    def submit(self, action_type: ApprovalActionType, description: str) -> ApprovalRequest:
        request_id = f"approval-{next(self._id_generator)}"
        request = ApprovalRequest(
            request_id=request_id, action_type=action_type, description=description
        )
        self._requests[request_id] = request
        return request

    def decide(self, request_id: str, approved: bool) -> ApprovalRequest:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        if request.decision != ApprovalDecision.PENDING:
            raise ApprovalAlreadyDecidedError(request_id)
        request.decision = ApprovalDecision.APPROVED if approved else ApprovalDecision.REJECTED
        return request

    def is_approved(self, request_id: str) -> bool:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        return request.decision == ApprovalDecision.APPROVED
