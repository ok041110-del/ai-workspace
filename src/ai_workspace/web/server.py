from __future__ import annotations

import dataclasses
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from ai_workspace.engines.authentication_manager import InMemoryAuthenticationManager
from ai_workspace.engines.engine_selection_policy import InMemoryEngineSelectionPolicy
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.guardian.service import ArchitectureGuardianService
from ai_workspace.integration.agent_adapter import AgentAdapter
from ai_workspace.integration.vault_adapter import VaultAdapter
from ai_workspace.intelligence.capability_service import CapabilityIntelligenceService
from ai_workspace.intelligence.experience_service import ExperienceIntelligenceService
from ai_workspace.intelligence.recommendation_explanation_service import (
    RecommendationExplanationService,
)
from ai_workspace.intelligence.recommendation_service import RecommendationIntelligenceService
from ai_workspace.intelligence.report import ProjectIntelligenceService
from ai_workspace.memory.execution_memory_store import ExecutionMemoryStore
from ai_workspace.runtime.agent.agent_manager import InMemoryAgentManager
from ai_workspace.runtime.agent.agent_registry import InMemoryAgentRegistry
from ai_workspace.runtime.agent.agent_scheduler import InMemoryAgentScheduler
from ai_workspace.runtime.automation.automation_action_executor import AutomationActionExecutor
from ai_workspace.runtime.automation.automation_repository import InMemoryAutomationRepository
from ai_workspace.runtime.automation.automation_scheduler import AutomationScheduler
from ai_workspace.runtime.automation.automation_service import AutomationService
from ai_workspace.runtime.dashboard.dashboard_repository import InMemoryDashboardRepository
from ai_workspace.runtime.dashboard.dashboard_service import DashboardService
from ai_workspace.runtime.engine.engine_registry import InMemoryEngineRegistry
from ai_workspace.runtime.execution.execution_dispatcher import ExecutionDispatcher
from ai_workspace.runtime.execution.recommendation_execution_service import (
    RecommendationExecutionService,
)
from ai_workspace.runtime.execution.recommendation_orchestration_service import (
    RecommendationOrchestrationService,
)
from ai_workspace.runtime.production.config import ProductionConfig
from ai_workspace.runtime.production.config_loader import load_production_config
from ai_workspace.runtime.production.health import HealthMonitor
from ai_workspace.runtime.production.lifecycle import LifecycleManager
from ai_workspace.runtime.production.logging_setup import configure_logging
from ai_workspace.storage.file_memory_engine import FileMemoryEngine
from ai_workspace.web.app import create_app


