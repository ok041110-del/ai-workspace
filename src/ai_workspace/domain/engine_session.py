from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EngineSession:
    session_id: str
    task_id: str
