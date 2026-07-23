# TASKS — 전체 Task 및 진행 상태

이 문서는 AI Workspace의 모든 Task를 Phase 단위로 관리한다. 규칙(`.ai/RULES.md`)에
따라 **한 번에 하나의 Task만** 진행하며, Task를 완료로 표시하기 전 반드시 테스트
(해당되는 경우) 를 수행한다.

상태 값: `TODO` / `IN_PROGRESS` / `REVIEW` / `DONE` / `BLOCKED` / `CANCELLED`

---

## Phase 0 — 문서화 및 구조 설계

| ID | Task | 상태 | 승인 필요 | 비고 |
|---|---|---|---|---|
| P0-1 | 프로젝트 비전/철학 분석 및 문서 구조 설계 | DONE | 아니오 | 본 세션에서 수행 |
| P0-2 | 디렉터리 구조 생성 (`docs/`, `.ai/`, `workspace/`, `tests/`) | DONE | 아니오 | 본 세션에서 수행 |
| P0-3 | `docs/PRD.md` 작성 | DONE | 아니오 | 목표/요구사항/성공기준 포함 |
| P0-4 | `docs/ARCHITECTURE.md` 작성 | DONE | 아니오 | 레이어/컴포넌트/데이터흐름/의존성 규칙 포함 |
| P0-5 | `docs/ROADMAP.md` 작성 | DONE | 아니오 | Phase 0~5 계획 포함 |
| P0-6 | `.ai/RULES.md` 작성 | DONE | 아니오 | 개발 철학의 내부 규정화 |
| P0-7 | `.ai/MEMORY.md` 초기화 | DONE | 아니오 | 최초 컨텍스트 기록 |
| P0-8 | `.ai/DECISIONS.md` 초기 ADR 작성 (ADR-0001~0004) | DONE | 아니오 | 모두 "제안" 상태, Phase 완료 승인 시 확정 |
| P0-9 | `.ai/TASKS.md` 작성 (본 문서) 및 Phase 1 세부 Task 정의 | DONE | 아니오 | |
| P0-10 | `README.md` 작성 | DONE | 아니오 | 프로젝트 소개/시작 방법/구조/문서 링크 |
| P0-11 | **Phase 0 완료 승인 요청** | TODO | **예 (Phase 완료)** | 사용자 승인 후 Phase 1 착수 |

> Phase 0에서는 애플리케이션 코드를 작성하지 않는다 (사용자 지시 사항).

---

## Phase 1 — 핵심 도메인 모델 & CLI 골격

> 착수 조건: P0-11(Phase 0 완료 승인)이 승인된 이후에만 시작한다.
> Phase 1 자체도 "신규 기능"에 해당하므로 착수 전 승인이 필요하다.

| ID | Task | 상태 | 승인 필요 | 의존성 |
|---|---|---|---|---|
| P1-0 | **Phase 1 착수 승인 요청** (범위/설계 방향 확인) | TODO | **예 (신규 기능)** | P0-11 |
| P1-1 | `src/ai_workspace/` 패키지 구조 확정 및 생성 | TODO | 아니오 | P1-0 |
| P1-2 | Project 도메인 모델 설계 및 구현 (`domain/project.py`) | TODO | 아니오 | P1-1 |
| P1-3 | Task 도메인 모델 및 상태 전이 규칙 구현 (`domain/task.py`) | TODO | 아니오 | P1-1 |
| P1-4 | Workflow 도메인 모델(순서/의존관계) 초안 구현 (`domain/workflow.py`) | TODO | 아니오 | P1-3 |
| P1-5 | 파일 기반 저장소 인터페이스 및 구현 (`storage/`) | TODO | 아니오 | P1-2, P1-3 |
| P1-6 | Project/Task 생성·조회 최소 CLI 명령 구현 (`cli/`) | TODO | 아니오 | P1-2, P1-3, P1-5 |
| P1-7 | 단위 테스트 작성 (`tests/domain/`, `tests/storage/`, `tests/cli/`) | TODO | 아니오 | P1-2 ~ P1-6 |
| P1-8 | `docs/ARCHITECTURE.md` 갱신 (실제 구현된 구조 반영) | TODO | 아니오 | P1-1 ~ P1-7 |
| P1-9 | `.ai/DECISIONS.md`의 ADR-0004(저장 방식) 상태를 "승인됨"으로 갱신 | TODO | 아니오 | P1-5 |
| P1-10 | **Phase 1 완료 승인 요청** | TODO | **예 (Phase 완료)** | P1-1 ~ P1-9 |

### Phase 1 Task별 완료 조건 (Definition of Done)

- **P1-1**: `docs/ARCHITECTURE.md` §6에서 제안한 하위 구조가 실제로 생성되고,
  구조가 문서와 일치함.
- **P1-2 / P1-3 / P1-4**: 각 도메인 모델에 타입 힌트가 적용되고, 상태 전이 규칙이
  코드와 문서(주석 최소화, 필요 시 `docs/ARCHITECTURE.md` 갱신) 모두에 반영됨.
- **P1-5**: 저장 인터페이스를 통해서만 파일 접근이 이루어지며, 저장 형식 변경이
  도메인 모델에 영향을 주지 않음을 테스트로 확인함.
- **P1-6**: 최소 CLI로 Project 생성 → Task 생성 → 조회가 end-to-end로 동작함.
- **P1-7**: `pytest` 실행 시 전체 테스트가 통과함 (Test Before Complete 원칙).
- **P1-10**: 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자 승인을 받음.

---

## Phase 2 이후 — 개요 (상세 Task는 각 Phase 착수 시 정의)

| Phase | 상세 Task 정의 시점 |
|---|---|
| Phase 2 (Task/Workflow 실행 관리) | Phase 1 완료 승인 이후 |
| Phase 3 (엔진 어댑터) | Phase 2 완료 승인 이후 |
| Phase 4 (승인 시스템 & 자동화) | Phase 3 완료 승인 이후 |
| Phase 5 (다중 프로젝트 & 메모리 고도화) | Phase 4 완료 승인 이후 |

각 Phase 상세 Task는 착수 시점에 `docs/ROADMAP.md`의 해당 Phase 목표를 기준으로
이 문서에 추가한다 (Documentation First + Task Driven Development 원칙).

---

## 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-07-23 | Phase 0 문서 세트(P0-1 ~ P0-10) 작성 완료. P0-11(Phase 0 완료 승인) 대기 중. |
