"""`ExecutionDispatcher`가 발행하는 Event 타입 상수(M20-T01,
`agents/events.py`와 동일한 패턴). `ExecutionDispatcher`는 이 Event를
발행하기만 하고, 누가 구독하는지 알지 못한다(M20 Dashboard가 첫
구독자이지만 그 사실을 이 모듈은 모른다)."""

ENGINE_EXECUTION_STARTED = "engine_execution_started"
ENGINE_EXECUTION_COMPLETED = "engine_execution_completed"
