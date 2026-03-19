# Claude Code Settings Configuration

> Version: 1.0 | Created: 2026-02-01
> Source: Boris Cherny's 13 Tips for Claude Code + Custom Implementation

---

## 1. 개요

이 문서는 Claude Code의 `~/.claude/settings.json` 설정을 정리한 가이드입니다.
Boris Cherny의 워크플로우 팁을 기반으로 바이브 코딩에 최적화된 설정을 구성했습니다.

---

## 2. 설정 파일 위치

```
~/.claude/
├── settings.json          # 전역 설정 (권한, 훅, 모델)
├── CLAUDE.md              # 전역 가이드라인
└── commands/              # 커스텀 슬래시 커맨드
    ├── commit-push.md
    ├── pr-review.md
    ├── project-review.md
    └── memory-save.md
```

---

## 3. Pre-allowed Permissions (사전 허용 권한)

### 3.1 개념

매번 "Allow?" 프롬프트 없이 자동으로 실행되는 명령어 설정입니다.
바이브 코딩 스타일에서는 개발 흐름을 끊지 않기 위해 필수입니다.

### 3.2 현재 설정 (Developer Set)

#### ✅ 허용된 명령어 (52개)

| 카테고리 | 명령어 | 설명 |
|---------|--------|------|
| **Git (15)** | `git status`, `git diff`, `git log`, `git add`, `git commit`, `git push`, `git pull`, `git branch`, `git checkout`, `git merge`, `git stash`, `git fetch`, `git remote`, `git show`, `git rebase` | 버전 관리 전체 |
| **Package Managers (8)** | `npm`, `npx`, `yarn`, `pnpm`, `bun`, `bunx`, `pip`, `pip3` | JS/Python 패키지 관리 |
| **Languages (5)** | `python`, `python3`, `pytest`, `go`, `cargo`, `rustc` | 언어 런타임 |
| **File System (14)** | `ls`, `pwd`, `mkdir`, `cp`, `mv`, `cat`, `head`, `tail`, `wc`, `grep`, `find`, `tree`, `which`, `echo` | 파일 조회/조작 |
| **DevOps (6)** | `gh`, `ansible`, `ansible-playbook`, `docker`, `docker-compose`, `make` | 인프라 도구 |
| **Network (2)** | `curl`, `wget` | HTTP 요청 |
| **Utility (2)** | `code`, `open` | IDE/파일 열기 |

#### ❌ 차단된 명령어 (12개)

| 위험 수준 | 명령어 | 이유 |
|----------|--------|------|
| **🔴 Critical** | `rm -rf /*`, `rm -rf ~/*` | 시스템/홈 전체 삭제 |
| **🔴 Critical** | `sudo rm:*` | 루트 권한 삭제 |
| **🔴 Critical** | `chmod 777` | 보안 취약 권한 |
| **🔴 Critical** | `>/dev/sda`, `mkfs:*`, `dd if=*of=/dev/*` | 디스크 파괴 |
| **🔴 Critical** | `:(){ :\|:& };:` | Fork Bomb |
| **🟠 High** | `shutdown`, `reboot` | 시스템 종료 |
| **🟠 High** | `kill -9 1`, `killall` | 프로세스 강제 종료 |

### 3.3 설정 패턴

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(npm:*)",
      ...
    ],
    "deny": [
      "Bash(rm -rf /*)",
      ...
    ]
  }
}
```

**패턴 문법**:
- `Bash(command:*)` - command로 시작하는 모든 명령 허용
- `Bash(*keyword*)` - keyword 포함 명령 매칭

---

## 4. Hooks (훅 시스템)

### 4.1 개념

도구 실행 전/후에 자동으로 실행되는 셸 명령어입니다.

### 4.2 Hook 종류

| Hook | 타이밍 | 용도 |
|------|--------|------|
| **PreToolUse** | 도구 실행 전 | 검증, 로깅, 차단 |
| **PostToolUse** | 도구 실행 후 | 포매팅, 알림 |
| **SessionStart** | 세션 시작 시 | 초기화, 인사 |

### 4.3 현재 설정

#### PreToolUse Hooks

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "echo '[🔵 실행 예정] Bash 명령: $CLAUDE_TOOL_INPUT'"
  }]
}
```
→ Bash 명령 실행 전 로깅

```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "if echo $CLAUDE_TOOL_INPUT | grep -qE '\\.env|\\.secret|credentials|password'; then echo '❌ 보안 파일 수정 차단됨' && exit 1; fi"
  }]
}
```
→ 보안 파일 수정 차단 (`.env`, `.secret`, `credentials`, `password`)

