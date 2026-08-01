import pytest

from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.budget import Budget
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.engines.budget_policy_engine import InMemoryBudgetPolicyEngine
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.interfaces.engine_adapter import CostEstimate, EngineResult, EngineSessionStatus
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


class CostedEngineAdapter(MockEngineAdapter):
    """M64: `estimate_cost()`가 고정 비용을 반환하고 `run()` 호출 여부를
    기록하는 테스트용 Adapter — 비용 기반 선택을 테스트에서 재현할 수
    있게 한다. M65: `succeed=False`면 계속 실패해 신뢰도 추적을
    재현할 수 있다."""

    def __init__(
        self,
        estimated_cost_usd: float,
        capabilities: frozenset[str] = frozenset(),
        *,
        succeed: bool = True,
    ) -> None:
        super().__init__(capabilities)
        self._estimated_cost_usd = estimated_cost_usd
        self._succeed = succeed
        self.run_count = 0

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        self.run_count += 1
        if not self._succeed:
            if session_id not in self._sessions:
                raise ValueError("unknown session")
            self._sessions[session_id] = EngineSessionStatus.COMPLETED
            return EngineResult(success=False, output="", error="mock failure")
        return super().run(session_id, task, model=model)

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=self._estimated_cost_usd)


def test_run_executes_task_via_mock_adapter_and_returns_success() -> None:
    """T2-05 DoD: EngineRuntime.run()이 MockEngineAdapter를 통해 Task를
    "실행"하고 EngineResult(success=True)를 반환한다."""
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())

    result = runtime.run(make_task())

    assert result.success is True


def test_register_engine_duplicate_raises_error() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())

    with pytest.raises(DuplicateEngineError):
        runtime.register_engine("mock", MockEngineAdapter())


def test_run_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task(), required_capabilities=frozenset({"vision"}))


def test_status_reflects_completed_after_run() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()

    runtime.run(task)

    assert runtime.status(task.task_id) == EngineSessionStatus.COMPLETED


def test_cancel_then_status_is_cancelled() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    task = make_task()
    runtime.run(task)

    runtime.cancel(task.task_id)

    assert runtime.status(task.task_id) == EngineSessionStatus.CANCELLED


def test_status_unknown_task_raises_not_found() -> None:
    runtime = InMemoryEngineRuntime()

    with pytest.raises(EngineTaskNotFoundError):
        runtime.status("unknown")


def test_estimate_cost_returns_selected_adapters_estimate() -> None:
    runtime = InMemoryEngineRuntime()
    adapter = MockEngineAdapter()
    runtime.register_engine("mock", adapter)

    estimate = runtime.estimate_cost(make_task())

    assert estimate == adapter.estimate_cost(make_task())


def test_estimate_cost_raises_no_suitable_engine_when_capability_unmatched() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.estimate_cost(make_task(), required_capabilities=frozenset({"vision"}))


def test_run_parallel_preserves_order() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())
    tasks = [make_task("t1"), make_task("t2"), make_task("t3")]

    results = runtime.run_parallel(tasks)

    assert [result.success for result in results] == [True, True, True]


def test_run_ensemble_runs_same_task_via_each_named_engine() -> None:
    """M62(ADR-0080): 같은 Task를 여러 등록된 엔진 이름으로 동시에 돌려
    이름별 결과를 얻는다."""
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("claude", MockEngineAdapter())
    runtime.register_engine("codex", MockEngineAdapter())
    task = make_task()

    results = runtime.run_ensemble(task, ["claude", "codex"])

    assert set(results) == {"claude", "codex"}
    assert results["claude"].success is True
    assert results["codex"].success is True


def test_run_ensemble_unregistered_name_yields_failed_result_not_exception() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("claude", MockEngineAdapter())

    results = runtime.run_ensemble(make_task(), ["claude", "unknown"])

    assert results["claude"].success is True
    assert results["unknown"].success is False


