---
tags: [system]
---

# Project Intelligence 사용법

이 폴더는 Intelligence Layer(`intelligence/`)가 만드는 **생성된
리포트** 전용이다. 세 파일 모두 사람이나 AI가 직접 편집하는 원본이
아니라, 매번 처음부터 다시 계산해 덮어쓰는 파일이다 — 직접 수정해도
다음 실행 때 사라진다.

`14 Tasks/*.md`와 달리 `VaultDocumentKind` 체계(Index append/
Backlink 검증)를 쓰지 않는다 — 원자적 전체 교체(overwrite)만 한다.

## `Project Intelligence.md` (Milestone 29, ADR-0043)

`src/ai_workspace/intelligence/report.py`의
`ProjectIntelligenceService.publish()`가 Vault Task 문서(`14
Tasks/`)를 읽어 계산한다
(`vault.intelligence_report.write_project_intelligence_report()`).

- **Snapshot**: 전체 Task 수/상태별·Milestone별·Owner별 집계,
  진행률, 활성 Agent 수
- **Health**: Healthy/Warning/Critical (Rule 기반)
- **Risk**: 정체(Stagnant) Task/Owner 과부하/Milestone 정체
- **Recommendation**: 위 Risk에 대응하는 다음 행동 추천(Rule 기반,
  AI 추론/LLM 호출 없음)

## `Project Context.md` (Milestone 30, ADR-0044)

`src/ai_workspace/intelligence/context_service.py`의
`ContextIntelligenceService.publish()`가 Knowledge Layer(M16, `.ai/`
/`docs/` 6개 문서)를 읽어 지금 하는 작업(Task/Milestone)과 관련된
맥락을 정리한다
(`vault.context_report.write_project_context_report()`).

- **관련 ADR/Task/Architecture/Rules/Roadmap·PRD**: subject(예:
  "M30-T05")가 Markdown 제목 단위로 언급된 항목만 나열
- **Freshness**: Healthy/Warning (언급된 Milestone 번호와 현재
  Milestone의 거리로 판단)
- **Gap**: ADR/Task/Architecture 중 언급이 0건인 항목(Rule/
  Roadmap·PRD는 범용 문서라 Gap 판정 대상 아님)
- **Context Quality Score**: Gap/Freshness를 조합한 0~100% 점수

## `Capability Intelligence.md` (Milestone 31, ADR-0045)

`src/ai_workspace/intelligence/capability_service.py`의
`CapabilityIntelligenceService.publish()`가 기존 `AgentAdapter`
(M28)가 노출한 활성 Agent 정보를 읽어, 정의된 `AgentCapability`
(11종) 대비 실제 커버리지를 정리한다
(`vault.capability_report.write_capability_report()`).

- **Snapshot**: 활성 Agent 수, Role별/Capability별 집계
- **Coverage**: none/partial/full(정의된 Capability 대비 커버 비율).
  M29/M30의 healthy/warning/critical과 달리 중립적인 이름을 쓴다 —
  활성 Agent 0명은 시스템 이상이 아니라 이 저장소가 아직 Agent
  프로세스를 상시 구동하지 않는 워크숍 단계의 자연스러운 상태이기
  때문이다
- **Gap**: 정의된 Capability 중 활성 Agent가 0명인 항목

## `Intelligence Overview.md` (Milestone 32, ADR-0046)

`src/ai_workspace/intelligence/synthesis_service.py`의
`IntelligenceSynthesisService.publish()`가 위 세 리포트를 만드는
Service(`ProjectIntelligenceService`/`ContextIntelligenceService`/
`CapabilityIntelligenceService`)를 그대로 실행한 뒤 결과만 합성한다
(`vault.intelligence_overview.write_intelligence_overview_report()`)
— 새로운 데이터 소스나 판단 기준을 추가하지 않는다.

- **요약**: 세 리포트의 등급(Project Health/Context Freshness/
  Capability Coverage) + 통합 Finding 수
- **Findings**: 위 세 리포트의 Risk/Gap을 출처(Project/Context/
  Capability)별로 그대로 옮겨 담은 목록(target 기준 정렬, 새
  우선순위 알고리즘 없음)

