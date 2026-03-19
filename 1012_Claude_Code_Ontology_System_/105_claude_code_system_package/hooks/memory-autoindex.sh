#!/bin/bash
# memory-autoindex.sh — PostToolUse Hook: 메모리 파일 자동 인덱싱
# Write/Edit 도구로 ~/.claude/memory/ 에 파일 생성/수정 시
# 백그라운드에서 Qdrant 인덱싱 자동 실행
#
# Phase 3 개선: 메모리 저장 → [자동] → Qdrant 벡터화
# 이전: 메모리 저장 → [끊김] → 수동 인덱싱 필요

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // .toolName // empty' 2>/dev/null)

# Write 또는 Edit 도구인지 확인
if [ "$TOOL_NAME" != "Write" ] && [ "$TOOL_NAME" != "Edit" ]; then
    exit 0
fi

# 파일 경로 추출
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .toolInput.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# memory/ 디렉토리 파일인지 확인
if ! echo "$FILE_PATH" | grep -q "/.claude/memory/"; then
    exit 0
fi

# .md 파일인지 확인
if ! echo "$FILE_PATH" | grep -qE "\.md$"; then
    exit 0
fi

# MEMORY.md (인덱스 파일)는 인덱싱 제외
if echo "$FILE_PATH" | grep -q "MEMORY.md"; then
    exit 0
fi

# Qdrant 상태 확인 (1초 타임아웃)
if ! curl -s --max-time 1 http://localhost:6333/healthz > /dev/null 2>&1; then
    exit 0
fi

# 백그라운드에서 인덱싱 실행 (nohup — Hook 즉시 반환)
VENV_PYTHON="$HOME/.claude/venv/bin/python3"
INDEXER="$HOME/.claude/scripts/memory_indexer.py"

if [ -f "$VENV_PYTHON" ] && [ -f "$INDEXER" ]; then
    nohup "$VENV_PYTHON" "$INDEXER" --file "$FILE_PATH" --no-relations \
        >> /tmp/memory_autoindex.log 2>&1 &
fi

exit 0
