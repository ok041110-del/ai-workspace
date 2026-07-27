from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineExecutionResult:
    """`ExecutionDispatcher.dispatch()`의 결과를 표현하는 순수 domain
    객체(M18-T01, M19-T02에서 확장). `interfaces/
    execution_environment.py`의 `ExecutionResult`(OS 프로세스 실행
    결과 — returncode/stdout/stderr)와는 완전히 다른 개념이라 이름을
    분리했다 — 이쪽은 "어떤 Engine이 실행됐고 얼마나 걸렸는지"를
    다루는 상위 개념이다. 어떤 Provider도 참조하지 않는다.

    **Reliability 확장(M19-T02)**: `retry_count`(실제로 소요된 재시도
    횟수 — 첫 시도가 성공하면 0), `cancelled`(취소로 종료됐는지),
    `timed_out`(Timeout으로 종료됐는지, **휴리스틱** — `EngineAdapter`
    인터페이스를 이번 Milestone에서 변경하지 않기로 한 제약 때문에
    Timeout과 다른 실행 오류를 완전히 구분할 수 없다. 알려진 기술
    부채로, `.ai/DECISIONS.md`의 ADR-0031 참고) 세 필드를 추가했다.
    셋 다 기본값이 있어 기존 M18 호출부는 전혀 영향받지 않는다."""

    success: bool
    output: str
    error: str | None
    engine: str | None
    execution_time: float
    retry_count: int = 0
    cancelled: bool = False
    timed_out: bool = False