def test_run_ensemble_empty_names_returns_empty_dict() -> None:
    runtime = InMemoryEngineRuntime()

    assert runtime.run_ensemble(make_task(), []) == {}


def test_run_without_policy_picks_first_registered_matching_adapter() -> None:
    """M64 이전과 100% 동일 동작(회귀 확인): policy 미주입 시 등록 순서상
    첫 매칭을 그대로 고른다 — 비용이 더 낮은 두 번째 엔진을 무시한다."""
    runtime = InMemoryEngineRuntime()
    expensive_first = CostedEngineAdapter(10.0)
    cheap_second = CostedEngineAdapter(1.0)
    runtime.register_engine("expensive", expensive_first)
    runtime.register_engine("cheap", cheap_second)

    runtime.run(make_task())

    assert expensive_first.run_count == 1
    assert cheap_second.run_count == 0


def test_run_with_policy_selects_cheapest_registered_adapter() -> None:
    """M64(ADR-0082): engine_selection_policy를 주입하면 등록 순서와
    무관하게 예상 비용이 가장 낮은 엔진이 선택된다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    expensive_first = CostedEngineAdapter(10.0)
    cheap_second = CostedEngineAdapter(1.0)
    runtime.register_engine("expensive", expensive_first)
    runtime.register_engine("cheap", cheap_second)

    runtime.run(make_task())

    assert expensive_first.run_count == 0
    assert cheap_second.run_count == 1


def test_run_with_policy_and_budget_excludes_over_budget_candidate() -> None:
    """M64: budget_policy_engine을 함께 주입하면 예산을 초과하는 후보는
    선택 대상에서 제외된다(InMemoryEngineSelectionPolicy가 이미 위임하는
    규칙을 EngineRuntime 경로에서도 재사용)."""
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=5.0))
    runtime = InMemoryEngineRuntime(
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        budget_policy_engine=budget_policy_engine,
    )
    over_budget = CostedEngineAdapter(10.0)
    cheapest_within_budget = CostedEngineAdapter(1.0)
    pricier_within_budget = CostedEngineAdapter(4.0)
    runtime.register_engine("over_budget", over_budget)
    runtime.register_engine("pricier_within_budget", pricier_within_budget)
    runtime.register_engine("cheapest_within_budget", cheapest_within_budget)

    runtime.run(make_task())

    assert over_budget.run_count == 0
    assert pricier_within_budget.run_count == 0
    assert cheapest_within_budget.run_count == 1


def test_run_raises_no_suitable_engine_when_no_candidate_within_budget() -> None:
    budget_policy_engine = InMemoryBudgetPolicyEngine(Budget(max_cost_usd=1.0))
    runtime = InMemoryEngineRuntime(
        engine_selection_policy=InMemoryEngineSelectionPolicy(),
        budget_policy_engine=budget_policy_engine,
    )
    runtime.register_engine("too_expensive", CostedEngineAdapter(5.0))

    with pytest.raises(NoSuitableEngineError):
        runtime.run(make_task())


def test_run_with_policy_excludes_engine_after_repeated_failures() -> None:
    """M65(ADR-0083): 성공 0건 + 표본 3건 이상(M49와 동일한 임계값) 쌓인
    엔진은 비용이 가장 싸도 더 이상 선택되지 않는다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))

    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 0

    runtime.run(make_task("after-exclusion"))

    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 1


