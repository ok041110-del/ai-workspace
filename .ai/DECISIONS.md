# DECISIONS — Architecture Decision Record (ADR)

이 문서는 AI Workspace 프로젝트의 주요 설계 결정을 기록한다. 각 ADR은 결정
내용뿐 아니라 **배경, 대안, 이유, 결과**를 함께 남겨 이후 재검토가 가능하도록 한다.

형식은 다음을 따른다.

```
## ADR-000X: 제목
- 상태: 제안 / 승인됨 / 반려됨 / 폐기됨
- 날짜: YYYY-MM-DD
- 배경: 왜 이 결정이 필요했는가
- 결정: 무엇을 결정했는가
- 대안: 검토했던 다른 선택지와 그 장단점
- 이유: 왜 이 대안을 선택했는가
- 결과/영향: 이 결정이 프로젝트에 미치는 영향
```

---

## ADR-0001: 문서 구조를 README / docs / .ai 3계층으로 구성

- 상태: 승인됨 (2026-07-23, Phase 0 완료 승인)
- 날짜: 2026-07-23
- 배경: AI Workspace는 "문서 우선" 원칙을 따르며, 사람과 AI 구현 엔진이 모두
  읽을 수 있는 일관된 문서 체계가 필요했다.
- 결정: 문서를 세 계층으로 분리한다.
  - `README.md`: 프로젝트 소개 및 진입점
  - `docs/`: 사람 중심의 제품/구조/계획 문서 (PRD, ARCHITECTURE, ROADMAP)
  - `.ai/`: AI 구현 엔진이 작업 시 참조하는 운영 문서 (RULES, TASKS, MEMORY,
    DECISIONS)
- 대안:
  - 단일 `docs/` 폴더에 모두 모아두는 방식 — 단순하지만 "사람을 위한 설명 문서"와
    "AI가 매 세션 참조해야 하는 운영 문서"의 성격이 섞여 관리가 어려움.
  - 각 컴포넌트별로 별도 하위 문서 폴더를 만드는 방식 — 초기 단계에는 과도한
    세분화로 판단.
- 이유: 문서의 "독자"와 "갱신 빈도"가 다르다. `docs/`는 상대적으로 안정적인 제품
  정의, `.ai/`는 작업할 때마다 갱신되는 살아있는 문서다. 이를 분리하면 AI 구현
  엔진이 매 세션 시작 시 `.ai/`만 우선 참조해도 충분하도록 만들 수 있다.
- 결과/영향: 이후 모든 Task는 `.ai/TASKS.md`를 갱신하고, 아키텍처/요구사항
  변경은 `docs/`를 갱신하는 것으로 책임이 명확히 나뉜다.

## ADR-0002: 구현 엔진을 Adapter 패턴으로 추상화

