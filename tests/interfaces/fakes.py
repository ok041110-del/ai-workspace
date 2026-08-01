from __future__ import annotations

import itertools
from collections.abc import Callable

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.budget import Budget, BudgetDecision
from ai_workspace.domain.dashboard import (
    EngineStatus,
    ExecutionRecord,
    ExecutionStats,
    ReliabilityStats,
    WorkspaceStatus,
)
from ai_workspace.domain.knowledge import KnowledgeDocument
from ai_workspace.domain.llm_policy import LLMPolicyDecision
from ai_workspace.domain.project import Project
from ai_workspace.domain.session import WorkspaceSession
from ai_workspace.domain.step import Step
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.interfaces.agent_manager import AgentManager, InvalidAgentTransitionError
from ai_workspace.interfaces.agent_registry import (
    AgentNotRegisteredError,
    AgentRegistry,
    DuplicateAgentRegistrationError,
)
from ai_workspace.interfaces.agent_repository import AgentNotFoundError, AgentRepository
from ai_workspace.interfaces.agent_scheduler import AgentScheduler
from ai_workspace.interfaces.approval_engine import (
    ApprovalActionType,
    ApprovalAlreadyDecidedError,
    ApprovalDecision,
    ApprovalEngine,
    ApprovalRequest,
    ApprovalRequestNotFoundError,
)
from ai_workspace.interfaces.automation_engine import (
    AutomationEngine,
    DuplicateTriggerError,
    TriggerNotBoundError,
    TriggerNotFoundError,
)
from ai_workspace.interfaces.budget_policy_engine import BudgetPolicyEngine
from ai_workspace.interfaces.context_manager import ContextManager, SnapshotNotFoundError
from ai_workspace.interfaces.dashboard_repository import DashboardRepository
from ai_workspace.interfaces.engine_adapter import (
    CostEstimate,
    EngineAdapter,
    EngineExecutionError,
    EngineResult,
    EngineSessionStatus,
    SessionNotFoundError,
)
from ai_workspace.interfaces.engine_runtime import (
    DuplicateEngineError,
    EngineRuntime,
    EngineTaskNotFoundError,
    NoSuitableEngineError,
)
from ai_workspace.interfaces.event_bus import Event, EventBus, SubscriptionNotFoundError
from ai_workspace.interfaces.event_store import EventStore
from ai_workspace.interfaces.execution_environment import (
    ExecutionEnvironment,
    ExecutionNotFoundError,
    ExecutionResult,
)
from ai_workspace.interfaces.interaction_engine import (
    InteractionEngine,
    NormalizedRequest,
    UnsupportedSurfaceError,
)
from ai_workspace.interfaces.knowledge_provider import KnowledgeProvider
from ai_workspace.interfaces.knowledge_repository import (
    KnowledgeDocumentNotFoundError,
    KnowledgeRepository,
)
from ai_workspace.interfaces.llm_policy_engine import LLMPolicyEngine
from ai_workspace.interfaces.memory_engine import MemoryEngine
from ai_workspace.interfaces.project_repository import ProjectNotFoundError, ProjectRepository
from ai_workspace.interfaces.task_engine import TaskEngine, TaskNotFoundError
from ai_workspace.interfaces.workflow_engine import WorkflowEngine

_ALLOWED_AGENT_TRANSITIONS: dict[AgentStatus, frozenset[AgentStatus]] = {
    AgentStatus.IDLE: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.RUNNING: frozenset(
        {
            AgentStatus.WAITING,
            AgentStatus.PAUSED,
            AgentStatus.STOPPED,
            AgentStatus.ERROR,
            AgentStatus.IDLE,
        }
    ),
    AgentStatus.WAITING: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.PAUSED: frozenset({AgentStatus.RUNNING, AgentStatus.STOPPED}),
    AgentStatus.ERROR: frozenset({AgentStatus.STOPPED}),
    AgentStatus.STOPPED: frozenset(),
}