def test_run_with_policy_does_not_exclude_engine_with_insufficient_sample() -> None:
    """실패가 1~2건뿐이면(표본 부족) 아직 제외되지 않는다 — M49와 동일한
    "성급하게 제외하지 않음" 원칙."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    runtime.run(make_task("warmup-0"))
    runtime.run(make_task("warmup-1"))

    assert failing_cheap.run_count == 2
    assert reliable_expensive.run_count == 0


def test_run_with_policy_reprobes_excluded_engine_after_probe_interval() -> None:
    """M66(ADR-0084): 제외된 엔진도 `_PROBE_INTERVAL`(5)번 연속 건너뛰면
    다음 선택에서 다시 후보로 포함되어 복구 여부를 재확인한다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))
    assert failing_cheap.run_count == 3

    for i in range(5):
        runtime.run(make_task(f"skip-{i}"))
    assert failing_cheap.run_count == 3
    assert reliable_expensive.run_count == 5

    runtime.run(make_task("probe"))

    assert failing_cheap.run_count == 4


def test_run_with_policy_recovers_after_successful_probe() -> None:
    """M66: probe 실행이 성공하면 `is_unreliable()`이 거짓이 되어 이후
    다시 정상적으로 선택된다(비용이 가장 싸므로)."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    recovering_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("recovering_cheap", recovering_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"warmup-{i}"))
    for i in range(5):
        runtime.run(make_task(f"skip-{i}"))

    recovering_cheap._succeed = True
    runtime.run(make_task("probe"))

    assert recovering_cheap.run_count == 4

    runtime.run(make_task("after-recovery"))

    assert recovering_cheap.run_count == 5
    assert reliable_expensive.run_count == 5


def test_run_without_policy_does_not_apply_reliability_exclusion() -> None:
    """M65 이전과 100% 동일 동작(회귀 확인): policy 미주입 시 신뢰도
    추적 자체는 여전히 계속 실패하는 엔진도 그대로 계속 선택한다."""
    runtime = InMemoryEngineRuntime()
    failing_only = CostedEngineAdapter(1.0, succeed=False)
    runtime.register_engine("failing_only", failing_only)

    for i in range(5):
        runtime.run(make_task(f"t{i}"))

    assert failing_only.run_count == 5


def test_run_ensemble_auto_without_policy_picks_first_n_matching_registered_order() -> None:
    """M68: policy 미주입 시 등록 순서상 조건을 만족하는 첫 top_n개를
    고른다 — run()의 정책 미주입 동작과 동일한 원칙."""
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("first", MockEngineAdapter())
    runtime.register_engine("second", MockEngineAdapter())
    runtime.register_engine("third", MockEngineAdapter())

    results = runtime.run_ensemble_auto(make_task(), top_n=2)

    assert set(results) == {"first", "second"}


def test_run_ensemble_auto_with_policy_selects_cheapest_n_candidates() -> None:
    """M68(ADR-0086): engine_selection_policy를 주입하면 비용이 낮은
    순서로 top_n개를 동적으로 고른다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    runtime.register_engine("expensive", CostedEngineAdapter(10.0))
    runtime.register_engine("cheapest", CostedEngineAdapter(1.0))
    runtime.register_engine("middle", CostedEngineAdapter(5.0))

    results = runtime.run_ensemble_auto(make_task(), top_n=2)

    assert set(results) == {"cheapest", "middle"}


def test_run_ensemble_auto_filters_by_required_capabilities() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("vision", MockEngineAdapter(frozenset({"vision"})))
    runtime.register_engine("code", MockEngineAdapter(frozenset({"code_generation"})))

    results = runtime.run_ensemble_auto(
        make_task(), required_capabilities=frozenset({"code_generation"}), top_n=5
    )

    assert set(results) == {"code"}


def test_run_ensemble_auto_returns_fewer_than_top_n_when_not_enough_candidates() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("only", MockEngineAdapter())

    results = runtime.run_ensemble_auto(make_task(), top_n=5)

    assert set(results) == {"only"}


def test_run_ensemble_auto_raises_no_suitable_engine_when_no_candidate_matches() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter(frozenset({"code_generation"})))

    with pytest.raises(NoSuitableEngineError):
        runtime.run_ensemble_auto(make_task(), required_capabilities=frozenset({"vision"}))


