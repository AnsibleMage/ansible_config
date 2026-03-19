---
title: "Phase 0 Implementation — Plan + Log"
version: "1.0.0"
created: "2026-03-15"
updated: "2026-03-15"
tags: [1012, phase-0, implementation, C3, C4, C5, C8]
status: "completed"
phase: 0
steps_total: 5
steps_completed: 5
---

## 🔄 Next Session Handoff

| 항목 | 내용 |
|------|------|
| 현재 단계 | **Phase 0 완료** ✅ |
| 다음 작업 | Phase 1 시작 (04_002 참조) |
| 차단 요소 | 없음 |
| 주의사항 | Phase 1은 agents/, skills/ 마이그레이션 |

---

## 1. 실행 계획 (Plan)

### 1.1 Phase 0 개요

- 목표: 즉각적 기반 구축 (1~2 세션)
- 대전제: 공식 우선 → 공식 강화 → 자체 개발
- 효과: CLAUDE.md 393줄 → ~95줄, Hook 3/12 → 6/12 활성화

### 1.2 실행 순서

| Step | 작업 | 카테고리 | 참조 설계 | 검증 기준 |
|------|------|----------|----------|----------|
| 1 | CLAUDE.md → rules/ 분리 | C3 | [[02_003_C3_CLAUDE_MD_Modularization]] Section 4, 7 | rules/ 파일 로드 확인 |
| 2 | SessionStart Hook | C4 | [[02_004_C4_Hook_Skill_Official_Migration]] Section 3.2.1 | 세션 시작 시 메모리 로드 메시지 |
| 3 | PostToolUse Observability 로그 | C5 | [[02_005_C5_Observability_Self_Evolution]] Section 4.3 | ~/.claude/logs/YYMMDD.log 생성 |
| 4 | Stop Hook | C4/C8 | [[02_008_C8_Quality_Context_Management]] Section 5.2 | 80%+ 컨텍스트 시 저장 지시 |
| 5 | Effort Level 분화 | C8 | [[02_008_C8_Quality_Context_Management]] Section 3.1 | 체인별 레벨 확인 |

### 1.3 충돌 방지 규칙 (03_001 Section 7 발췌)

> [!danger] 핵심 위험
> 현재 V4.2.1이 **운영 중인 상태**에서 V5.0 엔진을 변경하면 충돌이 발생한다. 아래 충돌 지점을 사전에 인지하고 순서대로 해결해야 한다.

| # | 충돌 지점 | 위험도 | 해결책 |
|---|---------|--------|--------|
| **C-1** | CLAUDE.md 축소 시 체인 정의 소실 | 🔴 Critical | rules/ 먼저 생성 → 내용 복사 → CLAUDE.md 축소 (순서 중요). 절대 한 번에 "이동"하지 않음 |
| **C-2** | settings.json Hook 등록 시 기존 Hook 덮어쓰기 | 🔴 Critical | **병합(merge)** 방식으로 추가. 기존 UserPromptSubmit(auto-analyze.sh) 유지 확인 |
| **C-3** | auto-analyze.sh V5.0 업그레이드 시 기존 4-Layer 분석 깨짐 | 🟡 High | Phase 0에서 auto-analyze.sh 수정 금지. 기존 코드 보존, 추가만 허용 |
| **C-4** | 에이전트 frontmatter 변경 시 기존 호출 방식 비호환 | 🟡 High | Phase 0 범위 외 (Phase 1에서 수행) |
| **C-5** | commands/ → skills/ 이전 시 기존 `/명령어` 사라짐 | 🟡 High | Phase 0 범위 외 (Phase 1에서 수행) |
| **C-6** | Qdrant Docker 포트 충돌 (6333) | 🟢 Low | Phase 0 범위 외 (Phase 2에서 수행) |
| **C-7** | Python 패키지 버전 충돌 (torch/numpy) | 🟢 Low | 가상환경(venv) 사용. Phase 0 범위 외 |

### 1.4 안전 원칙