class FakeProjectRepository(ProjectRepository):
    def __init__(self) -> None:
        self._projects: dict[str, Project] = {}

    def load(self, project_id: str) -> Project:
        if project_id not in self._projects:
            raise ProjectNotFoundError(project_id)
        return self._projects[project_id]

    def save(self, project: Project) -> None:
        self._projects[project.project_id] = project

    def list_projects(self) -> list[Project]:
        return list(self._projects.values())


class FakeWorkflowEngine(WorkflowEngine):
    def plan(self, workflow: Workflow) -> list[str]:
        order: list[str] = []
        visited: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visited:
                return
            for dependency in workflow.dependencies.get(task_id, set()):
                visit(dependency)
            visited.add(task_id)
            order.append(task_id)

        for task_id in workflow.task_ids:
            visit(task_id)
        return order


class FakeTaskEngine(TaskEngine):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._id_generator = itertools.count(1)
        self._steps: dict[str, list[Step]] = {}
        self._step_id_generator = itertools.count(1)

    def create_task(self, project_id: str, title: str) -> Task:
        if not project_id or not title:
            raise ValueError("project_id와 title은 비어 있을 수 없습니다.")
        task_id = f"task-{next(self._id_generator)}"
        task = Task(task_id=task_id, project_id=project_id, title=title, status=TaskStatus.TODO)
        self._tasks[task_id] = task
        return task

    def transition(self, task: Task, new_status: TaskStatus) -> Task:
        task.transition_to(new_status)
        return task

    def get_task(self, task_id: str) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def record_step(self, task_id: str, description: str) -> Step:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        step = Step(
            step_id=f"step-{next(self._step_id_generator)}",
            task_id=task_id,
            description=description,
        )
        self._steps.setdefault(task_id, []).append(step)
        return step

    def get_steps(self, task_id: str) -> list[Step]:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return list(self._steps.get(task_id, []))


class FakeMemoryEngine(MemoryEngine):
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._store[key] = value

    def recall(self, key: str) -> str | None:
        return self._store.get(key)

    def search(self, query: str) -> list[str]:
        return [key for key, value in self._store.items() if query in value]


class FakeApprovalEngine(ApprovalEngine):
    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._id_generator = itertools.count(1)

    def submit(self, action_type: ApprovalActionType, description: str) -> ApprovalRequest:
        request_id = f"approval-{next(self._id_generator)}"
        request = ApprovalRequest(
            request_id=request_id, action_type=action_type, description=description
        )
        self._requests[request_id] = request
        return request

    def decide(self, request_id: str, approved: bool) -> ApprovalRequest:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        if request.decision != ApprovalDecision.PENDING:
            raise ApprovalAlreadyDecidedError(request_id)
        request.decision = ApprovalDecision.APPROVED if approved else ApprovalDecision.REJECTED
        return request

    def is_approved(self, request_id: str) -> bool:
        request = self._requests.get(request_id)
        if request is None:
            raise ApprovalRequestNotFoundError(request_id)
        return request.decision == ApprovalDecision.APPROVED


class FakeAutomationEngine(AutomationEngine):
    def __init__(self) -> None:
        self._triggers: list[str] = []
        self._workflows: dict[str, Workflow] = {}

    def register_trigger(self, trigger_id: str, description: str) -> None:
        if trigger_id in self._triggers:
            raise DuplicateTriggerError(trigger_id)
        self._triggers.append(trigger_id)

    def list_triggers(self) -> list[str]:
        return list(self._triggers)

    def bind_workflow(self, trigger_id: str, workflow: Workflow) -> None:
        if trigger_id not in self._triggers:
            raise TriggerNotFoundError(trigger_id)
        self._workflows[trigger_id] = workflow

    def fire(self, trigger_id: str) -> Workflow:
        if trigger_id not in self._triggers:
            raise TriggerNotFoundError(trigger_id)
        if trigger_id not in self._workflows:
            raise TriggerNotBoundError(trigger_id)
        return self._workflows[trigger_id]


