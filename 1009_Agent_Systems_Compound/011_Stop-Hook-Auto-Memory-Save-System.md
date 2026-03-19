# 011. Stop Hook Auto Memory Save System

> ~~매 응답 완료 시 자동으로 메모리를 저장하는 Hook 시스템~~
> **상태: 실패 → 지침 기반으로 전환 (V3.6)**

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| **Stop Hook 방식** | ❌ **실패** (스키마 불일치) |
| **대체 방식** | ✅ **지침 기반** (CLAUDE.md V3.6) |
| **구현일** | 2026-02-03 |
| **전환일** | 2026-02-03 |

---

## 1. 원래 의도

### 배경

| 문제 | 설명 |
|------|------|
| 세션 휘발성 | Claude Code 종료 후 재시작 시 이전 대화 컨텍스트 소실 |
| 수동 저장 번거로움 | `/memory-save` 매번 수동 호출 필요 |
| 저장 누락 | 중요한 작업도 저장하지 않고 세션 종료 가능 |

### 원래 해결책 (실패)

`Stop` Hook을 사용하여 **매 응답 완료 시** 자동으로 메모리 저장 트리거.

---

## 2. 실패 원인 분석

### 에러 메시지

```
Stop hook error: JSON validation failed: Hook JSON output validation failed:
- : Invalid input

Expected schema:
{
  "continue": "boolean (optional)",
  "suppressOutput": "boolean (optional)",
  "stopReason": "string (optional)",
  "decision": "\"approve\" | \"block\" (optional)",
  "reason": "string (optional)",
  "systemMessage": "string (optional)",
  "permissionDecision": "\"allow\" | \"deny\" | \"ask\" (optional)",
  "hookSpecificOutput": { ... }
}

The hook's stdout was: {
  "decision": "block",
  "hookSpecificOutput": {
    "additionalContext": "..."
  }
}
```

### 근본 원인

| 문제점 | 설명 |
|--------|------|
| **스키마 불일치** | Stop hook은 `hookSpecificOutput` 필드를 지원하지 않음 |
| **실행 시점** | Stop hook은 응답 **완료 후** 실행되어 Claude에게 추가 작업 지시 불가 |
| **아키텍처 한계** | Stop hook은 응답 차단/허용만 가능, 새 지시 주입 불가 |

### Hook별 지원 필드 비교

| Hook | hookSpecificOutput | additionalContext | 응답 후 지시 |
|------|-------------------|-------------------|-------------|
| **UserPromptSubmit** | ✅ | ✅ | - (응답 전) |
| **PreToolUse** | ✅ | - | - (도구 실행 전) |
| **PostToolUse** | ✅ | ✅ | - (도구 실행 후) |
| **Stop** | ❌ | ❌ | ❌ **불가** |
| **SessionStart** | - | - | - |
| **SessionEnd** | - | - | - |

---

## 3. 해결책: 지침 기반 메모리 저장

### 핵심 변경

```
이전 (실패):
  응답 완료 → Stop hook 실행 → ❌ 스키마 에러

현재 (정상):
  응답 작성 중 → 메모리 저장 판단 → 저장 → 응답 완료
```

### CLAUDE.md V3.6 추가 섹션

**위치**: `Our Identity` 섹션 하위

```markdown
### 응답 완료 프로토콜 (MANDATORY)

> **모든 의미 있는 작업 완료 시, 응답 마지막에 실행**

작업 완료
    ↓
┌─────────────────────────────┐
│ 메모리 저장 여부 판단        │
│ - 새로운 지식/인사이트?      │
│ - 중요한 결정/변경?          │
│ - 향후 참조 가치?            │
└─────────────────────────────┘
    ↓ Yes
┌─────────────────────────────┐
│ ~/.claude/memory/에 자동 저장       │
│ - 파일명: YYMM_SEQ_keyword   │
│ - 체인/에이전트/스킬 기록    │
│ - 💾 메모리 저장 완료        │
└─────────────────────────────┘
    ↓
🎵 완료! 다음은 뭘 할까요?
```

### 저장 기준

| 저장 O | 저장 X |
|--------|--------|
| 분석/설계 결과 | 단순 Q&A |
| 새로운 구현 | 파일 읽기만 |
| 중요한 결정 | 간단한 수정 |
| 학습/인사이트 | 반복 작업 |

---

## 4. 설정 변경 내역

### settings.json 변경

