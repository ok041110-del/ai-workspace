"""Intelligence Layer (ADR-0043, Milestone 29).

Project/Workflow/Task/Agent 데이터를 종합해 **Project Snapshot/
Health/Risk/Recommendation**을 산출하는 **Read Only Query Layer**다.
`integration/`(Integration Layer)과 같은 층위에서 그 위에 얹히는
신규 최상위 패키지로, Integration Layer가 이미 노출한 값(`VaultAdapter`
/`AgentAdapter`)만 읽어 집계·판단할 뿐 쓰기를 하지 않는다.

**경계(§8 규칙 21)**: 이 패키지의 어떤 모듈도 `domain`/`interfaces`/
`engines`/`vault`를 직접 import하지 않는다 — 오직 `integration/`의
Adapter만 생성자로 주입받는다. `tests/intelligence/
test_intelligence_layering.py`가 `ast` 기반으로 이를 강제한다.

**데이터 소스(ADR-0043)**: Core Domain 27종 Interface에는 project
단위 전체 목록 조회가 없어(`TaskEngine.get_task()`는 단건만),
Vault Task 문서(`VaultAdapter.list_tasks()`)를 단일 데이터 소스로
쓴다. Agent 데이터는 `AgentAdapter.list_active_agents()`를 그대로
재사용한다. Event(EventStore)는 이번 범위에서 쓰지 않는다(YAGNI).

현재 구성원:

- `snapshot.ProjectSnapshotAnalyzer`(Milestone 29-T02) — Task
  상태/Milestone/Owner 집계와 진행률을 계산한다.
- `health_risk.ProjectHealthRiskAnalyzer`(Milestone 29-T03) —
  `ProjectSnapshotWithTasks`를 입력으로 Health(Healthy/Warning/
  Critical)와 Risk(정체 Task/Owner 과부하/Milestone 정체)를 Rule
  기반으로 판단한다. Adapter를 직접 호출하지 않고 Snapshot 산출물만
  재사용한다(새 데이터 접근 경로 없음). **"의존성 위험"은 Vault
  Task 문서에 의존관계 필드가 없어(Core Domain `WorkflowEngine`의
  의존관계 정보가 필요하나 project 전체 열거 Interface가 없음,
  ADR-0043에서 이미 예견된 한계) M29 범위에서 판정하지 않는다 —
  필요해지면 별도 ADR/Interface 검토 대상이다.
"""

from __future__ import annotations
