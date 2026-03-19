---
title: "Claude Code 메모리 시스템 현황 분석 및 개선 방향"
version: "1.2.0"
created: "2026-03-14"
updated: "2026-03-14"
tags: [claude-code, memory-system, analysis, improvement, auto-memory]
status: completed
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: 현재 메모리 시스템 전면 분석 + 공식 메모리 기능 조사 + 갭 분석

### 다음 작업 (TODO)
- [ ] 메모리 읽기 메커니즘 개선안 설계 (SessionStart Hook 또는 InstructionsLoaded Hook 활용)
- [ ] 공식 Auto Memory와 커스텀 메모리의 통합 전략 수립
- [ ] 메모리 검색/연결 그래프 프로토타입 개발
- [ ] MEMORY.md 200줄 제한 대응 — 인덱스 최적화
- [ ] 의미 기반 메모리 검색 시스템 설계

### 작업 조언
> [!tip] 다음 Claude Code에게
> - **핵심 문제**: 현재 메모리는 저장(Write)은 잘 되지만, 읽기(Read)가 체계적으로 이루어지지 않는다
> - 공식 Auto Memory가 2026년 3월 기준 모든 사용자에게 무료 제공 중이다
> - `~/.claude/CLAUDE.md` Section 3(Memory & Protocol)과 `auto-analyze.sh` Hook이 핵심 파일이다
> - 공식 문서: https://code.claude.com/docs/en/memory
> - [[01_001_Current_System_Analysis]] 보고서의 전략적 권고 R4(메모리 아키텍처 재설계)와 연결된다
> - InstructionsLoaded Hook이 공식적으로 제공되므로 이를 활용한 메모리 자동 로드 검토 필요

---

# Claude Code 메모리 시스템 현황 분석 및 개선 방향

> **분석 방법론**: ResearchChain (WebSearch ∥ Explore ∥ WebFetch) → 분석 → Write
> **분석 일자**: 2026-03-14

---

## 1. Executive Summary

현재 메모리 시스템은 **"쓰기 편향(Write-Biased)"** 구조이다. Hook이 매 프롬프트마다 메모리 저장을 지시하지만, **세션 시작 시 과거 메모리를 자동으로 읽어오는 메커니즘이 사실상 부재**하다. MEMORY.md 인덱스(200줄 제한)만 로드될 뿐, 실제 메모리 파일의 내용은 Claude가 자발적으로 읽지 않으면 참조되지 않는다.

| 측면 | 현재 상태 | 문제점 |
|------|----------|--------|
| **저장 (Write)** | ✅ 매 프롬프트마다 Hook이 저장 지시 | 과도한 저장, 중복 가능성 |
| **인덱스 로드** | ⚠️ MEMORY.md 첫 200줄 자동 로드 | 인덱스만 보이고 실제 내용은 미로드 |
| **내용 읽기 (Read)** | ❌ 자동 읽기 메커니즘 부재 | 세션 시작 시 과거 컨텍스트 복원 안 됨 |
| **연결/검색** | ❌ 의미 기반 검색 없음 | 관련 메모리를 찾으려면 수동 탐색 필요 |

---

## 2. 현재 커스텀 메모리 시스템 상세 분석

### 2.1 아키텍처 개요

```
[사용자 프롬프트 입력]
    ↓
[auto-analyze.sh V3.0] ← UserPromptSubmit Hook
    ├── 이전 프롬프트 메모리 저장 지시 (additionalContext 주입)
    ├── 4-Layer 분석 실행
    └── 프롬프트 순번 추적 (/tmp/claude_prev_prompt_state_${SESSION_ID}.json)
    ↓
[Claude가 저장 지시 수신]
    ├── 최근 메모리 3개 확인 (중복 방지)
    ├── 저장 여부 판단
    └── YYMM_SEQ_keyword.md 파일 생성/갱신
    ↓
[MEMORY.md 인덱스 업데이트]
```

### 2.2 저장 (Write) 메커니즘 — 상세

**트리거**: `auto-analyze.sh` V3.0의 UserPromptSubmit Hook

