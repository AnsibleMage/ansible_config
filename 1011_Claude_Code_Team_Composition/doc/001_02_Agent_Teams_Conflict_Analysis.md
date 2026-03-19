# Claude Code Agent Teams vs Dynamic Chain Orchestration V3.8
## Conflict Analysis & Improvement Report

> 2026-02-06 | Prepared for An (Ansible)
> Ari (Aria) & An (Ansible) Collaboration

---

## 1. Executive Summary

**Opus 4.6**에서 새롭게 도입된 **Agent Teams**는 여러 독립 Claude Code 세션이 팀을 이뤄 병렬로 작업하는 기능입니다. 앤(An)이 기존에 구축한 **Dynamic Chain Orchestration V3.8** 시스템(커스텀 서브에이전트 24개 + 체인 패턴 10개)과 설계 철학이 유사하지만, 작동 메커니즘은 근본적으로 다릅니다. 본 리포트는 두 시스템 간의 충돌 가능성을 분석하고 개선 방향을 제시합니다.

---

## 2. Architecture Comparison

### 2.1 Core Mechanism Differences

| Aspect | An's System (V3.8) | Agent Teams (Opus 4.6) |
|--------|---------------------|------------------------|
| **Execution Model** | Single session, subagent fork within same context | Multiple independent Claude Code sessions |
| **Orchestration** | CLAUDE.md chain patterns (A~J) + Hook auto-analysis | Team lead + shared task list + mailbox messaging |
| **Communication** | Subagent returns result to main agent only | Direct teammate-to-teammate messaging |
| **Context** | Shared main session context, forked window | Fully independent context per teammate |
| **Configuration** | ~/.claude/agents/ + CLAUDE.md chain mapping | ~/.claude/teams/ + natural language instruction |
| **Token Cost** | Lower (results summarized back) | Higher (N independent context windows) |
| **Status** | Production (V3.8, actively used) | Experimental (env variable required) |

---

## 3. Conflict Analysis

| # | Conflict Area | Severity | Description |
|---|---------------|----------|-------------|
| 1 | Hook Inheritance (Teammates) | **HIGH** | Teammate 세션이 CLAUDE.md + hooks를 상속하여 4-Layer 분석이 모든 teammate에서 중복 실행 |
| 2 | Memory System Race Condition | **HIGH** | 다수 teammate가 동시에 ~/.claude/memory/에 쓰면 YYMM_SEQ 네이밍 충돌 발생 |
| 3 | Chain vs Team Orchestration Overlap | **MEDIUM** | Dynamic Chain과 Agent Teams 모두 에이전트 조율을 시도, 이중 오케스트레이션 위험 |
| 4 | Context Token Multiplication | **MEDIUM** | CLAUDE.md (841줄) × N teammates = 대량 토큰 소비, Max $100 한도 압박 |
| 5 | Task System Duplication | **LOW** | 기존 TodoWrite + 체인 TODO와 Agent Teams shared task list가 이중 관리 |
| 6 | Permission Inheritance | **LOW** | Teammate가 lead의 52개 allow 권한 전체 상속, 불필요한 권한 노출 |

### 3.1 [HIGH] Hook Inheritance - 4-Layer 분석 중복 실행

**Problem:** Agent Teams의 teammate는 작업 디렉토리의 CLAUDE.md와 settings.json을 로드합니다. 앤의 settings.json에는 UserPromptSubmit hook(auto-analyze.sh)이 등록되어 있어, 모든 teammate가 프롬프트 입력 시마다 4-Layer 분석을 독립적으로 실행하게 됩니다.

- Teammate 3명 × 프롬프트 10회 = 4-Layer 분석 30회 (불필요한 토큰 소비)
- prompt_analyzer.py가 MCP 서버(prompt-analyzer)와 동시 접근 시 경합 발생 가능
- 이전 프롬프트 자동 저장 (V3.8) 기능이 teammate 간 상태 파일(/tmp/claude_prev_prompt_state.json) 충돌

### 3.2 [HIGH] Memory System Race Condition

**Problem:** 앤의 '응답 완료 프로토콜'에 따르면 모든 의미 있는 작업 후 ~/.claude/memory/에 YYMM_SEQ_keyword.md 형식으로 저장합니다. Agent Teams에서 여러 teammate가 동시에 작업을 완료하면:

- Teammate A와 B가 동시에 '최근 메모리 3개 읽기' → 같은 SEQ 번호 산출
- 2602_023_xxx.md를 두 teammate가 동시 생성 시도 → 파일 덮어쓰기 또는 실패
- 중복 방지 규칙(최근 3개 확인)이 동시성 환경에서 무력화

### 3.3 [MEDIUM] Chain vs Team Orchestration Overlap

**Problem:** 앤의 Dynamic Chain은 CLAUDE.md 내 체인 패턴으로 에이전트를 순차/병렬 조합합니다. Agent Teams는 별도의 task list + messaging으로 조율합니다. 둘을 동시에 사용하면:

- Lead 세션이 DevChain 실행 → subagent fork + 동시에 teammate에게 같은 작업 할당 = 이중 실행
- 체인의 '→ (순차)' 제어가 teammate의 독립 실행과 충돌
- 어떤 오케스트레이션이 우선인지 모호 (CLAUDE.md chain vs. Team lead 지시)

