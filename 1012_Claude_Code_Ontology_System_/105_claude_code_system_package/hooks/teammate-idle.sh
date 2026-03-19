#!/bin/bash
# TeammateIdle Hook: Teammate 유휴 관리
# V1.0 (2026-03-15)
#
# V4.2.1 CLAUDE.md의 자연어 규칙을 코드로 강제 실행:
# - 120초 무응답 → 재활성화 시도 (exit code 2)
# - 300초 정체 → 종료 허용 (exit code 0)

INPUT=$(cat)
TEAMMATE_ID=$(echo "$INPUT" | jq -r '.teammateId // empty')
IDLE_DURATION=$(echo "$INPUT" | jq -r '.idleDuration // 0')
LAST_ACTIVITY=$(echo "$INPUT" | jq -r '.lastActivity // empty')

# 로깅
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
echo "[$(date +%Y-%m-%d\ %H:%M)] TeammateIdle | id=$TEAMMATE_ID | idle=${IDLE_DURATION}s | last=$LAST_ACTIVITY" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

if [ "$IDLE_DURATION" -ge 300 ]; then
    # 300초 이상 정체 → 종료 허용
    jq -n '{
        "hookSpecificOutput": {
            "hookEventName": "TeammateIdle",
            "additionalContext": "Teammate 300초 이상 정체 — 자동 종료 허용. Lead가 직접 수행하거나 재할당하세요."
        }
    }'
    exit 0
elif [ "$IDLE_DURATION" -ge 120 ]; then
    # 120초 이상 무응답 → 재활성화 시도
    jq -n '{
        "hookSpecificOutput": {
            "hookEventName": "TeammateIdle",
            "additionalContext": "Teammate 120초 무응답 — 재활성화 시도. 할당된 작업을 계속 진행하세요."
        }
    }'
    exit 2  # 정지 방지
fi

exit 0
