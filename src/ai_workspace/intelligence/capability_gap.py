"""Intelligence Layer — Capability Coverage & Gap Analyzer (ADR-0045, Milestone 31-T03).

`capability.AgentCapabilitySnapshot`(M31-T02 산출물)만 입력으로 받는
순수 Rule 기반 판단 계층이다 — Adapter를 직접 호출하지 않는다(이미
Snapshot 단계에서 읽어온 값만 재사용, 새로운 데이터 접근 경로 없음).
AI 추론/LLM 호출은 하지 않는다(사용자 지시 — Rule 기반만)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_workspace.intelligence.capability import AgentCapabilitySnapshot

#: Coverage 등급(Interface/Domain Enum이 아니라 이 모듈 안의 문자열
#: 상수 — intelligence/는 domain을 직접 참조하지 않는다). M29/M30의
#: healthy/warning/critical과 달리 중립적인 이름을 쓴다 — 활성
#: Agent 0명은 시스템 이상이 아니라 이 저장소가 아직 Agent 프로세스를
#: 상시 구동하지 않는 워크숍 단계의 자연스러운 상태이기 때문이다
#: (ADR-0045, M29 `active_agent_count`도 항상 0으로 관찰됨).
COVERAGE_NONE = "none"
COVERAGE_PARTIAL = "partial"
COVERAGE_FULL = "full"


@dataclass(frozen=True)
class CapabilityGap:
    capability: str
    detail: str


@dataclass(frozen=True)
class CapabilityCoverage:
    level: str
    ratio: float


@dataclass(frozen=True)
class CapabilityGapReport:
    coverage: CapabilityCoverage
    gaps: list[CapabilityGap]


class CapabilityGapAnalyzer:
    """`AgentCapabilitySnapshot`을 입력으로 Coverage/Gap을 계산하는
    Rule 기반 Analyzer. 새 판단 기준 없이 "정의된 Capability 대비
    활성 Agent가 0명인 Capability"만 Gap으로 판정한다."""

    def analyze(self, snapshot: AgentCapabilitySnapshot) -> CapabilityGapReport:
        """
        입력: `AgentCapabilitySnapshot`(M31-T02 산출물)
        출력: `CapabilityGapReport`(Coverage 등급/비율 + Gap 목록)
        예외: 없음
        보장: side-effect 없음(read-only), Snapshot을 변경하지 않는다.
        """
        gaps = [
            CapabilityGap(
                capability=capability,
                detail=f"'{capability}' Capability를 제공하는 활성 Agent 없음",
            )
            for capability, count in sorted(snapshot.by_capability.items())
            if count == 0
        ]
        coverage = self._determine_coverage(snapshot, gaps)
        return CapabilityGapReport(coverage=coverage, gaps=gaps)

    def _determine_coverage(
        self, snapshot: AgentCapabilitySnapshot, gaps: list[CapabilityGap]
    ) -> CapabilityCoverage:
        total_known = len(snapshot.known_capabilities)
        if total_known == 0:
            return CapabilityCoverage(level=COVERAGE_FULL, ratio=1.0)

        covered = total_known - len(gaps)
        ratio = covered / total_known
        if ratio <= 0.0:
            level = COVERAGE_NONE
        elif ratio < 1.0:
            level = COVERAGE_PARTIAL
        else:
            level = COVERAGE_FULL
        return CapabilityCoverage(level=level, ratio=ratio)
