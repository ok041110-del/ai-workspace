# ROADMAP — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.2.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft |

## 계층 구조

AI Workspace의 계획은 다음 4단계 계층으로 관리한다.

```
Roadmap
  └─ Milestone   (프로젝트의 큰 목표)
       └─ Phase   (Milestone을 달성하기 위한 단계)
            └─ Task   (실제 구현 단위)
```

| 계층 | 역할 |
|---|---|
| Milestone | 프로젝트가 도달해야 하는 큰 목표. 여러 Phase로 구성되며, 자체 완료 조건(DoD)을 가진다. |
| Phase | 하나의 Milestone을 달성하기 위한 실행 단계. 여러 Task로 구성되며, 자체 완료 조건(DoD)을 가진다. |
| Task | 실제로 수행하는 최소 작업 단위. 세부 내용은 `.ai/TASKS.md`에서 관리한다. |

각 **Milestone 완료**와 각 **Phase 완료**는 모두 `.ai/RULES.md`의 Approval Required
원칙에 따라 **사용자 승인**을 받아야 다음 단계로 진행한다.

## Milestone / Phase 개요

| Milestone | 구성 Phase | 핵심 목표 | 상태 |
|---|---|---|---|
| M1. 기반 구축 (Foundation) | Phase 0, Phase 1 | 문서 체계와 핵심 도메인 모델(Project/Task/Workflow) 확정 | 진행 중 (Phase 0 승인 완료, Phase 1 진행 중) |
| M2. 오케스트레이션 코어 (Orchestration Core) | Phase 2, Phase 3 | Workflow/Task 실행, 승인 체계, 첫 구현 엔진(Claude Code) 연동 | 예정 |
| M3. 자동화 및 확장 (Automation & Scale) | Phase 4, Phase 5 | 자동화 도입, 다중 프로젝트 및 장기 메모리 고도화 | 예정 |

---

## Milestone 1 — 기반 구축 (Foundation)

**목표**: AI Workspace의 문서 체계를 완성하고, 이후 모든 오케스트레이션 기능의
토대가 되는 핵심 도메인 모델(Project/Task/Workflow)과 최소 CLI 골격을 확보한다.

**구성 Phase**: Phase 0, Phase 1

**Milestone Definition of Done**
1. `docs/`, `.ai/` 문서 체계가 모두 작성되고 사용자 승인을 받았다 (Phase 0).
2. Project/Task/Workflow 도메인 모델과 파일 기반 저장, 최소 CLI가 동작하며
   테스트를 통과한다 (Phase 1).
3. Milestone 2 착수에 필요한 아키텍처 결정(Adapter 패턴, Approval Engine 분리 등)이
   ADR로 확정되어 있다.

### Phase 0 — 문서화 및 구조 설계 (완료, 승인됨)

- **목표**: 애플리케이션 코드를 작성하지 않고, 프로젝트의 목적/구조/규칙/계획을
  문서로 명확히 정의한다.
- **산출물**: `README.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`,
  `docs/ROADMAP.md`, `.ai/RULES.md`, `.ai/TASKS.md`, `.ai/MEMORY.md`,
  `.ai/DECISIONS.md`, `workspace/`, `tests/` 디렉터리 구조
- **Phase Definition of Done**: 위 문서가 모두 작성되고, 사용자가 내용을 검토·
  승인한다.
- **승인 필요 여부**: 예 (Phase 완료 승인) — **2026-07-23 승인 완료**

### Phase 1 — 핵심 도메인 모델 & CLI 골격 (진행 중)

