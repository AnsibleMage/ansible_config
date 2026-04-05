---
title: "AI 코딩 에이전트 자기평가 편향 분석 — 계획/개발/리뷰 일원화 시 품질 저하 문제와 개선 전략"
version: "1.0.0"
created: "2026-04-05"
updated: "2026-04-05"
tags: [claude-code, harness, bias, self-evaluation, agent-teams, quality]
status: completed
type: research
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Harness_Research 폴더 문서 8종에서 편향성/품질 저하 관련 내용 추출 및 체계화

### 다음 작업 (TODO)
- [ ] 현재 V5.1.0 체인의 검증 루프와 본 문서의 전략 대비 GAP 분석
- [ ] Agent Teams 기반 Plan-Execute-Verify 실전 적용 테스트

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 Harness_Research 폴더 리서치 결과에서 "편향성으로 인한 품질 저하" 부분만 추출한 분석 문서
> - 핵심 참조: `Harness_Utilization_Plan.md` (편향 매트릭스), `07_Claude_Code_Agent_System_Analysis.md` (패턴 A/B/C)
> - V5.1.0의 검증 루프(MAX 3) + 3종 리뷰어가 이미 부분적으로 대응하고 있음
> - Agent Teams 적용은 아직 실전 테스트 미완 — 구조적 해결의 핵심

---

# AI 코딩 에이전트 자기평가 편향 분석

## 개요

동일한 AI 모델(Claude)이 **계획(Plan) → 개발(Execute) → 리뷰(Verify)**를 전부 수행할 때 발생하는 **자기평가 편향(Self-Evaluation Bias)** 문제와, Harness_Research 문서들에서 도출된 5가지 개선 전략을 정리한다.

### 분석 메타정보

| 항목 | 내용 |
|------|------|
| **분석 대상** | Harness_Research 폴더 문서 8종 |
| **분석 방법** | 키워드 탐색(bias, 편향, self-praise, 자기평가) → 컨텍스트 확인 → 체계화 |
| **핵심 발견** | 5대 편향 유형 + 5가지 개선 전략 + 수치적 효과 |

---

## 1. 문제 정의: Self-Praise Bias

### 1.1 핵심 문제

동일 모델이 코드를 생성하고, 그 코드를 스스로 리뷰하면 **과도하게 긍정적으로 평가**하는 현상.

> **Evaluator Bias**: Generator가 만든 결과를 자신이 평가할 때 과도하게 긍정적 평가
> — `Report_01_anthropic_harness_analysis.md`:54

> GAN 스타일 반복으로 self-praise bias 제거 및 task quality 향상
> — `Harness_Elements_Consolidated.md`:25

### 1.2 구체적 메커니즘

같은 세션에서 Plan → Execute → Verify를 수행하면:

```
[같은 컨텍스트]
Planner가 설계 → 같은 모델이 구현 → 같은 모델이 리뷰
                                      ↑
                              설계 의도를 알고 있으므로
                              "의도대로 구현됨" = "좋다"로 판단
                              (실제 품질과 무관)
```

이것이 피해야 할 안티패턴으로 명시됨:

> **피해야 할 것**: Evaluator without skeptical bias control
> — `Report_01_anthropic_harness_analysis.md`:1420

---

## 2. 5대 편향 유형

`Harness_Utilization_Plan.md`:944-952에서 체계적으로 정리된 편향 매트릭스:

| # | 편향 유형 | 문제 상황 | 설명 |
|---|----------|----------|------|
| 1 | **Confirmation Bias** | Planner가 자신의 설계만 검증 | 자기 가설에 맞는 증거만 찾음 |
| 2 | **Anchoring Bias** | Executor가 첫 설계에 고착 | 초기 정보에 과도하게 의존 |
| 3 | **Authority Bias** | Planner의 "이렇게 하자"만 따름 | 계획자의 결정을 무비판적 수용 |
| 4 | **Self-serving Bias** | "내 구현이 좋다"고 평가 | 자기 산출물에 대한 과대평가 |
| 5 | **Dunning-Kruger** | "충분하다"고 자기평가 | 능력 한계를 인식하지 못함 |

### 2.1 앵커링 편향의 구체적 발생 경로

`Harness_Utilization_Plan.md`:826-841에서 위험한 방식과 안전한 방식을 대비:

```
🚫 위험한 방식 (context sharing):
  Leader 세션:
    - [Planner와 모든 대화 기록 포함]
    - Executor 생성: Planner 정보 + 대화 기록 모두 전달
    → Executor가 Planner의 결정에 영향받음 (앵커링 편향)

✅ 안전한 방식 (output-only handoff):
  Leader 세션:
    - Planner 완료: 산출물만 추출
      ├─ requirements.md (요구사항만, "누가" 정보 X)
      ├─ architecture.md (설계만, "왜" 과정 X)
      └─ plan.md (계획만, Planner의 생각 과정 X)
    - Executor 생성: 산출물만 전달
    → Executor가 산출물 기반 독립 판단
```

---

## 3. 개선 전략 5가지

