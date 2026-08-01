"""Observability Layer — Learning Runtime Analyzer (ADR-0072, Milestone 54).

M39(`ExecutionMemoryStore`)~M53(Decay)까지 쌓인 Learning 신호를
StatusLine(별도 프로세스)에서 읽을 수 있게 배선한다. M50(ADR-0067)
이 `<vault_root>/.ai-workspace-data/`에 영속화해 둔
`FileMemoryEngine` 데이터를, `ExecutionMemoryStore`(M39)/
`ExperienceIntelligenceService`(M40)에 그대로 태워 `ExperienceReport`
를 얻는다 — 새 Domain/Interface/Service 없이 기존 조합만 재사용한다.
`project_root`는 `vault_root`와 같다(ADR-0037, `web/server.py`에서도
동일하게 가정)."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.observability.snapshot import LearningRuntimeInfo
from ai_workspace.storage.file_memory_engine import FileMemoryEngine

_DATA_DIR_NAME = ".ai-workspace-data"


class LearningRuntimeAnalyzer:
    def analyze(self, project_root: Path) -> LearningRuntimeInfo:
        """
        입력: project_root(= vault_root, ADR-0037)
        출력: `LearningRuntimeInfo` — 추적 중인 task 수와 가장 위험한
              task(decayed_failure_rate 최댓값, 동점이면 task_id
              오름차순)
        예외: 없음
        보장: side-effect 없음(read-only) — Vault/저장소에 쓰지
              않는다. 기록이 없으면 모든 필드가 `None`/0.
        """
        vault_adapter = VaultAdapter(project_root)
        execution_memory_store = ExecutionMemoryStore(
            FileMemoryEngine(project_root / _DATA_DIR_NAME)
        )
        report = ExperienceIntelligenceService(vault_adapter, execution_memory_store).generate()

        if not report.stats:
            return LearningRuntimeInfo(
                tracked_task_count=0,
                highest_risk_task_id=None,
                highest_risk_decayed_failure_rate=None,
                highest_risk_recent_failure_streak=None,
            )

        highest_risk = sorted(
            report.stats,
            key=lambda stat: (-stat.decayed_failure_rate, stat.task_id),
        )[0]
        return LearningRuntimeInfo(
            tracked_task_count=len(report.stats),
            highest_risk_task_id=highest_risk.task_id,
            highest_risk_decayed_failure_rate=highest_risk.decayed_failure_rate,
            highest_risk_recent_failure_streak=highest_risk.recent_failure_streak,
        )
