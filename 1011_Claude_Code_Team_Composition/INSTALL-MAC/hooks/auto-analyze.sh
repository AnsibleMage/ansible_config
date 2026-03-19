#!/bin/bash
# Claude Code UserPromptSubmit Hook V3.0
# 1. Agent Teams teammate 감지 → 스킵
# 2. 이전 프롬프트 자동 메모리 저장 지시
# 3. 현재 프롬프트 4-Layer 분석
#
# V3.0 (2026-02-06): Agent Teams 호환성 추가
# - teammate 세션 감지 시 4-Layer 분석 및 메모리 저장 지시 스킵
# - 상태 파일 SESSION_ID별 분리

# stdin에서 JSON 입력 받기
INPUT=$(cat)

# 프롬프트 추출
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')

# 프롬프트가 비어있으면 종료
if [ -z "$PROMPT" ]; then
    exit 0
fi

# === Agent Teams teammate 감지 ===
# teammate 세션에서는 4-Layer 분석 및 메모리 저장 지시를 스킵
# 감지 방법: 환경변수 또는 teams 디렉토리 내 활성 팀 존재 여부
IS_TEAMMATE=false

# 방법 1: 환경변수 직접 확인
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    IS_TEAMMATE=true
fi

# 방법 2: teammateMode가 설정된 상태에서 Lead가 아닌 경우
if [ -n "$CLAUDE_CODE_AGENT_TEAM_NAME" ] && [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" != "lead" ] && [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" != "" ]; then
    IS_TEAMMATE=true
fi

# teammate면 최소 출력만 하고 종료
if [ "$IS_TEAMMATE" = true ]; then
    echo "[$(date)] TEAMMATE DETECTED - role=$CLAUDE_CODE_AGENT_TEAM_ROLE team=$CLAUDE_CODE_AGENT_TEAM_NAME session=$SESSION_ID" >> /tmp/claude_teammate_hook.log
    jq -n '{
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "🤖 [TEAMMATE MODE] 4-Layer 분석 스킵 - Lead 세션에서만 실행됩니다."
        }
    }'
    exit 0
fi

# === 이전 프롬프트 메모리 저장 시스템 ===
# V3.0: SESSION_ID별 상태 파일 분리 (Agent Teams 동시성 보호)
if [ -n "$SESSION_ID" ]; then
    STATE_FILE="/tmp/claude_prev_prompt_state_${SESSION_ID}.json"
else
    STATE_FILE="/tmp/claude_prev_prompt_state.json"
fi
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
        ANALYZER="$HOME/.claude/scripts/prompt_analyzer.py"
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
