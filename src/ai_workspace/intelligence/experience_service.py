"""Intelligence Layer — Experience Intelligence Service (ADR-0055, Milestone 40-T02~T03).

`ExecutionMemoryStore.query()`(M39, `memory/`)를 조회해
`ExperienceAnalyzer`(M40-T02)에 넘기고, 결과를 Vault에 노출하는 얇은
조합 계층. `RecommendationIntelligenceService`(M35)와 같은 뼈대 —
판정 로직은 전혀 갖지 않는다(Analyzer의 책임).

**Role 기반 경계(ADR-0055)**: `intelligence/`는 여전히 `domain`/
`interfaces`/`engines`/`vault`를 직접 참조하지 않는다
(ARCHITECTURE.md §8 규칙 21, 무변경). `*Service`로 끝나는 클래스를
담은 모듈은 `integration/`의 Adapter뿐 아니라 `memory/`의 Read-Only
제공자에도 의존할 수 있다 — 특정 클래스 이름(`ExecutionMemoryStore`)을
규칙에 나열하지 않고, "Memory Domain(§13.2 — 저장/검색만, 판단하지
않음)에 속하는 컴포넌트인가"라는 역할 기준으로 판단한다. Analyzer는
여전히 순수하다 — 이 Service만 `ExecutionMemoryStore`를 쥐고, 그
조회 결과(`ExecutionMemoryEntry`, `memory/`)를 `intelligence/`가
스스로 정의한 `ExperienceRecord`로 변환해서 `ExperienceAnalyzer.
analyze()`에 넘긴다 — Analyzer는 `memory/`를 전혀 import하지 않는다."""

from __future__ import annotations

from pathlib import Path

from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.experience_rules import (
    ExperienceAnalyzer,
    ExperienceRecord,
    ExperienceReport,
)
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore


class ExperienceIntelligenceService:
    """`ExecutionMemoryStore`(M39) + `ExperienceAnalyzer`(M40-T02)를
    조합해 `ExperienceReport`를 만들고, 필요하면 Vault에 노출한다."""

    def __init__(
        self, vault_adapter: VaultAdapter, execution_memory_store: ExecutionMemoryStore
    ) -> None:
        self._vault_adapter = vault_adapter
        self._execution_memory_store = execution_memory_store
        self._analyzer = ExperienceAnalyzer()

    def generate(self) -> ExperienceReport:
        """
        입력: 없음
        출력: `ExecutionMemoryStore`에 쌓인 모든 기록을 task_id별로
              집계한 `ExperienceReport`
        예외: 없음 — 기록이 없으면 `stats=[]`.
        보장: side-effect 없음(read-only) — Vault에 쓰지 않는다.
              쓰기가 필요하면 `publish()`를 쓴다.
        """
        entries = self._execution_memory_store.query()
        records = [
            ExperienceRecord(
                task_id=entry.task_id,
                action=entry.action,
                result=entry.result,
                timestamp=entry.timestamp,
                reason=entry.reason,
            )
            for entry in entries
        ]
        return self._analyzer.analyze(records)

    def publish(self) -> tuple[ExperienceReport, Path]:
        """`generate()` 결과를 Markdown으로 렌더링해 Vault에 쓴다
        (`VaultAdapter.publish_experience_intelligence()`에 위임).

        보장: `15 Project Intelligence/Experience Intelligence.md`가
              이번 결과로 완전히 덮어써진다(누적 append 아님).
        """
        report = self.generate()
        markdown = render_markdown(report)
        path = self._vault_adapter.publish_experience_intelligence(markdown)
        return report, path


def render_markdown(report: ExperienceReport) -> str:
    """`ExperienceReport`를 Vault 문서 Markdown으로 렌더링한다. 순수
    함수(입출력 문자열 변환만, I/O 없음)."""
    lines = [
        "---",
        "tags: [experience-intelligence]",
        "type: experience-intelligence",
        "---",
        "",
        "# Experience Intelligence",
        "",
        "> Milestone 40(Experience Intelligence)이 Execution Memory"
        "(M39)에 쌓인 실행 기록을 task_id별로 집계한 읽기 전용 문서다"
        "(ADR-0055). 판단 기준을 바꾸지 않는다 — Recommendation에는"
        " 반영되지 않는다(Learning 없음). 매 생성 시 이 문서 전체가"
        " 덮어써진다 — 편집해도 다음 생성 때 사라진다.",
        "",
        "## Task별 실행 경험",
        "",
    ]
    if report.stats:
        lines.append("| Task | 총 실행 | 성공 | 실패 | 최근 결과 | 최근 시각 |")
        lines.append("|---|---|---|---|---|---|")
        for stat in report.stats:
            lines.append(
                f"| {stat.task_id} | {stat.total} | {stat.success_count} | "
                f"{stat.failure_count} | {stat.last_result} | {stat.last_timestamp} |"
            )
    else:
        lines.append("- 기록된 실행 경험 없음")
    lines.append("")
    return "\n".join(lines)
