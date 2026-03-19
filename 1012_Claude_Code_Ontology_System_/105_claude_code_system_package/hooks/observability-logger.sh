#!/bin/bash
# ~/.claude/hooks/observability-logger.sh
# PostToolUse Hook: 모든 도구 사용 후 1줄 로그 append
# C5 Observability — Phase 0 (최소 구현)
# V1.1 (2026-03-16): 필드명 수정 toolName→tool_name, toolResult→tool_response

LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y%m%d).log"

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null)
TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_response // "OK"' 2>/dev/null)

if echo "$TOOL_RESULT" | grep -qi "error\|fail\|exception"; then
    STATUS="ERR"
else
    STATUS="OK"
fi

# 체인 상태 파일에서 현재 체인 읽기 (없으면 "-")
CHAIN_STATE_FILE="/tmp/claude_current_chain.txt"
if [ -f "$CHAIN_STATE_FILE" ]; then
    CHAIN=$(cat "$CHAIN_STATE_FILE")
else
    CHAIN="-"
fi

# Agent 도구인 경우 서브에이전트 타입 추출
AGENT_NAME="$TOOL_NAME"
if [ "$TOOL_NAME" = "Agent" ]; then
    SUBAGENT=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // .tool_input.agent // "agent"' 2>/dev/null)
    if [ -n "$SUBAGENT" ] && [ "$SUBAGENT" != "null" ]; then
        AGENT_NAME="$SUBAGENT"
    fi
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
echo "$TIMESTAMP | $CHAIN | ${AGENT_NAME}[${STATUS}] | -" >> "$LOG_FILE"

exit 0
