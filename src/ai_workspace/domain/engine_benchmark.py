from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineBenchmarkProfile:
    """Milestone 77(Engine Benchmark & Capability Profiling, ADR-0095)가
    Provider(engine_name) 하나에 대해 조회하는 객관적 성능 요약. 새 측정을
    하지 않고 `EngineRuntime`이 M65(`EngineReliabilityStat`, 실행 경로
    무관 전체 성공/실패 카운트)와 M69(`EngineExecutionMemoryStat`, latency
    기록)로 이미 누적해 둔 in-process 상태를 읽기 전용으로 집계한 결과다.

    `execution_count`/`success_count`/`failure_count`는 `run()`/
    `run_parallel()`/`run_ensemble()`/`run_ensemble_auto()` 전체 실행
    경로를 반영하는 반면(M65가 모든 경로에서 기록), `latency_sample_count`/
    `total_latency_seconds`는 latency를 실제로 기록하는 경로(`run()`/
    `run_ensemble_auto()`, M69)만 반영한다 — 그래서 `average_latency_
    seconds()`의 표본 수가 `execution_count`보다 적을 수 있다(설계상
    허용, `run_parallel()`/`run_ensemble()`은 애초에 latency를 기록하지
    않는다). Routing 로직에는 전혀 관여하지 않는 순수 조회용 리포트다."""

    engine_name: str
    execution_count: int
    success_count: int
    failure_count: int
    latency_sample_count: int
    total_latency_seconds: float

    def success_rate(self) -> float | None:
        if self.execution_count == 0:
            return None
        return self.success_count / self.execution_count

    def failure_rate(self) -> float | None:
        if self.execution_count == 0:
            return None
        return self.failure_count / self.execution_count

    def average_latency_seconds(self) -> float | None:
        if self.latency_sample_count == 0:
            return None
        return self.total_latency_seconds / self.latency_sample_count
