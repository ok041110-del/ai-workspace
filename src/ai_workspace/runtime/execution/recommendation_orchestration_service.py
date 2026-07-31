"""Execution Layer — Recommendation Orchestration Service (ADR-0059, Milestone 43-T05).

**책임(Responsibility, §13.3 Orchestration)**: Recommendation 단계를
완결한다 — `ExperienceIntelligenceService.generate()`(M40)로
`ExperienceReport`를 얻고, `RecommendationIntelligenceService.
generate(experience_report=...)`(M35, Adaptation은 M42)를 호출해
Adaptation까지 반영된 최종 `RecommendationIntelligenceReport`를
만든 뒤, `RecommendationExecutionService`(M36, M43에서 Recommendation
의존성 제거)에 그 결과를 그대로 전달한다.

이 Service 자체는 판단 로직을 전혀 갖지 않는다 — 정해진 순서로
호출만 한다(Orchestrating Connector·M32 Synthesis·M40 Experience가
이미 재사용해 온 것과 같은 조합 패턴, ADR-0041). `RecommendationRuleAnalyzer`
(M35)/`RecommendationAdjustmentAnalyzer`(M42)의 판단, `ExecutionGate`/
`ActionBuilder`(M36)의 실행 판정/변환, 이 어느 것도 이 Service에
포함되지 않는다.

**네 가지 책임의 분리(사용자 결정, ADR-0059)**:
- Composition Root(`web/server.py`) — 조립
- Analyzer(`RecommendationRuleAnalyzer`/`RecommendationAdjustmentAnalyzer`) — 판단
- `RecommendationOrchestrationService`(이 모듈) — 실행 흐름 제어
- `RecommendationExecutionService` — 실행"""

from __future__ import annotations

from pathlib import Path

from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.runtime.execution.recommendation_execution_service import (
    RecommendationExecutionOutcome,
    RecommendationExecutionService,
)


class RecommendationOrchestrationService:
    """`ExperienceIntelligenceService`(M40) + `RecommendationIntelligenceService`
    (M35/M42) + `RecommendationExecutionService`(M36)를 정해진 순서로
    호출만 하는 순수 흐름 제어 계층. 새 판단 로직 없음."""

    def __init__(
        self,
        experience_service: ExperienceIntelligenceService,
        recommendation_service: RecommendationIntelligenceService,
        execution_service: RecommendationExecutionService,
    ) -> None:
        self._experience_service = experience_service
        self._recommendation_service = recommendation_service
        self._execution_service = execution_service

    def execute(self, *, manual_trigger: bool) -> RecommendationExecutionOutcome:
        """
        입력: manual_trigger(호출자가 수동 트리거임을 명시적으로
              전달해야 함 — 기본값 없음)
        출력: `RecommendationExecutionOutcome`(M36과 동일)
        예외: 없음
        보장: side-effect는 전부 `RecommendationExecutionService`가
              일으킨다 — 이 메서드 자체는 Experience 조회 +
              Recommendation 계산(Read Only)만 추가로 수행한다.
        """
        experience_report = self._experience_service.generate()
        report = self._recommendation_service.generate(experience_report=experience_report)
        return self._execution_service.execute(report, manual_trigger=manual_trigger)

    def publish(self, *, manual_trigger: bool) -> tuple[RecommendationExecutionOutcome, Path]:
        """`execute()`와 동일한 흐름으로 `RecommendationExecutionService.
        publish()`를 호출해 Vault에도 기록한다(`AutomationActionExecutor`
        가 사용하는 진입점)."""
        experience_report = self._experience_service.generate()
        report = self._recommendation_service.generate(experience_report=experience_report)
        return self._execution_service.publish(report, manual_trigger=manual_trigger)
