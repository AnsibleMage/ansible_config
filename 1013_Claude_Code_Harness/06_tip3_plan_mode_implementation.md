---
title: "Tip #3 플랜 모드 — Pre-Mortem + 독립 검토 + 편향 대응 구현 가이드"
version: "1.0.0"
created: "2026-04-05"
updated: "2026-04-05"
tags: [claude-code, plan-mode, pre-mortem, independent-review, bias, boris-tip3, hook]
status: completed
type: design
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Boris Tip #3 플랜모드 4요소 중 3+4번 구현 완료

### 다음 작업 (TODO)
- [ ] Windows 회사컴에서 동일 적용
- [ ] 실전 테스트 — plan.md Write 시 Hook 트리거 확인
- [ ] Agent 독립 검토 품질 평가 (허점 3개가 실질적인지)

### 작업 조언
> [!tip] 다음 Claude Code에게
> - Boris 플랜모드 4요소 중 1,2번은 기존 시스템에 이미 있었고, 3,4번을 이 세션에서 구현
> - 핵심 교훈: "도구 투입이 아닌 프레이밍과 구조의 문제" (L1 #4)
> - 편향 대응은 Pre-Mortem + 확신도 + 한계 선언만 채택, 나머지는 의식적으로 안 함
> - plan-review-trigger.sh의 오탐 필터(templates/, .claude/plans/) 확인

---

# Tip #3 플랜 모드 — Pre-Mortem + 독립 검토 + 편향 대응

## 개요

Boris의 플랜 모드 4가지 요소와 04_01/04_02 편향 분석을 종합하여, V5.1.0에 적용한 전체 작업 내역.

### Boris 플랜 모드 4요소 적용 현황

| # | Boris 요소 | 구현 상태 | 구현 방법 |
|---|-----------|----------|----------|
| 1 | 상세 계획 수립 | ✅ 기존 | research.md → plan.md 워크플로우 (§2.6) |
| 2 | Claude가 질문 + 사용자 승인 | ✅ 기존 | Gate 2 (draft/approved/rejected) |
| 3 | "시니어라면 허점은?" | ✅ **이번 구현** | Pre-Mortem Gate |
| 4 | Claude A ≠ Claude B | ✅ **이번 구현** | Hook → Agent 독립 검토 |

---

## Part A: Pre-Mortem Gate (Boris #3 — 시니어 프레이밍)

### 핵심 인사이트

> "검토하라"는 task 지시(동작 1개), "시니어라면"은 identity 프레이밍(추론 전략, 우선순위, 주의 배분 패턴 전체를 조건화)

에이전트 추가가 아니라 **프롬프트 프레이밍**이 답.

### 수정된 파일 (4개)

#### 1. `~/.claude/workflow/templates/plan_template.md` — §5 추가

```markdown
## 5. Pre-Mortem — "시니어라면 허점은?"

> 10년차 시니어 엔지니어가 이 계획을 검토한다면 가장 먼저 의심할 부분은?

### 이 계획이 실패하는 가장 가능성 높은 시나리오 3개
1. [시나리오 1 — 기술적 위험]
2. [시나리오 2 — 설계적 허점]
3. [시나리오 3 — 운영/통합 위험]

### 이 분석이 근본적으로 틀렸다면, 가장 가능성 높은 이유는?
- [1줄 자기 반론]
```

#### 2. `~/.claude/workflow/templates/research_template.md` — §6 추가

```markdown
## 6. Pre-Mortem — 이 분석이 틀렸다면?
- **이 분석이 근본적으로 틀렸다면, 가장 가능성 높은 이유는?**: [1줄]
- **놓쳤을 가능성이 있는 관점**: [1줄]
```

#### 3. `~/.claude/rules/orchestration.md` §2.6 — Pre-Mortem Gate 섹션 추가

Gate 2 직전에:
```markdown
#### Pre-Mortem Gate (plan.md 승인 전 필수)
1. "10년차 시니어 엔지니어라면 이 계획의 허점은?" — 실패 시나리오 3개
2. "이 분석이 근본적으로 틀렸다면?" — 자기 반론 1개
3. plan.md §5 Pre-Mortem 섹션에 기록
4. Pre-Mortem 섹션이 비어있으면 Gate 2 제출 금지
```

#### 4. 체인 스킬 파일 (dev-chain.md, system-design.md) — Step 4에 Pre-Mortem 명시

---

## Part B: 독립 검토 Hook (Boris #4 — Claude A ≠ B)

### 핵심 인사이트

> 같은 세션에서 순차 검토는 의미 없다. LLM의 다음 토큰 예측은 이전 컨텍스트에 조건부. 컨텍스트에 "이 plan이 이러한 이유로 선택되었다"는 정보가 있으면, "이 plan이 틀렸다"는 출력의 확률이 수학적으로 억제된다.

### 해결: Hook → Agent (output-only handoff)

```
plan.md Write 완료
    ↓
[Hook] plan-review-trigger.sh 자동 감지
    ↓
[Hook 주입] "⚠️ 독립 검토 필수 — Agent spawn하라"
    ↓
[아리] Agent spawn (plan.md 경로만 전달, reasoning 차단)
    ↓
[Agent] 새 컨텍스트에서 시니어 검토 (허점 3개 + 실패 시나리오 + 확신도)
    ↓
[아리] 검토 결과 + plan.md를 앤에게 보고 → Gate 2 승인 요청
```

### 신규 파일: `~/.claude/hooks/plan-review-trigger.sh`

```bash
#!/bin/bash
# plan-review-trigger.sh — PostToolUse Hook: plan.md 독립 검토 트리거
# Boris Tip #3+4: "시니어라면 허점은?" + "Claude A ≠ Claude B"
# V1.0 (2026-04-05)

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // .toolName // empty' 2>/dev/null)

# Write 도구만 감지
if [ "$TOOL_NAME" != "Write" ]; then
    exit 0
fi

# 파일 경로 추출
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .toolInput.file_path // empty' 2>/dev/null)
if [ -z "$FILE_PATH" ]; then exit 0; fi

# 오탐 방지 필터
if echo "$FILE_PATH" | grep -q "templates/"; then exit 0; fi
if echo "$FILE_PATH" | grep -q "/.claude/plans/"; then exit 0; fi

# plan*.md 패턴 확인
BASENAME=$(basename "$FILE_PATH")
if ! echo "$BASENAME" | grep -qiE '^plan'; then exit 0; fi
if ! echo "$BASENAME" | grep -qE '\.md$'; then exit 0; fi

# 독립 검토 지시 주입
jq -n --arg path "$FILE_PATH" '{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "⚠️ [독립 검토 필수] plan.md Write 감지 → Agent spawn 필수"
    }
}'
exit 0
```

### settings.json 변경

PostToolUse `Write|Edit` 그룹에 5번째 Hook으로 추가:
```json
{
    "type": "command",
    "command": "/Users/changjaeyou/.claude/hooks/plan-review-trigger.sh"
}
```

### orchestration.md 변경

Pre-Mortem Gate와 Gate 2 사이에 독립 검토 섹션 추가:
```markdown
#### 독립 검토 (plan.md → Agent) — 자동 트리거
- Hook이 plan.md Write 감지 → 독립 Agent 검토 강제
- Agent는 plan.md 파일 경로만 전달 (reasoning 차단)
- 독립 검토 없이 Gate 2 제출 금지
```

---

## Part C: 편향 대응 (04_01/04_02 기반)

### 채택한 것

| 전략 | 구현 | 파일 |
|------|------|------|
| Pre-Mortem 프레이밍 | ✅ plan/research 템플릿 | Part A |
| 확신도 명시 의무 | ✅ 리뷰어 3종 프롬프트 | agents/*-reviewer.md |
| 리뷰어 한계 선언 | ✅ "관점 분화 리뷰" 면책 | agents/*-reviewer.md |

### 의식적으로 안 한 것

| 전략 | 이유 |
|------|------|
| 3-Teammate 완전 분리 | 매번 Teams 오버헤드 과다 |
| 정보 차단 프로토콜 | 일상 작업에 과함 |
| 전체 로드맵식 구현 | 04_02 결론: "투명한 취약성 > 완전한 방어" |

### 리뷰어 확신도 + 한계 선언 (3종 공통)

```markdown
## 확신도 명시 (필수)
확신도: X/10
주요 불확실성: [가장 확신이 낮은 판단 1개]
- 90%+ 확신 시 반증 1개 의무

## 한계 선언 (필수)
> ⚠️ 이 리뷰는 동일 세션 컨텍스트를 공유하는 관점 분화 리뷰입니다.
```

---

## 이 세션의 L1 실수 기록 (4건)

| # | 실수 | 회피법 |
|---|------|--------|
| 1 | 미구현 기능을 "작동 불가"로 오판 | 구현됨/미구현/대체재 3분류 |
| 2 | 앤 교정 후 L1 기록 의무 미이행 | auto-analyze.sh에 교정 감지 Hook 추가 |
| 3 | 복원 후 원본 폴더 삭제 시도 | 삭제는 앤 명시 지시만 |
| 4 | Boris 통찰을 도구 투입으로 단순화 | 프레이밍과 구조의 문제로 접근 |

---

## 관련 문서

### 직접 참조 (Direct Links)
- `01_claude_code_7_best_practices.md` — Boris 7가지 팁 원본
- `04_01_self_evaluation_bias_analysis.md` — 5대 편향 + 5가지 전략
- `04_02_v510_bias_deep_analysis.md` — V5.1.0 편향 심층 분석 (8에이전트)
- `~/.claude/hooks/plan-review-trigger.sh` — 독립 검토 Hook
- `~/.claude/workflow/templates/plan_template.md` — Pre-Mortem 포함 템플릿
- `~/.claude/rules/orchestration.md` §2.6 — 워크플로우 통합

### 역참조 (Backlinks)
- `02_tip2_tip5_implementation_guide.md` — Tip #2+#5 가이드
- `03_tip7_hook_automation_guide.md` — Tip #7 가이드

### 관련 주제 (Topic Links)
- `~/.claude/agents/logic-reviewer.md` — 확신도 + 한계 선언 추가
- `~/.claude/agents/security-reviewer.md` — 동일
- `~/.claude/agents/edge-case-reviewer.md` — 동일
- `~/.claude/rules/lessons-learned.md` — L1 실수 4건

---

## Release Notes

### v1.0.0 (2026-04-05)
- Boris 플랜모드 #3(Pre-Mortem) + #4(독립 검토 Hook) 구현
- 편향 대응: 확신도 명시 + 한계 선언 (리뷰어 3종)
- L1 실수 4건 기록 + auto-analyze.sh 교정 감지 Hook 추가
> **프롬프트 흐름:** "시니어라면 허점은?" 검토 요청 → 앤 교정("도구가 아닌 프레이밍") → Pre-Mortem 즉시 구현 → 앤 아이디어("Hook→Agent 독립 검토") → plan-review-trigger.sh 구현 → 확신도+한계선언 추가
