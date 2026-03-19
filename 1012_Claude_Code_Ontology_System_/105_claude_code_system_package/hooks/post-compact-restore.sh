#!/bin/bash
# post-compact-restore.sh — PostCompact Hook
# C5 Observability Phase 2 Step 9
# /compact 실행 후 작업 상태를 복원하여 additionalContext로 주입

# Teammate 감지 → 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

# C5 로깅: COMPACT_DONE 이벤트
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
echo "$TIMESTAMP | COMPACT_DONE | - | -" >> "$LOG_DIR/$(date +%Y%m%d).log"

# 최근 메모리 파일 3개 찾기
MEMORY_DIR="$HOME/.claude/projects/-Users-changjaeyou/memory"
RECENT_MEMORIES=""
if [ -d "$MEMORY_DIR" ]; then
    RECENT_FILES=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -3)
    for f in $RECENT_FILES; do
        BASENAME=$(basename "$f" .md)
        # frontmatter에서 name 추출
        NAME=$(grep -m1 '^name:' "$f" 2>/dev/null | sed 's/^name: *//')
        if [ -z "$NAME" ]; then
            NAME="$BASENAME"
        fi
        RECENT_MEMORIES="${RECENT_MEMORIES}- ${BASENAME}: ${NAME}
"
    done
fi

# TODO 추출 (MEMORY.md에서)
MEMORY_INDEX="$MEMORY_DIR/MEMORY.md"
TODO_ITEMS=""
if [ -f "$MEMORY_INDEX" ]; then
    TODO_ITEMS=$(grep -E '^\- \[ \]' "$MEMORY_INDEX" 2>/dev/null | head -5)
fi

# 복원 메시지 조립
RESTORE_MSG="
## Compact 후 작업 복원

> [!info] /compact가 실행되어 이전 대화가 압축되었습니다.

### 최근 메모리 (참고용)
${RECENT_MEMORIES:-메모리 파일 없음}
### 작업 계속
이전 작업에서 이어서 진행합니다. 필요 시 메모리를 조회하세요.
"

# additionalContext 주입
jq -n --arg ctx "$RESTORE_MSG" '{
    "hookSpecificOutput": {
        "hookEventName": "PostCompact",
        "additionalContext": $ctx
    }
}'

exit 0
