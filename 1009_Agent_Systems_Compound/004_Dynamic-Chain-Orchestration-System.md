# 동적 체인 오케스트레이션 시스템

> 문서 버전: 1.0 | 작성일: 2026-02-01
> 적용 대상: CLAUDE.md V2.2
> 위계: PRIORITY 1 (최우선 실행)

---

## 📋 개요

동적 체인 오케스트레이션은 사용자 프롬프트를 언어학적으로 분석하여 최적의 작업 흐름(체인)을 자동으로 선택하거나 생성하는 시스템입니다.

### 핵심 특징

| 특징 | 설명 |
|------|------|
| **자동 분석** | 4-Layer 언어학적 프롬프트 분석 |
| **이중 전략** | 기존 체인 선택 + 동적 체인 생성 |
| **혼합 체인** | 에이전트와 스킬 조합 가능 |
| **모델 최적화** | 단계별 opus/sonnet 자동 지정 |

---

## 🔬 4-Layer 프롬프트 분석

translation-specialist 스킬의 언어학적 분석 기법을 차용합니다.

### 분석 레이어

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 어휘 분석 (Lexical)                               │
│  ─────────────────────────────────────────────────────────  │
│  • 키워드 추출                                              │
│  • 전문 용어 식별                                           │
│  • 도메인 판별 (개발/분석/디자인/문서 등)                    │
│  • 출력: 관련 에이전트/스킬 후보 목록                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: 통사 분석 (Syntactic)                             │
│  ─────────────────────────────────────────────────────────  │
│  • 문장 구조 파악                                           │
│  • 명령/질문/요청 유형 분류                                 │
│  • 동사 분석 (만들다/분석하다/수정하다 등)                   │
│  • 출력: 작업 유형 및 순서                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: 담화 분석 (Discourse)                             │
│  ─────────────────────────────────────────────────────────  │
│  • 이전 대화 맥락 참조                                      │
│  • 배경 정보 이해                                           │
│  • 암묵적 전제 파악                                         │
│  • 출력: 체인 복잡도 판단 (Simple/Medium/Complex)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: 화용 분석 (Pragmatic)                             │
│  ─────────────────────────────────────────────────────────  │
│  • 실제 의도 파악                                           │
│  • 기대 결과물 형태 예측                                    │
│  • 암묵적 요구사항 추론                                     │
│  • 출력: 최종 산출물 정의                                   │
└─────────────────────────────────────────────────────────────┘
```

### 분석 예시

**프롬프트**: "이 API가 느린데 원인 찾아서 고쳐줘"

| Layer | 분석 | 결과 |
|-------|------|------|
| 어휘 | API, 느린, 원인, 고쳐 | 성능, 디버깅, 수정 |
| 통사 | 찾다 → 고치다 (순차) | 분석 후 수정 작업 |
| 담화 | 긴급한 톤, 문제 해결 맥락 | FastTrack 적합 |
| 화용 | 빠른 해결 원함 | 수정된 코드 + 설명 |

---

## 🔄 체인 선택/생성 프로세스

### 전체 흐름

```
사용자 프롬프트 수신
        ↓
┌───────────────────────┐
│  4-Layer 분석 실행    │
└───────────────────────┘
        ↓
┌───────────────────────┐
│  복잡도 판단          │
│  Simple → 직접 처리   │
│  Medium/Complex → ↓   │
└───────────────────────┘
        ↓
┌───────────────────────────────────────────┐
│  1차: 기존 체인 매칭                       │
│  ─────────────────────────────────────────│
│  9개 체인과 비교:                          │
│  A. DevChain      F. DocChain             │
│  B. ThinkChain    G. DesignChain          │
│  C. FastTrack     H. WebDevChain          │
│  D. LearnChain    I. CollabChain          │
│  E. DecisionChain                         │
│                                           │
│  매칭률 80% 이상 → 해당 체인 실행         │
└───────────────────────────────────────────┘
        ↓ 매칭 실패 또는 부분 매칭
┌───────────────────────────────────────────┐
│  2차: 동적 체인 생성                       │
│  ─────────────────────────────────────────│
│  1. 에이전트 풀에서 필요한 것 선별        │
│  2. 스킬 풀에서 필요한 것 선별            │
│  3. 순차/병렬/혼합 패턴 결정              │
│  4. 각 단계에 모델(opus/sonnet) 지정      │
│  5. 커스텀 체인 구성                       │
└───────────────────────────────────────────┘
        ↓
┌───────────────────────┐
│  체인 구성 선언       │
│  (사용자에게 공개)    │
└───────────────────────┘
        ↓
┌───────────────────────┐
│  체인 실행            │
└───────────────────────┘
```

---

## 🔗 에이전트 + 스킬 혼합 체인

### 호출 방식 차이

| 유형 | 호출 도구 | 모델 지정 | 표기 |
|------|----------|----------|------|
| 에이전트 | `Task(model: "opus")` | ✅ 가능 | `[O]` 또는 `[S]` |
| 스킬 | `Skill()` | ❌ 메인 세션 | `[-]` |

### 혼합 체인 예시

**프롬프트**: "브랜드 가이드라인 적용해서 대시보드 만들고 품질 검토해줘"

```
/brand-guidelines[-] → system_architect[O] → /web-artifacts-builder[-] → quality_reviewer[S]
      스킬                 에이전트                  스킬                    에이전트
