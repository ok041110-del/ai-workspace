from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.domain.project import Project


class ProjectNotFoundError(Exception):
    pass


class ProjectRepository(ABC):
    """Project의 조회/저장 계약. 구체 구현체: Phase 1의 FileProjectRepository."""

    @abstractmethod
    def load(self, project_id: str) -> Project:
        """
        입력: project_id (빈 문자열이 아닌 식별자)
        출력: project_id에 해당하는 Project
        예외: 저장소에 해당 project_id가 없으면 ProjectNotFoundError
        보장: side-effect 없음(read-only). 반환된 Project는 마지막 save() 이후의
              최신 상태를 반영한다.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, project: Project) -> None:
        """
        입력: project_id가 채워진 Project 인스턴스
        출력: 없음
        예외: 없음 (동일 project_id가 이미 있으면 덮어쓴다)
        보장: save(project) 직후 load(project.project_id)를 호출하면 동일한
              내용의 Project를 반환한다 (멱등적 upsert).
        """
        raise NotImplementedError

    @abstractmethod
    def list_projects(self) -> list[Project]:
        """
        입력: 없음
        출력: 저장된 모든 Project의 목록 (없으면 빈 리스트)
        예외: 없음
        보장: 반환된 리스트를 호출자가 수정해도 저장소 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError
