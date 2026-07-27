from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from ai_workspace.runtime.production.config import ProductionConfig

_ENV_PREFIX = "AI_WORKSPACE_"

_BOOL_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_BOOL_FALSE_VALUES = frozenset({"0", "false", "no", "off"})


class InvalidConfigFileError(ValueError):
    """설정 파일의 값이 `ProductionConfig` 필드 타입으로 변환할 수 없을 때
    발생한다."""


def _parse_bool(value: str, *, key: str) -> bool:
    normalized = value.strip().lower()
    if normalized in _BOOL_TRUE_VALUES:
        return True
    if normalized in _BOOL_FALSE_VALUES:
        return False
    raise InvalidConfigFileError(f"{key} 값을 불리언으로 해석할 수 없습니다: {value}")


def _load_config_file(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise InvalidConfigFileError(f"설정 파일의 최상위 구조는 매핑이어야 합니다: {path}")
    return data


def load_production_config(
    *, config_path: str | Path | None = None, env: Mapping[str, str] | None = None
) -> ProductionConfig:
    """기본값 → 설정 파일 → Environment Variable 순으로 겹쳐 쓴
    `ProductionConfig`를 만든다(M22-T01, 사용자 DoD — Env Var/설정
    파일 둘 다 지원). Env Var가 가장 마지막에 적용돼 배포 환경에서
    가장 구체적인 값으로 덮어쓸 수 있다(예: 컨테이너 오케스트레이션이
    주입하는 환경 변수가 파일 설정보다 우선).

    `ProductionConfig`/`ConfigLoader`는 서로 다른 책임이다(`domain/
    llm_policy.py`↔`storage/llm_policy_loader.py`와 동일한 분리
    패턴) — 이 로더만 PyYAML/`os.environ`을 안다."""
    values: dict[str, Any] = {}
    if config_path is not None:
        values.update(_load_config_file(config_path))

    env = env if env is not None else os.environ
    if (value := env.get(f"{_ENV_PREFIX}HOST")) is not None:
        values["host"] = value
    if (value := env.get(f"{_ENV_PREFIX}PORT")) is not None:
        values["port"] = int(value)
    if (value := env.get(f"{_ENV_PREFIX}LOG_LEVEL")) is not None:
        values["log_level"] = value.upper()
    if (value := env.get(f"{_ENV_PREFIX}DASHBOARD_ENABLED")) is not None:
        values["dashboard_enabled"] = _parse_bool(value, key=f"{_ENV_PREFIX}DASHBOARD_ENABLED")
    if (value := env.get(f"{_ENV_PREFIX}AUTOMATION_ENABLED")) is not None:
        values["automation_enabled"] = _parse_bool(
            value, key=f"{_ENV_PREFIX}AUTOMATION_ENABLED"
        )
    if (value := env.get(f"{_ENV_PREFIX}AUTOMATION_TICK_SECONDS")) is not None:
        values["automation_tick_seconds"] = float(value)

    return ProductionConfig(**values)
