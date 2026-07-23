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
