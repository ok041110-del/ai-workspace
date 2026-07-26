from __future__ import annotations

import itertools

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)


class MockEngineAdapter(EngineAdapter):
    """실제 구현 엔진을 호출하지 않고 즉시 성공 결과를 반환하는 자리표시자
    EngineAdapter(T2-05). Milestone 3에서 실제 Claude Code 등 어댑터로
    교체될 때까지 Engine Runtime과 Agent의 연동을 검증하는 데 쓰인다."""

    def __init__(self, capabilities: frozenset[str] = frozenset({"code_generation"})) -> None:
        self._capabilities = capabilities
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        session_id = f"mock-session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output=f"{task.task_id} 완료(Mock)")

    def cancel(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return self._capabilities

    def supports_parallel(self) -> bool:
        return True

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)
