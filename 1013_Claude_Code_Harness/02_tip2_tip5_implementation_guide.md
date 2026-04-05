---
title: "Tip #2 CLAUDE.md 투자 + Tip #5 검증 루프 — 구현 가이드"
version: "1.0.0"
created: "2026-04-05"
updated: "2026-04-05"
tags: [claude-code, lessons-learned, verification-loop, L1-L2-cache, implementation-guide]
status: completed
type: design
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Mac에서 수행한 Tip #2 + #5 구현 내역을 Windows 재현용 가이드로 작성

### 다음 작업 (TODO)
- [ ] Windows 회사컴에서 이 가이드를 따라 동일하게 적용
- [ ] 적용 후 테스트 (L1 기록→삭제, 검증 루프 체인 실행)

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 Mac에서 수행한 작업을 Windows에서 재현하기 위한 **실행 가이드**
> - 모든 파일 내용이 포함되어 있으므로 그대로 복사-붙여넣기 가능
> - `~/.claude/` 경로는 Windows에서 `%USERPROFILE%\.claude\`로 치환
> - 수정 전 반드시 기존 파일 백업할 것

---

# Tip #2 CLAUDE.md 투자 + Tip #5 검증 루프 — 구현 가이드

## 개요

Claude Code 창시자 Boris + 해커톤 우승자의 7가지 팁 중 **#2(CLAUDE.md 실수 기록)** 와 **#5(검증 루프)** 를 Mac에서 구현한 내역을 정리. Windows 회사컴에서 동일 작업을 재현하기 위한 상세 가이드.

### 작업 배경

| 참조 문서 | 위치 |
|----------|------|
| 원본 7가지 팁 정리 | `1013_Claude_Code_Harness/01_claude_code_7_best_practices.md` |
| CLAUDE.md | `~/.claude/CLAUDE.md` (V5.1.0) |
| 오케스트레이션 | `~/.claude/rules/orchestration.md` |
| 메모리 프로토콜 | `~/.claude/rules/memory-protocol.md` |

---

## Part A: Tip #2 — L1/L2 실수 기록 캐시 시스템

### A-1. 설계 요약

Boris의 핵심 메시지: **"실수 발생 → CLAUDE.md에 기록 → 동일 실수 반복 방지"**

이를 CPU L1/L2 캐시 비유로 구현:

| 계층 | 위치 | 특성 | 용량 |
|------|------|------|------|
| **L1** | `rules/lessons-learned.md` | 항상 로드, 즉시 참조 | MAX 100항목 |
| **L2** | `memory/` (feedback type) | 벡터 리콜, 필요 시 검색 | 무제한 |

졸업 로직: L1이 101번째 → oldest를 L2로 이동 (PIN 마킹된 항목은 면제)

### A-2. 수정 파일 목록 (3개)

#### 파일 1: `~/.claude/rules/lessons-learned.md` (신규 생성)

```markdown
## 4. Lessons Learned (L1 Cache)

> **항상 로드** — 앤의 교정/거부에서 추출한 핵심 실수 기록
> MAX 100항목. 초과 시 가장 오래된 항목을 feedback memory(L2)로 졸업.

### 운영 규칙
- 앤이 교정/거부/불만 표시 시 → 즉시 이 파일에 기록
- 항목 형식: `| # | 실수 요약 | 회피법 | 등록일 | PIN |`
- LLM 성능 향상 시 → MAX를 줄여 L2 전환 (앤 판단)

### 졸업 로직 (L1 → L2)
- **트리거**: 101번째 항목 등록 시
- **졸업 대상**: 등록일이 가장 오래된 항목
- **졸업 절차**:
  1. 해당 항목을 feedback memory(L2)로 저장 (`memory/YYMM_SEQ_graduated_lesson.md`)
  2. L1 테이블에서 삭제
  3. 번호 재정렬
- **졸업 면제**: 앤이 `[PIN]` 마킹한 항목은 졸업 대상에서 제외

