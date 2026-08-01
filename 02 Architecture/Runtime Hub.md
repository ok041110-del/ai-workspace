---
tags: [architecture, observability]
type: concept
---

# Runtime Hub

> Map of Content(Milestone 47). Observability/Runtime 관련 산출물을
> 모은다. **실시간 값 자체를 담은 Vault Node는 없다** — StatusLine
> 출력은 휘발성이라 영속 문서로 존재하지 않는다([[Vault Information Architecture]] T03 Node Definition). 이 Hub는 "이 개념이 무엇인가"
> 로만 안내한다.

## Concept

- [[Runtime]]
- [[Observability]]
- [[Guardian]](Runtime이 재사용하는 평가기)

## 실측 근거(Architecture Overview §3.37~3.38)

- StatusLine이 표시하는 것: Claude Runtime(Model/Effort/Context),
  Recommendation 파이프라인 7단계, Git/Guardian/Vault/MCP 실행 환경
- StatusLine이 표시하지 않는 것(정직하게 Not Available): `ruff`/
  `mypy`/Coverage 실시간 상태, MCP 상세 호출 이력, GitHub PR 상태,
  현재 실행 중인 Task

## 관련 문서

- [[Architecture Hub]]
- [[Knowledge Hub]]
- [[Architecture Overview]]