```bash
# auto-analyze.sh 핵심 로직 (요약)
1. SESSION_ID 기반 상태 파일에서 이전 프롬프트 로드
2. 이전 프롬프트가 존재하면 → "🧠 [AUTO-MEMORY-SAVE] 이전 프롬프트 저장 필요" 주입
3. 현재 프롬프트를 상태 파일에 저장 (다음 턴에서 사용)
```

**저장 규칙** (CLAUDE.md Section 3):

| 규칙 | 내용 |
|------|------|
| 파일명 | `YYMM_SEQ_keyword.md` (예: `2603_006_v421_system_analysis.md`) |
| 중복 방지 | 저장 전 최근 3개 메모리 확인 → 동일 주제면 업데이트 |
| 저장 판단 | 분석/설계/결정/인사이트 → 저장 O / 단순 Q&A/파일 읽기 → 저장 X |
| 격리 규칙 | Agent/Teammate는 메모리 저장 **절대 금지** → Lead만 저장 |
| 마지막 프롬프트 | Hook이 감지 못함 → `/memory-save` 수동 실행 필요 |

**문서 구조**:
```markdown
# [작업 제목]
## 사용자 프롬프트
## 메타 정보 (작성일, 요약, 시사점)
## 사용된 도구 (Chain, Agents, Skills, Tools)
## 내용
## 관련 메모리
```

**현재 저장량**: 125개+ 메모리 파일 (2026년 2~3월)

### 2.3 읽기 (Read) 메커니즘 — 상세

> [!danger] 핵심 문제: 읽기 메커니즘이 사실상 부재

**MEMORY.md 인덱스 자동 로드**:
- Claude Code는 세션 시작 시 `MEMORY.md`의 **첫 200줄**만 자동 로드
- 현재 MEMORY.md는 단순 테이블 (파일명 | 주제 | 날짜)
- 인덱스를 보고 실제 파일을 읽으려면 Claude가 **자발적으로** Read 도구를 사용해야 함

**CLAUDE.md의 읽기 규칙** (실제 내용):
```
## When to access memories
- When specific known memories seem relevant to the task at hand.
- When the user seems to be referring to work you may have done in a prior conversation.
- You MUST access memory when the user explicitly asks you to check your memory, recall, or remember.
```

**문제 분석**:

| 기대 동작 | 실제 동작 | 갭 |
|----------|----------|-----|
| 세션 시작 시 최근 3개 메모리 자동 읽기 | MEMORY.md 인덱스만 로드, 실제 파일 미읽기 | **Critical** |
| 관련 작업 시 과거 메모리 참조 | Claude가 자발적으로 읽어야 하나 대부분 생략 | **High** |
| 사용자 요청 시 메모리 검색 | "기억해?" 등 명시적 요청 시만 작동 | **Medium** |

### 2.4 "세션 시작 시 3개 읽기" 규칙 분석

앤이 설정한 규칙 (CLAUDE.md Section 3 "응답 완료 프로토콜"):

```
1. 최근 메모리 3개 읽기 (중복 방지)
2. 저장 여부 판단
3. 중복이면 기존 파일 업데이트, 새 주제면 새 파일 생성
4. 💾 메모리 저장 완료 → 🎵 완료! 다음은 뭘 할까요?
```

> [!warning] 이 규칙의 문제
> "최근 메모리 3개 읽기"는 **저장 전 중복 방지** 목적이지, **세션 시작 시 컨텍스트 복원** 목적이 아니다. 세션 시작 시 자동으로 과거 메모리를 읽는 규칙은 **존재하지 않는다**.

### 2.5 SessionStart Hook 분석

```json
// settings.json의 SessionStart Hook
"SessionStart": [
  {
    "hooks": []  // ← 비어 있음!
  }
]
```

> [!danger] SessionStart Hook이 의도적으로 비활성화됨
> 메모리 파일 `2602_002`에 따르면 오케스트레이션 안정화 과정에서 SessionStart Hook을 **의도적으로** 빈 배열로 변경했다. 당시에는 합리적 결정이었으나, 메모리 읽기 메커니즘의 공백을 만든 원인이 되었다.
>
> 또한 `session-memo-writer` 에이전트가 `/agents/archive/`에 존재하지만 비활성 상태이다. 이 에이전트에는 "Phase 1: 이전 메모 읽기" 로직이 있었으나 폐기되었다.

---

