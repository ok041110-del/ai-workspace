from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.domain.engine_selection import EngineSelectionDecision


@dataclass(frozen=True)
class AgentProposal:
    """Multi-Agent Negotiation(Milestone 84)에서 개별 Agent가 실행 전
    단계에서 제시하는 선호안. `NegotiationCoordinator.negotiate()`의
    입력으로만 쓰이며, 이 값 자체는 실행에 아무 영향을 주지 않는다
    (`EngineSelectionDecision`/`EngineRecommendation`이 이미 확립한
    "Decision Only" 원칙과 동일). `NegotiationCoordinator`는 Agent
    인스턴스를 직접 알지 못한다 — 호출자가 각 Agent의 선호를 이 값으로
    조립해 전달한다(결합 최소화, ADR-0080/0081 원칙과 동일).

    `priority`는 `Agent.priority`(Milestone 57, ADR-0075)와 같은 의미
    (낮을수록 우선)이며, 다수결이 동률일 때만 tie-break에 쓰인다.
    `preferred_workflow_order`를 생략하면(기본값 `None`) 이 Agent는
    Workflow 순서에 대한 의견이 없다는 뜻이다 — 아무도 의견을 내지
    않으면 협상은 그 부분을 건너뛰고 기존 `WorkflowEngine.plan()` 결과를
    그대로 쓴다(충돌이 아니므로 fallback 대상이 아니다)."""

    agent_id: str
    engine_name: str
    model: str | None = None
    priority: int = 0
    preferred_workflow_order: tuple[str, ...] | None = None


@dataclass(frozen=True)
class NegotiatedPlan:
    """`NegotiationCoordinator.negotiate()`의 결과. `decision`은 새 반환
    타입을 만들지 않기 위해 기존 `EngineSelectionDecision`(M17)을 그대로
    재사용하고, 협상 고유의 필드(`workflow_order`/`consensus_reached`)만
    감싼다.

    `consensus_reached`가 `False`면 `decision`/`workflow_order` 모두
    협상 결과가 아니라 기존 단독 의사결정(`EngineRuntime.decide_engine()`/
    `WorkflowEngine.plan()`)으로 즉시 fallback한 값이다 — 호출자는 이
    필드만 보고 실제로 합의가 있었는지 알 수 있다."""

    decision: EngineSelectionDecision
    workflow_order: list[str] | None
    consensus_reached: bool
    reason: str
