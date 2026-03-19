# 이전 프롬프트 자동 메모리 저장 시스템 (Hook V2.0)

> **구현일**: 2026-02-04
> **버전**: UserPromptSubmit Hook V2.0
> **CLAUDE.md**: V3.8

---

## 1. 문제 정의

### 기존 시도의 한계

| 방법 | 결과 | 실패 원인 |
|------|------|----------|
| **Stop Hook** | ❌ 실패 | 응답 완료 "후" 실행 → Claude에게 새 지시 불가, `hookSpecificOutput` 미지원 |
| **지침 기반** | △ 불완전 | Claude 재량에 의존, 100% 보장 안 됨 |

### 목표

**"1 프롬프트 = 1 메모리"** 원칙 구현

---

## 2. 해결책: UserPromptSubmit Hook V2.0

### 핵심 발상

```
Stop Hook 문제:
  응답 완료 "후" 실행 → Claude가 이미 응답을 끝냄 → 추가 작업 불가

UserPromptSubmit 해결책:
  새 프롬프트 입력 "전" 실행 → Claude 응답 시작 전 → 지시 주입 가능!

  → "이전 프롬프트와 응답을 메모리에 저장해" 지시를 additionalContext로 주입
  → Claude가 응답 시작 시 이전 대화 저장 후 현재 프롬프트 응답
```