### 실수 기록

| # | 실수 요약 | 회피법 | 등록일 | PIN |
|---|----------|--------|--------|-----|
```

#### 파일 2: `~/.claude/rules/orchestration.md` — §2.1 수정

아래 1줄을 §2.1 Hook 분석 흐름의 **"이전 프롬프트 자동 저장"** 항목 바로 다음에 추가:

```markdown
**실수 기록 의무**: 앤이 교정("아니", "그거 말고", "다시")하거나 거부하면 → `rules/lessons-learned.md` L1에 즉시 기록 + feedback memory(L2) 동시 저장. 생략 금지.
```

> 정확한 삽입 위치: `**주의**: 마지막 프롬프트는...` 줄 바로 다음

#### 파일 3: `~/.claude/rules/memory-protocol.md` — 응답 완료 프로토콜 수정

기존 Step 2 다음에 Step 2-1을 추가:

```markdown
2-1. **실수 감지**: 앤의 교정/거부 발생 시 → L1(`rules/lessons-learned.md`) + L2(feedback memory) 동시 기록
```

### A-3. 검증 방법

1. `rules/lessons-learned.md` 파일 존재 확인
2. 테스트: 가짜 실수 1건 기록 → 테이블에 행 추가 확인 → 삭제
3. `orchestration.md`에서 "실수 기록 의무" grep → 1건 확인
4. `memory-protocol.md`에서 "실수 감지" grep → 1건 확인

---

## Part B: Tip #5 — 검증 루프 프로토콜 (Verification Loop)

### B-1. 설계 요약

Boris의 핵심 메시지: **"이게 된다는 걸 증명해 봐" → 품질 2~3배 향상**

기존 시스템에는 Gate 1~3 + 3종 리뷰어 인프라가 있었으나, **"실패→자동수정→재검증" 반복 루프**가 체인 정의에 없었음. 이를 추가.

| 규칙 | 내용 |
|------|------|
| 트리거 | 리뷰어 Critical 1+건 또는 Bash 테스트 실패 |
| 자동 수정 | code_developer가 Critical/실패 항목만 최소 수정 |
| 재검증 | 동일 리뷰어/테스트 재실행 |
| MAX 반복 | **3회** (원본 1회 + 재시도 2회 = 총 3회 검증) |
| MAX 초과 | 앤에게 잔여 이슈 보고 |
| Warning/Info | 재시도 트리거 아님 |

### B-2. 수정 파일 목록 (3개)

#### 파일 1: `~/.claude/rules/orchestration.md` — §2.4에 검증 루프 프로토콜 섹션 추가

삽입 위치: `> **Pre-execution Declaration 형식**:` 줄 바로 다음, 체인 A 정의 바로 위

```markdown
#### 검증 루프 프로토콜 (Verification Loop)

> **Boris 1순위 원칙**: "이게 된다는 걸 증명해 봐"
> 3종 리뷰어 또는 테스트가 있는 모든 체인에 적용 (A, B, C, D, G, J).

| 규칙 | 내용 |
|------|------|
| **트리거** | 리뷰어 Critical 1+건 또는 Bash 테스트 실패 |
| **자동 수정** | code_developer가 Critical/실패 항목만 최소 수정 |
| **재검증** | 동일 리뷰어/테스트 재실행 |
| **MAX 반복** | **3회** (원본 1회 + 재시도 2회 = 총 3회 검증) |
| **MAX 초과** | 앤에게 잔여 이슈 보고 (아래 형식) |
| **Warning/Info** | 재시도 트리거 아님 (1회차 보고 후 통과) |

**표기법**: `{검증 루프 × MAX 3}`