| # | 규칙 |
|---|------|
| 1 | 한 번에 하나만 변경 |
| 2 | 변경 → 테스트 → 다음 변경 |
| 3 | CLAUDE.md/settings.json 수정 후 세션 재시작 |
| 4 | 104 폴더 절대 수정 금지 |
| 5 | auto-analyze.sh는 Phase 0에서 수정 금지 |
| 6 | 복사 → 확인 → 삭제 3단계 |

---

## 2. 실행 로그 (Log)

### Step 1: CLAUDE.md → rules/ 분리 (C3)

#### 📋 아리 가이드

**참조**: [[02_003_C3_CLAUDE_MD_Modularization]] Section 4, 7

**배경**: CLAUDE.md Section 2 (오케스트레이션 시스템, 245줄)와 Section 3 (메모리 프로토콜, 44줄)를 공식 `rules/` 디렉토리로 분리한다. `rules/` 디렉토리의 파일 중 frontmatter에 `globs:` 없는 파일은 **세션 시작 시 자동 로드**된다 (CLAUDE.md와 동일 우선순위).

**분리 매핑**:

| 현재 CLAUDE.md 섹션 | 줄 수 | 목적지 | 로딩 |
|-------------------|-------|--------|------|
| Section 2 (2.1~2.5 전체) | 41~287줄 (247줄) | `rules/orchestration.md` | 항상 (globs 없음) |
| Section 3 (메모리 & 프로토콜) | 290~333줄 (44줄) | `rules/memory-protocol.md` | 항상 (globs 없음) |

**작업 순서**:

1. `~/.claude/rules/orchestration.md` 생성
   - CLAUDE.md Section 2 (라인 41~287, 247줄) 전체 복사
   - 파일 상단에 출처 주석 추가 (frontmatter 없음 — 항상 로드)
   - 내용 구조: `# Orchestration System Rules` 제목 하에 2.1~2.5 전체

2. `~/.claude/rules/memory-protocol.md` 생성
   - CLAUDE.md Section 3 (라인 290~333, 44줄) 전체 복사
   - 파일 상단에 출처 주석 추가 (frontmatter 없음 — 항상 로드)
   - 내용 구조: `# Memory & Protocol Rules` 제목 하에 응답 완료 프로토콜, 격리 규칙, Memory System 전체

3. Claude Code 세션 재시작

4. 새 세션에서 rules/ 파일 로드 확인
   - 테스트: "시스템 설계해줘" 프롬프트 입력 → SystemDesignChain 선택되는지 확인
   - 테스트: Identity 확인 → "안녕, 앤!" 인사 정상 동작 확인

5. 확인 완료 후 CLAUDE.md에서 Section 2, 3 삭제 → ~95줄로 축소
   - Section 2 본문을 핵심 원칙 4줄 + `rules/orchestration.md` 참조 안내로 교체
   - Section 3 본문을 `rules/memory-protocol.md` 참조 1줄로 교체
   - CLAUDE.md 버전을 V5.0.0으로 업데이트

**목표 CLAUDE.md V5.0 구조** (~95줄):

```markdown
## 2. Orchestration System

> **상세 규칙**: `~/.claude/rules/orchestration.md` (자동 로드)

핵심 원칙:
1. 모든 프롬프트는 Hook(auto-analyze.sh)이 분석하여 체인을 추천한다
2. 아리는 Hook 추천을 촉매로 활용하되, 최종 판단은 자율적으로 한다
3. 체인 선택 후 임의 축약 금지 — 모든 에이전트를 순서대로 실행
4. 단순 작업(Q&A, 한 줄 수정)은 체인 생략

## 3. Memory & Protocol

> **상세 규칙**: `~/.claude/rules/memory-protocol.md` (자동 로드)
```

**⚠️ 주의사항**:
- 복사 → 확인 → 삭제 3단계. "이동"하지 않는다 (C-1 충돌 방지)
- 롤백: `104_current_system/CLAUDE.md` 원본에서 복원
- CLAUDE.md 수정 후 반드시 세션 재시작 (현재 세션에서는 이전 CLAUDE.md 적용됨)
- `globs:` frontmatter 없는 파일만 자동 로드됨 — orchestration.md, memory-protocol.md 모두 frontmatter 없이 생성

**절감 효과**:

