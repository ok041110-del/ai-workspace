import logging

from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.logging_setup import (
    LOGGER_NAME,
    configure_logging,
    get_logger,
)


def test_configure_logging_sets_level_from_config() -> None:
    logger = configure_logging(ProductionConfig(log_level="DEBUG"))

    assert logger.level == logging.DEBUG
    assert logger.name == LOGGER_NAME


def test_configure_logging_always_adds_console_handler() -> None:
    logger = configure_logging(ProductionConfig())

    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


def test_configure_logging_adds_file_handler_when_given(tmp_path) -> None:
    log_file = tmp_path / "workspace.log"

    logger = configure_logging(ProductionConfig(), log_file=log_file)
    logger.info("hello")
    for handler in logger.handlers:
        handler.flush()

    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    assert "hello" in log_file.read_text(encoding="utf-8")


def test_configure_logging_is_idempotent_and_does_not_duplicate_handlers() -> None:
    configure_logging(ProductionConfig())
    logger = configure_logging(ProductionConfig())

    assert len(logger.handlers) == 1


def test_get_logger_returns_named_child_of_ai_workspace() -> None:
    logger = get_logger("production.lifecycle")

    assert logger.name == "ai_workspace.production.lifecycle"


def test_get_logger_without_name_returns_root_ai_workspace_logger() -> None:
    logger = get_logger()

    assert logger.name == LOGGER_NAME