### 전략 A: Agent Teams 구조적 분리

**출처**: `07_Claude_Code_Agent_System_Analysis.md`:187-240

Agent Teams는 **구조적으로 독립성을 강제**한다:

1. **컨텍스트 격리**: 각 팀원은 독립 컨텍스트. 리더 대화 기록 미전달.
2. **역할 분리**: 계획자 팀원 ≠ 실행자 팀원 ≠ 검증자 팀원
3. **정보 차단**: 팀원 간 정보는 **명시적 메시지**로만 전달 (암묵적 공유 없음)
4. **Plan Approval**: 계획과 실행 사이에 승인 게이트 강제

> Subagent는 "같은 세션 안에서 분리"였지만, Agent Teams는 "아예 다른 인스턴스로 분리". 이것이 진정한 의미의 독립성.
> — `07_Claude_Code_Agent_System_Analysis.md`:196

**3가지 실행 패턴**:

| 패턴 | 이름 | 핵심 효과 | 출처 (라인) |
|------|------|----------|-----------|
| A | Plan-Execute-Verify 완전 분리 | 각 단계를 완전히 다른 인스턴스가 수행 | :200-216 |
| B | 경쟁적 검증 (Adversarial Review) | 상호 반박을 견딘 가설만 수용 → 앵커링 편향 구조적 제거 | :218-227 |
| C | 교차 검증 리뷰 | 각 검토자가 다른 관점만 담당 → 편향 없는 다각적 검토 | :230-240 |

### 전략 B: Skeptical Evaluator Mode

**출처**: `Harness_Elements_Consolidated.md`:112-116

Evaluator가 **명시적으로 비판적 태도**를 취하도록 강제:

- **반드시 3개 이상 문제점 찾기** 규칙
- Quality threshold 설정 (점수 < 0.7이면 재작업)
- Generator 제안을 무조건 수용하지 않음
- Recursive improvement loop: threshold까지 자동 개선

> Evaluator prompt: "반드시 3개 이상 문제점 찾기". Quality threshold 설정 (점수 < threshold이면 재작업).
> — `Harness_Elements_Consolidated.md`:116

### 전략 C: 3중 검증 체계 (Hook 기반 외부 검증)

**출처**: `07_Claude_Code_Agent_System_Analysis.md`:243-254

```
Agent Teams (내부 독립성)
  + TaskCompleted Hook (외부 품질 게이트)
  + TeammateIdle Hook (외부 완료 검증)
  = 3중 검증 체계

  1차: 팀원 자체 완료 판단 (실행자 관점)
  2차: 다른 팀원의 독립 검증 (팀 내 독립성)
  3차: Hook 스크립트의 자동 검증 (시스템 수준 독립성)
```

핵심은 **실행자가 아닌 외부 스크립트**가 품질을 판단한다는 점:

> Hooks는 **독립적 검증 레이어**로 기능. 팀원(실행자)이 아닌 외부 스크립트(검증자)가 품질을 판단.
> — `07_Claude_Code_Agent_System_Analysis.md`:123

### 전략 D: Devil's Advocate 에이전트

**출처**: `.claude_harness/agents/devils-advocate.md`

의도적 반론 제기 에이전트로 확증 편향을 구조적으로 차단:

1. **모든 결론에 반론 제기**: "정말 그런가? 반대 증거는?"
2. **가정 도전**: "이 가정이 틀렸다면?"
3. **대안 제시**: "다른 접근법은 없는가?"
4. **편향 탐지**: "확증 편향에 빠진 것은 아닌가?"

활용 패턴:
- **경쟁적 검증**: 다른 가설들과 상호 반박 시도
- **Plan 검증**: "이 계획의 최악의 시나리오는?"
- **아키텍처 도전**: "모놀리스가 이 규모에서 더 나은 이유 3가지"

### 전략 E: 자기평가 금지 원칙

**출처**: `.claude_harness/CLAUDE.md`:38, 53-56

> **자기평가 편향 제거**: Plan/Execute/Verify는 반드시 다른 Agent가 수행한다.

구체적 규칙:
1. **3-Teammate 분리**: Planner(plan mode) ≠ Executor(auto mode) ≠ Verifier(read-only)
2. **정보 차단**: 산출물만 전달, 작성자 정보·과정·시행착오 제거
3. **자기평가 금지**: Planner는 설계를 평가하지 않고, Executor는 코드를 평가하지 않음
4. **Skeptical Evaluator**: Verifier는 최소 3개 이상 문제점 필수 발견

Executor 에이전트에도 명시적 제약:
> ❌ 자기 평가 금지 (검증은 Verifier의 영역)
> — `.claude_harness/agents/executor.md`:104

---

## 4. 수치적 효과

`Harness_Utilization_Plan.md`:1161-1166에서 독립성 달성 현황:

| 항목 | 기존 (체인만) | Agent Teams 적용 후 | 개선율 |
|------|------------|-------------------|--------|
| Plan vs Execute 분리 | 70% | 90% | +20%p |
| Execute vs Verify 분리 | 90% | 98% | +8%p |
| **자기평가 편향 제거** | **60%** | **20%** | **-40%p** (낮을수록 좋음) |
| 정보 차단 효과 | 50% | 95% | +45%p |

