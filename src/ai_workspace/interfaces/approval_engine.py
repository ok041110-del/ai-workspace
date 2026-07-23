from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class ApprovalActionType(Enum):
    ARCHITECTURE_CHANGE = "architecture_change"
    NEW_FEATURE = "new_feature"
    REFACTORING = "refactoring"
    PHASE_COMPLETION = "phase_completion"


class ApprovalDecision(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ApprovalRequest:
    request_id: str
    action_type: ApprovalActionType
    description: str
    decision: ApprovalDecision = ApprovalDecision.PENDING


class ApprovalRequestNotFoundError(Exception):
    pass


class ApprovalAlreadyDecidedError(Exception):
    pass


class ApprovalEngine(ABC):
    """승인 대상 행위(아키텍처 변경/신규 기능/리팩토링/Phase 완료) 판별·차단 계약.
    구체 구현체는 Phase 2에서 작성한다."""

    @abstractmethod
    def submit(self, action_type: ApprovalActionType, description: str) -> ApprovalRequest:
        """
        입력: action_type(4가지 중 하나), description
        출력: decision이 PENDING인 새 ApprovalRequest
        예외: 없음
        보장: 반환된 request_id는 유일하며, decide()가 호출되기 전까지 decision은
              PENDING을 유지한다.
        """
        raise NotImplementedError

    @abstractmethod
    def decide(self, request_id: str, approved: bool) -> ApprovalRequest:
        """
        입력: request_id, approved(승인 여부)
        출력: decision이 APPROVED 또는 REJECTED로 갱신된 ApprovalRequest
        예외: request_id가 없으면 ApprovalRequestNotFoundError.
              이미 PENDING이 아닌 요청이면 ApprovalAlreadyDecidedError
              (한 번 결정된 요청은 다시 바꿀 수 없다).
        보장: 이 메서드가 성공적으로 반환되면 이후 is_approved(request_id)는
              이번 결정을 그대로 반영한다.
        """
        raise NotImplementedError

    @abstractmethod
    def is_approved(self, request_id: str) -> bool:
        """
        입력: request_id
        출력: decision == APPROVED이면 True, 그 외(PENDING/REJECTED)는 False
        예외: request_id가 없으면 ApprovalRequestNotFoundError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError
