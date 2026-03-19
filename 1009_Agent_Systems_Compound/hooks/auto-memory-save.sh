#!/bin/bash
# Claude Code Stop Hook - 자동 메모리 저장
# 매 응답 완료 시 메모리 저장 지시

STATE_FILE="/tmp/claude_memory_last_save"
COOLDOWN=30  # 30초 쿨다운 (무한 루프 방지)

# stdin 읽기 (Stop 훅 입력)
INPUT=$(cat)

# 마지막 저장 후 쿨다운 시간 이내면 스킵 (무한 루프 방지)
if [ -f "$STATE_FILE" ]; then
    LAST_SAVE=$(cat "$STATE_FILE" 2>/dev/null || echo "0")
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_SAVE))
    if [ "$DIFF" -lt "$COOLDOWN" ]; then
        # 쿨다운 중 - 일반 종료 (block 안 함)
        exit 0
    fi
fi

# 현재 시간 기록
date +%s > "$STATE_FILE"

# Claude에게 메모리 저장 지시 (decision: block으로 계속 실행)
cat << 'EOF'
{
  "decision": "block",
  "hookSpecificOutput": {
    "additionalContext": "\n\n🧠 [AUTO-MEMORY-SAVE]\n이 작업을 ~/.memory/에 저장해주세요.\n\n저장 형식:\n- 파일명: YYMM_SEQ_keyword.md\n- 체인/에이전트/스킬/도구 사용 내역 포함\n- 간결하게 핵심만 기록\n\n저장 후 '💾 메모리 저장 완료'라고 알려주세요."
  }
}
EOF
