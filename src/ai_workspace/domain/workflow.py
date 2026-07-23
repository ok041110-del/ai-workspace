from __future__ import annotations

from dataclasses import dataclass, field


class WorkflowCycleError(ValueError):
    pass


@dataclass
class Workflow:
    workflow_id: str
    task_ids: list[str]
    dependencies: dict[str, set[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_dependencies()
        self._validate_no_cycle()

    def _validate_dependencies(self) -> None:
        known = set(self.task_ids)
        for task_id, depends_on in self.dependencies.items():
            if task_id not in known:
                raise ValueError(f"알 수 없는 Task입니다: {task_id}")
            unknown = depends_on - known
            if unknown:
                raise ValueError(f"알 수 없는 의존 Task입니다: {unknown}")

    def _validate_no_cycle(self) -> None:
        visited: set[str] = set()
        stack: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in stack:
                raise WorkflowCycleError(f"순환 의존이 감지되었습니다: {task_id}")
            if task_id in visited:
                return
            stack.add(task_id)
            for dependency in self.dependencies.get(task_id, set()):
                visit(dependency)
            stack.remove(task_id)
            visited.add(task_id)

        for task_id in self.task_ids:
            visit(task_id)
