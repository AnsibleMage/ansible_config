# MetaThinkChain 완벽 실행 프롬프트

> **목적**: Claude Code 시스템 개선을 위한 메타 사고 체인 완벽 구동
> **작성일**: 2026-02-04
> **체인**: MetaThinkChain (심층 분석 + 의사결정 + 학습 통합)

---

## MetaThinkChain 구조

```
Phase 1 (병렬): insight_explorer[S] ∥ connection_creator[S]
     ↓
Phase 2 (병렬): multidimensional_analyst[O] ∥ learning_evolver[S]
     ↓
Phase 3 (선택): balanced_judge[O] | problem_reframer[O]
     ↓
Phase 4 (통합): integrated_sage[O]
```

---

## 🚀 Claude Code 세션 시작용 프롬프트

```
📋 체인 구성: MetaThinkChain

## 주제
Claude Code 시스템의 다음 진화 단계 설계

## 분석 대상
~/.claude/ 폴더 전체 (CLAUDE.md, hooks, scripts, memory, settings.json)

## 실행 지시

### Phase 1: 병렬 탐색 (insight_explorer ∥ connection_creator)

**[Task 1-A] insight_explorer (sonnet)**
- ~/.claude/ 전체 구조 탐색
- 현재 시스템의 강점/약점 패턴 발견
- 숨겨진 개선 기회 탐지
- 출력: "현재 시스템 인사이트 리포트"

**[Task 1-B] connection_creator (sonnet)** (병렬 실행)
- 체인 시스템 ↔ 메모리 시스템 ↔ Hook 시스템 간 연결점 분석
- 외부 도구(Cowork, LaunchAgent)와의 통합 가능성
- 다른 AI 시스템(Gemini, GPT)의 좋은 패턴 연결
- 출력: "시스템 연결 맵 및 통합 기회"

### Phase 2: 병렬 심층 분석 (multidimensional_analyst ∥ learning_evolver)

**[Task 2-A] multidimensional_analyst (opus)**
- Phase 1 결과를 다차원으로 분석
- 기술적 차원: 구현 가능성, 복잡도
- 가치 차원: 생산성 향상, 사용자 경험
- 시간 차원: 단기 vs 장기 효과
- 리스크 차원: 실패 가능성, 부작용
- 출력: "다차원 분석 매트릭스"

**[Task 2-B] learning_evolver (sonnet)** (병렬 실행)
- ~/.claude/memory/ 22개 파일에서 학습 패턴 추출
- 반복되는 문제/해결책 패턴
- 앤(An)의 작업 스타일 진화 방향
- 출력: "학습 기반 진화 방향 제안"

### Phase 3: 의사결정 (balanced_judge 또는 problem_reframer)

**[Task 3] balanced_judge (opus)**
- Phase 2 결과를 종합하여 최적 개선안 선정
- 장단점 균형 평가
- 우선순위 결정
- 출력: "우선순위화된 개선안 Top 5"

**또는** 문제 재정의가 필요한 경우:

**[Task 3-Alt] problem_reframer (opus)**
- 근본적인 질문 재정의
- "시스템 개선"의 의미 재해석
- 출력: "재정의된 문제와 새로운 접근법"

### Phase 4: 통합 지혜 (integrated_sage)

**[Task 4] integrated_sage (opus)**
- 모든 Phase 결과 통합
- 실행 가능한 로드맵 생성
- 즉시 실행 가능한 첫 번째 액션 명시
- 출력: "Claude Code 시스템 진화 마스터플랜"

## 출력 형식

각 Phase 완료 후:
```
✅ Phase N 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[결과 요약]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

최종 출력:
```
🎯 MetaThinkChain 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## 마스터플랜
[통합된 진화 계획]

## 즉시 실행 액션
[첫 번째 구체적 액션]

## 메모리 저장
[세션 결과를 ~/.claude/memory/에 저장]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

실행하라, 아리.
```

