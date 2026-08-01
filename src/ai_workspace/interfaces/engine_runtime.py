from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
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
    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> EngineResult:
        """
        입력: task (실행할 Task), required_capabilities (선택할 엔진이 반드시
              지원해야 하는 능력 태그 집합, 생략 시 제약 없음), model (선택적,
              선택된 엔진에 그대로 전달할 모델 이름 — Milestone 14. 이 값이
              엔진 선택 자체에 영향을 주지는 않는다)
        출력: EngineResult(success, output, error)
        예외: required_capabilities를 모두 만족하는 등록된 엔진이 없으면
              NoSuitableEngineError. 선택된 엔진에서 EngineExecutionError가
              발생하면 그대로 전파한다.
        보장: run() 호출이 예외 없이 반환되면, 이후 status(task.task_id)는
              EngineResult.success에 대응하는 COMPLETED(성공) 또는
              FAILED(실패)를 반환한다. 세션 생성/정리는 이 호출 안에서
              완결되며 호출자에게 session_id가 노출되지 않는다. model을
              생략하면 이전 계약(Milestone 14 이전)과 동일하게 동작한다.
        """
        raise NotImplementedError

    @abstractmethod
    def run_parallel(
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> list[EngineResult]:
        """
        입력: tasks (병렬로 실행할 Task 목록), required_capabilities (선택할
              엔진이 반드시 지원해야 하는 능력 태그 집합, 생략 시 제약 없음),
              model (선택적, 배치의 모든 Task에 동일하게 전달할 모델 이름)
        출력: tasks와 같은 순서, 같은 길이의 EngineResult 목록
        예외: required_capabilities를 모두 만족하면서 병렬 실행(supports_parallel)을
              지원하는 등록된 엔진이 없으면 NoSuitableEngineError(Runtime 자체가
              이 요청을 처리할 수 없는 치명적 오류이므로, 개별 Task 실행을
              시작하기 전에 즉시 전파된다 — 아래 "개별 Task 실패" 보장과는
              다른 층위다).
        보장(M10-T01, 개별 Task 실패 격리):
          1. 반환된 목록의 길이는 항상 len(tasks)와 같다.
          2. 반환된 목록의 i번째 원소는 tasks의 i번째 Task에 대한 결과다
             (실행 완료 순서가 아니라 입력 순서를 따른다).
          3. 개별 Task 실행 중 발생한 예외(예: EngineExecutionError)는 그
             Task의 EngineResult(success=False, error=예외 메시지)로 변환된다.
          4. 개별 Task 실패만으로는 run_parallel() 자체가 예외를 던지지
             않는다 — 위 "예외" 항목(NoSuitableEngineError 등 Runtime 자체의
             치명적 오류)만 예외로 전파되며, 그 외에는 항상 EngineResult
             목록을 정상 반환한다.
        """
        raise NotImplementedError

    @abstractmethod
    def run_ensemble(
        self,
        task: Task,
        engine_names: list[str],
        *,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        """**Multi-LLM Orchestrator(Milestone 62, ADR-0080)**: `run()`/
        `run_parallel()`이 "어떤 하나의 엔진을 고를지"만 결정하는 것과 달리,
        이 메서드는 **같은 Task**를 `engine_names`로 지정된 여러 등록된
        엔진에 동시에 돌려 비교 가능한 결과 묶음을 만든다. capability 기준
        선택(`_select`/`_require_adapter`)을 거치지 않고 `register_engine()`
        에 쓰인 이름으로 정확히 지정한다 — 여러 Provider(Claude/Codex/
        Gemini 등)를 의도적으로 섞어 돌리는 것이 목적이므로 "능력 만족하는
        첫 하나" 규칙은 맞지 않는다. 결과를 투표/합치는 로직은 포함하지
        않는다 — 호출자가 반환된 결과를 비교·선택한다(YAGNI).

        입력: task (모든 엔진에 동일하게 실행할 Task), engine_names (실행할
              등록된 엔진 이름 목록), model (선택적, 모든 엔진에 동일하게
              전달할 모델 이름)
        출력: engine_names의 각 이름을 key로, 그 엔진의 EngineResult를
              value로 하는 dict. 반환된 dict의 key 집합은 항상 입력
              engine_names와 같다(중복 이름은 마지막 결과로 덮어써짐).
        예외: 없음 — `engine_names`가 비어 있으면 빈 dict를 반환한다.
        보장(개별 엔진 실패 격리, `run_parallel()`의 M10-T01/T02 원칙과
        동일): 등록되지 않은 이름이거나 실행 중 예외가 발생해도 그 이름의
        `EngineResult(success=False, error=...)`로만 반영되고, 다른 이름의
        결과나 이 메서드 자체의 반환에는 영향을 주지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def estimate_cost(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> CostEstimate:
        """
        입력: task (비용을 추정할 Task), required_capabilities (run()과 동일한
              선택 기준 — 어떤 엔진이 선택될지가 추정치에 영향을 준다)
        출력: 선택된 엔진의 CostEstimate(estimated_tokens, estimated_cost_usd)
        예외: required_capabilities를 모두 만족하는 등록된 엔진이 없으면
              NoSuitableEngineError(run()과 동일한 선택 규칙)
        보장: side-effect 없음(세션을 생성하지 않는다 — run()과 달리 실제
              실행이나 세션 생명주기에 관여하지 않는다, M15-T02). 엔진 선택은
              run()과 동일한 규칙(등록 순서상 첫 매칭)을 따르므로, 같은
              required_capabilities로 run()을 호출했을 때 선택될 엔진과
              항상 같은 엔진의 추정치를 반환한다.
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
