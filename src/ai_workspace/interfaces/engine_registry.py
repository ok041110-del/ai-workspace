from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.engine_selection import EngineCandidate
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineAdapter


class DuplicateEngineRegistrationError(Exception):
    """이미 등록된 name으로 Engine을 다시 등록하려 할 때 발생한다."""


class EngineNotRegisteredError(Exception):
    """등록되지 않은 name의 Engine을 조회하려 할 때 발생한다."""


class EngineRegistry(ABC):
    """등록된 `EngineAdapter`가 무엇인지 조회하는 계약(M17-T01,
    `AgentRegistry`와 동일한 설계 원칙). `EngineRuntime`(실행 담당)과는
    완전히 별도의 컴포넌트다 — `EngineRuntime`은 이 저장소가 신설되기
    전부터 이미 자체적으로 Adapter를 등록·관리하고 있었고(내부 dict),
    이 계약은 그 내부 구현을 대체하지 않는다. 대신 후보 조회가 필요한
    쪽(`EngineSelectionPolicy` 등)이 같은 Adapter를 조립 시점에 이
    Registry에도 등록해 별도로 조회한다 — `EngineRuntime`의 실행
    계약(run/estimate_cost)은 이번 Milestone에서 전혀 확장하지 않는다."""

    @abstractmethod
    def register(self, name: str, adapter: EngineAdapter) -> None:
        """
        입력: name (Engine 식별 이름), adapter (등록할 EngineAdapter)
        출력: 없음
        예외: 이미 동일한 name이 등록되어 있으면 DuplicateEngineRegistrationError
        보장: register(name, adapter) 이후 get(name)은 adapter를 반환하고,
              list_candidates()의 후보 목록에 포함될 수 있다.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> EngineAdapter:
        """
        입력: name
        출력: 등록된 EngineAdapter
        예외: 등록되어 있지 않으면 EngineNotRegisteredError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def list_candidates(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineCandidate]:
        """
        입력: task (비용을 추정할 Task), required_capabilities (후보가
              반드시 지원해야 하는 능력 태그 집합, 생략 시 제약 없음)
        출력: required_capabilities를 모두 만족하는 등록된 Engine 전부를
              EngineCandidate로 나열(없으면 빈 리스트, 등록 순서 유지)
        예외: 없음
        보장: side-effect 없음(세션을 생성하지 않는다 — `EngineAdapter.
              estimate_cost()`만 호출한다). 반환된 리스트를 호출자가
              수정해도 내부 상태는 변하지 않는다(방어적 복사).
        """
        raise NotImplementedError