class FakeEngineAdapter(EngineAdapter):
    def __init__(
        self, capabilities: frozenset[str] = frozenset({"code_generation"}), parallel: bool = True
    ) -> None:
        self._capabilities = capabilities
        self._parallel = parallel
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)
        self.received_models: list[str | None] = []

    def create_session(self) -> str:
        session_id = f"session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        self.received_models.append(model)
        self._sessions[session_id] = EngineSessionStatus.COMPLETED
        return EngineResult(success=True, output=f"{task.task_id} 완료")

    def cancel(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        self._sessions[session_id] = EngineSessionStatus.CANCELLED

    def status(self, session_id: str) -> EngineSessionStatus:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions[session_id]

    def destroy_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        del self._sessions[session_id]

    def capabilities(self) -> frozenset[str]:
        return self._capabilities

    def supports_parallel(self) -> bool:
        return self._parallel

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=100, estimated_cost_usd=0.01)


class FailingFakeEngineAdapter(EngineAdapter):
    def create_session(self) -> str:
        return "session-failing"

    def run(self, session_id: str, task: Task, *, model: str | None = None) -> EngineResult:
        raise EngineExecutionError("구현 엔진 프로세스를 실행할 수 없습니다.")

    def cancel(self, session_id: str) -> None:
        raise SessionNotFoundError(session_id)

    def status(self, session_id: str) -> EngineSessionStatus:
        raise SessionNotFoundError(session_id)

    def destroy_session(self, session_id: str) -> None:
        raise SessionNotFoundError(session_id)

    def capabilities(self) -> frozenset[str]:
        return frozenset()

    def supports_parallel(self) -> bool:
        return False

    def estimate_cost(self, task: Task) -> CostEstimate:
        return CostEstimate(estimated_tokens=0, estimated_cost_usd=0.0)


class FakeExecutionEnvironment(ExecutionEnvironment):
    """실제 프로세스를 실행하지 않고 미리 준비된 결과/예외를 반환하는
    테스트용 구현체(M11-T01). `execute()`에 전달된 명령을 기록해,
    `EngineAdapter`가 이 인터페이스를 통해서만 명령을 실행하는지
    검증할 수 있다."""

    def __init__(self) -> None:
        self.result: ExecutionResult | None = None
        self.exception: BaseException | None = None
        self.executed_commands: list[list[str]] = []
        self.cancelled_ids: list[str] = []
        self._running: set[str] = set()

    def execute(
        self,
        execution_id: str,
        command: list[str],
        *,
        cwd: str | None = None,
        timeout: float | None = None,
    ) -> ExecutionResult:
        self.executed_commands.append(command)
        if self.exception is not None:
            raise self.exception
        self._running.add(execution_id)
        try:
            if self.result is not None:
                return self.result
            return ExecutionResult(returncode=0, stdout="", stderr="")
        finally:
            self._running.discard(execution_id)

    def cancel(self, execution_id: str) -> None:
        if execution_id not in self._running:
            raise ExecutionNotFoundError(execution_id)
        self.cancelled_ids.append(execution_id)
        self._running.discard(execution_id)