**잔여 보고 형식** (MAX 초과 시 필수):
```
⚠️ 검증 루프 MAX 3회 소진
- 잔여 Critical: [미해결 항목 목록]
- 시도한 수정: [각 회차별 수정 요약]
- 권장 조치: [앤에게 제안]
```
```

#### 파일 2: `~/.claude/rules/orchestration.md` — 체인 6개 표기 수정

각 체인의 마지막 줄(코드블록 닫기 ``` 바로 위)에 `→ {검증 루프 × MAX 3}` 추가:

| 체인 | 수정 전 마지막 줄 | 수정 후 |
|------|------------------|---------|
| **A. SystemDesignChain** | `→ (Edit[-] ∥ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]))` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |
| **B. AutomationChain** | `→ code_developer[O] → (Bash[-] ∥ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]))` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |
| **C. GameDevChain** | `→ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O])` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |
| **D. DevChain** | `→ code_developer[O] → ((logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]) ∥ Bash[테스트][-])` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |
| **G. WebDevChain+** | `→ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O])` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |
| **J. HotfixChain** | `→ (Bash[테스트][-] ∥ quality_reviewer[O])` | 그 다음 줄에 `→ {검증 루프 × MAX 3}` 추가 |

> E(Research), F(Doc), H(MetaThink), I(Rails)는 검증 루프 미적용 (리뷰어/테스트 없음)

#### 파일 3-1: `~/.claude/skills/chains/dev-chain.md` 전체 교체

아래 내용으로 전체 교체 (주요 변경: Step 7 검증 루프 추가, `[S]`→`[O]` 모델 통일, quality_reviewer→3종 리뷰어):

```markdown
---
name: dev-chain
description: 일반 소프트웨어 개발, 코딩, TDD. "개발", "구현", "코딩", "기능 추가" 키워드에 반응. 중규모+ 작업 시 research→plan 워크플로우 포함.
user-invocable: false
---

# DevChain (D) — Effort: MEDIUM

> 요구사항→탐색→연구→계획→구현→리뷰. 중규모 이상 작업에서 research/plan 필수.

## 체인 패턴

```
requirements_analyst[O] → (system_architect[O] ∥ Explore[O] ∥ Context7[∥])
→ [research.md 생성] → [plan.md 생성 + 승인 게이트]
→ code_developer[O] → ((logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]) ∥ Bash[테스트][-])
→ {검증 루프 × MAX 3}
```

## 단계 목록 (임의 축약 금지)

1. **[순차]** 요구사항 분석 (`requirements_analyst[opus]`)
2. **[병렬]** 아키텍처 설계 (`system_architect[opus]`) + 코드 탐색 (`Explore[opus]`) + 라이브러리 조사 (`Context7`)
3. **[순차]** **research.md 생성** — Step 2 결과를 `~/.claude/workflow/templates/research_template.md` 기반으로 작성. Gate 1 검증 (`gate1_checker.sh`)
4. **[순차]** **plan.md 생성 + 인간 승인 게이트** — research.md 기반으로 계획 작성 (Status: draft). 앤 검토 → approved 후 다음 단계 진행
5. **[순차]** TDD 구현 (`code_developer[opus]`) — 승인된 plan.md 기반으로 기계적 구현
6. **[병렬]** 3종 리뷰 (`logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]`) + 테스트 실행 (`Bash[테스트]`)
7. **[검증 루프]** Critical 1+건 또는 테스트 실패 시 → `code_developer` 최소 수정 → Step 6 재실행 (× MAX 3). MAX 초과 시 잔여 보고 후 앤 판단 위임
8. **[순차]** plan.md 체크리스트 완료 확인 — 모든 `- [ ]`가 `- [x]`로 변경 확인

## 복잡도 분기

| 복잡도 | 기준 | 워크플로우 | 인간 게이트 |
|--------|------|-----------|-----------|
| 단순 | 한 줄 수정, Q&A | Step 1→5→6 직행 (research/plan 생략) | 불필요 |
| 중규모 | 파일 3개+ 수정, 새 기능 | 전체 7단계 | 조건부 (명시적 거부 없으면 진행) |
| 대규모 | 아키텍처 변경, 신규 시스템 | 전체 7단계 | 필수 (명시적 승인 필요) |

## 트리거 조건

- "개발해줘", "구현", "코딩", "기능 추가", "만들어줘"
- DevChain 키워드 감지 시 자동 선택

## 주의사항

- **임의 축약 금지**: 정의된 7단계를 모두 실행한다
- "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
- 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
- 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다
- **Simple Task Exception**: 단순 Q&A, 한 줄 수정은 체인 자체를 생략
- **검증 루프**: Step 7에서 Critical/테스트실패 → 자동 수정 → 재검증 × MAX 3. 초과 시 잔여 보고

## Pre-execution Declaration

```
📋 체인 구성: DevChain [MEDIUM] → requirements → architect∥Explore∥Context7 → research.md → plan.md+gate → developer → 3종리뷰∥test → {검증 루프 × MAX 3} → checklist
```
```