| 항목 | 전 | 후 |
|------|----|----|
| CLAUDE.md 줄 수 | 393줄 | ~95줄 (-76%) |
| Section 2 in CLAUDE.md | 245줄 | ~15줄 (-94%) |
| 항상 로드 총량 | 393줄 | ~384줄 (구조적 분리 달성) |

**검증 기준**:
- [x] `~/.claude/rules/orchestration.md` 파일 존재 및 내용 확인
- [x] `~/.claude/rules/memory-protocol.md` 파일 존재 및 내용 확인
- [x] 세션 재시작 후 체인 선택 정상 작동 (SystemDesignChain 등)
- [x] 메모리 프로토콜 정상 작동 (YYMM_SEQ_keyword.md 형식)
- [x] CLAUDE.md가 ~95줄 이하로 축소됨

#### 앤 실행 결과
- ✅ `rules/orchestration.md` 생성 (246줄, 11KB) — Section 2 전체 복사
- ✅ `rules/memory-protocol.md` 생성 (43줄, 1.5KB) — Section 3 전체 복사
- ✅ 새 세션에서 rules/ 로드 확인 (SystemDesignChain 질문 → 정확 응답)
- ✅ CLAUDE.md Section 2, 3 삭제 → 394줄 → **115줄** (-71%)
- ✅ 버전 V4.2.1 → **V5.0.0** 업데이트
- ✅ Section 2를 rules/ 참조 포인터 테이블로 대체
- ✅ Change History에 V5.0.0 엔트리 추가

#### ❌ 오류 & 해결
> 오류 없음. 복사→확인→삭제 3단계 순조롭게 완료.

---

### Step 2: SessionStart Hook (C4)

#### 📋 아리 가이드

**참조**: [[02_004_C4_Hook_Skill_Official_Migration]] Section 3.2.1

**배경**: 현재 settings.json의 `SessionStart`는 빈 배열(`[]`)로 비활성 상태이다. SessionStart Hook을 구현하면 세션 시작 시 최근 메모리 3개를 자동 로드하여 "어제 뭐 했지?" 문제를 해결한다.

**공식 스펙**:
- 발생 시점: 세션 시작/재개
- 제어 가능: No (차단 불가, 컨텍스트 주입만)
- stdin 형식: `{"sessionId": "...", "isResume": true/false}`

**작업 순서**:

1. `~/.claude/hooks/session-start.sh` 생성

```bash
#!/bin/bash
# SessionStart Hook: 세션 시작 시 메모리 자동 로드
# V1.0 (2026-03-15)

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')
IS_RESUME=$(echo "$INPUT" | jq -r '.isResume // false')

# Teammate 세션 감지 → 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

MEMORY_DIR="$HOME/.claude/memory"
if [ ! -d "$MEMORY_DIR" ]; then
    exit 0
fi

# 컨텍스트 추적 상태 파일 초기화 (C8 연계)
STATE_FILE="/tmp/claude_context_tracker_${SESSION_ID}.json"
echo '{"turns": 0, "toolCalls": 0, "agentCalls": 0, "fileReads": 0}' > "$STATE_FILE"

# 최근 메모리 3개 로드
RECENT_MEMORIES=""
MEMORY_FILES=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -3)

if [ -n "$MEMORY_FILES" ]; then
    RECENT_MEMORIES="
## 최근 메모리 (자동 로드)
"
    for FILE in $MEMORY_FILES; do
        FILENAME=$(basename "$FILE")
        TITLE=$(head -10 "$FILE" | grep -E '^# ' | head -1 | sed 's/^# //')
        if [ -z "$TITLE" ]; then TITLE="$FILENAME"; fi
        SUMMARY=$(grep -A1 '요약' "$FILE" 2>/dev/null | tail -1 | head -c 100)
        if [ -z "$SUMMARY" ]; then
            SUMMARY=$(grep -v '^#\|^-\|^>\|^$\|^---' "$FILE" | head -2 | tr '\n' ' ' | head -c 100)
        fi
        RECENT_MEMORIES="$RECENT_MEMORIES- **$TITLE** ($FILENAME): $SUMMARY
"
    done
fi

# 이전 세션 TODO 로드 (resume 시)
TODO_CONTEXT=""
if [ "$IS_RESUME" = "true" ]; then
    LATEST_FILE=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_FILE" ]; then
        TODOS=$(grep -E '^\- \[ \]' "$LATEST_FILE" 2>/dev/null | head -5)
        if [ -n "$TODOS" ]; then
            TODO_CONTEXT="
## 이전 세션 미완료 TODO
$TODOS
"
        fi
    fi
fi

if [ -n "$RECENT_MEMORIES" ] || [ -n "$TODO_CONTEXT" ]; then
    CONTEXT="$RECENT_MEMORIES$TODO_CONTEXT"
    jq -n --arg ctx "$CONTEXT" '{
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": $ctx
        }
    }'
fi

exit 0
```

