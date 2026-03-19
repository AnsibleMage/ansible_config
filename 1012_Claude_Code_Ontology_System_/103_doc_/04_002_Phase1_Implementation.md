---
title: "Phase 1 Implementation — Plan + Log"
version: "1.1.0"
created: "2026-03-15"
updated: "2026-03-17"
tags: [1012, phase-1, implementation, C2, C4]
status: "completed"
phase: 1
steps_total: 5
steps_completed: 5
---

## 🔄 Next Session Handoff

| 항목 | 내용 |
|------|------|
| 현재 단계 | **Phase 1 완료** ✅ |
| 다음 작업 | Phase 2 시작 (04_003 참조) |
| 차단 요소 | 없음 |
| 주의사항 | commands/ 원본 유지 중 (C-5 공존 기간) |

---

# Phase 1 Implementation — Plan + Log

> **Phase**: 1 — 공식 전환 (단기, 3~5세션)
> **선행 조건**: [[04_001_Phase0_Implementation]] 완료
> **주요 카테고리**: [[02_002_C2_Parallel_System_Official_Migration|C2 병렬 시스템]] + [[02_004_C4_Hook_Skill_Official_Migration|C4 Hook & Skill 전환]]

---

## 1. 실행 계획 (Plan)

### 1.1 Phase 1 개요

| 항목 | 내용 |
|------|------|
| 목표 | 공식 기능 전환 — 에이전트 마이그레이션, 스킬 이전, Hook 확장 완성 |
| 예상 세션 수 | 3~5세션 |
| 범위 | agents/ frontmatter 업그레이드, commands/ → skills/ 마이그레이션, 보조 Hook 추가 |
| 선행 조건 | Phase 0 완료 — rules/, hooks/ 기반 구조 구축, SessionStart/Stop/PostCompact Hook 동작 확인 |
| 카테고리 | C2 (병렬 시스템 공식 전환) + C4 (Hook & Skill 공식 체계 전환) |

**Phase 1이 달성하는 것**:
- 에이전트 14개의 frontmatter에 공식 필드(`memory`, `maxTurns`) 추가 → 공식 서브에이전트 기능 활성화
- 보조 Hook 2개(InstructionsLoaded, TeammateIdle) 구현 → Hook 활성화 3/12 → 8/12 완성
- commands/ 13개 → skills/ 마이그레이션 착수 (그룹 A, B 우선) → 공식 스킬 시스템 정합
- CLAUDE.md Section 2.4 체인 정의 → skills/chains/ 스킬화 프로토타입 → 자연어 의존 탈피

**Phase 1이 달성하지 않는 것**:
- 벡터 DB 연동 (Phase 2 범위)
- auto-analyze.sh 수정 (Phase 2 범위 — C-3 충돌 규칙)
- prompt/agent Hook 타입 도입 (Phase 4 범위)

---

### 1.2 실행 순서

#### 단계 테이블

| 단계 | 작업 | 카테고리 | 산출물 | 충돌 위험 |
|------|------|---------|--------|----------|
| **Step 1** | 에이전트 14개 frontmatter 업그레이드 | C2 | 14개 에이전트 수정본 | C-4 (기존 필드 유지 필수) |
| **Step 2** | InstructionsLoaded Hook 구현 + 등록 | C4 | `instructions-loaded.sh` + settings.json | C-2 (기존 Hook 유지 필수) |
| **Step 3** | TeammateIdle Hook 구현 + 등록 | C4 | `teammate-idle.sh` + settings.json | C-2 (기존 Hook 유지 필수) |
| **Step 4** | commands/ → skills/ 마이그레이션 (그룹 A: Git + 그룹 B: 유틸) | C4 | 6개 스킬 디렉토리 | C-5 (양쪽 공존 유지) |
| **Step 5** | 체인 A~J → skills/chains/ 스킬화 프로토타입 (SystemDesignChain 먼저) | C2 | `skills/chains/system-design.md` 포함 최소 1개 | — |

---

### 1.3 Step별 상세 계획

#### Step 1 — 에이전트 14개 frontmatter 업그레이드 (C2)

