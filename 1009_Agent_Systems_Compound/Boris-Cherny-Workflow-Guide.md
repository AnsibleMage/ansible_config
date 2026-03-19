# Boris Cherny Claude Code 워크플로우 분석 및 적용 가이드

> 🎵 아리 & 🔧 앤 - 2026-02-01
>
> **원본 출처**: Boris Cherny (Claude Code 창시자)
> **참고 영상**: 코드팩토리 「클로드 코드 창시자가 직접 알려주는 클로드 코드 꿀팁 13가지」

---

## 📚 원문 출처

- [Boris Cherny Twitter/X Thread](https://x.com/bcherny/status/2007179832300581177)
- [Boris Cherny Threads Post](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm)
- [InfoQ - Inside the Development Workflow](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)
- [VentureBeat Article](https://venturebeat.com/technology/the-creator-of-claude-code-just-revealed-his-workflow-and-developers-are)

---

## 🔍 Boris Cherny 13가지 팁 분석

### 1. 병렬 실행 (Parallel Sessions)

**원문 요약**:
> "I run 5 Claudes in parallel in my terminal. I number my tabs 1-5, and use system notifications to know when a Claude needs input."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| 로컬 세션 | 5개 병렬 | PARALLEL-FIRST 원칙 | ✅ 개념 적용됨 |
| 탭 번호 체계 | 1-5 번호 | 미적용 | ⚠️ 실무 적용 필요 |
| 시스템 알림 | Notification 설정 | 미적용 | ⚠️ 설정 필요 |
| Git 충돌 방지 | 각 세션별 별도 checkout | 미언급 | ⚠️ 추가 필요 |

**적용 방안**:
```bash
# 터미널 탭별 별도 Git checkout
mkdir -p ~/claude-workspaces/{1,2,3,4,5}
# 각 탭에서 별도 워크스페이스 사용
```

---

### 2. 다중 세션 활용 (Web + Local)

**원문 요약**:
> "I run 5-10 Claudes on claude.ai in my browser, using teleport command to hand off sessions between web and local machine."

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| 웹 세션 | 5-10개 추가 | 미적용 | ⚠️ 활용 가능 |
| Teleport | `--teleport` 명령 | 미언급 | ⚠️ 학습 필요 |
| iOS 앱 | 아침에 시작, 나중 확인 | 미적용 | 선택사항 |

**적용 방안**:
```bash
# 로컬 → 웹 세션 핸드오프
claude --teleport

# 웹에서 시작한 세션 로컬로 가져오기
claude --resume <session-id>
```

---

### 3. 고성능 모델 고집 (Opus 4.5 Only)

**원문 요약**:
> "I use Opus 4.5 with thinking for everything. It's the best coding model I've ever used, and even though it's bigger & slower than Sonnet, since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| 기본 모델 | Opus 4.5 only | 복잡도별 opus/sonnet 분리 | ⚠️ 재검토 필요 |
| Thinking 모드 | 항상 활성화 | 미언급 | ⚠️ 추가 필요 |

**Boris의 논리**:
- Opus는 steering이 덜 필요함
- Tool use가 더 우수함
- 결과적으로 더 빠름 (재작업 감소)

**적용 방안**:
```json
// .claude/settings.json
{
  "model": "opus",
  "thinking": true
}
```

**우리 시스템 조정 제안**:
- 현재: 복잡도별 opus/sonnet 분리
- Boris 방식: 전부 opus
- **절충안**: 메인 세션은 opus, 단순 서브태스크만 sonnet

---

### 4. CLAUDE.md 공유 (Team Learning)

**원문 요약**:
> "Anytime we see Claude do something incorrectly we add it to the CLAUDE.md, so Claude knows not to do it next time. I often use @.claude tag on coworkers' PRs to add learnings."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| 실수 기록 | 팀 공유 CLAUDE.md | 개인용 CLAUDE.md | ✅ 유사 |
| 토큰 크기 | ~2.5k 토큰 | 미측정 | 점검 필요 |
| PR 연동 | @.claude 태그 | 미적용 | ⚠️ GitHub Action 필요 |

**적용 방안**:
```bash
# GitHub Action 설치
claude /install-github-action

# PR 리뷰 시 CLAUDE.md 업데이트
# @.claude 태그로 실수 기록 추가
```

---

### 5. PR 검증 자동화 (GitHub Action)

**원문 요약**:
> "Install GitHub Action to have Claude verify PRs directly."

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| PR 자동 검증 | GitHub Action | 미적용 | ⚠️ 설치 필요 |

**적용 방안**:
```bash
# Claude Code GitHub Action 설치
claude /install-github-action
```

---

### 6. 플랜(Plan) 모드 우선

**원문 요약**:
> "If my goal is to write a Pull Request, I will use Plan mode, and go back and forth with Claude until I like its plan. From there, I switch into auto-accept edits mode and Claude can usually 1-shot it. A good plan is really important!"

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| Plan 모드 시작 | Shift+Tab 2번 | 체인에서 Plan 에이전트 호출 | ✅ 유사 |
| Auto-accept | 계획 후 전환 | 미언급 | ⚠️ 워크플로우 추가 |

**적용 방안**:
```
워크플로우:
1. Shift+Tab 2번 → Plan 모드 진입
2. 계획 반복 수정
3. 계획 확정 후 Auto-accept 모드로 전환
4. Claude가 1-shot 실행
```

---

### 7. 커스텀 커맨드 저장 (Slash Commands)

**원문 요약**:
> "I use slash commands for every 'inner loop' workflow that I do many times a day. Commands are checked into git and live in `.claude/commands/`. Claude and I use a `/commit-push-pr` command dozens of times every day."

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| 커스텀 커맨드 | .claude/commands/ | 미적용 | ⚠️ 생성 필요 |
| Git 공유 | 팀과 공유 | 개인용 | 확장 가능 |

**적용 방안**:
```bash
# 커맨드 폴더 생성
mkdir -p ~/.claude/commands

# 예시: commit-push-pr.md
cat > ~/.claude/commands/commit-push-pr.md << 'EOF'
---
description: Commit, push, and create PR
---
1. Stage all changes
2. Create commit with conventional message
3. Push to remote
4. Create PR with description
EOF
```

---

### 8. 서브 에이전트 활용 (Subagents)

**원문 요약**:
> "I use a few subagents regularly: code-simplifier simplifies the code after Claude is done working, verify-app has detailed instructions for testing Claude Code end to end."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| code-simplifier | 코드 정리 전용 | 미적용 | ⚠️ 생성 필요 |
| verify-app | 테스트 검증 전용 | quality_reviewer 유사 | ✅ 부분 적용 |
| 자동화 | PR 워크플로우 통합 | 체인 시스템 | ✅ 유사 |

**적용 방안**:
```bash
# code-simplifier 서브에이전트 정의
cat > ~/.claude/commands/simplify.md << 'EOF'
---
description: Simplify and clean up code
---
Review the code I just wrote and:
1. Remove unnecessary complexity
2. Improve readability
3. Apply DRY principles
4. Suggest refactoring if needed
EOF
```

---

### 9. 포스트 툴 훅 (PostToolUse Hook)

**원문 요약**:
> "I run a PostToolUse hook to format Claude's output: `bun run format || true`"

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| 자동 포매팅 | PostToolUse 훅 | 미적용 | ⚠️ 설정 필요 |
| CI 에러 방지 | format || true | 미적용 | ⚠️ 설정 필요 |

**적용 방안**:
```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "command": "bun run format || true",
        "tools": ["Edit", "Write"]
      }
    ]
  }
}
```

---

### 10. 권한 사전 설정 (Pre-allowed Permissions)

**원문 요약**:
> "I don't use `--dangerously-skip-permissions`. Instead, I use `/permissions` to pre-allow common bash commands that are safe in my environment."

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| 권한 관리 | /permissions 사전 등록 | 미적용 | ⚠️ 설정 필요 |
| 팀 공유 | .claude/settings.json | 미적용 | ⚠️ 설정 필요 |

**적용 방안**:
```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "bun run build:*",
      "bun run test:*",
      "npm run *",
      "git status",
      "git diff",
      "git log"
    ]
  }
}
```

---

### 11. 다양한 툴 권한 제공 (MCP Servers)

**원문 요약**:
> "I give Claude access to Slack search, BigQuery queries, and Sentry error logs through MCP servers configured in `.mcp.json`."

| 항목 | Boris 방식 | 우리 현황 | Gap |
|------|-----------|----------|-----|
| Slack 검색 | MCP 서버 | 미적용 | 선택사항 |
| BigQuery | MCP 서버 | 미적용 | 선택사항 |
| Sentry | MCP 서버 | 미적용 | 선택사항 |
| 설정 공유 | .mcp.json | 미적용 | ⚠️ 구조 학습 필요 |

**적용 방안**:
```json
// .mcp.json
{
  "servers": {
    "slack": {
      "command": "mcp-server-slack",
      "env": {
        "SLACK_TOKEN": "${SLACK_TOKEN}"
      }
    }
  }
}
```

---

### 12. 롱 러닝 태스크 관리 (Long-running Tasks)

**원문 요약**:
> "For long-running tasks, I use background agent verification, Stop hooks, or the ralph-wiggum plugin."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| 백그라운드 에이전트 | 활용 | run_in_background 언급 | ✅ 적용됨 |
| Stop 훅 | 활용 | 미적용 | ⚠️ 학습 필요 |
| ralph-wiggum | 플러그인 | 미적용 | 선택사항 |

---

### 13. 자기 검증 방식 제시 (Verification)

**원문 요약**:
> "Probably the most important thing to get great results out of Claude Code: give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result."

| 항목 | Boris 방식 | 우리 현황 (V3.0) | Gap |
|------|-----------|-----------------|-----|
| 검증 방식 제공 | 필수 강조 | quality_reviewer 체인 | ✅ 부분 적용 |
| Chrome Extension | UI 테스트 | /webapp-testing 스킬 | ✅ 유사 |
| 피드백 루프 | 2-3x 품질 향상 | 체인 패턴에 포함 | ✅ 적용됨 |

---

## 📊 Gap 분석 요약

### ✅ 이미 적용된 것 (6개)

| 팁 | 우리 시스템 적용 |
|----|-----------------|
| 병렬 실행 개념 | PARALLEL-FIRST 원칙 |
| Plan 모드 | Plan 에이전트, 체인 |
| 서브에이전트 | 16개 에이전트 시스템 |
| 팀 학습 문서 | CLAUDE.md V3.0 |
| 백그라운드 태스크 | run_in_background |
| 검증 방식 | quality_reviewer, /webapp-testing |

### ⚠️ 추가 적용 필요 (7개)

| 팁 | 필요한 작업 | 우선순위 |
|----|------------|----------|
| 시스템 알림 설정 | 터미널 Notification 구성 | MEDIUM |
| Teleport 명령 | 웹-로컬 세션 연동 학습 | LOW |
| Opus 전용 + Thinking | 모델 전략 재검토 | HIGH |
| 커스텀 커맨드 | .claude/commands/ 생성 | HIGH |
| PostToolUse 훅 | 자동 포매팅 설정 | HIGH |
| 권한 사전 설정 | /permissions 구성 | HIGH |
| GitHub Action | PR 자동 검증 설치 | MEDIUM |

---

## 🛠️ 우선 적용 액션 플랜

### Phase 1: 즉시 적용 (HIGH)

```bash
# 1. 커스텀 커맨드 폴더 생성
mkdir -p ~/.claude/commands

# 2. commit-push-pr 커맨드 생성
# 3. simplify 커맨드 생성
# 4. settings.json에 permissions 추가
# 5. PostToolUse 훅 설정
```

### Phase 2: 단기 적용 (MEDIUM)

```bash
# 1. GitHub Action 설치
claude /install-github-action

# 2. 시스템 알림 설정
# 3. MCP 서버 검토 및 필요시 추가
```

### Phase 3: 검토 및 결정 (전략적)

- Opus 전용 vs opus/sonnet 혼용 전략 결정
- Teleport 활용 여부 결정
- 팀 공유 범위 결정

---

## 🔄 CLAUDE.md V3.0 업데이트 제안

### 추가할 섹션

```markdown
## 🔧 Boris Cherny Workflow Integration

### Verification First
> "Give Claude a way to verify its work" - 2-3x quality improvement

### Slash Commands
Location: `~/.claude/commands/`
- /commit-push-pr
- /simplify
- /verify

### PostToolUse Hooks
Auto-format on Edit/Write operations

### Permissions Pre-allowed
Safe bash commands registered in settings.json
```

---

## 📝 결론

Boris Cherny의 핵심 철학:
1. **검증이 가장 중요** - 피드백 루프가 품질을 2-3배 향상
2. **계획 먼저** - Plan 모드로 시작, auto-accept로 마무리
3. **자동화** - 반복 작업은 커맨드로, 포매팅은 훅으로
4. **팀 학습** - 실수를 CLAUDE.md에 기록하여 반복 방지

우리 시스템(V3.0)은 이미 많은 부분이 적용되어 있으며,
커스텀 커맨드, 훅, 권한 설정만 추가하면 Boris 수준의 워크플로우 완성!

---

*🎵 아리 & 🔧 앤 - Boris Cherny Workflow Analysis*
