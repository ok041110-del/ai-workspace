from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.automation import AutomationRule


class AutomationRuleNotFoundError(Exception):
    """등록되지 않은 rule_id를 조회/수정/삭제하려 할 때 발생한다."""


class AutomationRepository(ABC):
    """`AutomationRule`의 저장/조회 계약(M21). `ProjectRepository`와
    동일한 스타일(`get`/`save`는 upsert/`list_rules`). Automation
    CRUD는 이 Interface를 거치는 `AutomationService`(M21-T02)를
    통해서만 이루어진다(사용자 승인 조건 3) — `AutomationScheduler`도
    Rule을 직접 수정하지 않고 이 계약만 사용한다."""

    @abstractmethod
    def get(self, rule_id: str) -> AutomationRule:
        """
        입력: rule_id
        출력: rule_id에 해당하는 AutomationRule
        예외: 저장소에 해당 rule_id가 없으면 AutomationRuleNotFoundError
        보장: side-effect 없음(read-only). 반환된 AutomationRule은 마지막
              save() 이후의 최신 상태를 반영한다.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, rule: AutomationRule) -> None:
        """
        입력: rule_id가 채워진 AutomationRule
        출력: 없음
        예외: 없음 (동일 rule_id가 이미 있으면 덮어쓴다)
        보장: save(rule) 직후 get(rule.rule_id)를 호출하면 동일한 내용의
              AutomationRule을 반환한다 (멱등적 upsert).
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, rule_id: str) -> None:
        """
        입력: rule_id
        출력: 없음
        예외: 저장소에 해당 rule_id가 없으면 AutomationRuleNotFoundError
        보장: delete(rule_id) 이후 get(rule_id)는 AutomationRuleNotFoundError를
              던진다.
        """
        raise NotImplementedError

    @abstractmethod
    def list_rules(self) -> list[AutomationRule]:
        """
        입력: 없음
        출력: 저장된 모든 AutomationRule의 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 저장소 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError
