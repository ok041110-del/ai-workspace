import pytest

from ai_workspace.runtime.production.config import InvalidConfigurationError, ProductionConfig


def test_default_values() -> None:
    config = ProductionConfig()

    assert config.host == "127.0.0.1"
    assert config.port == 8080
    assert config.log_level == "INFO"
    assert config.dashboard_enabled is True
    assert config.automation_enabled is True
    assert config.automation_tick_seconds == 30.0
    assert config.engine_settings == {}


def test_config_is_immutable() -> None:
    config = ProductionConfig()

    with pytest.raises(Exception):  # noqa: B017 - frozen dataclass raises FrozenInstanceError
        config.host = "0.0.0.0"  # type: ignore[misc]


def test_invalid_log_level_raises() -> None:
    with pytest.raises(InvalidConfigurationError):
        ProductionConfig(log_level="TRACE")


def test_non_positive_port_raises() -> None:
    with pytest.raises(InvalidConfigurationError):
        ProductionConfig(port=0)


def test_non_positive_automation_tick_seconds_raises() -> None:
    with pytest.raises(InvalidConfigurationError):
        ProductionConfig(automation_tick_seconds=0)


def test_engine_settings_accepts_custom_mapping() -> None:
    config = ProductionConfig(engine_settings={"claude_code": "enabled"})

    assert config.engine_settings == {"claude_code": "enabled"}
