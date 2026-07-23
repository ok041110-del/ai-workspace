# MEMORY — 프로젝트 장기 메모리

## 0. 이 문서의 역할과 사용 원칙 (중요)

`MEMORY.md`는 단순한 작업 메모가 아니라, AI Workspace 프로젝트의 **장기
메모리(Long-term Memory)**다. 다음 원칙에 따라 관리하고 사용한다.

1. **항상 읽는 문서가 아니다.** 매 Task마다 통째로 읽는 문서는 `.ai/TASKS.md`
   (현재 무엇을 해야 하는가)와 `.ai/RULES.md`(어떻게 해야 하는가)이며,
   `MEMORY.md`는 다음과 같은 **필요한 경우에만** 읽는다.
   - 새 세션(또는 새 AI 구현 엔진 호출)을 시작해 프로젝트 전체 맥락을 빠르게
     파악해야 할 때
   - 오래된 결정의 배경이나 이유가 궁금할 때
   - 프로젝트 규모가 커져 `.ai/TASKS.md`, `.ai/DECISIONS.md`만으로는 전체 그림이
     보이지 않을 때
2. **핵심 컨텍스트를 압축하여 저장한다.** 모든 대화나 변경 이력을 빠짐없이
   기록하는 로그가 아니다. 상세 이력은 `.ai/TASKS.md`의 "진행 로그"와
   `.ai/DECISIONS.md`의 ADR이 담당하고, `MEMORY.md`는 그중 **반드시 기억해야
   하는 결론만** 압축해서 담는다.
3. **프로젝트가 커져도 빠르게 현재 상황을 파악할 수 있도록 유지한다.** 새로운
   내용이 생겼다고 무조건 append하지 않는다. 오래되어 더 이상 유효하지 않은
   내용은 삭제하거나 최신 결론으로 교체한다. 이 문서는 "쌓이는 문서"가 아니라
   "항상 최신 상태의 요약본"이어야 한다.
4. **구현 세부사항이 아니라 사실과 의사결정을 기록한다.** 코드가 어떻게
   짜였는지가 아니라, "무엇이 결정되었는가", "왜 그렇게 결정했는가", "지금
   프로젝트가 어디까지 왔는가"를 기록한다. 구현 세부사항은 코드와
   `docs/ARCHITECTURE.md`가 진실의 원천(source of truth)이다.

이 문서는 아래 6개 섹션을 최소한으로 유지한다: 현재 Milestone, 프로젝트 정체성,
핵심 아키텍처, 반드시 유지해야 하는 설계 원칙, 주요 의사결정 요약, 이후 작업에
필요한 핵심 컨텍스트.

---

## 1. 현재 Milestone

- **현재 위치**: Milestone 1 (기반 구축) / **Phase 1 (핵심 도메인 모델 & CLI
  골격) 진행 중**
- **Phase 0**: 2026-07-23 사용자 승인 완료 (`.ai/TASKS.md` P0-11 DONE).
- **Phase 1 착수**: 2026-07-23 사용자 승인 완료 (P1-0 DONE).
- **P1-1(디렉터리 구조 생성)**: DONE.
- **Workspace Core 범위/Interfaces 계층 확정 (ADR-0005, 2026-07-23)**: Workspace
  Core를 순수 오케스트레이터로 한정하고, Workspace Core → Interfaces(추상
  계약) → 구체 구현체(Phase별)로 이어지는 구조를 채택함. Phase 1 Task 순서를
  "디렉터리 구조 → 공통 도메인 모델 → Interfaces 정의(7개) → Workspace Core
  골격 → ProjectRepository 구현 → CLI → 테스트 환경"으로 재구성함.
- **다음 단계**: `.ai/TASKS.md`의 P1-2(공통 도메인 모델 정의)부터 순서대로 진행.

## 2. 프로젝트 정체성

- **프로젝트명**: AI Workspace
- **한 줄 정의**: Claude Code, Codex, Gemini CLI 등 AI 구현 엔진을 관리하는
  오케스트레이션 플랫폼.
- **핵심 원칙**: AI Workspace는 코드를 작성하지 않는다. 프로젝트 관리, Task
  관리, Workflow 오케스트레이션, 장기 메모리, 승인, 자동화, 다중 프로젝트 관리,
  구현 엔진 관리만 담당한다. 실제 코드 작성은 구현 엔진의 책임이다.

## 3. 핵심 아키텍처 (요약)

자세한 내용은 `docs/ARCHITECTURE.md` 참고. 여기서는 언제든 빠르게 떠올릴 수
있어야 하는 구조만 압축한다.

```
Workspace(CLI) → Workspace Core → Interfaces → 구체 구현체 → 구현 엔진
```

