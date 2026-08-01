---
tags: [system]
type: documentation
---

# IMPLEMENTATION_TEMPLATE

Task 하나를 실제로 구현한 뒤 "무엇을 했는가"를 보고할 때 이 구조를
쓴다. [[TASK_TEMPLATE]]의 "완료 write-up"이 TASKS.md에 들어가는
한 문단 요약이라면, 이 템플릿은 그 문단을 쓰기 전에 생각을 정리하는
체크리스트다.

## 구조

```
### 변경 파일
- {{path}}(신규/수정)

### 핵심 변경
- {{무엇이 바뀌었는가, 컴포넌트 단위}}

### 설계 결정
- {{왜 이렇게 했는가. 대안이 있었다면 왜 기각했는지}}

### 테스트/검증
- {{어떤 테스트를 추가/실행했고 결과가 어땠는가}}

### 문서 갱신
- {{ARCHITECTURE.md/ADR/Vault 중 갱신한 것}}
```

## 사용 방법

1. 구현이 끝난 직후, 커밋하기 전에 이 5개 절을 짧게 채운다.
2. "핵심 변경"과 "설계 결정"만 추려 [[TASK_TEMPLATE]]의 완료
   write-up 한 문단으로 압축한다 — 이 템플릿 전체를 TASKS.md에
   그대로 붙여넣지 않는다(Short Prompt Workflow와 동일한 압축
   원칙).
3. 새 최상위 Interface를 추가했다면 [[ADR_TEMPLATE]]도 함께 쓴다.

## 관련 문서

- [[TASK_TEMPLATE]]
- [[ADR_TEMPLATE]]
- [[PROJECT_INDEX]]

## 원문

- 없음(이 문서 자체가 Vault 전용 작성 가이드이며 GitHub에 대응
  원문이 없다 — 결과물은 `.ai/TASKS.md`/커밋 메시지에 반영된다)
