# TASKS — 전체 Task 및 진행 상태

이 문서는 `docs/ROADMAP.md`의 **Milestone → Task** 계층을 그대로 따른다.
**Phase 계층은 2026-07-24부로 폐지되었다 (ADR-0021, Migration Table은
`docs/ROADMAP.md` 하단 참고).** `.ai/RULES.md`에 따라 **한 번에 하나의 Task만**
진행하며, Task를 완료로 표시하기 전 반드시 테스트(해당되는 경우)를 수행한다.

Task ID 형식: `T{Milestone 번호}-{일련번호}` (예: `T1-01`). 하나의 Task는
**하나의 구현 목표 + 하나의 Commit + 하나의 구현 사이클**이 되도록 설계한다.

상태 값: `TODO` / `IN_PROGRESS` / `DONE` (필요 시 `BLOCKED` / `CANCELLED` 사용)

각 Task는 다음 정보를 포함한다.

- **목적**: 이 Task가 왜 필요한가
- **작업 내용**: 실제로 수행하는 일
- **완료 조건 (DoD)**: 무엇을 확인해야 완료로 볼 수 있는가
- **상태**: 현재 진행 상태

---

## Milestone 1 — 기반 구축 (Foundation)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 1 Definition of Done" 참고.
> T1-01~T1-11은 문서화 작업(구 Phase 0), T1-12~T1-28은 구현 작업(구 Phase 1)에
> 해당한다. 그룹 구분은 참고용 설명일 뿐 별도 승인 단계를 두지 않는다 — Milestone
> 전체에 대한 승인은 T1-28(Milestone 1 Review) 하나로 일원화된다.
> **2026-07-24**: 원래 T1-18~T1-25(8개)였던 구현 Task를 아키텍처 책임 경계에
> 맞춰 T1-18~T1-28(11개)로 재분해함(ADR-0022). 상세 사유는 T1-18 앞의 안내문과
> ADR-0022 참고.

#### T1-01: 프로젝트 비전/철학 분석 및 문서 구조 설계
- 목적: 프로젝트 비전과 개발 철학을 바탕으로 어떤 문서를, 어떤 구조로 만들지
  결정한다.
- 작업 내용: 사용자가 제시한 비전/철학을 분석하고 `README/docs/.ai/workspace/tests`
  구조를 설계한다.
- 완료 조건(DoD): 문서 구조가 결정되고 이후 Task(T1-02 이후)의 기준이 된다.
- 상태: DONE

#### T1-02: 디렉터리 구조 생성
- 목적: 설계한 문서 구조를 실제 디렉터리로 반영한다.
- 작업 내용: `docs/`, `.ai/`, `workspace/`, `tests/` 디렉터리를 생성한다.
- 완료 조건(DoD): 4개 디렉터리가 저장소에 존재한다.
- 상태: DONE

#### T1-03: `docs/PRD.md` 작성
- 목적: 프로젝트의 목표와 요구사항을 명확히 정의해 이후 설계의 기준을 세운다.
- 작업 내용: 배경, 목표, 비목표, 핵심 개념, 기능/비기능 요구사항, 성공 기준,
  리스크를 작성한다.
- 완료 조건(DoD): 위 항목이 모두 포함된 PRD가 작성된다.
- 상태: DONE

#### T1-04: `docs/ARCHITECTURE.md` 작성
- 목적: PRD 요구사항을 만족하는 구조를 설계해 구현 전 청사진을 마련한다.
- 작업 내용: 컴포넌트(Workspace Core / Core Engines / Engine Adapter), 데이터
  흐름, 의존성 규칙, 디렉터리 매핑, 대안 비교를 작성한다.
- 완료 조건(DoD): 각 컴포넌트의 책임과 의존 방향이 명시되고, 사용자 피드백
  (v0.2.0)이 반영된다.
- 상태: DONE

#### T1-05: `docs/ROADMAP.md` 작성
- 목적: Milestone 단위의 장기 계획을 수립한다.
- 작업 내용: (작성 당시에는 Milestone → Phase 계층으로 계획을 작성했으며, 각
  Milestone/Phase의 DoD를 명시함. 이후 T1-?? 시점에 Phase 계층은 폐지됨 —
  Migration Table 참고.)
- 완료 조건(DoD): 당시 기준 Milestone 1~3, Phase 0~5가 모두 DoD와 함께
  정의된다(작성 당시 상태 그대로 보존, 이후 여러 차례 개정을 거쳐 현재 버전에
  이름).
- 상태: DONE

#### T1-06: `.ai/RULES.md` 작성
- 목적: 개발 철학을 프로젝트 내부 규정으로 명문화해 모든 작업의 기준으로 삼는다.
- 작업 내용: 언어 규칙, Documentation/Architecture First, Task Driven
  Development, One Task At A Time, Test Before Complete, Approval Required,
  이유 설명 원칙, 코딩/커밋 규칙을 작성한다.
- 완료 조건(DoD): 8개 원칙이 모두 문서화된다.
- 상태: DONE

#### T1-07: `.ai/MEMORY.md` 작성
- 목적: 세션이 끝나도 유지되어야 할 핵심 컨텍스트를 압축된 형태로 보존한다.
- 작업 내용: MEMORY.md의 역할/사용 원칙을 정의하고, 현재 Milestone·프로젝트
  정체성·핵심 아키텍처·설계 원칙·주요 의사결정 요약·다음 작업 컨텍스트를 기록한다.
- 완료 조건(DoD): "필요할 때만 참조하는 압축된 장기 메모리"라는 역할이 문서 내에
  명시되고, 요구된 6개 항목이 모두 포함된다.
- 상태: DONE

#### T1-08: `.ai/DECISIONS.md` 초기 ADR 작성
- 목적: 문서 구조, Adapter 패턴, 승인 체계, 저장 방식에 대한 결정 근거를 남긴다.
- 작업 내용: ADR-0001~0004를 배경/결정/대안/이유/결과 형식으로 작성한다.
- 완료 조건(DoD): 4개 ADR이 모두 "제안" 상태로 작성되고, 이후 승인과 함께 상태를
  갱신할 기준이 마련된다.
- 상태: DONE

#### T1-09: `.ai/TASKS.md` 작성 (본 문서)
- 목적: Milestone/Task 계층에 따라 실제 작업을 추적할 수 있게 한다.
- 작업 내용: (작성 당시에는 ROADMAP의 Milestone/Phase 구조를 따르는 Task 목록을
  작성함. 이후 Phase 폐지에 따라 본 문서 전체가 Milestone → Task 체계로
  재작성됨 — 2026-07-24, 진행 로그 참고.)
- 완료 조건(DoD): 당시 기준 Phase 0의 모든 Task와 Phase 1의 세부 Task가
  목적/작업내용/DoD/상태 형식으로 작성된다(작성 당시 상태 그대로 보존).
- 상태: DONE

#### T1-10: `README.md` 작성
- 목적: 프로젝트를 처음 접하는 사람이 빠르게 개요를 파악할 수 있게 한다.
- 작업 내용: 프로젝트 소개, 시작 방법, 디렉터리 구조, 문서 링크, 개발 철학
  요약을 작성한다.
- 완료 조건(DoD): 위 5개 항목이 모두 포함된다.
- 상태: DONE

#### T1-11: 문서화 완료 승인 요청 (구 "Phase 0 완료 승인 요청")
- 목적: Approval Required 원칙에 따라 문서화 산출물(T1-01~T1-10)을 사용자에게
  검토받는다.
- 작업 내용: 완성된 문서 세트를 제시하고 승인을 요청한다. 1차 피드백(MEMORY 역할
  명확화, ARCHITECTURE 컴포넌트 보완, ROADMAP Milestone화, TASKS 구조 일치)을
  반영해 재요청한다.
- 완료 조건(DoD): 사용자가 문서화 산출물에 대해 명시적으로 승인한다.
- 상태: **DONE (2026-07-23 사용자 승인)**