- **목표**: AI Workspace의 핵심 도메인 개념(Project, Task, Workflow)을 정의하고,
  Workspace Core가 구체 구현이 아닌 **Interfaces(추상 계약)**에만 의존하는
  순수 오케스트레이터 골격을 만든다 (ADR-0005). 조회/생성이 가능한 CLI 골격도
  함께 만든다. 특정 구현 엔진(Claude Code 등)에 대한 **구체적인 Adapter 구현**과
  Workflow/Task/Memory/Approval/Automation의 **구체적인 처리 로직**은 아직
  하지 않는다 (각각 Phase 3, Phase 2 범위) — Phase 1에서는 **7개 Interface
  (ProjectRepository, WorkflowEngine, TaskEngine, MemoryEngine, ApprovalEngine,
  AutomationEngine, EngineAdapter)를 정의**하고, 그중 `ProjectRepository`의
  구체 구현체(파일 기반)만 함께 만든다.
- **세부 목표** (승인된 착수 순서, ADR-0005 반영)
  1. 디렉터리 구조 생성 (`src/ai_workspace/{domain,interfaces,core,storage,engines,adapters,cli}`)
  2. 공통 도메인 모델 정의 (Project, Task, Workflow)
  3. Interfaces 정의 (ProjectRepository, WorkflowEngine, TaskEngine,
     MemoryEngine, ApprovalEngine, AutomationEngine, EngineAdapter — 계약만,
     구체 구현 없음)
  4. Workspace Core 기본 골격 구현 (Interfaces에만 의존: 프로젝트 로드/설정
     로드/서비스 초기화/Engine 등록·관리/Task 실행 요청/종료)
  5. ProjectRepository 파일 기반 구현 (Markdown/JSON)
  6. CLI 진입점 구성 (Workspace Core를 통한 Project/Task 생성·조회)
  7. 기본 테스트 환경 구축 및 테스트 작성
- **Phase Definition of Done**: 위 7단계가 모두 구현되고 테스트를 통과하며,
  `docs/ARCHITECTURE.md`가 실제 구조와 일치하도록 갱신된다.
- **우선순위**: 최우선 (다른 모든 Phase의 기반)
- **승인 필요 여부**: 예 (아키텍처 변경/신규 기능에 해당) — **2026-07-23 착수
  승인 완료**, 동일 날짜에 Workspace Core 범위/Interfaces 계층 구조를 사용자
  지시로 확정(ADR-0005) (완료 시점에 별도로 Phase 완료 승인 필요)
- **세부 Task**: `.ai/TASKS.md`의 "Milestone 1 > Phase 1" 섹션 참고.

---

## Milestone 2 — 오케스트레이션 코어 (Orchestration Core)

**목표**: Task/Workflow가 실제로 실행되고, 승인 없이는 진행되지 않는 안전장치가
동작하며, 최소 1개 구현 엔진(Claude Code)에 실제로 Task를 위임할 수 있는 상태를
만든다.

**구성 Phase**: Phase 2, Phase 3

**Milestone Definition of Done**
1. Workflow Engine이 Task 간 의존관계에 따라 실행 순서를 결정한다 (Phase 2).
2. Approval Engine이 아키텍처 변경/신규 기능/리팩토링/Phase 완료 4가지 행위를
   판별하여 승인 없이는 차단한다 (Phase 2).
3. `EngineAdapter` 인터페이스가 확정되고, Claude Code Adapter로 최소 1개 Task를
   실제로 위임·수행·결과 수집까지 완료한다 (Phase 3).

### Phase 2 — Workflow/Task 실행 관리

- **목표**: Task 간 의존관계를 실행 가능한 Workflow로 관리하고, Approval Engine을
  연동하여 승인 없이는 특정 행위가 진행되지 않도록 한다.
- **세부 목표**
  1. Workflow 정의(Task 순서, 의존관계, 조건부 분기) 모델링
  2. Approval Engine 컴포넌트 구현 (승인 대상 4가지 행위 판별 및 차단)
  3. Task/Workflow 상태와 `.ai/TASKS.md`, `.ai/DECISIONS.md` 간 동기화 방식 확정
- **Phase Definition of Done**: 의존관계가 있는 Task들을 Workflow Engine이 순서
  대로 실행하고, 승인 대상 행위 시도 시 Approval Engine이 이를 차단하는 것이
  테스트로 확인된다.
- **우선순위**: 높음 (Phase 1 완료 후 즉시 진행)

### Phase 3 — 엔진 어댑터 (Claude Code 우선)

- **목표**: `EngineAdapter` 인터페이스를 확정하고, Claude Code를 대상으로 한
  어댑터를 1차 구현하여 실제 Task 위임이 가능하도록 한다.
- **세부 목표**
  1. `EngineAdapter` 공통 인터페이스 확정 (입력: Task, 출력: EngineResult)
  2. Claude Code Adapter 구현 (호출 방식, 결과 수집, 오류 처리)
  3. 어댑터 계층의 테스트 전략 수립 (Mock 기반)
- **Phase Definition of Done**: Claude Code Adapter를 통해 최소 1개 Task가
  end-to-end(위임 → 실행 → 결과 수집 → Task 상태 갱신)로 동작한다.
- **우선순위**: 높음 (실질적 오케스트레이션의 시작점)
- **비고**: Codex, Gemini CLI 어댑터는 Claude Code 어댑터가 안정화된 이후 동일한
  패턴으로 추가한다.

---

## Milestone 3 — 자동화 및 확장 (Automation & Scale)

**목표**: 반복 작업을 자동으로 트리거할 수 있고, 여러 프로젝트를 동시에 운영하며
장기 메모리를 효율적으로 활용할 수 있는 상태를 만든다.

**구성 Phase**: Phase 4, Phase 5

**Milestone Definition of Done**
1. Automation Engine이 최소 1개 시나리오를 조건/일정에 따라 자동 실행한다
   (Phase 4).
2. 2개 이상의 프로젝트를 Workspace Core에서 동시에 등록·조회·우선순위 조정할 수
   있다 (Phase 5).
3. Memory Engine이 누적된 컨텍스트 중 필요한 부분만 검색/요약해 제공한다
   (Phase 5).

### Phase 4 — Automation Engine 도입

- **목표**: 승인 이력 관리를 정식화하고, 반복 작업을 자동으로 트리거하는
  Automation Engine을 도입한다.
- **세부 목표**
  1. 승인/반려 이력의 구조화된 기록 방식 확정
  2. Automation Engine 최소 구현 (조건/일정 기반 트리거)
  3. 자동화된 작업도 Task Engine을 통해 동일한 이력 체계로 추적되도록 통합
- **Phase Definition of Done**: 최소 1개의 자동화 시나리오(예: 정기적인 상태
  점검 Task 생성)가 사람 개입 없이 트리거되고, Task 이력에 정상적으로 기록된다.
- **우선순위**: 중간

### Phase 5 — 다중 프로젝트 & Memory Engine 고도화

- **목표**: 여러 프로젝트를 동시에 운용할 때 필요한 대시보드성 조회 기능과, 장기
  메모리의 검색/요약 기능을 고도화한다.
- **세부 목표**
  1. 다중 프로젝트 상태 조회/우선순위 조정 기능 (Workspace Core 확장)
  2. Memory Engine 검색 및 요약 전략 설계
  3. 필요 시 저장소를 파일 기반에서 DB 기반으로 전환 검토 (ADR 필요)
- **Phase Definition of Done**: 2개 이상 프로젝트를 동시에 등록·조회할 수 있고,
  Memory Engine에서 특정 프로젝트의 핵심 컨텍스트만 검색해 조회할 수 있다.
- **우선순위**: 중간 ~ 낮음 (Milestone 1~2 안정화 이후)

---

## 우선순위 원칙

1. 기반이 되는 도메인 모델(Milestone 1)을 가장 먼저 확정한다.
2. "관리만 하고 실행은 못하는" 상태를 최소화하기 위해, 승인 체계와 실제 엔진
   연동(Milestone 2)을 그 다음으로 우선한다.
3. 자동화와 다중 프로젝트 고도화(Milestone 3)는 핵심 오케스트레이션이 안정화된
   이후에 진행한다.
