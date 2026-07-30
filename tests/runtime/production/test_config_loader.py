import pytest

from ai_workspace.runtime.production.config_loader import (
    InvalidConfigFileError,
    load_production_config,
)


def test_load_with_no_file_or_env_returns_defaults() -> None:
    config = load_production_config(env={})

    assert config.host == "127.0.0.1"
    assert config.port == 8080


def test_load_from_config_file(tmp_path) -> None:
    config_file = tmp_path / "production.yaml"
    config_file.write_text(
        "host: 0.0.0.0\nport: 9090\nlog_level: DEBUG\nautomation_tick_seconds: 15\n"
        "engine_settings:\n  claude_code: enabled\n",
        encoding="utf-8",
    )

    config = load_production_config(config_path=config_file, env={})

    assert config.host == "0.0.0.0"
    assert config.port == 9090
    assert config.log_level == "DEBUG"
    assert config.automation_tick_seconds == 15.0
    assert config.engine_settings == {"claude_code": "enabled"}


def test_env_vars_override_config_file(tmp_path) -> None:
    config_file = tmp_path / "production.yaml"
    config_file.write_text("host: 0.0.0.0\nport: 9090\n", encoding="utf-8")

    config = load_production_config(
        config_path=config_file, env={"AI_WORKSPACE_PORT": "7000"}
    )

    assert config.host == "0.0.0.0"
    assert config.port == 7000


def test_env_vars_without_file() -> None:
    config = load_production_config(
        env={
            "AI_WORKSPACE_HOST": "0.0.0.0",
            "AI_WORKSPACE_PORT": "5000",
            "AI_WORKSPACE_LOG_LEVEL": "warning",
            "AI_WORKSPACE_DASHBOARD_ENABLED": "false",
            "AI_WORKSPACE_AUTOMATION_ENABLED": "0",
            "AI_WORKSPACE_AUTOMATION_TICK_SECONDS": "45",
        }
    )

    assert config.host == "0.0.0.0"
    assert config.port == 5000
    assert config.log_level == "WARNING"
    assert config.dashboard_enabled is False
    assert config.automation_enabled is False
    assert config.automation_tick_seconds == 45.0


def test_vault_root_env_var() -> None:
    config = load_production_config(env={"AI_WORKSPACE_VAULT_ROOT": "/srv/vault"})

    assert config.vault_root == "/srv/vault"


def test_invalid_bool_env_var_raises() -> None:
    with pytest.raises(InvalidConfigFileError):
        load_production_config(env={"AI_WORKSPACE_DASHBOARD_ENABLED": "maybe"})


def test_non_mapping_config_file_raises(tmp_path) -> None:
    config_file = tmp_path / "production.yaml"
    config_file.write_text("- just\n- a\n- list\n", encoding="utf-8")

    with pytest.raises(InvalidConfigFileError):
        load_production_config(config_path=config_file, env={})
