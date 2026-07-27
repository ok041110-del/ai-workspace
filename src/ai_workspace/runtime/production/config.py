from __future__ import annotations

from dataclasses import dataclass, field

_VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_AUTOMATION_TICK_SECONDS = 30.0


class InvalidConfigurationError(ValueError):
    """`log_level`이 알려진 값이 아니거나 `port`/`automation_tick_seconds`
    가 유효 범위를 벗어날 때 발생한다."""


@dataclass(frozen=True)
class ProductionConfig:
    """Workspace Server 설정을 담는 불변 객체(M22-T01, 사용자 승인
    조건 1 — Infrastructure Layer의 Immutable 설정 객체). Core
    Domain(`domain`/`interfaces`/`engines`)은 이 타입을 전혀 알지
    못한다 — `runtime/production/`과 `web/`만 참조한다.

    `engine_settings`는 이번 Milestone 시점에 이 서버가 실제
    `EngineAdapter`를 등록하지 않는다는 알려진 한계(M21 Review)를
    반영해 최소 자리표시자로 둔다 — 구체적인 키는 아직 정의하지
    않는다."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    log_level: str = DEFAULT_LOG_LEVEL
    dashboard_enabled: bool = True
    automation_enabled: bool = True
    automation_tick_seconds: float = DEFAULT_AUTOMATION_TICK_SECONDS
    engine_settings: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.log_level not in _VALID_LOG_LEVELS:
            raise InvalidConfigurationError(
                f"알 수 없는 log_level입니다: {self.log_level} "
                f"(허용값: {sorted(_VALID_LOG_LEVELS)})"
            )
        if self.port <= 0:
            raise InvalidConfigurationError(f"port는 양수여야 합니다: {self.port}")
        if self.automation_tick_seconds <= 0:
            raise InvalidConfigurationError(
                f"automation_tick_seconds는 양수여야 합니다: {self.automation_tick_seconds}"
            )
