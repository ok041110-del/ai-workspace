from __future__ import annotations

import itertools
from collections.abc import Callable

from ai_workspace.domain.agent import Agent, AgentCapability, AgentRole, AgentStatus
from ai_workspace.domain.project import Project
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
from ai_workspace.interfaces.automation_engine import AutomationEngine, DuplicateTriggerError
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


class FakeMemoryEngine(MemoryEngine):
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def remember(self, key: str, value: str) -> None:
        self._store[key] = value

    def recall(self, key: str) -> str | None:
        return self._store.get(key)


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

    def register_trigger(self, trigger_id: str, description: str) -> None:
        if trigger_id in self._triggers:
            raise DuplicateTriggerError(trigger_id)
        self._triggers.append(trigger_id)

    def list_triggers(self) -> list[str]:
        return list(self._triggers)


class FakeEngineAdapter(EngineAdapter):
    def __init__(
        self, capabilities: frozenset[str] = frozenset({"code_generation"}), parallel: bool = True
    ) -> None:
        self._capabilities = capabilities
        self._parallel = parallel
        self._sessions: dict[str, EngineSessionStatus] = {}
        self._id_generator = itertools.count(1)

    def create_session(self) -> str:
        session_id = f"session-{next(self._id_generator)}"
        self._sessions[session_id] = EngineSessionStatus.RUNNING
        return session_id

    def run(self, session_id: str, task: Task) -> EngineResult:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
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

    def run(self, session_id: str, task: Task) -> EngineResult:
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
        self, task: Task, required_capabilities: frozenset[str] = frozenset()
    ) -> EngineResult:
        adapter = self._select(required_capabilities)
        session_id = adapter.create_session()
        result = adapter.run(session_id, task)
        adapter.destroy_session(session_id)
        self._task_status[task.task_id] = (
            EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
        )
        return result

    def run_parallel(
        self, tasks: list[Task], required_capabilities: frozenset[str] = frozenset()
    ) -> list[EngineResult]:
        adapter = self._select(required_capabilities, require_parallel=True)
        results: list[EngineResult] = []
        for task in tasks:
            session_id = adapter.create_session()
            result = adapter.run(session_id, task)
            adapter.destroy_session(session_id)
            self._task_status[task.task_id] = (
                EngineSessionStatus.COMPLETED if result.success else EngineSessionStatus.FAILED
            )
            results.append(result)
        return results

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