class FakeEngineRuntime(EngineRuntime):
    def __init__(self) -> None:
        self._engines: dict[str, EngineAdapter] = {}
        self._task_status: dict[str, EngineSessionStatus] = {}

    def register_engine(self, name: str, adapter: EngineAdapter) -> None:
        if name in self._engines:
            raise DuplicateEngineError(name)
        self._engines[name] = adapter

    def _select(
        self, required_capabilities: frozenset[str], require_parallel: bool = False
    ) -> EngineAdapter:
        for adapter in self._engines.values():
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            if require_parallel and not adapter.supports_parallel():
                continue
            return adapter
        raise NoSuitableEngineError(required_capabilities)

    def run(
        self,
        task: Task,
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> EngineResult:
        adapter = self._select(required_capabilities)
        session_id = adapter.create_session()
        result = adapter.run(session_id, task, model=model)
        adapter.destroy_session(session_id)
        self._task_status[task.task_id] = (
            EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
        )
        return result

    def run_parallel(
        self,
        tasks: list[Task],
        required_capabilities: frozenset[str] = frozenset(),
        *,
        model: str | None = None,
    ) -> list[EngineResult]:
        adapter = self._select(required_capabilities, require_parallel=True)
        results: list[EngineResult] = []
        for task in tasks:
            try:
                session_id = adapter.create_session()
                result = adapter.run(session_id, task, model=model)
                adapter.destroy_session(session_id)
            except BaseException as exc:
                self._task_status[task.task_id] = EngineSessionStatus.FAILED
                results.append(EngineResult(success=False, output="", error=str(exc)))
                continue
            self._task_status[task.task_id] = (
                EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
            )
            results.append(result)
        return results

    def run_ensemble(
        self,
        task: Task,
        engine_names: list[str],
        *,
        model: str | None = None,
    ) -> dict[str, EngineResult]:
        results: dict[str, EngineResult] = {}
        for name in engine_names:
            adapter = self._engines.get(name)
            if adapter is None:
                results[name] = EngineResult(
                    success=False, output="", error=f"engine '{name}' not registered"
                )
                continue
            try:
                session_id = adapter.create_session()
                results[name] = adapter.run(session_id, task, model=model)
                adapter.destroy_session(session_id)
            except BaseException as exc:
                results[name] = EngineResult(success=False, output="", error=str(exc))
        return results

    def estimate_cost(
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> CostEstimate:
        adapter = self._select(required_capabilities)
        return adapter.estimate_cost(task)

    def cancel(self, task_id: str) -> None:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        self._task_status[task_id] = EngineSessionStatus.CANCELLED

    def status(self, task_id: str) -> EngineSessionStatus:
        if task_id not in self._task_status:
            raise EngineTaskNotFoundError(task_id)
        return self._task_status[task_id]


class FakeAgentManager(AgentManager):
    def __init__(self) -> None:
        self._id_generator = itertools.count(1)

    def create(
        self, role: AgentRole, capabilities: frozenset[AgentCapability] = frozenset()
    ) -> Agent:
        agent_id = f"agent-{next(self._id_generator)}"
        return Agent(agent_id=agent_id, role=role, capabilities=capabilities)

    def transition(self, agent: Agent, new_status: AgentStatus) -> Agent:
        if new_status not in _ALLOWED_AGENT_TRANSITIONS[agent.status]:
            raise InvalidAgentTransitionError(
                f"{agent.status} -> {new_status} 전이는 허용되지 않습니다."
            )
        agent.status = new_status
        return agent


class FakeAgentRegistry(AgentRegistry):
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        if agent.agent_id in self._agents:
            raise DuplicateAgentRegistrationError(agent.agent_id)
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        if agent_id not in self._agents:
            raise AgentNotRegisteredError(agent_id)
        return self._agents[agent_id]

    def list_active(self) -> list[Agent]:
        return list(self._agents.values())

    def remove(self, agent_id: str) -> None:
        if agent_id not in self._agents:
            raise AgentNotRegisteredError(agent_id)
        del self._agents[agent_id]


class FakeAgentScheduler(AgentScheduler):
    def select(
        self, candidates: list[Agent], capability: AgentCapability, max_count: int = 1
    ) -> list[Agent]:
        matched = [agent for agent in candidates if capability in agent.capabilities]
        return matched[:max_count]


class FakeAgentRepository(AgentRepository):
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def load(self, agent_id: str) -> Agent:
        if agent_id not in self._agents:
            raise AgentNotFoundError(agent_id)
        return self._agents[agent_id]

    def save(self, agent: Agent) -> None:
        self._agents[agent.agent_id] = agent

    def list_agents(self) -> list[Agent]:
        return list(self._agents.values())


class FakeEventBus(EventBus):
    def __init__(self) -> None:
        self._subscribers: dict[str, Callable[[Event], None]] = {}
        self._id_generator = itertools.count(1)

    def publish(self, event: Event) -> None:
        for handler in list(self._subscribers.values()):
            try:
                handler(event)
            except Exception:
                pass

    def subscribe(self, handler: Callable[[Event], None]) -> str:
        subscription_id = f"sub-{next(self._id_generator)}"
        self._subscribers[subscription_id] = handler
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        if subscription_id not in self._subscribers:
            raise SubscriptionNotFoundError(subscription_id)
        del self._subscribers[subscription_id]


class FakeEventStore(EventStore):
    def __init__(self) -> None:
        self._events: list[Event] = []

    def record(self, event: Event) -> None:
        self._events.append(event)

    def replay(self, since_event_id: str | None = None) -> list[Event]:
        if since_event_id is None:
            return list(self._events)
        for index, event in enumerate(self._events):
            if event.event_id == since_event_id:
                return list(self._events[index + 1 :])
        return []


class FakeContextManager(ContextManager):
    def __init__(self) -> None:
        self._snapshots: dict[str, dict[str, str]] = {}
        self._id_generator = itertools.count(1)
        self._latest_snapshot_by_project: dict[str, str] = {}

    def assemble_context(self, session: WorkspaceSession) -> dict[str, str]:
        context: dict[str, str] = {}
        if session.current_project_id is not None:
            context["project_id"] = session.current_project_id
        if session.current_mission_id is not None:
            context["mission_id"] = session.current_mission_id
        if session.memory_snapshot_id in self._snapshots:
            context.update(self._snapshots[session.memory_snapshot_id])
        return context

    def create_snapshot(self, session: WorkspaceSession, summary: str | None = None) -> str:
        snapshot_id = f"snapshot-{next(self._id_generator)}"
        context = self.assemble_context(session)
        if summary is not None:
            context["summary"] = summary
        self._snapshots[snapshot_id] = context
        if session.current_project_id is not None:
            self._latest_snapshot_by_project[session.current_project_id] = snapshot_id
        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> dict[str, str]:
        if snapshot_id not in self._snapshots:
            raise SnapshotNotFoundError(snapshot_id)
        return dict(self._snapshots[snapshot_id])

    def latest_snapshot_id(self, project_id: str) -> str | None:
        return self._latest_snapshot_by_project.get(project_id)

    def find_snapshots(self, query: str) -> list[str]:
        return [
            snapshot_id
            for snapshot_id, context in self._snapshots.items()
            if any(query in value for value in context.values())
        ]


class FakeInteractionEngine(InteractionEngine):
    def __init__(self, surfaces: frozenset[str] = frozenset({"cli"})) -> None:
        self._surfaces = surfaces

    def normalize(
        self, surface: str, raw_input: str, session_id: str | None = None
    ) -> NormalizedRequest:
        if surface not in self._surfaces:
            raise UnsupportedSurfaceError(surface)
        return NormalizedRequest(surface=surface, text=raw_input.strip(), session_id=session_id)

    def format_response(self, surface: str, message: str) -> str:
        if surface not in self._surfaces:
            raise UnsupportedSurfaceError(surface)
        return message

    def supported_surfaces(self) -> frozenset[str]:
        return self._surfaces


class FakeLLMPolicyEngine(LLMPolicyEngine):
    def __init__(self, rules: dict[AgentRole, LLMPolicyDecision] | None = None) -> None:
        self._rules = dict(rules) if rules is not None else {}

    def select(self, role: AgentRole) -> LLMPolicyDecision | None:
        return self._rules.get(role)


class FakeBudgetPolicyEngine(BudgetPolicyEngine):
    def __init__(self, budget: Budget | None = None) -> None:
        self._budget = budget

    def check(self, estimate: CostEstimate) -> BudgetDecision:
        if self._budget is None:
            return BudgetDecision(allowed=True)
        if (
            self._budget.max_tokens is not None
            and estimate.estimated_tokens > self._budget.max_tokens
        ):
            return BudgetDecision(allowed=False, reason="max_tokens exceeded")
        if (
            self._budget.max_cost_usd is not None
            and estimate.estimated_cost_usd > self._budget.max_cost_usd
        ):
            return BudgetDecision(allowed=False, reason="max_cost_usd exceeded")
        return BudgetDecision(allowed=True)


class FakeKnowledgeRepository(KnowledgeRepository):
    def __init__(self, documents: list[KnowledgeDocument] | None = None) -> None:
        self._documents = list(documents) if documents is not None else []

    def list_all(self) -> list[KnowledgeDocument]:
        return list(self._documents)

    def get(self, document_id: str) -> KnowledgeDocument:
        for document in self._documents:
            if document.document_id == document_id:
                return document
        raise KnowledgeDocumentNotFoundError(document_id)


class FakeKnowledgeProvider(KnowledgeProvider):
    def __init__(self, documents: list[KnowledgeDocument] | None = None) -> None:
        self._documents = list(documents) if documents is not None else []
        self.received_queries: list[str] = []

    def provide(self, query: str) -> list[KnowledgeDocument]:
        self.received_queries.append(query)
        return list(self._documents)


class FakeDashboardRepository(DashboardRepository):
    def __init__(self) -> None:
        self._workspace_status = WorkspaceStatus(
            project_name=None, current_task_title=None, status="idle", started_at=None
        )
        self._engine_statuses: dict[str, EngineStatus] = {}
        self._executions: list[ExecutionRecord] = []
        self.auth_failure_calls: list[str] = []

    def record_execution_started(
        self, *, engine_name: str, task_title: str, started_at: str
    ) -> None:
        self._workspace_status = WorkspaceStatus(
            project_name=self._workspace_status.project_name,
            current_task_title=task_title,
            status="running",
            started_at=started_at,
        )
        self._engine_statuses[engine_name] = EngineStatus.RUNNING

    def record_execution_completed(self, record: ExecutionRecord) -> None:
        self._executions.insert(0, record)
        self._engine_statuses[record.engine] = (
            EngineStatus.READY if record.success else EngineStatus.ERROR
        )
        self._workspace_status = WorkspaceStatus(
            project_name=self._workspace_status.project_name,
            current_task_title=None,
            status="idle",
            started_at=None,
        )

    def record_authentication_failure(self, *, engine_name: str) -> None:
        self.auth_failure_calls.append(engine_name)
        self._engine_statuses[engine_name] = EngineStatus.AUTH_REQUIRED

    def workspace_status(self) -> WorkspaceStatus:
        return self._workspace_status

    def engine_statuses(self) -> dict[str, EngineStatus]:
        return dict(self._engine_statuses)

    def recent_executions(self, limit: int = 20) -> list[ExecutionRecord]:
        return list(self._executions[:limit])

    def execution_stats(self) -> ExecutionStats:
        return ExecutionStats(
            total=len(self._executions),
            success=sum(1 for record in self._executions if record.success),
            failure=sum(
                1
                for record in self._executions
                if not record.success and not record.cancelled and not record.timed_out
            ),
            cancelled=sum(1 for record in self._executions if record.cancelled),
            timed_out=sum(1 for record in self._executions if record.timed_out),
        )

    def reliability_stats(self) -> ReliabilityStats:
        return ReliabilityStats(
            retry_count=sum(record.retry_count for record in self._executions),
            timeout_count=sum(1 for record in self._executions if record.timed_out),
            cancelled_count=sum(1 for record in self._executions if record.cancelled),
            authentication_failure_count=len(self.auth_failure_calls),
        )
