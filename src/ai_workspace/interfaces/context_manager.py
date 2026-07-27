from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.session import WorkspaceSession


class SnapshotNotFoundError(Exception):
    """존재하지 않는 snapshot_id를 복원하려 할 때 발생한다."""


class ContextManager(ABC):
    """Agent에게 제공할 Context를 조립하고 Memory Snapshot의 생명주기(생성/복원)를
    관리하는 계약(ARCHITECTURE.md §3.8, ADR-0017). 저장/검색 자체는
    `MemoryEngine`에 위임하며(Agent → Context Manager → Memory Engine,
    ARCHITECTURE.md §8 규칙 7), Context Manager는 그 결과를 조합해 Context를
    구성하고 `WorkspaceSession.memory_snapshot_id`가 가리키는 Snapshot을
    소유·관리한다. `MemoryEngine`은 저장/검색만 담당하며 Snapshot 개념을 알지
    못한다."""

    @abstractmethod
    def assemble_context(self, session: WorkspaceSession) -> dict[str, str]:
        """
        입력: session (Context를 조립할 대상 WorkspaceSession)
        출력: Agent에게 제공할 key-value 형태의 Context
        예외: 없음
        보장: side-effect 없음(read-only). session.memory_snapshot_id가
              가리키는 Snapshot이 존재하면 그 내용이 결과에 반영된다.
        """
        raise NotImplementedError

    @abstractmethod
    def create_snapshot(self, session: WorkspaceSession, summary: str | None = None) -> str:
        """
        입력: session (현재 Context 상태를 저장할 대상 WorkspaceSession),
              summary (선택, M7-T01 — 이 Snapshot에 함께 저장할 자연어
              요약. 생략하면 요약 없이 기존과 동일하게 동작)
        출력: 새로 생성된 Snapshot을 식별하는 snapshot_id
        예외: 없음
        보장: create_snapshot(session) 직후 restore_snapshot(snapshot_id)를
              호출하면 그 시점의 assemble_context(session) 결과에 summary가
              주어졌을 경우 `{"summary": summary}`가 추가된 Context를
              반환한다. summary는 `MemoryEngine`이 저장하는 문자열의 일부가
              되므로 `find_snapshots()`로도 검색된다. 여러 Snapshot에 걸친
              누적 요약(요약의 요약)은 하지 않는다 — 매번 최신 요약 하나만
              저장한다.
        """
        raise NotImplementedError

    @abstractmethod
    def restore_snapshot(self, snapshot_id: str) -> dict[str, str]:
        """
        입력: snapshot_id (create_snapshot()이 반환한 값)
        출력: 해당 Snapshot이 저장하고 있던 Context
        예외: 존재하지 않는 snapshot_id면 SnapshotNotFoundError
        보장: side-effect 없음(read-only). 반환된 dict를 호출자가 수정해도
              Context Manager 내부 상태는 변하지 않는다(방어적 복사).
        """
        raise NotImplementedError

    @abstractmethod
    def find_snapshots(self, query: str) -> list[str]:
        """
        입력: query (검색어)
        출력: 내용에 query가 포함된 Snapshot들의 snapshot_id 목록(없으면
              빈 리스트)
        예외: 없음
        보장: side-effect 없음(read-only). 저장/검색 자체는 `MemoryEngine.
              search()`에 위임한다(§8 규칙 7 — Agent는 이 메서드를 통해서만
              검색하며 MemoryEngine을 직접 호출하지 않는다).
        """
        raise NotImplementedError

    @abstractmethod
    def latest_snapshot_id(self, project_id: str) -> str | None:
        """
        입력: project_id
        출력: 해당 project_id로 `create_snapshot()`이 가장 최근에 생성한
              snapshot_id(없으면 `None`)
        예외: 없음
        보장: side-effect 없음(read-only). `create_snapshot(session, ...)`
              호출 시 `session.current_project_id`가 `project_id`와
              같으면, 그 직후 `latest_snapshot_id(project_id)`는 새로
              생성된 snapshot_id를 반환한다(M8-T01). `find_snapshots()`와
              달리 내용 일치가 아니라 "가장 최근 생성"이라는 정렬 순서를
              계약한다 — `MemoryEngine.search()`는 이 순서를 보장하지
              않으므로(계약 문서 참고) 별도로 추적한다.
        """
        raise NotImplementedError