```

### 실행 패턴

| 패턴 | 기호 | 조건 | 예시 |
|------|------|------|------|
| Sequential | → | 다음 단계가 이전 결과 필요 | A → B → C |
| Parallel | ∥ | 독립적 작업 | A ∥ B ∥ C |
| Hybrid | (A∥B)→C | 복합 의존성 | (분석∥조사) → 종합 |

---

## 📊 모델 자동 지정

### 에이전트별 모델 매핑

#### Opus 할당 (9개) - 복잡한 추론/설계/판단
```
multidimensional_analyst, problem_reframer, solution_innovator,
complexity_resolver, balanced_judge, integrated_sage,
requirements_analyst, system_architect, Plan
```

#### Sonnet 할당 (14개) - 일반 구현/탐색/검토
```
insight_explorer, connection_creator, insight_amplifier,
learning_evolver, code_developer, quality_reviewer,
quality_manager, context_manager, Explore, general-purpose,
link-doctor, doc-indexer, knowledge-mapper, 기타 Obsidian 에이전트
```

### 스킬 모델
- 모든 스킬은 메인 세션 모델 사용 `[-]`
- `/docx`, `/pdf`, `/frontend-design` 등

---

## 📢 실행 전 선언

체인 실행 전 사용자에게 구성을 공개합니다:

### 기존 체인 선택 시
```
📋 체인 구성: DevChain
   → requirements_analyst[O] → system_architect[O] → code_developer[S] → quality_reviewer[S]
```

### 동적 체인 생성 시
```
📋 체인 구성: 동적 생성
   → complexity_resolver[O] → multidimensional_analyst[O] → /docx[-]
```

---

## ⚡ 단순 작업 예외

다음 경우 체인 오케스트레이션 생략:

| 상황 | 처리 |
|------|------|
| 단순 질문/답변 | 직접 응답 |
| 한 줄 코드 수정 | 직접 수정 |
| 파일 읽기/검색만 필요 | 도구 직접 사용 |
| "간단히" 명시적 요청 | 최소 처리 |

---

## 🎯 동적 생성 예시 모음

### 예시 1: 레거시 마이그레이션

**프롬프트**: "레거시 코드 분석해서 마이크로서비스로 분해하고 API 문서 만들어줘"

**분석**:
- 기존 체인: 부분 매칭 (DevChain + DocChain)
- 동적 생성 필요

**생성 체인**:
```
complexity_resolver[O] → multidimensional_analyst[O] → system_architect[O] → /docx[-]
```

### 예시 2: 디자인 + 개발 통합

**프롬프트**: "Anthropic 브랜드로 랜딩 페이지 만들고 테스트해줘"

**생성 체인**:
```
/brand-guidelines[-] → /frontend-design[-] → /webapp-testing[-] → quality_reviewer[S]
```

### 예시 3: 연구 + 문서화

**프롬프트**: "이 기술 스택 장단점 분석하고 팀에 공유할 프레젠테이션 만들어줘"

**생성 체인**:
```
learning_evolver[S] → (multidimensional_analyst[O] ∥ connection_creator[S]) → integrated_sage[O] → /pptx[-]
```

---

## 📐 위계 구조

```
PRIORITY 1: 동적 체인 오케스트레이션 (본 시스템)
    ↓
PRIORITY 2: Core Working Principles
    - STEP-BY-STEP
    - TODO Management
    - CLEAR Framework
    ↓
PRIORITY 3: 스킬 자동 매핑 프로토콜
    - 키워드 → 에이전트/스킬 매칭
    - 모델 지정
    ↓
PRIORITY 4: 체인 패턴 실행
    - 9개 기본 체인
    - 실행 패턴 (순차/병렬/혼합)
```

---

## 🔧 구현 세부사항

### Task 도구 호출 예시
```typescript
Task(
  subagent_type: "system_architect",
  model: "opus",
  description: "시스템 아키텍처 설계",
  prompt: "마이크로서비스 아키텍처를 설계해주세요..."
)
```

### Skill 도구 호출 예시
```typescript
Skill(
  skill: "frontend-design",
  args: "대시보드 UI 구현"
)
```

### 병렬 실행 (단일 메시지에 다중 호출)
```typescript
// 동시에 여러 Task 호출
Task(subagent_type: "insight_explorer", model: "sonnet", ...)
Task(subagent_type: "connection_creator", model: "sonnet", ...)
```

---

## 📚 관련 문서

- [CLAUDE.md V2.2](/Users/changjaeyou/.claude/CLAUDE.md) - 전체 시스템 프롬프트
- [Claude-Code-Model-Auto-Switching-Analysis.md](./Claude-Code-Model-Auto-Switching-Analysis.md) - 모델 전환 분석
- [Claude-Code-Available-Tools.md](/Users/changjaeyou/Documents/Obsidian-Vault/Claude-Code-Available-Tools.md) - 사용 가능 도구 목록

---

*동적 체인 오케스트레이션 시스템 V1.0 - Claude Code 통합 가이드라인 V2.2*