#### 파일 3-2: `~/.claude/skills/chains/system-design.md` 전체 교체

```markdown
---
name: system-design-chain
description: 시스템 설계, 아키텍처, CLAUDE.md 업데이트, 체인 개선에 사용. "시스템 설계", "아키텍처", "체인 개선" 키워드에 반응. 메타 작업 자동 감지. 대규모 작업이므로 research→plan 워크플로우 + 인간 승인 필수.
user-invocable: false
---

# SystemDesignChain (A) — Effort: HIGH

> 모든 에이전트 완전 실행. 탐색 범위 제한 금지. 깊이 있는 분석 필수.
> 대규모 체인 — research.md + plan.md + 인간 승인 게이트 필수.

## 체인 패턴

```
(Explore[O] ∥ Read[-]) → (system_architect[O] ∥ problem_reframer[O])
→ [research.md 생성] → [plan.md 생성 + 인간 승인 게이트(필수)]
→ solution_innovator[O] → integrated_sage[O]
→ (Edit[-] ∥ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]))
→ {검증 루프 × MAX 3}
```

## 단계 목록 (임의 축약 금지)

1. **[병렬]** 코드베이스 탐색 (`Explore[opus]`) + 관련 파일 읽기 (`Read[main]`)
2. **[병렬]** 시스템 아키텍처 설계 (`system_architect[opus]`) + 관점 전환 (`problem_reframer[opus]`)
3. **[순차]** **research.md 생성** — Step 1-2 결과를 `~/.claude/workflow/templates/research_template.md` 기반으로 작성. Gate 1 검증 (`gate1_checker.sh`)
4. **[순차]** **plan.md 생성 + 인간 승인 게이트 (필수)** — research.md 기반으로 계획 작성 (Status: draft). 앤 검토 → approved 후 다음 단계 진행. SystemDesignChain은 항상 대규모이므로 인간 승인 필수.
5. **[순차]** 혁신 솔루션 도출 (`solution_innovator[opus]`)
6. **[순차]** 통합 지혜 정리 (`integrated_sage[opus]`)
7. **[병렬]** 파일 수정 (`Edit[main]`) + 3종 리뷰 (`logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]`)
8. **[검증 루프]** Critical 1+건 시 → `code_developer` 최소 수정 → Step 7 재실행 (× MAX 3). MAX 초과 시 잔여 보고 후 앤 판단 위임

## 복잡도 분기

- SystemDesignChain은 **항상 대규모**로 분류
- research.md + plan.md + 인간 승인 게이트 **필수**
- 단순 작업은 이 체인을 선택하지 않음 (HotfixChain 또는 직행)

## 트리거 조건

- "시스템 설계", "아키텍처", "체인 개선"
- 메타 작업 자동 감지 (CLAUDE.md 수정, Hook 개선 등)

## 주의사항

- **임의 축약 금지**: 정의된 8단계를 모두 실행한다
- "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
- 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
- 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다

- **검증 루프**: Step 8에서 Critical → 자동 수정 → 재검증 × MAX 3. 초과 시 잔여 보고

## Pre-execution Declaration

```
📋 체인 구성: SystemDesignChain [HIGH] → Explore∥Read → architect∥reframer → research.md → plan.md+gate(필수) → innovator → sage → Edit∥3종리뷰 → {검증 루프 × MAX 3}
```
```

