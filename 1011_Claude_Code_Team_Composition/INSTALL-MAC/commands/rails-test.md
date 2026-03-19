# /rails-test - 테스트 실행 및 품질 검증

전체 테스트 스위트를 실행하고 코드 품질을 검증합니다.

## 트리거
- "테스트", "RSpec", "검증", "커버리지"

## 실행 단계

### 1. 전체 테스트 실행

```bash
bundle exec rspec
```

### 2. 결과 분석

#### 성공 시
```
Finished in 5.23 seconds
50 examples, 0 failures

Coverage: 85.5%
```

#### 실패 시
```
50 examples, 2 failures

Failed examples:
rspec ./spec/models/user_spec.rb:42
rspec ./spec/requests/articles_spec.rb:78
```

### 3. 커버리지 확인

```bash
# SimpleCov 리포트
open coverage/index.html
```

커버리지 기준:
- 최소: 80%
- 권장: 90%+

### 4. 정적 분석

#### RuboCop
```bash
bundle exec rubocop
```

#### Brakeman (보안)
```bash
bundle exec brakeman -o brakeman_report.html
```

#### Bundler Audit (의존성 보안)
```bash
bundle audit
```

### 5. N+1 쿼리 확인

개발 환경에서 Bullet gem 확인:
- 콘솔 경고
- 브라우저 알림
- 로그 파일

### 6. 테스트 실패 시 수정

```
┌─────────────────────────────────────────┐
│ 테스트 실패 발견                          │
├─────────────────────────────────────────┤
│ 1. 실패 원인 분석                         │
│ 2. 코드 수정                             │
│ 3. 테스트 재실행                          │
│ 4. 통과 확인                             │
│ 5. 커밋                                  │
└─────────────────────────────────────────┘
```

### 7. 결과 보고

```
=== 테스트 결과 ===

📊 RSpec
   ✓ 50 examples, 0 failures
   ⏱️ 5.23 seconds

📈 Coverage
   ✓ 85.5% (minimum: 80%)
   ⚠️ Uncovered: app/services/payment_service.rb:42-58

🔍 RuboCop
   ✓ No offenses detected

🔒 Brakeman
   ✓ No warnings

📦 Bundle Audit
   ✓ No vulnerabilities found

=== 결과: PASS ===

배포 준비 완료. /rails-deploy로 배포하세요.
```

## 테스트 유형별 실행

### Model 테스트만
```bash
bundle exec rspec spec/models/
```

### Request 테스트만
```bash
bundle exec rspec spec/requests/
```

### System 테스트만
```bash
bundle exec rspec spec/system/
```

### 특정 파일
```bash
bundle exec rspec spec/models/user_spec.rb
```

### 특정 라인
```bash
bundle exec rspec spec/models/user_spec.rb:42
```

### 태그 필터
```bash
bundle exec rspec --tag focus
bundle exec rspec --tag ~slow
```

## 병렬 테스트 (선택)

```bash
# parallel_rspec gem 필요
bundle exec parallel_rspec spec/
```

## CI 환경 설정

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - run: bundle exec rails db:setup
      - run: bundle exec rspec
      - run: bundle exec rubocop
      - run: bundle exec brakeman
```

## 문제 해결

### 테스트가 느릴 때
- `spring` 사용
- 불필요한 DB 접근 줄이기
- `let` 대신 `let!` 주의

### 불안정한 테스트 (Flaky)
- 시간 의존 테스트 수정
- 비동기 테스트 대기 추가
- 데이터베이스 클리닝 확인

### 커버리지가 낮을 때
- 미커버 파일 확인
- 엣지 케이스 테스트 추가
- 브랜치 커버리지 확인

## 다음 단계

모든 테스트 통과 시:
- `/rails-deploy`: 프로덕션 배포