def build_app(
    *, project_name: str | None = None, config: ProductionConfig | None = None
) -> FastAPI:
    """`workspace start`가 실행할 FastAPI 앱을 조립한다(M20-T04,
    M21-T05, M22-T05). `EventBus`/`InMemoryDashboardRepository`/
    `DashboardService`/Automation/Production 컴포넌트를 이 함수
    하나로 조립해, 실제 서버 기동(`uvicorn.run`)과 분리한다 —
    이렇게 하면 실제 소켓을 열지 않고도 `TestClient`로 테스트할 수
    있다. `config`를 주지 않으면 `load_production_config()`(기본값
    → 설정 파일 → Environment Variable)로 만든다.

    `EngineRegistry`/`AuthenticationManager`/`ExecutionDispatcher`는
    Automation의 RUN_TASK Action이 사용할 실행 파이프라인이다(M21
    사용자 승인 조건 5 — `ExecutionDispatcher`가 유일한 실행
    진입점). 이 시점에는 아직 어떤 `EngineAdapter`도 등록돼 있지
    않다 — 실제 Engine 등록·인증은 Workspace Core(CLI 경로)의
    책임이고, 이 Dashboard/Automation 서버 모듈은 그 등록을 대신하지
    않는다(Out of Scope). 그 상태에서 RUN_TASK가 발동하면
    `EngineNotRegisteredError`가 발생하지만, `AutomationScheduler`
    가 이를 삼켜(swallow) 다른 Rule 평가에 영향을 주지 않는다.

    `LifecycleManager`/`HealthMonitor`는 여기서 조립된 컴포넌트를
    그대로 주입받을 뿐(사용자 승인 조건 2/3 — 생성이 아닌 생명주기
    관리, 조회 전용) 새로운 컴포넌트를 만들지 않는다.

    `VaultAdapter`/`AgentAdapter`/`RecommendationExecutionService`
    (M38)는 M29~M37이 만들었지만 이 Composition Root에는 한 번도
    조립된 적이 없던 컴포넌트다 — 새 정책 없이 기존 생성자 그대로
    조립만 한다(`tests/runtime/execution/test_recommendation_execution_service.py`
    와 동일한 패턴). `RUN_RECOMMENDATION` Action이 `AutomationScheduler`
    로 발동하면 `AutomationActionExecutor`가 `RecommendationOrchestrationService.
    publish(manual_trigger=True)`(M43)를 호출한다 — `ExecutionGate`는
    `source=next_task`만 여전히 승인한다(M36과 동일, 새 정책 없음).

    `ExecutionMemoryStore`(M39)도 이 시점에 처음 조립돼
    `RecommendationExecutionService`에 주입된다 — 매 실행 결과가
    `ExecutionMemory`로 자동 기록된다(ADR-0053). `FileMemoryEngine`
    (M50, ADR-0067)이 `<vault_root>/.ai-workspace-data/`에 JSON으로
    영속화해, 서버 재시작 후에도 학습 이력이 유지된다 — M39 당시의
    `InMemoryMemoryEngine`(프로세스 생존 중에만 유지) 한계는 이번
    Milestone에서 해소됐다.

    `ExperienceIntelligenceService`(M40)+`RecommendationOrchestrationService`
    (M43)도 이 시점에 처음 조립된다 — `RecommendationExecutionService`
    는 M43부터 Recommendation 의존성을 갖지 않으므로(ADR-0059),
    Orchestration Service가 Experience 조회 → Recommendation 계산
    (Adaptation 포함) → Explanation 기록(M44) → Guardian 평가(M48)
    → Execution 위임까지 전체 흐름을 제어한다.
    `RecommendationExplanationService`(M44)도 이 시점에 조립돼
    선택적으로 주입된다.

    `ArchitectureGuardianService`(M41)도 이 시점에 처음 자동 실행
    경로에 조립된다(ADR-0065) — `vault_root`가 곧 Repository Root
    (ADR-0037)이므로 `src_root`는 `vault_root/src/ai_workspace`로
    계산한다. Guardian이 위반을 발견하면 Recommendation/Explanation
    은 그대로 발행되고 Execution만 차단된다(`ExecutionGate`,
    M36)."""
    config = config or load_production_config()

    event_bus = InMemoryEventBus()
    dashboard_repository = InMemoryDashboardRepository(
        event_bus=event_bus, project_name=project_name
    )

    engine_registry = InMemoryEngineRegistry()
    authentication_manager = InMemoryAuthenticationManager()
    execution_dispatcher = ExecutionDispatcher(
        engine_registry=engine_registry,
        authentication_manager=authentication_manager,
        event_bus=event_bus,
    )
    engine_selection_policy = InMemoryEngineSelectionPolicy()

    vault_adapter = VaultAdapter(Path(config.vault_root))
    agent_adapter = AgentAdapter(
        InMemoryAgentManager(), InMemoryAgentRegistry(), InMemoryAgentScheduler()
    )
    execution_memory_store = ExecutionMemoryStore(
        FileMemoryEngine(Path(config.vault_root) / ".ai-workspace-data")
    )
    recommendation_service = RecommendationIntelligenceService(
        vault_adapter,
        ProjectIntelligenceService(vault_adapter, agent_adapter),
        CapabilityIntelligenceService(agent_adapter, vault_adapter),
    )
    recommendation_execution_service = RecommendationExecutionService(
        vault_adapter,
        engine_registry,
        engine_selection_policy,
        execution_dispatcher,
        execution_memory_store,
    )
    experience_service = ExperienceIntelligenceService(vault_adapter, execution_memory_store)
    explanation_service = RecommendationExplanationService(vault_adapter)
    guardian_service = ArchitectureGuardianService(
        vault_adapter, Path(config.vault_root) / "src" / "ai_workspace"
    )
    recommendation_orchestration_service = RecommendationOrchestrationService(
        experience_service,
        recommendation_service,
        recommendation_execution_service,
        explanation_service,
        guardian_service,
    )

    automation_repository = InMemoryAutomationRepository()
    automation_service = AutomationService(automation_repository=automation_repository)
    action_executor = AutomationActionExecutor(
        engine_registry=engine_registry,
        engine_selection_policy=engine_selection_policy,
        execution_dispatcher=execution_dispatcher,
        recommendation_orchestration_service=recommendation_orchestration_service,
    )
    automation_scheduler = AutomationScheduler(
        automation_repository=automation_repository, action_executor=action_executor
    )
    automation_scheduler.bind_event_bus(event_bus)

    dashboard_service = DashboardService(
        dashboard_repository=dashboard_repository, automation_service=automation_service
    )

    lifecycle_manager = LifecycleManager(
        automation_scheduler=automation_scheduler, dashboard_service=dashboard_service
    )
    health_monitor = HealthMonitor(
        lifecycle_manager=lifecycle_manager,
        dashboard_service=dashboard_service,
        automation_scheduler=automation_scheduler,
        event_bus=event_bus,
        engine_registry=engine_registry,
    )
    dashboard_service.attach_health_monitor(health_monitor)

    return create_app(
        dashboard_service=dashboard_service,
        event_bus=event_bus,
        automation_service=automation_service,
        automation_scheduler=automation_scheduler,
        automation_tick_seconds=config.automation_tick_seconds,
        production_config=config,
        lifecycle_manager=lifecycle_manager,
        health_monitor=health_monitor,
        execution_memory_store=execution_memory_store,
    )


def run_server(
    *,
    host: str | None = None,
    port: int | None = None,
    project_name: str | None = None,
    config_path: str | Path | None = None,
    log_file: str | Path | None = None,
) -> None:
    """`workspace start`의 실제 진입점 — `uvicorn.run()`을 호출해
    상시 실행되는 서버를 띄운다. 기존 CLI 명령(1회성 실행)에는 전혀
    영향을 주지 않는다 — 서버는 이 함수가 호출될 때만 실행된다.

    `host`/`port`를 명시하면 Configuration(설정 파일/Environment
    Variable)보다 우선한다(CLI 인자가 가장 구체적인 값). 둘 다
    `None`이면(기본값) Configuration이 정한 값을 그대로 쓴다."""
    loaded_config = load_production_config(config_path=config_path)
    config = dataclasses.replace(
        loaded_config,
        host=host if host is not None else loaded_config.host,
        port=port if port is not None else loaded_config.port,
    )
    configure_logging(config, log_file=log_file)
    app = build_app(project_name=project_name, config=config)
    uvicorn.run(app, host=config.host, port=config.port)
