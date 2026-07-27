---
tags: [system]
---

# AI_CONTEXT

이 문서는 AI(Claude 등)가 이 Vault를 처음 열었을 때 가장 먼저 읽어야
하는 문서다. "이 프로젝트가 무엇인지"와 "이 Vault를 어떻게 써야
하는지"만 담는다.

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

## 이 Vault를 읽는 순서 ([[AI_RULES]] 참고)

Vault 전체를 읽지 않는다. 작업 종류에 따라 최소 문서만 읽는다:

```
어떤 작업이든 시작 → [[Overview]] → [[Architecture Overview]]
                                          ↓
                         작업 영역에 맞는 Index (예: [[Dashboard Index]])
                                          ↓
                              필요하면 GitHub 원문
```

## 현재 상태 (요약)

- Milestone 1~22 완료(2026-07-27 기준), Milestone 23(Mobile
  Experience) 목표 검토 중.
- 이 Vault(M23-Preparation)는 M23 착수 전 지식 허브를 먼저
  구축하는 준비 단계다.
- 상세 진행률은 [[Overview]]와 [[Milestones Index]] 참고.

## 관련 문서

- [[AI_RULES]]
- [[Overview]]
- [[Architecture Overview]]

## 원문

- `README.md`
- `docs/ROADMAP.md`