> 문서화 작업(T1-01~T1-11)에서는 애플리케이션 코드를 작성하지 않는다 (사용자
> 지시 사항).

---

#### T1-12: 구현 착수 승인 요청 (구 "Phase 1 착수 승인 요청")
- 목적: 도메인 모델/CLI 골격 착수 전 범위와 설계 방향을 확인받는다.
- 작업 내용: `docs/ROADMAP.md`의 구현 목표와 세부 Task 계획을 제시하고 승인을
  요청한다.
- 완료 조건(DoD): 사용자가 구현 착수를 승인한다.
- 상태: **DONE (2026-07-23, 문서화 완료 승인과 함께 착수 순서 포함하여 승인,
  이후 ADR-0005로 Workspace Core 범위/Interfaces 계층 구조를 재확정)**
- 의존성: T1-11

> **2026-07-23 Multi-Agent First 전환(ADR-0006~0009)으로 구현 작업 범위를
> 재구성함.** Agent가 핵심 도메인이 되고, Workspace Core는 Task를 직접 실행하지
> 않고 Agent에 위임하는 오케스트레이터가 된다. 순서: 디렉터리 확장 → 도메인 →
> Interfaces → Agent 도메인 추가 → 신규 Interface/EngineAdapter 확장 →
> Workspace Core 골격(Agent 위임) → 저장소 → CLI → 테스트.
>
> **참고: 이 구현 작업(T1-12~T1-28)은 계약과 골격까지만 만든다.** Agent/Engine/
> Adapter/EventBus/Interaction의 실제 처리 로직은 Milestone 2·3에서 구현한다.

#### T1-13: `src/ai_workspace/` 디렉터리 구조 생성
- 목적: 이후 모든 코드가 따를 디렉터리 구조를 확정한다.
- 작업 내용: `docs/ARCHITECTURE.md` §6에서 제안한 `domain/ interfaces/ core/
  storage/ engines/ adapters/ cli/` 구조를 실제로 생성한다 (로직 없이 패키지
  골격만).
- 완료 조건(DoD): 생성된 구조가 `docs/ARCHITECTURE.md`와 100% 일치한다.
- 상태: **DONE (2026-07-23)** — 최초 `domain/core/engines/adapters/cli/` 생성 후,
  ADR-0005 반영을 위해 `interfaces/`, `storage/` 패키지를 추가함. 각 패키지에
  빈 `__init__.py` 배치. 로직은 포함하지 않음.
- 의존성: T1-12

#### T1-14: 공통 도메인 모델 정의 (Project, Task, Workflow)
- 목적: Workspace Core와 Interfaces가 공통으로 참조할 핵심 데이터 모델을
  먼저 정의한다.
- 작업 내용:
  - `domain/project.py`: Project 모델(식별자, 이름, 목표, 상태, 우선순위)
  - `domain/task.py`: Task 모델과 `TODO → IN_PROGRESS → REVIEW → DONE
    (/BLOCKED/CANCELLED)` 상태 전이 규칙
  - `domain/workflow.py`: Task 목록과 의존관계를 표현하는 최소 Workflow 모델
    (순환 의존 감지 포함, 실행 로직은 Milestone 2에서 다룸)
- 완료 조건(DoD): 세 모델 각각에 대한 단위 테스트(정상 케이스 + 허용되지 않는
  전이/순환 의존 거부)가 통과한다.
- 상태: **DONE (2026-07-23)** — `domain/project.py`(Project, ProjectStatus),
  `domain/task.py`(Task, TaskStatus, 상태 전이 규칙), `domain/workflow.py`
  (Workflow, 순환/미지정 의존 검증) 구현. 테스트 실행을 위해 최소
  `pyproject.toml`(pytest `pythonpath=["src"]`)을 함께 추가하고 `pytest`를
  설치함.
  ※ Multi-Agent First 전환(ADR-0006)으로 Workflow는 "협업 흐름"으로 재정의되며,
    Agent 도메인 추가 및 Workflow 재정의는 후속 Task **T1-16**에서 진행한다.
- 의존성: T1-13

#### T1-15: Interfaces 정의 (7개)
- 목적: Workspace Core와 향후 구체 구현체가 공유할 추상 계약을 확정한다
  (ADR-0002, ADR-0005 반영). 계약만 정의하고 구체 구현은 하지 않는다
  (`ProjectRepository`의 구체 구현만 T1-23에서 별도 진행).
- 작업 내용: `interfaces/`에 아래 7개 인터페이스를 정의한다 (`abc.ABC` 또는
  `typing.Protocol` 사용).
  - `project_repository.py` — `ProjectRepository`
  - `workflow_engine.py` — `WorkflowEngine`
  - `task_engine.py` — `TaskEngine`
  - `memory_engine.py` — `MemoryEngine`
  - `approval_engine.py` — `ApprovalEngine`
  - `automation_engine.py` — `AutomationEngine`
  - `engine_adapter.py` — `EngineAdapter` (`run_task(task) -> EngineResult`)
- 완료 조건(DoD): 각 인터페이스에 대해 최소 Mock/Stub 구현체로 계약 준수를
  확인하는 단위 테스트가 통과한다 (실제 로직 없이 계약만 검증).
- 상태: **DONE (2026-07-23)** — 7개 Interface를 `abc.ABC`로 정의하고 각
  메서드 docstring에 입력/출력/예외/보장사항을 명시함. `tests/interfaces/fakes.py`에
  7개 Fake 구현체(테스트 전용, `src/`에는 포함하지 않음)를 작성하고 22개 계약
  테스트로 검증함.
  ※ Multi-Agent First 심화+안정화 보완(ADR-0010~0019)으로 신규 Interface 9종
    (AgentManager, AgentRepository, AgentRegistry, AgentScheduler,
    InteractionEngine, EventBus, EventStore, EngineRuntime, ContextManager)
    추가, MemoryEngine 계약 축소(Snapshot 이관), EngineAdapter 세션 생명주기
    계약 갱신은 후속 Task **T1-18~T1-21**에서 진행한다(총 16종, ADR-0022로
    책임 경계별 4개 Task로 분해).
- 의존성: T1-14

#### T1-16: 도메인 확장 (Mission/Workflow 재정의/Step, WorkspaceSession, Agent 계열, LLM Policy 초안)
- 목적: Multi-Agent First 심화 구조의 핵심 도메인을 추가·재정의하고, 향후
  Milestone(M2~M4)에서 구현할 LLM 선택 정책의 **Domain만** 미리 정의한다
  (ADR-0010~0012). **2026-07-23 사용자 지시로 LLM Policy Domain 초안이 이
  Task 범위에 추가됨** (Policy Engine/Router 등 실제 동작 로직은 제외).
- 작업 내용:
  - `domain/mission.py`, `domain/step.py`: `Mission`(목표), `Step`(Task 내부
    세부 실행 단위). `domain/workflow.py`는 Mission→Workflow→Task→Step 계층
    안에서 재정의(`mission_id` 추가, 기존 순환 의존 검증 유지).
  - `domain/session.py`: `WorkspaceSession`(현재 프로젝트/Mission/활성 Workflow/
    활성 Agent/Memory Snapshot/Engine Session).
  - `domain/agent.py`: `Agent`, `AgentRole`, `AgentCapability`(**Coordination**/
    Planning/Coding/Review/Documentation/Research/Vision/Voice/Git/MCP …),
    `AgentStatus`(IDLE/RUNNING/WAITING/PAUSED/STOPPED/ERROR 등).
  - `domain/llm_policy.py` (초안, Domain만): `LLMProvider`(OpenAI/Anthropic/
    Google/xAI), `LLMModel`(provider + 확장 가능한 name 문자열, 초기 모델 목록
    데이터 포함), `LLMEffort`(Low/Medium/High). **LLM Policy Engine, LLM Router,
    Provider/Model 선택 로직, Adapter 변경, 실제 LLM 호출 로직은 절대 구현하지
    않는다.**
  - `.ai/RULES.md`에 "Temporary LLM Policy" 섹션 추가(M2~M4 진행 경로 명시) +
    `docs/llm_policy.example.yaml` 정책 초안 작성.
