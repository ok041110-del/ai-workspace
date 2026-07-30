---
tags: [system]
---

# Project Intelligence 사용법

이 폴더는 Intelligence Layer(`intelligence/`)가 만드는 **생성된
리포트** 전용이다. 두 파일 모두 사람이나 AI가 직접 편집하는 원본이
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

## 관련 문서

- [[Milestones Index]]
- [[Dashboard Index]]
- [[Architecture Overview]]

## 원문

- `.ai/TASKS.md`의 "Milestone 29 — Project Intelligence"/"Milestone
  30 — Context Intelligence" 절
- `.ai/DECISIONS.md`의 ADR-0043/ADR-0044
- `src/ai_workspace/intelligence/`
