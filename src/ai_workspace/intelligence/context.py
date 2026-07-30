"""Intelligence Layer — Context Analyzer (ADR-0044, Milestone 30-T02).

`KnowledgeAdapter.list_all()`이 이미 노출한 Knowledge 문서 전체
텍스트를 Markdown 제목(`#`/`##`/`###`) 단위로 쪼개, `subject`(Task/
Milestone 식별자)가 언급된 항목만 `ContextEntry`로 채택한다. 새
지식을 만들지 않는다 — 이미 있는 문서를 구조적으로 파싱·필터링할
뿐이다(Rule 기반, LLM 호출 없음)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ai_workspace.integration.knowledge_adapter import KnowledgeAdapter, KnowledgeDocumentView

_HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.*)$", re.MULTILINE)
_MILESTONE_PATTERN = re.compile(r"[Mm]ilestone\s+(\d+)")
_M_TASK_PATTERN = re.compile(r"\bM(\d+)(?:-T\d+)?\b")
#: "M29-T01" 형태와 "Milestone 29-T01" 형태를 이 저장소가 문서 종류마다
#: 섞어서 쓴다(Task 제목은 "M29-T01:", ADR 제목은 "(Milestone 29-T01)").
#: subject 매칭이 실패하지 않도록 두 형태를 모두 생성해 대조한다.
_SUBJECT_MILESTONE_TASK = re.compile(r"^M(\d+)-T(\d+)$")
_SUBJECT_MILESTONE_ONLY = re.compile(r"^M(\d+)$")


@dataclass(frozen=True)
class ContextEntry:
    """Knowledge 문서 한 구간(제목+본문) 중 subject가 언급된 항목."""

    kind: str
    heading: str
    source_path: str
    milestone: str | None


@dataclass(frozen=True)
class ProjectContext:
    subject: str
    entries: list[ContextEntry]

    def by_kind(self, kind: str) -> list[ContextEntry]:
        return [entry for entry in self.entries if entry.kind == kind]


def _subject_variants(subject: str) -> list[str]:
    """`subject`(예: "M30-T01"/"M29")가 문서마다 다르게 표기될 수 있는
    형태를 전부 만든다 — 원문 그대로도 항상 포함한다."""
    variants = [subject]
    task_match = _SUBJECT_MILESTONE_TASK.match(subject)
    if task_match:
        variants.append(f"Milestone {task_match.group(1)}-T{task_match.group(2)}")
        return variants
    milestone_match = _SUBJECT_MILESTONE_ONLY.match(subject)
    if milestone_match:
        variants.append(f"Milestone {milestone_match.group(1)}")
    return variants


def _extract_milestone(text: str) -> str | None:
    match = _MILESTONE_PATTERN.search(text) or _M_TASK_PATTERN.search(text)
    return f"M{match.group(1)}" if match else None


def _split_sections(document: KnowledgeDocumentView) -> list[tuple[str, str]]:
    """문서 텍스트를 (제목, 본문) 목록으로 쪼갠다. 첫 제목 이전 텍스트는
    버린다(frontmatter/도입부는 subject 매칭 대상이 아니다). 평면
    분할이다 — 각 제목의 본문은 레벨과 무관하게 바로 다음 제목
    전까지만이라, 상위 제목(`## Milestone 30`)의 본문에는 그 아래
    하위 제목(`### M30-T01`)의 텍스트가 포함되지 않는다(계층 구조를
    만들지 않음, YAGNI) — 대신 하위 제목 자체가 별도 항목으로 매칭될
    수 있어 실질적인 누락은 없다."""
    matches = list(_HEADING_PATTERN.finditer(document.content))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document.content)
        body = document.content[start:end]
        sections.append((heading, body))
    return sections


class ContextAnalyzer:
    """`KnowledgeAdapter`만 생성자로 주입받는 Read Only Analyzer.
    `domain`/`interfaces`/`engines`/`vault`를 직접 참조하지 않는다."""

    def __init__(self, knowledge_adapter: KnowledgeAdapter) -> None:
        self._knowledge_adapter = knowledge_adapter

    def analyze(self, subject: str) -> ProjectContext:
        """
        입력: subject(Task ID "M30-T03" 또는 Milestone ID "M29" 등,
              빈 문자열이 아니어야 함)
        출력: `ProjectContext`(subject가 언급된 Knowledge 구간 목록)
        예외: 없음 — 언급된 구간이 없으면 `entries=[]`
        보장: side-effect 없음(read-only), Knowledge 문서를 수정하지
              않는다.
        """
        variants = _subject_variants(subject)
        entries: list[ContextEntry] = []
        for document in self._knowledge_adapter.list_all():
            for heading, body in _split_sections(document):
                haystack = f"{heading}\n{body}"
                if not any(variant in haystack for variant in variants):
                    continue
                entries.append(
                    ContextEntry(
                        kind=document.kind,
                        heading=heading,
                        source_path=document.source_path,
                        milestone=_extract_milestone(heading) or _extract_milestone(body),
                    )
                )
        return ProjectContext(subject=subject, entries=entries)