- 완료 조건(DoD): 추가/재정의된 모델에 대한 단위 테스트가 통과한다(기존 도메인
  테스트 회귀 없음). LLM Policy는 Domain 정의와 문서만 존재하고 동작 로직이
  없음을 확인한다.
- 상태: **DONE (2026-07-23)** — `domain/mission.py`(Mission), `domain/step.py`
  (Step), `domain/session.py`(WorkspaceSession), `domain/agent.py`(Agent,
  AgentRole, AgentCapability(Coordination 포함), AgentStatus), `domain/workflow.py`
  에 `mission_id` 추가(기존 순환/미지정 의존 검증 유지), `domain/llm_policy.py`
  (LLMProvider, LLMModel, LLMEffort, INITIAL_MODELS — Domain 데이터만, Policy
  Engine/Router 없음) 구현. `.ai/RULES.md`에 "Temporary LLM Policy" 섹션
  (§7) 추가, `docs/llm_policy.example.yaml` 정책 초안 작성. 신규 테스트 9개
  추가(전체 41개 통과). `docs/ARCHITECTURE.md`는 변경하지 않음(사용자 지시).
- 의존성: T1-14

#### T1-17: Core/Agent/LLM Domain 마무리 및 코드 품질 도구(Ruff/MyPy) 도입
- 목적: T1-16에서 추가한 Domain을 완성도 있게 마무리하고(Task-Workflow 관계
  보완), 이후 모든 Task에서 상시 사용할 코드 품질 도구를 도입한다. **Domain만
  다루며 Policy Engine/Router/Adapter는 구현하지 않는다.**
- 작업 내용:
  - `domain/task.py`에 `workflow_id: str | None = None` 추가 — Task가 어떤
    Workflow에 속하는지 참조할 수 있도록 함(Mission→Workflow→Task→Step 계층의
    부모 참조 체계를 `Workflow.mission_id`, `Step.task_id`와 동일한 패턴으로
    완성). Workflow 배정 전에도 Task가 존재할 수 있어 선택 필드로 둠(필수 필드로
    하면 `TaskEngine.create_task(project_id, title)` 계약을 건드리게 되어
    Interface 변경이 필요해지므로, 이번 Domain 전용 범위에서는 선택 필드가 맞음).
  - Agent Domain 재검토: 특정 LLM Provider/Model에 의존하는 필드가 없는지
    확인 — 기존 구현이 이미 Provider 비의존임을 확인, 코드 변경 없음.
  - LLM Domain 재검토: `LLMModel`이 고정 Enum이 아니라 `provider + name` 조합의
    확장 가능한 구조인지 확인 — 기존 구현이 이미 이 요건을 만족함을 확인, 코드
    변경 없음.
  - `pyproject.toml`에 `[tool.ruff]`, `[tool.mypy]` 설정과 `dev` 선택적
    의존성(pytest/ruff/mypy)을 추가하고, `ruff`/`mypy` 위반을 모두 수정한다.
- 완료 조건(DoD): `ruff check src tests`, `mypy src`, `pytest` 모두 통과한다.
- 상태: **DONE (2026-07-23)** — `domain/task.py`에 `workflow_id` 필드 추가,
  관련 테스트 2개 추가(전체 43개 통과). `ruff`/`mypy` 설정 추가 및 위반 1건
  수정(줄 길이) 후 전부 통과. Agent/LLM Domain은 기존 구현이 요건을 이미
  만족하여 코드 변경 없음.
- 의존성: T1-16

> **2026-07-24 Task 분해 재검토**: T1-18을 "신규 Interface 정의 및 EngineAdapter
> 세션 계약 확장(총 16종)"이라는 단일 Task로 계획했으나, 아키텍처 검토 결과
> 서로 의존하지 않는 4개 하위 계층(Agent Runtime / Engine Runtime / Memory /
> Interaction)을 한 Task에 묶고 있어 "Task = 하나의 구현 목표 + 하나의 Commit"
> 원칙(ADR-0021)에 맞지 않는다고 판단함. 사용자 승인에 따라 T1-18을 4개 Task
> (T1-18~T1-21)로 분리하고, 이후 Task 번호를 T1-22~T1-28로 순연함(ADR-0022).
> **다만 "인터페이스 정의 → 구현 → 테스트"를 한 Task 안에서 끝내는 기존 원칙은
> 유지**하며, 인터페이스 정의 자체만 별도로 잘게 쪼개지 않는다(과도한 세분화
> 방지).

#### T1-18: Agent Runtime Interfaces
- 목적: Agent Runtime 계층(ARCHITECTURE.md §3.4)과 그 이벤트 인프라(§3.5)의
  계약을 확정한다 (ADR-0010, ADR-0018, ADR-0019). 계약만 정의하고 구체 구현은
  이후 Milestone에서 진행한다.
- 작업 내용 (`interfaces/`):
  - `agent_manager.py` — `AgentManager`(생성/생명주기/상태)
  - `agent_registry.py` — `AgentRegistry`(등록/조회/제거 — **런타임 등록부**,
    프로세스 생존 동안만 유지됨을 docstring에 명시하여 `AgentRepository`와 구분)
  - `agent_scheduler.py` — `AgentScheduler`(Capability 기준 선택/병렬/우선순위)
  - `agent_repository.py` — `AgentRepository`(조회/저장 — **영속 저장소**,
    재시작 후에도 유지됨을 docstring에 명시)
  - `event_bus.py` — `EventBus`(publish/subscribe)
  - `event_store.py` — `EventStore`(Bus의 **독립 구독자**, 기록/Replay/Audit;
    지금 구현 안 함, ADR-0018). `EventBus.subscribe()`가 다른 구독자와 동일한
    API로 EventStore를 등록해야 함(버스 내부에 EventStore 전용 특별 경로를
    두지 않음)을 계약에 명시한다.
- 완료 조건(DoD): 6개 인터페이스 각각에 대해 Fake 구현체 + 계약 테스트가
  통과한다 (실제 로직 없이 계약만 검증).
- 상태: **DONE (2026-07-24)** — `interfaces/agent_manager.py`,
  `agent_registry.py`, `agent_scheduler.py`, `agent_repository.py`,
  `event_bus.py`(+`Event` dataclass), `event_store.py` 6개 파일 추가. 각각
  Fake 구현체(`tests/interfaces/fakes.py`)와 계약 테스트
  (`test_agent_manager.py`/`test_agent_registry.py`/`test_agent_scheduler.py`/
  `test_agent_repository.py`/`test_event_bus.py`/`test_event_store.py`)를
  추가했으며, `test_event_bus.py`에 EventStore가 `EventBus.subscribe()`를
  다른 구독자와 동일한 경로로 등록됨(ADR-0018)을 검증하는 테스트를 포함함.
  `AgentRegistry`(런타임 등록부)와 `AgentRepository`(영속 저장소)는 각각
  `AgentNotRegisteredError`/`AgentNotFoundError`로 예외를 구분해 책임을
  명확히 함. `ruff check src tests`, `mypy src`, `pytest`(66개, 기존 43개 +
  신규 23개) 모두 통과.
- 의존성: T1-15, T1-16

#### T1-19: Engine Runtime Interfaces
- 목적: Engine Runtime과 EngineAdapter의 세션 생명주기 계약을 확정한다
  (ADR-0016). EngineRuntime의 엔진 선택 로직이 EngineAdapter의 정확한 메서드
  시그니처(`capabilities`/`estimate_cost`/`supports_parallel`)에 직접 의존하므로
  두 계약을 같은 Task에서 함께 정의한다.
