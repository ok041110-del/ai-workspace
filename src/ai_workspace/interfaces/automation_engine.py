from __future__ import annotations

from abc import ABC, abstractmethod


class DuplicateTriggerError(Exception):
    pass


class AutomationEngine(ABC):
    """조건/일정 기반 자동 트리거 등록 계약. 구체 구현체는 Milestone 2(T2-03)에서
    작성한다."""

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