- **Workspace Core**: 순수 오케스트레이터. 프로젝트 로드·설정 로드·서비스
  초기화·Engine 등록/관리·Task 실행 요청·종료만 담당하며, 실제 처리 로직은
  전혀 포함하지 않는다. 오직 **Interfaces에만** 의존한다 (ADR-0005).
- **Interfaces (추상 계약, Phase 1에서 정의)**: `ProjectRepository`,
  `WorkflowEngine`, `TaskEngine`, `MemoryEngine`, `ApprovalEngine`,
  `AutomationEngine`, `EngineAdapter`.
- **구체 구현체 (Phase별)**: `FileProjectRepository`(Phase 1) → Workflow/Task/
  Memory/Approval/Automation Engine 구현체(Phase 2) → ClaudeCodeAdapter 등
  (Phase 3).
- 의존 방향은 항상 위(Workspace/CLI)에서 아래(구현 엔진)로만 향하며, Workspace
  Core는 구체 구현체를 전혀 알지 못한다.

## 4. 반드시 유지해야 하는 설계 원칙

- 실제 코드 작성 금지 원칙은 **Phase 0(문서화 단계)에 한정**된다. Phase 1부터는
  승인을 받은 뒤 코드를 작성한다.
- **Workspace Core는 순수 오케스트레이터다 (ADR-0005).** Workflow/Task/Memory/
  Approval/Automation 처리, 구현 엔진 직접 호출, 파일 저장 세부 구현을
  Workspace Core에 절대 넣지 않는다. Workspace Core는 오직 Interfaces에만
  의존한다.
- 승인이 필요한 4가지 행위: 아키텍처 변경, 신규 기능, 리팩토링, Phase 완료.
  Approval Engine이라는 단일 컴포넌트가 판별·차단한다 (우회 경로 없음).
- 구현 엔진은 반드시 Engine Adapter를 통해서만 호출한다 (엔진 비종속성).
- Engine Adapter(및 다른 5개 Engine)의 **구체 구현은 Phase 2/3에서** 이루어진다.
  Phase 1에서 실제 처리 로직을 앞당겨 구현하지 않는다.
- 계획은 Milestone → Phase → Task 계층을 따르며, Task는 한 번에 하나씩만
  진행한다.
- 모든 문서/설명/주석/커밋 메시지는 한국어, 코드 식별자는 Python 표준(영어)을
  따른다.

## 5. 주요 의사결정 요약

전체 배경/대안/이유는 `.ai/DECISIONS.md`의 각 ADR 참고. 여기서는 결론만 압축한다.

| ADR | 결론 | 상태 |
|---|---|---|
| ADR-0001 | 문서를 `README` / `docs/`(사람용) / `.ai/`(AI 운영용) 3계층으로 분리 | 승인됨 |
| ADR-0002 | 구현 엔진은 Adapter 패턴으로 추상화 (`EngineAdapter` 인터페이스) | 제안 (Phase 1에서 인터페이스 설계 후 승인 예정) |
| ADR-0003 | 승인 절차는 별도 Approval Engine 컴포넌트로 분리 (인라인 금지) | 제안 (Phase 2에서 확정 예정) |
| ADR-0004 | Phase 1 저장 방식은 파일 기반(Markdown/JSON)으로 시작 | 제안 (Phase 1에서 구현 후 승인 예정) |
| ADR-0005 | Workspace Core는 순수 오케스트레이터로 한정, Interfaces 계층 분리 | 승인됨 |

기술 스택(Python, pydantic/dataclasses, 파일 기반 저장, CLI)은 아직 **제안**
단계이며, Phase 1 착수 시 정식 승인이 필요하다.

## 6. 이후 작업에 필요한 핵심 컨텍스트

- 구현 엔진 연동 순서: Claude Code 최우선 → Codex → Gemini CLI (동일한 Adapter
  패턴으로 순차 추가).
- Phase 1의 범위는 "도메인 모델 + Interfaces(7개, 계약만) + Workspace Core
  골격 + ProjectRepository 구체 구현 + 최소 CLI + 테스트 환경"까지다. 나머지
  5개 Engine(Workflow/Task/Memory/Approval/Automation)의 **구체 구현은
  Phase 2**, `EngineAdapter`의 **구체 구현(Claude Code 등)은 Phase 3**에서
  다룬다. Phase 1에서 실제 처리 로직을 앞당겨 구현하지 않는다.
- Workspace Core는 더 이상 "Project Manager 역할(프로젝트 등록/다중 프로젝트
  관리)"을 자체적으로 포함하지 않는다 (ADR-0005로 변경). 프로젝트 로드는
  `ProjectRepository` 인터페이스를 통해서만 이루어지며, 다중 프로젝트
  대시보드/우선순위 조정 같은 고도화 기능은 Phase 5에서 Workspace Core를
  확장할 때 다시 검토한다.