- 작업 내용 (`interfaces/`):
  - `engine_runtime.py` — `EngineRuntime`(엔진 선택/세션 풀 관리/병렬 실행;
    ADR-0016)
  - `engine_adapter.py` 확장 — `create_session`/`run`/`cancel`/`status`/
    `destroy_session`/`capabilities`/`supports_parallel`/`estimate_cost`
    (기존 `run_task` 기반 계약/테스트를 새 계약으로 교체)
- 완료 조건(DoD): `EngineRuntime` Fake + 계약 테스트, 확장된 `EngineAdapter`
  Fake + 계약 테스트가 통과한다 (`run_task` 기반 기존 테스트는 새 계약으로
  교체됨).
- 상태: **DONE (2026-07-24)** — `interfaces/engine_adapter.py`를
  `create_session`/`run`/`cancel`/`status`/`destroy_session`/`capabilities`/
  `supports_parallel`/`estimate_cost` 세션 계약으로 교체(기존 `run_task` 제거,
  `EngineSessionStatus`/`CostEstimate`/`SessionNotFoundError` 추가).
  `interfaces/engine_runtime.py` 신규 추가 — `EngineRuntime`(엔진 선택/
  세션 풀 관리(내부 캡슐화)/병렬 실행 `run_parallel`; `DuplicateEngineError`/
  `NoSuitableEngineError`/`EngineTaskNotFoundError`). `tests/interfaces/
  fakes.py`의 `FakeEngineAdapter`/`FailingFakeEngineAdapter`를 새 계약에 맞게
  재작성하고 `FakeEngineRuntime`을 추가함. `test_engine_adapter.py`를 새
  계약 기준으로 재작성하고 `test_engine_runtime.py`를 신규 추가(총 13개
  테스트). `ruff check src tests`, `mypy src`, `pytest`(79개, 기존 66개 +
  신규 13개) 모두 통과.
- 의존성: T1-15

#### T1-20: Memory Interfaces
- 목적: Context 조립과 Memory 저장/검색의 역할 분리를 계약으로 확정한다
  (ADR-0017). `ContextManager`가 축소된 `MemoryEngine` 계약을 전제로 설계되므로
  같은 Task에서 함께 다룬다.
- 작업 내용 (`interfaces/`):
  - `context_manager.py` — `ContextManager`(Context 조립/Memory Snapshot
    생명주기; ADR-0017)
  - `memory_engine.py` 재확인 — 현재 구현(`remember`/`recall`)을 점검한 결과
    **Snapshot 관련 메서드가 애초에 존재하지 않아 제거할 코드가 없음을 확인**.
    "저장/검색만 담당"이라는 계약이 이미 만족되어 있으므로 **코드 변경 없음**
    (T1-17에서 Agent/LLM Domain을 재검토 후 변경 없음으로 처리한 것과 동일한
    패턴).
- 완료 조건(DoD): `ContextManager` Fake + 계약 테스트가 통과하고, `MemoryEngine`
  기존 계약·테스트에 회귀가 없음을 확인한다.
- 상태: **DONE (2026-07-24)** — `interfaces/context_manager.py` 신규 추가:
  `ContextManager`(`assemble_context`/`create_snapshot`/`restore_snapshot`,
  `SnapshotNotFoundError`). `WorkspaceSession.memory_snapshot_id`가 가리키는
  Snapshot을 Context Manager가 소유·관리하며 `MemoryEngine`은 이를 알지
  못함을 docstring에 명시. `memory_engine.py`는 재검토 결과 계획대로
  **코드 변경 없음**(Snapshot 관련 메서드가 원래 없어 이미 "저장/검색만"
  계약을 만족). `tests/interfaces/fakes.py`에 `FakeContextManager` 추가,
  `test_context_manager.py` 신규 추가(4개 테스트). 기존 `MemoryEngine`
  테스트(`test_memory_engine.py`)는 변경 없이 그대로 통과. `ruff check
  src tests`, `mypy src`, `pytest`(83개, 기존 79개 + 신규 4개) 모두 통과.
- 의존성: T1-15, T1-16

#### T1-21: Interaction Interfaces
- 목적: 입력 표면 정규화 계약을 확정한다 (ADR-0013). Agent Runtime/Engine
  Runtime/Memory 어느 것과도 의존관계가 없는 독립 계층이라 별도 Task로 둔다.
- 작업 내용 (`interfaces/`):
  - `interaction_engine.py` — `InteractionEngine`(입력 정규화; 기존
    `ConversationEngine` 명칭을 대체, 지금 구현 안 함)
- 완료 조건(DoD): `InteractionEngine` Fake + 계약 테스트가 통과한다.
- 상태: **DONE (2026-07-24)** — `interfaces/interaction_engine.py` 신규
  추가: `InteractionEngine`(`normalize`/`format_response`/
  `supported_surfaces`, `NormalizedRequest` dataclass,
  `UnsupportedSurfaceError`). 기존 `ConversationEngine` 명칭을 대체하며,
  Agent Runtime/Engine Runtime/Memory 어느 것에도 의존하지 않고 UI
  Surfaces와 Workspace Core 사이에만 위치함을 docstring에 명시.
  `tests/interfaces/fakes.py`에 `FakeInteractionEngine` 추가,
  `test_interaction_engine.py` 신규 추가(4개 테스트). `ruff check src
  tests`, `mypy src`, `pytest`(87개, 기존 83개 + 신규 4개) 모두 통과.
  (병렬로 진행된 별도 세션에서도 T1-21 구현이 제안되었으나
  `handle_request` 단일 메서드로 정규화와 응답 변환을 합쳐 Workspace
  Core의 책임과 경계가 흐려질 수 있어 채택하지 않고, ARCHITECTURE.md
  §3.2의 "정규화 + 변환" 2단계 책임에 그대로 대응하는 이 설계를 유지함.)
- 의존성: T1-15

#### T1-22: Workspace Core Skeleton
- 목적: 최상위 오케스트레이터로서 Workspace Core의 최소 형태를 마련한다
  (ADR-0005 유지 + ADR-0010 재정의). 실제 처리 로직은 포함하지 않는다.
- 작업 내용: `core/`에 다음 책임만 구현한다 (모두 Interfaces에만 의존).
  1. 프로젝트 로드 (`ProjectRepository`)
  2. 설정(Config) 로드
  3. 서비스 초기화
  4. WorkspaceSession 관리 (생성/갱신/종료)
  5. Agent Runtime · Engine Runtime 초기화 (Registry/Scheduler/Manager/EventBus,
     Engine Runtime 준비)
  6. Workflow 시작 (`WorkflowEngine`)
  7. 종료(Shutdown)
  ※ Task 실행은 Workspace Core가 하지 않고 **Agent Runtime에 위임**한다.
  ※ Registry/Scheduler/Manager/EventBus/EngineRuntime을 조립하는 코드가
    번거로워지면 `AgentRuntime` 파사드 인터페이스 도입을 재검토한다(지금은
    도입하지 않음 — YAGNI).
- 완료 조건(DoD): Mock Interfaces를 주입해 위 책임이 단위 테스트로 검증되고,
  Core 코드에 구체 클래스 직접 참조가 없음을 확인한다. **Task를 직접 실행하지
  않고 Agent Runtime에 위임함**을 테스트로 확인한다.
- 상태: DONE
- 의존성: T1-16, T1-18, T1-19

#### T1-23: Repositories
- 목적: Project/Agent 데이터와 이벤트 로그를 세션 간에 영속화한다 (ADR-0004,
  ADR-0014 반영).
- 작업 내용: `storage/`에 `FileProjectRepository`, `FileAgentRepository`,
  `FileEventStore`(append-only 로그)를 구현한다.
- 완료 조건(DoD): 세 구현체가 각 인터페이스 계약을 만족함을 테스트로 확인하고,
  Workspace Core에 주입해도 Core 코드 변경이 필요 없음을 확인한다.
- 상태: DONE
- 의존성: T1-18