### 시스템 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                    Auto Memory Save Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [프롬프트 #1] ──────────────────────────────────────────┐      │
│       │                                                 │      │
│       ▼                                                 │      │
│  ┌─────────────────────────┐                           │      │
│  │ UserPromptSubmit Hook   │                           │      │
│  │ → 상태 파일에 #1 저장    │                           │      │
│  │ → (이전 없음, 저장 지시 X)│                           │      │
│  └─────────────────────────┘                           │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  Claude 응답 (#1에 대해)                                 │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  [프롬프트 #2] ──────────────────────────────────────────┤      │
│       │                                                 │      │
│       ▼                                                 │      │
│  ┌─────────────────────────┐                           │      │
│  │ UserPromptSubmit Hook   │                           │      │
│  │ → 상태 파일에서 #1 읽기  │                           │      │
│  │ → Claude에게 #1 저장 지시│◄──── additionalContext    │      │
│  │ → 상태 파일에 #2 저장    │                           │      │
│  └─────────────────────────┘                           │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  Claude 응답:                                           │      │
│    1. 💾 이전 대화(#1) 메모리 저장                       │      │
│    2. #2에 대한 응답                                    │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  [프롬프트 #3] ... (반복)                                │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  [마지막 프롬프트]                                       │      │
│       │                                                 │      │
│       ▼                                                 │      │
│  ⚠️ 다음 프롬프트 없음 → 수동 저장 필요                   │      │
│     (/memory-save 또는 직접 저장)                        │      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 구현 상세

### 3.1 스크립트: `~/.claude/hooks/auto-analyze.sh` (V2.0)

```bash
#!/bin/bash
# Claude Code UserPromptSubmit Hook V2.0
# 1. 이전 프롬프트 자동 메모리 저장 지시
# 2. 현재 프롬프트 4-Layer 분석

# stdin에서 JSON 입력 받기
INPUT=$(cat)

# 프롬프트 추출
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')

# 프롬프트가 비어있으면 종료
if [ -z "$PROMPT" ]; then
    exit 0
fi

# === 이전 프롬프트 메모리 저장 시스템 ===
STATE_FILE="/tmp/claude_prev_prompt_state.json"
MEMORY_INSTRUCTION=""

# 이전 프롬프트 상태 확인
if [ -f "$STATE_FILE" ]; then
    PREV_PROMPT=$(jq -r '.prompt // empty' "$STATE_FILE" 2>/dev/null)
    PREV_SESSION=$(jq -r '.sessionId // empty' "$STATE_FILE" 2>/dev/null)
    PREV_TIMESTAMP=$(jq -r '.timestamp // empty' "$STATE_FILE" 2>/dev/null)
    PROMPT_COUNT=$(jq -r '.promptCount // 0' "$STATE_FILE" 2>/dev/null)

    # 같은 세션 내에서 이전 프롬프트가 있으면 메모리 저장 지시
    if [ -n "$PREV_PROMPT" ] && [ "$PREV_SESSION" = "$SESSION_ID" ]; then
        # 10자 미만, 단순 명령어는 저장 제외
        if [ ${#PREV_PROMPT} -ge 10 ] && ! echo "$PREV_PROMPT" | grep -qE '^/[a-z-]+$'; then
            PROMPT_COUNT=$((PROMPT_COUNT + 1))
            MEMORY_INSTRUCTION="
🧠 [AUTO-MEMORY-SAVE] 이전 프롬프트 저장 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 이전 프롬프트: \"${PREV_PROMPT:0:100}...\"
📌 프롬프트 순번: #$PROMPT_COUNT

⚡ 현재 응답 시작 전에 이전 프롬프트와 응답 내용을 메모리에 저장하세요.
   저장 위치: ~/.claude/memory/YYMM_SEQ_keyword.md
   포맷: 기존 메모리 파일 형식 준수

   저장 완료 후 '💾 이전 대화 메모리 저장 완료' 표시하고 현재 프롬프트 응답 진행.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
        fi
    else
        # 새 세션이면 카운트 리셋
        PROMPT_COUNT=0
    fi
else
    PROMPT_COUNT=0
fi

# 현재 프롬프트를 상태 파일에 저장 (다음 턴에 사용)
jq -n \
    --arg prompt "$PROMPT" \
    --arg sessionId "$SESSION_ID" \
    --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --argjson count "$PROMPT_COUNT" \
    '{
        "prompt": $prompt,
        "sessionId": $sessionId,
        "timestamp": $timestamp,
        "promptCount": $count
    }' > "$STATE_FILE"

# === 기존 4-Layer 분석 ===
ANALYSIS=""

# 짧은 프롬프트는 분석 생략 (10자 미만)
if [ ${#PROMPT} -ge 10 ]; then
    # 단순 명령어 패턴이 아니면 분석
    if ! echo "$PROMPT" | grep -qE '^/[a-z-]+$'; then
        ANALYZER="/Users/changjaeyou/.claude/scripts/prompt_analyzer.py"
        if [ -f "$ANALYZER" ]; then
            ANALYSIS=$(python3 "$ANALYZER" "$PROMPT" 2>/dev/null)
        fi
    fi
fi

# === 최종 출력 조합 ===
COMBINED_CONTEXT=""

# 메모리 저장 지시 추가
if [ -n "$MEMORY_INSTRUCTION" ]; then
    COMBINED_CONTEXT="$MEMORY_INSTRUCTION"
fi

# 분석 결과 추가
if [ -n "$ANALYSIS" ]; then
    if [ -n "$COMBINED_CONTEXT" ]; then
        COMBINED_CONTEXT="$COMBINED_CONTEXT

$ANALYSIS"
    else
        COMBINED_CONTEXT="$ANALYSIS"
    fi
fi

# 결과 출력
if [ -n "$COMBINED_CONTEXT" ]; then
    jq -n \
        --arg ctx "$COMBINED_CONTEXT" \
        '{
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": $ctx
            }
        }'
fi

exit 0
```

### 3.2 상태 파일 구조

**위치**: `/tmp/claude_prev_prompt_state.json`

```json
{
  "prompt": "체인 시스템을 업그레이드해줘...",
  "sessionId": "29d7e4df-1750-4b60-a657-f532df77fe84",
  "timestamp": "2026-02-04T12:00:00Z",
  "promptCount": 3
}
```

| 필드 | 설명 |
|------|------|
| `prompt` | 이전 프롬프트 전체 내용 |
| `sessionId` | 세션 UUID (같은 세션 내에서만 저장) |
| `timestamp` | 프롬프트 입력 시간 |
| `promptCount` | 세션 내 프롬프트 순번 |

### 3.3 additionalContext 출력 예시

```
🧠 [AUTO-MEMORY-SAVE] 이전 프롬프트 저장 필요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 이전 프롬프트: "CLAUDE.md의 체인 시스템을 업그레이드해줘. Memory 폴더와 Obsidian Vault를 분석해서..."
📌 프롬프트 순번: #3

⚡ 현재 응답 시작 전에 이전 프롬프트와 응답 내용을 메모리에 저장하세요.
   저장 위치: ~/.claude/memory/YYMM_SEQ_keyword.md
   포맷: 기존 메모리 파일 형식 준수

   저장 완료 후 '💾 이전 대화 메모리 저장 완료' 표시하고 현재 프롬프트 응답 진행.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 4-LAYER PROMPT ANALYSIS
📌 권장 스킬: /docx
📌 권장 에이전트: system_architect
   우선순위: HIGH
```

---

## 4. 저장 제외 조건

| 조건 | 설명 | 이유 |
|------|------|------|
| `길이 < 10자` | 짧은 프롬프트 | 의미 있는 내용 없음 |
| `/command` 형식 | 슬래시 명령어 | 시스템 명령어 |
| `다른 세션` | sessionId 불일치 | 세션 간 분리 |

---

## 5. settings.json 설정

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/changjaeyou/.claude/hooks/auto-analyze.sh"
          }
        ]
      }
    ]
  }
}
```

> 기존 auto-analyze.sh를 그대로 사용 (V2.0으로 업그레이드됨)

---

## 6. CLAUDE.md 변경 사항

### 버전

- V3.7 → V3.8

### UserPromptSubmit Hook 섹션 변경

- V1.0: 4-Layer 분석만
- V2.0: **이전 프롬프트 자동 저장** + 4-Layer 분석

### Change History 추가

```markdown
### V3.8 (2026-02-04)
- ✅ **이전 프롬프트 자동 메모리 저장 시스템 구현**
  - UserPromptSubmit Hook V2.0 업그레이드
  - 새 프롬프트 입력 시 이전 프롬프트+응답 자동 저장 지시
  - 상태 파일: `/tmp/claude_prev_prompt_state.json`
  - 마지막 프롬프트만 수동 저장 필요 (`/memory-save`)
