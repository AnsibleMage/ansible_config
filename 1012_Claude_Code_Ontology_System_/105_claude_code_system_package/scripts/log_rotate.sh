#!/bin/bash
# log_rotate.sh — C5 Observability 로그 로테이션
# 일별 로그 90일 보존 / 세션 통계 180일 보존 / 월간 리포트 무기한 보존

LOG_DIR="$HOME/.claude/logs"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

echo "🔄 로그 로테이션 시작: $TIMESTAMP"

# 일별 로그 (.log) — 90일 이전 삭제
DELETED_DAILY=0
if [ -d "$LOG_DIR" ]; then
    while IFS= read -r -d '' file; do
        rm "$file"
        DELETED_DAILY=$((DELETED_DAILY + 1))
    done < <(find "$LOG_DIR" -maxdepth 1 -name "*.log" -mtime +90 -print0 2>/dev/null)
fi
echo "  일별 로그: ${DELETED_DAILY}개 삭제 (90일 기준)"

# 세션 통계 (.json) — 180일 이전 삭제
DELETED_SESSION=0
SESSIONS_DIR="$LOG_DIR/sessions"
if [ -d "$SESSIONS_DIR" ]; then
    while IFS= read -r -d '' file; do
        rm "$file"
        DELETED_SESSION=$((DELETED_SESSION + 1))
    done < <(find "$SESSIONS_DIR" -name "*.json" -mtime +180 -print0 2>/dev/null)
fi
echo "  세션 통계: ${DELETED_SESSION}개 삭제 (180일 기준)"

# 월간 리포트 — 삭제하지 않음 (무기한 보존)
REPORT_COUNT=0
if [ -d "$LOG_DIR/reports" ]; then
    REPORT_COUNT=$(find "$LOG_DIR/reports" -name "*_monthly.md" | wc -l | tr -d ' ')
fi
echo "  월간 리포트: ${REPORT_COUNT}개 보존 (무기한)"

# 결과 로그 기록
echo "$TIMESTAMP | LOG_ROTATE | daily=${DELETED_DAILY} session=${DELETED_SESSION} reports=${REPORT_COUNT} | OK" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

echo "✅ 로그 로테이션 완료"
