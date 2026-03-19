---
name: dev-chain
description: 일반 소프트웨어 개발, 코딩, TDD. "개발", "구현", "코딩", "기능 추가" 키워드에 반응. 중규모+ 작업 시 research→plan 워크플로우 포함.
user-invocable: false
---

# DevChain (D) — Effort: MEDIUM

> 요구사항→탐색→연구→계획→구현→리뷰. 중규모 이상 작업에서 research/plan 필수.

## 체인 패턴

```
requirements_analyst[O] → (system_architect[O] ∥ Explore[O] ∥ Context7[∥])
→ [research.md 생성] → [plan.md 생성 + 승인 게이트]
→ code_developer[S] → (quality_reviewer[S] ∥ Bash[테스트][-])
```

## 단계 목록 (임의 축약 금지)

1. **[순차]** 요구사항 분석 (`requirements_analyst[opus]`)
2. **[병렬]** 아키텍처 설계 (`system_architect[opus]`) + 코드 탐색 (`Explore[opus]`) + 라이브러리 조사 (`Context7`)
3. **[순차]** **research.md 생성** — Step 2 결과를 `~/.claude/workflow/templates/research_template.md` 기반으로 작성. Gate 1 검증 (`gate1_checker.sh`)
4. **[순차]** **plan.md 생성 + 인간 승인 게이트** — research.md 기반으로 계획 작성 (Status: draft). 앤 검토 → approved 후 다음 단계 진행
5. **[순차]** TDD 구현 (`code_developer[opus]`) — 승인된 plan.md 기반으로 기계적 구현
6. **[병렬]** 코드 리뷰 (`quality_reviewer[opus]`) + 테스트 실행 (`Bash[테스트]`)
7. **[순차]** plan.md 체크리스트 완료 확인 — 모든 `- [ ]`가 `- [x]`로 변경 확인

## 복잡도 분기

| 복잡도 | 기준 | 워크플로우 | 인간 게이트 |
|--------|------|-----------|-----------|
| 단순 | 한 줄 수정, Q&A | Step 1→5→6 직행 (research/plan 생략) | 불필요 |
| 중규모 | 파일 3개+ 수정, 새 기능 | 전체 7단계 | 조건부 (명시적 거부 없으면 진행) |
| 대규모 | 아키텍처 변경, 신규 시스템 | 전체 7단계 | 필수 (명시적 승인 필요) |

## 트리거 조건

- "개발해줘", "구현", "코딩", "기능 추가", "만들어줘"
- DevChain 키워드 감지 시 자동 선택

## 주의사항

- **임의 축약 금지**: 정의된 7단계를 모두 실행한다
- "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
- 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
- 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다
- **Simple Task Exception**: 단순 Q&A, 한 줄 수정은 체인 자체를 생략

## Pre-execution Declaration

```
📋 체인 구성: DevChain [MEDIUM] → requirements → architect∥Explore∥Context7 → research.md → plan.md+gate → developer → reviewer∥test → checklist
```
