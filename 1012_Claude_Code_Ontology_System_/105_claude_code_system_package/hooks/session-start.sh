#!/bin/bash
# SessionStart Hook: 세션 시작 시 메모리 자동 로드
# V1.0 (2026-03-15)

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')
IS_RESUME=$(echo "$INPUT" | jq -r '.isResume // false')

# Teammate 세션 감지 → 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

MEMORY_DIR="$HOME/.claude/memory"
if [ ! -d "$MEMORY_DIR" ]; then
    exit 0
fi

# 컨텍스트 추적 상태 파일 초기화 (C8 연계)
STATE_FILE="/tmp/claude_context_tracker_${SESSION_ID}.json"
echo '{"turns": 0, "toolCalls": 0, "agentCalls": 0, "fileReads": 0}' > "$STATE_FILE"

# V5.0: 메모리 리콜 서버 자동 시작 (C1)
# Qdrant 가동 중이고 서버가 미실행일 때만 시작
if curl -s --max-time 1 http://localhost:6333/healthz > /dev/null 2>&1; then
    if ! curl -s --max-time 1 http://localhost:18765/health > /dev/null 2>&1; then
        nohup "$HOME/.claude/venv/bin/python3" "$HOME/.claude/scripts/memory_recall_server.py" \
            > /tmp/memory_recall_server.log 2>&1 &
    fi
fi

# 최근 메모리 3개 로드
RECENT_MEMORIES=""
MEMORY_FILES=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -3)

if [ -n "$MEMORY_FILES" ]; then
    RECENT_MEMORIES="
## 최근 메모리 (자동 로드)
"
    for FILE in $MEMORY_FILES; do
        FILENAME=$(basename "$FILE")
        TITLE=$(head -10 "$FILE" | grep -E '^# ' | head -1 | sed 's/^# //')
        if [ -z "$TITLE" ]; then TITLE="$FILENAME"; fi
        SUMMARY=$(grep -A1 '요약' "$FILE" 2>/dev/null | tail -1 | head -c 100)
        if [ -z "$SUMMARY" ]; then
            SUMMARY=$(grep -v '^#\|^-\|^>\|^$\|^---' "$FILE" | head -2 | tr '\n' ' ' | head -c 100)
        fi
        RECENT_MEMORIES="$RECENT_MEMORIES- **$TITLE** ($FILENAME): $SUMMARY
"
    done
fi

# 이전 세션 TODO 로드 (resume 시)
TODO_CONTEXT=""
if [ "$IS_RESUME" = "true" ]; then
    LATEST_FILE=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_FILE" ]; then
        TODOS=$(grep -E '^\- \[ \]' "$LATEST_FILE" 2>/dev/null | head -5)
        if [ -n "$TODOS" ]; then
            TODO_CONTEXT="
## 이전 세션 미완료 TODO
$TODOS
"
        fi
    fi
fi

if [ -n "$RECENT_MEMORIES" ] || [ -n "$TODO_CONTEXT" ]; then
    CONTEXT="$RECENT_MEMORIES$TODO_CONTEXT"
    jq -n --arg ctx "$CONTEXT" '{
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": $ctx
        }
    }'
fi

exit 0