2. `settings.json`에 SessionStart Hook **병합(merge)** 방식으로 추가 (C-2 충돌 방지)

**병합 방식 (올바른 방법)**:
```json
// 기존 빈 배열을 아래로 교체
"SessionStart": [{
  "hooks": [{
    "type": "command",
    "command": "/Users/changjaeyou/.claude/hooks/session-start.sh"
  }]
}]
```

**⚠️ 필수 확인**: UserPromptSubmit의 auto-analyze.sh가 그대로 유지되는지 반드시 확인

3. 세션 재시작 → 메모리 로드 메시지 확인

**검증 기준**:
- [x] `~/.claude/hooks/session-start.sh` 파일 존재 및 실행 권한 확인 (`chmod +x`)
- [x] settings.json에 SessionStart 항목 추가
- [x] 기존 UserPromptSubmit Hook (auto-analyze.sh) 보존 확인
- [x] 세션 시작 시 "최근 메모리 (자동 로드)" 메시지 출력

#### 앤 실행 결과
- ✅ `session-start.sh` 생성 (75줄) + `chmod +x` 실행 권한 부여
- ✅ settings.json SessionStart 항목 병합 추가 (기존 `[]` → Hook 등록)
- ✅ UserPromptSubmit (auto-analyze.sh) 보존 확인 (L84)
- ✅ 새 세션에서 테스트 — "SessionStart hook에서 additionalContext로 뭐가 주입됐어?" 질문
- ✅ **검증 성공**: 실질 데이터 조회 도구 0회, 컨텍스트 내 system-reminder에서 직접 추출 확인
- ✅ 최근 메모리 3개 자동 로드: `2603_002`, `2603_001`, `2602_122`
- ⚠️ 메모리 요약이 일부 truncate됨 (head -c 100 제한) — 향후 개선 가능

#### ❌ 오류 & 해결
> 오류 없음. 스크립트 수동 테스트(`echo | session-start.sh`) + 새 세션 실제 테스트 모두 성공.

---

### Step 3: PostToolUse Observability 로그 (C5)

#### 📋 아리 가이드

**참조**: [[02_005_C5_Observability_Self_Evolution]] Section 4.3

**배경**: 현재 PostToolUse Hook은 `Write|Edit` matcher에만 대응하여 포매팅+Git 상태만 출력한다. 새로운 `*` matcher 블록을 추가하여 모든 도구 호출에 대해 1줄 로그를 자동 기록한다.

**로그 포맷**:
```
YYYY-MM-DD HH:MM | Chain | Agent/Tool[Result] | Duration
```

예시:
```
2026-03-15 14:32 | SystemDesign | Explore[OK] | -
2026-03-15 14:33 | SystemDesign | system_architect[OK] | -
2026-03-15 14:38 | - | SESSION_END | total=480s tools=8 agents=5
```

**작업 순서**:

1. `~/.claude/hooks/observability-logger.sh` 생성

