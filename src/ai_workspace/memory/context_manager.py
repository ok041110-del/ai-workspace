from __future__ import annotations

import itertools
import json

from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.interfaces.context_manager import ContextManager, SnapshotNotFoundError
from ai_workspace.interfaces.memory_engine import MemoryEngine


class InMemoryContextManager(ContextManager):
    """Agent에게 제공할 Context를 조립하고 Memory Snapshot 생명주기를 관리하는
    최소 구현체(ARCHITECTURE.md §3.8, ADR-0017, T2-04). Snapshot 데이터는
    자체 보관하지 않고 `MemoryEngine`(저장/검색만 아는 하위 서비스)을 거쳐
    저장한다(§8 규칙 7 — Agent → Context Manager → Memory Engine).

    **Memory 요약(M7-T01)**: `create_snapshot()`의 선택적 `summary`는
    Agent가 이미 만든 요약 문자열을 그대로 전달받아 Context에 얹을
    뿐이다 — 이 클래스는 요약을 생성하지 않는다(무엇을 요약할지, 어떻게
    요약할지는 EngineRuntime을 호출할 수 있는 Agent 계층의 책임).

    **세션 연속성(M8-T01)**: `latest_snapshot_id(project_id)`가 반환할
    "project별 최신 snapshot" 포인터는 **`MemoryEngine`을 거치지 않고
    이 클래스 내부에서만 관리**한다(`_latest_snapshot_by_project`) —
    `MemoryEngine.search()`(따라서 `find_snapshots()`)는 값의 substring
    일치로 동작하는데, 포인터도 같이 저장하면 우연히 검색어와 일치해
    실제 Snapshot이 아닌 포인터 key가 검색 결과에 섞여 나올 위험이
    있다. 포인터는 "가장 최근 것이 무엇인지"를 가리키는 내부 색인일
    뿐 사용자에게 검색될 "메모리 내용"이 아니므로, `MemoryEngine`의
    책임(저장된 값의 내용 검색) 밖에 둔다."""

    def __init__(self, memory_engine: MemoryEngine) -> None:
        self._memory_engine = memory_engine
        self._id_generator = itertools.count(1)
        self._latest_snapshot_by_project: dict[str, str] = {}

    def assemble_context(self, session: WorkspaceSession) -> dict[str, str]:
        context: dict[str, str] = {}
        if session.current_project_id is not None:
            context["project_id"] = session.current_project_id
        if session.current_mission_id is not None:
            context["mission_id"] = session.current_mission_id
        if session.memory_snapshot_id is not None:
            stored = self._memory_engine.recall(session.memory_snapshot_id)
            if stored is not None:
                context.update(json.loads(stored))
        return context

    def create_snapshot(self, session: WorkspaceSession, summary: str | None = None) -> str:
        snapshot_id = f"snapshot-{next(self._id_generator)}"
        context = self.assemble_context(session)
        if summary is not None:
            context["summary"] = summary
        self._memory_engine.remember(snapshot_id, json.dumps(context, ensure_ascii=False))
        if session.current_project_id is not None:
            self._latest_snapshot_by_project[session.current_project_id] = snapshot_id
        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> dict[str, str]:
        stored = self._memory_engine.recall(snapshot_id)
        if stored is None:
            raise SnapshotNotFoundError(snapshot_id)
        return json.loads(stored)

    def find_snapshots(self, query: str) -> list[str]:
        return self._memory_engine.search(query)

    def latest_snapshot_id(self, project_id: str) -> str | None:
        return self._latest_snapshot_by_project.get(project_id)
