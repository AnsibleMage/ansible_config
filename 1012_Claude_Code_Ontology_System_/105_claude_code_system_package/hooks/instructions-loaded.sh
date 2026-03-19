#!/bin/bash
# InstructionsLoaded Hook: 규칙 파일 로딩 감사 로그
# V1.0 (2026-03-15)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')
MEMORY_TYPE=$(echo "$INPUT" | jq -r '.memory_type // empty')
LOAD_REASON=$(echo "$INPUT" | jq -r '.load_reason // empty')

# 로깅
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
echo "[$(date +%Y-%m-%d\ %H:%M)] InstructionsLoaded | file=$FILE_PATH | type=$MEMORY_TYPE | reason=$LOAD_REASON" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

exit 0