### 3.4 [MEDIUM] Context Token Multiplication

**Problem:** 현재 CLAUDE.md V3.8은 841줄(약 15,000+ 토큰)입니다. Agent Teams에서 각 teammate가 이를 독립적으로 로드하면:

- Teammate 4명 = CLAUDE.md만 약 60,000 토큰 소비
- 현재 세션에서 이미 144K/180K (80%) 사용 중, autocompact 빈번 발동
- Max $100 플랜의 5시간 rolling limit에 빠르게 도달

---

## 4. Improvement Recommendations

### 4.1 Hook 분기 처리 (Team-Aware Hooks)

**Target:** Conflict #1 해결

auto-analyze.sh에 teammate 감지 로직을 추가하여, teammate 세션에서는 4-Layer 분석을 건너뛰도록 합니다.

**구현 방법:** 환경변수 CLAUDE_CODE_AGENT_TEAM_ROLE 또는 ~/.claude/teams/ 디렉토리 존재 여부로 팀 모드를 감지하고, teammate인 경우 hook을 스킵합니다. /tmp/claude_prev_prompt_state.json도 세션 ID별로 분리합니다.

### 4.2 Memory Locking Mechanism

**Target:** Conflict #2 해결

메모리 저장 시 파일 기반 잠금(lock file)을 도입하거나, Lead 세션만 메모리를 관리하도록 역할을 분리합니다.

- **Option A:** ~/.claude/memory/.lock 파일로 원자적(atomic) 순차 쓰기 보장
- **Option B (권장):** Teammate는 결과를 Lead에게 메시지로 전달 → Lead만 메모리 저장 실행
- **Option C:** 세션 ID 기반 네임스페이스 분리 (YYMM_SEQ_SESSID_keyword.md)

### 4.3 Orchestration Layer 분리

**Target:** Conflict #3 해결

기존 Dynamic Chain과 Agent Teams의 사용 시나리오를 명확히 구분합니다.

| Scenario | Use Dynamic Chain | Use Agent Teams |
|----------|-------------------|-----------------|
| **Sequential pipeline** | O (requirements → architect → dev → review) | X |
| **Independent parallel research** | X | O (각 teammate가 다른 각도 조사) |
| **Cross-layer development** | X | O (frontend/backend/test 분리 소유) |
| **Quick hotfix** | O (HotfixChain) | X (overhead too high) |
| **System design + review** | O (SystemDesignChain) | Hybrid possible |
| **Large multi-module feature** | X (context limit) | O (module per teammate) |

### 4.4 CLAUDE.md Lite for Teammates

**Target:** Conflict #4 해결

Teammate용 경량 CLAUDE.md를 생성하여 불필요한 컨텍스트 소비를 줄입니다.

- 현재: 841줄 전체 로드 (Chain 패턴, Rails 시스템, 변경이력 등 teammate에 불필요)
- 제안: Core Principles + Agent Mapping + Memory Rules만 포함한 200줄 이하 경량 버전
- 구현: 프로젝트별 .claude/CLAUDE.md에 teammate 전용 버전 배치 또는 spawn prompt에 핵심만 포함

### 4.5 Chain-to-Team Migration Path

**Target:** 장기적 시스템 통합

Agent Teams가 정식 출시되면 일부 체인 패턴을 Team 구성으로 자연스럽게 전환할 수 있습니다.

| Chain | Current (Subagent) | Future (Agent Team) |
|-------|---------------------|---------------------|
| **ResearchChain** | WebSearch ∥ Context7 → analyst → sage | 3 teammates: Researcher / Analyst / Synthesizer |
| **GameDevChain** | Roblox ∥ Web 듀얼 트랙 | 2 teammates: Roblox Dev / Web Dev + Lead review |
| **WebDevChain+** | Design → Frontend → Testing 순차 | 3 teammates: Designer / Developer / Tester |
| **DevChain** | Sequential pipeline (keep as-is) | Not recommended (sequential dependency) |
| **HotfixChain** | Fast single-session (keep as-is) | Not recommended (overhead too high) |

---

## 5. Conclusion

결론적으로, 앤의 Dynamic Chain Orchestration V3.8과 Opus 4.6 Agent Teams는 **직접적인 기능 충돌은 없습니다.** Agent Teams는 아직 experimental이며, 별도의 환경변수(CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)를 설정하지 않으면 활성화되지 않습니다.

그러나 두 시스템을 동시에 사용할 경우, Hook 중복 실행(#1)과 Memory Race Condition(#2)은 반드시 해결해야 할 HIGH 레벨 이슈입니다. 현재 Agent Teams를 활성화하지 않은 상태라면 기존 시스템은 안전하게 작동합니다.

**권장 액션:**

- **단기:** Agent Teams 미활성화 상태에서 기존 시스템 유지 (현재 상태, 안전)
- **중기:** Agent Teams 정식 출시 시 Hook 분기 처리 + Memory 잠금 구현
- **장기:** ResearchChain, GameDevChain 등 병렬성 높은 체인을 Agent Teams로 점진적 전환
