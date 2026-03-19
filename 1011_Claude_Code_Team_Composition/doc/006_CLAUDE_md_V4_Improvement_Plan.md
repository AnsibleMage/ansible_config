# CLAUDE.md V4.0 개선 작업 계획서

> 작성일: 2026-02-06 | 수정일: 2026-02-06
> 작성: Ari (Claude Code) | 승인: An (Ansible)
> 목적: CLAUDE.md 시스템의 **정확한 작동**을 위한 개선 (경량화 아닌 정밀화)
> 상태: **✅ 앤 승인 완료 — Phase A부터 순차 진행**

---

## 앤의 결정사항 (확정)

| # | 항목 | 결정 |
|---|------|------|
| 1 | Phase 순서 | **A → B → C** |
| 2 | Change History | **옵션 A**: 최근 3개 유지, 나머지 `~/.claude/CHANGELOG.md` 아카이브 |
| 3 | Rails 8 섹션 | **옵션 B**: `~/.claude/RAILS.md` 분리 + "레일즈/RAILS" 감지 시 자동 연관 읽기 |
| 4 | 구버전 CLAUDE.md | **유지** (아카이빙 용도) |

---

## 현재 상태 진단

### 발견된 문제 (심각도순)

| # | 문제 | 심각도 | 영향 |
|---|------|--------|------|
| 1 | prompt_analyzer.py 체인 동기화 불일치 (30%만 정확) | CRITICAL | 체인 추천 70% 실패 |
| 2 | 키워드 오탐 (버전→번역, 문서→docx, 계획→Plan) | CRITICAL | 매 프롬프트마다 잘못된 추천 |
| 3 | 가장 많이 쓰는 체인 2개 미등록 (SystemDesign, Automation) | CRITICAL | 핵심 작업 체인 매칭 불가 |
| 4 | CLAUDE.md 정보 중복 (같은 에이전트가 3곳에 등장) | MEDIUM | 불일치 위험 |
| 5 | Change History 110줄 (실행에 불필요) | LOW | 컨텍스트 낭비 |
| 6 | settings.json 내용 재문서화 (이중 관리) | LOW | 불일치 위험 |

---

## Phase A: prompt_analyzer.py V3.0 업그레이드

> **목표**: 체인 동기화 100% + 오탐률 40% → 15% 이하

### Step A-1: 체인 동기화 수정 (CRITICAL)

- [x] A-1-1. 백업 생성 (`prompt_analyzer.py.v21.backup`)
- [x] A-1-2. 3개 누락 체인 추가 (SystemDesignChain, AutomationChain, GameDevChain)
- [x] A-1-3. 4개 구명칭 변경 (DocChain→DocChain+, WebDevChain→WebDevChain+, ThinkChain/LearnChain/DecisionChain→MetaThinkChain, FastTrack→HotfixChain)
- [x] A-1-4. 2개 폐기 체인 삭제 (DesignChain, CollabChain)
- [x] A-1-5. fallback 로직 수정 (라인 524,529: ThinkChain→MetaThinkChain, FastTrack→HotfixChain)
- [x] A-1-6. 주석 업데이트 (A~K → A~J, V2.1 → V3.0)

### Step A-2: 키워드 오탐 방지 시스템 (CRITICAL)

- [x] A-2-1. 컨텍스트 윈도우 분석 함수 구현 (`get_context_window()`)
- [x] A-2-2. 번역 키워드 오탐 수정 ("버전" → 주변 언어명 확인 필수) + lang_patterns 확장
- [x] A-2-3. 문서 키워드 오탐 수정 ("문서" → 동사 분석: 보여줘 vs 만들어)
- [x] A-2-4. 명시적 제약 감지 추가 ("작업하지 말고", "분석만", "먼저 보여줘")
- [x] A-2-5. 메타 작업 자동 감지 추가 (CLAUDE.md, Hook, 체인 → SystemDesignChain 우선)
- [x] A-2-6. 상호 배제 규칙 추가 (번역↔문서 배제, 제약→구현 억제)

### Step A-3: 추천 품질 개선

- [x] A-3-1. 신뢰도 점수 도입 (0.0~1.0): 화용=0.95, 메타=0.85, 키워드=0.7, fallback=0.5
- [x] A-3-2. 0.6 미만 추천 필터링
- [x] A-3-3. 최대 3개 추천 제한 (신뢰도 순 정렬)
- [x] A-3-4. 출력 포맷 개선 (신뢰도 % 표시, 제약/필터링 표시)

---

## Phase B: CLAUDE.md V4.0 구조 재설계

> **목표**: 중복 제거 + 실행 정확성 강화

### Step B-1: 사전 준비

- [x] B-1-1. CLAUDE.md V3.9 백업 (`CLAUDE.md.v39.backup`)
- [x] B-1-2. Change History V2.0~V3.7을 `~/.claude/CHANGELOG.md`로 아카이브
- [x] B-1-3. Rails 8 섹션을 `~/.claude/RAILS.md`로 분리
- [x] B-1-4. CLAUDE.md에 Rails 자동 연관 읽기 지시 추가 (RailsDevChain 섹션에 포함)

### Step B-2: V4.0 구조 작성

- [x] B-2-1. 섹션 1: Identity & Principles (기존 1+3 통합)
- [x] B-2-2. 섹션 2: Orchestration System (기존 2+5+6+7 통합)
  - [x] B-2-2a. Hook 분석 흐름 (V3.0 신규 기능 포함)
  - [x] B-2-2b. 통합 매핑 테이블 (Agent 16개 + Skill 16개 + Explore 3개)
  - [x] B-2-2c. Chain Patterns (A~J 10개)
  - [x] B-2-2d. Chain ↔ Teams 선택 기준 + 전환 적합도
