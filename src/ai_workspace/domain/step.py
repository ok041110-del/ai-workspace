from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Step:
    step_id: str
    task_id: str
    description: str
