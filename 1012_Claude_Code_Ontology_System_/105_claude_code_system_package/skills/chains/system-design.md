---
name: system-design-chain
description: 시스템 설계, 아키텍처, CLAUDE.md 업데이트, 체인 개선에 사용. "시스템 설계", "아키텍처", "체인 개선" 키워드에 반응. 메타 작업 자동 감지. 대규모 작업이므로 research→plan 워크플로우 + 인간 승인 필수.
user-invocable: false
---

# SystemDesignChain (A) — Effort: HIGH

> 모든 에이전트 완전 실행. 탐색 범위 제한 금지. 깊이 있는 분석 필수.
> 대규모 체인 — research.md + plan.md + 인간 승인 게이트 필수.

## 체인 패턴

```
(Explore[S] ∥ Read[-]) → (system_architect[O] ∥ problem_reframer[O])
→ [research.md 생성] → [plan.md 생성 + 인간 승인 게이트(필수)]
→ solution_innovator[O] → integrated_sage[O] → (Edit[-] ∥ quality_reviewer[S])
```

## 단계 목록 (임의 축약 금지)

1. **[병렬]** 코드베이스 탐색 (`Explore[opus]`) + 관련 파일 읽기 (`Read[main]`)
2. **[병렬]** 시스템 아키텍처 설계 (`system_architect[opus]`) + 관점 전환 (`problem_reframer[opus]`)
3. **[순차]** **research.md 생성** — Step 1-2 결과를 `~/.claude/workflow/templates/research_template.md` 기반으로 작성. Gate 1 검증 (`gate1_checker.sh`)
4. **[순차]** **plan.md 생성 + 인간 승인 게이트 (필수)** — research.md 기반으로 계획 작성 (Status: draft). 앤 검토 → approved 후 다음 단계 진행. SystemDesignChain은 항상 대규모이므로 인간 승인 필수.
5. **[순차]** 혁신 솔루션 도출 (`solution_innovator[opus]`)
6. **[순차]** 통합 지혜 정리 (`integrated_sage[opus]`)
7. **[병렬]** 파일 수정 (`Edit[main]`) + 코드 리뷰 (`quality_reviewer[opus]`)

## 복잡도 분기

- SystemDesignChain은 **항상 대규모**로 분류
- research.md + plan.md + 인간 승인 게이트 **필수**
- 단순 작업은 이 체인을 선택하지 않음 (HotfixChain 또는 직행)

## 트리거 조건

- "시스템 설계", "아키텍처", "체인 개선"
- 메타 작업 자동 감지 (CLAUDE.md 수정, Hook 개선 등)

## 주의사항

- **임의 축약 금지**: 정의된 7단계를 모두 실행한다
- "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
- 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
- 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다

## Pre-execution Declaration

```
📋 체인 구성: SystemDesignChain [HIGH] → Explore∥Read → architect∥reframer → research.md → plan.md+gate(필수) → innovator → sage → Edit∥reviewer
```