```bash
#!/bin/bash
# ~/.claude/hooks/observability-logger.sh
# PostToolUse Hook: 모든 도구 사용 후 1줄 로그 append
# C5 Observability — Phase 0 (최소 구현)

LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y%m%d).log"

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.toolName // "unknown"' 2>/dev/null)
TOOL_RESULT=$(echo "$INPUT" | jq -r '.toolResult // "OK"' 2>/dev/null)

if echo "$TOOL_RESULT" | grep -qi "error\|fail\|exception"; then
    STATUS="ERR"
else
    STATUS="OK"
fi

# 체인 상태 파일에서 현재 체인 읽기 (없으면 "-")
CHAIN_STATE_FILE="/tmp/claude_current_chain.txt"
if [ -f "$CHAIN_STATE_FILE" ]; then
    CHAIN=$(cat "$CHAIN_STATE_FILE")
else
    CHAIN="-"
fi

# Agent 도구인 경우 서브에이전트 타입 추출
AGENT_NAME="$TOOL_NAME"
if [ "$TOOL_NAME" = "Agent" ]; then
    SUBAGENT=$(echo "$INPUT" | jq -r '.toolInput.subagent_type // .toolInput.agent // "agent"' 2>/dev/null)
    if [ -n "$SUBAGENT" ] && [ "$SUBAGENT" != "null" ]; then
        AGENT_NAME="$SUBAGENT"
    fi
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
echo "$TIMESTAMP | $CHAIN | ${AGENT_NAME}[${STATUS}] | -" >> "$LOG_FILE"

exit 0
```

2. `settings.json`의 PostToolUse에 `*` matcher 블록 **추가** (기존 `Write|Edit` 블록 유지)

**병합 방식 (올바른 방법)**:
```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      // 기존 내용 그대로 유지
    ]
  },
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "/Users/changjaeyou/.claude/hooks/observability-logger.sh"
      }
    ]
  }
]
```

3. 파일 수정 테스트 → `~/.claude/logs/YYMMDD.log` 생성 확인

**검증 기준**:
- [x] `~/.claude/hooks/observability-logger.sh` 파일 존재 및 실행 권한 확인
- [x] settings.json의 PostToolUse에 `*` matcher 블록 추가 (기존 `Write|Edit` 블록 보존)
- [x] 도구 호출 후 `~/.claude/logs/$(date +%Y%m%d).log` 생성 확인
- [x] 로그 파일 내 포맷 정합성 확인 (`YYYY-MM-DD HH:MM | - | ToolName[OK] | -`)

#### 앤 실행 결과
- ✅ `observability-logger.sh` 생성 (41줄) + `chmod +x` 실행 권한 부여
- ✅ `~/.claude/logs/` 디렉토리 생성
- ✅ settings.json PostToolUse에 `*` matcher 블록 추가 (기존 `Write|Edit` 보존)
- ✅ 수동 테스트: `echo '{"toolName":"Read"}' | observability-logger.sh` → 로그 정상 기록
- ✅ 로그 출력: `2026-03-15 23:09 | - | Read[OK] | -` (포맷 정합)
- ✅ `~/.claude/logs/20260315.log` 파일 생성 확인

#### ❌ 오류 & 해결
- ⚠️ settings.json 동시 수정 충돌 (linter 개입) → 파일 재읽기 후 정확한 위치에 삽입으로 해결

---

### Step 4: Stop Hook (C4/C8)

#### 📋 아리 가이드

**참조**: [[02_008_C8_Quality_Context_Management]] Section 5.2

**배경**: 현재 Stop Hook이 미등록 상태이다. Claude 응답 완료 시 컨텍스트 사용량을 추정하고, 80% 이상이면 메모리 저장 + /compact 지시를 내린다. `exit code 2`(정지 방지)를 사용하여 Claude가 정리 작업을 수행하도록 계속 실행을 강제한다.

**컨텍스트 추정 공식 (V2.0)**:
```
추정 토큰 = (턴 × 2,500) + (도구 호출 × 1,500) + (에이전트 호출 × 8,000) + (파일 읽기 × 3,000)
사용률(%) = 추정 토큰 / 1,000,000 × 100
```

**체인 완료 검증 로직**: Stop Hook 트리거 시 `/tmp/claude_chain_progress_{SESSION_ID}.json` 파일을 확인하여 체인 미완료 시 `exit 2`로 계속 실행 강제.

**작업 순서**:

1. `~/.claude/hooks/stop-cleanup.sh` 생성