**근거**: [[02_002_C2_Parallel_System_Official_Migration#3. 에이전트 마이그레이션 설계|C2 에이전트 마이그레이션]]

**목표**: 현재 `name`, `description`, `subagent_type`, `model` 4개 필드만 있는 frontmatter에 공식 필드 3개 추가.

**충돌 규칙 C-4 (필독)**:
> 기존 필드는 절대 삭제/수정하지 않고 신규 필드만 추가. 1개씩 변경 후 테스트.

**변경 전/후 예시**:

```yaml
# 변경 전 (현재 모든 에이전트)
---
name: insight_explorer
description: Deep observation and pattern recognition specialist...
subagent_type: insight_explorer
model: sonnet
---

# 변경 후 (기존 4줄 유지 + 3줄 추가)
---
name: insight_explorer
description: Deep observation and pattern recognition specialist...
subagent_type: insight_explorer
model: sonnet
maxTurns: 15
memory: true
permissionMode: default
---
```

**에이전트별 `maxTurns` 기준**:

| 에이전트 | Model | `maxTurns` | `isolation` | 이유 |
|---------|-------|------------|-------------|------|
| insight_explorer | S | 15 | — | 인지 에이전트, 중간 복잡도 |
| multidimensional_analyst | O | 20 | — | 다차원 분석, 고복잡도 |
| connection_creator | O | 15 | — | 연결/은유, 중간 복잡도 |
| problem_reframer | O | 15 | — | 관점 전환, 중간 복잡도 |
| solution_innovator | O | 20 | — | 혁신 솔루션, 고복잡도 |
| insight_amplifier | O | 20 | — | 심화 분석, 고복잡도 |
| learning_evolver | O | 15 | — | 메타인지, 중간 복잡도 |
| complexity_resolver | O | 15 | — | 긴급 분해, 중간 복잡도 |
| balanced_judge | O | 15 | — | 판단, 중간 복잡도 |
| integrated_sage | O | 20 | — | 통합 지혜, 고복잡도 |
| requirements_analyst | O | 20 | — | 요구사항, 고복잡도 |
| system_architect | O | 25 | — | 아키텍처 설계, 최고복잡도 |
| **code_developer** | S | **30** | **worktree** | 코드 수정 에이전트 — isolation 필수 |
| **quality_reviewer** | S | **20** | **worktree** | 코드 리뷰 에이전트 — isolation 필수 |

> [!note] isolation: worktree 대상
> **코드를 직접 수정하는 에이전트만** worktree 격리 적용. `code_developer`, `quality_reviewer` 2개만 해당.

**실행 순서**: `insight_explorer` 1개 먼저 변경 → 테스트 → 정상이면 나머지 13개 일괄 적용.

---

#### Step 2 — InstructionsLoaded Hook 구현 + 등록 (C4)

**근거**: [[02_004_C4_Hook_Skill_Official_Migration#3.2.4 InstructionsLoaded Hook|C4 InstructionsLoaded 설계]]

**목적**: CLAUDE.md 또는 rules 파일이 로딩될 때마다 감사(audit) 로그 기록. 규칙 파일 로딩 순서 및 충돌 디버깅 지원.

**공식 스펙**:
- 발생 시점: CLAUDE.md 또는 rules 파일 로딩 시
- 제어 가능 여부: No (감사 전용, 차단 불가)
- stdin: `{"file_path": "...", "memory_type": "User|Project|Local|Managed", "load_reason": "session_start|nested_traversal|path_glob_match|include"}`

**구현 파일**: `~/.claude/hooks/instructions-loaded.sh`

```bash
#!/bin/bash
# InstructionsLoaded Hook: 규칙 파일 로딩 감사 로그
# V1.0 (2026-03-15)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')
MEMORY_TYPE=$(echo "$INPUT" | jq -r '.memory_type // empty')
LOAD_REASON=$(echo "$INPUT" | jq -r '.load_reason // empty')

# 로깅
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
echo "[$(date +%Y-%m-%d\ %H:%M)] InstructionsLoaded | file=$FILE_PATH | type=$MEMORY_TYPE | reason=$LOAD_REASON" \
    >> "$LOG_DIR/$(date +%Y%m%d).log"

exit 0
```

**settings.json 등록 (기존 Hook 유지 필수 — C-2 규칙)**:
```json
"InstructionsLoaded": [{
  "hooks": [{
    "type": "command",
    "command": "/Users/changjaeyou/.claude/hooks/instructions-loaded.sh"
  }]
}]
```

**검증 시나리오 (T-5)**: CLAUDE.md가 있는 프로젝트 진입 후 `~/.claude/logs/YYMMDD.log`에 로딩 이벤트 기록 확인.

---

#### Step 3 — TeammateIdle Hook 구현 + 등록 (C4)

**근거**: [[02_004_C4_Hook_Skill_Official_Migration#3.2.5 TeammateIdle Hook|C4 TeammateIdle 설계]] + [[02_002_C2_Parallel_System_Official_Migration#5. Resilience 공식 전환|C2 Resilience]]

**목적**: V4.2.1의 자연어 Resilience 규칙(CLAUDE.md의 "120초 재활성화, 300초 종료")을 공식 Hook으로 코드화하여 강제력 부여.

**공식 스펙**:
- 발생 시점: 팀원 유휴 직전
- 제어 가능 여부: Yes (exit code 2 = 정지 방지)
- stdin: `{"teammateId": "...", "idleDuration": 120, "lastActivity": "..."}`

**구현 파일**: `~/.claude/hooks/teammate-idle.sh`

```bash
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
```

**settings.json 등록 (기존 Hook 유지 필수 — C-2 규칙)**:
```json
"TeammateIdle": [{
  "hooks": [{
    "type": "command",
    "command": "/Users/changjaeyou/.claude/hooks/teammate-idle.sh"
  }]
}]
```

**검증 시나리오 (T-6)**: Agent Teams에서 Teammate 120초 유휴 시 exit code 2 → 정지 방지 확인.

---

#### Step 4 — commands/ → skills/ 마이그레이션 그룹 A + B (C4)

**근거**: [[02_004_C4_Hook_Skill_Official_Migration#5. commands/ → skills/ 마이그레이션 설계|C4 마이그레이션 설계]]

**목적**: `commands/` 13개를 공식 `skills/` 구조로 전환. Phase 1에서는 그룹 A(Git 3개), 그룹 B(유틸 3개) 먼저 진행. 그룹 C(Rails 7개)는 분량이 많으므로 별도 세션에서 처리.

**충돌 규칙 C-5 (필독)**:
> 양쪽 공존 기간 운영. skills/에 새 스킬 생성 후 commands/ 유지 → 검증 후 commands/ 파일 삭제. 한 번에 전체 삭제 금지.

**그룹 A: Git 3개**

| 커맨드 | 스킬 디렉토리 | 핵심 frontmatter 필드 |
|--------|-------------|---------------------|
| `/commit-push` | `skills/commit-push/SKILL.md` | `allowed-tools: [Bash]` |
| `/pr-review` | `skills/pr-review/SKILL.md` | `allowed-tools: [Bash, Read, Grep]` |
| `/project-review` | `skills/project-review/SKILL.md` | `allowed-tools: [Read, Write, Glob, Grep]` |

**그룹 B: 유틸 3개**

| 커맨드 | 스킬 디렉토리 | 핵심 frontmatter 필드 |
|--------|-------------|---------------------|
| `/readme-gen` | `skills/readme-gen/SKILL.md` | `allowed-tools: [Read, Write, Glob]` |
| `/analyze` | `skills/analyze/SKILL.md` | `allowed-tools: [Bash]` |
| `/memory-save` | `skills/memory-save/SKILL.md` | `allowed-tools: [Read, Write, Glob]` |

**SKILL.md 공통 frontmatter 형식**:
```yaml
---
name: [커맨드명]
description: [기능 설명 — Claude가 자동 선택 기준]
user-invocable: true
allowed-tools: [도구 목록]
---
```

**실행 순서**: `/commit-push` 프로토타입 먼저 생성 → 기존 commands/ 버전과 동작 비교 → 일치 확인 후 나머지 5개 진행.

**검증 시나리오 (T-8)**: `/commit-push` 스킬 호출 시 기존 command와 동일 동작 확인.

---

#### Step 5 — 체인 A~J → skills/chains/ 스킬화 프로토타입 (C2)

**근거**: [[02_002_C2_Parallel_System_Official_Migration#4. 체인 → 스킬 전환 설계|C2 체인 스킬화 설계]]

**목적**: CLAUDE.md Section 2.4의 자연어 체인 정의를 공식 `skills/chains/` 스킬로 전환. Phase 1에서는 SystemDesignChain(A)을 프로토타입으로 먼저 구현.

**스킬화 원리**:

| 체인 기호 | 공식 구조 매핑 |
|----------|-------------|
| `→` (순차) | Subagent 순차 호출 |
| `∥` (병렬) | Agent Teams 병렬 실행 |

**`skills/chains/` 디렉토리 구조 (목표)**:

```
~/.claude/skills/chains/
├── system-design.md    ← Chain A (Phase 1 프로토타입)
├── automation.md       ← Chain B
├── game-dev.md         ← Chain C
├── dev.md              ← Chain D
├── research.md         ← Chain E
├── doc.md              ← Chain F
├── web-dev.md          ← Chain G
├── meta-think.md       ← Chain H
├── rails-dev.md        ← Chain I
└── hotfix.md           ← Chain J
```

**SystemDesignChain(A) 스킬 구조 예시**:

```yaml
---
name: system-design-chain
description: 시스템 설계, 아키텍처, CLAUDE.md 업데이트, 체인 개선에 사용. "시스템 설계", "아키텍처", "체인 개선" 키워드에 반응.
user-invocable: false
---

# SystemDesignChain (A)

## 체인 패턴
(Explore ∥ Read) → (system_architect ∥ problem_reframer)
→ solution_innovator → integrated_sage → (Edit ∥ quality_reviewer)

## 단계 목록 (임의 축약 금지)
1. [병렬] 코드베이스 탐색 (Explore) + 관련 파일 읽기 (Read)
2. [병렬] 시스템 아키텍처 설계 (system_architect) + 관점 전환 (problem_reframer)
3. [순차] 혁신 솔루션 도출 (solution_innovator)
4. [순차] 통합 지혜 정리 (integrated_sage)
5. [병렬] 파일 수정 (Edit) + 코드 리뷰 (quality_reviewer)

## 주의사항
- 임의 축약 금지: 정의된 5단계를 모두 실행한다
- "충분하다"는 자의적 판단으로 후반부 에이전트 생략 금지
```

**진행 방식**: SystemDesignChain 1개 먼저 구현 → 기존 자연어 체인과 동작 비교 → 정상이면 나머지 B~J 순차 진행.

---

### 1.4 충돌 예방 규칙 (Phase 1 해당 항목)

**03_001 Section 7에서 추출한 Phase 1 관련 충돌 규칙**:

#### C-4. 에이전트 frontmatter 변경 (Step 1 해당)

**위험도**: High

| 항목 | 내용 |
|------|------|
| 문제 | `memory: true` 등 신규 필드 추가 시 기존 에이전트 동작이 변할 수 있음 |
| 해결책 | 기존 필드(name, description, subagent_type, model) 절대 삭제/수정 금지, 신규 필드만 추가 |
| 테스트 | 1개만 먼저 변경 → 테스트 → 나머지 일괄 |
| 롤백 | `104_current_system/agents/` 원본으로 복원 |

#### C-5. commands/ → skills/ 이전 (Step 4 해당)

**위험도**: High

| 항목 | 내용 |
|------|------|
| 문제 | commands/ 삭제 시 기존 슬래시 커맨드(`/commit-push` 등) 사라짐 |
| 해결책 | 양쪽 공존 기간 운영 — skills/에 스킬 생성 후 commands/ 유지 |
| 우선순위 | 동일 이름이면 skill 우선 (공식 동작) |
| 삭제 기준 | 스킬 동작 확인 후 commands/ 파일 1~2개씩 삭제 (한 번에 전체 삭제 금지) |

#### C-2. settings.json Hook 등록 (Step 2, 3 해당)

**위험도**: Critical

| 항목 | 내용 |
|------|------|
| 문제 | 새 Hook 등록 시 기존 Hook(auto-analyze.sh) 덮어쓰기 위험 |
| 해결책 | 병합(merge) 방식으로 신규 Hook 추가 — 기존 Hook 배열 유지 |
| 검증 | 수정 후 Claude 재시작 → 프롬프트 입력 → 4-Layer 분석 출력 확인 |

**안전 원칙 5가지** (변경 전 필독):

| # | 원칙 |
|---|------|
| 1 | 104 백업 절대 건드리지 않음 |
| 2 | 한 번에 하나만 변경 |
| 3 | 변경 → 테스트 → 다음 변경 |
| 4 | 삭제 전 복사 완료 확인 |
| 5 | 롤백 방법 미리 확인 |

---

### 1.5 Hook 완성 후 상태 (Phase 1 완료 시)

| Hook 이벤트 | Phase 0 이후 | Phase 1 이후 | 타입 |
|------------|------------|------------|------|
| SessionStart | ✅ session-start.sh | ✅ 유지 | command |
| UserPromptSubmit | ✅ auto-analyze.sh | ✅ 유지 | command |
| PreToolUse | ✅ 보안 필터 | ✅ 유지 | command |
| PostToolUse | ✅ 포매팅+Git+로그 | ✅ 유지 | command |
| Stop | ✅ stop-cleanup.sh | ✅ 유지 | command |
| PostCompact | ✅ post-compact.sh | ✅ 유지 | command |
| **InstructionsLoaded** | ❌ | ✅ **Step 2 구현** | command |
| **TeammateIdle** | ❌ | ✅ **Step 3 구현** | command |

**결과**: Phase 0의 6/12 → Phase 1 완료 후 **8/12** (Hook 활성화율 25% → 67%)

---

## 2. 실행 로그 (Log)

### Step 1 — 에이전트 14개 frontmatter 업그레이드

| 항목 | 내용 |
|------|------|
| 카테고리 | C2 |
| 대상 파일 | `~/.claude/agents/101_*.md` ~ `114_*.md` (14개) |
| 작업 유형 | 기존 파일 수정 (필드 추가만) |

#### 📋 아리 가이드

> 04_002 Section 1.3 Step 1 참조. 14개 에이전트에 maxTurns + isolation(2개) 추가. 1개(insight_explorer) 먼저 변경 → 테스트 → 나머지 일괄.

#### 앤 실행 결과

- ✅ 14개 에이전트 전체에 `maxTurns` 필드 추가 (15~30 범위)
- ✅ `code_developer`(113), `quality_reviewer`(114)에 `isolation: worktree` 추가
- ✅ 기존 필드(name, description, subagent_type/model) 보존 확인 (C-4 규칙 준수)
- ✅ `color` 필드도 일부 에이전트에 추가 (시각적 구분)
- 📊 maxTurns 분포: S모델 15~20, O모델 15~25, code_developer 30(최대)

#### 오류 & 해결

> 오류 없음. insight_explorer 프로토타입 변경 후 나머지 13개 일괄 적용.

---

### Step 2 — InstructionsLoaded Hook 구현 + 등록

| 항목 | 내용 |
|------|------|
| 카테고리 | C4 |
| 신규 파일 | `~/.claude/hooks/instructions-loaded.sh` |
| 수정 파일 | `~/.claude/settings.json` (Hook 등록) |

#### 📋 아리 가이드

> 04_002 Section 1.3 Step 2 참조. instructions-loaded.sh 생성 + settings.json 병합 등록.

#### 앤 실행 결과

- ✅ `~/.claude/hooks/instructions-loaded.sh` 생성 (507 bytes) + `chmod +x`
- ✅ settings.json에 InstructionsLoaded Hook 병합 등록 (기존 Hook 보존 — C-2 규칙)
- ✅ 규칙 파일 로딩 시 `~/.claude/logs/YYMMDD.log`에 감사 로그 기록 확인
- ✅ 로그 형식: `[날짜] InstructionsLoaded | file=경로 | type=타입 | reason=사유`

#### 오류 & 해결

> 오류 없음.

---

### Step 3 — TeammateIdle Hook 구현 + 등록

| 항목 | 내용 |
|------|------|
| 카테고리 | C4 |
| 신규 파일 | `~/.claude/hooks/teammate-idle.sh` |
| 수정 파일 | `~/.claude/settings.json` (Hook 등록) |

#### 📋 아리 가이드

> 04_002 Section 1.3 Step 3 참조. teammate-idle.sh 생성 + settings.json 병합 등록. 120s→exit 2(재활성화), 300s→exit 0(종료 허용).

#### 앤 실행 결과

- ✅ `~/.claude/hooks/teammate-idle.sh` 생성 (1,377 bytes) + `chmod +x`
- ✅ settings.json에 TeammateIdle Hook 병합 등록 (기존 Hook 보존 — C-2 규칙)
- ✅ 120초 유휴 → exit code 2 (정지 방지, 재활성화 지시)
- ✅ 300초 정체 → exit code 0 (종료 허용, Lead에게 대체 지시)
- ✅ 로그: `[날짜] TeammateIdle | id=팀원ID | idle=초 | last=활동`

#### 오류 & 해결

> 오류 없음.

---

### Step 4 — commands/ → skills/ 마이그레이션 (그룹 A + B)

| 항목 | 내용 |
|------|------|
| 카테고리 | C4 |
| 신규 파일 | `~/.claude/skills/commit-push/SKILL.md` 등 6개 |
| commands/ | 유지 (삭제 금지 — C-5 규칙) |

#### 📋 아리 가이드

> 04_002 Section 1.3 Step 4 참조. 그룹 A(Git 3개) + 그룹 B(유틸 3개) → skills/ 마이그레이션. commands/ 보존 (C-5 공존 규칙).

#### 앤 실행 결과

- ✅ 6개 skills/ 디렉토리 생성:
  - `skills/commit-push/SKILL.md` (Git — allowed-tools: Bash)
  - `skills/pr-review/SKILL.md` (Git — allowed-tools: Bash, Read, Grep)
  - `skills/project-review/SKILL.md` (Git — allowed-tools: Read, Write, Glob, Grep)
  - `skills/readme-gen/SKILL.md` (유틸 — allowed-tools: Read, Write, Glob)
  - `skills/analyze/SKILL.md` (유틸 — allowed-tools: Bash)
  - `skills/memory-save/SKILL.md` (유틸 — allowed-tools: Read, Write, Glob)
- ✅ commands/ 13개 원본 보존 (C-5 공존 기간 유지)
- ✅ skills/ 스킬 호출 시 commands/ 동일 기능 동작 확인

#### 오류 & 해결

> 오류 없음. 공존 기간 동안 동일 이름 시 skill 우선 동작 확인.

---

### Step 5 — 체인 A~J → skills/chains/ 스킬화 프로토타입

| 항목 | 내용 |
|------|------|
| 카테고리 | C2 |
| 신규 파일 | `~/.claude/skills/chains/system-design.md` (프로토타입 1개 이상) |
| 수정 파일 | CLAUDE.md Section 2.4 (스킬 참조로 교체 — Phase 완료 시) |

#### 📋 아리 가이드

> 04_002 Section 1.3 Step 5 참조. SystemDesignChain(A) 프로토타입을 skills/chains/system-design.md로 생성. 나머지 B~J는 향후 진행.

#### 앤 실행 결과

- ✅ `skills/chains/system-design.md` 생성 — SystemDesignChain(A) 프로토타입
  - frontmatter: name, description, user-invocable: false
  - 5단계 체인 패턴 (Explore∥Read → architect∥reframer → innovator → sage → Edit∥reviewer)
  - 트리거 조건, 임의 축약 금지 주의사항, Pre-execution Declaration 포함
- ✅ Effort: HIGH 태그 반영
- 📝 나머지 B~J 스킬화는 Phase 3 A1에서 DevChain(D) 추가 완료 (2026-03-17)
- 📝 Phase 3에서 system-design.md를 5→7단계로 수정 (research/plan 삽입)

#### 오류 & 해결

> 오류 없음. 프로토타입 1개로 패턴 검증 후 Phase 3에서 확장.

---

## 3. 최종 결과 요약

| 단계 | 작업 | 상태 |
|------|------|------|
| Step 1 | 에이전트 14개 frontmatter 업그레이드 | ✅ | maxTurns 14개, isolation 2개 (code_developer, quality_reviewer) |
| Step 2 | InstructionsLoaded Hook 구현 + 등록 | ✅ | instructions-loaded.sh, 감사 로그 정상 |
| Step 3 | TeammateIdle Hook 구현 + 등록 | ✅ | teammate-idle.sh, 120s→exit 2, 300s→exit 0 |
| Step 4 | commands/ → skills/ 마이그레이션 (A+B 6개) | ✅ | 6개 skills/ 생성, commands/ 보존 (C-5) |
| Step 5 | 체인 → skills/chains/ 스킬화 프로토타입 | ✅ | SystemDesignChain(A) 프로토타입 |

**진행률**: 5 / 5 (100%) ✅

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[02_002_C2_Parallel_System_Official_Migration#3. 에이전트 마이그레이션 설계|C2 에이전트 마이그레이션]] — Step 1의 기술 근거 (에이전트 frontmatter 14개 필드)
- [[02_004_C4_Hook_Skill_Official_Migration#3.2.4 InstructionsLoaded Hook|C4 InstructionsLoaded]] — Step 2의 구현 설계 (감사 로그 스크립트)
- [[02_004_C4_Hook_Skill_Official_Migration#3.2.5 TeammateIdle Hook|C4 TeammateIdle]] — Step 3의 구현 설계 (120s/300s 임계값)
- [[03_001_Prerequisites_Checklist#7.2 충돌별 상세 해결책|충돌 해결책 C-4, C-5]] — Step 1, 4의 충돌 방지 상세 절차

### 역참조 (Backlinks)
- [[04_001_Phase0_Implementation]] — Phase 0 완료 후 이 문서의 Phase 1이 시작됨
- [[04_003_Phase2_Implementation]] — Phase 1 완료 후 Phase 2(메모리 혁신)로 이어짐
- [[01_001_Improvement_Direction_Overview#5. 실행 순서 권고|Phase 1 실행 순서]] — 상위 로드맵 문서

### 관련 주제 (Topic Links)
- [[01_001_Improvement_Direction_Overview#C2. 병렬 시스템|C2 개선 방향]] — Phase 1 C2 범위의 전략적 배경
- [[01_001_Improvement_Direction_Overview#C4. Hook & Skill 공식 체계 전환|C4 개선 방향]] — Phase 1 C4 범위의 전략적 배경

---

## Release Notes

### v1.1.0 (2026-03-17)
- 5개 Step 실행 로그(Section 2) 백필 — 메모리(2603_018, 2603_020) + 실제 파일 검증 기반
- Step 1: 에이전트 14개 maxTurns + isolation 확인 기록
- Step 2: instructions-loaded.sh 507bytes, 감사 로그 정상
- Step 3: teammate-idle.sh 1377bytes, 120s/300s 임계값 정상
- Step 4: skills/ 6개 생성, commands/ 보존 확인
- Step 5: system-design.md 프로토타입, Phase 3에서 5→7단계 확장 기록
> **프롬프트:** "04_001, 04_002 작업을 체크해서 미비된것이 있는지 체크해줘"

### v1.0.0 (2026-03-15)
- 초기 작성: Phase 1 실행 계획 수립
- 5단계 실행 순서 정의 (에이전트 업그레이드, Hook 2개, 마이그레이션, 체인 스킬화)
- C2 에이전트 14개 frontmatter 업그레이드 상세 (maxTurns 기준, isolation 대상)
- C4 InstructionsLoaded, TeammateIdle Hook 구현 코드 포함
- C4 commands/ → skills/ 마이그레이션 그룹 A+B 계획 (6개)
- C2 체인 A~J → skills/chains/ 스킬화 프로토타입 설계
- 충돌 예방 규칙 C-4, C-5, C-2 요약 포함
- Phase 1 완료 시 Hook 활성화율 25% → 67% (8/12) 달성
- 로그 섹션은 Phase 1 시작 시 기록 예정 (플레이스홀더)
> **프롬프트:** "You are creating a Phase 1 Implementation document."
