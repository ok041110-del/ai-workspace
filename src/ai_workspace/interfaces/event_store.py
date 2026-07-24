from __future__ import annotations

from abc import ABC, abstractmethod

from ai_workspace.interfaces.event_bus import Event


class EventStore(ABC):
    """EventBus에 발행된 Event를 영구 기록하고 재생(Replay)/감사(Audit)하기
    위한 계약. ARCHITECTURE.md §3.5, ADR-0018.

    EventStore는 EventBus의 배달 경로에 포함되지 않는 **독립 구독자**다. 즉
    EventStore는 EventBus.subscribe()를 통해 등록된 하나의 구독자로서 Event를
    수신하여 record()를 호출할 뿐이며, EventBus가 EventStore를 특별히 인식하거나
    이를 거쳐서 다른 구독자에게 전달하지 않는다. 실제 기록 방식(파일/DB 등)의
    구체 구현은 지금 하지 않는다(Milestone 2 이후)."""

    @abstractmethod
    def record(self, event: Event) -> None:
        """
        입력: 기록할 Event (보통 EventBus 구독 handler를 통해 전달받음)
        출력: 없음
        예외: 없음
        보장: record(event) 이후 replay()의 결과에 event가 포함된다.
        """
        raise NotImplementedError

    @abstractmethod
    def replay(self, since_event_id: str | None = None) -> list[Event]:
        """
        입력: since_event_id (이 event_id 다음부터 재생, None이면 처음부터
              재생)
        출력: record()된 순서를 유지하는 Event 목록 (없으면 빈 리스트)
        예외: 없음 (since_event_id가 기록에 없으면 빈 리스트를 반환한다)
        보장: 반환된 리스트를 호출자가 수정해도 저장소 내부 상태는 변하지
              않는다 (방어적 복사).
        """
        raise NotImplementedError
