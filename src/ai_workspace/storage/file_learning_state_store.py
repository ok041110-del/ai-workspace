from __future__ import annotations

import json
from pathlib import Path

from ai_workspace.interfaces.engine_runtime import EngineRuntime
from ai_workspace.interfaces.workflow_engine import WorkflowEngine

_STORE_FILENAME = "learning_state.json"


class FileLearningStateStore:
    """Persistent Learning Memory(Milestone 83, ADR-0101): `EngineRuntime`
    (M65/M69/M70/M81)과 `WorkflowEngine`(M71)의 `export_learning_state()`/
    `import_learning_state()` 스냅샷을 단일 JSON 파일 하나로 영속화한다
    — `FileMemoryEngine`(M50, ADR-0067)과 동일한 패턴(JSON 직렬화,
    `base_dir` 생성자 주입, `<vault_root>/.ai-workspace-data/` 배치)을
    따른다. 새로운 Core Domain Interface가 아니다 — `EngineRuntime`/
    `WorkflowEngine` 어느 쪽도 구현하지 않는 순수 I/O 헬퍼 클래스다.

    `save()`/`load()`는 파일 손상·권한 오류·디스크 문제 등 어떤 I/O
    예외가 발생해도 조용히 무시하고 반환한다 — "저장/복원 실패 시 기존
    in-process 동작으로 즉시 fallback"해야 한다는 요구를 그대로
    반영한다(새 로깅/예외 인프라를 추가하지 않는다, YAGNI). `load()`가
    실패하면 `engine_runtime`/`workflow_engine`은 생성 직후의 빈
    in-process 상태를 그대로 유지한다."""

    def __init__(self, base_dir: str | Path) -> None:
        self._path = Path(base_dir) / _STORE_FILENAME
        self._base_dir = Path(base_dir)

    def save(self, engine_runtime: EngineRuntime, workflow_engine: WorkflowEngine) -> None:
        try:
            self._base_dir.mkdir(parents=True, exist_ok=True)
            data = {
                "engine_runtime": engine_runtime.export_learning_state(),
                "workflow_engine": workflow_engine.export_learning_state(),
            }
            self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def load(self, engine_runtime: EngineRuntime, workflow_engine: WorkflowEngine) -> None:
        try:
            if not self._path.exists():
                return
            data = json.loads(self._path.read_text(encoding="utf-8"))
            engine_runtime.import_learning_state(data.get("engine_runtime", {}))
            workflow_engine.import_learning_state(data.get("workflow_engine", {}))
        except Exception:
            pass