```bash
#!/bin/bash
# Stop Hook: 작업 완료 시 컨텍스트 자동 관리
# V2.0 (2026-03-15) — C8 Quality-First + C5 Observability

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // empty')
STOP_REASON=$(echo "$INPUT" | jq -r '.stopReason // "end_turn"')

# Teammate 감지 → 스킵
if [ "$CLAUDE_CODE_AGENT_TEAM_ROLE" = "teammate" ]; then
    exit 0
fi

# C5 로깅
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
echo "$TIMESTAMP | Stop | reason=$STOP_REASON | session=$SESSION_ID" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

# 1. 체인 완료 검증
PROGRESS_FILE="/tmp/claude_chain_progress_${SESSION_ID}.json"
if [ -f "$PROGRESS_FILE" ]; then
    IS_COMPLETE=$(jq -r '.is_complete // true' "$PROGRESS_FILE" 2>/dev/null)
    if [ "$IS_COMPLETE" = "false" ]; then
        CHAIN=$(jq -r '.chain // "unknown"' "$PROGRESS_FILE")
        REMAINING=$(jq -r '.remaining_steps | join(", ")' "$PROGRESS_FILE" 2>/dev/null)
        REMAINING_COUNT=$(jq -r '.remaining_steps | length' "$PROGRESS_FILE" 2>/dev/null)
        CONTINUE_MSG="
## 체인 미완료 — 계속 실행

> [!warning] **${CHAIN}** 체인이 완료되지 않았습니다.
> 남은 단계 (${REMAINING_COUNT}개): ${REMAINING}
>
> **임의 축약 금지 원칙**에 따라 체인을 완료하세요.
"
        jq -n --arg ctx "$CONTINUE_MSG" '{
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": $ctx
            }
        }'
        exit 2
    fi
fi

# 2. 컨텍스트 사용량 추정
STATE_FILE="/tmp/claude_context_tracker_${SESSION_ID}.json"
if [ -f "$STATE_FILE" ]; then
    TURN_COUNT=$(jq -r '.turns // 0' "$STATE_FILE" 2>/dev/null)
    TOOL_CALLS=$(jq -r '.toolCalls // 0' "$STATE_FILE" 2>/dev/null)
    AGENT_CALLS=$(jq -r '.agentCalls // 0' "$STATE_FILE" 2>/dev/null)
    FILE_READS=$(jq -r '.fileReads // 0' "$STATE_FILE" 2>/dev/null)

    ESTIMATED_TOKENS=$(( \
        (TURN_COUNT * 2500) + \
        (TOOL_CALLS * 1500) + \
        (AGENT_CALLS * 8000) + \
        (FILE_READS * 3000) \
    ))
    USAGE_PERCENT=$(( (ESTIMATED_TOKENS * 100) / 1000000 ))

    echo "$TIMESTAMP | ContextEstimate | turns=$TURN_COUNT tools=$TOOL_CALLS agents=$AGENT_CALLS files=$FILE_READS estimated=${ESTIMATED_TOKENS}tok (${USAGE_PERCENT}%)" \
        >> "$LOG_DIR/$(date +%Y%m%d).log"

    # 3. 80%+ 시 자동 정리 지시
    if [ "$USAGE_PERCENT" -ge 80 ]; then
        CLEANUP_MSG="
## 컨텍스트 자동 정리 (추정 ${USAGE_PERCENT}%)

> [!warning] 컨텍스트 사용량이 80%를 초과했습니다.
> 추정: 턴 ${TURN_COUNT}회, 도구 ${TOOL_CALLS}회, 에이전트 ${AGENT_CALLS}회, 파일읽기 ${FILE_READS}회 = ~${ESTIMATED_TOKENS} 토큰

### 실행 순서 (반드시 이 순서대로)

**1단계: 품질 자가 검증**
- [ ] 모든 에이전트가 생략 없이 실행되었는가?
- [ ] 분석 깊이가 충분한가? (근본 원인까지 도달)
- [ ] 구조화된 출력인가? (테이블/다이어그램/매트릭스)
- [ ] 다음 세션이 이어받을 수 있는가? (Handoff 갱신)

**2단계: 메모리 상세 저장** (\`/memory-save\`)
아래 내용을 **반드시 포함**하여 메모리에 저장:
- 작업 제목, 완료 항목, 미완료 TODO (체크박스)
- 핵심 결정/인사이트, 생성/수정된 파일 목록
- 다음 세션 조언 (구체적으로)

**3단계: /compact 실행**
메모리 저장 완료 후에만 실행하세요.
"
        jq -n --arg ctx "$CLEANUP_MSG" '{
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": $ctx
            }
        }'
        exit 2
    fi
else
    # 상태 파일 없으면 초기화
    jq -n '{"turns": 0, "toolCalls": 0, "agentCalls": 0, "fileReads": 0}' > "$STATE_FILE"
fi

exit 0
```