- 상태: 제안 (Phase 1 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
- 배경: Claude Code, Codex, Gemini CLI는 호출 방식과 능력이 서로 다르다. 이를
  Orchestration Layer가 직접 알게 하면 엔진 추가/교체 시마다 핵심 로직을 수정해야
  한다.
- 결정: 모든 구현 엔진은 공통 `EngineAdapter` 인터페이스(예: `run_task`)를
  구현하고, Orchestration Layer는 이 인터페이스에만 의존한다.
- 대안:
  - 엔진별로 별도 파이프라인을 만드는 방식 — 초기 구현은 빠르지만 엔진이
    늘어날수록 중복과 불일치가 커짐 (기각).
  - 엔진 호출을 설정 파일 기반 스크립트로 느슨하게 연결하는 방식 — 유연하지만
    타입 안전성과 테스트 용이성이 떨어짐 (기각).
- 이유: Open-Closed Principle을 따라, 신규 엔진 추가가 기존 코드 변경 없이
  Adapter 하나를 새로 작성하는 것만으로 가능하도록 하기 위함.
- 결과/영향: Phase 3에서 `EngineAdapter` 인터페이스를 먼저 확정하고, Claude Code
  어댑터를 1차 구현체로 삼는다.

## ADR-0003: 승인 절차를 별도 Approval Engine 컴포넌트로 분리

- 상태: 제안 (Phase 2 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
- 배경: 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료는 반드시 사용자 승인을
  거쳐야 한다는 요구사항이 있다. 이를 Workflow 로직 곳곳에 조건문으로 흩어 넣으면
  우회 경로가 생기기 쉽고 정책 변경 시 여러 곳을 고쳐야 한다.
- 결정: 승인이 필요한 행위 유형을 열거형으로 정의하고, 모든 승인 판단과 대기
  상태 관리를 단일 컴포넌트인 Approval Engine에 위임한다.
- 대안:
  - Workflow Engine 내부에 승인 체크 로직을 인라인으로 작성 — 구현은 빠르지만
    누락/우회 위험이 크고 감사(audit)가 어려움 (기각).
- 이유: 승인은 시스템의 "안전 장치"에 해당하므로, 단일 지점에서 강제되어야
  누락 없이 일관되게 적용된다.
- 결과/영향: Phase 2에서 Approval Engine을 구현하며, 승인/반려 이력은
  `.ai/DECISIONS.md`와 연동해 기록한다.

## ADR-0004: Phase 1 저장 방식은 파일 기반(Markdown/JSON)으로 시작

- 상태: 제안 (Phase 1 착수 시 재확인 및 확정 예정)
- 날짜: 2026-07-23
- 배경: 데이터베이스 도입은 초기 단계에서 불필요한 복잡도를 추가할 수 있다
  (YAGNI). 동시에 문서 우선 철학상, 저장된 데이터도 사람이 직접 읽을 수 있으면
  유리하다.
- 결정: Phase 1에서는 프로젝트/Task 데이터를 파일 기반(Markdown 및/또는 JSON)으로
  저장한다.
- 대안:
  - SQLite 등 경량 DB 도입 — 쿼리와 동시성 처리에 유리하지만 Phase 1 범위(단일
    사용자, 소규모 데이터)에는 과함 (기각, Phase 5에서 재검토 예정).
- 이유: 초기 단계의 단순성과 "사람이 직접 확인 가능한 저장 형식"이라는 문서
  우선 철학에 부합한다.
- 결과/영향: Phase 5에서 다중 프로젝트/장기 메모리 고도화 시 DB 전환 필요성을
  재검토하며, 그 경우 별도 ADR을 작성한다.

## ADR-0005: Workspace Core를 순수 오케스트레이터로 한정하고 Interfaces 계층을 명시적으로 분리

- 상태: 승인됨 (2026-07-23, Phase 1 진행 중 사용자 지시로 확정)
- 날짜: 2026-07-23
- 배경: 기존 설계(v0.2.0)는 Workspace Core가 "프로젝트 등록/조회/보관"과 "다중
  프로젝트 관리"까지 직접 포함하고, Core Engine을 구체적으로 호출하는 형태였다.
  이 경우 Workspace Core가 점점 비대해지고, 실제 Workflow/Task/Memory/Approval/
  Automation 처리 로직과 뒤섞일 위험이 있었다. 또한 Phase별로 구현 순서가
  다른 컴포넌트(Engine은 Phase 2, Adapter는 Phase 3)를 Workspace Core가 조기에
  구체적으로 알게 되면, Phase 1 시점에 존재하지 않는 구현체 때문에 설계가
  막히는 문제가 있었다.
- 결정:
  1. Workspace Core의 책임을 **프로젝트 로드, 설정 로드, 서비스 초기화, Engine
     등록 및 관리, Task 실행 요청, 애플리케이션 종료** 6가지로 한정한다.
     Workflow/Task/Memory/Approval/Automation 처리, 구현 엔진 직접 호출, 파일
     저장 세부 구현은 Workspace Core에 포함하지 않는다.
  2. Workspace Core와 그 협력 대상 사이에 **Interfaces(추상 계약)** 계층을
     명시적으로 둔다: `ProjectRepository`, `WorkflowEngine`, `TaskEngine`,
     `MemoryEngine`, `ApprovalEngine`, `AutomationEngine`, `EngineAdapter`.
  3. Phase 1에서는 이 7개 Interface **정의만** 하고, `ProjectRepository`의
     구체 구현체(`FileProjectRepository`)만 함께 구현한다. 나머지 5개 Engine의
     구체 구현체는 Phase 2, `EngineAdapter`의 구체 구현체(Claude Code/Codex/
     Gemini CLI)는 Phase 3에서 구현한다.
- 대안:
  - Workspace Core가 각 Engine의 로직을 직접 포함하는 방식 — 초기 구현은
    간단하지만 책임이 섞이고, Phase별로 순차 구현하기 어려움 (기각).
  - Interfaces 없이 구체 클래스에 바로 의존하는 방식 — 인터페이스 계층 설계
    비용은 없지만, 구체 구현체가 아직 없는 Phase 1 시점에 Workspace Core를
    완성할 수 없고, 이후 구현체 교체 시 Workspace Core 수정이 불가피함 (기각).
- 이유: Interfaces를 먼저 정의하면 Workspace Core를 Phase 1에서 완성할 수
  있고(구체 구현체는 아직 없어도 됨), 각 Engine/Adapter를 이후 Phase에서 독립적으로
  구현·테스트할 수 있다. 이는 ADR-0002(Adapter 패턴)의 정신을 Engine
  전반으로 확장한 것이다.
- 결과/영향: `docs/ARCHITECTURE.md` v0.3.0에 반영됨. Phase 1 Task 목록
  (`.ai/TASKS.md`)이 "도메인 모델 → Interfaces 정의 → Workspace Core 골격 →
  ProjectRepository 구현 → CLI → 테스트" 순서로 재구성됨.
