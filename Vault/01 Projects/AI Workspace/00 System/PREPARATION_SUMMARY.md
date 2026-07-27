---
tags: [system, milestone]
---

# PREPARATION_SUMMARY

M23-Preparation(Obsidian Knowledge Base 구축, T01~T07 + T01A~T01C)
전체의 완료 결과를 한 문서로 요약한다. 개별 Task 상세는 GitHub
`.ai/TASKS.md`의 "M23-Preparation" 절, Milestone 이력 전체는
[[Milestones Index]] 참고.

## 구현 완료 항목

| Task | 내용 |
|---|---|
| T01 | Vault 초기 구성(PARA 구조) + `AI_CONTEXT`/`AI_RULES` + Template 6종 |
| T02 | `Overview`/`Architecture Overview`/`Architecture Map` |
| T03 | `ADR Index`(ADR-0001~0034, 34개 3줄 요약) |
| T04 | `Backend Index`/`API Catalog` |
| T05 | `Dashboard Index`/`Automation Index`/`Production Index` |
| T06 | `iOS Design`/`Android Placeholder`/`Milestones Index`(M1~M22) |
| T07 | `Decisions Index`/Daily 사용법 + Vault 전체 검증 |
| T01A | `PROJECT_INDEX`(Router)/`AI_CONTEXT` 현재 상태 중심 개편/`AI_RULES` Retrieval·Prompt Rules/`PROMPT_PROFILE`/`DESIGN_TEMPLATE` |
| T01B | 산출물 작성용 Template 5종(`TASK`/`IMPLEMENTATION`/`ADR`/`API`/`DECISION_TEMPLATE`) + Template Mapping |
| T01C | `EXECUTION_PROFILE`(Standard Workflow 7단계) |

## 신규 시스템 구성요소(`00 System/`)

| 문서 | 역할 |
|---|---|
| [[PROJECT_INDEX]] | Vault 최초 진입점 — 작업/산출물/실행 흐름 Router |
| [[AI_CONTEXT]] | 현재 상태 요약 + 프로젝트 정의 |
| [[AI_RULES]] | Backlink/Tag/GitHub Link/AI Reading/Context Retrieval/Prompt Rules |
| [[PROMPT_PROFILE]] | 짧은 프롬프트 패턴 + Template Mapping + Execution Profile 연계 |
| [[EXECUTION_PROFILE]] | Standard Workflow 7단계(Task Start~Completion Report) |
| PREPARATION_SUMMARY(이 문서) | M23-Preparation 전체 결과 및 M23 착수 기준 |

## 생성된 템플릿 목록(`99 Templates/`, 13종)

- **설계/실행용**(`_TEMPLATE.md`): [[DESIGN_TEMPLATE]],
  [[TASK_TEMPLATE]], [[IMPLEMENTATION_TEMPLATE]], [[ADR_TEMPLATE]],
  [[API_TEMPLATE]], [[DECISION_TEMPLATE]]
- **Vault 등록용**(`Template - X.md`): [[Template - Architecture]],
  [[Template - ADR Summary]], [[Template - API]],
  [[Template - Decision]], [[Template - Milestone]],
  [[Template - Daily]]

## 운영 Workflow 요약

1. **Retrieval First** — [[PROJECT_INDEX]]의 라우팅 표로 필요한
   문서만 찾는다.
2. **Short Prompt Workflow** — 문서 내용을 다시 붙여넣지 않고
   `[[링크]]`로만 참조한다([[PROMPT_PROFILE]]).
3. **Template First** — 만들려는 산출물에 맞는 템플릿을 먼저
   고른다(Template Index/Mapping).
4. **Standard Execution Workflow** — Task Start → Context
   Retrieval → Template Selection → Task Execution → Document
   Update → Validation → Completion Report([[EXECUTION_PROFILE]]).

## 프로젝트 현재 기준선(Baseline)

- **코드/아키텍처**: Milestone 1~22 완료. Interface 27종(ADR-0034
  기준, M20/M21에서 2종 추가 후 M22는 추가 없음). v0.5.0 아키텍처
  기준선(ADR-0024) 이후 구조 변경 없이 기능만 확장.
- **지식 관리**: M23-Preparation으로 GitHub Source of Truth를
  요약+링크로 Index화한 Obsidian Vault(`Vault/`, 30개 문서) 구축
  완료. Retrieval/Prompt/Template/Execution 4개 효율화 원칙 도입.
- **문서 버전**: `docs/ARCHITECTURE.md` v0.24.0, `docs/ROADMAP.md`
  v0.22.0(T01D 갱신 예정 포함).
- **미착수**: Milestone 23(Mobile Experience) 자체 — 아래 Start
  Criteria 충족 후 착수.

## M23 Start Criteria(착수 조건)

Mobile Experience(M23) 목표 검토를 시작하려면 아래를 먼저
확정한다:

| # | 조건 | 현재 상태 |
|---|---|---|
| 1 | Client 코드 저장소 위치(이 저장소 내부 vs 별도 저장소) 결정 | 미정([[Decisions Index]] "왜 Server와 iOS를 분리했는가" 참고) |
| 2 | 서버 지원 범위 확정(서버 API 소비 전용 / PWA / 네이티브 앱 코드까지 이 저장소가 포함하는지) | 미정 — M23 kickoff 시 사용자 확인 필요 |
| 3 | Push 발송 주체(서버 자체 vs 별도 서비스) 결정 | 미정([[iOS Design]] "미결정 사항" 참고) |
| 4 | M22 Production API(`uptime`/`started_at`/`version`/`health_status`)가 M23 요구를 충족하는지 재확인 | 충족(설계 시점부터 M23 재사용 목적으로 준비됨, ADR-0034) |
| 5 | Vault Index가 M23 작업에 필요한 최소 컨텍스트(Backend/API/Production)를 제공하는지 확인 | 충족(T04~T05 완료) |

1~3은 사용자 결정이 필요한 미해결 항목이며, M23 목표 검토
(kickoff) 시점에 명시적으로 다시 확인한다.

## 향후 개선 대상(Deferred Items)

- **T08(Optional) — Obsidian MCP 연동**: Claude Code 도입 시점으로
  이월(사용자 지시, 지금 범위 아님).
- **Client 저장소 분리 여부**: [[Decisions Index]]에 "미정"으로
  기록됨 — M23 kickoff에서 결정.
- **Android 설계**: [[Android Placeholder]] — iOS 설계 확정 후
  착수.
- **Vault↔GitHub 자동 동기화**: 이번 범위 아님(수동 갱신 유지).

## 관련 문서

- [[PROJECT_INDEX]]
- [[Milestones Index]]
- [[Overview]]

## 원문

- `.ai/TASKS.md`(M23-Preparation Review)
- `docs/ROADMAP.md`
