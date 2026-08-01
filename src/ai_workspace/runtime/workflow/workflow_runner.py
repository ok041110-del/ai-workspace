from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from ai_workspace.agents.events import MISSION_PLANNED
from ai_workspace.domain.task import TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.interfaces.task_engine import TaskEngine
from ai_workspace.interfaces.workflow_engine import WorkflowEngine


@dataclass
class WorkflowRunResult:
    completed_task_ids: list[str] = field(default_factory=list)
    failed_task_id: str | None = None

    @property
    def success(self) -> bool:
        return self.failed_task_id is None


class WorkflowRunner:
    """Workflow에 속한 여러 Task를 `WorkflowEngine.plan()`이 계산한
    순서대로 사람 개입 없이 순차 실행하는 조율자(Milestone 12).

    새 Agent가 아니다 — `AgentRuntime`/`AgentScheduler`를 전혀 사용하지
    않는다(Multi-Agent 선택/조정은 이번 범위 밖). `WorkflowEngine`(Core
    Engine)에 실행 책임을 넣지 않은 이유도 같다 — Core Engine이 EventBus
    에 의존하면 Agent → Core Engine 의존 방향(ARCHITECTURE.md §8)이
    뒤집힌다.

    `EventBus.publish()`는 계약상 예외를 던지지 않는다(구독자 예외는
    Bus 내부에서 격리됨, interfaces/event_bus.py 참고) — 따라서 실패
    감지는 오직 `TaskEngine.get_task(task_id).status`로만 한다. Task가
    `DONE`에 도달하지 못했다면(재작업 소진 등으로 파이프라인이 중간에
    멈춘 경우 포함) 그 자리에서 Workflow 실행을 중단한다.

    `workflow.task_ids`의 모든 Task는 호출 전에 이미 `TaskEngine.
    create_task()`로 생성되어 있어야 한다(전제 조건 — 이 클래스는 Task를
    새로 만들지 않는다).

    **Workflow Learning(Milestone 71, ADR-0089)**: `run()`이 끝나면 실제로
    쓰인 순서(`order`)와 성공 여부를 `WorkflowEngine.record_run_outcome()`
    으로 자동 기록한다 — 호출자가 별도로 학습을 챙기지 않아도 다음 `plan()`
    호출부터 반영된다."""

    def __init__(
        self, *, workflow_engine: WorkflowEngine, event_bus: EventBus, task_engine: TaskEngine
    ) -> None:
        self._workflow_engine = workflow_engine
        self._event_bus = event_bus
        self._task_engine = task_engine

    def run(self, workflow: Workflow) -> WorkflowRunResult:
        order = self._workflow_engine.plan(workflow)
        completed_task_ids: list[str] = []
        for task_id in order:
            self._publish_mission_planned(task_id)
            if self._task_engine.get_task(task_id).status != TaskStatus.DONE:
                self._workflow_engine.record_run_outcome(workflow, order, success=False)
                return WorkflowRunResult(
                    completed_task_ids=completed_task_ids, failed_task_id=task_id
                )
            completed_task_ids.append(task_id)
        self._workflow_engine.record_run_outcome(workflow, order, success=True)
        return WorkflowRunResult(completed_task_ids=completed_task_ids)

    def _publish_mission_planned(self, task_id: str) -> None:
        self._event_bus.publish(
            Event(
                event_id=str(uuid.uuid4()),
                event_type=MISSION_PLANNED,
                payload={"task_id": task_id},
            )
        )
