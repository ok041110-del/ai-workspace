from __future__ import annotations

import pytest

from ai_workspace.domain.agent import Agent, AgentRole
from ai_workspace.events.event_bus import InMemoryEventBus
from ai_workspace.interfaces.event_bus import Event
from ai_workspace.interfaces.remote_agent_dispatcher import AgentUnreachableError
from ai_workspace.runtime.agent.remote_agent_dispatcher import LoopbackAgentDispatcher


def test_dispatch_delivers_event_to_registered_location_bus() -> None:
    dispatcher = LoopbackAgentDispatcher()
    bus = InMemoryEventBus()
    received: list[Event] = []
    bus.subscribe(received.append)
    dispatcher.register_location("worker-1", bus)
    agent = Agent(agent_id="a1", role=AgentRole.CODING, location="worker-1")
    event = Event(event_id="e1", event_type="mission_planned")

    dispatcher.dispatch(agent, event)

    assert received == [event]


def test_dispatch_does_not_deliver_to_other_locations() -> None:
    dispatcher = LoopbackAgentDispatcher()
    bus_a = InMemoryEventBus()
    bus_b = InMemoryEventBus()
    received_b: list[Event] = []
    bus_b.subscribe(received_b.append)
    dispatcher.register_location("worker-a", bus_a)
    dispatcher.register_location("worker-b", bus_b)
    agent = Agent(agent_id="a1", role=AgentRole.CODING, location="worker-a")

    dispatcher.dispatch(agent, Event(event_id="e1", event_type="x"))

    assert received_b == []


def test_dispatch_unregistered_location_raises() -> None:
    dispatcher = LoopbackAgentDispatcher()
    agent = Agent(agent_id="a1", role=AgentRole.CODING, location="unknown")

    with pytest.raises(AgentUnreachableError):
        dispatcher.dispatch(agent, Event(event_id="e1", event_type="x"))


def test_dispatch_agent_without_location_raises() -> None:
    dispatcher = LoopbackAgentDispatcher()
    agent = Agent(agent_id="a1", role=AgentRole.CODING)

    with pytest.raises(AgentUnreachableError):
        dispatcher.dispatch(agent, Event(event_id="e1", event_type="x"))


def test_register_location_overwrites_previous_registration() -> None:
    dispatcher = LoopbackAgentDispatcher()
    old_bus = InMemoryEventBus()
    new_bus = InMemoryEventBus()
    received_new: list[Event] = []
    new_bus.subscribe(received_new.append)
    dispatcher.register_location("worker-1", old_bus)
    dispatcher.register_location("worker-1", new_bus)
    agent = Agent(agent_id="a1", role=AgentRole.CODING, location="worker-1")

    dispatcher.dispatch(agent, Event(event_id="e1", event_type="x"))

    assert received_new == [Event(event_id="e1", event_type="x")]