## `Session Resume.md` (Milestone 33, ADR-0047)

`src/ai_workspace/intelligence/session_resume_service.py`의
`SessionResumeService.publish()`가 "현재 작업"을 고른 뒤 위 세
Service(`ProjectIntelligenceService`/`ContextIntelligenceService`/
`CapabilityIntelligenceService`) + M32 `IntelligenceSynthesisAnalyzer`
를 그대로 실행해 조합한다(`vault.session_resume.
write_session_resume_report()`) — 새로운 데이터 소스나 판단 기준을
추가하지 않는다.

- **현재 작업**: 활성 상태(in-progress/review) Task 중 `updated`가
  가장 최근인 1건(없으면 "현재 진행 중인 Task 없음")
- **Project 상태**: 진행률/Health(M29 재사용)
- **관련 Context**: 현재 작업을 subject로 한 Context Intelligence
  결과(M30 재사용)
- **Capability 상태**: Coverage(M31 재사용)
- **다음 작업**: M29 Recommendation을 그대로 노출(새 추천 로직 없음)

## `Workflow Intelligence.md` (Milestone 34, ADR-0048)

`src/ai_workspace/intelligence/workflow_service.py`의
`WorkflowIntelligenceService.publish()`가 Vault Task 문서(`14
Tasks/`)를 읽어 Milestone별 Task 실행 흐름을 계산한다
(`vault.workflow_intelligence.write_workflow_intelligence_report()`).
여기서 "Workflow"는 `domain.Workflow`(영속 저장소 없는 휘발성 값
객체)가 아니라 **Milestone 안의 Task 실행 순서**를 가리킨다 —
`domain.Workflow`/`WorkflowEngine`/`WorkflowAdapter`는 사용하지
않는다.

- **Milestone별 진행률**: 완료 Task 수 / 전체 Task 수
- **Blocked**: `todo` Task 중 Task ID 순서상 선행 Task가 아직
  완료(`done`/`archived`)되지 않은 것(Rule 기반, `WorkflowFlowAnalyzer`)
- **Next(다음 실행 가능)**: 선행 Task가 모두 완료된 `todo` Task
- 미완료 Task가 없는(이미 끝난) Milestone은 표시하지 않음 — 진행
  중인 Milestone이 하나도 없으면 "현재 진행 중인 Milestone 없음"

## `Recommendation Intelligence.md` (Milestone 35, ADR-0049)

`src/ai_workspace/intelligence/recommendation_service.py`의
`RecommendationIntelligenceService.publish()`가 M29/M31/M33/M34
Intelligence를 조합해 단일 다음 행동(Next Action)을 결정한다
(`vault.recommendation_intelligence.
write_recommendation_intelligence_report()`). Execution Layer
이전의 마지막 Decision Layer — 자동으로 실행하지 않고 추천만
제공한다.

- **다음 행동**: 5단계 Priority Rule 중 첫 번째로 해당하는 것 —
  ① Current Work(M33) 계속 수행 ② Workflow Next Task(M34) 시작
  ③ Workflow Blocked Task(M34) 해소 ④ Capability Gap(M31) 보완
  ⑤ M29 Project Recommendation(priority 최고) 그대로 노출. 모두
  해당 없으면 "추천할 다음 행동 없음"
- **근거**: 현재 작업/Workflow 진행 상황/Capability Coverage/Project
  Recommendation 전체를 함께 노출해 판단 근거를 투명하게 보여줌

## 관련 문서

- [[Milestones Index]]
- [[Dashboard Index]]
- [[Architecture Overview]]

## 원문

- `.ai/TASKS.md`의 "Milestone 29 — Project Intelligence"/"Milestone
  30 — Context Intelligence"/"Milestone 31 — Capability
  Intelligence"/"Milestone 32 — Intelligence Synthesis"/"Milestone
  33 — Session Resume"/"Milestone 34 — Workflow Intelligence"/
  "Milestone 35 — Recommendation Intelligence" 절
- `.ai/DECISIONS.md`의 ADR-0043/ADR-0044/ADR-0045/ADR-0046/ADR-0047/
  ADR-0048/ADR-0049
- `src/ai_workspace/intelligence/`
