from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineExecutionResult:
    """`ExecutionDispatcher.dispatch()`의 결과를 표현하는 순수 domain
    객체(M18-T01). `interfaces/execution_environment.py`의
    `ExecutionResult`(OS 프로세스 실행 결과 — returncode/stdout/stderr)
    와는 완전히 다른 개념이라 이름을 분리했다 — 이쪽은 "어떤 Engine이
    실행됐고 얼마나 걸렸는지"를 다루는 상위 개념이다. 어떤 Provider도
    참조하지 않는다."""

    success: bool
    output: str
    error: str | None
    engine: str | None
    execution_time: float
