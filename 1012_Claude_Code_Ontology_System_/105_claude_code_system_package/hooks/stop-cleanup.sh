#!/bin/bash
# Stop Hook: 작업 완료 시 컨텍스트 자동 관리
# V2.0 (2026-03-15) — C8 Quality-First + C5 Observability

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')
STOP_REASON=$(echo "$INPUT" | jq -r '.stopReason // "end_turn"')

# Teammate 감지 → 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

# C5 로깅
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
echo "$TIMESTAMP | Stop | reason=$STOP_REASON | session=$SESSION_ID" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

# 1. 체인 완료 검증
PROGRESS_FILE="/tmp/claude_chain_progress_${SESSION_ID}.json"
if [ -f "$PROGRESS_FILE" ]; then
    IS_COMPLETE=$(jq -r '.is_complete // true' "$PROGRESS_FILE" 2>/dev/null)
    if [ "$IS_COMPLETE" = "false" ]; then
        CHAIN=$(jq -r '.chain // "unknown"' "$PROGRESS_FILE")
        REMAINING=$(jq -r '.remaining_steps | join(", ")' "$PROGRESS_FILE" 2>/dev/null)
        REMAINING_COUNT=$(jq -r '.remaining_steps | length' "$PROGRESS_FILE" 2>/dev/null)
        CONTINUE_MSG="
## 체인 미완료 — 계속 실행

> [!warning] **${CHAIN}** 체인이 완료되지 않았습니다.
> 남은 단계 (${REMAINING_COUNT}개): ${REMAINING}
>
> **임의 축약 금지 원칙**에 따라 체인을 완료하세요.
"
        jq -n --arg ctx "$CONTINUE_MSG" '{
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": $ctx
            }
        }'
        exit 2
    fi
fi

# 2. 컨텍스트 사용량 추정
STATE_FILE="/tmp/claude_context_tracker_${SESSION_ID}.json"
if [ -f "$STATE_FILE" ]; then
    TURN_COUNT=$(jq -r '.turns // 0' "$STATE_FILE" 2>/dev/null)
    TOOL_CALLS=$(jq -r '.toolCalls // 0' "$STATE_FILE" 2>/dev/null)
    AGENT_CALLS=$(jq -r '.agentCalls // 0' "$STATE_FILE" 2>/dev/null)
    FILE_READS=$(jq -r '.fileReads // 0' "$STATE_FILE" 2>/dev/null)

    ESTIMATED_TOKENS=$(( \
        (TURN_COUNT * 2500) + \
        (TOOL_CALLS * 1500) + \
        (AGENT_CALLS * 8000) + \
        (FILE_READS * 3000) \
    ))
    USAGE_PERCENT=$(( (ESTIMATED_TOKENS * 100) / 1000000 ))

    echo "$TIMESTAMP | ContextEstimate | turns=$TURN_COUNT tools=$TOOL_CALLS agents=$AGENT_CALLS files=$FILE_READS estimated=${ESTIMATED_TOKENS}tok (${USAGE_PERCENT}%)" \
        >> "$LOG_DIR/$(date +%Y%m%d).log"

    # 3. 80%+ 시 자동 정리 지시
    if [ "$USAGE_PERCENT" -ge 80 ]; then
        CLEANUP_MSG="
## 컨텍스트 자동 정리 (추정 ${USAGE_PERCENT}%)

> [!warning] 컨텍스트 사용량이 80%를 초과했습니다.
> 추정: 턴 ${TURN_COUNT}회, 도구 ${TOOL_CALLS}회, 에이전트 ${AGENT_CALLS}회, 파일읽기 ${FILE_READS}회 = ~${ESTIMATED_TOKENS} 토큰

### 실행 순서 (반드시 이 순서대로)

**1단계: 품질 자가 검증**
- [ ] 모든 에이전트가 생략 없이 실행되었는가?
- [ ] 분석 깊이가 충분한가? (근본 원인까지 도달)
- [ ] 구조화된 출력인가? (테이블/다이어그램/매트릭스)
- [ ] 다음 세션이 이어받을 수 있는가? (Handoff 갱신)

**2단계: 메모리 상세 저장** (\`/memory-save\`)
아래 내용을 **반드시 포함**하여 메모리에 저장:
- 작업 제목, 완료 항목, 미완료 TODO (체크박스)
- 핵심 결정/인사이트, 생성/수정된 파일 목록
- 다음 세션 조언 (구체적으로)

**3단계: /compact 실행**
메모리 저장 완료 후에만 실행하세요.
"
        jq -n --arg ctx "$CLEANUP_MSG" '{
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": $ctx
            }
        }'
        exit 2
    fi
else
    # 상태 파일 없으면 초기화
    jq -n '{"turns": 0, "toolCalls": 0, "agentCalls": 0, "fileReads": 0}' > "$STATE_FILE"
fi

exit 0
