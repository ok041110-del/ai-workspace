"""Integration Layer — Workspace Adapter Layer (ADR-0039, Milestone 28-T03).

ADR-0035가 정한 경계를 유지하기 위한 유일한 통로다: **Core Domain
(`domain`/`interfaces`/`engines`)은 `vault`를 모르고, `vault`는 Core
Domain을 모른다.** 이 경계를 넘는 통신은 반드시 이 패키지를 거친다 —
그 외 어떤 모듈도 두 쪽을 동시에 import하지 않는다.

**Workspace Adapter Layer**: 이 패키지가 구현하는 개념적 계층 이름.
"Adapter 3개"가 아니라, 외부 관심사(Vault, Workflow, Agent, 그리고
향후 Runtime/Service/Notification/Sync 등)마다 하나씩 추가되는
확장 가능한 계층으로 정의한다(ADR-0039).

**Adapter vs Connector**(Milestone 28-T05, ADR-0040): 이 패키지는
두 종류의 구성원을 구분한다.

- **Adapter** — 외부 시스템(Vault, Core Domain의 Workflow/Task
  Engine, Core Domain의 Agent Manager/Registry/Scheduler) **하나**
  와의 연결만 담당한다. 비즈니스 로직도, 여러 시스템을 조합하는
  오케스트레이션도 하지 않는다.
- **Connector** — 여러 Adapter를 조합해 유스케이스 하나를
  오케스트레이션한다(예: "Vault Task로 Workflow 만들기", "Workflow
  Task에 Agent 배정하기"). Connector도 자체 비즈니스 로직(상태 전이
  규칙, 선택 알고리즘 등)은 만들지 않는다 — 항상 Adapter가 감싼
  Core Domain Engine에 위임하고, Connector 자신은 조합·ID 변환·
  파생 값 계산만 한다. **Peer Connector**(`WorkflowTaskLink`/
  `WorkflowAgentLink`)는 서로 참조하지 않는다 — 각자 유스케이스
  하나만 책임진다.

**Orchestrating Connector**(Milestone 28-T06, ADR-0041): Peer
Connector와 달리, 여러 Connector/Adapter를 함께 조합해 더 상위
유스케이스(사용자 요청 전체)를 라우팅·조합하는 것 자체가 존재
이유인 Connector. `conversation_workflow_link.ConversationConnector`
가 유일한 예 — Conversation Layer(사용자 입력 해석/요청 라우팅/
결과 조합만 담당, 자연어 해석 자체는 코드가 아니라 AI의 역할)가
Task/Workflow/Agent 요청을 처리하는 유일한 진입점이다. Orchestrating
Connector도 새 비즈니스 로직을 만들지 않는다 — Peer Connector 호출
순서를 배열하고 결과를 묶을 뿐이다.

현재 구성원:

- **Adapter**(Milestone 28-T03): `vault_adapter.VaultAdapter`
  (`vault/`를 아는 유일한 구성원), `workflow_adapter.WorkflowAdapter`
  (`WorkflowEngine`/`TaskEngine` Interface에만 의존),
  `agent_adapter.AgentAdapter`(`AgentManager`/`AgentRegistry`/
  `AgentScheduler` Interface에만 의존).
- **Peer Connector**: `workflow_task_link.WorkflowTaskLink`
  (Milestone 28-T04, Vault Task↔Core Domain Workflow/Task 연결),
  `workflow_agent_link.WorkflowAgentLink`(Milestone 28-T05, Task↔
  Agent 배정/추적).
- **Orchestrating Connector**: `conversation_workflow_link.
  ConversationConnector`(Milestone 28-T06) — 위 두 Peer Connector와
  `VaultAdapter`를 조합해 Conversation Layer 요청 전체(Task 생성→
  Workflow 생성→Agent 배정→Vault 반영, Task 상태 조회/전이)를
  처리한다.

세 Adapter는 서로를 참조하지 않고, Peer Connector끼리도 서로를
참조하지 않는다(예: Agent 배정 책임을 `WorkflowTaskLink`에 얹지
않고 별도 `WorkflowAgentLink`로 분리). Orchestrating Connector만
예외적으로 여러 Peer Connector/Adapter를 조합한다(ADR-0041)."""

from __future__ import annotations
