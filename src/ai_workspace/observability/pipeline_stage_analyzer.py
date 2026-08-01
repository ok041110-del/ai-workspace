"""Observability Layer — Pipeline Stage Analyzer (ADR-0062, Milestone 45).

Recommendation(M35)→Adaptation(M42)→Explainability(M44)→
Orchestration(M43)→Execution(M36)→Memory(M39)→Experience(M40) 7단계
각각의 상태를, 이미 Vault에 발행된 산출물의 존재 여부만으로
재구성한다(§13.3 Explainability와 동일한 원칙 — 새 판단 없음).

**Phase 1의 정직한 한계(ADR-0062 결정 3)**:
- Adaptation/Orchestration은 별도 Vault 산출물이 없다(M42/M43
  Domain Analysis에서 이미 확인된 대로, 두 개념 모두 다른 산출물
  안에 구조적으로 포함된다) — `STRUCTURAL_INCLUDED`로 표시한다.
- Memory(M39, `ExecutionMemoryStore`)는 M50(ADR-0067)부터
  `FileMemoryEngine`으로 JSON 파일에 영속화된다. M54(ADR-0072)에서
  `LearningRuntimeAnalyzer`가 이 파일을 읽는 배선을 추가해,
  `NOT_OBSERVABLE`이 `OBSERVED_DONE`/`OBSERVED_NOT_YET`으로
  승격됐다 — 판정 기준은 다른 단계와 동일하게 "산출물(여기서는
  추적 중인 학습 기록)이 존재하는가"뿐이다(추정 금지)."""

from __future__ import annotations

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.observability.snapshot import PipelineStageState, PipelineStageStatus

_RECOMMENDATION_REPORT = ("15 Project Intelligence", "Recommendation Intelligence.md")
_EXPLANATION_REPORT = ("15 Project Intelligence", "Recommendation Explanation.md")
_EXECUTION_REPORT = ("15 Project Intelligence", "Recommendation Execution.md")
_EXPERIENCE_REPORT = ("15 Project Intelligence", "Experience Intelligence.md")


class PipelineStageAnalyzer:
    def analyze(
        self, vault_adapter: VaultAdapter, *, has_learning_records: bool
    ) -> tuple[PipelineStageState, ...]:
        """
        입력: vault_adapter(읽기 전용 `report_last_modified()`만 사용),
              has_learning_records(M54 — `LearningRuntimeAnalyzer`가
              이미 계산한 `tracked_task_count > 0` 여부. 이 클래스는
              `FileMemoryEngine`을 직접 읽지 않는다 — 계산 위치를
              중복시키지 않기 위해 이미 계산된 값만 받는다)
        출력: 7단계 `PipelineStageState`(순서 고정)
        예외: 없음
        보장: Vault에 쓰지 않는다. Adaptation/Orchestration의 판단
              로직, Memory의 영속화 여부를 바꾸지 않는다(관측만 한다).
        """
        recommendation_mtime = vault_adapter.report_last_modified(*_RECOMMENDATION_REPORT)
        explanation_mtime = vault_adapter.report_last_modified(*_EXPLANATION_REPORT)
        execution_mtime = vault_adapter.report_last_modified(*_EXECUTION_REPORT)
        experience_mtime = vault_adapter.report_last_modified(*_EXPERIENCE_REPORT)

        return (
            _observed_stage(
                "Recommendation", recommendation_mtime, "Recommendation Intelligence.md"
            ),
            PipelineStageState(
                name="Adaptation",
                status=PipelineStageStatus.STRUCTURAL_INCLUDED,
                note=(
                    "별도 Vault 산출물 없음 — Recommendation Intelligence.md에 "
                    "구조적으로 포함(ADR-0058)"
                ),
            ),
            _observed_stage(
                "Explainability", explanation_mtime, "Recommendation Explanation.md"
            ),
            PipelineStageState(
                name="Orchestration",
                status=PipelineStageStatus.STRUCTURAL_INCLUDED,
                note=(
                    "별도 Vault 산출물 없음 — 판단 로직 없는 흐름 제어(ADR-0059), "
                    "Execution 산출물로 갈음"
                ),
            ),
            _observed_stage("Execution", execution_mtime, "Recommendation Execution.md"),
            _memory_stage(has_learning_records),
            _observed_stage("Experience", experience_mtime, "Experience Intelligence.md"),
        )


def _observed_stage(name: str, mtime: float | None, report_filename: str) -> PipelineStageState:
    if mtime is None:
        return PipelineStageState(
            name=name,
            status=PipelineStageStatus.OBSERVED_NOT_YET,
            note=f"{report_filename} 없음 — 아직 발행된 적 없음",
        )
    return PipelineStageState(
        name=name,
        status=PipelineStageStatus.OBSERVED_DONE,
        note=f"{report_filename} 존재",
    )


def _memory_stage(has_learning_records: bool) -> PipelineStageState:
    if not has_learning_records:
        return PipelineStageState(
            name="Memory",
            status=PipelineStageStatus.OBSERVED_NOT_YET,
            note="FileMemoryEngine(M50)에 기록된 실행 이력 없음 — 아직 실행된 적 없음",
        )
    return PipelineStageState(
        name="Memory",
        status=PipelineStageStatus.OBSERVED_DONE,
        note="FileMemoryEngine(M50)에 실행 이력 존재(M54, LearningRuntimeAnalyzer)",
    )
