---
tags: [system]
---

# AI_CONTEXT

이 문서는 [[PROJECT_INDEX]] 다음으로 읽는 문서다. "지금 프로젝트가
어떤 상태인가"를 가장 먼저 보여주고, 그 다음에만 프로젝트 자체를
설명한다 — 매 세션마다 정적인 설명을 다시 읽기보다 "지금 무엇이
바뀌었는가"를 먼저 파악하도록 순서를 둔다.

## 현재 상태(가장 먼저 확인)

- **완료**: Milestone 1~22 전체 + **M23-Preparation(Obsidian
  Knowledge Base 구축, T01~T07 + T01A~T01D) 전체 완료** +
  **Milestone 23-T01(Reading Profiles)/T02(Obsidian Integration
  Architecture, ADR-0035) 완료**. Vault 30개+ 문서, Retrieval
  First/Short Prompt Workflow/Template First/Standard Execution
  Workflow 4개 운영 원칙 도입 완료.
- **진행 중**: Milestone 23이 "Obsidian Integration & Auto Save"로
  재정의됨(2026-07-27) — GitHub↔Vault 자동 저장 구조 구현. 다음
  Task는 M23-T03(Vault Save Engine). 원래 M23이 다루던 Mobile
  Experience는 별도 Milestone(번호 미정)으로 이월됨 — Start
  Criteria 3개 결정(Client 별도 저장소/Server API 전용/Push는
  Server 생성+FCM·APNs 전송)은 [[PREPARATION_SUMMARY]]의 "Mobile
  Experience Start Criteria" 절에 그대로 보존.
- **Baseline**: 코드/아키텍처는 v0.5.0 기준선(ADR-0024) + Interface
  27종(ADR-0034) 유지. Vault를 포함한 전체 산출물의 상세 Baseline은
  [[PREPARATION_SUMMARY]] 참고.
- 상세 진행률·이력은 [[Overview]]와 [[Milestones Index]] 참고
  (이 섹션이 바뀔 때마다 그 문서들도 함께 갱신한다).

## 프로젝트 한 줄 정의

**AI Workspace** — Claude Code, Codex, Gemini CLI 등 AI 구현 엔진을
멀티 에이전트로 오케스트레이션하는 Python 플랫폼. AI Workspace는
코드를 직접 작성하지 않는다 — 역할을 가진 Agent들이 협업해 프로젝트
/Task/Workflow/메모리/승인/자동화/구현 엔진을 관리하도록 조율한다.

## Source of Truth는 GitHub다

- 저장소: `ok041110-del/ai-workspace`
- 실제 코드: `src/ai_workspace/`
- 실제 문서: `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`, `docs/PRD.md`
- 실제 결정 기록: `.ai/DECISIONS.md`(ADR)
- 실제 진행 이력: `.ai/TASKS.md`

이 Vault(Obsidian)는 위 GitHub 문서를 **대체하지도, 복사하지도**
않는다. 요약과 링크만 제공하는 Knowledge Index다.

## 이 Vault를 읽는 순서

작업별 상세 라우팅은 [[PROJECT_INDEX]]의 표를 따른다. 이 문서는
그 표에서 참조하는 진입점 중 하나일 뿐, 매번 전체 흐름을 다시
설명하지 않는다.

## 관련 문서

- [[PROJECT_INDEX]]
- [[AI_RULES]]
- [[PREPARATION_SUMMARY]]
- [[Overview]]
- [[Architecture Overview]]

## 원문

- `README.md`
- `docs/ROADMAP.md`