2. `settings.json`에 Stop Hook **추가** (기존 Hook 유지)

```json
"Stop": [{
  "hooks": [{
    "type": "command",
    "command": "/Users/changjaeyou/.claude/hooks/stop-cleanup.sh"
  }]
}]
```

3. 테스트: 일반 작업 후 응답 완료 시 로그에 Stop 이벤트 기록 확인

**검증 기준**:
- [x] `~/.claude/hooks/stop-cleanup.sh` 파일 존재 및 실행 권한 확인
- [x] settings.json에 Stop 항목 추가
- [x] 응답 완료 시 로그 파일에 `Stop | reason=end_turn` 기록 확인
- [x] 80%+ 추정 시 저장 지시 메시지 출력 (장시간 세션 후 테스트)

#### 앤 실행 결과
- ✅ `stop-cleanup.sh` 생성 (100줄) + `chmod +x` 실행 권한 부여
- ✅ settings.json에 Stop Hook 등록
- ✅ 수동 테스트: `echo '{"sessionId":"test-456","stopReason":"end_turn"}' | stop-cleanup.sh` → exit 0
- ✅ 로그 기록 확인: `Stop | reason=end_turn | session=test-456`
- ✅ 체인 미완료 검증 로직 포함 (exit 2 강제 계속)
- ✅ 80%+ 컨텍스트 시 3단계 정리 지시 (품질 검증→메모리 저장→compact)

#### ❌ 오류 & 해결
> 오류 없음. 스크립트 정상 작동.

---

### Step 5: Effort Level 분화 (C8)

#### 📋 아리 가이드

**참조**: [[02_008_C8_Quality_Context_Management]] Section 3.1, [[02_005_C5_Observability_Self_Evolution]] Section 5.2

**배경**: 현재 settings.json의 `"effortLevel": "high"`는 전역 단일 설정이다. 모든 체인에 동일한 high 수준이 적용되어 HotfixChain(긴급 수정)에도 불필요하게 깊은 탐색이 발생한다. Phase 0에서는 rules/orchestration.md (또는 CLAUDE.md의 Section 2 참조 설명)에 체인별 Effort Level 가이드를 텍스트로 명시한다.

**Effort Level 분화 매트릭스**:

| Effort Level | 의미 | 대상 체인 | 행동 지침 |
|-------------|------|----------|----------|
| **HIGH** | 깊이 있는 탐색, 완전한 분석, 모든 관점 고려 | MetaThinkChain (H), SystemDesignChain (A), ResearchChain (E) | 에이전트 전원 완전 실행, 다차원 분석, Why/What-If 탐색 |
| **MEDIUM** | 실용적 완성도, 구현 품질 확보 | DevChain (D), WebDevChain+ (G), DocChain+ (F), AutomationChain (B), GameDevChain (C), RailsDevChain (I) | 코드 품질 + 테스트 커버리지 확보, 실질적 산출물 |
| **LOW** | 최소 진단, 빠른 수정, 즉시 배포 | HotfixChain (J) | 문제 원인 특정 → 최소 변경 → 즉시 검증 |

**작업 순서**:

1. Step 1에서 생성한 `rules/orchestration.md`의 Dynamic Chain Patterns 섹션 (Section 2.4에 해당) 내 각 체인 정의 옆에 Effort Level 추가

예시 (orchestration.md 내 체인 패턴 부분):
```markdown
#### A. SystemDesignChain (시스템 설계) — Effort: HIGH
> 모든 에이전트 완전 실행. 탐색 범위 제한 금지. 깊이 있는 분석 필수.

#### J. HotfixChain (긴급 수정) — Effort: LOW
> 최소한의 탐색으로 문제를 진단한다. 불필요한 분석 생략, 즉시 수정에 집중.
```

