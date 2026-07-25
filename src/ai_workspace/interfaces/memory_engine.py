from __future__ import annotations

from abc import ABC, abstractmethod


class MemoryEngine(ABC):
    """장기 메모리 조회/기록 계약. 구체 구현체는 Phase 2에서 작성한다."""

    @abstractmethod
    def remember(self, key: str, value: str) -> None:
        """
        입력: key(빈 문자열 아님), value
        출력: 없음
        예외: 없음
        보장: remember(key, value) 이후 recall(key)는 value를 반환한다.
              동일 key로 다시 호출하면 이전 값을 덮어쓴다.
        """
        raise NotImplementedError

    @abstractmethod
    def recall(self, key: str) -> str | None:
        """
        입력: key
        출력: 저장된 값, 없으면 None
        예외: 없음
        보장: side-effect 없음(read-only).
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> list[str]:
        """
        입력: query (검색어)
        출력: **value에 query 문자열이 부분 문자열로 포함된** 항목들의
              key 목록(없으면 빈 리스트). 대소문자 구분 여부·정렬 순서는
              구현체가 정의한다. key 자체는 검색 대상이 아니다.
        예외: 없음
        보장: side-effect 없음(read-only). 반환된 리스트를 호출자가
              수정해도 내부 상태는 변하지 않는다(방어적 복사).

        참고(M4-T08): 지금은 key만 반환하지만, 나중에 검색 결과의 관련도나
        일치 부분을 함께 보여줘야 할 필요가 생기면 `list[tuple[str, str]]`
        (key, value 쌍)로 확장할 수 있다 — 지금 시점에는 그 필요가
        증명되지 않아 최소 형태(key 목록)로 유지한다(YAGNI).
        """
        raise NotImplementedError