- [x] B-2-3. 섹션 3: Memory & Protocol (기존 10+11 통합)
- [x] B-2-4. 섹션 4: Settings Reference (8줄 테이블)
- [x] B-2-5. 섹션 5: Repository & Review (기존 12+13 통합)
- [x] B-2-6. 섹션 6: Change History (V4.0, V3.9, V3.8)

### Step B-3: V4.0 검증

- [x] B-3-1. 통합 매핑 테이블 ↔ prompt_analyzer V3.0 키워드 교차 대조
- [x] B-3-2. 에이전트 누락 확인 (V3.9의 모든 에이전트가 V4.0에 존재)
- [x] B-3-3. Chain Patterns 정확성 확인 (10개 전체)

---

## Phase C: 검증 테스트

> **목표**: 개선 후 시스템이 정확하게 작동하는지 실증 확인

### Step C-1: prompt_analyzer 테스트 (20건)

**오탐 방지 (5건)**:

- [x] C-1-1. "CLAUDE.md 최적화해줘" → SystemDesignChain (NOT /translation-specialist)
- [x] C-1-2. "문서로 보여줘" → 텍스트 출력 (NOT /docx)
- [x] C-1-3. "라이트 버전으로 만들어" → SystemDesignChain (NOT /translation-specialist)
- [x] C-1-4. "작업하지 말고 계획만" → system_architect (NOT code_developer)
- [x] C-1-5. "이전 버전 복구해줘" → 수정 작업 (NOT /translation-specialist)

**정탐 확인 (10건)**:

- [x] C-1-6. "영어 버전으로 번역해줘" → /translation-specialist
- [x] C-1-7. "Word 문서 만들어줘" → /docx
- [x] C-1-8. "Hook 자동화 개발해줘" → AutomationChain
- [x] C-1-9. "Roblox 게임 만들어줘" → GameDevChain
- [x] C-1-10. "급한 버그 수정해줘" → HotfixChain
- [x] C-1-11. "심층 분석해줘" → MetaThinkChain
- [x] C-1-12. "Rails 앱 개발해줘" → RailsDevChain
- [x] C-1-13. "Solid Queue 조사해줘" → ResearchChain
- [x] C-1-14. "React 웹앱 만들어줘" → WebDevChain+
- [x] C-1-15. "PRD 작성해줘" → /rails-prd or DocChain+

**체인 동기화 (5건)**:

- [x] C-1-16. "CLAUDE.md 아키텍처 설계" → SystemDesignChain
- [x] C-1-17. "MCP 서버 자동화 개발" → AutomationChain
- [x] C-1-18. "Three.js 게임 개발" → GameDevChain
- [x] C-1-19. "API 개발해줘" → DevChain
- [x] C-1-20. "PDF 보고서 만들어줘" → DocChain+

### Step C-2: CLAUDE.md 통합 매핑 검증

- [x] C-2-1. 매핑 테이블 ↔ prompt_analyzer 1:1 대응 확인
- [x] C-2-2. 체인 내 에이전트 호출 순서 일치 확인

### Step C-3: 엔드투엔드 실동작 테스트

- [x] C-3-1. 실제 프롬프트 5개로 Hook → Chain → Agent 전체 흐름 확인
- [x] C-3-2. 메모리 저장 정상 작동 확인
- [x] C-3-3. 최종 결과 리포트 작성

---

## 위험 관리

| 위험 | 대응 |
|------|------|
| 매핑 테이블 통합 시 누락 | 현재 3곳 교차 대조 후 통합 |
| analyzer 수정 시 기존 정탐 깨짐 | 회귀 테스트 15건으로 검증 |
| CLAUDE.md 재작성 시 행동 변화 | V3.9 백업, 문제 시 롤백 |

**롤백 계획**:
```
CLAUDE.md V3.9 → ~/.claude/CLAUDE.md.v39.backup
prompt_analyzer.py V2.1 → ~/.claude/scripts/prompt_analyzer.py.v21.backup
```

---

## 최종 비교: V3.9 vs V4.0

| 항목 | V3.9 (현재) | V4.0 (목표) |
|------|------------|------------|
| 줄 수 | 924줄 | ~490줄 |
| 에이전트 매핑 | 3곳 분산 | **1곳 통합** |
| 체인 동기화 | 30% | **100%** |
| 오탐률 | ~40% | **<15%** |
| settings.json 중복 | 120줄 | 15줄 |
| Change History | 110줄 | 30줄 |
| Rails 8 | CLAUDE.md 내 80줄 | 별도 RAILS.md + 자동 연관 |
| 정확성 보장 | 없음 | 테스트 20건 |

---

## 진행 상황 요약 (실시간 업데이트)

```
Phase A-1 (체인 동기화):  ████████████████████ 100% (6/6) ✅
Phase A-2 (오탐 방지):    ████████████████████ 100% (6/6) ✅
Phase A-3 (품질 개선):    ████████████████████ 100% (4/4) ✅
Phase B-1 (사전 준비):    ████████████████████ 100% (4/4) ✅
Phase B-2 (V4.0 작성):    ████████████████████ 100% (9/9) ✅
Phase B-3 (V4.0 검증):    ████████████████████ 100% (3/3) ✅
Phase C-1 (테스트 20건):   ████████████████████ 100% (20/20) ✅
Phase C-2 (매핑 검증):    ████████████████████ 100% (2/2) ✅
Phase C-3 (실동작 테스트): ████████████████████ 100% (3/3) ✅
─────────────────────────────────────────────────
전체:                     ████████████████████ 100% (57/57) ✅
```

---

*CLAUDE.md V4.0 개선 작업 계획서 | 2026-02-06*
*Prepared by Ari (Aria) | Approved by An (Ansible)*
