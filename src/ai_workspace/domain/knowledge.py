from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class KnowledgeKind(Enum):
    """M16: 프로젝트 Knowledge의 종류. 사용자가 예시로 든 7종(Architecture/
    ADR/Decision/Rule/Workflow/Task/Project) 중, 이 저장소에 실제로 대응하는
    문서 파일이 하나뿐인 것들은 통합했다(YAGNI) — ADR과 Decision은 둘 다
    `.ai/DECISIONS.md` 하나에 기록되고, Workflow와 Task는 둘 다
    `.ai/TASKS.md` 하나에 기록된다."""

    ARCHITECTURE = "architecture"
    ADR = "adr"
    RULE = "rule"
    TASK = "task"
    PROJECT = "project"


@dataclass(frozen=True)
class KnowledgeDocument:
    """프로젝트 문서 파일 하나를 통째로 표현하는 순수 domain 객체
    (M16-T01). 어떤 LLM Provider/Engine/Agent도 참조하지 않는다 —
    Claude/GPT/Gemini 어떤 조합이든 동일한 `KnowledgeDocument`를 본다."""

    document_id: str
    kind: KnowledgeKind
    title: str
    content: str
    source_path: str
