"""M28-T06 DoD: Conversation Connector가 vault/Core Domain Engine/
AgentManager를 직접 import하지 않고, 항상 기존 Adapter/Connector
(VaultAdapter/WorkflowTaskLink/WorkflowAgentLink)를 통해서만 접근하는지
소스 트리에서 직접 확인한다(ADR-0041)."""

from __future__ import annotations

import ast
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "ai_workspace"
    / "integration"
    / "conversation_workflow_link.py"
)

#: Conversation Connector가 직접 import해서는 안 되는 모듈(접두사 매칭).
#: `vault`/Core Domain의 Workflow·Task·Agent Engine은 반드시
#: VaultAdapter/WorkflowTaskLink/WorkflowAgentLink를 거쳐야 한다.
_FORBIDDEN_MODULE_PREFIXES = (
    "ai_workspace.vault",
    "ai_workspace.interfaces.workflow_engine",
    "ai_workspace.interfaces.task_engine",
    "ai_workspace.interfaces.agent_manager",
    "ai_workspace.interfaces.agent_registry",
    "ai_workspace.interfaces.agent_scheduler",
    "ai_workspace.engines.workflow_engine",
    "ai_workspace.engines.task_engine",
    "ai_workspace.runtime.agent",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_conversation_connector_does_not_import_vault_or_core_engines_directly() -> None:
    modules = _imported_modules(_MODULE_PATH)

    offenders = [
        module
        for module in modules
        for prefix in _FORBIDDEN_MODULE_PREFIXES
        if module == prefix or module.startswith(f"{prefix}.")
    ]

    assert offenders == []


def test_conversation_connector_only_uses_integration_and_domain_modules() -> None:
    modules = _imported_modules(_MODULE_PATH)
    ai_workspace_modules = [m for m in modules if m.startswith("ai_workspace.")]

    assert all(
        m.startswith("ai_workspace.integration.") or m.startswith("ai_workspace.domain.")
        for m in ai_workspace_modules
    )
