"""Integration Layer — Workspace Adapter Layer (ADR-0039, Milestone 28-T03).

ADR-0035가 정한 경계를 유지하기 위한 유일한 통로다: **Core Domain
(`domain`/`interfaces`/`engines`)은 `vault`를 모르고, `vault`는 Core
Domain을 모른다.** 이 경계를 넘는 통신은 반드시 이 패키지의 Adapter를
거친다 — 그 외 어떤 모듈도 두 쪽을 동시에 import하지 않는다.

**Workspace Adapter Layer**: 이 패키지가 구현하는 개념적 계층 이름.
"Adapter 3개"가 아니라, 외부 관심사(Vault, Workflow, Agent, 그리고
향후 Runtime/Service/Notification/Sync 등)마다 하나씩 추가되는
확장 가능한 계층으로 정의한다(ADR-0039). 각 Adapter는 연결·변환·
위임만 담당하고 비즈니스 로직이나 Workspace Intelligence(자연어
해석, 계획 수립 등)를 갖지 않는다 — 그런 로직은 항상 Core Domain
(Engine)이나 Conversation Layer(Milestone 28-T06)의 몫이다.

현재 구성원(Milestone 28-T03):

- `vault_adapter.VaultAdapter` — `vault/`를 아는 유일한 구성원.
- `workflow_adapter.WorkflowAdapter` — `WorkflowEngine`/`TaskEngine`
  Interface에만 의존.
- `agent_adapter.AgentAdapter` — `AgentManager`/`AgentRegistry`/
  `AgentScheduler` Interface에만 의존.

세 Adapter는 서로를 참조하지 않는다 — Task↔Workflow 연결
(Milestone 28-T04), Workflow↔Agent 연결(Milestone 28-T05)은 이
Adapter들을 조합해서 쓰는 상위 호출자(Conversation Layer 등)의
책임이다."""

from __future__ import annotations
