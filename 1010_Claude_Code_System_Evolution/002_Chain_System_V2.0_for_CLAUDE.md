## 🔗 Dynamic Chain Patterns V2.0 (10)

> **Notation**: [O] = opus, [S] = sonnet, [-] = main session
> **Pattern**: → = 순차, ∥ = 병렬, ⟳ = 반복

### 🆕 A. SystemDesignChain (시스템 설계)
```
(Explore[S] ∥ Read[-]) → (system_architect[O] ∥ problem_reframer[O])
→ integrated_sage[O] → (Edit[-] ∥ quality_reviewer[S])
```
> **Use Case**: CLAUDE.md 업데이트, 체인 개선, 아키텍처 설계
> **트리거**: "시스템 설계", "아키텍처", "V*.* 업데이트", "체인 개선"

### 🆕 B. AutomationChain (자동화 개발)
```
requirements_analyst[O] → (WebSearch[∥] ∥ Context7[∥])
→ code_developer[S] → (Bash[-] ∥ quality_reviewer[S])
```
> **Use Case**: Hook, MCP, 커스텀 커맨드, 스크립트 개발
> **트리거**: "Hook", "MCP", "자동화", "스크립트", "커맨드"

### 🆕 C. GameDevChain (게임 개발)
```
requirements_analyst[O] →
( (system_architect[O] → code_developer[S])[Roblox] ∥
  (system_architect[O] → /frontend-design[-])[Web] ) →
quality_reviewer[S]
```
> **Use Case**: Roblox + Web 듀얼 트랙 게임 개발
> **트리거**: "Roblox", "게임", "Lua", "Three.js", "WebGL"

### ✅ D. DevChain (개발)
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S] ∥ Context7[∥])
→ code_developer[S] → (quality_reviewer[S] ∥ Bash[테스트][-])
```
> **Use Case**: 일반 소프트웨어 개발
> **트리거**: "개발", "구현", "코드", "TDD"

### ✅ E. ResearchChain (연구)
```
(WebSearch[∥] ∥ Context7[∥] ∥ Explore[S]) →
(multidimensional_analyst[O] ∥ insight_explorer[S]) →
integrated_sage[O] → Write[-] | /docx[-]
```
> **Use Case**: 기술 분석, 적합성 조사, 트렌드 연구
> **트리거**: "조사", "research", "트렌드", "비교 분석"

### ✅ F. DocChain+ (문서)
```
[Solo]   requirements_analyst[O] → /docx|/pdf|/pptx|/xlsx[-] → quality_reviewer[S]
[Collab] /doc-coauthoring[-] → /docx|/pdf|/pptx[-] → quality_reviewer[S]
```
> **Use Case**: 문서 생성 (단독/협업 모드)
> **트리거**: "Word", "PDF", "PPT", "보고서", "협업 문서"

### ✅ G. WebDevChain+ (웹 개발)
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[S] ∥ /brand-guidelines[-])
→ (/theme-factory[-] → /frontend-design[-]) → /webapp-testing[-]
→ quality_reviewer[S]
```
> **Use Case**: 웹 애플리케이션 개발 (디자인 포함)
> **트리거**: "웹", "React", "프론트엔드", "UI/UX"

### 🔄 H. MetaThinkChain (메타 사고)
```
(insight_explorer[S] ∥ connection_creator[S]) →
(multidimensional_analyst[O] ∥ learning_evolver[S]) →
balanced_judge[O] | problem_reframer[O] → integrated_sage[O]
```
> **Use Case**: 심층 분석, 의사결정, 학습
> **트리거**: "심층 분석", "의사결정", "학습", "Why", "What-If"

### 🔄 I. RailsDevChain (Rails 8)
```
/rails-prd[-] → /rails-plan[-] → (/rails-dev[-] → /rails-test[-]) × N
→ /rails-deploy[-] → /rails-verify[-]
```
> **Use Case**: Rails 8 바이브코딩 풀 사이클
> **트리거**: "Rails", "레일즈", "Kamal", "바이브코딩"

### ⚡ J. HotfixChain (긴급 수정)
```
(complexity_resolver[O] ∥ Explore[S] ∥ Grep[-]) → code_developer[S]
→ (Bash[테스트][-] ∥ quality_reviewer[S])
```
> **Use Case**: 긴급 버그 수정, 핫픽스
> **트리거**: "급한", "즉시", "당장", "버그", "핫픽스", "긴급"

---

### Chain Selection Priority

```
사용자 프롬프트 분석
        ↓
┌─────────────────────────────────────┐
│ 1. 트리거 키워드 매칭               │
│    → 매칭 시 해당 체인 자동 선택     │
└─────────────────────────────────────┘
        ↓ 미매칭
┌─────────────────────────────────────┐
│ 2. 작업 유형 추론                   │
│    시스템 → SystemDesignChain       │
│    자동화 → AutomationChain         │
│    게임   → GameDevChain            │
│    개발   → DevChain                │
│    조사   → ResearchChain           │
│    문서   → DocChain+               │
│    웹     → WebDevChain+            │
│    사고   → MetaThinkChain          │
│    Rails  → RailsDevChain           │
│    긴급   → HotfixChain             │
└─────────────────────────────────────┘
        ↓ 미매칭
┌─────────────────────────────────────┐
│ 3. Dynamic Chain 동적 생성          │
│    Agent + Skill 조합               │
└─────────────────────────────────────┘
```

---

### V2.0 변경 요약

| 구분 | 기존 V1.0 | 신규 V2.0 |
|------|----------|----------|
| **총 체인** | 11개 | 10개 |
| **신규 추가** | - | SystemDesignChain, AutomationChain, GameDevChain |
| **강화** | - | DevChain, ResearchChain, DocChain+, WebDevChain+ |
| **통합** | ThinkChain, LearnChain, DecisionChain | → MetaThinkChain |
| **통합** | DesignChain | → WebDevChain+ |
| **통합** | CollabChain | → DocChain+ |
| **리네이밍** | FastTrack | → HotfixChain |
| **미사용 제거** | 6개 미사용 | 0개 |