## 3. Claude 공식 메모리 시스템 분석

### 3.1 공식 Auto Memory (Claude Code)

> 출처: [How Claude remembers your project](https://code.claude.com/docs/en/memory)

| 항목 | 내용 |
|------|------|
| **도입 시기** | Claude Code v2.1.59+ |
| **기본 상태** | **기본 활성화** (`autoMemoryEnabled: true`) |
| **저장 위치** | `~/.claude/projects/<project>/memory/` |
| **인덱스** | `MEMORY.md` (첫 200줄만 세션 시작 시 로드) |
| **토픽 파일** | 세션 시작 시 미로드, **필요 시 on-demand 읽기** |
| **저장 주체** | Claude가 자율적으로 판단 (매 세션 저장하지 않음) |
| **토글** | `/memory` 명령 또는 `autoMemoryEnabled` 설정 |

**공식 시스템의 2가지 메모리**:

| | CLAUDE.md | Auto Memory |
|---|---------|------------|
| **작성자** | 사용자 | Claude |
| **내용** | 지시/규칙 | 학습/패턴 |
| **로드** | 매 세션 전체 | 매 세션 첫 200줄만 |
| **용도** | 코딩 표준, 워크플로우 | 빌드 명령, 디버깅, 선호도 |

### 3.2 공식 Chat Memory (Claude.ai/Desktop)

> 출처: [Claude Help Center](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)

| 항목 | 내용 |
|------|------|
| **도입** | 2025년 8월 (유료), 2026년 3월 (무료 확대) |
| **작동** | 대화 히스토리를 자동 요약, 24시간마다 업데이트 |
| **범위** | 모든 대화에 컨텍스트 제공 |
| **플랫폼** | Web, Desktop, Mobile |
| **메모리 임포트** | ChatGPT/Gemini에서 메모리 가져오기 가능 |

### 3.3 공식 Memory Tool (API)

> 출처: [Memory tool - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)

API 수준에서 에이전트가 메모리를 읽고 쓸 수 있는 도구. 커스텀 에이전트 개발 시 활용 가능.

### 3.4 최근 발표 (2026년 3월)

| 날짜 | 발표 | 출처 |
|------|------|------|
| 2026-03-02 | 메모리 기능 무료 사용자 확대 | [MacRumors](https://www.macrumors.com/2026/03/02/anthropic-memory-import-tool/) |
| 2026-03-03 | 메모리 임포트 도구 출시 (ChatGPT→Claude) | [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-03/anthropic-tries-to-win-users-from-chatgpt-with-memory-feature) |
| 2026-03-14 | 1M 토큰 컨텍스트 윈도우 GA | [WebAndITNews](https://www.webanditnews.com/2026/03/14/anthropic-hands-every-claude-user-a-million-token-memory-and-the-race-for-infinite-context-just-got-real/) |

---

## 4. 갭 분석: 커스텀 vs 공식 vs 이상

### 4.1 기능 매트릭스

| 기능 | 공식 Auto Memory | 앤의 커스텀 시스템 | 이상적 시스템 |
|------|-----------------|-------------------|-------------|
| 자동 저장 | ✅ Claude 자율 판단 | ✅ Hook 강제 지시 | ✅ 지능적 선택 저장 |
| 세션 시작 로드 | ⚠️ MEMORY.md 200줄만 | ⚠️ MEMORY.md 200줄만 | ✅ 관련 메모리 자동 로드 |
| 토픽 파일 읽기 | ⚠️ On-demand | ❌ 거의 안 읽음 | ✅ 작업 관련성 기반 자동 |
| 구조화된 문서 | ❌ 자유 형식 | ✅ YYMM_SEQ 표준 형식 | ✅ 구조 + 의미 태깅 |
| 중복 방지 | ❌ 없음 | ✅ 최근 3개 확인 | ✅ 의미 기반 중복 감지 |
| 에이전트 격리 | ❌ 없음 | ✅ Lead-only 규칙 | ✅ 역할 기반 접근 제어 |
| 메모리 검색 | ❌ 없음 | ❌ 없음 | ✅ 의미 기반 검색 |
| 연결 그래프 | ❌ 없음 | ⚠️ 관련 메모리 수동 | ✅ 자동 연결 + 시각화 |
| 세션 간 연속성 | ⚠️ 약함 | ⚠️ 약함 | ✅ 완전한 컨텍스트 복원 |

### 4.2 핵심 갭 3개

#### GAP 1: 읽기 메커니즘 부재 (Critical)

```
현재: 저장 → 인덱스 → (끝)
이상: 저장 → 인덱스 → 세션 시작 시 관련 메모리 자동 로드 → 작업 중 추가 참조
```

**원인**: SessionStart Hook이 비어 있고, CLAUDE.md에 "세션 시작 시 자동 읽기" 규칙이 없다. "최근 3개 읽기"는 저장 전 중복 방지 목적이지 세션 복원 목적이 아니다.

#### GAP 2: 의미 기반 검색 부재 (High)

125개+ 메모리 파일이 있지만, 현재 작업과 관련된 메모리를 찾는 방법이 없다. MEMORY.md의 테이블을 훑어보는 것이 유일한 방법이며, 200줄 제한으로 오래된 메모리는 인덱스에서도 잘린다.

#### GAP 3: 세션 간 연속성 부재 (High)

어제 작업한 내용을 오늘 이어서 할 때, Claude는 어제의 맥락을 모른다. 메모리 파일에 기록은 되어 있지만 자동으로 로드되지 않으므로, 사용자가 "어제 했던 작업 기억해?"라고 명시적으로 요청해야 한다.

---

## 5. 근본 원인 분석 (5-Why)

```
Why 1: 왜 메모리가 읽히지 않는가?
→ 세션 시작 시 메모리를 자동 로드하는 메커니즘이 없다

Why 2: 왜 자동 로드 메커니즘이 없는가?
→ SessionStart Hook이 비어 있고, CLAUDE.md에 읽기 규칙이 모호하다

Why 3: 왜 읽기 규칙이 모호한가?
→ 시스템 설계 시 "저장"에 집중했고, "검색/복원"은 후순위였다

Why 4: 왜 저장에 집중했는가?
→ LLM의 세션 간 연속성 부재가 가장 급한 문제였고, "일단 저장"이 첫 단계였다

Why 5: 왜 검색으로 진화하지 못했는가?
→ 메모리 읽기 실패가 "눈에 보이는 고장"이 아니어서 incident-driven 진화에서 감지되지 않았다
```

> [!important] 근본 원인
> 메모리 읽기 실패는 **"침묵하는 고장(Silent Failure)"**이다. 저장 실패는 에러 메시지로 감지되지만, 읽기 누락은 "Claude가 그냥 모르는 것처럼 보일 뿐" 사용자가 원인을 특정하기 어렵다. 이것이 시스템의 incident-driven 진화에서 이 문제가 늦게 발견된 이유이다.

---

## 6. 개선 전략 (4단계 로드맵)

### Phase 1: 즉시 개선 — 세션 시작 메모리 로드 (1세션)

**목표**: 세션 시작 시 최근 관련 메모리를 자동 로드

**방법 A: CLAUDE.md 규칙 강화**
```markdown
## 세션 시작 프로토콜 (MANDATORY)
1. MEMORY.md 인덱스를 읽는다
2. 최근 메모리 3개의 **실제 파일**을 Read 도구로 읽는다
3. 현재 작업 디렉토리와 관련된 메모리가 있으면 추가로 읽는다
4. 읽은 메모리의 핵심 컨텍스트를 인지한 후 작업을 시작한다
```

**방법 B: SessionStart Hook 활용**
```bash
# SessionStart Hook에서 최근 메모리 3개를 additionalContext로 주입
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's/\//-/g')/memory"
RECENT=$(ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -3)
# 각 파일의 첫 20줄을 additionalContext로 전달
```

**방법 C: InstructionsLoaded Hook 활용** (공식 지원)
```
InstructionsLoaded Hook이 공식 제공됨 → 지시 파일 로드 시점에 메모리 로드 트리거
```

**권장**: 방법 A(즉시 적용 가능) + 방법 B(자동화)

### Phase 2: 단기 개선 — MEMORY.md 인덱스 최적화 (1~2세션)

**목표**: 200줄 제한 내에서 최대한 유용한 인덱스 제공

**개선안**:
- 카테고리별 그룹핑 (프로젝트별, 작업 유형별)
- 최근 10개 메모리에 1줄 요약 포함
- 오래된 메모리는 카테고리별 카운트만 표시
- 자주 참조되는 메모리에 ⭐ 마킹

```markdown
# Memory Index

## 최근 (자동 로드 대상)
| 파일 | 요약 | 날짜 |
|------|------|------|
| `2603_006_*.md` | V4.2.1 시스템 종합 분석 - Observability 최우선 권고 | 03-14 |
| `2603_005_*.md` | 1012 폴더 CLAUDE.md 설정 - 상호 접근 제어 | 03-14 |

## 프로젝트별 (필요 시 참조)
- claude-code (8개): 시스템 설계, 테스트, 개선
- roblox (5개): 게임 개발
- ...
```

### Phase 3: 중기 개선 — 의미 기반 메모리 연결 (2~3세션)

**목표**: 현재 작업과 관련된 메모리를 자동으로 찾아 제안

**방법**:
- 메모리 파일의 태그/키워드 기반 매칭
- 현재 프롬프트의 키워드 → 메모리 파일의 키워드 대조
- `prompt_analyzer.py`를 확장하여 메모리 매칭 기능 추가

### Phase 4: 장기 개선 — 지식 그래프 메모리 (미래)

**목표**: 메모리 간 관계를 그래프로 관리, 컨텍스트 복원 자동화

**구성 요소**:
- 메모리 노드 (각 파일)
- 관계 엣지 (선행/후속/관련/반박/보강)
- 중요도 가중치 (사용 빈도, 최신성)
- MCP 서버로 구현하여 검색/추천 API 제공

---

## 7. 공식 기능 활용 전략

### 7.1 공식 Auto Memory + 커스텀 시스템 병행

| 용도 | 시스템 | 이유 |
|------|--------|------|
| 빌드 명령, 코드 스타일 | **공식 Auto Memory** | 자동 학습에 적합 |
| 분석 결과, 설계 결정 | **커스텀 메모리** | 구조화된 기록 필요 |
| 프로젝트 컨텍스트 | **CLAUDE.md** | 매 세션 전체 로드 |
| 세션 간 작업 연속 | **커스텀 + 개선된 읽기** | 자동 복원 필요 |

### 7.2 공식 InstructionsLoaded Hook 활용

```
공식 문서에서 InstructionsLoaded Hook이 언급됨:
"Use the InstructionsLoaded hook to log exactly which instruction files are loaded,
 when they load, and why."
```

이 Hook을 활용하면 지시 파일 로드 시점에 메모리 로드를 트리거할 수 있다.

### 7.3 서브에이전트 메모리

```
공식 문서: "Subagents can also maintain their own auto memory.
See subagent configuration for details."
```

현재 커스텀 시스템에서는 서브에이전트 메모리를 금지하고 있지만, 공식 기능이 지원되므로 안전한 활용 방법을 검토할 수 있다.

---

## 8. 즉시 실행 가능한 액션 목록

| 우선순위 | 액션 | 파일 | 효과 |
|---------|------|------|------|
| **P0** | CLAUDE.md에 "세션 시작 시 최근 3개 메모리 파일 Read" 규칙 추가 | `~/.claude/CLAUDE.md` | 즉시 읽기 개선 |
| **P0** | SessionStart Hook에 메모리 요약 주입 스크립트 추가 | `~/.claude/hooks/` + `settings.json` | 자동 컨텍스트 복원 |
| **P1** | MEMORY.md 인덱스를 카테고리+요약 형식으로 재구성 | `~/.claude/projects/*/memory/MEMORY.md` | 인덱스 유용성 향상 |
| **P1** | "응답 완료 프로토콜"에서 "읽기"와 "중복 방지"를 분리 명시 | `~/.claude/CLAUDE.md` | 규칙 혼동 해소 |
| **P2** | prompt_analyzer.py에 메모리 키워드 매칭 추가 | `~/.claude/scripts/prompt_analyzer.py` | 의미 기반 추천 |

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[01_001_Current_System_Analysis#7. 전략적 권고 TOP 5|R4 메모리 재설계 권고]] — 본 문서의 분석이 R4 권고의 상세 근거
- [[02_001_Claude_Code_Official_Docs_Core_Engine#2.4 Auto Memory 동작 원리|공식 Auto Memory]] — MEMORY.md 200줄 로드, 토픽 파일 on-demand

### 역참조 (Backlinks)
- [[01_001_Improvement_Direction_Overview#C1. 온톨로지 메모리 시스템|C1 개선 방향]] — 본 문서의 GAP 1~3이 C1 카테고리의 근거
- [[01_001_Current_System_Analysis#6. 핵심 위험 TOP 3|시스템 위험 3]] — Observability 부재를 메모리 맥락에서 참조

### 관련 주제 (Topic Links)
- [[05_001_Intelligence_Architecture_Ontology_Research#1.2 데이터 정제 및 온톨로지 구축 파이프라인|온톨로지 파이프라인]] — 메모리 벡터화 → 그래프 RAG의 기술적 해결책
- [[03_001_Ontology_YouTube_Summary#1. 온톨로지의 모든 것|액티브 온톨로지]] — 메모리를 동적 지식 구조로 전환하는 개념적 기반
- [[07_001_Neural_Reference_Deep_Analysis#4.2 컨텍스트 윈도우 보존|컨텍스트 보존]] — 신경망 참조로 메모리 로드 시 토큰 90%+ 절감

---

## Release Notes

### v1.2.0 (2026-03-15)
- 관련 문서 섹션을 Neural Map 형식(Direct/Backlink/Topic)으로 전면 교체
- 07_001 신경망 참조 시스템 적용: 섹션 레벨 `#앵커` + 관계 설명
> **프롬프트:** "102 CLAUDE.md 참고해서 101 CLAUDE.md를 고쳐줘. 07_001 문서를 참조해서 101의 01_ 2개 문서를 수정해줘"

### v1.1.0 (2026-03-14)
- Explore 에이전트 결과 반영: SessionStart Hook 의도적 비활성화 확인 (2602_002 문서)
- session-memo-writer 에이전트가 archive에 존재하나 비활성 상태 확인
- 상태 파일(`/tmp/claude_prev_prompt_state_${SESSION_ID}.json`) 세션 종료 시 소실 확인
- 메모리 파일 실제 수량: 프로젝트별 13개 (전체 시스템 125개 컴포넌트와 별도)
- Section 2.5에 SessionStart Hook 의도적 비활성화 배경 추가

### v1.0.0 (2026-03-14)
- 초기 작성: 메모리 시스템 현황 전면 분석
- 커스텀 메모리 시스템 Write/Read 메커니즘 상세 분석
- 공식 Auto Memory (Claude Code) + Chat Memory (Claude.ai) 조사
- 갭 분석: 3개 핵심 갭 식별 (읽기 부재, 검색 부재, 연속성 부재)
- 5-Why 근본 원인: "침묵하는 고장(Silent Failure)"
- 4단계 개선 로드맵 제시
- 즉시 실행 가능한 액션 5개 도출
- 앤 프롬프트: *"현재 적용된 메모리 시스템에 대해 신규 문서를 만들어줘 어떻게 수집하는지 작업을 진행할때 어떻게 메모리를 읽어오는지 저장만하고 작업시 읽어오지 않는것 같기도 하고 이전에 내가 3개를 세션 시작시 불러오라고 세팅했는데 잘 작동하지 않는거 같기도 하고 세심히 분석해서 상세히 보고서 써줘 난 메모리 시스템을 혁신적으로 개선할려해. 그리고 클로드에서 공식적으로 메모리 기능을 제공하기 시작했어 웹을 검색해 해당 내용을 찾아서 그 내용도 넣어줘"*

Sources:
- [How Claude remembers your project - Claude Code Docs](https://code.claude.com/docs/en/memory)
- [Anthropic Makes Claude Memory Feature Free For All Users](https://dataconomy.com/2026/03/04/anthropic-makes-claude-memory-feature-free-for-all-users/)
- [Anthropic Adds Free Memory Feature and Import Tool](https://www.macrumors.com/2026/03/02/anthropic-memory-import-tool/)
- [Claude Code Memory Explained](https://joseparreogarcia.substack.com/p/claude-code-memory-explained)
- [Claude Help Center - Memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)