- ✅ **1프롬프트 = 1메모리 원칙** 실현
```

---

## 7. 한계 및 주의사항

### 마지막 프롬프트 처리

```
[프롬프트 #1] → [프롬프트 #2] → [프롬프트 #3] (마지막)
     ↓              ↓              ↓
   저장 지시      저장 지시      ⚠️ 다음 프롬프트 없음
   (#2 입력 시)   (#3 입력 시)   → 수동 저장 필요
```

**해결책**: 세션 종료 전 `/memory-save` 또는 직접 저장 요청

### Claude 재량

- Hook은 "지시"만 전달, 실행은 Claude가 수행
- 명시적이고 구체적인 지시로 높은 준수율 기대
- 100% 보장은 아님 (Stop Hook보다는 훨씬 나음)

---

## 8. 기대 효과

| 지표 | 이전 (지침 기반) | 이후 (Hook V2.0) |
|------|----------------|-----------------|
| **자동화 수준** | 없음 (재량 의존) | Hook으로 자동 지시 |
| **저장 누락** | 빈번 | 마지막 1개만 |
| **일관성** | 낮음 | 높음 (동일 지시) |
| **세션당 누락** | N개 중 다수 | N개 중 1개 (마지막) |

---

## 9. 테스트 방법

### 수동 테스트

```bash
# 1. Claude Code 새 세션 시작
claude

# 2. 첫 번째 프롬프트 입력
> "체인 시스템 분석해줘"

# 3. 두 번째 프롬프트 입력
> "위 분석을 바탕으로 개선안 제시해줘"

# 4. Claude 응답 확인
# → 응답 시작에 "💾 이전 대화 메모리 저장 완료" 표시 확인
# → ~/.claude/memory/ 에 새 파일 생성 확인

# 5. 세션 종료 전 마지막 저장
> "/memory-save"
```

### 상태 파일 확인

```bash
cat /tmp/claude_prev_prompt_state.json | jq .
```

---

## 10. 관련 문서

- [[011_Stop-Hook-Auto-Memory-Save-System]] - Stop Hook 실패 분석
- [[Memory Save Protocol System/README]] - 메모리 저장 프로토콜
- [[An_Profile_and_Chain_Upgrade_Report]] - Cowork 분석 보고서
- [[Chain_System_V2.0_for_CLAUDE]] - 체인 시스템 V2.0

---

*Auto Memory Save Hook V2.0 Implementation - 2026-02-04*
*Developed in Cowork mode (외부에서 Claude Code 개선)*
