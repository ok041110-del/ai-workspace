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
    구현체가 내부적으로 관리하며, 호출자에게 session_id를 노출하지 않는다.

    **Provider Concurrency Management(Milestone 74, ADR-0092)**: `register_
    engine()`에 선택적 `max_concurrency`를 지정하면, 구현체는 그 엔진에서
    동시에 실행 중인 세션 수가 한도에 도달했을 때 `run()`/`run_parallel()`의
    엔진 선택에서 그 엔진을 제외하고(다른 후보로 자동 fallback) 후보가
    남아 있으면 그것을 선택한다. 생략(기본값 `None`)하면 이전 동작과 100%
    동일하게 무제한이다."""

    @abstractmethod
    def register_engine(
        self, name: str, adapter: EngineAdapter, *, max_concurrency: int | None = None
    ) -> None:
        """
        입력: name (엔진 식별 이름, 예: "claude_code"), adapter (등록할
              EngineAdapter 구현체), max_concurrency (선택, Milestone 74 —
              이 엔진에서 동시에 실행 가능한 세션(run() 등 하나의 실행
              단위) 최대 개수. 생략하거나 `None`이면 무제한)
        출력: 없음
        예외: 이미 동일한 name이 등록되어 있으면 DuplicateEngineError
        보장: register_engine(name, adapter) 이후 run()/run_parallel()의 엔진
              선택 대상에 adapter가 포함된다. `max_concurrency`를 지정하면
              그 한도는 구현체 내부 in-process 카운터로만 추적된다(영속화
              없음) — 이 카운터는 `run()`/`run_parallel()`이 그 엔진의 세션을
              생성한 시점부터 실행이 끝날 때까지만 증가한다.
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
              NoSuitableEngineError — Milestone 74부터는 능력은 만족하지만
              `max_concurrency` 한도에 도달해 다른 후보로도 fallback할 수
              없는 경우(모든 후보가 busy)도 이 예외로 취급한다(기존 예외
              정책 그대로 재사용, 새 예외 타입 없음). 선택된 엔진에서
              EngineExecutionError가 발생하면 그대로 전파한다.
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
    def run_ensemble_auto(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        top_n: int = 2,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        """**Dynamic Ensemble Routing(Milestone 68, ADR-0086)**:
        `run_ensemble()`(M62)은 `engine_names`를 호출자가 직접 나열해야
        했고, `run()`/`estimate_cost()`가 이미 쓰는 `EngineSelectionPolicy`
        기반 비용·신뢰도 인식 선택(M64/M65/M66)을 전혀 활용하지 못했다.
        이 메서드는 `engine_names`를 직접 받는 대신 `run()`과 동일한
        `required_capabilities` 기준으로 후보를 추리고, 그중 상위 `top_n`
        개를 동적으로 골라 `run_ensemble()`에 그대로 위임한다 — 실제
        동시 실행/개별 실패 격리 메커니즘은 새로 만들지 않고 M62의
        것을 그대로 재사용한다(YAGNI).

        입력: task (모든 후보 엔진에 동일하게 실행할 Task),
              required_capabilities (후보가 반드시 지원해야 하는 능력
              태그 집합, 생략 시 제약 없음), top_n (선택할 최대 엔진
              개수, 기본값 2 — 1 미만이면 후보를 조회하지 않고 빈 dict를
              반환한다), model (선택적, 선택된 모든 엔진에 동일하게
              전달할 모델 이름)
        출력: 실제로 선택된 엔진 이름을 key로 하는 `run_ensemble()`의
              반환값 그대로. 선택된 엔진 수는 0 이상 `top_n` 이하이며,
              후보 수가 `top_n`보다 적으면 있는 만큼만 선택된다.
        예외: `top_n >= 1`인데 required_capabilities를 만족하는(그리고
              `engine_selection_policy` 주입 시 신뢰도상 제외되지 않는)
              등록된 엔진이 하나도 없으면 NoSuitableEngineError(선택
              단계 오류는 `run()`과 동일하게 예외로 전파하고, 개별 엔진의
              실행 실패는 `run_ensemble()`과 동일하게 결과로만 격리한다).
        보장: `engine_selection_policy`가 주입된 구현체는 그 정책으로
              후보를 반복 선택해(매번 이미 선택된 후보를 제외하고
              재선택) 비용이 낮은 순으로 최대 `top_n`개를 고르며,
              M65/M66의 신뢰도 기반 제외·Probe 규칙도 그대로 적용된다.
              주입되지 않았으면(기본값) 등록 순서상 조건을 만족하는
              첫 `top_n`개를 고른다 — `run()`의 정책 미주입 시 동작과
              동일한 원칙이다.
        """
        raise NotImplementedError

    @abstractmethod
    def record_consensus_outcome(
        self,
        required_capabilities: frozenset[str],
        agreeing_engines: tuple[str, ...],
        dissenting_engines: tuple[str, ...],
    ) -> None:
        """**Adaptive Consensus(Milestone 70, ADR-0088)**: `run_ensemble()`/
        `run_ensemble_auto()`(M62/M68)의 결과를 `ResultAggregator`(M63)로
        합의(다수결)한 뒤, 어떤 엔진의 투표가 최종 합의와 일치(agreeing)
        했고 어떤 엔진이 소수 의견(dissenting)이었는지를 `(required_
        capabilities, engine_name)` 키로 in-process 누적한다. `EngineRuntime`
        은 `ResultAggregator`의 존재를 모른다(ADR-0080/0081의 결합 방지
        원칙 유지) — 호출자(대개 `AdaptiveConsensusAggregator`)가 자신이
        계산한 합의 결과를 이 메서드로 "다시 알려주는" 것으로만 연결된다.

        입력: required_capabilities (그 Ensemble 실행에 쓰인 능력 태그
              집합 — `run_ensemble_auto()`에 전달했던 값과 같아야 한다),
              agreeing_engines (합의된 output과 일치한 성공 엔진 이름들),
              dissenting_engines (성공했지만 합의된 output과 다른 엔진
              이름들)
        출력: 없음
        예외: 없음
        보장: 이후 `consensus_weight(required_capabilities, name)` 호출
              결과에 이 기록이 반영된다. `agreeing_engines`/
              `dissenting_engines`에 없는 엔진(예: 실패한 엔진)의 기록은
              변하지 않는다.
        """
        raise NotImplementedError

    @abstractmethod
    def consensus_weight(self, required_capabilities: frozenset[str], engine_name: str) -> float:
        """**Adaptive Consensus(Milestone 70, ADR-0088)**: `record_consensus_
        outcome()`으로 누적된, 같은 `required_capabilities` 조합에서
        `engine_name`이 과거 Ensemble 합의와 일치했던 비율을 반환한다.

        입력: required_capabilities, engine_name
        출력: 표본이 3건 이상(M49/M65/M69와 동일한 최소 표본 기준)이면
              `agree_count / total`, 그렇지 않으면(표본 부족 또는 기록
              없음) 중립값 0.5 — 검증된 고성능 엔진보다는 낮지만 이미
              나쁜 것으로 확인된 엔진보다는 높게 취급해, 아직 검증되지
              않았을 뿐인 엔진이 부당하게 불리해지지 않도록 한다.
        예외: 없음
        보장: side-effect 없음(read-only).
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
