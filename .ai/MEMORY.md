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

- **관리 체계**: 2026-07-24부로 `Milestone → Phase → Task`에서 **`Milestone →
  Task`**로 전환됨 (ADR-0021). Task ID는 `T{Milestone 번호}-{일련번호}` 형식
  (예: `T1-18`). 과거 Phase 0/Phase 1의 모든 Task(P0-1~P0-11, P1-0~P1-13)는
  Milestone 1 소속 `T1-01`~`T1-25`로 번호만 이어졌다가, 같은 날 설계 검토를
  거쳐 `T1-18`~`T1-28`로 추가 재분해됨(ADR-0022, 대응표는 `docs/ROADMAP.md`
  하단 참고).
- **현재 위치**: **Milestone 1(기반 구축) 완료 — 2026-07-25 사용자 승인.**
  `T1-01`~`T1-29` 전체 DONE(T1-28 Milestone 1 Review 포함). 다음은
  Milestone 2(멀티 에이전트 코어) 목표/DoD 확정 후 `T2-01`부터 착수(아직
  세부 Task 미정의 — Task Driven Development 원칙상 착수 시점에 정의).
- **완료된 Task 요약**: `T1-01`~`T1-11`(문서화 세트 작성 및 승인), `T1-12`
  (구현 착수 승인), `T1-13`(디렉터리 구조), `T1-14`(Project/Task/Workflow
  도메인), `T1-15`(Interfaces 7종), `T1-16`(Mission/Step/WorkspaceSession/
  Agent 계열 + LLM Policy 초안), `T1-17`(Task-Workflow 관계 보완 +
  Ruff/MyPy 도입), `T1-18`(Agent Runtime Interfaces 6종:
  AgentManager/AgentRegistry/AgentScheduler/AgentRepository/EventBus/
  EventStore — 구현 없이 계약만 정의, Fake+계약 테스트 포함), `T1-19`(Engine
  Runtime Interfaces: `EngineRuntime` 신규 + `EngineAdapter`를 `run_task`
  단일 메서드에서 세션 기반 계약(`create_session`/`run`/`cancel`/`status`/
  `destroy_session`/`capabilities`/`supports_parallel`/`estimate_cost`)으로
  교체), `T1-20`(Memory Interfaces: `ContextManager` 신규 정의 —
  `assemble_context`/`create_snapshot`/`restore_snapshot`; `MemoryEngine`은
  재검토 후 변경 없음), `T1-21`(Interaction Interfaces: `InteractionEngine`
  신규 정의 — `normalize`/`format_response`/`supported_surfaces`, 기존
  `ConversationEngine` 명칭 대체), `T1-29`(SOP Skills System: `.ai/skills/`
  에 7개 표준 작업 절차 문서 추가, 별도 세션에서 완료되어 병합됨), `T1-22`
  (Workspace Core Skeleton: `core/workspace_core.py`에 `WorkspaceCore` 구현
  — Project 로드/Config 보관/WorkspaceSession in-memory 관리(생성·갱신·
  종료)/Agent Runtime·Engine Runtime Interface 보관(읽기 전용 프로퍼티)/
  Workflow 시작(`WorkflowEngine.plan` 위임)/Shutdown; Task 실행 메서드를
  아예 두지 않고 `SpyEngineRuntime`으로 "직접 실행하지 않음"을 테스트로
  증명), `T1-23`(Repositories: `storage/`에 `FileProjectRepository`/
  `FileAgentRepository`(엔티티당 JSON 파일)/`FileEventStore`(단일
  append-only JSON Lines 로그) 구현. Enum/frozenset 직렬화는 구현체
  내부에서만 처리해 도메인 모델은 변경하지 않음. `FileProjectRepository`를
  `WorkspaceCore`에 직접 주입해 Core 코드 변경 없이 동작함을 테스트로
  증명), `T1-24`(CLI: `cli/main.py`에 argparse 기반 `project create`/
  `project show` 구현. `WorkspaceCore`는 6개 미구현 Interface를 필수로
  요구해 지금은 `FileProjectRepository`를 직접 사용하기로 결정 — 완전 연동은
  Milestone 2+ Agent/Engine Runtime 구체 구현 이후로 미룸. §2.4 Stage
  Checkpoint 4개 경계가 처음으로 모두 실제 발동함), `T1-25`(Tests: 전체
  스위트 통합 점검 — `tests/interfaces/`는 이미 탄탄해 보강 불필요로 판단,
  `tests/core/test_workspace_core.py`(6개: update_session 나머지 필드/
  config 기본값/start_session 기본값/unknown session 예외), `tests/domain/
  test_task.py`(5개: DONE·CANCELLED 종단 상태, BLOCKED 순환, REVIEW 반려,
  TODO→CANCELLED), `tests/domain/test_workflow.py`(1개: 3노드 간접 순환)
  보강. 프로덕션 코드 변경 없음), `T1-26`(Documentation:
  `docs/ARCHITECTURE.md` v0.7.0 — 문서 헤더 상태, §7 Interface 표(
  `ProjectRepository`/`AgentRepository`/`EventStore`를 "완료(계약+구현)"로
  세분화), §9 디렉터리 구조(`core`/`storage`/`cli` 완료 표시) 3곳만 실제
  구현과 대조해 수정. 시스템 구조 자체는 이미 일치해 변경 없음) — 전체
  139개 테스트 통과(회귀 없음), `ruff`/`mypy` 클린), `T1-27`(ADR:
  `.ai/DECISIONS.md`의 ADR-0002(EngineAdapter 세션 생명주기 계약,
  ADR-0009·ADR-0015 반영해 재확정)/ADR-0004(파일 기반 저장 — 실제로는
  JSON만 채택되었음을 확인)를 "제안"→"승인됨"으로 확정. 소스 코드 변경
  없음), `T1-28`(Milestone 1 Review: 도메인/Interfaces 16종/Workspace
  Core/저장소/CLI/테스트 결과를 종합 제시하고 사용자 승인을 받음. 미결
  항목(Interfaces 13종 구체 구현 등)은 계획대로 Milestone 2·3으로 이월) —
  전체 139개 테스트 통과(회귀 없음), `ruff`/`mypy` 클린.
- **Milestone 1 Task 구조는 모두 완료됨** (T1-01~T1-29). 남은 작업 없음 —
  다음은 Milestone 2 착수.
- **아키텍처는 v0.6.3으로 갱신** (ADR-0006~0022, Multi-Agent First 심화 + 안정화
  보완 + Task-Workflow 관계 보완 + Phase→Task 거버넌스 전환 + Task 분해 원칙).
  시스템 구조 자체(컴포넌트/의존성)는 T1-18 설계 검토로 변경되지 않았음 — 자세한
  내용은 §3, `docs/ARCHITECTURE.md` §0 참고. `docs/ARCHITECTURE.md` §7의
  Interface 표는 T1-18(Agent Runtime 6종), T1-19(EngineRuntime,
  EngineAdapter 계약), T1-20(ContextManager), T1-21(InteractionEngine)에서
  정의한 Interface 상태를 "완료"로 갱신함. Milestone 1의 계약 정의 Task
  (T1-18~T1-21)가 모두 끝났으므로 다음은 구현 단계(T1-22 이후)로 넘어간다.
  T1-29(SOP Skills)는 별도 세션의 병렬 작업이 origin에 먼저 병합되어 있어
  `git merge`로 반영함 — `.ai/skills/`에 문서만 추가되어 코드/아키텍처
  변경은 없음.