#### T1-24: CLI
- 목적: 사람이 실제로 Project를 다뤄볼 수 있는 최소 진입점을 제공한다 (UI
  Surface의 하나).
- 작업 내용: `cli/`에 Workspace Core와 파일 저장소를 연결해 Project 생성·조회
  명령을 구현한다 (Agent/협업 실행은 구체 구현이 없는 이 시점에는 골격까지만).
- 완료 조건(DoD): CLI로 Project 생성 → 조회가 end-to-end로 동작한다.
- 상태: TODO
- 의존성: T1-22, T1-23

#### T1-25: Tests
- 목적: Test Before Complete 원칙에 따라 Milestone 1 전체 구현 산출물을
  마지막으로 한 번 더 점검한다. (개별 Task(T1-18~T1-24)는 각자 완료 조건에
  자체 테스트를 이미 포함하므로, 이 Task는 신규 테스트를 처음 작성하는 단계가
  아니라 **전체 스위트 통합 점검 및 커버리지 보강**이다.)
- 작업 내용: `pytest` 설정을 정리하고, `tests/{domain,interfaces,core,storage,
  cli}/` 전체를 훑어 누락된 컴포넌트별 테스트를 보강한다. `ruff`/`mypy`도 전체
  기준으로 함께 통과시킨다.
- 완료 조건(DoD): `ruff`, `mypy`, `pytest` 실행 시 전체가 통과한다.
- 상태: TODO
- 의존성: T1-16 ~ T1-24

#### T1-26: Documentation
- 목적: 문서와 실제 구현이 일치하는지 확인한다 (Documentation First).
- 작업 내용: 구현된 구조/디렉터리/컴포넌트를 ARCHITECTURE.md와 대조하고 필요 시
  갱신한다.
- 완료 조건(DoD): 문서와 실제 코드가 일치한다.
- 상태: TODO
- 의존성: T1-16 ~ T1-25

#### T1-27: ADR
- 목적: EngineAdapter(세션 생명주기 계약 포함) 설계와 파일 기반 저장 결정을 정식
  확정한다.
- 작업 내용: `.ai/DECISIONS.md`의 ADR-0002, ADR-0004 상태를 "승인됨"으로 갱신한다
  (ADR-0002는 ADR-0009·ADR-0015의 세션 생명주기 계약을 포함해 재확정).
- 완료 조건(DoD): 두 ADR 상태가 "승인됨"으로 표시된다.
- 상태: TODO
- 의존성: T1-19(ADR-0002), T1-23(ADR-0004)

#### T1-28: Milestone 1 Review
- 목적: Approval Required 원칙에 따라 Milestone 1 산출물을 검토받는다.
- 작업 내용: 도메인(Agent 포함), 전체 Interfaces, Workspace Core 골격, 저장소,
  CLI, 테스트 결과를 제시하고 승인을 요청한다. **T1-29(SOP Skills System)도
  Milestone 1 기간 중 추가된 산출물이므로 함께 검토 대상에 포함한다.**
- 완료 조건(DoD): 위 모든 Task가 DONE이고 테스트가 통과한 상태에서 사용자가
  승인한다.
- 상태: TODO
- 의존성: T1-01 ~ T1-27

#### T1-29: Standard Operating Procedure (SOP) Skills System
- 목적: LLM/구현 엔진에 독립적인 표준 작업 절차(SOP)를 `.ai/skills/`에
  문서화해, 이후 어떤 구현 엔진이 작업을 이어받아도 동일한 절차를 따르게
  한다.
- 작업 내용: `.ai/skills/`에 7개 SOP 가이드라인 문서를 추가한다
  (`Repository-Analysis.md`, `Architecture-Review.md`, `Task-Planning.md`,
  `Task-Implementation.md`, `Code-Review.md`, `Documentation.md`,
  `Milestone-Review.md`). 공통 8개 섹션 형식과 Repository First/Interface
  First/SOLID/YAGNI 등 이 프로젝트의 핵심 원칙을 반영한다.
- 완료 조건(DoD): 7개 문서가 동일한 형식을 따르고, `pytest`/`ruff`/`mypy`에
  회귀가 없다.
