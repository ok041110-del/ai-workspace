from __future__ import annotations

import logging
from pathlib import Path

from ai_workspace.runtime.production.config import ProductionConfig

LOGGER_NAME = "ai_workspace"

_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(
    config: ProductionConfig, *, log_file: str | Path | None = None
) -> logging.Logger:
    """`ProductionConfig.log_level`을 기준으로 표준 `logging` 모듈을
    설정한다(M22-T02). `logging`은 Domain에 침투하지 않는다 — 이
    함수는 `runtime/production/`(Infrastructure Layer)에만 있고,
    `domain`/`interfaces`/`engines`는 이 모듈을 참조하지 않는다.

    Console 출력은 항상 켜진다. `log_file`을 주면 동일한 로그를
    File에도 함께 남긴다(둘 다 지원, 사용자 DoD). 여러 번 호출해도
    핸들러가 중복 누적되지 않도록 매 호출마다 기존 핸들러를 비운다
    (idempotent 재설정 — 예: 서버 재시작 없이 Configuration Reload
    시에도 안전)."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(config.log_level)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """`ai_workspace` 로거(또는 그 하위 로거)를 반환한다.
    `configure_logging()`을 먼저 호출하지 않아도 표준 `logging`
    기본 동작(핸들러 없으면 루트로 전파)으로 안전하게 쓸 수 있다."""
    if name is None:
        return logging.getLogger(LOGGER_NAME)
    return logging.getLogger(f"{LOGGER_NAME}.{name}")