- **Milestone 2(멀티 에이전트 코어) 완료 — 2026-07-25 사용자 승인.**
  `T2-01`~`T2-08` 전체 DONE. Agent Runtime(`AgentRuntime`/`InMemory
  AgentScheduler`/`InMemoryEventBus`), Core Engines 4종, Memory 계열
  (`InMemoryContextManager`가 `MemoryEngine`을 실제로 주입받아 사용),
  Engine Runtime+`MockEngineAdapter`, 능력별 Agent 4종(Planning/Coding/
  Review/Documentation)을 구현해 `MissionPlanned`→`CodeCompleted`→
  `ReviewCompleted`→`DocumentationCompleted` Event 체인이 실제로 동작함
  (Event Store 기록·Mission→Workflow→Task→Step 다단계 계획 포함). 전체
  205개 테스트 통과, `ruff`/`mypy` 클린.
  **Retrospective 결론**(전문은 `.ai/TASKS.md` T2-08 항목): Goal/DoD 3개
  항목 전부 달성, 아키텍처 변경 불필요(ARCHITECTURE.md와 구현 일치 유지).
  기술 부채는 **Deferred by Design**(#1 `AgentManager`/`AgentRegistry`
  프로덕션 구현 없음, #2 CLI-WorkspaceCore 미완전 연동, #5 병렬성 실제
  미검증)과 **Implementation Observation**(#3 `InMemoryEventBus` 재귀
  발행 시 수신 순서 뒤집힘, #4 Event ID 생성 방식 컴포넌트별 불일치,
  #6 `Step` 도메인이 아직 Workflow 실행에 미반영)으로 구분해 기록.
  "Milestone 2는 계획된 범위를 모두 완료했으며 남은 항목은 미완료가 아니라
  M3 이상 확장 범위 또는 의도적 이월"임을 명시적으로 선언.
  **설계 철학(DX-02)**이 T2-07에서 첫 공식 적용됨 — 기존 테스트 점검 후
  실제 빈틈만 채우는 방식으로 새 파일 0개 생성.
- **Milestone 3(실행 엔진 연동 & 상호작용) 완료 — 2026-07-25 사용자 승인.**
  `M3-T01`~`M3-T08` 전체 DONE. `ManagedEngineRuntime`(생명주기/Timeout/
  Cancel/Event, T2-05의 `InMemoryEngineRuntime`은 목적이 달라 전혀
  건드리지 않음) → `ClaudeCodeEngineAdapter`(실제 Claude Code CLI
  서브프로세스, 로컬 `--help` + 1회 실제 호출로 `--output-format json`
  스키마 검증 후 구현) → `ProcessRunner`(`subprocess.Popen` 기반, 실제
  프로세스를 강제 종료 가능) → `RecoveringEngineRuntime`(실패·예외 시
  재시도하는 데코레이터, 재시도 소진 시 예외는 계약대로 그대로 재전파) →
  `EngineApprovalPipeline`(실행 전 사람 승인 게이트, `ApprovalEngine`·
  `EngineRuntime`·`EventBus` 3개 대등 의존성 조합, 상태 머신 새로 안 만듦)
  → `WorkspaceCore`(`EngineSession` 추적 — `AgentSession`/
  `WorkspaceSession`과 공통 `BaseSession` 없이 독립 유지) 전체가 같은
  `EventBus`를 공유하며 실제 구현으로 연결되어 동작함을 E2E 테스트(순서
  포함 Event 검증)로 증명(M3-T07). **M3 전체에서 새 Interface(ABC)를
  하나도 추가하지 않음** — Milestone 1의 `EngineRuntime`/`EngineAdapter`
  계약만으로 실행 엔진 전체를 구현. 전체 281개 테스트 통과, `ruff`/
  `mypy` 클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M3-T08 "Milestone 3
  Review" 참고): 사용자 제공 8개 Task 체크리스트 기준 전부 충족. Review
  중 원래 `docs/ROADMAP.md` M3 DoD와 대조해 자체적으로 2개 항목
  (Interaction Layer 미구현, `CodingAgent`의 실제 Engine 경로 미검증)이
  8개 Task 범위에 애초에 포함되지 않았음을 발견·보고했고, 사용자 승인으로
  두 항목은 **Milestone 4로 공식 이관**됨(M3 미완료가 아니라 범위 재정의).
  기술 부채는 M3에서 의도적으로 미구현(Retry Backoff/Persistent Runtime
  Recovery/실제 CLI 기반 E2E/Approval 비동기 처리/Process Timeout 정책
  고도화)과 M2 이월 항목(#1 AgentManager/Registry 프로덕션 구현, #2 CLI-
  WorkspaceCore 연동, #5 병렬성 실제 검증 — 전부 여전히 미해결)으로
  구분해 `.ai/TASKS.md`에 기록.
- **Milestone 4(자동화 및 확장) 완료 — 2026-07-26 사용자 승인.**
  `M4-T01`~`M4-T09` 전체 DONE. `InMemoryAgentManager`/`InMemoryAgentRegistry`
  (M4-T01, M2 이월 부채 #1 해소) → `WorkspaceCore.save_project()`로
  CLI가 `WorkspaceCore`를 유일한 진입점으로 사용(M4-T02, 부채 #2 해소) →
  `InMemoryInteractionEngine`(M4-T03, CLI는 이미 구조화된 입력이라 이
  계층을 거치지 않는 예외 Surface로 문서화) → `CodingAgent` 파이프라인이
  M3 실제 Engine 스택(`ClaudeCodeEngineAdapter`+`ManagedEngineRuntime`+
  `RecoveringEngineRuntime`) 위에서도 동작함을 소스 변경 없이 새 테스트로
  증명(M4-T04, Runtime/Agent Event 정확한 중첩 순서·재시도 실증 포함) →
  `WorkspaceCore.list_projects()`+CLI `project list`(M4-T05, 다중
  프로젝트 운용·세션 격리·Project 객체 독립성 검증) → **ADR-0023**으로
  `AgentScheduler`(선택)/`EngineRuntime`(실행) 병렬 책임 경계를 확정하고
  `ManagedEngineRuntime.run_parallel()`을 `ThreadPoolExecutor` 기반 실제
  동시 실행으로 재구현(M4-T06, 부채 #5 해소, Effort High 승인) →
  `AutomationEngine.bind_workflow`/`fire`(M4-T07, fire()는 Workflow
  반환만 하고 실행은 호출자 책임 — `InMemoryAutomationEngine`이
  `WorkflowEngine`에 의존하지 않도록 결합도 최소화) →
  `MemoryEngine.search()`+`ContextManager.find_snapshots()`(M4-T08,
  검색만 구현, 요약은 LLM Router 준비 이후로 이관). **M4 전체에서 새
  Interface(ABC) 파일을 하나도 추가하지 않음**(3개 기존 Interface에
  메서드만 순수 추가) — M1~M4 내내 Interface First가 실증됨. 전체
  331개 테스트 통과(M3 완료 시점 281개 → M4에서 50개 신규), `ruff`/
  `mypy` 클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M4-T09 "Milestone 4
  Review" 참고): ROADMAP DoD 3개 항목 중 자동화·다중 프로젝트는 완전
  충족, 메모리는 검색만 충족(요약은 사전 합의된 범위 조정, M3처럼 뒤늦게
  발견한 gap이 아님). M2/M3에서 이월된 부채(#1/#2/#5, Interaction Layer,
  CodingAgent 통합) 전부 해소. 신규 부채: `RecoveringEngineRuntime`이
  병렬 배치 내 개별 Task 재시도 미지원, `MemoryEngine.search()` 선형
  스캔.
  **ADR-0024 신규 — v0.5.0 아키텍처 기준선(Baseline) 선언**(사용자
  제안): `pyproject.toml` 버전을 `0.1.0`→`0.5.0`으로 상향. 근거: M2·M3·
  M4 세 Milestone 내내 새 최상위 Interface가 한 번도 추가되지 않아 M1의
  Interface 설계가 구조적으로 안정적임이 반복 확인됨. 이후 M5+는 기존
  16종 Interface·계층 구조를 기본값으로 유지하고 새 기능은 그 위에
  조립하며, 구조 변경이 필요하면 지금까지처럼 "Interface 변경 여부
  우선 검토" 절차를 거친다.
- **Milestone 5(실제 개발 수행) 완료 — 2026-07-26 사용자 승인.**
  `M5-T01`~`M5-T07` 전체 DONE. `LLMPolicyEngine`(M1 이후 첫 신규 최상위
  Interface, 총 17종, `.ai/RULES.md` §7 로드맵의 M2~M3 단계를 소급
  구현) → `AgentRuntime`이 `start_agent()` 시점에 정책을 조회해
  `AgentSession.llm_policy_decision`에 기록(M5-T02, 실제 Adapter 전환은
  아직 없음 — 여러 Adapter가 실제로 생기기 전까지 의미 없음) →
  `DevelopmentContext`로 Coding→Review 사이 실제 산출물이 이어짐(M5-T03,
  `EngineAdapter.run()` 계약 무변경) → `ShellAgent`(실제 쉘 실행,
  화이트리스트+고정 명령으로 명령어 삽입 방지, M5-T04) →
  `CLIProvider`+`CLIEngineAdapter` 프레임워크로 Codex/Gemini 지원(M5-T05,
  `ClaudeCodeEngineAdapter`는 별도 유지·2단계 전략, CLI 미설치로 검증은
  WebSearch 공개 문서 기반) → `CoordinatorAgent`(ADR-0019 Coordination
  Capability 최초 구현체)가 테스트 결과에 따라 `ReviewAgent`(트리거를
  `CODE_COMPLETED`→`CODE_VERIFIED`로 재배선)로 보내거나 `CodingAgent`로
  재작업시킴(M5-T06, `max_rework_attempts`로 무한 루프 방지, Step 이력은
  `TaskEngine.record_step()`으로 실행 컨텍스트가 소유 — M2 이월 부채 #6
  해소). 파이프라인이 Planning→Coding→Shell→Coordinator→Review→
  Documentation 6-Agent 구성으로 확장됨. 전체 398개 테스트 통과(M4
  완료 시점 331개 → M5에서 67개 신규), `ruff`/`mypy` 클린. 프로젝트
  최초 외부 런타임 의존성(`pyyaml`) 추가.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M5-T07 참고): M5-T01~06
  6개 Task 전부 완료, PRD 7.8/7.3 갭 해소. **M2~M4와 달리 새 최상위
  Interface 1개(`LLMPolicyEngine`) 추가** — RULES §7이 애초에 예정해둔
  계약이 실현된 것으로 Interface First 원칙 위반은 아님. 신규 부채:
  정책→실행 자동 연결 미완성(라우팅 로직 없음), Codex/Gemini CLI 실사용
  미검증, `ClaudeCodeEngineAdapter`/`CLIEngineAdapter` 미통합, Memory
  요약은 여전히 차단(정책 결정≠실제 LLM 호출 서비스). M2 이월 부채
  #1/#2/#4/#5/#6 모두 해소, #3(EventBus 재귀 발행 순서)만 그대로 유지.
- **Milestone 6(Policy 기반 실행 라우팅) 완료 — 2026-07-26 사용자 승인.**
  목표는 "Policy→Execution 라우팅 완성" — RULES §7 로드맵의 "M4 단계"
  (Policy Engine 자동 선택)를 완성해 `LLMPolicyDecision`에 따라
  `CodingAgent`/`ReviewAgent`/`DocumentationAgent`가 실제로 다른
  `EngineAdapter`(Claude Code/Codex/Gemini CLI)를 골라 실행하게 함.
  근본 원인은 `ManagedEngineRuntime`이 Adapter를 정확히 1개만 등록
  가능하도록 M3-T01에서 의도적으로 좁혀 둔 것이었다 — `EngineRuntime`
  인터페이스 자체는 이미 다중 등록·Capability 기준 선택을 계약해
  두었으므로 **인터페이스 변경 없이 구현체만 갱신**(M6-T01: `dict[str,
  EngineAdapter]`로 교체 + `_task_adapters`로 task별 실행 어댑터 추적).
  `domain/llm_policy.py`에 `LLMProvider→capability` 태그 매핑(ANTHROPIC→
  `claude_code`/OPENAI→`codex`/GOOGLE→`gemini`)과 `required_capabilities()`
  순수 함수를 추가해 Agent 3종이 이를 `engine_runtime.run()`에 전달(M6-T02,
  정책 없으면 빈 집합으로 하위 호환). `tests/integration/
  test_m6_policy_routing.py`(M6-T03)로 3개 Adapter를 동시 등록하고 저장소의
  실제 `docs/llm_policy.example.yaml`을 로드해 Coding/Review/Documentation이
  각각 claude/codex/gemini CLI를 실제로 호출함을 E2E로 증명. **소스 파일
  5개만 수정, 신규 소스 파일 0개, 새 Interface 0개 추가**(M2/M3/M4와 동일
  패턴). 전체 `pytest` 416개(M5 완료 398개 → M6에서 18개 신규) 통과,
  `ruff`/`mypy` 클린. `poetry.lock`을 이번 Milestone에서 최초로 커밋함
  (재현 가능한 의존성 고정, 코드 변경 아님).
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M6-T04 참고): 완성한
  것은 **Provider 단위** 라우팅(어느 CLI를 쓸지)뿐이고, 같은 Provider
  안의 **Model/Effort**(opus vs sonnet, low vs high)는 실제 실행에
  아직 반영되지 않음 — `EngineAdapter.run()`이 Model/Effort를 인자로
  받지 않기 때문. `EngineAdapter` 계약 확장이 필요한 더 큰 결정이라
  **M7+ 논의 대상으로 명시적으로 이월**. 그 외 이월 부채(Adapter 계열
  통합, Codex/Gemini CLI 실검증, `run_parallel` 개별 재시도,
  `MemoryEngine.search` 성능, `ShellAgent` 화이트리스트 고정, Memory
  Engine 요약 미구현)는 사용자 확정대로 전부 그대로 이월.
- **Milestone 7(Memory 요약) 완료 — 2026-07-26 사용자 승인.** 목표는
  PRD 7.4(장기 메모리)와 M4 DoD가 원래 요구했던 "검색/요약" 중 "요약"만
  M4-T08에서 "LLM 없이는 구현 불가"로 미뤄뒀던 것을 완성. M6에서 실제
  LLM 호출 인프라(`EngineRuntime`→`EngineAdapter`)가 완성되어 이 차단
  사유가 해소됨. 핵심 설계 발견: `DocumentationAgent`가 이미
  `engine_runtime.run()`을 호출하고 있었지만 **반환값을 캡처하지 않고
  그대로 버리고 있었다** — 이 결과를 재활용하면 신규 LLM 호출 없이도
  요약을 만들 수 있음(YAGNI). `interfaces/context_manager.py`의
  `create_snapshot()`에 `summary: str | None = None`(기본값 있음, 하위
  호환) 파라미터만 추가(M7-T01) — `MemoryEngine`은 여전히 저장/검색만
  담당하고 요약이 뭔지 전혀 모름(ADR-0017 경계 그대로 유지).
  `DocumentationAgent`가 `result = engine_runtime.run(...)`으로 캡처한
  `output`을 `create_snapshot(session, summary=result.output)`으로
  전달(M7-T02, 2줄 변경). 저장된 요약은 기존 `MemoryEngine.search()`
  (M4-T08)로 그대로 검색되어 별도 구현 없이 PRD 7.4 "검색/요약"을 함께
  충족. `tests/agents/test_pipeline.py`의 기존 `build_pipeline()` 헬퍼를
  재사용해 전체 파이프라인 실행 후 요약이 검색·복원됨을 E2E로 증명
  (M7-T03, 새 테스트 픽스처 없이 기존 것 재사용). **소스 파일 3개만
  수정, 신규 소스 파일 0개, 새 Interface 0개 추가**(M6보다도 더 작은
  변경 폭). 전체 `pytest` 425개(M6 완료 416개 → M7에서 9개 신규) 통과,
  `ruff`/`mypy` 클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M7-T04 참고): 실패해도
  결과를 그대로 저장하는 단순화, 누적 압축("요약의 요약") 없음은 사전
  승인된 의도된 단순화. **이번에 새로 드러난 것**:
  `WorkspaceSession.memory_snapshot_id`가 어디서도 자동 갱신되지 않아
  — 검색(`find_snapshots`)은 완전히 동작하지만 새 세션이 이전 세션의
  요약을 자동으로 이어받는 "세션 연속성"은 아직 수동으로만 가능함을
  **M8+ 논의 대상으로 명시적으로 이월**. 그 외 이월 부채(Model/Effort
  라우팅, Adapter 계열 통합, Codex/Gemini CLI 실검증, `run_parallel`
  개별 재시도, `MemoryEngine.search` 성능, `ShellAgent` 화이트리스트
  고정)는 사용자 확정대로 전부 그대로 이월.
- **Milestone 8(세션 연속성) 완료 — 2026-07-26 사용자 승인.** 목표는 M7
  Review가 이월한 갭 — `WorkspaceSession.memory_snapshot_id`가 자동
  갱신되지 않아 PRD 7.4 "자동 이어받기"가 수동으로만 가능하던 것을
  완성. 핵심 설계 결정: §8 규칙 7("Memory 접근은 Agent → Context
  Manager → Memory Engine")에 따라 **Workspace Core는 건드리지 않고
  Agent 계층(PlanningAgent)에서 해결**. `ContextManager.
  latest_snapshot_id(project_id)`(M8-T01, MemoryEngine을 거치지 않고
  Context Manager 내부 dict로만 관리 — search() substring 오염 방지) →
  `DocumentationAgent`가 `create_snapshot()` 반환값을
  `workspace_session.memory_snapshot_id`에 되먹임(M8-T02) →
  `PlanningAgent`가 Mission 시작 시 비어 있으면 자동 복원(M8-T03,
  이미 값 있으면 덮어쓰지 않음). **소스 파일 4개만 수정, 신규 파일
  0개, 새 Interface 0개**(`ContextManager`에 메서드 1개만 추가). 전체
  `pytest` 442개(M7 완료 425개 → M8에서 17개 신규) 통과, `ruff`/`mypy`
  클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M8-T05 참고): 동시성
  경쟁 조건(여러 세션이 동시에 같은 project_id로 Mission 실행 시
  `latest_snapshot_id` 갱신 레이스)과 세션 리셋 옵션 없음을 **M9+ 논의
  대상으로 명시적으로 이월**. 그 외 이월 부채(Model/Effort 라우팅,
  Adapter 계열 통합, Codex/Gemini CLI 실검증, `run_parallel` 개별
  재시도, `MemoryEngine.search` 성능, `ShellAgent` 화이트리스트 고정)는
  그대로 이월.
- **Milestone 9(세션 견고성) 완료 — 2026-07-26 사용자 승인.** M8 Review가
  제시한 3개 후보(Model/Effort 라우팅, 세션 견고성, Adapter 계열 통합)
  중 Interface 변경이 필요 없고 외부 CLI 의존이 없는 **세션 견고성**을
  선택(설계 검토 대화에서 사용자 확정). M9-T01(조사): `InMemoryContext
  Manager._latest_snapshot_by_project`가 락 없는 dict인 것이 실제
  문제인지 조사한 결과 — CLI에 Mission 시작 명령 자체가 없고,
  `InMemoryEventBus.publish()`가 완전 동기이며, 유일한 스레딩
  (`run_parallel`/timeout)이 `ContextManager`를 전혀 건드리지 않아
  **재현 경로가 현재 코드베이스에 존재하지 않음을 확인, 조치 불필요로
  종결**(M2 Event ID 부채와 동일 패턴 — "문제 없음"도 정당한 조사
  결론). M9-T02(락 추가)는 이 결과에 따라 스킵. `PlanningAgent.
  plan_mission(..., reset=True)`(M9-T03)로 세션 리셋 옵션 추가 — M8-T03
  자동 복원을 건너뛴다. 같은 세션에 이미 있는 `memory_snapshot_id`는
  건드리지 않아 범위를 좁게 유지. CLI `--reset` 플래그 노출은 범위
  제외(CLI가 Mission 시작 자체를 아직 노출 안 함, YAGNI). **소스 파일
  1개만 수정**(`agents/planning_agent.py`), 신규 파일 0개, 새 Interface
  0개(M6~M8보다도 좁은 변경 폭). 전체 `pytest` 445개(M8 완료 442개 →
  M9에서 3개 신규) 통과, `ruff`/`mypy` 클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M9-T05 참고): 이월
  부채는 M8과 동일하게 유지(Model/Effort 라우팅, Adapter 계열 통합,
  Codex/Gemini CLI 실검증, `run_parallel` 개별 재시도, `MemoryEngine.
  search` 성능, `ShellAgent` 화이트리스트 고정) — M9는 새 부채를 남기지
  않고 이월 항목 중 하나(세션 리셋)만 해소했다.
- **Milestone 10(실행 복원력) 완료 — 2026-07-26 사용자 승인.** 착수 전
  사용자가 제시한 5개 Technical Debt 후보(Model/Effort 라우팅, Adapter
  통합, Codex/Gemini 실환경 검증, Memory 최적화, run_parallel 복원력)를
  PRD·코드와 재대조한 결과 3개를 제외(Codex/Gemini는 이 세션 환경에
  CLI 바이너리 자체가 없어 실행 불가 — `which codex`/`which gemini`
  둘 다 not found; Adapter 통합은 기능 이득 없는 순수 리팩토링; Memory
  최적화는 PRD §11이 이미 "필요해지면"으로 유보한 항목)하고, 외부 의존
  없이 확인 가능한 **run_parallel 복원력**을 선택. 착수 조사에서
  `ManagedEngineRuntime.run_parallel()`이 `[future.result() for future
  in futures]` 리스트 컴프리헨션 때문에 **Task 1개가 예외를 던지면 이미
  완료된 다른 Task의 결과까지 전부 유실**되는 버그를 새로 확인(M4
  Review가 "개별 재시도 미지원"이라고만 기록했던 것보다 심각한 문제).
  `interfaces/engine_runtime.py`의 `run_parallel()` docstring에 4가지
  보장(반환 길이=입력 길이/순서 보존/개별 예외→`EngineResult(success=
  False)` 변환/개별 실패만으로는 예외 없음, `NoSuitableEngineError`는
  예외)을 명시(M10-T01, 시그니처 불변) → `ManagedEngineRuntime`이
  `future.result()`를 개별 try/except로 캐치해 버그 수정(M10-T02) →
  `RecoveringEngineRuntime.run_parallel()`이 이전엔 `inner`에 단순
  위임했던 것을, 첫 병렬 패스 후 실패한 Task만 기존 `self.run()`의
  재시도 루프로 재실행하도록 변경(M10-T03, 새 재시도 로직 없이 재사용).
  핵심 설계 원칙: "Runtime 자체의 치명적 오류(`NoSuitableEngineError`)"
  는 여전히 즉시 전파하고, "개별 Task 실행 실패"만 격리한다 — 세
  구현체·`docs/ARCHITECTURE.md` §3.9에 일관 반영. **소스 파일 3개만
  수정, 신규 파일 0개, 새 Interface 0개**(시그니처 변경도 없음). 전체
  `pytest` 449개(M9 완료 445개 → M10에서 4개 신규) 통과, `ruff`/`mypy`
  클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` M10-T05 참고): 재분석
  으로 제외한 Codex/Gemini 실환경 검증(환경 의존)·Adapter 통합(ROI
  낮음)·Memory 최적화(증거 없이 하면 YAGNI 위반 위험)는 이유와 함께
  이월. 그 외 이월 부채(Model/Effort 라우팅, Retry Backoff/Persistent
  Runtime Recovery/Approval 비동기 처리/Process Timeout 고도화,
  `ShellAgent` 화이트리스트 고정)는 그대로 유지.
- **Milestone 11(Execution Environment) 완료 — 2026-07-26 사용자 승인.**
  주제는 "Claude Code/API/App, GitHub Codespaces, Replit, Codex/Gemini
  CLI, Copilot 등을 어디에 배치할지"였다. 설계 검토 결과 두 축이 뒤섞여
  있었음을 확인: **엔진**(무엇으로 작업을 시킬지 — Claude Code/Codex
  CLI/Gemini CLI/Copilot, 이미 `EngineAdapter`가 담당)과 **실행
  환경**(어디서 실행되는지 — 로컬/Codespaces/Replit/Docker, 담당 계층
  없었음)이 그것이다. Task→Agent→Engine Runtime→Engine Adapter라는
  기존 최상위 흐름에 새 Layer를 추가하지 않고, `ExecutionEnvironment`
  를 **`EngineAdapter` 하위(내부) 인터페이스**로 두기로 사용자가 최종
  승인(ADR-0025) — Agent/Engine Runtime은 실행 환경을 알 필요가 없고,
  `EngineAdapter`가 이미 세션 생명주기 계약(ADR-0015)을 갖고 있어 그
  경계 안이 자연스럽다는 것이 근거. `interfaces/execution_environment.py`
  에 `ExecutionEnvironment`(execute/cancel, M1 이후 두 번째 신규 최상위
  Interface, 총 18종, M11-T01) → `adapters/local_execution_environment.py`
  의 `LocalExecutionEnvironment`가 새 프로세스 로직 없이 기존
  `ProcessRunner`(M3-T03)를 그대로 감싸 구현(M11-T02) →
  `ClaudeCodeEngineAdapter`/`CLIEngineAdapter`가 `ProcessRunner`를 직접
  생성하던 것을 생성자 **주입(DI)**으로 전환(기본값
  `LocalExecutionEnvironment()`, M11-T03) — 새 실행 환경(예: 향후
  Codespaces)을 추가해도 `EngineAdapter` 코드를 전혀 수정하지 않고
  확장 가능함을 전용 테스트로 직접 증명(OCP). Codespaces/Replit/Docker
  실행 환경은 실제 요구사항이 생길 때까지 구현하지 않는다(YAGNI,
  `LocalExecutionEnvironment`만 존재). **신규 소스 파일 2개, 수정 5개**
  (`ClaudeCodeEngineAdapter`/`CLIEngineAdapter`/`CLIProvider`/
  `CodexProvider`/`GeminiCliProvider` — Provider들의 `parse_result()`
  시그니처도 `ExecutionResult` 기준으로 함께 갱신). Claude API/App은
  프로그램적으로 제어할 API가 없거나(App) 로컬 프로세스가 필요 없어
  (API) 이 구조에 아예 들어오지 않는다는 점도 함께 정리됨. 전체
  `pytest` 460개(M10 완료 449개 → M11에서 11개 신규) 통과, `ruff`/
  `mypy` 클린.
  **Milestone Review 결론**(전문은 `.ai/TASKS.md` "Milestone 11
  Review" 참고): M5 이후 두 번째로 새 최상위 Interface 1개를 추가했지만
  기존 보호 자산(`EngineAdapter`/`EngineRuntime` 등)의 계약은 전혀
  바뀌지 않음. 이월 부채는 M10과 동일하게 유지(Model/Effort 라우팅,
  Adapter 계열 통합, Codex/Gemini CLI 실검증, `MemoryEngine.search`
  성능, Retry Backoff 등, `ShellAgent` 화이트리스트 고정) — M11은 새
  부채를 남기지 않았다.
- **Milestone 12(Workflow Automation) 완료 — 2026-07-26 사용자 승인.**
  목표는 "Workflow가 사람 개입 없이 순차적으로 Task를 실행하는
  MVP"(Multi-Agent/Routing/병렬/Retry/Approval 범위 밖, 사용자 확정).
  **핵심 발견**: `WorkspaceCore.start_workflow()`가 `WorkflowEngine.
  plan()`으로 순서를 계산해왔지만, 그 순서를 실제로 실행하는 코드는
  M1부터 지금까지 어디에도 없었다 — `plan()`은 순수 함수, Task 실행은
  `PlanningAgent.plan_mission()`(Task 1개 생성+즉시 시작)뿐이었다.
  `WorkflowEngine`(Core Engine)이나 새 Agent가 아니라, 기존 3개
  Interface(`WorkflowEngine`/`EventBus`/`TaskEngine`)만 조합하는 독립
  조율자 `runtime/workflow/workflow_runner.py`의 `WorkflowRunner`를
  신설(M12-T01, `EngineApprovalPipeline`과 동일한 "조합형 조율자"
  패턴). `EventBus.publish()`가 계약상 예외를 던지지 않는다는 사실을
  재확인해(구독자 예외는 Bus 내부에서 격리), 계획했던 try/except
  기반 실패 감지 대신 `TaskStatus.DONE` 여부만으로 단순화(불필요한
  코드를 만들기 전에 걷어낸 사례). 실제 5-Agent 파이프라인(Coding→
  Shell→Coordinator→Review→Documentation) 위에서 Task 2개짜리
  Workflow가 사람 개입 없이 완주하는 시나리오와, 중간 Task가 재작업
  소진으로 실패해 이후 Task가 아예 실행되지 않는(TODO 상태 그대로)
  중단 시나리오를 통합 테스트로 증명(M12-T02). **신규 소스 파일 1개,
  기존 파일 수정 0개, 새 Interface 0개**(M9 이후 가장 작은 변경 폭).
  전체 `pytest` 465개(M11 완료 460개 → M12에서 5개 신규) 통과,
  `ruff`/`mypy` 클린. 새 Interface가 없어 신규 ADR은 작성하지 않음.
  이월 부채는 M11과 동일하게 유지.
- **Milestone 13(Multi-Agent Collaboration) 완료 — 2026-07-26 사용자
  승인.** 목표는 "같은 Capability의 Agent가 여러 개 등록돼 있을
  때 `AgentScheduler.select()`가 실제로 하나만 고르고 나머지는 개입
  하지 않는다"는 것을 실제로 증명(MVP, 사용자 확정). **핵심 발견**:
  `AgentScheduler`는 M1부터 정의만 되어 있었고 실제 협업 흐름에서
  한 번도 쓰인 적이 없었다 — 각 Agent가 Event를 구독하면 무조건
  처리하는 고정 배선 구조였기 때문. 새 중앙 디스패처를 만들지 않고,
  `agents/scheduling.py`에 `is_agent_selected()`를 추가해 각 Agent가
  처리 직전 스스로 "내가 선택됐나"를 확인하는 **자가 확인 가드**
  패턴을 채택(`AgentScheduler.select()`가 결정적이라는 성질을 이용 —
  같은 후보로 같은 질문을 하면 모든 인스턴스가 같은 결론에 도달).
  `CodingAgent`에 `agent_registry`/`agent_scheduler`를 **선택적**
  (기본값 `None`) 매개변수로 추가해 기존 호출부(수십 곳)를 전혀
  건드리지 않음. 실제 `InMemoryAgentManager`/`InMemoryAgentRegistry`/
  `InMemoryAgentScheduler`(Fake 아님)로 같은 CODING Capability의
  `CodingAgent` 2개를 등록해도 `MissionPlanned` 하나에 `CodeCompleted`
  가 정확히 1번만 발행됨을 통합 테스트로 증명(M13-T03). **신규 소스
  파일 0개, 기존 파일 수정 2개, 새 Interface 0개** — M1 이후 가장
  작은 변경 폭 중 하나. 전체 `pytest` 472개(M12 완료 465개 → M13에서
  7개 신규) 통과, `ruff`/`mypy` 클린. 새 Interface가 없어 신규 ADR은
  작성하지 않음. MVP는 `CodingAgent` 하나에만 적용(Review/Documentation
  등으로 확장은 후속 Milestone, YAGNI). 이월 부채는 M12와 동일하게
  유지.
- **Milestone 14(LLM Routing, Model 수준 라우팅) 완료 — 2026-07-26
  사용자 승인.** 목표는 "Policy가 정한 Model(opus/sonnet/haiku
  등)이 실제 실행까지 전달되게 한다"는 것(MVP, 사용자 확정). **핵심
  발견**: M6이 완성한 것은 **Provider 단위** 라우팅(어떤 CLI를 쓸지)
  뿐이었고, `LLMPolicyDecision`의 `model`/`effort`는 `EngineAdapter.
  run()`/`EngineRuntime.run()` 어디에도 전달할 자리가 없어 한 번도
  실제 실행에 반영된 적이 없었다(M6 Review 최초 이월, M10에서
  "Interface 변경이 필요한 무거운 작업"으로 재확인·재이월). **범위를
  Model만으로 좁힘**(Effort는 Claude Code CLI에 대응 플래그가 없어
  검증 불가능해 제외) — `EngineAdapter`/`EngineRuntime`(둘 다 RULES
  §1.2 보호 자산 또는 그 인접 계약) `run()`에 `model: str | None =
  None`(키워드 전용, 신규 **ADR-0026**)을 추가했다. 새 선택 로직 없이
  `ManagedEngineRuntime`/`RecoveringEngineRuntime`/
  `InMemoryEngineRuntime`은 전달만 하고, **`ClaudeCodeEngineAdapter`
  만** 실제로 `--model` 실행 인자에 반영(Codex/Gemini는 이 환경에
  CLI가 없어 검증 불가, 계약만 만족). `domain/llm_policy.py`에
  `model_name()` 신규(기존 `required_capabilities()`와 동일 패턴) —
  `CodingAgent`/`ReviewAgent`/`DocumentationAgent` 3개 Agent가 함께
  전달하도록 연결. 실제 `docs/llm_policy.example.yaml`(coding→
  anthropic/opus) 기반 6-Agent 파이프라인에서 `ClaudeCodeEngineAdapter`
  가 조립한 실제 명령에 `--model opus`가 포함됨을 통합 테스트로 증명
  (M14-T03). 새 소스 파일 0개, 기존 파일 수정 11개(Interface 2·
  Adapter 4·Runtime 3·Agent 3·domain 1, 일부 중복 집계) — M11(신규 2)
  보다 넓지만 M5(신규 6)보다는 좁은 폭. 전체 `pytest` 489개(M13 완료
  472개 → M14에서 17개 신규) 통과, `ruff`/`mypy` 클린. **새 최상위
  Interface는 0개이나 기존 `EngineAdapter`/`EngineRuntime` 계약을
  확장(ADR-0009/0015와 동일 계열)** — ADR-0026으로 정식 기록. 이월
  부채는 M13과 동일하게 유지(Effort 라우팅 신규 이월, Codex/Gemini
  실연동 계속 이월).
- **Milestone 15(Token & Cost Optimization) 완료 — 2026-07-27
  사용자 승인.** 목표는 "`EngineAdapter.estimate_cost()`를 실제로
  활용하는 Workspace 차원 Budget 정책을 도입해 Task 실행 전에 예산을
  확인하고 초과 시 막는다"(MVP, Provider 독립). **핵심 발견**:
  `estimate_cost()`는 M3부터 있었지만 `EngineRuntime`도 Agent도 호출한
  적이 없었다(M12의 `WorkflowEngine.plan()`, M13의 `AgentScheduler.
  select()`와 동일한 "만들어졌지만 쓰인 적 없는 기능" 패턴). `domain/
  budget.py`에 `Budget`/`BudgetDecision`(Provider 독립) 신규,
  `interfaces/budget_policy_engine.py`에 `BudgetPolicyEngine`
  Interface 신규(`LLMPolicyEngine`과 동일 설계 원칙 — side-effect
  없음, 정책 없으면 항상 허용), `InMemoryBudgetPolicyEngine` 최소
  구현. `EngineRuntime`(RULES §1.2 보호 자산)에 `estimate_cost(task,
  required_capabilities) -> CostEstimate`를 신규 추가(세션 미생성,
  `run()`과 동일한 선택 규칙, 신규 **ADR-0027**) — `InMemoryEngineRuntime`
  /`ManagedEngineRuntime`은 기존 선택 로직 재사용, `RecoveringEngineRuntime`
  은 순수 위임. `CodingAgent`에 선택적 `budget_policy_engine` DI 추가 —
  실행 직전 `estimate_cost()` → `check()`를 거쳐 예산 초과 시 Approval/
  Retry 없이 Task를 `BLOCKED`로 전환하고 실행하지 않는다. 실제
  `ManagedEngineRuntime`+`ClaudeCodeEngineAdapter`+`CodingAgent` 조합
  으로 예산 내/초과/미설정 3가지 시나리오를 통합 테스트로 증명
  (M15-T03). 새 소스 파일 3개(`domain/budget.py`, `interfaces/
  budget_policy_engine.py`, `engines/budget_policy_engine.py`), 기존
  파일 수정 5개(`EngineRuntime` Interface 1·구현체 3·`CodingAgent` 1).
  전체 `pytest` 511개(M14 완료 489개 → M15에서 22개 신규) 통과,
  `ruff`/`mypy` 클린. **새 최상위 Interface 1개(`BudgetPolicyEngine`)
  추가 + 기존 `EngineRuntime` 계약 확장** — 새 Interface 추가(M5/M11과
  동일 계열)와 기존 계약 확장(M14와 동일 계열)이 겹친 첫 Milestone.
  이월 부채는 M14와 동일하게 유지(여러 Task에 걸친 누적 예산 추적,
  예산 초과 시 Approval 흐름, 실제 API 과금 조회는 신규 이월 후보로
  기록했으나 전부 "사용자가 이번 범위에서 의도적으로 제외"한 항목이라
  기존 5개 부채 목록에는 추가하지 않음).
- **Milestone 16(Project Knowledge System) 완료 — 2026-07-27
  사용자 승인.** 목표는 "프로젝트 기존 문서(ARCHITECTURE/DECISIONS/
  RULES/TASKS/ROADMAP/PRD)를 Workspace 전용 Knowledge로 노출하고
  Agent가 Keyword 검색으로 참고하게 한다"(MVP, Provider/Engine
  독립). **핵심 설계 결정**: `interfaces/memory_engine.py`의
  `MemoryEngine`(M1부터 존재, `ContextManager`가 감싸 Mission 요약/
  세션 연속성에 사용)은 완전히 다른 개념이라 손대지 않고, 새 이름의
  컴포넌트 계열(`KnowledgeRepository`/`KnowledgeSearch`/
  `KnowledgeProvider`)을 신설(신규 **ADR-0028**). `domain/knowledge.py`
  에 `KnowledgeDocument`/`KnowledgeKind`(ARCHITECTURE/ADR/RULE/TASK/
  PROJECT 5종, Provider 독립), `storage/file_knowledge_repository.py`
  의 `FileKnowledgeRepository`가 고정 파일→kind 매핑으로 파일 하나를
  문서 하나로 노출(문단 파싱 없음, YAGNI). `engines/knowledge_search.py`
  의 `InMemoryKnowledgeSearch`(Keyword 포함 검색, `KnowledgeIndexer`는
  문서 수가 적어 이번 범위에서 제외), `engines/knowledge_provider.py`
  의 `InMemoryKnowledgeProvider`(Agent의 유일한 진입점, `ContextManager`
  가 `MemoryEngine`을 감싸는 것과 동일한 패턴). `domain/
  development_context.py`에 `related_knowledge` 필드 추가.
  `CodingAgent`에 선택적 `knowledge_provider` DI 추가 — 실제
  `docs/ARCHITECTURE.md`에 등장하는 키워드로 검색한 결과가 실행
  프롬프트에 그대로 반영됨을 실제 `FileKnowledgeRepository`(프로젝트
  루트) 기반 통합 테스트로 증명(M16-T03). 새 소스 파일 7개(domain 1·
  interfaces 3·storage 1·engines 2), 기존 파일 수정 2개
  (`development_context.py`/`coding_agent.py`) — M5(신규 6)보다 넓은,
  지금까지 중 가장 넓은 신규 파일 폭. 전체 `pytest` 532개(M15 완료
  511개 → M16에서 21개 신규) 통과, `ruff`/`mypy` 클린. **새 최상위
  Interface 3개**(`KnowledgeRepository`/`KnowledgeSearch`/
  `KnowledgeProvider`) 추가 — M1 이후 가장 큰 Interface 확장,
  ADR-0017/0025와 동일한 "신규 계층 도입" 계열로 ADR-0028 기록.
  이월 부채는 M15와 동일하게 유지(신규 이월 없음 — Review/
  Documentation Agent로의 확장, `KnowledgeIndexer`, Semantic
  Search는 전부 "사용자가 이번 범위에서 의도적으로 제외"한 항목).
- **Milestone 17(Intelligent Engine Selection) 완료 — 2026-07-27
  사용자 승인.** 목표는 "Task+Budget(M15)+Knowledge(M16)+등록된
  Engine 후보를 종합해 최적 Engine을 결정만 한다"(Decision Only,
  실행 연결은 M18). **핵심 발견**: `EngineRuntime`은 `required_
  capabilities`를 만족하는 등록된 Engine 중 첫 매칭만 고를 뿐, 여러
  후보를 나열·비교하는 방법이 없었다. **사용자 승인 조건**: (1)
  Decision Only 유지, (2) `EngineSelectionDecision`에 `reason` 포함,
  (3) 가능하면 `EngineRuntime.list_candidates()` 대신 기존 Registry/
  Manager 계층 활용 — 조사 결과 `AgentRegistry`에 대응하는 기존
  Engine Registry가 없어 `AgentManager`/`AgentRegistry` 분리와 동일한
  패턴으로 신규 `EngineRegistry`를 도입(신규 **ADR-0029**,
  `EngineRuntime`의 실행 계약은 전혀 확장하지 않음). `domain/
  engine_selection.py`에 `EngineCandidate`/`EngineSelectionDecision`
  (Provider 독립), `interfaces/engine_registry.py`의
  `EngineRegistry`(`register`/`get`/`list_candidates`, 세션 미생성),
  `interfaces/engine_selection_policy.py`의 `EngineSelectionPolicy`
  (후보가 어디서 왔는지 모름 — 조회/판단 책임 분리). `engines/
  engine_selection_policy.py`의 `InMemoryEngineSelectionPolicy`가
  `BudgetPolicyEngine.check()`를 재사용(M15, 예산 비교 로직 중복
  없음)해 예산 내 최저 비용 후보를 선택, Knowledge는 `reason`에만
  참고 반영. **결정과 실행의 분리**를 실제 `CodingAgent` 파이프라인
  실행 결과 + `inspect.signature()` 이중 증명(다른 Engine을 추천해도
  실제 실행은 영향받지 않음, `CodingAgent` 생성자에 관련 파라미터
  자체가 없음). 신규 소스 파일 5개, **기존 소스 파일 수정 0개**(M1
  이후 유일하게 기존 파일을 전혀 건드리지 않은 Milestone). 전체
  `pytest` 553개(M16 완료 532개 → M17에서 21개 신규) 통과, `ruff`/
  `mypy` 클린. **새 최상위 Interface 2개**(`EngineRegistry`/
  `EngineSelectionPolicy`) 추가, 기존 Interface는 하나도 확장하지
  않음(M14/M15/M16과 다른 패턴) — ADR-0017/0025/0028과 동일한 "신규
  계층 도입" 계열로 ADR-0029 기록. 이월 부채는 M16과 동일하게 유지
  (신규 이월: 실행 연결은 M18 예정으로 명시적으로 분리, Model 수준
  결정/ML 기반 고급 판단은 "사용자가 이번 범위에서 의도적으로 제외"
  한 항목이라 기존 부채 목록에는 추가하지 않음).
- **Milestone 18(Multi-Engine Execution Integration) 완료 —
  2026-07-27 사용자 승인.** 목표는 "M17의 `EngineSelectionDecision`
  을 실제 실행으로 연결하는 `ExecutionDispatcher`를 도입해, 선택된
  Engine을 인증 상태 확인 후 실행한다"(MVP). **핵심 발견**: 요청받은
  새 "ExecutionResult" Domain(success/output/error/engine/
  execution_time)이 M11 `interfaces/execution_environment.py`의
  기존 `ExecutionResult`(returncode/stdout/stderr, 프로세스 결과)와
  이름이 겹쳐 **`EngineExecutionResult`**로 명명(사용자 승인, M16
  `MemoryEngine` 충돌 발견과 같은 종류의 사전 점검). **사용자 승인
  조건**: (1) `EngineExecutionResult` 명명, (2) `ExecutionDispatcher`
  는 Interface가 아닌 구체 클래스(M12 `WorkflowRunner`와 동일
  패턴), (3) 인증 실패=`AuthenticationRequiredError` 예외/Decision
  부재=`EngineExecutionResult(success=False)`로 구분, (4)
  `CodingAgent`는 수정하지 않고 `ExecutionDispatcher`를 독립적으로
  구현·검증. `domain/execution_result.py`에 `EngineExecutionResult`
  (Provider 독립), `interfaces/authentication_manager.py`의
  `AuthenticationManager`(`is_authenticated`/`authentication_status`
  만 — `login`/`logout` 없음, "로그인 수행"이 아니라 "상태 확인"만
  담당, 신규 **ADR-0030**)/`AuthenticationRequiredError`,
  `engines/authentication_manager.py`의
  `InMemoryAuthenticationManager`(실제 로그인/OAuth/Credential
  없음). `runtime/execution/execution_dispatcher.py`의
  `ExecutionDispatcher`가 `dispatch(decision, task)`로 `decision`이
  `None`이면 Registry/Auth 어느 쪽도 호출하지 않고 즉시 실패 결과를,
  미인증이면 예외를, 인증되면 `EngineRegistry.get()`으로 정확히
  하나의 Adapter만 실행한다. 실제 `ClaudeCodeEngineAdapter`+
  `ExecutionEnvironment`로 실행됨(명령이 실제로 기록됨)과
  `EngineSelectionPolicy` 소스 코드에 `ExecutionDispatcher` 참조가
  없음을 모두 통합 테스트로 증명(M18-T03) — Task→Selection Policy→
  Decision→Dispatcher→Authentication→Registry→Adapter→
  ExecutionEnvironment→`EngineExecutionResult`로 이어지는 **첫
  End-to-End 실행 경로 완성**(M11/M15/M16/M17이 실행까지 연결됨).
  신규 소스 파일 4개, **기존 소스 파일 수정 0개**(M17에 이어 두
  번째로 기존 파일 무수정). 전체 `pytest` 567개(M17 완료 553개 →
  M18에서 14개 신규) 통과, `ruff`/`mypy` 클린. **새 최상위 Interface
  1개**(`AuthenticationManager`) 추가(`ExecutionDispatcher`는 구체
  클래스라 ADR 대상 아님) — ADR-0017/0025/0028/0029와 동일한 "신규
  계층 도입" 계열로 ADR-0030 기록. 이월 부채는 M17과 동일하게 유지
  (신규 이월: 실제 로그인/OAuth/Credential/Token Refresh, `CodingAgent`
  연결은 사용자가 명시적으로 후속 Milestone으로 분리).
- **Milestone 19(Reliability Layer) 완료 — 2026-07-27 사용자 승인.**
  목표는 "M18 Execution Layer의 안정성 확보 — 정책 기반 Retry,
  Timeout, 안전한 Cancellation"(MVP). **핵심 발견 3가지**: (1)
  `domain/retry_policy.py`의 `RetryPolicy`(M3)가 이미 있고
  `RecoveringEngineRuntime`이 "무조건 재시도"에 쓰고 있어 — M16/M18과
  달리 이번엔 같은 개념의 확장이라 새 이름 대신 기존 클래스에 필드
  추가(`retry_delay_seconds`/`non_retryable_exceptions`, 기본값 있어
  `RecoveringEngineRuntime` 무영향) + `decide() -> RetryDecision`.
  (2) `ClaudeCodeEngineAdapter.run()`이 Timeout과 다른 실행 오류를
  같은 예외 타입(`EngineExecutionError`)으로 던져 "EngineAdapter
  인터페이스 변경 금지" 제약과 충돌 — `timed_out`은 메시지 텍스트
  휴리스틱으로만 판정 가능(**신규 기술 부채, ADR-0031에 명시**). (3)
  DoD의 `NoSuitableEngineError`(`EngineRuntime` 시절)는 이 경로에
  실제로 나타나지 않음 — M18이 `EngineRegistry`를 직접 써서 실제로는
  `EngineNotRegisteredError` 발생. `runtime/execution/
  retry_executor.py`의 `RetryExecutor`(제네릭, `EngineExecutionResult`
  를 모름)가 "인증 확인→Registry 조회→Adapter 실행" 전체를 한 시도로
  묶어 재시도(`ExecutionDispatcher`는 재시도를 직접 구현하지 않음).
  `AuthenticationRequiredError`/`EngineNotRegisteredError`/
  `NoSuitableEngineError`는 기본적으로 재시도 안 함. 취소는
  `EngineAdapter`가 이미 쓰는 sentinel(`error == "cancelled"`, 사용자
  승인 조건)을 그대로 재사용해 즉시 반영, 재시도 루프 자체를 타지
  않음. `EngineExecutionResult`에 `retry_count`/`cancelled`/
  `timed_out` 확장(기본값 있어 M18 호출부 무영향). 실제
  `ClaudeCodeEngineAdapter`+`ExecutionEnvironment`로 Timeout 재시도·
  소진 후 반영, Cancellation 즉시 반영을 통합 테스트로 증명(M19-T03).
  신규 소스 파일 1개, 기존 파일 수정 3개(M17/M18에 이어 세 번째로
  작은 변경 폭). 전체 `pytest` 588개(M18 완료 567개 → M19에서 21개
  신규) 통과, `ruff`/`mypy` 클린. **새 최상위 Interface는 0개**이나
  사용자가 명시적으로 요구해 ADR-0031 작성(RetryPolicy 확장 근거 +
  timed_out 휴리스틱 기술 부채 정식 기록). 이월 부채는 M18과 동일,
  신규 이월 1건(timed_out 휴리스틱).
- **Milestone 20(Real-time Dashboard Platform) 완료 — 2026-07-27
  사용자 승인.** 목표는 "AI Workspace 운영 상태를 실시간으로
  관찰하는 Dashboard(CQRS Read Model, Task 미실행)"(MVP). 이
  프로젝트가 **처음으로 "서버"·외부 런타임 의존성·Web UI를
  도입**했다(기존엔 `pyyaml` 하나뿐이던 런타임 의존성에
  `fastapi`/`uvicorn` 추가). 사용자가 3단계로 승인한 설계: (1)
  `workspace start` 서버 런타임 도입, 기존 CLI 명령은 무영향. (2)
  `ExecutionDispatcher`에 `event_bus: EventBus | None = None` 선택적
  DI — Event만 발행하고 `DashboardRepository`를 직접 참조하지
  않음(M13부터 이어진 "선택적 DI로 기존 컴포넌트 무변경 확장"
  패턴), `InMemoryDashboardRepository`가 스스로 구독해 Read Model을
  갱신, API/WebSocket/Web UI는 `DashboardService`만 사용. (3) Task
  구조 T01~T07을 사용자가 직접 확정, "Core 계층은 웹 프레임워크를
  모르도록 유지하고 FastAPI는 Infrastructure 계층(`web/`)에서만
  사용" 원칙 명시. `domain/dashboard.py`(`EngineStatus`/
  `WorkspaceStatus`/`ExecutionRecord`/`ExecutionStats`/
  `ReliabilityStats`, `EngineExecutionResult`를 그대로 참조하지 않고
  필요 필드만 옮겨 담음), `interfaces/dashboard_repository.py`의
  `DashboardRepository`(**신규 최상위 Interface, 26번째** — 쓰기
  3개/읽기 5개 메서드를 한 Interface에 함께 정의, 구현체가 하나뿐이라
  물리적 분리는 과설계로 판단), `InMemoryDashboardRepository`(통계는
  조회 시점 계산 없이 매 Event마다 미리 갱신 — "Dashboard는 통계를
  계산하지 않는다"), `DashboardService`(`web/`을 전혀 import하지
  않음을 `ast` 기반 검증으로 증명), `web/`(신규 최상위 패키지 —
  `DashboardViewModel`/`DashboardBroadcaster`(WebSocket 연결 시점에
  캡처한 `asyncio.get_running_loop()`+`loop.call_soon_threadsafe()`로
  동기 `EventBus.publish()`→비동기 WebSocket 전송 경계를 넘김)/
  `routes.py`(REST 4종)/`app.py`/`server.py`/`static/`(정적
  HTML/CSS/Vanilla JS, 빌드 도구 없음, 현재 시각·경과 시간은
  브라우저가 1초마다 직접 계산·Polling 없음)). `cli/main.py`에
  `start` 서브커맨드(지연 import로 다른 CLI 명령은 FastAPI 몰라도
  됨). 실제 `ClaudeCodeEngineAdapter` 실행 결과가 Event→Repository→
  Service→REST API/WebSocket까지 그대로 반영됨을 통합 테스트로
  증명(M20-T06), FastAPI `response_model`이 stdlib `@dataclass`를
  문제없이 직렬화함도 실증(사전 불확실했던 리스크 해소). 신규 소스/
  정적 파일 13개, 기존 파일 수정 4개(전부 선택적 DI/신규 서브커맨드로
  하위 호환 유지). 전체 `pytest` 635개(M19 완료 588개 → M20에서
  47개 신규) 통과, `ruff`/`mypy` 클린(`mypy`는 이 환경에서
  `--python-executable "$(which python3)"` 필요 — 환경 설치 방식
  때문, 코드 문제 아님). **새 최상위 Interface 1개**
  (`DashboardRepository`) 추가로 ADR-0032 기록. 새로 발생한 기술
  부채 없음. 이월 부채는 M19와 동일하게 유지, 신규 이월 없음.
- **Milestone 21(Automation Engine) 완료 — 2026-07-27 사용자 승인.**
  목표는 "조건/일정에 따라 Task를 자동 실행하는 Automation(Dashboard와
  독립적인 Domain, `ExecutionDispatcher`를 통해서만 Task 실행)"
  (MVP). **핵심 발견**: M4-T07에 이미 `AutomationEngine`
  (trigger_id↔Workflow 연결 관리만 담당, "언제 발동할지"·"실제
  실행"은 원래부터 호출자 책임으로 명시적으로 떠넘겨져 있었음)이
  존재 — M21이 요청한 `AutomationRule`(4종 Trigger+Action)/
  `AutomationScheduler`(실제 일정 평가+자동 실행)는 그 떠넘겨진
  책임을 처음 구현하는 것이라 M16 `KnowledgeRepository`/M18
  `EngineExecutionResult`와 같은 "이름은 유사하지만 다른 개념"
  패턴으로 판단해 완전히 새 컴포넌트 세트를 도입(기존
  `AutomationEngine`은 무수정 유지). 사용자 최종 승인 조건 6개:
  (1) `AutomationScheduler`와 Trigger 책임 분리, (2) Dashboard는
  계속 Read Model 유지, (3) Automation CRUD는 API를 통해서만, (4)
  Dashboard는 Automation 미제어, (5) `ExecutionDispatcher` 유일한
  실행 진입점 유지, (6) `last_executed_at`/`next_execution_at`을
  도메인에 내장해 M23 Mobile과 연계. `domain/automation.py`
  (`TriggerKind`/`Trigger`/`ActionKind`/`Action` — kind로 태그된
  Flat 구조, `AutomationRule`은 `Task`처럼 가변 엔티티),
  `interfaces/automation_repository.py`의 `AutomationRepository`
  (**신규 최상위 Interface, 27번째**), `runtime/automation/`
  (`InMemoryAutomationRepository`/`AutomationService`(CRUD 유일
  진입점)/`TriggerEvaluator` 계층(Time/Interval/Startup/Event 4종,
  "언제 발동할지" 판단 전담)/`AutomationScheduler`(Rule을 별도
  보관하지 않고 매 호출마다 Repository 재조회 — CRUD가 API를
  거치기만 하면 자동 반영)/`AutomationActionExecutor`(RUN_TASK를
  M17/M18 파이프라인 `EngineSelectionPolicy.select()`→
  `ExecutionDispatcher.dispatch()`로 그대로 실행, RUN_WORKFLOW는
  `AutomationActionNotSupportedError`로 이번 범위 밖 명시)).
  Dashboard 연계는 **Reader→Reader** 패턴으로 확장 —
  `DashboardService`가 선택적 `automation_service` DI로
  `AutomationService.list_rules()`(읽기 전용)만 호출해
  `AutomationStatus` 집계(CQRS "쓰기측이 읽기측을 모른다" 방향성만
  유지). `web/automation_routes.py` REST API 8종, `web/app.py`를
  `lifespan` Context Manager로 전환해 서버 기동 시 Startup Trigger
  평가+주기적 `tick()` 백그라운드 Task 실행. 실제
  `ClaudeCodeEngineAdapter` 조합으로 Event Trigger→실제 Task
  실행까지 이어짐과 REST API로 만든 Rule이 Dashboard에 반영됨을
  통합 테스트로 증명(M21-T07). **실제 브라우저 검증**(Playwright,
  세션 한정 설치)에서 Web UI 다중 필드 표시 버그(`querySelector`
  단일 요소 한계)를 발견해 `querySelectorAll`로 즉시 수정 — pytest
  로는 잡히지 않는 정적 JS 결함을 실제 조작으로 잡은 사례. 신규
  소스/정적 파일 11개, 기존 파일 수정 5개(전부 선택적 DI/기본값
  유지로 하위 호환). 전체 `pytest` 720개(M20 완료 635개 → M21에서
  85개 신규) 통과, `ruff`/`mypy` 클린. **새 최상위 Interface 1개**
  (`AutomationRepository`) 추가로 ADR-0033 기록. 신규 기술 부채
  2건: RUN_WORKFLOW 미지원(`ExecutionDispatcher` 유일 진입점 원칙과
  정합성 있는 설계를 후속 Milestone으로 이월), Dashboard 서버의
  `InMemoryEngineRegistry`에 실제 `EngineAdapter`가 등록돼 있지
  않음(Workspace Core/CLI 경로와의 실제 통합은 Out of Scope로 이월).
- **Milestone 22(Production Platform) 완료 — 2026-07-27 사용자
  승인.** 목표는 "AI Workspace를 실제 운영 가능한 Production
  Platform으로 확장 — 비즈니스 로직 추가 없음, Server Runtime의
  Lifecycle/Configuration/Health/Logging만 담당"(MVP). 사용자 최종
  승인 조건 5개: (1) Configuration은 Infrastructure Layer의
  Immutable 설정 객체, (2) `LifecycleManager`는 생성이 아닌
  생명주기(Startup/Shutdown)만 관리, (3) `HealthMonitor`는 조회
  전용(Read Model), (4) Dashboard Health는 기존 `DashboardService`
  를 확장, (5) `uptime`/`started_at`/`version`/`health_status`를
  표준 상태 정보로 제공해 M23 재사용 대비. Kickoff 논의에서 추가
  확정: Version API는 `pyproject.toml`의 아키텍처 기준선 버전
  (ADR-0024)과 별개의 `WORKSPACE_VERSION` 상수로 관리, Health
  Monitor의 "Engine" 항목은 `EngineRegistry` Interface를 확장하지
  않고 구조적 연결 여부만 확인, Graceful Shutdown은 별도 계측 없이
  기존 `DashboardService.workspace_status()`(M20)를 폴링해 구현.
  `runtime/production/`(신규 패키지)에 `ProductionConfig`(frozen
  dataclass)+`load_production_config()`(기본값→YAML 파일→
  `AI_WORKSPACE_` Env Var 순으로 겹쳐 씀, `storage/
  llm_policy_loader.py`와 동일한 로더 분리 패턴)/`configure_logging()`
  (표준 `logging`, Console+File)/`LifecycleManager`(STARTUP/
  RUNNING/SHUTDOWN, Graceful Shutdown은 실행 중 Task 완료를
  기다리되 타임아웃 후 강제 개입 없음)/`HealthMonitor`(Server/
  Dashboard/Automation/EventBus/Engine 5개 컴포넌트를 가장 나쁜
  상태로 집계)/`WORKSPACE_VERSION`+`get_git_commit_hash()`. Dashboard
  Health는 **기존 `DashboardService`를 확장**(선택적
  `health_monitor` DI + `production_status()`, M21
  `automation_service`와 동일한 Reader→Reader 패턴)해 구현했는데,
  이 과정에서 `DashboardService`↔`HealthMonitor`(및
  `LifecycleManager`)가 서로를 참조하고 싶어 하는 이 프로젝트 첫
  순환 참조 상황이 발생 — `TYPE_CHECKING` 가드로 타입 힌트만
  지연 import해 런타임 순환을 없애고, `DashboardService.
  attach_health_monitor()`(생성 후 연결)로 조립 순서 문제를 풀었다
  (실제 순환 의존은 아님을 ADR-0034에 명시). `web/production_routes.py`
  에 `GET /api/health`(컴포넌트별 상세)/`GET /api/config`/
  `GET /api/version`/`GET /api/status`(4개 표준 필드만 담은 경량
  요약, M23 재사용 대비) 4종 추가. `web/app.py`가 `production_config`
  /`lifecycle_manager`/`health_monitor` 3개 모두 주입해야만
  Production 라우터를 등록(기존 M20/M21 호출부 무영향), `lifespan`
  이 `LifecycleManager`에 위임해 Graceful Shutdown을 tick Task
  취소보다 먼저 수행. `web/server.py`가 Configuration을 로드해
  전체 스택을 조립, CLI `--host`/`--port` 기본값을 `None`으로
  바꿔 미지정 시 Configuration이 살아있게 함. 실제 `uvicorn.run()`
  서버에 `curl`로 Lifecycle 전이·CLI 오버라이드를 확인, 실제
  Chromium(Playwright)으로 "Production 현황" 화면 렌더링을 확인.
  신규 소스 파일 7개, 기존 파일 수정 6개(전부 선택적 DI/기본값
  유지). 전체 `pytest` 771개(M21 완료 720개 → M22에서 51개 신규)
  통과, `ruff`/`mypy` 클린. **새 최상위 Interface 0개**(전부 구체
  클래스/dataclass, M19에 이어 두 번째 "새 Interface 없이도 ADR
  작성" 사례)로 ADR-0034 기록. 새로 발생한 기술 부채 없음(순환
  참조는 우회가 아니라 `TYPE_CHECKING`으로 근본 해결).
- **M23-Preparation(Obsidian Knowledge Base 구축) 전체 완료
  (2026-07-27, T01~T07 + T01A~T01D).** T01~T07(저장소 루트
  `Vault/`에 PARA 구조로 GitHub 요약+링크 Index를 구축 — Overview/
  Architecture/ADR/Backend/API/Dashboard/Automation/Production/
  iOS·Android/Milestones/Decisions). 2026-07-27 사용자 지시로
  **T01A(Vault Retrieval/Prompt
  효율화)** 추가 완료: `PROJECT_INDEX.md`(작업 종류→문서 라우팅
  표, Vault 최초 진입점) 신규, `AI_CONTEXT.md`를 "현재 상태" 절이
  최상단에 오도록 개편, `AI_RULES.md`에 Context Retrieval Rule/
  Prompt Rules 추가, `PROMPT_PROFILE.md`(짧은 프롬프트 패턴)/
  `DESIGN_TEMPLATE.md`(표준 설계 템플릿, `99 Templates/`) 신규 —
  Retrieval First/Short Prompt Workflow/Template First 3원칙 도입.
  기존 Backlink/Tag/원문 규칙과 문서 구조는 그대로 유지, 변경된
  파일만 수정. 이어서 **T01B(산출물별 작성 Template 5종)** 추가
  완료: `TASK_TEMPLATE`/`IMPLEMENTATION_TEMPLATE`/`ADR_TEMPLATE`/
  `API_TEMPLATE`/`DECISION_TEMPLATE.md` 신규 — T01에서 만든
  `Template - X.md`(Vault Index 등록용)와 역할을 분리해 "GitHub
  원문/실제 산출물 작성 전 계약 정리용"으로 위치시켰다.
  `PROMPT_PROFILE.md`에 산출물 종류→템플릿 Mapping 표,
  `PROJECT_INDEX.md`에 동일한 Template Index 절을 추가해 두 문서
  모두에서 템플릿을 찾을 수 있게 했다. 이어서 **T01C(EXECUTION_
  PROFILE 도입)** 추가 완료: `EXECUTION_PROFILE.md` 신규 —
  Task Start/Context Retrieval/Template Selection/Task Execution/
  Document Update/Validation/Completion Report 7단계 Standard
  Workflow를 정의해, "무엇을 읽을지"(T01A)/"무엇으로 만들지"
  (T01B)에 이어 "어떻게 처리할지"까지 문서화했다. `PROMPT_PROFILE.md`
  /`PROJECT_INDEX.md`에 각각 연계 절을 추가. 마지막으로
  **T01D(PREPARATION_SUMMARY + M23 Start Criteria)**로 마무리:
  `PREPARATION_SUMMARY.md` 신규(구현 완료 항목/신규 시스템 구성요소/
  템플릿 13종/운영 Workflow 4원칙/Baseline/M23 Start Criteria/
  Deferred Items 종합), `PROJECT_INDEX.md`에 "Preparation Status"
  절, `AI_CONTEXT.md`의 "현재 상태"를 M23 기준으로 갱신. Baseline:
  코드/아키텍처는 v0.5.0 기준선(ADR-0024) + Interface 27종
  (ADR-0034) 유지, Vault는 30개 문서 + 4개 운영 원칙(Retrieval
  First/Short Prompt Workflow/Template First/Standard Execution
  Workflow) 확정. M23 Start Criteria 5개 중 Client 저장소 위치/
  서버 지원 범위/Push 발송 주체 3개는 "미정"으로 정직하게 남기고
  M23 kickoff에서 재확인하기로 함. T08(Obsidian MCP 연동)만 Claude
  Code 도입 시점으로 이월 보류.
- **DX-01(Stage Checkpoint)**: `.ai/RULES.md` §2.4에 따라 2026-07-25부터
  Task 내부 4개 단계 경계마다 Smart Model Router를 실행해 Model/Effort를
  점검한다(`.ai/DECISIONS.md`의 `DX-01` 항목 참고). T1-23(첫 적용)에서는
  4개 경계 중 1개만 실제 발동하는 실행 누락이 있었으나, T1-24 이후에는
  매 Task마다 4개 경계 전부 실제로 발동하고 있다. T1-26에서 처음으로
  **"하향" 판정**(Sonnet/Medium→Sonnet/Low)이 실제로 나왔고 사용자가 승인해
  적용됨 — Skip Rule("동일")뿐 아니라 실제 Model/Effort 변경 경로도 처음
  검증되었다.
- **DX-02(설계 철학 영구 규칙화, 2026-07-25)**: T2-07에서 처음 제시된
  설계 철학(Architecture First 강화/최소 복잡성/YAGNI/점진적 확장/응집도/
  기존 코드 존중)을 `.ai/RULES.md` v0.4.0으로 영구 통합함(`.ai/DECISIONS.md`
  의 `DX-02` 항목 참고). §1.2/§4.2/§4.3 확장 + 신규 §4.5 Cohesion. 이후
  모든 Task의 설계 판단은 이 통합된 규칙을 기준으로 한다 — 특히 "새
  컴포넌트를 만들기 전 자문 질문 6개"(§4.2)를 습관적으로 적용할 것.
  개인 기억 시스템의 `feedback_design_philosophy.md`와 함께 사용.

## 2. 프로젝트 정체성

- **프로젝트명**: AI Workspace
- **한 줄 정의**: Claude Code, Codex, Gemini CLI 등 AI 구현 엔진을 **멀티
  에이전트로 오케스트레이션**하는 플랫폼.
- **핵심 원칙**: AI Workspace는 코드를 작성하지 않는다. 실제 코드 작성은 구현
  엔진의 책임이다. AI Workspace는 역할을 가진 Agent들이 협업하여 프로젝트/Task/
  Workflow/메모리/승인/자동화/다중 프로젝트/구현 엔진을 관리하도록 조율한다.
- **Multi-Agent First (ADR-0006)**: 멀티 에이전트는 선택 기능이 아니라 시스템의
  **기본 구조**다.

## 3. 핵심 아키텍처 (요약)

자세한 내용은 `docs/ARCHITECTURE.md` (v0.6.0) 참고. 여기서는 언제든 빠르게
떠올려야 하는 구조만 압축한다.

```
UI(CLI·Dashboard·Mobile·Voice·REST API·Slack·Discord·Webhook)
  → Interaction Layer
  → Workspace Core (최상위 오케스트레이터, WorkspaceSession 관리)
  → Agent Runtime(Registry · Scheduler · Manager · Event Bus)
       └ Event Bus의 독립 구독자: Event Store(기록/Replay/Audit)
  → Agents(Capability 중심: Coordination·Planning·Coding·Review·Documentation·…)  ←(Event Bus)→
  → Agent가 쓰는 3축:
       ① Core Engines(Task·Workflow·Approval·Automation)
       ② Context Manager → Memory Engine(저장/검색)
       ③ Engine Runtime → Engine Adapter → 구현 엔진(Claude Code·Codex·Gemini CLI)
```

- **Workspace Core**: 프로젝트/설정 로드, 서비스 초기화, **WorkspaceSession 관리,
  Agent Runtime·Engine Runtime 초기화, Workflow 시작, 종료**. Task는 Agent
  Runtime에 위임 (ADR-0010).
- **Agent Runtime**: Registry(등록/조회/제거) · Scheduler(Capability 기준 선택/
  병렬/우선순위) · Manager(생성/생명주기/상태) · Event Bus. **Scheduler 선택이
  실제로 개입을 가르는 자가 확인 가드**(`is_agent_selected()`, Milestone 13)를
  `CodingAgent`가 최초 채택 — 새 디스패처 없이 각 Agent가 스스로
  "내가 선택됐나"를 확인한다.
- **Event Store**: Event Bus의 **독립 구독자**로 이벤트 기록. 전달 게이팅 없음.
  Replay/Audit/복구 (ADR-0014, ADR-0018).
- **Agents**: **Capability 중심**(엔진 비종속). **Coordination Capability**로
  조정 역할 명시(ADR-0019). Event Bus로만 협업. 실제 일은 Engine Runtime에 위임.
- **Engine Runtime (ADR-0016)**: 엔진 선택/세션 풀/병렬. Agent와 Engine Adapter
  **사이**. Agent는 Engine Adapter를 직접 부르지 않는다.
- **Context Manager (ADR-0017)**: Context 조립 + Memory Snapshot 생명주기. 그 아래
  **Memory Engine은 저장/검색만**. Memory 접근은 Agent→Context Manager→Memory Engine.
- **Core Engines(서비스)**: Task/Workflow/Approval/Automation. Memory/Automation은
  Agent가 아니라 서비스(ADR-0012). **Workflow Engine은 실행 순서
  계획(`plan()`)만 담당** — 계획된 순서를 사람 개입 없이 실제로 순차
  실행하는 것은 **`WorkflowRunner`**(Agent도 Core Engine도 아닌 독립
  조율자, Milestone 12)의 책임이다.
- **Interaction Layer**: UI 표면 입력을 표준 요청으로 정규화(ADR-0013). Voice는
  이 계층에 붙는 표면.
- **Engine Adapter**: per-engine 세션 생명주기 계약 create_session/run/cancel/
  status/destroy_session/capabilities/supports_parallel/estimate_cost (ADR-0015).
  실제 명령을 어디서 실행할지는 하위 인터페이스 **ExecutionEnvironment**
  (execute/cancel, ADR-0025, Milestone 11)에 DI로 위임 — Agent/Engine
  Runtime은 이 인터페이스를 모른다. 현재 구현체는 `LocalExecutionEnvironment`
  뿐(Codespaces/Replit/Docker는 YAGNI로 미구현). `run()`은 선택적
  **`model`**도 받는다(ADR-0026, Milestone 14) — `ClaudeCodeEngineAdapter`
  만 실제로 `--model`에 반영, Codex/Gemini는 받되 무시(검증 불가 환경).
- **도메인**: Project · **Mission→Workflow→Task→Step** · **WorkspaceSession** ·
  Agent/AgentRole/AgentCapability(**Coordination 포함**)/AgentStatus.
- **Interfaces (총 18종, Milestone 1에서 16종 계약 정의 + Milestone 5
  `LLMPolicyEngine` + Milestone 11 `ExecutionEnvironment`)**: ProjectRepository,
  WorkflowEngine, TaskEngine, MemoryEngine(저장/검색), ApprovalEngine,
  AutomationEngine, EngineAdapter + AgentManager, AgentRepository, AgentRegistry,
  AgentScheduler, InteractionEngine, EventBus, EventStore, EngineRuntime,
  ContextManager, **LLMPolicyEngine, ExecutionEnvironment**.
- 의존 방향은 항상 위(UI)에서 아래(구현 엔진)로만 향한다. Agent 협업만 Event
  Bus를 통한 수평 결합이며, Event Store는 Bus의 독립 구독자다.

## 4. 반드시 유지해야 하는 설계 원칙

- 실제 코드 작성 금지 원칙은 **문서화 작업(T1-01~T1-11)에 한정**된다. 구현
  작업(T1-12~)부터는 승인을 받은 뒤 코드를 작성한다.
- **Multi-Agent First**: 모든 작업은 능력 있는 Agent들의 협업으로 수행한다.
  Workspace Core는 Task를 직접 실행하지 않고 **Agent Runtime에 위임**한다(ADR-0010).
- **Workspace Core는 Interfaces에만 의존하는 오케스트레이터다 (ADR-0005 유지).**
  처리 로직, 구현 엔진 직접 호출, 파일 저장 세부 구현을 Core에 넣지 않는다.
  WorkspaceSession 관리와 Agent Runtime 초기화가 Core의 핵심 책임이다.
- **Agent는 Capability 중심으로 선택한다 (ADR-0012).** Memory/Automation은
  Agent가 아니라 Core Engine(서비스)다.
- **Agent 간 직접 호출 금지, Event Bus 우선. 모든 이벤트는 Event Store에 기록**
  (ADR-0007, ADR-0014).
- **Voice 등 UI 표면은 Interaction Layer에 붙인다 (ADR-0013).** Workspace
  Core에 직접 연결하지 않는다.
- 구현 엔진은 반드시 **Engine Adapter(세션 생명주기 계약, ADR-0015)**를 통해서만
  호출한다.
- **Milestone 1은 계약과 골격까지만.** Agent Runtime/Engine/Adapter/Event Store/
  Interaction의 실제 처리 로직은 Milestone 2·3에서 구현한다.
- 승인이 필요한 4가지 행위: 아키텍처 변경, 신규 기능, 리팩토링, **Milestone
  완료**(2026-07-24 ADR-0021로 "Phase 완료"에서 변경). Approval Engine이
  판별·차단한다 (우회 경로 없음).
- 계획은 **Milestone → Task** 2단 계층을 따르며(ADR-0021, Phase 계층 폐지),
  Task는 한 번에 하나씩만 진행한다.
- 모든 문서/설명/주석/커밋 메시지는 한국어, 코드 식별자는 Python 표준(영어)을
  따른다.

## 5. 주요 의사결정 요약

전체 배경/대안/이유는 `.ai/DECISIONS.md`의 각 ADR 참고. 여기서는 결론만 압축한다.

| ADR | 결론 | 상태 |
|---|---|---|
| ADR-0001 | 문서를 `README` / `docs/`(사람용) / `.ai/`(AI 운영용) 3계층으로 분리 | 승인됨 |
| ADR-0002 | 구현 엔진은 Adapter 패턴으로 추상화 (`EngineAdapter`) | 제안 (T1-19에서 세션 계약 반영 완료, 구체 구현 후 승인 예정) |
| ADR-0003 | 승인 절차는 별도 Approval Engine 컴포넌트로 분리 (인라인 금지) | 제안 (Core Engines 구현 Milestone에서 확정) |
| ADR-0004 | Milestone 1 저장 방식은 파일 기반(Markdown/JSON)으로 시작 | 제안 (T1-23 구현 후 승인 예정) |
| ADR-0005 | Workspace Core는 Interfaces에만 의존하는 오케스트레이터 | 승인됨 (ADR-0010이 책임 재정의) |
| ADR-0006 | Multi-Agent First: Workspace Core=Agent 오케스트레이터, Agent Manager·Agent 도메인 | 승인됨 (ADR-0010~0012가 심화) |
| ADR-0007 | Agent 협업은 Event Bus 기반 느슨한 결합 | 승인됨 |
| ADR-0008 | Conversation Layer 도입 | 승인됨 (**ADR-0013으로 대체 → Interaction Layer**) |
| ADR-0009 | EngineAdapter를 확장 실행 계약으로 확대 | 승인됨 (ADR-0015가 세션 계약으로 확장) |
| ADR-0010 | **Agent Runtime 계층**(Registry/Scheduler/Manager/Event Bus) + Workspace Core 재정의 + WorkspaceSession | 승인됨 |
| ADR-0011 | **Mission→Workflow→Task→Step** 4단 계층 | 승인됨 |
| ADR-0012 | **Capability 중심 Agent**, Memory/Automation은 Engine(서비스) | 승인됨 |
| ADR-0013 | Conversation Layer → **Interaction Layer**(InteractionEngine) | 승인됨 |
| ADR-0014 | **Event Store** 도입(Replay/Audit/복구) | 승인됨 (ADR-0018이 위치 보완) |
| ADR-0015 | EngineAdapter **세션 생명주기 계약**(create/destroy_session 추가) | 승인됨 |
| ADR-0016 | **Engine Runtime** 계층(Agent Runtime↔Engine Adapter 사이): 엔진 선택/세션 풀/병렬 | 승인됨 |
| ADR-0017 | **Context Manager**로 Memory Snapshot 역할 분리(Memory Engine=저장/검색) | 승인됨 |
| ADR-0018 | Event Store를 Event Bus **독립 Subscriber**로 위치 조정 | 승인됨 |
| ADR-0019 | **Coordination Capability** 추가(조정 역할 명시) | 승인됨 |
| ADR-0020 | Task에 `workflow_id`(선택 필드) 추가 — Task-Workflow 관계 보완 | 승인됨 |
| ADR-0021 | **Phase 계층 폐지**, `Milestone → Task` 2단 체계로 전환 | 승인됨 |
| ADR-0022 | **Task 분해 원칙**: 아키텍처 책임 경계로 Task 분해, 정의·구현·테스트는 한 Task 내 완결 | 승인됨 |
| ADR-0023 | `run_parallel()` 병렬 실행 책임 경계: AgentScheduler(선택) vs EngineRuntime(실행) | 승인됨 |
| ADR-0024 | v0.5.0 아키텍처 기준선(Baseline) 선언 (`pyproject.toml` 버전 상향) | 승인됨 |
| ADR-0025 | **ExecutionEnvironment**를 새 최상위 Layer 대신 `EngineAdapter` 하위 인터페이스로 도입, DI 기본 방향 | 승인됨 |
| ADR-0026 | `EngineAdapter`/`EngineRuntime`에 `model` 파라미터 확장(Model 라우팅, `ClaudeCodeEngineAdapter`만 적용) | 승인됨 |
| ADR-0027 | `EngineRuntime`에 `estimate_cost()` 추가 + `BudgetPolicyEngine` 신설(Token & Cost Optimization) | 승인됨 |
| ADR-0028 | Project Knowledge System 도입(`KnowledgeRepository`/`KnowledgeSearch`/`KnowledgeProvider`), 기존 `MemoryEngine`과 분리 | 승인됨 |
| ADR-0029 | Intelligent Engine Selection 도입(`EngineRegistry`+`EngineSelectionPolicy`, Decision Only), `EngineRuntime` 계약 미확장 | 승인됨 |
| ADR-0030 | Execution Layer 도입(`ExecutionDispatcher` 구체 클래스 + `AuthenticationManager`), Decision-Execution 완전 분리, 첫 End-to-End 실행 경로 완성 | 승인됨 |
| ADR-0031 | Reliability Layer 도입(`RetryPolicy` 확장 + `RetryExecutor`), `timed_out` 휴리스틱 기술 부채 명시 | 승인됨 |

기술 스택(Python, dataclasses, 파일 기반 저장, CLI, 인메모리 Event Bus+파일
Event Store)은 제안 단계이며 각 구현 Milestone에서 확정한다.

## 6. 이후 작업에 필요한 핵심 컨텍스트

- **Milestone 1 범위**: 도메인(Project/Task **+ Mission/Workflow(재정의)/
  Step + WorkspaceSession + Agent/AgentRole/AgentCapability(Coordination 포함)/
  AgentStatus**) + Interfaces 16종(계약만) + **세션 생명주기 EngineAdapter 계약** +
  Agent Runtime·Engine Runtime 위임형 Workspace Core 골격 + 파일 저장소(Project/
  Agent/EventStore) + 최소 CLI + 테스트. 실제 처리 로직은 Milestone 1 범위 밖.
- **Milestone별 구체 구현 순서**: Agent Runtime·Event Store·기본 Agent, Core
  Engines·Context Manager (Milestone 2, 완료) → Engine Runtime·Engine
  Adapter(Claude Code 우선) (Milestone 3, 완료) → 자동화·다중 프로젝트·메모리
  고도화 + **Interaction Layer + CodingAgent 실제 Engine 경로 통합(M3에서
  이관)** (Milestone 4, 완료, v0.5.0 아키텍처 기준선) → **LLM Policy
  Engine·DevelopmentContext+Agent 강화·ShellAgent·Codex/Gemini Adapter·
  Workflow 조건부 분기**(Milestone 5, Task List 확정).
- 구현 엔진 연동 순서: Claude Code 최우선 → Codex → Gemini CLI.
- Voice/Slack 등 표면, Event Store, Interaction은 **구조에는 포함하되 구현은 뒤로**
  미룬다 (인터페이스만 Milestone 1에서 정의).
- **미완료 유지 항목**: `EngineAdapter`는 T1-19에서 `run_task` 기반 계약을
  세션 생명주기 계약(create_session/run/…/destroy_session)으로 교체 완료함
  (구체 구현은 여전히 Milestone 3). `ConversationEngine`은 `InteractionEngine`
  으로 **T1-21**(Interaction Interfaces)에서 대체 예정.
- **LLM Policy는 여전히 "Temporary"이나 M5-T01로 Rule 기반 선택 단계에
  진입함(2026-07-26)**: `interfaces/llm_policy_engine.py`의
  `LLMPolicyEngine`(M1 이후 첫 신규 최상위 Interface, 총 17종) +
  `engines/llm_policy_engine.py`의 `InMemoryLLMPolicyEngine`이 실제로
  `docs/llm_policy.example.yaml`(이제 실제로 파싱됨, 키가 `AgentRole.value`
  와 정확히 일치)을 읽어 AgentRole별 Provider/Model/Effort를 반환한다.
  `storage/llm_policy_loader.py`가 PyYAML 파싱을 전담해 Engine은 저장
  형식을 모른다(PolicyLoader 계층 분리, 사용자 지시). 프로젝트 최초로
  `pyyaml`을 런타임 의존성으로 추가(순수 stdlib 기조 최초 이탈, 사용자
  승인). 남은 진행 경로: M5-T02(Agent가 실제로 이 Engine을 참조하도록
  연결) → M6+(Self Optimizer 자동 최적화, 원래 M5 목표였으나 이관됨).
  자세한 내용은 `.ai/RULES.md` §7 "Temporary LLM Policy" 참고.
- **현재 상태(2026-07-27)**: Milestone 1~19 전체 완료(사용자 승인).
  Milestone 20(Real-time Dashboard Platform)은 검토 시작 시점(Task
  Driven Development 원칙). 버전 v0.5.0 유지(ADR-0024 기준선 —
  M19까지의 변경은 전부 기존 계약 위에서의 추가·확장이거나 신규
  계층 도입 계열이라 기준선 재선언 대상이 아니라고 판단했으나,
  M16~M18에서 Interface가 19→25종으로 크게 늘어난 만큼 다음 기준선
  재검토 시점에 누적 변화를 함께 검토할 필요가 있음). `pytest`
  588개, `ruff`/`mypy` 클린. Task→Selection Policy→Decision→
  Dispatcher→Authentication→Registry→Adapter→ExecutionEnvironment→
  `EngineExecutionResult`로 이어지는 첫 End-to-End 실행 경로가
  완성됐고(M11/M15/M16/M17/M18), M19에서 Retry/Timeout/Cancellation
  Reliability까지 더해졌다. **참고**: `pyproject.toml`의 런타임
  의존성은 지금까지 `pyyaml` 하나뿐이다 — M20(Dashboard, HTTP API+
  WebSocket+Web UI)은 이 프로젝트 최초로 웹 프레임워크 의존성을
  요구할 전망이다.
- **이 환경의 제약(2026-07-26 확인)**: `claude` CLI만 설치되어 있고
  `codex`/`gemini` CLI는 설치되어 있지 않다(`which` 확인). Codex/Gemini
  관련 Task는 이 세션에서 실행 불가 — 실제 CLI가 설치된 환경이 필요하다.
- **누적 Technical Debt(2026-07-27 기준, M15 완료 후)**: (1)
  **Effort 수준 라우팅 미완성** — Model은 M14에서 해소됐지만(opus/
  sonnet/haiku가 `--model`까지 반영됨), Effort(low/medium/high)는
  Claude Code CLI에 대응하는 플래그가 없어 검증 불가능한 상태가 되는
  것을 피하려 의도적으로 제외(M14 신규 이월 — 이전에는 "Model/Effort
  수준 라우팅 미완성"으로 함께 묶여 있었으나 Model만 먼저 해소).
  (2) `ClaudeCodeEngineAdapter`↔`CLIEngineAdapter` 프레임워크 미통합
  (M5-T05 최초 이월, M10 재분석에서 "기능 이득 없는 순수 리팩토링"으로
  재확인). (3) Codex/Gemini CLI 실제 바이너리 미검증(M5-T05 최초 이월,
  M10 재분석에서 이 환경엔 실행 자체가 불가능함을 확인 — M14도 같은
  이유로 Model 라우팅을 `ClaudeCodeEngineAdapter`에만 적용). (4)
  `MemoryEngine.search()` 선형 스캔(M4-T08 최초 이월, 성능 — M10
  재분석에서 PRD §11이 "필요해지면"으로 이미 유보한 항목임을 재확인,
  조사 우선 접근 권장). (5) Retry Backoff/Persistent Runtime Recovery/
  Approval 비동기 처리/Process Timeout 정책 고도화(M3-T08 최초 이월),
  `ShellAgent` 화이트리스트가 코드에 고정(M5-T04 최초 이월). M9-T01
  (동시성 경쟁 조건)·M9-T03(세션 리셋)·M10-T02/T03(run_parallel 개별
  실패 격리+재시도, M4-T06 이월 부채)·M14(Model 라우팅)은 해소되어
  더 이상 부채 목록에 없다.
- **M23-T01 완료: Reading Profiles(2026-07-27)**. M23-Preparation
  (T01A~T01D)에서 도입한 Retrieval First/Minimum Retrieval/Short
  Prompt Workflow/Template First/Standard Execution Workflow
  원칙을 15개 작업 유형(Architecture Design/Feature Design/API
  Design/Backend·Frontend·Mobile Implementation/Dashboard·
  Automation Development/ADR·Decision 작성/Bug Fix/Refactoring/
  Documentation/Milestone Planning/Daily 기록)별 표준 Reading
  Profile로 세분화. Vault `00 System/READING_PROFILES.md` 신규 —
  각 Profile은 목적/필수 문서/선택 문서/읽지 않는 문서/쓸 Template/
  예상 Retrieval 순서/예상 출력 문서 7항목 고정. `PROJECT_INDEX`
  (Reading Profiles Index 절)/`EXECUTION_PROFILE`(Context
  Retrieval·Template Selection 단계에 적용 절차)/`PROMPT_PROFILE`
  (Reading Profile 연계 절)에 연결해 기존 Router/Standard Workflow
  체계와 일관되게 유지. Milestone 23(Mobile Experience) 본 기능
  착수는 여전히 대기 상태(PREPARATION_SUMMARY의 Start Criteria
  1~3 미해결) — 이번 Task는 그 착수 전 Retrieval 기반을 한 단계
  더 다진 것.
