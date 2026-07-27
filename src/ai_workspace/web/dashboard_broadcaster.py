from __future__ import annotations

import asyncio
import dataclasses

from fastapi import WebSocket, WebSocketDisconnect

from ai_workspace.interfaces.event_bus import Event, EventBus
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.execution.events import (
    ENGINE_AUTHENTICATION_FAILED,
    ENGINE_EXECUTION_COMPLETED,
    ENGINE_EXECUTION_STARTED,
)
from ai_workspace.web.dashboard_viewmodel import build_dashboard_view_model

_RELEVANT_EVENT_TYPES = frozenset(
    {ENGINE_EXECUTION_STARTED, ENGINE_EXECUTION_COMPLETED, ENGINE_AUTHENTICATION_FAILED}
)


class DashboardBroadcaster:
    """Dashboard 관련 Event가 발생할 때마다 연결된 WebSocket 클라이언트
    전부에게 최신 스냅샷을 밀어주는 브로드캐스터(M20-T05). Polling을
    쓰지 않는다 — `EventBus` 구독이 유일한 갱신 트리거다.
    `EventBus.publish()`는 동기(sync)이지만 WebSocket 전송은 비동기
    이므로, 연결 시점의 이벤트 루프를 기억해 뒀다가
    `call_soon_threadsafe()`로 안전하게 넘긴다(발행이 다른 스레드에서
    일어나도 안전)."""

    def __init__(self, *, dashboard_service: DashboardService) -> None:
        self._dashboard_service = dashboard_service
        self._connections: dict[WebSocket, asyncio.AbstractEventLoop] = {}

    def register_event_bus(self, event_bus: EventBus) -> None:
        event_bus.subscribe(self._on_event)

    def _on_event(self, event: Event) -> None:
        if event.event_type not in _RELEVANT_EVENT_TYPES:
            return
        payload = dataclasses.asdict(
            build_dashboard_view_model(self._dashboard_service.snapshot())
        )
        for websocket, loop in list(self._connections.items()):
            loop.call_soon_threadsafe(self._schedule_send, websocket, payload)

    def _schedule_send(self, websocket: WebSocket, payload: dict[str, object]) -> None:
        asyncio.ensure_future(self._safe_send(websocket, payload))

    async def _safe_send(self, websocket: WebSocket, payload: dict[str, object]) -> None:
        try:
            await websocket.send_json(payload)
        except Exception:
            pass

    async def handle_connection(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[websocket] = asyncio.get_running_loop()
        try:
            await websocket.send_json(
                dataclasses.asdict(build_dashboard_view_model(self._dashboard_service.snapshot()))
            )
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            self._connections.pop(websocket, None)
