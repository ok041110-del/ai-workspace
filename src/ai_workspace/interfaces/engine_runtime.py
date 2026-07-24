from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    EngineAdapter,
    EngineResult,
    EngineSessionStatus,
)


class DuplicateEngineError(Exception):
    """이미 등록된 이름으로 엔진을 다시 등록하려 할 때 발생한다."""


class NoSuitableEngineError(Exception):
    """요구된 Capability를 만족하는 등록된 엔진이 하나도 없을 때 발생한다."""


class EngineTaskNotFoundError(Exception):
    """실행 중이거나 실행된 적이 없는 task_id를 취소/조회하려 할 때 발생한다."""


class EngineRuntime(ABC):
    """Agent Runtime과 Engine Adapter 사이에서 엔진 선택, 세션 풀 관리, 병렬
    실행을 담당하는 계약(ARCHITECTURE.md §3.9, ADR-0016). Agent는 EngineAdapter를
    직접 호출하지 않고 항상 이 EngineRuntime을 거친다(ARCHITECTURE.md §8
    의존성 규칙 6). 세션(create_session/destroy_session)은 이 계약의 구체
    구현체가 내부적으로 관리하며, 호출자에게 session_id를 노출하지 않는다."""

    @abstractmethod
    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        """
        입력: name (엔진 식별 이름, 예: "claude_code"), adapter (등록할
              EngineAdapter 구현체)
        출력: 없음
        예외: 이미 동일한 name이 등록되어 있으면 DuplicateEngineError
        보장: register_engine(name, adapter) 이후 run()/run_parallel()의 엔진
              선택 대상에 adapter가 포함된다.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, task: Task, required_capabilities: frozenset[str] = frozenset()) -> EngineResult:
        """
        입력: task (실행할 Task), required_capabilities (선택할 엔진이 반드시
              지원해야 하는 능력 태그 집합, 생략 시 제약 없음)
        출력: EngineResult(success, output, error)
        예외: required_capabilities를 모두 만족하는 등록된 엔진이 없으면
              NoSuitableEngineError. 선택된 엔진에서 EngineExecutionError가
              발생하면 그대로 전파한다.
        보장: run() 호출이 예외 없이 반환되면, 이후 status(task.task_id)는
              EngineResult.success에 대응하는 COMPLETED(성공) 또는
              FAILED(실패)를 반환한다. 세션 생성/정리는 이 호출 안에서
              완결되며 호출자에게 session_id가 노출되지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        """
        입력: tasks (병렬로 실행할 Task 목록), required_capabilities (선택할
              엔진이 반드시 지원해야 하는 능력 태그 집합, 생략 시 제약 없음)
        출력: tasks와 같은 순서, 같은 길이의 EngineResult 목록
        예외: required_capabilities를 모두 만족하면서 병렬 실행(supports_parallel)을
              지원하는 등록된 엔진이 없으면 NoSuitableEngineError
        보장: 반환된 목록의 i번째 원소는 tasks의 i번째 Task에 대한 결과다
              (실행 완료 순서가 아니라 입력 순서를 따른다).
        """
        raise NotImplementedError

    @abstractmethod
    def cancel(self, task_id: str) -> None:
        """
        입력: task_id (run()/run_parallel()로 한 번이라도 실행된 적이 있는
              Task의 task_id)
        출력: 없음
        예외: 해당 task_id가 run()/run_parallel()로 추적된 적이 없으면
              EngineTaskNotFoundError
        보장: cancel(task_id) 이후 status(task_id)는 CANCELLED를 반환한다.
        """
        raise NotImplementedError

    @abstractmethod
    def status(self, task_id: str) -> EngineSessionStatus:
        """
        입력: task_id
        출력: 해당 task_id로 실행된 가장 최근 실행의 상태
        예외: 해당 task_id가 run()/run_parallel()로 추적된 적이 없으면
              EngineTaskNotFoundError
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError
