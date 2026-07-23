# ROADMAP — AI Workspace

| 항목 | 내용 |
|---|---|
| 문서 버전 | v0.1.0 |
| 작성일 | 2026-07-23 |
| 상태 | Draft |

이 로드맵은 `docs/PRD.md`(요구사항)와 `docs/ARCHITECTURE.md`(구조)를 기반으로 한
단계별(Phase) 개발 계획이다. 각 Phase 완료 시점에는 **사용자 승인**을 받아야 다음
Phase로 진행한다 (Approval Required 원칙).

## Phase 개요

| Phase | 이름 | 핵심 목표 | 상태 |
|---|---|---|---|
| Phase 0 | 문서화 및 구조 설계 | PRD/ARCHITECTURE/ROADMAP 및 `.ai/` 문서 체계 수립 | 진행 중 (본 작업) |
| Phase 1 | 핵심 도메인 모델 & CLI 골격 | Project/Task/Workflow 도메인 모델, 파일 기반 저장, 최소 CLI | 예정 |
| Phase 2 | Task/Workflow 실행 관리 | Task 상태 전이, Workflow 의존관계 실행, Approval Gate 연동 | 예정 |
| Phase 3 | 엔진 어댑터 (Claude Code 우선) | EngineAdapter 인터페이스 확정 및 Claude Code 어댑터 구현 | 예정 |
| Phase 4 | 승인 시스템 & 자동화 고도화 | Approval Gate 정식화, Automation Scheduler 도입 | 예정 |
| Phase 5 | 다중 프로젝트 & 장기 메모리 고도화 | 다중 프로젝트 대시보드, Memory 검색/요약 | 예정 |

---

## Phase 0 — 문서화 및 구조 설계 (현재)

**목표**: 애플리케이션 코드를 작성하지 않고, 프로젝트의 목적/구조/규칙/계획을
문서로 명확히 정의한다.

**산출물**
- `README.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`
- `.ai/RULES.md`, `.ai/TASKS.md`, `.ai/MEMORY.md`, `.ai/DECISIONS.md`
- `workspace/`, `tests/` 디렉터리 구조

**완료 조건**
- 위 문서가 모두 작성되고, 사용자가 내용을 검토·승인한다.

**승인 필요 여부**: 예 (Phase 완료 승인)

---

## Phase 1 — 핵심 도메인 모델 & CLI 골격

**목표**: AI Workspace의 핵심 도메인 개념(Project, Task, Workflow)을 코드 수준의
모델로 정의하고, 이를 조회/생성할 수 있는 최소한의 CLI 골격을 만든다. 아직 구현
엔진과의 실제 연동은 하지 않는다 (Phase 3 범위).

**세부 목표**
1. `docs/ARCHITECTURE.md`에서 제안한 디렉터리 구조(`src/ai_workspace/...`)를 확정한다.
2. Project / Task 도메인 모델과 상태(전이) 규칙을 정의한다.
3. 파일 기반(Markdown/JSON) 저장 방식을 확정하고 최소 구현을 만든다.
4. Project/Task 생성·조회를 위한 최소 CLI 명령을 제공한다.
5. 위 모든 기능에 대한 테스트(`tests/`)를 작성한다.

**우선순위**: 최우선 (다른 모든 Phase의 기반)

**승인 필요 여부**: 예 (아키텍처 변경/신규 기능에 해당 — 착수 전 승인, 완료 시 승인)

**세부 Task**: `.ai/TASKS.md`의 "Phase 1" 섹션 참고.

---

## Phase 2 — Task/Workflow 실행 관리

**목표**: Task 간 의존관계를 실행 가능한 Workflow로 관리하고, Approval Gate를
연동하여 승인 없이는 특정 행위가 진행되지 않도록 한다.

**세부 목표**
1. Workflow 정의(Task 순서, 의존관계, 조건부 분기) 모델링
2. Approval Gate 컴포넌트 구현 (승인 대상 4가지 행위 판별 및 차단)
3. Task/Workflow 상태와 `.ai/TASKS.md`, `.ai/DECISIONS.md` 간 동기화 방식 확정

**우선순위**: 높음 (Phase 1 완료 후 즉시 진행)

---

## Phase 3 — 엔진 어댑터 (Claude Code 우선)

**목표**: `EngineAdapter` 인터페이스를 확정하고, Claude Code를 대상으로 한 어댑터를
1차 구현하여 실제 Task 위임이 가능하도록 한다.

**세부 목표**
1. `EngineAdapter` 공통 인터페이스 확정 (입력: Task, 출력: EngineResult)
2. Claude Code Adapter 구현 (호출 방식, 결과 수집, 오류 처리)
3. 어댑터 계층의 테스트 전략 수립 (Mock 기반)

**우선순위**: 높음 (실질적 오케스트레이션의 시작점)

**비고**: Codex, Gemini CLI 어댑터는 Claude Code 어댑터가 안정화된 이후 동일한
패턴으로 추가한다.

---

## Phase 4 — 승인 시스템 & 자동화 고도화

**목표**: 승인 이력 관리를 정식화하고, 반복 작업을 자동으로 트리거하는
Automation Scheduler를 도입한다.

**세부 목표**
1. 승인/반려 이력의 구조화된 기록 방식 확정
2. Automation Scheduler 최소 구현 (조건/일정 기반 트리거)
3. 자동화된 작업도 동일한 Task 이력 체계로 추적되도록 통합

**우선순위**: 중간

---

## Phase 5 — 다중 프로젝트 & 장기 메모리 고도화

**목표**: 여러 프로젝트를 동시에 운용할 때 필요한 대시보드성 조회 기능과, 장기
메모리의 검색/요약 기능을 고도화한다.

**세부 목표**
1. 다중 프로젝트 상태 조회/우선순위 조정 기능
2. Memory Store 검색 및 요약 전략 설계
3. 필요 시 저장소를 파일 기반에서 DB 기반으로 전환 검토 (ADR 필요)

**우선순위**: 중간 ~ 낮음 (Phase 1~4 안정화 이후)

---

## 마일스톤 요약

| 마일스톤 | 완료 기준 |
|---|---|
| M0: 문서 체계 완성 | Phase 0 산출물 전부 작성 및 승인 |
| M1: 도메인 모델 확정 | Phase 1 완료, Project/Task CLI 동작 |
| M2: 첫 워크플로우 실행 | Phase 2 완료, Approval Gate 연동 확인 |
| M3: 첫 실제 엔진 위임 | Phase 3 완료, Claude Code로 Task 위임 성공 |
| M4: 자동화 도입 | Phase 4 완료, 최소 1개 자동화 시나리오 동작 |
| M5: 다중 프로젝트 운용 | Phase 5 완료, 2개 이상 프로젝트 동시 관리 확인 |

## 우선순위 원칙

1. 기반이 되는 도메인 모델(Phase 1)을 가장 먼저 확정한다.
2. "관리만 하고 실행은 못하는" 상태를 최소화하기 위해, 승인 체계(Phase 2)와 실제
   엔진 연동(Phase 3)을 그 다음으로 우선한다.
3. 자동화(Phase 4)와 다중 프로젝트 고도화(Phase 5)는 핵심 오케스트레이션이
   안정화된 이후에 진행한다.