- 상태: **DONE (2026-07-24)** — 별도로 진행된 세션(`google-labs-jules[bot]`,
  PR #1)에서 작업되어 origin 브랜치에 먼저 병합됨. 원래 계획(T1-01~T1-28)에는
  없던 Task로, 병합 시점에 T1-28(Milestone 1 Review) 뒤에 편입함. 코드
  변경 없이 `.ai/skills/` 문서만 추가되어 기존 테스트에 영향 없음.
- 의존성: 없음 (Milestone 1의 다른 구현 Task와 독립적인 문서 작업)

---

## Milestone 2 — 멀티 에이전트 코어 (Multi-Agent Core)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 2 Definition of Done" 참고.
> 세부 Task(`T2-01`부터)는 Milestone 1 완료 승인 이후, 착수 시점에 이 문서에
> 추가한다 (Task Driven Development). 예정 작업 영역은 `docs/ROADMAP.md`의
> "Milestone 2" 섹션 참고 (Agent Runtime & Event Store & 기본 Agent / Core
> Engines & Context Manager 구현).

---

## Milestone 3 — 실행 엔진 연동 & 상호작용 (Engine Integration & Interaction)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 3 Definition of Done" 참고.
> 세부 Task(`T3-01`부터)는 Milestone 2 완료 승인 이후, 착수 시점에 이 문서에
> 추가한다. 예정 작업 영역은 `docs/ROADMAP.md`의 "Milestone 3" 섹션 참고
> (Engine Runtime & Engine Adapter 구현 / Interaction Layer 구현).

---

## Milestone 4 — 자동화 및 확장 (Automation & Scale)

> Milestone DoD: `docs/ROADMAP.md`의 "Milestone 4 Definition of Done" 참고.
> 세부 Task(`T4-01`부터)는 Milestone 3 완료 승인 이후, 착수 시점에 이 문서에
> 추가한다. 예정 작업 영역은 `docs/ROADMAP.md`의 "Milestone 4" 섹션 참고
> (자동화·다중 프로젝트·메모리 고도화).

---

## 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-07-23 | Phase 0 문서 세트(P0-1 ~ P0-10) 작성 완료. P0-11(Phase 0 완료 승인) 1차 요청. |
| 2026-07-23 | 사용자 피드백 반영: MEMORY 역할 명확화, ARCHITECTURE 컴포넌트/의존방향 보완,
ROADMAP·TASKS를 Milestone → Phase → Task 구조로 재구성. P0-11 재요청. |
| 2026-07-23 | 사용자가 Phase 0을 승인(P0-11 DONE)하고 Phase 1 착수 및 권장 순서(디렉터리 →
Workspace Core 골격 → 공통 도메인 모델 → Engine Adapter 인터페이스 → 파일 저장소 →
CLI → 테스트 환경)를 승인(P1-0 DONE). 해당 순서에 맞춰 Phase 1 Task(P1-1~P1-12)를
재구성함. ADR-0001을 "승인됨"으로 갱신. |
| 2026-07-23 | P1-1 완료: `src/ai_workspace/{domain,core,engines,adapters,cli}/` 패키지
골격 생성 (로직 없음). 다음 Task: P1-2 (Workspace Core 기본 골격 구현). |
| 2026-07-23 | 사용자 지시로 Workspace Core 범위(순수 오케스트레이터)와 Interfaces
계층 구조(ProjectRepository/WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/
AutomationEngine/EngineAdapter)를 확정함(ADR-0005). ARCHITECTURE.md v0.3.0으로
갱신하고, Phase 1 Task 순서를 "도메인 모델 → Interfaces 정의 → Workspace Core
골격 → ProjectRepository 구현 → CLI → 테스트"로 재구성(P1-1~P1-10). P1-1에
`interfaces/`, `storage/` 패키지 추가 반영. 다음 Task: P1-2 (공통 도메인 모델 정의). |
| 2026-07-23 | P1-2 완료: Project/Task/Workflow 도메인 모델 구현, `pytest` 10개
테스트 전부 통과. 다음 Task: P1-3 (Interfaces 정의 7개). |
| 2026-07-23 | P1-3 완료: 사용자 지시(계약 명시, Fake+계약 테스트 수준 검증)에 따라
ProjectRepository/WorkflowEngine/TaskEngine/MemoryEngine/ApprovalEngine/
AutomationEngine/EngineAdapter 7개 Interface를 계약(입력/출력/예외/보장사항 docstring
포함)으로 정의. Fake 구현체 + 계약 테스트 22개 작성, 전체(도메인 포함) 32개 테스트
통과. 다음 Task: P1-4 (Workspace Core 기본 골격 구현). |
| 2026-07-23 | **Multi-Agent First 전환**: 사용자 지시로 프로젝트 방향을 상시 멀티
에이전트 Workspace로 변경. 구현을 중단하고 아키텍처를 먼저 수정함. ADR-0006(Workspace
Core를 Agent 오케스트레이터로 재정의 + Agent Manager + Agent 도메인), ADR-0007(Event
Bus), ADR-0008(Conversation Layer), ADR-0009(EngineAdapter 확장 계약) 추가.
ARCHITECTURE.md v0.4.0, ROADMAP v0.3.0(M1~M4/Phase 0~6) 갱신. Phase 1을 P1-1~P1-12로
재구성(Agent 도메인 P1-4, 신규 Interface/EngineAdapter 확장 P1-5, Agent 위임형
Workspace Core P1-6 등). 기존 P1-1~P1-3 산출물은 유지. 구현 재개 대기. |
| 2026-07-23 | 사용자 지시로 `.ai/RULES.md`를 v0.2.0으로 재구성. 4개 그룹(Project
Principles / Development Workflow / Context Loading Rules / LLM Coding Rules)으로
정리하고 Interface First, Context Loading Rules, LLM Coding Rules(Think Before
Coding / Simplicity First / Surgical Changes / Goal-Driven Execution)를 추가함.
기존 언어·코딩·커밋 규칙은 공통 규칙으로 보존. |
| 2026-07-23 | **Multi-Agent First 심화**: 사용자 지시로 아키텍처를 재차 수정(문서만).
Agent Runtime 계층(Registry/Scheduler/Manager/Event Bus) 도입 + Workspace Core
책임 축소 + WorkspaceSession(ADR-0010), Mission→Workflow→Task→Step 계층(ADR-0011),
Capability 중심 Agent·Memory는 Engine(ADR-0012), Interaction Layer(ADR-0013),
Event Store(ADR-0014), EngineAdapter 세션 생명주기 계약(ADR-0015) 추가.
ARCHITECTURE.md v0.5.0, ROADMAP v0.4.0 갱신. Phase 1 P1-4~P1-7을 도메인 확장
(Mission/Step/WorkspaceSession/AgentCapability)·신규 Interface 7종·Agent Runtime
위임형 Workspace Core·EventStore 저장소로 갱신. 구현 재개 대기. |
| 2026-07-23 | **안정화 보완(P1-4 승인 조건)**: 사용자 권고 4건 반영(문서만).
Engine Runtime 계층 추가(Agent Runtime↔Engine Adapter 사이, ADR-0016), Context
Manager로 Memory Snapshot 역할 분리(ADR-0017), Event Store를 Event Bus 독립
Subscriber로 위치 조정(ADR-0018), Coordination Capability 추가(ADR-0019).
ARCHITECTURE.md v0.6.0, ROADMAP v0.5.0 갱신. Interfaces 14→16종(+EngineRuntime,
+ContextManager), MemoryEngine 계약 축소. Phase 1 P1-4~P1-6 반영. 구현 재개 대기. |
| 2026-07-23 | **P1-4 완료**: 사용자 지시로 범위를 확장해 Mission/Step/
WorkspaceSession/Agent 계열 도메인과 함께 **LLM Policy Domain 초안**(LLMProvider/
LLMModel/LLMEffort, Policy Engine·Router 제외)을 구현. `.ai/RULES.md`에
"Temporary LLM Policy" 섹션 추가, `docs/llm_policy.example.yaml` 작성. 신규
테스트 9개, 전체 41개 통과. `docs/ARCHITECTURE.md`는 변경하지 않음. 다음 Task:
P1-5 (신규 Interface 16종 정의 및 EngineAdapter 세션 계약 확장). |
| 2026-07-23 | **P1-5 완료**: 사용자 지시로 P1-5 범위를 "Core/Agent/LLM Domain
마무리 + 코드 품질 도구 도입"으로 재정의(기존 P1-5 "Interfaces 정의"는 P1-6으로
번호 이동, 이하 P1-6~P1-12를 P1-7~P1-13으로 순연). `domain/task.py`에
`workflow_id` 필드 추가(Task-Workflow 관계 보완). Agent/LLM Domain은 기존 구현이
요건(Provider 비의존, 확장 가능한 LLMModel 구조)을 이미 만족하여 코드 변경 없음.
`pyproject.toml`에 ruff/mypy 설정 추가, 위반 1건 수정 후 `ruff`/`mypy`/`pytest`
전부 통과(43개 테스트). `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`,
`.ai/DECISIONS.md`(ADR-0020) 갱신. 다음 Task: P1-6 (신규 Interface 16종 정의 및
EngineAdapter 세션 계약 확장). |
| 2026-07-24 | **Migration: Phase → Task 체계 전환 (ADR-0021)**. 사용자 지시로
프로젝트 관리 체계를 `Milestone → Phase → Task` 4단 계층에서 `Milestone → Task`
2단 계층으로 전환. 기능 구현/리팩터링/API 변경/기존 코드 변경은 전혀 하지 않음
(순수 문서 마이그레이션). 기존 Phase 0(P0-1~P0-11) + Phase 1(P1-0~P1-13) 총 25개
Task를 Milestone 1 소속 `T1-01`~`T1-25`로 그대로 재번호(내용·상태·이력 보존,
Migration Table은 `docs/ROADMAP.md` 하단 참고). Milestone 2~4는 아직 세부 Task가
없으므로 Phase 단위로 서술되어 있던 목표를 "예정 작업 영역"으로 재서술하고, 착수
시점에 `T2-01`/`T3-01`/`T4-01`부터 정의하기로 함. `docs/ROADMAP.md`,
`docs/ARCHITECTURE.md`, `.ai/DECISIONS.md`(ADR-0021), 본 문서, `.ai/MEMORY.md`,
`.ai/RULES.md`, `README.md`를 함께 갱신함. 다음 Task: **T1-18** (신규 Interface
16종 정의 및 EngineAdapter 세션 계약 확장 — 기존 계획상 "P1-6"과 동일한 작업). |
| 2026-07-24 | **T1-18 설계 검토 및 재분해 (ADR-0022)**. 사용자 요청으로 T1-18(신규
Interface 16종 정의 및 EngineAdapter 세션 계약 확장)의 설계를 검토함. Interface
계약 내용 자체는 대부분 유지(ADR-0010~0019에서 이미 충분히 근거가 검토된 결정)로
판정했으나, 서로 의존하지 않는 4개 아키텍처 하위 계층(Agent Runtime/Engine
Runtime/Memory/Interaction)을 하나의 Task로 묶은 것은 "Task = 하나의 구현
목표 + 하나의 커밋"(ADR-0021) 원칙에 어긋난다고 판단해 분리를 제안함. 사용자가
분리 방향을 승인하고 구체적인 분해 구조(T1-18~T1-28, 11개 Task)를 지시함. 이에
따라 기존 T1-18~T1-25(8개)를 T1-18~T1-28(11개)로 재구성: T1-18(Agent Runtime
Interfaces) / T1-19(Engine Runtime Interfaces) / T1-20(Memory Interfaces) /
T1-21(Interaction Interfaces) / T1-22(Workspace Core Skeleton, 구 T1-19) /
T1-23(Repositories, 구 T1-20) / T1-24(CLI, 구 T1-21) / T1-25(Tests, 구 T1-22) /
T1-26(Documentation, 구 T1-23) / T1-27(ADR, 구 T1-24) / T1-28(Milestone 1
Review, 구 T1-25). "인터페이스 정의 → 구현 → 테스트를 한 Task 안에서 완료"하는
기존 원칙은 유지하고, 구현/테스트를 별도 Task로 추가 분리하지는 않음. 부가 발견:
`memory_engine.py`는 이미 저장/검색만 담당하는 계약이라 T1-20에서 실질적인 코드
변경이 없음(No-Op). `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `.ai/DECISIONS.md`
(ADR-0022), `.ai/MEMORY.md`, `README.md`를 함께 갱신함. 다음 Task: **T1-18**
(Agent Runtime Interfaces). |
| 2026-07-24 | **T1-18 완료: Agent Runtime Interfaces**. 사용자 지시로 Agent
Runtime 계층(ARCHITECTURE.md §3.4)과 이벤트 인프라(§3.5)의 계약 6종을 정의함
(구현은 포함하지 않음). `interfaces/agent_manager.py`(`AgentManager`,
`InvalidAgentTransitionError`), `agent_registry.py`(`AgentRegistry`, 런타임
등록부 — `AgentNotRegisteredError`/`DuplicateAgentRegistrationError`),
`agent_scheduler.py`(`AgentScheduler`, Capability 기준 선택),
`agent_repository.py`(`AgentRepository`, 영속 저장소 —
`AgentNotFoundError`), `event_bus.py`(`EventBus`, `Event` dataclass,
`SubscriptionNotFoundError`), `event_store.py`(`EventStore`, `EventBus`의
독립 구독자, ADR-0018)를 추가함. `AgentRegistry`와 `AgentRepository`는 예외
이름을 다르게 하고 docstring에 런타임/영속 범위를 명시해 책임을 구분함.
`tests/interfaces/fakes.py`에 6개 Fake 구현체를 추가하고, 각 인터페이스별
계약 테스트 파일(`test_agent_manager.py` 등 6개, 총 23개 테스트)을 작성함 —
`test_event_bus.py`에는 `EventStore`가 `EventBus.subscribe()`를 다른 구독자와
동일한 경로로 등록됨을 검증하는 테스트를 포함함. `ruff check src tests`,
`mypy src`, `pytest`(66개, 전부 통과) 모두 통과함. 다음 Task: **T1-19**
(Engine Runtime Interfaces, 동일한 패턴). |
| 2026-07-24 | **T1-19 완료: Engine Runtime Interfaces**. Engine Runtime과
EngineAdapter의 세션 생명주기 계약을 확정함(ADR-0016). `interfaces/
engine_adapter.py`를 기존 `run_task` 단일 메서드 계약에서 세션 기반 계약
(`create_session`/`run`/`cancel`/`status`/`destroy_session`/`capabilities`/
`supports_parallel`/`estimate_cost`)으로 교체하고 `EngineSessionStatus`,
`CostEstimate`, `SessionNotFoundError`를 추가함. `interfaces/
engine_runtime.py`를 신규 추가해 `EngineRuntime`(엔진 선택, 세션 풀 관리는
구현체 내부로 캡슐화, `run_parallel`을 통한 병렬 실행)을 정의함 —
`DuplicateEngineError`/`NoSuitableEngineError`/`EngineTaskNotFoundError`.
Agent가 EngineAdapter를 직접 호출하지 않고 EngineRuntime을 거치는 의존
방향(ARCHITECTURE.md §8 규칙 6)을 계약에 명시함. `tests/interfaces/
fakes.py`의 `FakeEngineAdapter`/`FailingFakeEngineAdapter`를 새 계약으로
재작성하고 `FakeEngineRuntime`을 추가함. `test_engine_adapter.py`를 새
계약 기준으로 재작성(기존 `run_task` 기반 테스트 대체)하고
`test_engine_runtime.py`를 신규 추가함. `docs/ARCHITECTURE.md` §7
Interface 표를 갱신함. `ruff check src tests`, `mypy src`, `pytest`(79개,
기존 66개 + 신규 13개) 모두 통과. 다음 Task: **T1-20** (Memory Interfaces,
동일한 패턴). |
| 2026-07-24 | **T1-20 완료: Memory Interfaces**. Context 조립과 Memory
저장/검색의 역할 분리를 계약으로 확정함(ADR-0017). `interfaces/
context_manager.py`를 신규 추가해 `ContextManager`(`assemble_context`/
`create_snapshot`/`restore_snapshot`, `SnapshotNotFoundError`)를 정의함 —
`WorkspaceSession.memory_snapshot_id`가 가리키는 Snapshot을 Context
Manager가 소유·관리하고 `MemoryEngine`은 이를 알지 못함을 docstring에
명시함. `memory_engine.py`는 재검토 결과 Snapshot 관련 메서드가 애초에
없어 "저장/검색만" 계약을 이미 만족하고 있음을 확인, **코드 변경 없음**
(T1-17에서 Agent/LLM Domain을 재검토 후 변경 없음으로 처리한 것과 동일한
패턴). `tests/interfaces/fakes.py`에 `FakeContextManager`를 추가하고
`test_context_manager.py`를 신규 추가함(4개 테스트). 기존 `MemoryEngine`
계약·테스트는 변경 없이 그대로 통과해 회귀가 없음을 확인함.
`docs/ARCHITECTURE.md` §7 Interface 표를 갱신함. `ruff check src tests`,
`mypy src`, `pytest`(83개, 기존 79개 + 신규 4개) 모두 통과. 다음 Task:
**T1-21** (Interaction Interfaces, 동일한 패턴). |
| 2026-07-24 | **T1-21 완료: Interaction Interfaces**. 입력 표면 정규화
계약을 확정함(ADR-0013). `interfaces/interaction_engine.py`를 신규
추가해 `InteractionEngine`(`normalize`/`format_response`/
`supported_surfaces`, `NormalizedRequest`, `UnsupportedSurfaceError`)을
정의함 — 기존 `ConversationEngine` 명칭을 대체하고, Agent Runtime/Engine
Runtime/Memory 어느 것에도 의존하지 않고 UI Surfaces와 Workspace Core
사이에만 위치하는 독립 계층임을 docstring에 명시함.
`tests/interfaces/fakes.py`에 `FakeInteractionEngine`을 추가하고
`test_interaction_engine.py`를 신규 추가함(4개 테스트).
`docs/ARCHITECTURE.md` §7 Interface 표를 갱신함. `ruff check src tests`,
`mypy src`, `pytest`(87개, 기존 83개 + 신규 4개) 모두 통과. 이로써
T1-18~T1-21(Agent Runtime/Engine Runtime/Memory/Interaction Interfaces)
그룹이 모두 완료됨. **병합 메모**: 별도로 진행된 다른 세션에서도 같은
T1-21에 대해 `InteractionRequest`/`InteractionResponse`/
`InteractionError`/`InvalidRequestError` + `handle_request` 단일 메서드
설계를 독립적으로 구현해 origin 브랜치에 먼저 병합되어 있었음(PR #1).
두 설계가 병합 시점에 충돌하여 검토한 결과, `handle_request` 설계는
정규화와 Workspace Core의 응답 처리를 한 메서드로 묶어 Interaction
Layer와 Workspace Core의 책임 경계(ARCHITECTURE.md §3.2, §8 규칙 1~2)가
흐려질 수 있다고 판단해 채택하지 않고, 위 `normalize`/`format_response`
설계를 최종안으로 유지함. 다음 Task: **T1-22** (Workspace Core Skeleton). |
| 2026-07-24 | **병합: origin 브랜치의 병렬 작업 반영 (PR #1)**. `git push` 시
origin에 이미 다른 세션에서 병합한 커밋이 있어 `git merge`로 충돌을
해결함. T1-21 InteractionEngine은 위 병합 메모대로 이 세션의 설계
(`normalize`/`format_response`/`supported_surfaces`)를 유지함. 원래
계획에 없던 **T1-29(SOP Skills System)**: `.ai/skills/`에 7개 SOP
가이드라인 문서를 추가하는 순수 문서 작업으로, 코드/아키텍처와 충돌이
없어 그대로 수용하고 `.ai/TASKS.md`에 정식 Task로 편입함(T1-28 뒤,
Milestone 1 Review 검토 대상에 포함). `ruff check src tests`, `mypy src`,
`pytest`(87개, T1-21 관련 회귀 없음) 모두 통과 확인 후 병합 커밋 진행. |
| 2026-07-25 | **T1-22 완료: Workspace Core Skeleton**. `core/workspace_core.py`에
`WorkspaceCore`를 신규 구현함(ADR-0005, ADR-0010). 생성자에서
`ProjectRepository`/`WorkflowEngine`/`AgentRegistry`/`AgentScheduler`/
`AgentManager`/`EventBus`/`EngineRuntime` 7개 Interface와 `config:
dict[str, str]`를 키워드 전용으로 주입받아 보관한다 — Registry/Scheduler/
Manager/EventBus를 하나의 `AgentRuntime` 파사드로 묶지 않고 개별 필드로
유지함(T1-22 명세의 YAGNI 지시 그대로 따름). `load_project`(→
`ProjectRepository.load` 위임), `config` 프로퍼티(방어적 복사),
`start_session`/`get_session`/`update_session`/`end_session`(WorkspaceSession은
어떤 Interface로도 영속화 대상이 아니므로 Core 내부 in-memory 레지스트리로
관리, 신규 예외 `WorkspaceSessionNotFoundError`), `agent_registry`/
`agent_scheduler`/`agent_manager`/`event_bus`/`engine_runtime` 읽기 전용
프로퍼티(Milestone 2 구현체가 사용할 수 있도록 노출만 함), `start_workflow`
(→ `WorkflowEngine.plan` 위임), `shutdown`(모든 Session 정리)을 구현함.
**Task 직접 실행 금지 증명**: `run_task`/`execute_task` 같은 메서드를
아예 두지 않았고, 테스트에서 `run()`/`run_parallel()` 등 모든 메서드가
호출되면 `AssertionError`를 던지는 `SpyEngineRuntime`을 주입한 뒤 Core의
모든 공개 메서드를 호출해도 예외가 발생하지 않음을 확인해 Core가 Engine
Runtime을 스스로 호출하지 않음을 테스트로 증명함(`tests/core/
test_workspace_core.py`, 13개 테스트). `docs/ARCHITECTURE.md` §3.3·§9는
이미 이 설계와 일치해 변경하지 않음. `ruff check src tests`, `mypy src`,
`pytest`(100개, 기존 87개 + 신규 13개) 모두 통과. 다음 Task: **T1-23**
(Repositories: FileProjectRepository/FileAgentRepository/FileEventStore). |
| 2026-07-25 | **DX-01 완료: Stage Checkpoint + Smart Model Router 통합**
(`.ai/DECISIONS.md`의 `DX-01` 항목 참고 — 시스템 아키텍처 결정이 아니라 AI
세션 운영 절차 변경이라 ADR 번호를 소비하지 않고, Milestone 1의 T1-XX Task도
아니라 별도 Task ID 없이 진행 로그로만 기록함). `.ai/RULES.md`에 §2.4 Stage
Checkpoint를 신규 추가: Task 내부 4개 작업 단계 경계(Analysis/
Implementation/Validation/Task 완료 — `Task-Planning.md`/
`Task-Implementation.md` §5.1~5.6 절차 경계에 대응)마다 Smart Model
Router(`.claude/skills/smart-model-router`)를 실행해 Recommendation
(model/effort/confidence/reason)을 산출하고, Manual Recommendation
Executor(사용자 선택 + 한국어 UI + `/model` 안내 후 대기)로 소비함. "Phase"
대신 **"Stage"**를 공식 명칭으로 채택함(ADR-0021에서 이미 폐지된 프로젝트
관리 계층 "Phase"와의 혼동 방지). 동일/상향/하향 어떤 경우도 Model/Effort를
자동 전환하지 않으며, 불필요한 UI 노출을 막는 Skip Rule을 정의함. §5.1
언어 규칙을 세션 중 사용자에게 보이는 모든 메시지(진행 상황/질문/완료
보고/추천 결과/오류 안내/승인 요청)로 확장하고, 기술 용어(Model/Effort/
pytest/ruff/mypy/Commit Message/클래스·함수·파일명/API)는 원문 유지로
명시함. `Recommendation`의 실제 Python 구현은 Task Driven Development
원칙에 따라 지금 하지 않고 §7 로드맵(M2 이후)으로 미룸 — 지금은 §2.4 안의
개념적 스키마로만 정의함. `Task-Planning.md`(1곳), `Task-Implementation.md`
(3곳: §5.3→5.4, §5.4→5.5, §5.6 뒤)에 Stage Checkpoint 상호 참조를 추가함.
`README.md`/`docs/ARCHITECTURE.md`는 변경하지 않음(시스템 아키텍처가 아님).
적용 대상 소스 코드 없음(문서 전용 변경). |
| 2026-07-25 | **T1-23 완료: Repositories**(§2.4 Stage Checkpoint 적용,
Sonnet/Medium). `storage/`에 `FileProjectRepository`/`FileAgentRepository`
(엔티티당 JSON 파일 1개)/`FileEventStore`(단일 append-only JSON Lines
로그)를 구현함. Enum/frozenset은 JSON 직렬화가 안 되어 각 구현체 내부에서
`.value`↔생성자로 변환하고 도메인 모델(`Project`/`Agent`/`Event`)은 건드리지
않음. `tests/storage/`에 21개 신규 테스트 추가 — CRUD, Interface 계약
예외(`ProjectNotFoundError`/`AgentNotFoundError`), `replay(since_event_id)`
순서·필터링, 그리고 파일 기반의 핵심 차별점인 "새 인스턴스로 재오픈해도
데이터 유지"를 검증함. DoD의 "Workspace Core 주입 시 Core 코드 변경
불필요"는 `FileProjectRepository`를 `WorkspaceCore`에 직접 주입하는 테스트로
증명함(`AgentRepository`/`EventStore`는 T1-22 설계상 Workspace Core
생성자의 직접 의존 대상이 아니므로 해당 없음 — Agent Runtime/Event Bus
독립 구독자가 Milestone 2에서 사용할 대상). `ruff check src tests`,
`mypy src`, `pytest`(121개, 기존 100개 + 신규 21개) 모두 통과. 다음 Task:
**T1-24** (CLI).

**DX-01 첫 실사용 회고**: §2.4의 4개 Stage Checkpoint 중 실제로 Smart Model
Router가 재판단을 수행한 것은 Task 착수 전 1회뿐이었다. Implementation→
Validation, Validation→문서화 경계에서는 §2.4가 최소 요구하는 Skip Rule
한 줄 출력조차 하지 않고 통과함 — 규칙 자체의 결함이 아니라 실행 누락으로
판단됨(규칙은 정확히 쓰여 있음). Skip Rule 경로는 이번에 한 번도 실행되지
않아 검증되지 못함. 표시된 한국어 UI(박스 2회)는 승인된 템플릿과 일관됨.
TASKS.md 편집 중 `old_string` 오지정으로 텍스트를 잘못 덮어썼다가 즉시
되돌린 실수가 1건 있었음(Effort 인과관계는 불명확하나 참고 신호로 기록).
T1-24부터는 나머지 경계에서도 실제로 멈춰 재판단하기로 함. |