#### PostToolUse Hooks

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {"command": "echo '[✅ 파일 수정 완료]'"},
    {"command": "[자동 포매팅 스크립트]"},
    {"command": "if [ -d .git ]; then git status -s 2>/dev/null | head -5; fi"}
  ]
}
```

**자동 포매팅 지원**:

| 언어 | 도구 | 확장자 |
|------|------|--------|
| JavaScript/TypeScript | Prettier | `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, `.css`, `.scss`, `.html` |
| Python | Black | `.py` |
| Go | gofmt | `.go` |
| Rust | rustfmt | `.rs` |

#### SessionStart Hook

```json
{
  "matcher": ".*",
  "hooks": [{
    "command": "echo '🚀 Claude Code 세션 시작 - $(date +\"%Y-%m-%d %H:%M:%S\")'"
  }]
}
```

### 4.4 사용 가능한 환경 변수

| 변수 | 설명 |
|------|------|
| `$CLAUDE_TOOL_INPUT` | 도구에 전달된 입력 (JSON) |
| `$CLAUDE_FILE_PATH` | 수정된 파일 경로 |

---

## 5. Custom Slash Commands (커스텀 슬래시 커맨드)

### 5.1 개념

`/command-name` 형식으로 호출하는 사용자 정의 워크플로우입니다.

### 5.2 저장 위치

```
~/.claude/commands/[command-name].md
```

### 5.3 현재 등록된 커맨드

| 커맨드 | 파일 | 기능 |
|--------|------|------|
| `/commit-push` | `commit-push.md` | Git 커밋 + 푸시 자동화 |
| `/pr-review` | `pr-review.md` | PR/커밋 변경사항 리뷰 |
| `/project-review` | `project-review.md` | 프로젝트 전체 평가 |
| `/memory-save` | `memory-save.md` | 작업 내용 메모리 저장 |

### 5.4 커맨드 파일 형식

```markdown
---
description: 커맨드 설명 (한 줄)
---

[프롬프트 본문]

$ARGUMENTS (사용자가 전달한 인자)
```

---

## 6. Default Model

```json
{
  "defaultModel": "opus"
}
```

- 세션의 기본 모델 설정
- 옵션: `opus`, `sonnet`, `haiku`

---

## 7. 전체 설정 파일

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git merge:*)",
      "Bash(git stash:*)",
      "Bash(git fetch:*)",
      "Bash(git remote:*)",
      "Bash(git show:*)",
      "Bash(git rebase:*)",
      "Bash(npm:*)",
      "Bash(npx:*)",
      "Bash(yarn:*)",
      "Bash(pnpm:*)",
      "Bash(bun:*)",
      "Bash(bunx:*)",
      "Bash(pip:*)",
      "Bash(pip3:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pytest:*)",
      "Bash(go:*)",
      "Bash(cargo:*)",
      "Bash(rustc:*)",
      "Bash(ls:*)",
      "Bash(pwd:*)",
      "Bash(mkdir:*)",
      "Bash(cp:*)",
      "Bash(mv:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(tree:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(gh:*)",
      "Bash(ansible:*)",
      "Bash(ansible-playbook:*)",
      "Bash(docker:*)",
      "Bash(docker-compose:*)",
      "Bash(make:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(code:*)",
      "Bash(open:*)"
    ],
    "deny": [
      "Bash(rm -rf /*)",
      "Bash(rm -rf ~/*)",
      "Bash(sudo rm:*)",
      "Bash(chmod 777:*)",
      "Bash(*>/dev/sda*)",
      "Bash(mkfs:*)",
      "Bash(dd if=*of=/dev/*)",
      "Bash(:(){ :|:& };:*)",
      "Bash(shutdown:*)",
      "Bash(reboot:*)",
      "Bash(kill -9 1:*)",
      "Bash(killall:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "echo '[🔵 실행 예정] Bash 명령: $CLAUDE_TOOL_INPUT'"
        }]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "if echo $CLAUDE_TOOL_INPUT | grep -qE '\\.env|\\.secret|credentials|password'; then echo '❌ 보안 파일 수정 차단됨' && exit 1; fi"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "echo '[✅ 파일 수정 완료]'"},
          {"type": "command", "command": "[자동 포매팅 스크립트]"},
          {"type": "command", "command": "if [ -d .git ]; then git status -s 2>/dev/null | head -5; fi"}
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": ".*",
        "hooks": [{
          "type": "command",
          "command": "echo '🚀 Claude Code 세션 시작 - $(date +\"%Y-%m-%d %H:%M:%S\")'"
        }]
      }
    ]
  },
  "defaultModel": "opus"
}
```

---

## 8. 관련 문서

- [[Boris-Cherny-Workflow-Guide]] - Boris Cherny 13 Tips 원본 분석
- [[CLAUDE]] - Claude Code 통합 가이드라인
- [[008_boris_cherny_workflow_analysis_20260201]] - 메모리 기록

---

## 9. 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-01 | 1.0 | 초기 문서 작성, Developer Set 권한 설정 |

---

*Last updated: 2026-02-01 by 🎵 아리*
