from pathlib import Path

import pytest

from ai_workspace.domain.task import TaskStatus
from ai_workspace.engines.task_engine import InMemoryTaskEngine
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.integration.workflow_adapter import WorkflowAdapter
from ai_workspace.integration.workflow_task_link import WorkflowTaskLink


def _make_vault(tmp_path: Path) -> Path:
    (tmp_path / "11 Milestones").mkdir(parents=True)
    (tmp_path / "11 Milestones" / "Milestones Index.md").write_text(
        "# Milestones Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    (tmp_path / "12 Decisions").mkdir(parents=True)
    (tmp_path / "12 Decisions" / "Decisions Index.md").write_text(
        "# Decisions Index\n\n## 관련 문서\n\n- [[Overview]]\n", encoding="utf-8"
    )
    return tmp_path


def _make_link(tmp_path: Path) -> tuple[WorkflowTaskLink, VaultAdapter, Path]:
    vault_root = _make_vault(tmp_path)
    vault_adapter = VaultAdapter(vault_root)
    workflow_adapter = WorkflowAdapter(InMemoryWorkflowEngine(), InMemoryTaskEngine())
    return WorkflowTaskLink(vault_adapter, workflow_adapter), vault_adapter, vault_root


def _create_vault_task(vault_adapter: VaultAdapter, task_id: str, title: str) -> None:
    vault_adapter.create_task(
        task_id,
        title,
        status="todo",
        priority="high",
        milestone="M28",
        owner="AI",
        created="2026-07-30",
        updated="2026-07-30",
    )


def test_create_workflow_from_vault_tasks_translates_dependencies(tmp_path: Path) -> None:
    link, vault_adapter, _vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _create_vault_task(vault_adapter, "T28-04b", "구현")

    workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1",
        "mission-1",
        "project-1",
        [("T28-04a", "설계"), ("T28-04b", "구현")],
        dependencies={"T28-04b": {"T28-04a"}},
    )

    assert len(links) == 2
    assert workflow.task_ids == [entry.domain_task.task_id for entry in links]
    design_id, impl_id = (entry.domain_task.task_id for entry in links)
    assert workflow.dependencies == {impl_id: {design_id}}
    assert links[0].domain_task.workflow_id == "wf-1"


def test_plan_orders_by_dependency(tmp_path: Path) -> None:
    link, vault_adapter, _vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _create_vault_task(vault_adapter, "T28-04b", "구현")
    workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1",
        "mission-1",
        "project-1",
        [("T28-04a", "설계"), ("T28-04b", "구현")],
        dependencies={"T28-04b": {"T28-04a"}},
    )

    order = link.plan(workflow)

    design_id, impl_id = (entry.domain_task.task_id for entry in links)
    assert order == [design_id, impl_id]


def test_transition_and_reflect_updates_domain_and_vault(tmp_path: Path) -> None:
    link, vault_adapter, vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1", "mission-1", "project-1", [("T28-04a", "설계")]
    )

    transitioned = link.transition_and_reflect(
        links[0], TaskStatus.IN_PROGRESS, today="2026-07-30"
    )

    assert transitioned.status is TaskStatus.IN_PROGRESS
    vault_content = (vault_root / "14 Tasks" / "T28-04a.md").read_text(encoding="utf-8")
    assert "status: in-progress" in vault_content


def test_transition_to_unmappable_status_skips_vault(tmp_path: Path) -> None:
    link, vault_adapter, vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1", "mission-1", "project-1", [("T28-04a", "설계")]
    )
    link.transition_and_reflect(links[0], TaskStatus.IN_PROGRESS, today="2026-07-30")

    transitioned = link.transition_and_reflect(links[0], TaskStatus.BLOCKED, today="2026-07-30")

    assert transitioned.status is TaskStatus.BLOCKED
    vault_content = (vault_root / "14 Tasks" / "T28-04a.md").read_text(encoding="utf-8")
    assert "status: in-progress" in vault_content
    assert "status: blocked" not in vault_content


def test_transition_raises_when_domain_lifecycle_rejects_it(tmp_path: Path) -> None:
    link, vault_adapter, _vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1", "mission-1", "project-1", [("T28-04a", "설계")]
    )
    link.transition_and_reflect(links[0], TaskStatus.IN_PROGRESS, today="2026-07-30")
    link.transition_and_reflect(links[0], TaskStatus.REVIEW, today="2026-07-30")
    link.transition_and_reflect(links[0], TaskStatus.DONE, today="2026-07-30")

    # domain 쪽은 DONE -> IN_PROGRESS 재전이가 허용되지 않는다
    # (domain.Task._ALLOWED_TRANSITIONS[DONE] == frozenset()).
    with pytest.raises(Exception):
        link.transition_and_reflect(links[0], TaskStatus.IN_PROGRESS, today="2026-07-30")


def test_is_workflow_complete(tmp_path: Path) -> None:
    link, vault_adapter, _vault_root = _make_link(tmp_path)
    _create_vault_task(vault_adapter, "T28-04a", "설계")
    _create_vault_task(vault_adapter, "T28-04b", "구현")
    _workflow, links = link.create_workflow_from_vault_tasks(
        "wf-1", "mission-1", "project-1", [("T28-04a", "설계"), ("T28-04b", "구현")]
    )

    assert link.is_workflow_complete(links) is False

    for entry in links:
        link.transition_and_reflect(entry, TaskStatus.IN_PROGRESS, today="2026-07-30")
        link.transition_and_reflect(entry, TaskStatus.REVIEW, today="2026-07-30")
        link.transition_and_reflect(entry, TaskStatus.DONE, today="2026-07-30")

    assert link.is_workflow_complete(links) is True