### B-3. 부수 수정 사항

스킬 파일 2개에서 구버전 모델 표기 수정:

| 파일 | 변경 전 | 변경 후 |
|------|--------|--------|
| `dev-chain.md` | `code_developer[S]` | `code_developer[O]` |
| `dev-chain.md` | `quality_reviewer[S]` | 3종 리뷰어 `[O]` |
| `system-design.md` | `Explore[S]` | `Explore[O]` |
| `system-design.md` | `quality_reviewer[S]` | 3종 리뷰어 `[O]` |

> 이미 위 전체 교체 내용에 반영되어 있으므로 별도 작업 불필요

### B-4. 검증 방법

1. `orchestration.md`에서 `검증 루프 × MAX 3` grep → **7건** (프로토콜 1 + 체인 6)
2. 스킬 파일에서 `[S]` grep → **0건**
3. 스킬 파일에서 `검증 루프 × MAX 3` grep → **4건** (system-design 2 + dev-chain 2)
4. `잔여` grep → 프로토콜에 보고 형식 명시 확인

---

## 실행 순서 요약 (Windows에서)

```
[Step 1] lessons-learned.md 신규 생성
         → ~/.claude/rules/lessons-learned.md

[Step 2] orchestration.md §2.1에 "실수 기록 의무" 1줄 추가
         → 위치: "마지막 프롬프트는..." 줄 다음

[Step 3] memory-protocol.md에 "실수 감지" Step 2-1 추가
         → 위치: 기존 Step 2 다음

[Step 4] orchestration.md §2.4에 검증 루프 프로토콜 섹션 추가
         → 위치: Pre-execution Declaration 줄 다음, 체인 A 정의 직전

[Step 5] orchestration.md 체인 6개(A,B,C,D,G,J) 표기에 "→ {검증 루프 × MAX 3}" 추가
         → 각 체인 코드블록 마지막 줄 다음

[Step 6] dev-chain.md 전체 교체 (Part B 파일 3-1)

[Step 7] system-design.md 전체 교체 (Part B 파일 3-2)

[Step 8] 검증 (A-3 + B-4 체크리스트 실행)
```

> 총 수정 파일: **5개** (신규 1 + 수정 4)
> 예상 소요: Claude Code에게 이 문서를 보여주면 **5분 이내** 완료

---

## 관련 문서

### 직접 참조 (Direct Links)
- `1013_Claude_Code_Harness/01_claude_code_7_best_practices.md` — 원본 7가지 팁 정리
- `~/.claude/rules/orchestration.md` — 오케스트레이션 시스템 (수정 대상)
- `~/.claude/rules/lessons-learned.md` — L1 캐시 (신규 생성)
- `~/.claude/rules/memory-protocol.md` — 메모리 프로토콜 (수정 대상)
- `~/.claude/skills/chains/dev-chain.md` — DevChain 스킬 (수정 대상)
- `~/.claude/skills/chains/system-design.md` — SystemDesignChain 스킬 (수정 대상)

### 역참조 (Backlinks)
- (없음)

### 관련 주제 (Topic Links)
- `~/.claude/CLAUDE.md` V5.1.0 — 전체 시스템 가이드라인

---

## Release Notes

### v1.0.0 (2026-04-05)
- 초기 작성: Mac에서 수행한 Tip #2 + #5 구현 내역을 Windows 재현용 가이드로 작성
> **프롬프트:** "2번이랑 5번을 작업했어 세션이랑 메모리파일읽어서 1013 폴더에 02_ 작업내역을 상세히 기록해줘 윈도우 회사컴에게 동일한 작업을 할려고 이 용도로 작성해줘"