**이전**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/changjaeyou/.claude/hooks/auto-memory-save.sh"
          }
        ]
      }
    ]
  }
}
```

**이후**:
```json
{
  "hooks": {
    // Stop 섹션 제거됨
  }
}
```

### 파일 상태

| 파일 | 상태 |
|------|------|
| `~/.claude/hooks/auto-memory-save.sh` | 유지 (아카이브) |
| `~/.claude/settings.json` | Stop hook 제거됨 |
| `~/.claude/CLAUDE.md` | V3.6 (응답 완료 프로토콜 추가) |

---

## 5. 대안 접근법 비교

### 검토한 대안들

| 대안 | 설명 | 결과 |
|------|------|------|
| **A. Stop hook** | 응답 완료 후 hook 실행 | ❌ 스키마 에러 |
| **B. UserPromptSubmit** | 다음 프롬프트 시 이전 작업 저장 알림 | △ 가능하나 비직관적 |
| **C. 지침 기반** | CLAUDE.md에 규칙 추가 | ✅ **채택** |
| **D. systemMessage** | Stop hook에서 알림만 전달 | △ 강제 실행 불가 |

### 지침 기반 선택 이유

| 장점 | 설명 |
|------|------|
| **안정성** | Hook 스키마 의존 없음 |
| **유연성** | 저장 기준을 지침으로 명시 |
| **일관성** | 응답 흐름 내에서 자연스럽게 처리 |
| **디버깅** | 에러 발생 시 추적 용이 |

| 단점 | 설명 |
|------|------|
| **100% 보장 안됨** | Claude 재량에 의존 |
| **컨텍스트 소비** | 지침이 컨텍스트 일부 사용 |

---

## 6. 아카이브: 원래 구현 (참고용)

### 원래 실행 흐름 (동작하지 않음)

```
┌─────────────────────────────────────────────────────────────┐
│                    Stop Hook 실행 흐름 (실패)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  사용자 입력                                                 │
│       │                                                     │
│       ▼                                                     │
│  Claude 응답 생성                                            │
│       │                                                     │
│       ▼                                                     │
│  응답 완료 (Stop 이벤트)                                     │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────┐                    │
│  │     auto-memory-save.sh 실행        │                    │
│  │           ↓                         │                    │
│  │   hookSpecificOutput 반환           │                    │
│  │           ↓                         │                    │
│  │   ❌ 스키마 에러 발생                │                    │
│  └─────────────────────────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 원래 스크립트 (auto-memory-save.sh)

```bash
#!/bin/bash
# Claude Code Stop Hook - 자동 메모리 저장
# 상태: 실패 (스키마 불일치)

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
# ❌ 이 출력이 Stop hook 스키마와 맞지 않음
cat << 'EOF'
{
  "decision": "block",
  "hookSpecificOutput": {
    "additionalContext": "\n\n🧠 [AUTO-MEMORY-SAVE]\n이 작업을 ~/.claude/memory/에 저장해주세요.\n\n저장 형식:\n- 파일명: YYMM_SEQ_keyword.md\n- 체인/에이전트/스킬/도구 사용 내역 포함\n- 간결하게 핵심만 기록\n\n저장 후 '💾 메모리 저장 완료'라고 알려주세요."
  }
}
EOF
```

---

## 7. 교훈 및 향후 참고

### 학습 포인트

| 항목 | 교훈 |
|------|------|
| **Hook 스키마** | 각 Hook 타입별 지원 필드가 다름 |
| **Stop Hook 한계** | 응답 완료 후 실행되어 새 지시 주입 불가 |
| **대안 탐색** | Hook 실패 시 지침 기반 접근이 유효함 |

### Hook 사용 가이드

| 목적 | 적합한 Hook |
|------|------------|
| 프롬프트 전처리 | UserPromptSubmit |
| 도구 실행 전 검증 | PreToolUse |
| 도구 실행 후 처리 | PostToolUse |
| 세션 시작 알림 | SessionStart |
| **응답 후 작업** | ❌ Hook 불가 → **지침 기반** |

---

## 관련 문서

- [[012_Skills-vs-Subagent-Structural-Analysis]] - 후속 분석 및 수정
- [[009_UserPromptSubmit-Hook-Auto-Analysis]] - UserPromptSubmit 훅 시스템
- [[007_Claude-Code-Settings-Configuration]] - Claude Code 설정 전체
- [[CLAUDE.md]] - 통합 가이드라인 V3.6

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-03 | 1.0 | Stop Hook 자동 메모리 저장 구현 |
| 2026-02-03 | 2.0 | **실패 확인** - 스키마 불일치로 동작 안 함 |
| 2026-02-03 | 2.1 | **지침 기반으로 전환** - CLAUDE.md V3.6 |

---

*Stop Hook Auto Memory Save System - 실패 → 지침 기반 전환 (2026-02-03)*
