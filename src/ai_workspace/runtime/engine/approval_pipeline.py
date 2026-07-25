from __future__ import annotations

import uuid

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalEngine,
    ApprovalRequest,
)
from ai_workspace.interfaces.engine_adapter import EngineResult
from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.event_bus import Event, EventBus


class UnapprovedTaskExecutionError(Exception):
    """승인되지 않았거나(PENDING/REJECTED) 이 Pipeline을 거치지 않은
    request_id로 run_approved()를 호출하면 발생한다."""


class EngineApprovalPipeline:
    """Engine Task 실행 전 사람 승인을 요구하는 조율자(M3-T05). 기존
    `ApprovalEngine`(T2-03)/`EngineRuntime`(M3-T01)/`EventBus`(T2-02)를
    그대로 조합할 뿐이며, 이 클래스 자체는 새 상태를 갖지 않는다 — 승인
    상태는 `ApprovalEngine`이, 실행 상태는 내부 `EngineRuntime`이 그대로
    소유한다(불필요한 추상화 지양). request_id → Task 매핑만
    run_approved() 호출에 필요한 최소 데이터로 보관한다."""

    def __init__(
        self, *, approval_engine: ApprovalEngine, engine_runtime: EngineRuntime, event_bus: EventBus
    ) -> None:
        self._approval_engine = approval_engine
        self._engine_runtime = engine_runtime
        self._event_bus = event_bus
        self._pending_tasks: dict[str, Task] = {}

    def request_approval(self, task: Task) -> ApprovalRequest:
        request = self._approval_engine.submit(
            ApprovalActionType.ENGINE_TASK_EXECUTION, task.title
        )
        self._pending_tasks[request.request_id] = task
        self._publish(
            "approval_requested",
            {"request_id": request.request_id, "task_id": task.task_id},
        )
        return request

    def decide(self, request_id: str, approved: bool) -> ApprovalRequest:
        request = self._approval_engine.decide(request_id, approved)
        self._publish(
            "approval_granted" if approved else "approval_rejected", {"request_id": request_id}
        )
        return request

    def run_approved(self, request_id: str) -> EngineResult:
        if request_id not in self._pending_tasks or not self._approval_engine.is_approved(
            request_id
        ):
            raise UnapprovedTaskExecutionError(request_id)
        task = self._pending_tasks.pop(request_id)
        return self._engine_runtime.run(task)

    def _publish(self, event_type: str, payload: dict[str, str]) -> None:
        self._event_bus.publish(
            Event(event_id=str(uuid.uuid4()), event_type=event_type, payload=payload)
        )
