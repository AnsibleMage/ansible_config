# /rails-deploy - Kamal 2 프로덕션 배포

Kamal 2를 사용하여 프로덕션에 배포합니다.

## 트리거
- "배포", "deploy", "Kamal", "프로덕션"

## 사전 조건 확인

### 1. 테스트 통과 확인

```bash
bundle exec rspec
# Expected: 0 failures

bundle exec rubocop
# Expected: No offenses

bundle exec brakeman
# Expected: No warnings
```

### 2. 환경 변수 확인

```bash
cat .kamal/secrets
# KAMAL_REGISTRY_PASSWORD=...
# RAILS_MASTER_KEY=...
# DATABASE_URL=...
```

### 3. 설정 파일 확인

```bash
cat config/deploy.yml
# service, servers, registry 등 확인
```

## 배포 단계

### 1. 초기 설정 (최초 1회)

```bash
kamal setup
```

### 2. 배포 실행

```bash
kamal deploy
```

배포 과정:
1. Docker 이미지 빌드
2. Registry에 푸시
3. 서버에 배포
4. 마이그레이션 실행
5. 헬스체크
6. 이전 컨테이너 정리

### 3. 배포 상태 확인

```bash
kamal app details
```

출력 예시:
```
Traefik Host: 192.168.1.10
  Service: myapp
  App Host: 192.168.1.10
    CONTAINER ID   STATUS         NAMES
    abc123         Up 2 minutes   myapp-web-abc123
```

### 4. 헬스체크

```bash
curl -f https://myapp.com/up
# Expected: HTTP 200

curl https://myapp.com/health
# Expected: {"status":"healthy",...}
```

### 5. 로그 확인

```bash
kamal app logs --lines 50
# 에러 없는지 확인
```

## 배포 완료 메시지

```
=== 배포 완료 ===

📦 버전: abc123
🌐 URL: https://myapp.com
⏱️ 소요 시간: 3분 42초

✓ 이미지 빌드 완료
✓ Registry 푸시 완료
✓ 서버 배포 완료
✓ 마이그레이션 완료
✓ 헬스체크 통과

서버 상태:
- web: 2/2 running
- worker: 1/1 running

🎉 프로덕션 배포 성공!

다음 단계: /rails-verify로 프로덕션 검증
```

## 롤백

### 문제 발생 시

```bash
# 이전 버전으로 롤백
kamal rollback

# 상태 확인
kamal app details

# 로그 확인
kamal app logs
```

### 롤백 사유 기록

```
⚠️ 롤백 실행

원인: [문제 설명]
조치: [해결 방안]
```

## 유용한 Kamal 명령어

### 빌드만
```bash
kamal build
```

### 푸시만
```bash
kamal push
```

### 배포만 (이미지 있을 때)
```bash
kamal deploy --skip-push
```

### 서버 접속
```bash
kamal app exec --interactive 'bin/rails console'
```

### 특정 명령 실행
```bash
kamal app exec 'bin/rails runner "puts User.count"'
```

### 서비스 재시작
```bash
kamal app restart
```

## 배포 체크리스트

### Pre-deployment
- [ ] 모든 테스트 통과
- [ ] 커버리지 ≥ 80%
- [ ] 보안 검사 통과
- [ ] 환경 변수 설정
- [ ] 마이그레이션 안전성

### Deployment
- [ ] 이미지 빌드 성공
- [ ] Registry 푸시 성공
- [ ] 서버 배포 성공
- [ ] 마이그레이션 성공
- [ ] 헬스체크 통과

### Post-deployment
- [ ] 주요 기능 동작 확인
- [ ] 에러 로그 없음
- [ ] 성능 정상
- [ ] 알림 발송

## 템플릿 위치

- `~/.claude/templates/rails8/deploy_yml_Template.yml`
- `~/.claude/templates/rails8/DeployChecklist_Template.md`

## 다음 단계

배포 완료 후:
- `/rails-verify`: 프로덕션 검증 실행
