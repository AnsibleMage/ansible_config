---
title: "Boris Tip #2,#3,#5,#7 — Windows 설치 계획 및 검증"
version: "5.0.0"
created: "2026-04-06"
updated: "2026-04-06"
tags: [claude-code, installation, windows, boris-tips, verification, plan-review, obsidian-cli]
status: completed
type: design
---

# Boris Tip #2,#3,#5,#7 — Windows 설치 계획 및 검증

## 개요

Mac에서 구현된 Boris 7팁 중 #2(L1/L2 실수캐시), #3(플랜모드 Pre-Mortem), #5(검증루프), #7(Hook 자동화)을 Windows 클로드코드에 적용하는 설치 계획서. 추가로 Obsidian CLI 연동, 시니어 검증 스킬(`/plan-review`) 구축까지 포함.

### 설치 전 시스템 상태

| 구성요소 | 상태 | 비고 |
|---------|------|------|
| `rules/` 3파일 | ✅ 존재 | orchestration, memory-protocol, template-protocol |
| `agents/` 30개 | ✅ 존재 | 리뷰어 3종 확신도/한계선언 미반영 |
| `templates/` 3개 | ✅ 존재 | md-general, meeting-minutes, worklog |
| `scripts/memory-recall.sh` | ✅ 존재 | SessionStart Hook 작동 중 |
| `settings.json` | ✅ 존재 | Hook 3종 가동, Stop Hook 없음 |
| `hooks/` 폴더 | ❌ 없음 | 신규 생성 필요 |
| `skills/chains/` 폴더 | ❌ 없음 | 신규 생성 필요 |
| `workflow/templates/` 폴더 | ❌ 없음 | 신규 생성 필요 |
| `rules/lessons-learned.md` | ❌ 없음 | Tip #2 핵심 |
| prettier / black | ❌ 미설치 | Tip #7 전제 |

---

## 설치 순서 (충돌 최소화 재배치)

> 원본 팁 순번(2→5→7→3) 무시. **의존성 기반 효율 순서**로 재배치.

### Phase 1: 인프라 (폴더 + 패키지) — 전제조건, 의존성 없음

- [x] **1-1** `~/.claude/hooks/` 폴더 생성
- [x] **1-2** `~/.claude/skills/chains/` 폴더 생성
- [x] **1-3** `~/.claude/workflow/templates/` 폴더 생성
- [x] **1-4** `npm install -g prettier` 설치 → 3.8.1
- [x] **1-5** `pip install black` 설치 → 26.3.1

### Phase 2: 독립 신규 파일 — 기존 파일 수정 없음, 병렬 가능

