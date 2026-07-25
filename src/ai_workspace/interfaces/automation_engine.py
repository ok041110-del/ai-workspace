from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.workflow import Workflow


class DuplicateTriggerError(Exception):
    pass


class TriggerNotFoundError(Exception):
    """등록되지 않은 trigger_id에 Workflow를 연결하거나 발동하려 할 때
    발생한다."""


class TriggerNotBoundError(Exception):
    """Workflow가 아직 연결되지 않은 trigger_id를 발동(fire)하려 할 때
    발생한다."""


class AutomationEngine(ABC):
    """조건/일정 기반 자동 트리거 등록 계약. 구체 구현체는 Milestone 2(T2-03),
    Workflow 연결·발동(M4-T07)은 Milestone 4에서 확장한다.

    **책임 경계(M4-T07)**: AutomationEngine은 "어떤 trigger가 어떤 Workflow와
    연결되어 있는가"만 관리한다(연결 관리). trigger가 **언제** 발동되어야
    하는지 판단하는 조건/일정 평가는 호출자(향후 Scheduler/Cron 등)의
    책임이며, 발동된 Workflow를 **실제로 실행**하는 것도 호출자가
    `WorkflowEngine`을 통해 직접 수행한다 — AutomationEngine은
    `WorkflowEngine`에 의존하지 않는다."""

    @abstractmethod
    def register_trigger(self, trigger_id: str, description: str) -> None:
        """
        입력: trigger_id(저장소 내에서 유일해야 함), description
        출력: 없음
        예외: 이미 등록된 trigger_id면 DuplicateTriggerError
        보장: 등록 성공 시 이후 list_triggers()의 결과에 trigger_id가 포함된다.
        """
        raise NotImplementedError

    @abstractmethod
    def list_triggers(self) -> list[str]:
        """
        입력: 없음
        출력: 등록된 trigger_id 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 내부 상태는 변하지 않는다
              (방어적 복사).
        """
        raise NotImplementedError

    @abstractmethod
    def bind_workflow(self, trigger_id: str, workflow: Workflow) -> None:
        """
        입력: trigger_id(register_trigger로 등록되어 있어야 함), workflow
              (발동 시 반환할 Workflow)
        출력: 없음
        예외: 등록되지 않은 trigger_id면 TriggerNotFoundError
        보장: bind_workflow(trigger_id, workflow) 이후 fire(trigger_id)는
              동일한 workflow를 반환한다(다시 연결하면 최신 workflow로
              덮어쓴다).
        """
        raise NotImplementedError

    @abstractmethod
    def fire(self, trigger_id: str) -> Workflow:
        """
        입력: trigger_id
        출력: 연결된 Workflow(실행은 호출자 책임 — 이 메서드는 실행하지
              않는다)
        예외: 등록되지 않은 trigger_id면 TriggerNotFoundError. Workflow가
              연결되지 않았으면 TriggerNotBoundError.
        보장: side-effect 없음(read-only) — Workflow를 실행하거나 상태를
              바꾸지 않는다.
        """
        raise NotImplementedError