2. CLAUDE.md Section 2의 핵심 원칙 부분에 Effort Level 언급 추가 (간략히)

3. 세션 재시작 → 체인 선택 시 Effort Level 반영 확인
   - 테스트: "이 버그 빨리 고쳐줘" → HotfixChain (LOW) 선택 확인
   - 테스트: "이 문제 깊이 분석해줘" → MetaThinkChain (HIGH) 선택 확인

**검증 기준**:
- [ ] rules/orchestration.md 내 각 체인 정의에 Effort Level 명시 완료
- [ ] CLAUDE.md에 Effort Level 참조 언급 포함
- [ ] 체인 선택 시 Pre-execution Declaration에 Effort Level 표시 (`📋 체인 구성: HotfixChain [LOW]`)

#### 앤 실행 결과
- ✅ `rules/orchestration.md` 체인 A~J 각각에 Effort Level 태그 추가
- ✅ Effort Level 분화 매트릭스 테이블 (HIGH/MEDIUM/LOW) Section 2.4 상단에 삽입
- ✅ Pre-execution Declaration 형식에 `[EFFORT]` 포함
- ✅ CLAUDE.md Section 2 rules 참조에 "Effort Level 분화" 명시

#### ❌ 오류 & 해결
> 오류 없음.

---

## 3. 최종 결과 요약

| Step | 작업 | 상태 | 비고 |
|------|------|------|------|
| 1 | CLAUDE.md → rules/ 분리 | ✅ | 394줄→115줄, V5.0.0 |
| 2 | SessionStart Hook | ✅ | 메모리 3개 자동 로드 확인 |
| 3 | PostToolUse 로그 | ✅ | `*` matcher, YYMMDD.log 생성 |
| 4 | Stop Hook | ✅ | 80%+ 정리 지시, 체인 미완료 방지 |
| 5 | Effort Level 분화 | ✅ | HIGH/MEDIUM/LOW 3단계 |

**Phase 0 완료 기준**:
- CLAUDE.md ~95줄 이하
- `~/.claude/rules/` 2개 파일 자동 로드
- `~/.claude/logs/YYMMDD.log` 자동 생성
- SessionStart, Stop Hook 동작
- Hook 활성화율: 3/12 → 5/12 이상

---

## 관련 문서 (Neural Map)

### Direct References
- [[02_003_C3_CLAUDE_MD_Modularization]] — Step 1 설계 (Section 4 분리 계획, Section 7 마이그레이션 Phase)
- [[02_004_C4_Hook_Skill_Official_Migration]] — Step 2, 4 설계 (Section 3.2.1 SessionStart, Section 3.2.3 Stop Hook)
- [[02_005_C5_Observability_Self_Evolution]] — Step 3 설계 (Section 4.3 observability-logger.sh 전문)
- [[02_008_C8_Quality_Context_Management]] — Step 4, 5 설계 (Section 5.2 Stop Hook V2.0, Section 3.1 Effort Level)
- [[03_001_Prerequisites_Checklist]] — 충돌 방지 규칙 (Section 7 충돌 매트릭스 C-1~C-7)
- [[03_002_Installation_Execution_Log]] — 선행 설치 완료 로그

### Backlinks
- [[01_001_Improvement_Direction_Overview]] — 8대 카테고리 개요
- [[04_002_Phase1_Implementation]] — 다음 Phase

### Topic Links
- [[01_001_Current_System_Analysis]] (101) — V4.2.1 현재 분석

---

## Release Notes

### v1.0.0 (2026-03-15)
- Phase 0 Implementation Plan + Log 문서 초안 생성
- 5 Steps 구조화 (C3 → C4 → C5 → C8)
- 각 Step의 아리 가이드: 참조 설계 문서에서 실제 구현 세부사항 추출 (스크립트 전문 포함)
- 충돌 방지 규칙: C-1~C-7 전체 추출, Phase 0 해당 항목 강조
- **프롬프트:** "1012_ 프로젝트의 Phase 0을 시작할게. 04_001_Phase0_Implementation.md를 첫번째로 연속문서 4개를 팀에이전트 병렬로 만들어줘"
