---
tags: [system]
---

# PROMPT_PROFILE

Short Prompt Workflow의 실제 패턴 모음. [[AI_RULES]]의 Prompt
Rules가 원칙이고, 이 문서는 그 원칙을 반복 작업 유형별 짧은
프롬프트 예시로 구체화한다.

## 원칙

- 문서를 다시 붙여넣지 말고 `[[문서 제목]]`으로 참조한다.
- "무엇을 바꿀지"만 짧게 쓰고, "왜 이 프로젝트가 이런 구조인지"는
  다시 설명하지 않는다(이미 Vault에 있다).
- 새 설계는 자유 서술 대신 [[DESIGN_TEMPLATE]] 형식을 요청한다.

## 패턴별 예시

| 작업 유형 | 짧은 프롬프트 예시 |
|---|---|
| 새 Milestone/기능 설계 | "[[DESIGN_TEMPLATE]] 형식으로 <기능명> 설계해줘" |
| 기존 영역 확장 | "[[Dashboard Index]] 기준으로 <확장 내용> 추가 설계해줘" |
| 버그 수정 | "<증상> 발생. 관련 영역은 [[Automation Index]] 참고해서 원인 파악해줘" |
| 문서만 갱신 | "[[Production Index]] 갱신 — <바뀐 내용>만 반영" |
| 과거 결정 확인 | "[[ADR Index]]에서 <주제> 관련 ADR 찾아서 요약해줘" |
| Milestone 이력 확인 | "[[Milestones Index]]에서 <Milestone 번호> 요약 보여줘" |
| 새 Task 착수 | "TASKS.md에 <Task ID> DoD 작성하고 승인 요청해줘" |

## 안티패턴(피할 것)

- GitHub 파일 전체 내용을 프롬프트에 복사해 붙여넣기 — 대신
  경로/문서 제목만 언급.
- 이미 Vault에 정리된 배경 설명을 매번 다시 요청 — [[PROJECT_INDEX]]
  라우팅 표를 먼저 따른다.
- 템플릿 없이 새 설계 문서를 자유 형식으로 요청 — [[DESIGN_TEMPLATE]]
  를 우선 사용한다.

## 관련 문서

- [[PROJECT_INDEX]]
- [[AI_RULES]]
- [[DESIGN_TEMPLATE]]

## 원문

- 없음(이 문서 자체가 Vault 전용 프롬프트 가이드이며 GitHub에
  대응 원문이 없다)
