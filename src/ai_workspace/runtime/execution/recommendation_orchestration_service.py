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
- `RecommendationExecutionService` — 실행

**Recommendation Explainability 연결(M44, ADR-0061)**: `explanation_service`
를 선택적으로 주입하면, Recommendation을 계산한 직후(Execution
위임 전) `RecommendationExplanationService.publish()`(M44)를 호출해
근거를 Vault에 기록한다 — Recommendation→Explainability→Execution
순서(M44 설계). 미주입 시(기본값 `None`) M43 이전과 완전히 동일하게
동작한다.

**Architecture Guardian 연결(M48, ADR-0065)**: `guardian_service`를
선택적으로 주입하면, Recommendation/Explainability 계산이 모두 끝난
뒤(따라서 Guardian 위반이 있어도 Recommendation은 그대로 Vault에
남는다) `ArchitectureGuardianService.generate()`(M41, Read Only —
Vault에 쓰지 않는다)를 호출해 `ArchitectureHealthReport`를 얻고
`RecommendationExecutionService`에 전달한다 — Execution 직전
(Pre-Execution) Gate로만 작동하며, 미주입 시(기본값 `None`) M43
이전과 완전히 동일하게 동작한다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.guardian.service import ArchitectureGuardianService
from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.intelligence.recommendation_explanation_service import (
    RecommendationExplanationService,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.runtime.execution.recommendation_execution_service import (
    RecommendationExecutionOutcome,
    RecommendationExecutionService,
)


class RecommendationOrchestrationService:
    """`ExperienceIntelligenceService`(M40) + `RecommendationIntelligenceService`
    (M35/M42) + `RecommendationExplanationService`(M44, 선택) +
    `ArchitectureGuardianService`(M48, 선택) +
    `RecommendationExecutionService`(M36)를 정해진 순서로 호출만
    하는 순수 흐름 제어 계층. 새 판단 로직 없음."""

    def __init__(
        self,
        experience_service: ExperienceIntelligenceService,
        recommendation_service: RecommendationIntelligenceService,
        execution_service: RecommendationExecutionService,
        explanation_service: RecommendationExplanationService | None = None,
        guardian_service: ArchitectureGuardianService | None = None,
    ) -> None:
        self._experience_service = experience_service
        self._recommendation_service = recommendation_service
        self._execution_service = execution_service
        self._explanation_service = explanation_service
        self._guardian_service = guardian_service

    def execute(self, *, manual_trigger: bool) -> RecommendationExecutionOutcome:
        """
        입력: manual_trigger(호출자가 수동 트리거임을 명시적으로
              전달해야 함 — 기본값 없음)
        출력: `RecommendationExecutionOutcome`(M36과 동일)
        예외: 없음
        보장: side-effect는 전부 `RecommendationExecutionService`가
              일으킨다 — 이 메서드 자체는 Experience 조회 +
              Recommendation 계산 + Guardian 평가(전부 Read Only)만
              추가로 수행한다. `explanation_service`가 주입돼 있으면
              Vault에 근거도 함께 기록한다(M44, Recommendation
              자체는 바뀌지 않음). `guardian_service`가 주입돼 있으면
              위반 시 Execution만 차단된다(M48, Recommendation은
              영향받지 않음).
        """
        experience_report = self._experience_service.generate()
        report = self._recommendation_service.generate(experience_report=experience_report)
        if self._explanation_service is not None:
            self._explanation_service.publish(report, experience_report)
        guardian_report = (
            self._guardian_service.generate() if self._guardian_service is not None else None
        )
        return self._execution_service.execute(
            report, manual_trigger=manual_trigger, guardian_report=guardian_report
        )

    def publish(self, *, manual_trigger: bool) -> tuple[RecommendationExecutionOutcome, Path]:
        """`execute()`와 동일한 흐름으로 `RecommendationExecutionService.
        publish()`를 호출해 Vault에도 기록한다(`AutomationActionExecutor`
        가 사용하는 진입점)."""
        experience_report = self._experience_service.generate()
        report = self._recommendation_service.generate(experience_report=experience_report)
        if self._explanation_service is not None:
            self._explanation_service.publish(report, experience_report)
        guardian_report = (
            self._guardian_service.generate() if self._guardian_service is not None else None
        )
        return self._execution_service.publish(
            report, manual_trigger=manual_trigger, guardian_report=guardian_report
        )
