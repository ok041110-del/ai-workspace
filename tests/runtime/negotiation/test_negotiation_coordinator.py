from ai_workspace.adapters.mock_engine_adapter import MockEngineAdapter
from ai_workspace.domain.negotiation import AgentProposal
from ai_workspace.domain.task import Task, TaskStatus
from ai_workspace.domain.workflow import Workflow
from ai_workspace.engines.workflow_engine import InMemoryWorkflowEngine
from ai_workspace.runtime.engine.engine_runtime import InMemoryEngineRuntime
from ai_workspace.runtime.negotiation.negotiation_coordinator import NegotiationCoordinator


def make_task(task_id: str = "t1") -> Task:
    return Task(task_id=task_id, project_id="p1", title="구현하기", status=TaskStatus.TODO)


def make_runtime() -> InMemoryEngineRuntime:
    runtime = InMemoryEngineRuntime()
    runtime.register_engine("claude_code", MockEngineAdapter())
    runtime.register_engine("codex", MockEngineAdapter())
    return runtime


def test_negotiate_adopts_majority_engine_proposal() -> None:
    coordinator = NegotiationCoordinator(make_runtime())
    proposals = [
        AgentProposal(agent_id="a1", engine_name="claude_code"),
        AgentProposal(agent_id="a2", engine_name="claude_code"),
        AgentProposal(agent_id="a3", engine_name="codex"),
    ]

    plan = coordinator.negotiate(make_task(), proposals)

    assert plan.consensus_reached is True
    assert plan.decision.engine_name == "claude_code"


def test_negotiate_falls_back_when_no_proposals() -> None:
    coordinator = NegotiationCoordinator(make_runtime())

    plan = coordinator.negotiate(make_task(), [])

    assert plan.consensus_reached is False
    assert plan.decision.engine_name in {"claude_code", "codex"}


def test_negotiate_falls_back_when_engine_votes_tie() -> None:
    coordinator = NegotiationCoordinator(make_runtime())
    proposals = [
        AgentProposal(agent_id="a1", engine_name="claude_code"),
        AgentProposal(agent_id="a2", engine_name="codex"),
    ]

    plan = coordinator.negotiate(make_task(), proposals)

    assert plan.consensus_reached is False
    assert "동률" in plan.reason


def test_negotiate_tie_breaks_model_by_lowest_priority_within_winning_engine() -> None:
    coordinator = NegotiationCoordinator(make_runtime())
    proposals = [
        AgentProposal(agent_id="a1", engine_name="claude_code", model="sonnet", priority=5),
        AgentProposal(agent_id="a2", engine_name="claude_code", model="opus", priority=1),
        AgentProposal(agent_id="a3", engine_name="codex"),
    ]

    plan = coordinator.negotiate(make_task(), proposals)

    assert plan.consensus_reached is True
    assert plan.decision.engine_name == "claude_code"
    assert plan.decision.model == "opus"


def test_negotiate_adopts_majority_workflow_order_when_proposed() -> None:
    runtime = make_runtime()
    coordinator = NegotiationCoordinator(runtime, InMemoryWorkflowEngine())
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"])
    proposals = [
        AgentProposal(
            agent_id="a1",
            engine_name="claude_code",
            preferred_workflow_order=("t1", "t2"),
        ),
        AgentProposal(
            agent_id="a2",
            engine_name="claude_code",
            preferred_workflow_order=("t1", "t2"),
        ),
        AgentProposal(
            agent_id="a3",
            engine_name="codex",
            preferred_workflow_order=("t2", "t1"),
        ),
    ]

    plan = coordinator.negotiate(make_task(), proposals, workflow=workflow)

    assert plan.consensus_reached is True
    assert plan.workflow_order == ["t1", "t2"]


def test_negotiate_falls_back_when_workflow_order_violates_dependencies() -> None:
    runtime = make_runtime()
    coordinator = NegotiationCoordinator(runtime, InMemoryWorkflowEngine())
    workflow = Workflow(
        workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"], dependencies={"t2": {"t1"}}
    )
    proposals = [
        AgentProposal(
            agent_id="a1",
            engine_name="claude_code",
            preferred_workflow_order=("t2", "t1"),
        ),
        AgentProposal(
            agent_id="a2",
            engine_name="claude_code",
            preferred_workflow_order=("t2", "t1"),
        ),
    ]

    plan = coordinator.negotiate(make_task(), proposals, workflow=workflow)

    assert plan.consensus_reached is False
    assert plan.workflow_order == ["t1", "t2"]


def test_negotiate_uses_plan_when_no_workflow_order_proposed() -> None:
    runtime = make_runtime()
    coordinator = NegotiationCoordinator(runtime, InMemoryWorkflowEngine())
    workflow = Workflow(workflow_id="w1", mission_id="m1", task_ids=["t1", "t2"])
    proposals = [AgentProposal(agent_id="a1", engine_name="claude_code")]

    plan = coordinator.negotiate(make_task(), proposals, workflow=workflow)

    assert plan.consensus_reached is True
    assert plan.workflow_order == ["t1", "t2"]