편향 제거 방식별 기여도:

| 메커니즘 | 자기평가 편향 제거 기여 | 출처 |
|---------|---------------------|------|
| Agent Teams (구조적 강제) | 20% | :1165 |
| 규칙 기반 (CLAUDE.md 지시) | 60% | :1165 |
| Hook (외부 검증) | 보조 | :543 |

> Agent Teams의 구조적 강제(20%)가 규칙 기반(60%)보다 3배 효과적.
> 숫자가 낮을수록 편향이 적으므로, 구조적 접근이 압도적으로 우수.

---

## 5. 전략 간 관계 및 적용 우선순위

```
[구조적 해결 — 가장 효과적]
  전략 A: Agent Teams 분리 ─────────┐
  전략 E: 자기평가 금지 원칙 ────────┤
                                    ├→ 편향 20% (구조적 강제)
[프로세스적 해결]                     │
  전략 B: Skeptical Evaluator ──────┤
  전략 D: Devil's Advocate ─────────┘
                                    
[시스템적 해결]                       
  전략 C: 3중 검증 (Hook) ──────────→ 외부 검증 레이어
```

| 우선순위 | 전략 | 현재 V5.1.0 반영 상태 | 비고 |
|---------|------|---------------------|------|
| 1 | A: Agent Teams 분리 | 설정 있음, 실전 미적용 | 가장 효과적이나 오버헤드 존재 |
| 2 | B: Skeptical Evaluator | 3종 리뷰어 + 검증 루프 MAX 3으로 부분 반영 | 추가 개선 가능 |
| 3 | E: 자기평가 금지 | 메모리 격리 규칙으로 부분 반영 | 체인 내 역할 분리는 미완 |
| 4 | C: 3중 검증 | Hook 8/12 활성화 | 구조 있음, 검증 로직 보강 가능 |
| 5 | D: Devil's Advocate | 에이전트 정의만 존재 | 체인에 통합 미완 |

---

## 6. 최종 결론

> "구조적 Plan-Execute-Verify 독립성"은 **Agent Teams를 Primary 메커니즘으로 사용**할 때 가장 효과적으로 달성된다. 완전히 다른 인스턴스, 격리된 컨텍스트, 명시적 메시지 기반 통신이 자기평가 편향을 구조적으로 제거한다.
> — `Harness_Utilization_Plan.md`:1420

**핵심 교훈**: 규칙("편향 없이 리뷰하라")보다 **구조**("아예 다른 인스턴스에서 리뷰하게 하라")가 3배 효과적이다.

---

## 관련 문서

### 직접 참조 (Direct Links)
- `Harness_Utilization_Plan.md` — 5대 편향 매트릭스(§3.6), 컨텍스트 격리(§3.4), 독립성 수치(§7.1)
- `07_Claude_Code_Agent_System_Analysis.md` — Agent Teams 패턴 A/B/C(§1.7), 3중 검증(§1.7.4)
- `Report_01_anthropic_harness_analysis.md` — Self-praise bias 정의(§2.1.3), Skeptical Evaluator(§3.1.2)
- `Harness_Elements_Consolidated.md` — PGE 3-Agent GAN 루프(#1), Skeptical Mode(#14)
- `Harness_Elements_Extraction.md` — 미반영 요소 추출(§1.A)
- `.claude_harness/CLAUDE.md` — 자기평가 금지 원칙(Harness 섹션)
- `.claude_harness/agents/devils-advocate.md` — 비판적 검증 에이전트 전체
- `.claude_harness/agents/executor.md` — 자기 평가 금지 제약(:104)

### 역참조 (Backlinks)
- `02_tip2_tip5_implementation_guide.md` — 검증 루프 + Boris 1순위 팁 (편향 개선의 실전 적용)
- `03_tip7_hook_automation_guide.md` — Hook 기반 외부 검증 (전략 C의 구현체)

### 주제 연결 (Topic Links)
- `~/.claude/rules/orchestration.md` §2.4 — 검증 루프 프로토콜 (MAX 3)
- `~/.claude/rules/orchestration.md` §2.5 — Agent Teams 통합

---

## Release Notes

### v1.0.0 (2026-04-05)
- Harness_Research 폴더 문서 8종에서 편향성/품질 저하 관련 내용 추출
- 5대 편향 유형 + 5가지 개선 전략 + 수치적 효과 체계화

**앤의 원본 프롬프트**:
> /Users/changjaeyou/Documents/AnsibleMage/Harness_Research 폴더의 문서내용을 분석하고 클로드코드가 계획/ 개발 / 리뷰를 전부 수행했을때 편향성을 보여 품질이 저하되는것과 이를 개선하기 위한 전략을 이 나온 부분 찾아서 알려줘
> 분석결과를 /Users/changjaeyou/Documents/AnsibleMage/ansible_config/1013_Claude_Code_Harness 폴더에 신규 문서로 저장해줘