---

## 📋 간소화 버전 (복사용)

```
📋 체인 구성: MetaThinkChain
주제: Claude Code 시스템 진화

Phase 1 (병렬):
- insight_explorer[S]: ~/.claude/ 탐색 → 개선 기회 발견
- connection_creator[S]: 시스템 간 연결점 및 통합 기회

Phase 2 (병렬):
- multidimensional_analyst[O]: 다차원 분석 (기술/가치/시간/리스크)
- learning_evolver[S]: memory 22개에서 학습 패턴 추출

Phase 3:
- balanced_judge[O]: 우선순위화된 개선안 Top 5

Phase 4:
- integrated_sage[O]: 마스터플랜 + 즉시 실행 액션

~/.claude/memory/에 결과 저장하라.
```

---

## 🔥 원라이너 버전 (즉시 실행)

```
📋 체인: MetaThinkChain | 주제: Claude Code 시스템 진화 | (insight_explorer[S] ∥ connection_creator[S]) → (multidimensional_analyst[O] ∥ learning_evolver[S]) → balanced_judge[O] → integrated_sage[O] | ~/.claude/ 전체 분석 후 진화 마스터플랜 생성하고 메모리 저장하라
```

---

## 🎯 특정 분야별 변형 프롬프트

### A. Hook 시스템 진화

```
📋 체인 구성: MetaThinkChain
주제: Hook 시스템의 다음 진화 단계

분석 대상: ~/.claude/hooks/, ~/.claude/settings.json의 hooks 섹션
목표: UserPromptSubmit, PreToolUse, PostToolUse Hook의 최적 조합 설계

Phase 1~4 실행 후 Hook 시스템 진화 마스터플랜 생성하라.
```

### B. 메모리 시스템 진화

```
📋 체인 구성: MetaThinkChain
주제: Memory 시스템의 지능화

분석 대상: ~/.claude/memory/ 전체, 메모리 저장 규칙
목표: 자동 분류, 자동 연결, 자동 요약 시스템 설계

Phase 1~4 실행 후 지능형 메모리 시스템 설계하라.
```

### C. 체인 시스템 자체 진화

```
📋 체인 구성: MetaThinkChain
주제: Dynamic Chain Patterns V3.0 설계

분석 대상: CLAUDE.md의 체인 섹션, ~/.claude/chainreport/ 사용 패턴
목표: 자가 학습하는 체인 시스템 설계

Phase 1~4 실행 후 V3.0 체인 시스템 설계하라.
```

---

## 실행 시 기대 효과

```
┌─────────────────────────────────────────────────────────────┐
│  MetaThinkChain 실행 효과                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1 (병렬)                                              │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ insight     │  │ connection  │  → 약 2-3분              │
│  │ _explorer   │  │ _creator    │                          │
│  └─────────────┘  └─────────────┘                          │
│         ↓                                                   │
│  Phase 2 (병렬)                                              │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │ multi       │  │ learning    │  → 약 3-5분              │
│  │ dimensional │  │ _evolver    │                          │
│  └─────────────┘  └─────────────┘                          │
│         ↓                                                   │
│  Phase 3                                                    │
│  ┌─────────────────────────────┐                           │
│  │ balanced_judge              │  → 약 2-3분               │
│  └─────────────────────────────┘                           │
│         ↓                                                   │
│  Phase 4                                                    │
│  ┌─────────────────────────────┐                           │
│  │ integrated_sage             │  → 약 3-5분               │
│  └─────────────────────────────┘                           │
│         ↓                                                   │
│  📄 마스터플랜 + 메모리 저장                                  │
│                                                             │
│  총 예상 시간: 10-15분                                       │
│  Opus 호출: 4회, Sonnet 호출: 4회                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 관련 문서

- [[002_Chain_System_V2.0_for_CLAUDE]]
- [[005_Cowork_External_Observer_System]]
- [[006_Chain_Usage_Report_System]]