- [x] **2-1** `rules/lessons-learned.md` 신규 생성 (Tip #2 L1 캐시)
- [x] **2-2** `skills/chains/dev-chain.md` 업데이트 (Tip #5 검증루프 추가)
- [x] **2-3** `skills/chains/system-design.md` 업데이트 (Tip #5 검증루프 추가)
- [x] **2-4** `hooks/debug-residue-check.sh` 신규 생성 (Tip #7 Stop Hook)
- [x] **2-5** `hooks/plan-review-trigger.sh` 신규 생성 (Tip #3 독립검토)
- [x] **2-6** `workflow/templates/plan_template.md` 신규 생성 (Tip #3 Pre-Mortem §5)
- [x] **2-7** `workflow/templates/research_template.md` 신규 생성 (Tip #3 Pre-Mortem §6)

### Phase 3: 기존 파일 수정 — 한 파일당 한 번에 모든 변경 적용

- [x] **3-1** `rules/orchestration.md` 수정 (4개 변경 일괄)
  - §2.1에 "실수 기록 의무" 1줄 추가 (Tip #2)
  - §2.4에 검증 루프 프로토콜 섹션 추가 (Tip #5)
  - 체인 6개(A,B,C,D,G,J)에 `→ {검증 루프 × MAX 3}` 추가 (Tip #5)
  - §2.6에 Pre-Mortem Gate + 독립 검토 섹션 추가 (Tip #3)
- [x] **3-2** `rules/memory-protocol.md` 수정 (Tip #2)
  - §3.8 Step 2 다음에 Step 2-1 "실수 감지" 추가
- [x] **3-3** `agents/logic-reviewer.md` 수정 (Tip #3 확신도+한계선언)
- [x] **3-4** `agents/security-reviewer.md` 수정 (Tip #3 확신도+한계선언)
- [x] **3-5** `agents/edge-case-reviewer.md` 수정 (Tip #3 확신도+한계선언)

### Phase 4: settings.json — 마지막 (Hook 파일 존재 전제)

- [x] **4-1** `settings.json` Stop Hook 추가 (Tip #7)
- [x] **4-2** `settings.json` PostToolUse에 plan-review-trigger 추가 (Tip #3)
- [x] **4-3** PostToolUse black 경로 보정 (Windows bash PATH 이슈 → 절대경로 우선)

### Phase 5: Obsidian CLI 연동

- [x] **5-1** Obsidian CLI 활성화 확인 (앱 1.12.7, CLI 작동)
- [x] **5-2** Obsidian 인스톨러 업데이트 (v1.12.7 최신, 282MB 다운로드+설치)
- [x] **5-3** PATH 확인 + bash alias 등록 (`~/.bashrc`)
- [x] **5-4** Vault 에이전트 3개 CLI 전환 (doc-indexer, link-doctor, knowledge-mapper)
  - `backlinks`, `orphans`, `deadends`, `unresolved`, `files`, `folders`, `tags` 등
- [x] **5-5** Utility 에이전트 5개 CLI 전환 (meeting-note-wizard, project-dashboard, worklog-analyzer, memory-report-generator, session-memo-writer)
  - `search`, `read`, `create open`, `append`, `tasks`, `recents`, `wordcount` 등

### Phase 6: orchestration.md 보강 + 체인 스킬 보강

- [x] **6-1** orchestration.md 버전 갱신 (V5.0.0-WE → V5.2.0-WE)
- [x] **6-2** orchestration.md §2.6에 Plan 모드 전용 규칙 섹션 추가
- [x] **6-3** `skills/chains/dev-chain.md` Step 4에 Pre-Mortem + 독립 Agent spawn 명시
- [x] **6-4** `skills/chains/system-design.md` Step 4에 Pre-Mortem + 독립 Agent spawn 명시
- [x] **6-5** orchestration.md §2.6 `/plan-review` 스킬 + `plan-verifier` 에이전트 연동 재구성

### Phase 7: 시니어 검증 스킬 + 에이전트 신규 생성

- [x] **7-1** `agents/plan-verifier.md` 신규 생성 (10년차 시니어, permissionMode:plan, 문제점3개+필수)
- [x] **7-2** `skills/plan-review/SKILL.md` 신규 생성 (Mode A verify + Mode B full)
- [x] **7-3** `CLAUDE.md` Slash Commands에 `/plan-review` 추가
- [x] **7-4** `Component Catalog` 업데이트 (에이전트 +1, 스킬 +1 → 총 157개)
- [x] **7-5** `CHANGELOG.md` V5.2.0-WE 항목 추가

### Phase 8: 설계 결함 수정 — plan 저장 경로/파일명/Hook 필터

- [x] **8-1** `hooks/plan-review-trigger.sh` V2.0 — `.claude/plans/` 차단 필터 제거 (내장Plan은 파일명 ^plan 불일치로 자연 필터)
- [x] **8-2** `skills/plan-review/SKILL.md` — 저장 규칙 섹션 추가 (위치: `.claude/plans/`, 파일명: `plan_YYYYMMDD_HHMMSS_keyword.md`)
- [x] **8-3** `orchestration.md` Mode B 흐름도 — 저장 경로 `.claude/plans/plan_YYYYMMDD_HHMMSS_keyword.md` 명시
- [x] **8-4** 잘못 생성된 `workflow/plan.md` → `plans/plan_20260406_095600_system_review.md`로 이동
- [x] **8-5** L1 #1 기록 (플랜 생략 실수) + L1 #2 기록 (plan 저장 위치/파일명 실수)

### Phase 9: 실전 검증 — 신규 세션 Mode A 테스트

- [x] **9-1** 신규 세션에서 내장 Plan 모드 → hello-world.sh 계획 생성
- [x] **9-2** 승인 다이얼로그 옵션 4 → "검증해줘" 입력
- [x] **9-3** `plan-verifier` Agent spawn → 시니어 검증 실행 (1분, 48k tokens)
- [x] **9-4** 검증 결과: ⚠️ 수정 후 승인 (4/10), Critical 1건 + Warning 2건 + Info 2건
- [x] **9-5** Mode A (verify) 파이프라인 완전 작동 확인

### Phase 10: plan-verifier 팀에이전트 전환 — 편향 제거 강화

> Phase 9 테스트에서 plan-verifier가 서브에이전트(Agent 도구)로 실행됨 확인.
> 같은 세션 프로세스 공유 → 편향 제거 약화. TeamCreate로 전환하여 완전 독립 인스턴스 보장.

- [x] **10-1** `agents/plan-verifier.md` — "실행 방식" 섹션 추가: TeamCreate 필수, Agent 도구 사용 금지 명시
- [x] **10-2** `skills/plan-review/SKILL.md` — Mode A Step 3 + Mode B Step 4: 팀에이전트 spawn으로 변경
- [x] **10-3** `orchestration.md` §2.6 — 검증 에이전트 설명에 "TeamCreate 사용, 서브에이전트 금지" 추가

### Phase 11: Mode B 풀 워크플로우 실전 테스트 — PASS

> 신규 세션에서 `/plan-review full` 테스트. §2.6 정합성 분석 (중규모 작업).

- [x] **11-1** 신규 세션에서 `/plan-review full` + 중규모 요청 (§2.6 정합성 분석) 실행
- [x] **11-2** `.claude/plans/plan_20260406_103639_*.md` 저장 확인
- [x] **11-3** §5 Pre-Mortem 포함 확인
- [x] **11-4** plan-verifier **팀에이전트(TeamCreate)** spawn 확인 (`@plan-verifier>` 독립 메시지 통신)
- [x] **11-5** 시니어 검증 결과: ⚠️ 수정 후 승인 (7/10), Critical 2 + Warning 2 + Info 1
- [x] **11-6** Gate 2 승인 요청 → 앤 승인 → 5단계 수정 실행

### Phase 12: Mode B 시니어 지적 반영 수정 — 용어 통일 + 경로 확정

> Phase 11 시니어 검증에서 지적된 5건을 반영하여 시스템 파일 수정.

- [x] **12-1** 용어 통일: "Agent spawn" → "TeamCreate spawn" (orchestration.md 3곳, SKILL.md 1곳, L1 1곳)
- [x] **12-2** 포인터 삽입: orchestration.md 전반부 소섹션에 `→ 상세: 아래 참조` + `spawn 방식: TeamCreate 필수` 추가
- [x] **12-3** 경로 확정: research.md → `~/.claude/plans/research_YYYYMMDD_HHMMSS_keyword.md` (^research → Hook ^plan 불일치 → 오탐 없음)
- [x] **12-4** 주석 추가: SKILL.md `ls -t` 예시에 `# 실제 실행 시 Glob 도구 사용 권장`
- [x] **12-5** 메모리 저장: `2604_058_s26_integrity_analysis.md`

---

## 검증 결과

### V-1: Phase 1 인프라 검증

- [x] `~/.claude/hooks/` 폴더 존재 확인 ✅
- [x] `~/.claude/skills/chains/` 폴더 존재 확인 ✅
- [x] `~/.claude/workflow/templates/` 폴더 존재 확인 ✅
- [x] `prettier --version` → 3.8.1 ✅
- [x] `black --version` → 26.3.1 (절대경로) ✅

### V-2: Phase 2 신규 파일 검증

- [x] `rules/lessons-learned.md` 존재 + L1 캐시 테이블 포함 ✅
- [x] `skills/chains/dev-chain.md` 존재 + `검증 루프 × MAX 3` grep → 2건 ✅
- [x] `skills/chains/system-design.md` 존재 + `검증 루프 × MAX 3` grep → 2건 ✅
- [x] `hooks/debug-residue-check.sh` 존재 + bash 문법 OK ✅
- [x] `hooks/plan-review-trigger.sh` 존재 + bash 문법 OK ✅
- [x] `workflow/templates/plan_template.md` 존재 + §5 Pre-Mortem 포함 ✅
- [x] `workflow/templates/research_template.md` 존재 + §6 Pre-Mortem 포함 ✅

### V-3: Phase 3 수정 파일 검증

- [x] `orchestration.md`에서 `실수 기록 의무` grep → 1건 ✅
- [x] `orchestration.md`에서 `검증 루프 × MAX 3` grep → 7건 (프로토콜1 + 체인6) ✅
- [x] `orchestration.md`에서 `Pre-Mortem` grep → 3건+ ✅
- [x] `orchestration.md`에서 `plan-verifier` grep → 2건+ ✅
- [x] `memory-protocol.md`에서 `실수 감지` grep → 1건 ✅
- [x] `logic-reviewer.md`에서 `확신도` grep → 1건 ✅
- [x] `security-reviewer.md`에서 `확신도` grep → 1건 ✅
- [x] `edge-case-reviewer.md`에서 `확신도` grep → 1건 ✅

### V-4: Phase 4 settings.json 검증

- [x] `settings.json`에서 `Stop` 키 존재 확인 ✅
- [x] `settings.json`에서 `debug-residue-check` grep → 1건 ✅
- [x] `settings.json`에서 `plan-review-trigger` grep → 1건 ✅
- [x] JSON 문법 유효성 → valid ✅

### V-5: Phase 5 Obsidian CLI 검증

- [x] Obsidian CLI `--help` → `Obsidian CLI` 도움말 정상 출력 (경고 없음) ✅
- [x] 에이전트 8개에서 `Obsidian CLI` 또는 `OBSIDIAN=` grep → 8파일 ✅

### V-6: Phase 6 orchestration 보강 검증

- [x] `orchestration.md` 버전 → V5.2.0-WE ✅
- [x] `orchestration.md`에서 `Plan 모드 규칙` grep → 1건+ ✅
- [x] `dev-chain.md` Step 4에 `Pre-Mortem + 독립 검토` 포함 ✅
- [x] `system-design.md` Step 4에 `Pre-Mortem + 독립 검토` 포함 ✅

### V-7: Phase 7 시니어 검증 스킬 검증

- [x] `agents/plan-verifier.md` 존재 + `permissionMode: plan` + `시니어` 포함 ✅
- [x] `skills/plan-review/SKILL.md` 존재 + Mode A/B 포함 ✅
- [x] `CLAUDE.md` Slash Commands에 `/plan-review` 포함 ✅
- [x] `Component Catalog` 에이전트 34개 + 스킬 47개 = 157개 ✅

### V-8: Phase 8 설계 결함 수정 검증

- [x] Hook 오탐 필터에서 `.claude/plans/` 차단 제거 → 내장Plan은 파일명으로 자연 필터 ✅
- [x] `plan-review-trigger.sh` V2.0 문법 OK ✅
- [x] `SKILL.md`에 저장 규칙 섹션(위치+파일명+Hook 연동) 포함 ✅
- [x] `orchestration.md` Mode B 흐름도에 `plans/plan_YYYYMMDD_HHMMSS_keyword.md` 명시 ✅
- [x] `workflow/plan.md` 삭제 → `plans/plan_20260406_095600_system_review.md`로 이동 ✅
- [x] L1 #2 기록 완료 ✅

### V-9: Phase 9 실전 검증 (신규 세션)

- [x] 신규 세션에서 내장 Plan 모드 → plan 생성 → 승인 다이얼로그 표시 ✅
- [x] 옵션 4 "검증해줘" 입력 → `.claude/plans/` 최신 plan 자동 탐색 ✅
- [x] `plan-verifier` Agent spawn 성공 (5 tool uses, 48k tokens, 1분) ✅
- [x] 시니어 검증 결과 출력: 문제점 5개(Critical 1 + Warning 2 + Info 2) ✅
- [x] 확신도 4/10, 판정 ⚠️ 수정 후 승인 ✅
- [x] 검증 후 앤에게 판단 위임 (배치 위치, Hook 등록 확인) ✅
- [x] **Mode A (verify) 파이프라인 완전 작동 확인** ✅

### V-10: Phase 10 팀에이전트 전환 검증

- [x] `agents/plan-verifier.md`에 `TeamCreate 필수` + `Agent 도구 사용 금지` 명시 ✅
- [x] `skills/plan-review/SKILL.md` Mode A/B에 `TeamCreate` 명시 ✅
- [x] `orchestration.md`에 `TeamCreate 사용, 서브에이전트 금지` 명시 ✅

### V-11: Phase 11 Mode B 실전 검증

- [x] `/plan-review full` 실행 → `.claude/plans/plan_20260406_103639_*.md` 저장 ✅
- [x] Pre-Mortem §5 포함 ✅
- [x] **TeamCreate로 plan-verifier spawn** (`@plan-verifier>` 독립 메시지) ✅
- [x] 시니어 검증: ⚠️ 수정 후 승인 (7/10), Critical 2 + Warning 2 + Info 1 ✅
- [x] Gate 2 승인 → 5단계 수정 실행 ✅
- [x] **Mode B + TeamCreate 파이프라인 완전 작동 확인** ✅

### V-12: Phase 12 시니어 지적 반영 검증

- [x] 용어 통일 "TeamCreate spawn" — orchestration.md + SKILL.md + L1 ✅
- [x] research.md 경로 `~/.claude/plans/research_*` 확정 ✅
- [x] SKILL.md `ls -t` 예시에 Glob 권장 주석 추가 ✅
- [x] 메모리 `2604_058_s26_integrity_analysis.md` 저장 ✅

---

## 설치 후 시스템 상태 (최종)

| 구성요소 | 설치 전 | 설치 후 | 변화 |
|---------|--------|--------|------|
| `rules/` | 3파일 | **4파일** | +lessons-learned.md |
| `agents/` | 30개 | **31개** | +plan-verifier |
| `skills/` | 기존 | +**chains/ 2파일 업데이트** + **plan-review/ 신규** | +1 스킬 |
| `hooks/` | ❌ 없음 | **2파일** | +debug-residue-check, +plan-review-trigger |
| `workflow/templates/` | ❌ 없음 | **2파일** | +plan_template, +research_template |
| Hook 이벤트 | 3종 | **4종** | +Stop |
| Hook 수 | 5개 | **7개** | +2 |
| 패키지 | 없음 | prettier 3.8.1 + black 26.3.1 | +2 |
| Obsidian CLI | 경고 있음 | 경고 없음 + alias | 인스톨러 업데이트 |
| 총 컴포넌트 | 151개 | **157개** | +6 |
| 시스템 버전 | V5.1.1-WE | **V5.2.0-WE** | 버전업 |

---

## 관련 문서

### 직접 참조 (Direct Links)
- `02_tip2_tip5_implementation_guide.md` — Tip #2+#5 상세 가이드
- `03_tip7_hook_automation_guide.md` — Tip #7 상세 가이드
- `06_tip3_plan_mode_implementation.md` — Tip #3 상세 가이드
- `04_02_v510_bias_deep_analysis.md` — 편향 분석 (확신도/한계선언 근거)
- `~/.claude/agents/plan-verifier.md` — 시니어 검증 에이전트
- `~/.claude/skills/plan-review/SKILL.md` — 시니어 검증 스킬

### 역참조 (Backlinks)
- `01_claude_code_7_best_practices.md` — Boris 원본 7팁

---

## Release Notes

### v5.0.0 (2026-04-06)
- Phase 11 완료: Mode B + TeamCreate 실전 검증 PASS (7/10, 5건 지적→승인→수정 실행)
- Phase 12 추가: 시니어 지적 5건 반영 (용어 통일, 포인터, 경로 확정, 주석)
- V-11~V-12 검증 PASS (전체 V-1~V-12 ALL PASS)
> **프롬프트:** "저 세션 결과에 따라 07 문서 업데이트 해줘"

### v4.0.0 (2026-04-06)
- Phase 10 추가: plan-verifier 서브에이전트→팀에이전트(TeamCreate) 전환
- Phase 11 계획 수립
- V-10 PASS
> **프롬프트:** "07 문서 업데이트 해줘"

### v3.0.0 (2026-04-06)
- Phase 8 추가: plan 저장 경로/파일명/Hook 필터 설계 결함 수정
- Phase 9 추가: 신규 세션 Mode A 실전 검증 PASS
- V-8~V-9 ALL PASS, L1 #1~#2 기록
> **프롬프트:** "07 문서에 내용을 업데이트 해줘"

### v2.0.0 (2026-04-06)
- Phase 5~7 추가: Obsidian CLI + orchestration 보강 + 시니어 검증 스킬
- V-1~V-7 검증 체크박스 전체 PASS 확인
- 설치 후 시스템 상태 테이블 추가
> **프롬프트:** "07 문서에 신규 작업 내용도 기입해서 문서 수정해주고 검증도 체크박스가 없던데 이것도 확인해줘"

### v1.0.0 (2026-04-06)
- Windows 설치 계획 + 검증 계획 작성
- Phase 1~4 설치 완료 + 14/14 PASS
- 설치 순서: 의존성 기반 재배치
> **프롬프트:** "07번 문서로 분석결과 작업계획 검증계획 작성해서 해당 문서대로 진행해줘 설치순서는 순번을 무시하고 효율적이고 충돌이 적게 나는것으로 재 배치해줘"
