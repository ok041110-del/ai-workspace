---
tags: [architecture]
---

# Overview

> [[AI_CONTEXT]]를 먼저 읽었다면 이 문서는 그 다음 단계다.

## 프로젝트 소개

**AI Workspace**는 Claude Code, Codex, Gemini CLI 등 AI 구현
엔진을 멀티 에이전트로 오케스트레이션하는 Python 플랫폼이다.
AI Workspace 자체는 코드를 작성하지 않는다 — 역할을 가진 Agent들이
협업해 프로젝트/Task/Workflow/메모리/승인/자동화/구현 엔진을
관리하도록 조율한다. Multi-Agent First가 이 프로젝트의 기본
구조다(선택 기능이 아니다).

## 저장소 목록

| 저장소 | 역할 | 상태 |
|---|---|---|
| `ok041110-del/ai-workspace` | Python 백엔드(Server/Dashboard/Automation/Production) | 진행 중 |
| (이 Vault) | Knowledge Base(Obsidian) | 이 저장소 내 `Vault/`로 체크인 |
| iOS 앱 | Mobile Experience(M23) | 미착수 — [[iOS Design]] 참고 |
| Android 앱 | Mobile Experience(M23) | 미착수 — [[Android Placeholder]] 참고 |

## 현재 진행률

- **Milestone 1~22 완료**(2026-07-27 기준).
- **Milestone 23(Mobile Experience)**: 착수 전. 지식 허브를 먼저
  구축하는 **M23-Preparation** 진행 중(이 Vault 자체가 그 산출물).
- 상세 목록은 [[Milestones Index]] 참고.

## Backend 상태

Python 3.11 + FastAPI/uvicorn 기반 서버. Core Domain(도메인/
인터페이스/엔진)과 Infrastructure(Dashboard/Automation/Production/
Web API)가 분리돼 있다. Interface(추상 계약) 총 **27종**. 상세는
[[Architecture Overview]]와 [[Backend Index]] 참고.

## Mobile 계획

M23에서 iOS(Widget/Live Activity/Push Notification)와 Android를
다룰 예정이다. 서버가 이미 제공하는 REST API(`/api/dashboard`,
`/api/automation`, `/api/health`, `/api/status` 등)를 그대로
소비하는 Client로 설계한다 — 서버 쪽에 Mobile 전용 로직을 추가하지
않는다(M22 Production Platform이 이미 `uptime`/`started_at`/
`version`/`health_status` 표준 필드를 M23 재사용을 염두에 두고
설계함). 상세는 [[iOS Design]], [[Android Placeholder]] 참고.

## 현재 Milestone

**M23-Preparation** — Obsidian Knowledge Base 구축(이 Vault).
Task 진행 상태는 GitHub `.ai/TASKS.md`의 "M23-Preparation" 절
참고.

## 관련 문서

- [[AI_CONTEXT]]
- [[Architecture Overview]]
- [[Milestones Index]]

## 원문

- README.md
- docs/ROADMAP.md
- docs/PRD.md
