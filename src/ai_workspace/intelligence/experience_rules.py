"""Intelligence Layer — Experience Analyzer (ADR-0055, Milestone 40-T02).

task_id별 성공/실패 집계를 계산하는 순수 Analyzer.
`RecommendationRuleAnalyzer`(M35)와 같은 성격 — Adapter도 Store도
직접 쥐지 않고, `intelligence/`가 스스로 정의한 값 타입(`ExperienceRecord`)
만 입력으로 받는다. `memory/`를 포함해 이 파일 밖 어떤 패키지도
import하지 않는다(Analyzer 순수성, `tests/intelligence/
test_intelligence_layering.py`가 `*Service` 클래스 유무로 강제).
`ExecutionMemoryEntry`(`memory/execution_memory_store.py`, M39)를
`ExperienceRecord`로 변환하는 것은 `ExperienceIntelligenceService`
(M40-T02/T03)의 책임이다.

**Deterministic + Immutable Input(M40 DoD, 사용자 조건)**: 같은
`records`가 주어지면 항상 같은 `ExperienceReport`를 반환한다 — 현재
시각·난수·외부 상태를 전혀 참조하지 않는다. `records`(각 원소는
`ExperienceRecord`, 아래에서 `@dataclass(frozen=True)`로 정의)는
읽기만 하고 절대 수정하지 않는다 — 쓰기 메서드는 이 모듈 어디에도
없다."""

from __future__ import annotations

from dataclasses import dataclass

_RESULT_SUCCESS = "success"


@dataclass(frozen=True)
class ExperienceRecord:
    """`ExperienceAnalyzer`가 받는 입력 1건. `memory.execution_memory_store.
    ExecutionMemoryEntry`와 필드가 같지만, Analyzer 순수성을 위해
    `intelligence/`가 스스로 정의하는 별도 타입이다 — `memory/`를
    import하지 않고도 이 파일이 컴파일/타입체크되게 하는 목적뿐이다."""

    task_id: str
    action: str
    result: str
    timestamp: str
    reason: str | None = None


@dataclass(frozen=True)
class ExperienceStat:
    """task_id 하나에 대한 누적 실행 경험."""

    task_id: str
    total: int
    success_count: int
    failure_count: int
    last_result: str
    last_timestamp: str


@dataclass(frozen=True)
class ExperienceReport:
    """전체 task_id에 대한 `ExperienceStat` 목록. `task_id` 오름차순
    정렬(입력 순서와 무관하게 항상 같은 순서 — Deterministic 보장의
    일부)."""

    stats: list[ExperienceStat]


class ExperienceAnalyzer:
    """`ExperienceRecord` 목록을 task_id별로 집계하는 Read Only
    Analyzer. `analyze()` 하나만 제공하며, 어떤 저장소도 참조하지
    않는다(생성자 인자 없음) — 새 판단 기준·점수·AI 추론 없음."""

    def analyze(self, records: list[ExperienceRecord]) -> ExperienceReport:
        """
        입력: records (`ExperienceRecord` 목록, 어느 순서든 무관)
        출력: task_id별 성공/실패 집계 + 가장 최근 기록의 결과/시각을
              담은 `ExperienceReport`. `stats`는 task_id 오름차순.
        예외: 없음 — records가 비어 있으면 `stats=[]`.
        보장: side-effect 없음(read-only), `records`를 수정하지
              않는다. 같은 records(순서 무관)에는 항상 같은 결과.
        """
        grouped: dict[str, list[ExperienceRecord]] = {}
        for record in records:
            grouped.setdefault(record.task_id, []).append(record)

        stats = [
            self._summarize(task_id, entries) for task_id, entries in sorted(grouped.items())
        ]
        return ExperienceReport(stats=stats)

    @staticmethod
    def _summarize(task_id: str, entries: list[ExperienceRecord]) -> ExperienceStat:
        ordered = sorted(entries, key=lambda entry: entry.timestamp)
        latest = ordered[-1]
        success_count = sum(1 for entry in entries if entry.result == _RESULT_SUCCESS)
        return ExperienceStat(
            task_id=task_id,
            total=len(entries),
            success_count=success_count,
            failure_count=len(entries) - success_count,
            last_result=latest.result,
            last_timestamp=latest.timestamp,
        )
