from __future__ import annotations

from ai_workspace.domain.engine_selection import EngineCandidate
from ai_workspace.domain.task import Task
from ai_workspace.interfaces.engine_adapter import EngineAdapter
from ai_workspace.interfaces.engine_registry import (
    DuplicateEngineRegistrationError,
    EngineNotRegisteredError,
    EngineRegistry,
)


class InMemoryEngineRegistry(EngineRegistry):
    """등록된 `EngineAdapter`를 이름별로 보관하고, 요청된 Capability를
    만족하는 후보 전부를 `EngineCandidate`로 나열하는 최소 구현체
    (M17-T01)."""

    def __init__(self) -> None:
        self._engines: dict[str, EngineAdapter] = {}

    def register(self, name: str, adapter: EngineAdapter) -> None:
        if name in self._engines:
            raise DuplicateEngineRegistrationError(name)
        self._engines[name] = adapter

    def get(self, name: str) -> EngineAdapter:
        if name not in self._engines:
            raise EngineNotRegisteredError(name)
        return self._engines[name]

    def list_candidates(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineCandidate]:
        candidates = []
        for name, adapter in self._engines.items():
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            estimate = adapter.estimate_cost(task)
            candidates.append(
                EngineCandidate(
                    engine_name=name,
                    capabilities=adapter.capabilities(),
                    estimated_tokens=estimate.estimated_tokens,
                    estimated_cost_usd=estimate.estimated_cost_usd,
                    supports_parallel=adapter.supports_parallel(),
                )
            )
        return candidates
