---
title: "C2. 병렬 시스템 — 공식 기능 전환 심층 설계"
version: "1.0.0"
created: "2026-03-15"
updated: "2026-03-15"
tags: [claude-code, agent-teams, subagents, migration, parallel, c2]
status: completed
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: C2 병렬 시스템 공식 전환 심층 설계 — 에이전트 마이그레이션, 체인→스킬 전환, Hook 대체

### 다음 작업 (TODO)
- [ ] Phase 1 실행: 14개 에이전트 frontmatter 업그레이드 (`memory`, `isolation` 필드)
- [ ] Phase 2 실행: 체인 A~J → `.claude/skills/chains/` 스킬화 프로토타입 (A부터)
- [ ] Phase 2 실행: CLAUDE.md Section 2.4 체인 정의를 스킬 참조로 교체
- [ ] Phase 3 실행: TeammateIdle, TaskCompleted Hook 구현
- [ ] 전체 검증: 기존 체인과 신규 스킬의 동작 비교 테스트

### 작업 조언
> [!tip] 다음 Claude Code에게
> - **대전제**: 공식 기능 우선. 커스텀 체인/Resilience를 공식 구조로 대체하는 것이 목표
> - 104 폴더의 `agents/`, `CLAUDE.md`가 V4.2.1 원본 — 마이그레이션 비교 기준
> - 에이전트는 이미 `~/.claude/agents/`에 위치 (공식 위치와 동일) — frontmatter만 업그레이드
> - 체인→스킬 전환 시 **순차(→)는 Subagent**, **병렬(∥)은 Agent Teams**로 매핑
> - [[02_001_Claude_Code_Official_Docs_Core_Engine#3. 병렬 시스템 심층 분석|공식 병렬 문서]]가 기술 레퍼런스
> - 임의 축약 금지 원칙은 스킬 내부에서도 유지 — 스킬 정의에 단계 목록을 명시

---

# C2. 병렬 시스템 — 공식 기능 전환 심층 설계

> **상위 문서**: [[01_001_Improvement_Direction_Overview#C2. 병렬 시스템|C2 개선 방향]]
> **대전제**: [[01_001_Improvement_Direction_Overview#1.5 개선 대전제|공식 우선 → 공식 강화 → 자체 개발]]
> **V4.2.1 원본**: [[104_current_system/CLAUDE.md]] (비교 기준)

---

## 1. 설계 목표

### 1.1 한 문장 목표

> **커스텀 체인/에이전트/Resilience를 공식 Subagent + Agent Teams + Hook으로 전면 전환하여, 공식 업데이트 시 자동으로 혜택을 받는 구조로 만든다.**

### 1.2 구체적 목표

| 항목 | 현재 (V4.2.1) | 목표 (V5.0) | 대전제 |
|------|-------------|------------|--------|
| **에이전트 위치** | `~/.claude/agents/` (이미 공식) | frontmatter 필드 확장 | 1순위 (공식 사용) |
| **체인 정의** | CLAUDE.md 자연어 인코딩 | `.claude/skills/chains/` 스킬 | 2순위 (공식 강화) |
| **병렬 실행** | 환경변수 기반 Agent Teams | 공식 Agent Teams API | 1순위 (공식 사용) |
| **Resilience** | CLAUDE.md 규칙 (수동) | TeammateIdle/TaskCompleted Hook | 1순위 (공식 사용) |
| **임의 축약 금지** | CLAUDE.md 원칙 | 스킬 내부에 단계 목록 인코딩 | 2순위 (공식 강화) |

### 1.3 **하지 않는 것**

| 하지 않는 것 | 이유 |
|-------------|------|
| 체인 개수 변경 (10개 유지) | 체인 간소화는 C5(Observability)의 데이터 기반으로 판단 |
| 에이전트 모델 재배정 | Opus/Sonnet 역할 분리는 검증됨, 변경 불필요 |
| 새 에이전트 추가 | 현재 14개로 충분, 복잡도 증가 방지 |

---

## 2. 현재 구조 vs 목표 구조

### 2.1 현재 (V4.2.1)

```
~/.claude/CLAUDE.md (393줄)
├── Section 2.3: 통합 매핑 테이블 (에이전트 14 + 스킬 + 도구)
├── Section 2.4: 체인 정의 A~J (자연어 패턴)
├── Section 2.5: Agent Teams 통합 (환경변수, Resilience 규칙)
└── 에이전트 행동 규칙 (메모리 금지, 착수 보고 등)

~/.claude/agents/ (14개 .md 파일)
├── 101~110: 인지 에이전트
├── 111~114: 역할 에이전트
└── archive/: 비활성 8개
```

**문제점**:
- 체인 정의가 CLAUDE.md 안에 자연어로 인코딩 → LLM 해석 의존
- Resilience 규칙이 자연어 → 강제력 없음 (Claude가 무시 가능)
- 에이전트 frontmatter에 `memory`, `isolation`, `hooks` 필드 미사용

### 2.2 목표 (V5.0)

```
~/.claude/CLAUDE.md (~100줄, C3에서 경량화)
├── 핵심 원칙만 (Identity, CLEAR, 대전제)
└── @~/.claude/rules/orchestration.md 참조

~/.claude/agents/ (14개 .md — frontmatter 확장)
├── memory: true                    ← 공식 서브에이전트 메모리
├── isolation: worktree             ← 코드 변경 에이전트만
├── hooks: [TeammateIdle 참조]      ← 공식 Hook 연동
└── maxTurns: 적정값                ← 무한 루프 방지

~/.claude/skills/chains/ (10개 스킬 — 체인 패턴 스킬화)
├── system-design.md    (A)
├── automation.md       (B)
├── game-dev.md         (C)
├── dev.md              (D)
├── research.md         (E)
├── doc.md              (F)
├── web-dev.md          (G)
├── meta-think.md       (H)
├── rails-dev.md        (I)  ← 향후 제거 대상 (앤 지시 시)
└── hotfix.md           (J)

~/.claude/hooks/
├── auto-analyze.sh     (기존 유지)
├── teammate-idle.sh    (신규 — TeammateIdle Hook)
└── task-completed.sh   (신규 — TaskCompleted Hook)
```

---

## 3. 에이전트 마이그레이션 설계 (Phase 1)

### 3.1 현재 에이전트 frontmatter 분석

현재 `~/.claude/agents/101_Insight_Explorer.md` 예시:

```yaml
---
name: insight_explorer
description: Deep observation and pattern recognition specialist...
subagent_type: insight_explorer
model: sonnet
---
```

### 3.2 목표 frontmatter (공식 14개 필드 적용)

```yaml
---
name: insight_explorer
description: Deep observation and pattern recognition specialist. 5+ "Why?" iterations, cross-domain discovery, bias mitigation.
subagent_type: insight_explorer
model: sonnet
maxTurns: 15
memory: true
permissionMode: default
# isolation: worktree  ← 코드 변경하는 에이전트만
# hooks: []            ← 향후 필요 시 추가
# skills: []           ← 특정 스킬 제한 시
# mcpServers: []       ← 특정 MCP만 허용 시
# disallowedTools: []  ← 도구 제한 시
---
```

### 3.3 에이전트별 마이그레이션 매트릭스

| 에이전트 | Model | `memory` | `isolation` | `maxTurns` | 변경 사항 |
|---------|-------|----------|-------------|------------|----------|
| insight_explorer | S | `true` | — | 15 | memory, maxTurns 추가 |
| multidimensional_analyst | **O** | `true` | — | 20 | memory, maxTurns 추가 |
| connection_creator | **O** | `true` | — | 15 | memory, maxTurns 추가 |
| problem_reframer | **O** | `true` | — | 15 | memory, maxTurns 추가 |
| solution_innovator | **O** | `true` | — | 20 | memory, maxTurns 추가 |
| insight_amplifier | **O** | `true` | — | 20 | memory, maxTurns 추가 |
| learning_evolver | **O** | `true` | — | 15 | memory, maxTurns 추가 |
| complexity_resolver | **O** | `true` | — | 15 | memory, maxTurns 추가 |
| balanced_judge | **O** | `true` | — | 15 | memory, maxTurns 추가 |
| integrated_sage | **O** | `true` | — | 20 | memory, maxTurns 추가 |
| requirements_analyst | **O** | `true` | — | 20 | memory, maxTurns 추가 |
| system_architect | **O** | `true` | — | 25 | memory, maxTurns 추가 |
| **code_developer** | S | `true` | **`worktree`** | 30 | memory, isolation, maxTurns |
| **quality_reviewer** | S | `true` | **`worktree`** | 20 | memory, isolation, maxTurns |

> [!note] `isolation: worktree` 대상
> **코드를 직접 수정하는 에이전트만** worktree 격리 — `code_developer`, `quality_reviewer`
> 인지 에이전트(분석/판단)는 코드 수정하지 않으므로 격리 불필요

### 3.4 메모리 격리 규칙 변경

| 항목 | V4.2.1 (현재) | V5.0 (목표) |
|------|-------------|------------|
| 규칙 위치 | CLAUDE.md 자연어 | 에이전트 frontmatter `memory: true/false` |
| Lead-only 저장 | 자연어 규칙 "절대 금지" | 공식 `memory` 필드가 제어 |
| Teammate 격리 | 환경변수 감지 (auto-analyze.sh) | 공식 Agent Teams 자체 관리 |

**대전제 적용**: 공식 `memory: true`가 서브에이전트 자체 메모리를 관리 → 커스텀 "Lead-only" 규칙의 필요성 재평가

---

## 4. 체인 → 스킬 전환 설계 (Phase 2)

### 4.1 스킬화 원리

**현재**: CLAUDE.md에 자연어로 체인 패턴 정의

```
#### A. SystemDesignChain
(Explore[S] ∥ Read[-]) → (system_architect[O] ∥ problem_reframer[O])
→ solution_innovator[O] → integrated_sage[O] → (Edit[-] ∥ quality_reviewer[S])
```

**목표**: `.claude/skills/chains/system-design.md`로 스킬화

```markdown
---
name: system-design-chain
description: 시스템/아키텍처 설계 체인. CLAUDE.md 개선, 체인 설계, 아키텍처 수립.
user-invocable: true
allowed-tools: [Agent, Read, Edit, Write, Glob, Grep, Bash, WebSearch]
---

# SystemDesignChain (A)

## 트리거
"시스템 설계", "아키텍처", "체인 개선", 메타 작업 자동 감지

## 실행 단계 (임의 축약 금지)

### Step 1: 탐색 (병렬)
- Explore[S]: 코드베이스 탐색
- Read[-]: 관련 파일 직접 읽기
→ 두 결과를 통합하여 다음 단계에 전달

### Step 2: 설계 (병렬)
- system_architect[O]: 아키텍처 설계안 작성
- problem_reframer[O]: 문제 재정의 및 관점 전환
→ 두 관점을 종합

### Step 3: 혁신
- solution_innovator[O]: 혁신적 해결책 도출
→ Step 2 결과를 기반으로 창의적 대안 제시

### Step 4: 통합
- integrated_sage[O]: 모든 결과를 통합 종합
→ 최종 설계안 확정

### Step 5: 적용 (병렬)
- Edit[-]: 파일 수정 적용
- quality_reviewer[S]: 코드/문서 품질 검토
→ 적용 + 검증 동시 수행
```

### 4.2 체인 A~J 스킬화 매핑

| 체인 | 스킬 파일명 | 순차(→) 단계 | 병렬(∥) 단계 | 실행 방식 |
|------|-----------|-------------|-------------|----------|
| **A** SystemDesign | `system-design.md` | 5 | Step 1,2,5 | Subagent 순차 + Agent Teams 병렬 |
| **B** Automation | `automation.md` | 4 | Step 2 | Subagent 순차 + 병렬 검색 |
| **C** GameDev | `game-dev.md` | 3 | Step 2 (듀얼) | Agent Teams (Roblox ∥ Web) |
| **D** Dev | `dev.md` | 4 | Step 2 | Subagent 순차 + 병렬 탐색 |
| **E** Research | `research.md` | 5 | Step 1,2 | Subagent 순차 + 병렬 검색/분석 |
| **F** Doc | `doc.md` | 3 | — | Subagent 순차 |
| **G** WebDev | `web-dev.md` | 5 | Step 2 | Subagent 순차 + 병렬 탐색 |
| **H** MetaThink | `meta-think.md` | 6 | Step 1,2 | Subagent 순차 + 병렬 사고 |
| **I** RailsDev | `rails-dev.md` | 6 | Step 3 반복 | Subagent 순차 + 반복 |
| **J** Hotfix | `hotfix.md` | 3 | Step 1,3 | Subagent 순차 + 병렬 탐색/검증 |

### 4.3 순차 vs 병렬 실행 매핑

```
CLAUDE.md 표기  →  공식 구현
─────────────────────────────
→ (순차)        →  Agent 도구로 subagent 순차 호출
∥ (병렬)        →  Agent 도구로 동시에 여러 subagent 호출
                   (Claude Code가 병렬 도구 호출 자체 지원)
```

> [!important] Agent Teams vs 병렬 Subagent
> **병렬 Subagent**: 같은 세션 내 여러 Agent 도구 동시 호출 → 결과만 반환
> **Agent Teams**: 독립 프로세스, 공유 작업 목록, 팀원 간 직접 메시지 가능
>
> **판단 기준**: 결과만 필요하면 병렬 Subagent (가벼움), 협업 필요하면 Agent Teams (무거움)

### 4.4 CLAUDE.md 체인 정의 대체

**현재 (Section 2.4, ~70줄)** → 삭제하고 스킬 참조로 대체:

```markdown
### 2.4 Dynamic Chain Patterns → Skills

체인 패턴은 `.claude/skills/chains/`에 스킬로 정의되어 있다.
각 스킬은 사용자가 `/체인명`으로 직접 호출하거나, 아리가 자동 선택한다.

| 체인 | 스킬 | 트리거 |
|------|------|--------|
| A. SystemDesign | `/system-design` | 시스템 설계, 아키텍처 |
| B. Automation | `/automation` | Hook, MCP, 스크립트 |
| ... | ... | ... |

> ⚠️ 임의 축약 금지: 스킬 내부에 정의된 모든 단계를 순서대로 실행한다.
```

**효과**: CLAUDE.md에서 ~70줄 절감 → C3(모듈화)에 기여

---

## 5. Resilience → 공식 Hook 대체 (Phase 3)

### 5.1 현재 Resilience 규칙 (V4.2.1)

| 규칙 | 현재 구현 | 강제력 |
|------|----------|--------|
| Teammate 무응답 (120초) | CLAUDE.md 자연어 | ❌ 없음 (Claude가 지킬 수도, 안 지킬 수도) |
| Teammate 정체 (300초) | CLAUDE.md 자연어 | ❌ 없음 |
| 착수 보고 (30초) | CLAUDE.md 자연어 | ❌ 없음 |
| 메모리 저장 금지 | CLAUDE.md 자연어 | ❌ 없음 |
| Hook 중복 방지 | auto-analyze.sh 환경변수 감지 | ✅ 코드 강제 |

### 5.2 공식 Hook 대체 설계

| V4.2.1 규칙 | V5.0 공식 Hook | 강제력 | 구현 |
|------------|---------------|--------|------|
| Teammate 무응답 | **`TeammateIdle`** Hook | ✅ **코드 강제** | exit code 2 → 정지 방지 |
| Teammate 정체 | **`TeammateIdle`** Hook | ✅ **코드 강제** | 유휴 감지 → 재할당/종료 |
| 착수 보고 | **`TaskCompleted`** Hook | ✅ **코드 강제** | 완료 시 Lead에 결과 전달 |
| 메모리 저장 금지 | `memory: false` frontmatter | ✅ **설정 강제** | Teammate 에이전트에 설정 |
| Hook 중복 방지 | 공식 팀 모드 자체 처리 | ✅ **자동** | 공식 API가 관리 |

### 5.3 TeammateIdle Hook 설계

```bash
#!/bin/bash
# ~/.claude/hooks/teammate-idle.sh
# TeammateIdle Hook: Teammate가 유휴 상태일 때 트리거

# 유휴 시간 (초) — Hook이 자동 제공
IDLE_SECONDS="${IDLE_SECONDS:-0}"

if [ "$IDLE_SECONDS" -ge 120 ]; then
    # 120초 이상 무응답 → Lead에게 알림 + 작업 재할당
    echo '{"decision": "reassign", "reason": "120초 무응답 — 자동 재할당"}'
    exit 2  # exit code 2 = 정지 방지 (Teammate 유지하고 재활성화)
elif [ "$IDLE_SECONDS" -ge 300 ]; then
    # 300초 이상 정체 → Teammate 종료
    echo '{"decision": "shutdown", "reason": "300초 정체 — 자동 종료"}'
    exit 0  # 정상 종료 허용
fi

exit 0
```

### 5.4 TaskCompleted Hook 설계

```bash
#!/bin/bash
# ~/.claude/hooks/task-completed.sh
# TaskCompleted Hook: 에이전트 작업 완료 시 트리거

# 완료된 작업 정보 (stdin으로 전달)
TASK_INFO=$(cat)

# 결과를 로그에 기록 (C5 Observability 연계)
echo "[$(date +%Y-%m-%d\ %H:%M)] TaskCompleted: $TASK_INFO" >> ~/.claude/logs/$(date +%Y%m%d).log

# 정상 완료 허용
exit 0
```

---

## 6. 마이그레이션 검증 계획

### 6.1 검증 시나리오

| # | 시나리오 | 체인 | 검증 항목 |
|---|---------|------|----------|
| T-1 | "시스템 설계해줘" | A (SystemDesign) | 스킬 자동 선택, 5단계 완전 실행 |
| T-2 | "이 버그 긴급 수정" | J (Hotfix) | 병렬 탐색 + 순차 수정 |
| T-3 | "이 주제를 조사해줘" | E (Research) | 병렬 검색 + 순차 분석 |
| T-4 | 긴 작업에서 Teammate 무응답 시뮬레이션 | Teams | TeammateIdle Hook 트리거 확인 |
| T-5 | Subagent `memory: true` 확인 | 개별 | 에이전트 자체 메모리 저장 확인 |

### 6.2 롤백 계획

| 문제 | 감지 방법 | 롤백 |
|------|----------|------|
| 스킬 기반 체인이 동작 안 함 | T-1~3 실패 | `104_current_system/CLAUDE.md`에서 체인 정의 복원 |
| TeammateIdle Hook 오작동 | T-4 예상 외 종료 | Hook 비활성화 (`settings.json`에서 제거) |
| `memory: true` 충돌 | 메모리 파일 중복 | frontmatter에서 `memory: false`로 복구 |

---

## 7. 구현 단계 (Phase)

### Phase 1: 에이전트 frontmatter 업그레이드 (1세션)

| 단계 | 작업 | 산출물 |
|------|------|--------|
| 1-1 | 14개 에이전트에 `memory: true`, `maxTurns` 추가 | 업데이트된 .md 파일 14개 |
| 1-2 | code_developer, quality_reviewer에 `isolation: worktree` 추가 | 2개 파일 |
| 1-3 | 검증: T-5 실행 | 에이전트 메모리 동작 확인 |

### Phase 2: 체인 → 스킬 전환 (2~3세션)

| 단계 | 작업 | 산출물 |
|------|------|--------|
| 2-1 | 체인 A (SystemDesign) 스킬 프로토타입 | `skills/chains/system-design.md` |
| 2-2 | 검증: T-1 실행 → 기존 체인과 동작 비교 | 테스트 결과 |
| 2-3 | 나머지 체인 B~J 스킬화 (A 검증 후) | `skills/chains/` 9개 추가 |
| 2-4 | CLAUDE.md Section 2.4 → 스킬 참조로 교체 | CLAUDE.md ~70줄 절감 |
| 2-5 | 검증: T-2, T-3 실행 | 전체 체인 동작 확인 |

### Phase 3: Resilience Hook 구현 (1세션)

| 단계 | 작업 | 산출물 |
|------|------|--------|
| 3-1 | `teammate-idle.sh` Hook 구현 | `hooks/teammate-idle.sh` |
| 3-2 | `task-completed.sh` Hook 구현 | `hooks/task-completed.sh` |
| 3-3 | `settings.json`에 Hook 등록 | TeammateIdle, TaskCompleted 이벤트 |
| 3-4 | CLAUDE.md Section 2.5 Resilience 규칙 → Hook 참조로 교체 | 자연어 규칙 삭제 |
| 3-5 | 검증: T-4 실행 | Teammate 무응답 자동 처리 확인 |

---

## 8. 파일 구조 (최종)

```
~/.claude/
├── agents/                        ← Phase 1: frontmatter 업그레이드
│   ├── 101_Insight_Explorer.md    ← memory: true, maxTurns: 15
│   ├── ...
│   ├── 113_Code_Developer.md      ← memory: true, isolation: worktree, maxTurns: 30
│   └── 114_Quality_Reviewer.md    ← memory: true, isolation: worktree, maxTurns: 20
├── skills/
│   └── chains/                    ← Phase 2: 체인 스킬화 (신규)
│       ├── system-design.md       (A)
│       ├── automation.md          (B)
│       ├── game-dev.md            (C)
│       ├── dev.md                 (D)
│       ├── research.md            (E)
│       ├── doc.md                 (F)
│       ├── web-dev.md             (G)
│       ├── meta-think.md          (H)
│       ├── rails-dev.md           (I)
│       └── hotfix.md              (J)
├── hooks/                         ← Phase 3: Resilience Hook (신규)
│   ├── auto-analyze.sh            (기존 유지)
│   ├── teammate-idle.sh           (신규)
│   └── task-completed.sh          (신규)
└── settings.json                  ← Hook 이벤트 등록 추가
```

---

## 9. 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 |
|--------|------|------|------|
| 스킬 기반 체인이 자연어 정의보다 정확도 낮음 | Medium | High | A 체인 프로토타입 먼저, 비교 테스트 |
| `memory: true`로 메모리 파일 폭발 | Medium | Medium | 에이전트별 메모리는 자동 정리 (공식) |
| TeammateIdle Hook이 정상 작업을 오탐 | Low | High | 120초 임계값 충분히 관대하게 |
| 104 원본과 호환성 단절 | Low | Medium | 104 보존, 단계별 롤백 가능 |
| Agent Teams 공식 API 변경 | Medium | High | 스킬 레이어가 완충재 역할 (추상화) |

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[01_001_Improvement_Direction_Overview#C2. 병렬 시스템|C2 개선 방향]] — 상위 방향 문서
- [[02_001_C1_Ontology_Memory_Deep_Design#3. 아키텍처 설계|C1 아키텍처]] — 메모리 MCP 서버가 서브에이전트에서 활용

### 역참조 (Backlinks)
- [[01_001_Improvement_Direction_Overview#6. 카테고리별 심층 문서 계획|심층 문서 계획]] — 이 문서를 02_002로 계획

### 관련 주제 (Topic Links)
- [[02_004_C4_Hook_Skill_Official_Migration#3. Hook 확장 설계|C4 Hook 확장]] — TeammateIdle/TaskCompleted Hook이 C2 Resilience 대체
- [[02_005_C5_Observability_Self_Evolution#5. Effort Level 체인별 분화|C5 Effort 분화]] — 체인별 effort 설정과 연계
- [[02_007_C7_Agentic_Workflow_Paradigm#3. 아키텍처 설계|C7 워크플로우]] — 체인 패턴과 워크플로우 공존 구조

---

## Release Notes

### v1.0.0 (2026-03-15)
- 초기 작성: C2 병렬 시스템 공식 전환 심층 설계
- 에이전트 14개 frontmatter 업그레이드 매트릭스 (memory, isolation, maxTurns)
- 체인 A~J → `.claude/skills/chains/` 스킬화 설계 + 예시 (SystemDesignChain)
- Resilience → 공식 Hook 대체 (TeammateIdle, TaskCompleted) + 셸 스크립트
- 3단계 Phase + 검증 시나리오 5개 + 롤백 계획
- 리스크 5개 식별 + 완화 전략
> **프롬프트:** "c2 진행해줘"
