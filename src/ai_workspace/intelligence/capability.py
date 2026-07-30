"""Intelligence Layer — Agent Capability Snapshot Analyzer (ADR-0045, Milestone 31-T02).

`AgentAdapter.list_active_agent_capabilities()`/`known_capabilities()`
가 이미 노출한 값만 읽어 집계한다 — 새 비즈니스 로직·쓰기 없음
(Query Layer Only, Read Only). `snapshot.ProjectSnapshotAnalyzer`
(Milestone 29-T02)와 같은 성격의 Analyzer다."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.integration.agent_adapter import AgentAdapter


@dataclass(frozen=True)
class AgentCapabilitySnapshot:
    """활성 Agent 전체를 Capability/Role 관점에서 집계한 스냅샷. 그
    자체로는 아무 판단(Coverage/Gap)도 내리지 않는다 — 판단은
    M31-T03의 책임이다."""

    total_active_agents: int
    by_capability: dict[str, int]
    by_role: dict[str, int]
    known_capabilities: frozenset[str]


class CapabilitySnapshotAnalyzer:
    """Agent Capability Snapshot을 계산하는 Read Only Analyzer.
    `AgentAdapter`에만 의존한다 — `domain`/`interfaces`/`engines`/
    `vault`를 직접 참조하지 않는다."""

    def __init__(self, agent_adapter: AgentAdapter) -> None:
        self._agent_adapter = agent_adapter

    def analyze(self) -> AgentCapabilitySnapshot:
        """
        입력: 없음
        출력: `AgentCapabilitySnapshot`(활성 Agent 수 + Capability별/
              Role별 집계 + 정의된 Capability 카탈로그)
        예외: 없음 — 활성 Agent가 하나도 없으면 모든 Capability의
              집계가 0인 Snapshot을 반환한다.
        보장: side-effect 없음(read-only).
        """
        agents = self._agent_adapter.list_active_agent_capabilities()
        known = self._agent_adapter.known_capabilities()

        by_capability: dict[str, int] = dict.fromkeys(known, 0)
        by_role: dict[str, int] = {}
        for agent in agents:
            by_role[agent.role] = by_role.get(agent.role, 0) + 1
            for capability in agent.capabilities:
                by_capability[capability] = by_capability.get(capability, 0) + 1

        return AgentCapabilitySnapshot(
            total_active_agents=len(agents),
            by_capability=by_capability,
            by_role=by_role,
            known_capabilities=known,
        )
