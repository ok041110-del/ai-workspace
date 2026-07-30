---
tags: [system]
---

# Project Intelligence 사용법

이 폴더는 Milestone 29(Project Intelligence)가 만드는 **생성된
리포트** 전용이다. `Project Intelligence.md`는 사람이나 AI가 직접
편집하는 원본이 아니라, `src/ai_workspace/intelligence/report.py`의
`ProjectIntelligenceService.publish()`가 Vault Task 문서(`14 Tasks/`)
를 다시 읽어 매번 처음부터 다시 계산해 덮어쓰는 파일이다 — 직접
수정해도 다음 실행 때 사라진다.

`14 Tasks/*.md`와 달리 `VaultDocumentKind` 체계(Index append/
Backlink 검증)를 쓰지 않는다(ADR-0043) — 원자적 전체 교체(overwrite)
만 한다(`vault.intelligence_report.write_project_intelligence_report()`).

## 담는 내용

- **Snapshot**: 전체 Task 수/상태별·Milestone별·Owner별 집계,
  진행률, 활성 Agent 수
- **Health**: Healthy/Warning/Critical (Rule 기반)
- **Risk**: 정체(Stagnant) Task/Owner 과부하/Milestone 정체
- **Recommendation**: 위 Risk에 대응하는 다음 행동 추천(Rule 기반,
  AI 추론/LLM 호출 없음)

## 관련 문서

- [[Milestones Index]]
- [[Dashboard Index]]
- [[Architecture Overview]]

## 원문

- `.ai/TASKS.md`의 "Milestone 29 — Project Intelligence" 절
- `.ai/DECISIONS.md`의 ADR-0043
- `src/ai_workspace/intelligence/`
