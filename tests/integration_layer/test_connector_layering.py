"""M28 Architecture Freeze: Integration Layer 내부 참조 방향 검증
(docs/ARCHITECTURE.md §8 규칙 19, ADR-0040/ADR-0041).

Adapter는 다른 Adapter/Connector를 참조하지 않는다. Peer Connector는
Adapter만 조합하고 다른 Peer Connector를 참조하지 않는다. Orchestrating
Connector만 Peer Connector/Adapter를 함께 조합할 수 있고, 그 반대
방향(Adapter/Peer Connector가 Orchestrating Connector를 참조)은
금지된다 — 참조는 항상 Orchestrating Connector → (Peer Connector |
Adapter) → Core 한 방향으로만 흐른다."""

from __future__ import annotations

import ast
from pathlib import Path

_INTEGRATION_DIR = Path(__file__).resolve().parents[2] / "src" / "ai_workspace" / "integration"

_ADAPTERS = {"vault_adapter", "workflow_adapter", "agent_adapter", "knowledge_adapter"}
_PEER_CONNECTORS = {"workflow_task_link", "workflow_agent_link"}
_ORCHESTRATING_CONNECTORS = {"conversation_workflow_link"}
#: 어떤 Adapter/Connector 계층에서나 참조할 수 있는 순수 값 객체 모듈.
#: 로직이 없으므로(값 객체 정의만) 계층 규칙의 대상이 아니다.
_SHARED_VALUE_MODULES = {"models"}


def _integration_imports(module_name: str) -> set[str]:
    path = _INTEGRATION_DIR / f"{module_name}.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("ai_workspace.integration."):
                imported.add(node.module.rsplit(".", 1)[-1])
    return imported


def test_adapters_do_not_reference_other_integration_modules() -> None:
    for adapter in _ADAPTERS:
        imports = _integration_imports(adapter) - _SHARED_VALUE_MODULES
        assert imports == set(), f"{adapter}가 다른 integration 모듈을 참조합니다: {imports}"


def test_peer_connectors_only_reference_adapters() -> None:
    allowed = _ADAPTERS | _SHARED_VALUE_MODULES
    for connector in _PEER_CONNECTORS:
        imports = _integration_imports(connector)
        assert imports <= allowed, (
            f"{connector}가 Adapter가 아닌 모듈을 참조합니다: {imports - allowed}"
        )


def test_nothing_references_orchestrating_connectors() -> None:
    for module_path in _INTEGRATION_DIR.glob("*.py"):
        module_name = module_path.stem
        if module_name in _ORCHESTRATING_CONNECTORS or module_name == "__init__":
            continue
        imports = _integration_imports(module_name)
        offending = imports & _ORCHESTRATING_CONNECTORS
        assert offending == set(), (
            f"{module_name}이 Orchestrating Connector를 참조합니다: {offending}"
        )