def test_run_ensemble_auto_with_top_n_below_one_returns_empty_dict() -> None:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("mock", MockEngineAdapter())

    assert runtime.run_ensemble_auto(make_task(), top_n=0) == {}


def test_run_ensemble_auto_excludes_unreliable_engine_with_policy() -> None:
    """M68이 M65/M66의 신뢰도 기반 제외 규칙을 그대로 적용받는지 확인한다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    failing_cheap = CostedEngineAdapter(1.0, succeed=False)
    reliable_expensive = CostedEngineAdapter(10.0)
    runtime.register_engine("failing_cheap", failing_cheap)
    runtime.register_engine("reliable_expensive", reliable_expensive)

    for i in range(3):
        runtime.run(make_task(f"t{i}"))
    assert failing_cheap.run_count == 3

    results = runtime.run_ensemble_auto(make_task("after"), top_n=2)

    assert set(results) == {"reliable_expensive"}


def test_run_with_policy_prefers_proven_success_over_untested_on_cost_tie() -> None:
    """M69(ADR-0087): 같은 비용(tie)에서, 이미 같은 required_capabilities
    조합으로 3회 이상 성공한 "검증된" 엔진이 아직 한 번도 실행된 적
    없는 "미검증" 엔진보다 tie-break에서 우선한다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    proven = CostedEngineAdapter(1.0)
    runtime.register_engine("proven", proven)
    for i in range(3):
        runtime.run(make_task(f"seed-{i}"))
    assert proven.run_count == 3

    untested = CostedEngineAdapter(1.0)
    runtime.register_engine("untested", untested)

    runtime.run(make_task("tie"))

    assert proven.run_count == 4
    assert untested.run_count == 0


def test_run_with_policy_prefers_untested_over_proven_failure_on_cost_tie() -> None:
    """M69(ADR-0087): 반대로, 같은 비용(tie)에서 검증된 이력이 "전량
    실패"라면 아직 미검증인 엔진이 오히려 우선한다 — 이미 나쁜 것으로
    확인된 이력이 완전한 미지수보다 낮게 평가된다."""
    runtime = InMemoryEngineRuntime(engine_selection_policy=InMemoryEngineSelectionPolicy())
    proven_bad = CostedEngineAdapter(1.0, succeed=False)
    runtime.register_engine("proven_bad", proven_bad)
    for i in range(2):
        runtime.run(make_task(f"seed-{i}"))
    assert proven_bad.run_count == 2

    untested = CostedEngineAdapter(1.0)
    runtime.register_engine("untested", untested)

    # proven_bad는 아직 신뢰도 제외 임계값(표본 3건) 미만이라 후보에는
    # 남아 있지만, 실행 메모리 성공률(0/2)이 확정되기엔 표본이 부족해
    # 아직 tie-break에는 반영되지 않는다 — 등록 순서상 첫 번째인
    # proven_bad가 그대로 선택된다.
    runtime.run(make_task("still-unknown"))
    assert proven_bad.run_count == 3
    assert untested.run_count == 0

    # 이제 proven_bad의 표본이 3건이 되어 성공률(0.0)이 확정된다 —
    # 완전히 미검증인 untested(중립으로 취급)가 더 우선한다.
    runtime.run(make_task("now-known-bad"))
    assert proven_bad.run_count == 3
    assert untested.run_count == 1


def test_run_without_policy_is_unaffected_by_execution_memory() -> None:
    """M69 이전과 100% 동일 동작(회귀 확인): policy 미주입 시 실행
    메모리는 기록만 되고 선택에는 전혀 반영되지 않는다."""
    runtime = InMemoryEngineRuntime()
    first = CostedEngineAdapter(1.0, succeed=False)
    second = CostedEngineAdapter(1.0)
    runtime.register_engine("first", first)
    runtime.register_engine("second", second)

    for i in range(5):
        runtime.run(make_task(f"t{i}"))

    assert first.run_count == 5
    assert second.run_count == 0
