from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai_workspace.domain.workflow import Workflow


class WorkflowExecutionError(Exception):
    pass


class WorkflowEngine(ABC):
    """Task 실행 순서/의존관계 조율 계약. 구체 구현체는 Milestone 2(T2-03)에서
    작성한다.

    **Workflow Learning(Milestone 71, ADR-0089)**: `plan()`은 원래 의존관계만
    만족하면 되는 순수 계산이었다. `record_run_outcome()`(기록)/
    `recommended_order()`(조회) 두 메서드를 최소 확장해, 같은 `task_ids`
    조합(동일한 Workflow)이 다시 계획될 때 과거에 성공률이 가장 높았던
    실행 순서를 `plan()`이 우선 반환하도록 한다. 이 두 메서드를 전혀
    호출하지 않으면(과거 실행 이력이 없으면) `plan()`은 기존과 100%
    동일하게 동작한다.

    **Workflow Adaptive Planning(Milestone 72, ADR-0090)**: `recommended_
    order()`는 `dependencies`가 바뀌어도(같은 `task_ids`이면) 과거 추천을
    반환할 수 있는 "힌트"일 뿐이다. `plan()`은 이 힌트를 **현재**
    `workflow.dependencies`에 대해 검증한 뒤에만 채택하고, 검증에
    실패하면(추천이 없거나 지금 dependency를 어기면) 기존 위상 정렬로
    완전히 동일하게 fallback한다 — 추천이 Workflow 정합성을 깨뜨리는
    일은 없다.

    **Workflow Cost Optimization(Milestone 73, ADR-0091)**: `recommended_
    order()`가 동일한 최고 성공률의 순서 후보 여럿을 만나면, 구현체가
    M64 `EngineSelectionPolicy` 기반 비용 정보를 알 수 있는 경우에 한해
    예상 실행 비용이 더 낮은 후보를 추가 tie-break로 우선한다. 이 메서드
    시그니처는 무변경이다 — 비용 사용 여부는 구현체의 생성 시점 구성
    (예: 선택적 협력자 주입)에 달려 있고, 비용 정보를 알 수 없으면 기존
    tie-break(표본 수 → 먼저 기록된 순서)로 즉시 fallback한다."""

    @abstractmethod
    def plan(self, workflow: Workflow) -> list[str]:
        """
        입력: 순환 의존이 없는(Workflow 생성 시 자체 검증됨) Workflow 인스턴스
        출력: 의존관계를 만족하는 실행 순서로 정렬된 task_id 리스트
              (의존 대상 task_id가 항상 그것에 의존하는 task_id보다 앞선다)
        예외: 계획 수립이 불가능한 상태(예: 알 수 없는 내부 불일치)를 만나면
              WorkflowExecutionError
        보장: 반환된 리스트에는 workflow.task_ids의 모든 원소가 정확히 한 번씩
              포함된다. 입력 workflow는 변경하지 않는다(side-effect 없음).
              같은 `task_ids` 조합에 `recommended_order()`가 값을 반환하고
              (Milestone 71) 그 순서가 현재 `workflow.dependencies`를 실제로
              만족하면(Milestone 72) 그 순서를 그대로 반환하고, 없거나
              현재 dependency를 어기면(과거 이력 없음 또는 dependency가
              바뀌어 더 이상 유효하지 않음, 100% 하위 호환) 기존 계획
              로직(위상 정렬)을 쓴다.
        """
        raise NotImplementedError

    @abstractmethod
    def record_run_outcome(self, workflow: Workflow, order: list[str], success: bool) -> None:
        """**Workflow Learning(Milestone 71, ADR-0089)**: `plan()`이 반환한
        `order`로 `workflow`를 실제로 실행한 결과(성공/실패)를 기록한다 —
        보통 `WorkflowRunner.run()`이 완료 직후 자동으로 호출한다.

        입력: workflow (실행에 쓰인 Workflow — `task_ids`+`dependencies`
              조합이 동일한 키로 취급된다), order (실제로 실행된 순서,
              보통 이 `workflow`로 호출한 `plan()`의 반환값), success (그
              실행이 성공했는지)
        출력: 없음
        예외: 없음
        보장: 이후 같은 `task_ids` 조합으로 `recommended_order()`/`plan()`을
              호출하면 이 기록이 반영된다.
        """
        raise NotImplementedError

    @abstractmethod
    def recommended_order(self, workflow: Workflow) -> list[str] | None:
        """**Workflow Learning(Milestone 71, ADR-0089)**: 같은 `task_ids`
        조합으로 과거에 기록된(`record_run_outcome()`) 실행 순서들 중,
        표본이 3건 이상이고 성공률이 가장 높은 순서를 반환한다(M49/M65/
        M69/M70과 동일한 최소 표본 기준).

        **Workflow Adaptive Planning(Milestone 72, ADR-0090)**: `dependencies`
        는 더 이상 키에 포함되지 않는다 — 반환된 순서는 "이 `task_ids`
        조합에서 과거에 성공률이 높았던 순서"라는 힌트일 뿐, 호출 시점의
        `workflow.dependencies`를 반드시 만족한다는 보장은 없다. 그 검증은
        `plan()`의 책임이다.

        입력: workflow
        출력: 조건을 만족하는 기록이 있으면 그 순서(`list[str]`), 없으면
              `None`
        예외: 없음
        보장: side-effect 없음(read-only). 성공률이 동률이면(Milestone 73)
              구현체가 비용을 계산할 수 있는 경우 예상 비용이 더 낮은 순서를
              우선하고, 그래도 동률이거나 비용을 알 수 없으면 표본 수가
              더 많은 순서, 그마저 같으면 먼저 기록된 순서를 반환한다.
        """
        raise NotImplementedError

    @abstractmethod
    def export_learning_state(self) -> dict[str, Any]:
        """**Persistent Learning Memory(Milestone 83, ADR-0101)**:
        `record_run_outcome()`(M71)이 in-process로 누적한 `WorkflowOrderStat`
        학습 데이터를 JSON 직렬화 가능한 순수 값으로 구성된 스냅샷으로
        내보낸다 — 새 Learning 데이터를 만들지 않고 이미 존재하는 값
        객체를 그대로 인코딩할 뿐이다.

        입력: 없음
        출력: 이 구현체가 정의하는 JSON 직렬화 가능한 dict(정확한 키
              구조는 구현체 책임 — 호출자는 나중에 같은 구현체의
              `import_learning_state()`에 그대로 전달하는 것 외의
              용도로 내부 구조에 의존해서는 안 된다)
        예외: 없음
        보장: side-effect 없음(read-only). 반환값은 내부 상태의 독립된
              복사본이다.
        """
        raise NotImplementedError

    @abstractmethod
    def import_learning_state(self, state: dict[str, Any]) -> None:
        """**Persistent Learning Memory(Milestone 83, ADR-0101)**:
        `export_learning_state()`가 만든 스냅샷으로 M71의 in-process
        학습 상태를 복원한다 — 보통 Workspace 시작 시(구성 요소 생성
        직후) 한 번 호출된다.

        입력: state (같은 구현체의 `export_learning_state()`가 반환한 값)
        출력: 없음
        예외: 없음(형식이 예상과 다르면 구현체는 예외를 던질 수 있다 —
              호출자는 이 메서드 호출을 항상 예외 처리로 감싸 "저장/복원
              실패 시 기존 in-process 동작으로 즉시 fallback"해야 한다)
        보장: `import_learning_state(state)` 이후 이 구현체의 학습
              상태는 `state`를 내보냈던 시점과 동일해진다(기존 누적
              상태는 대체된다, 병합이 아니다). `plan()`의 위상 정렬
              로직은 전혀 건드리지 않는다.
        """
        raise NotImplementedError
