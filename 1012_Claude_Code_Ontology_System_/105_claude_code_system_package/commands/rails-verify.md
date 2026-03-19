# /rails-verify - 프로덕션 검증

프로덕션 배포 후 시스템 상태를 종합 검증합니다.

## 트리거
- "검증", "verify", "프로덕션 테스트", "배포 확인"

## 검증 단계

### 1. Health Check

```bash
# 기본 헬스체크
curl -sf https://myapp.com/up
# Expected: HTTP 200

# 상세 헬스체크
curl -s https://myapp.com/health | jq
```

예상 응답:
```json
{
  "status": "healthy",
  "checks": {
    "database": {"status": "ok"},
    "cache": {"status": "ok"},
    "queue": {"status": "ok", "workers": 2},
    "cable": {"status": "ok"}
  }
}
```

### 2. Smoke Test

```bash
# 핵심 엔드포인트 테스트
endpoints=(
  "/"
  "/login"
  "/articles"
  "/api/v1/articles"
)

for endpoint in "${endpoints[@]}"; do
  status=$(curl -o /dev/null -s -w "%{http_code}" "https://myapp.com$endpoint")
  echo "$endpoint: $status"
done
```

예상 결과:
```
/: 200
/login: 200
/articles: 200
/api/v1/articles: 200
```

### 3. Performance Check

```bash
# TTFB 측정
curl -o /dev/null -s -w "TTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" https://myapp.com/
```

기준:
- TTFB: < 200ms
- Total: < 500ms

### 4. Log Analysis

```bash
# 최근 로그에서 에러 확인
kamal app logs --lines 100 | grep -i "error\|exception\|fatal"
# Expected: (empty)

# 에러 카운트
kamal app logs --lines 500 | grep -c "ERROR"
# Expected: 0
```

### 5. Service Status

```bash
# 컨테이너 상태
kamal app details

# 데이터베이스 연결
kamal app exec 'bin/rails runner "puts ActiveRecord::Base.connected?"'
# Expected: true

# 큐 워커 상태
kamal app exec 'bin/rails runner "puts SolidQueue::Process.where(kind: \"Worker\").count"'
# Expected: > 0
```

### 6. 기능별 검증

```bash
# 사용자 카운트
kamal app exec 'bin/rails runner "puts User.count"'

# 최근 데이터 확인
kamal app exec 'bin/rails runner "puts Article.last&.title"'
```

## 검증 결과 보고

```
=== 프로덕션 검증 결과 ===

🏥 Health Check
   ✓ /up: 200 OK
   ✓ /health: healthy
   ✓ Database: connected
   ✓ Cache: operational
   ✓ Queue: 2 workers active
   ✓ Cable: operational

🔥 Smoke Test
   ✓ Homepage: 200 (142ms)
   ✓ Login: 200 (89ms)
   ✓ Articles: 200 (156ms)
   ✓ API: 200 (78ms)

⚡ Performance
   ✓ TTFB: 85ms (< 200ms)
   ✓ Total: 342ms (< 500ms)
   ✓ Memory: 65% (< 80%)
   ✓ CPU: 12% (< 70%)

📋 Logs
   ✓ Errors: 0
   ✓ Warnings: 3 (acceptable)
   ✓ Slow queries: 0

🖥️ Services
   ✓ Web: 2/2 running
   ✓ Worker: 1/1 running
   ✓ Database: connected
   ✓ SSL: valid (expires in 89 days)

=== 결과: PASS ===

🎉 프로덕션 검증 완료!
모든 시스템이 정상 동작 중입니다.
```

## 실패 시 대응

### Health Check 실패
```
⚠️ Health Check 실패

원인: [에러 메시지]
조치:
1. 로그 확인: kamal app logs
2. 서비스 재시작: kamal app restart
3. 롤백 고려: kamal rollback
```

### Performance 저하
```
⚠️ Performance 저하 감지

현재: TTFB 450ms (기준: < 200ms)
조치:
1. 슬로우 쿼리 확인
2. 캐시 상태 확인
3. 서버 리소스 확인
```

### 에러 로그 발견
```
⚠️ 에러 로그 발견

에러 수: 5
최근 에러:
- [에러 메시지 1]
- [에러 메시지 2]

조치:
1. 에러 원인 분석
2. 핫픽스 또는 롤백 결정
```

## 자동화 검증 스크립트

```bash
#!/bin/bash
# scripts/verify_production.sh

BASE_URL="https://myapp.com"
FAILED=0

echo "=== Production Verification ==="

# Health Check
echo -n "Health: "
if curl -sf "$BASE_URL/up" > /dev/null; then
  echo "PASS"
else
  echo "FAIL"
  FAILED=1
fi

# Smoke Tests
for path in "/" "/login" "/articles"; do
  echo -n "$path: "
  if curl -sf "$BASE_URL$path" > /dev/null; then
    echo "PASS"
  else
    echo "FAIL"
    FAILED=1
  fi
done

# Performance
TTFB=$(curl -o /dev/null -s -w '%{time_starttransfer}' "$BASE_URL/")
TTFB_MS=$(echo "$TTFB * 1000" | bc | cut -d'.' -f1)
echo "TTFB: ${TTFB_MS}ms"

if [ "$TTFB_MS" -gt 200 ]; then
  echo "⚠️ TTFB exceeds threshold"
  FAILED=1
fi

# Result
if [ $FAILED -eq 0 ]; then
  echo "✅ All checks passed!"
  exit 0
else
  echo "❌ Some checks failed!"
  exit 1
fi
```

## 모니터링 대시보드

검증 후 지속적 모니터링:
- `/health` 엔드포인트 주기적 호출
- 에러 알림 설정
- 성능 메트릭 수집

## 완료

```
🎉 프로덕션 검증 완료!

다음 작업:
1. 모니터링 대시보드 확인
2. 사용자 피드백 수집
3. 다음 스프린트 계획
```
