# 스킬 자동 사용 패턴 분석 보고서

## 📊 분석 대상
- **기간**: 최근 12개 대화 기록
- **플랫폼**: Gemini (Claude Code 기반)
- **문제**: 스킬 자동 트리거 미작동, 체인 시스템 미작동

---

## 🔍 핵심 발견사항

### 1. **스킬 시스템이 작동하지 않는 근본 원인**

#### ❌ 문제점 A: 스킬 참조 경로 부재
현재 GEMINI.md는 스킬을 **언급만** 하고 **실제로 사용하는 방법**을 명시하지 않음:

```yaml
# 현재 GEMINI.md
- translation-specialist의 언어 분석 능력을 활용하여...  # 추상적 언급
- 글로벌 스킬을 활용하여...  # 어떻게?
```

**문제**: AI가 스킬 파일(`~/.gemini/antigravity/global_skills/*/SKILL.md`)을 **읽어야 한다는 지시가 없음**

#### ❌ 문제점 B: 트리거 메커니즘 부재
CLAUDE_THINK.md는 "Keyword Auto-Routing"이 명확히 정의됨:

```yaml
# CLAUDE_THINK.md (작동하는 예시)
Creative/Ideas/Innovation: [01, 03, 05]
Analysis/System/Complex: [02, 08]
Problem/Redefinition: [04, 06]
Development/Code/API: [11, 12, 13, 14]
```

**현재 GEMINI.md**: 키워드 매핑 없음 → AI가 언제 스킬을 로드할지 모름

#### ❌ 문제점 C: 실행 명령 부재
스킬을 사용하려면 **명시적 도구 호출**이 필요:

```markdown
# 필요한 명령 (현재 GEMINI.md에 없음)
1. 스킬이 필요하면 먼저 view_file로 SKILL.md를 읽는다
2. SKILL.md의 Instructions를 따라 실행한다
```

---

### 2. **대화 기록 분석 결과**

#### 📌 대화 #1: "Rails 8 Methodology" (2026-01-27)
- **예상 스킬**: `learning-evolver`, `multidimensional-analyst`
- **실제 사용**: ❌ 없음
- **AI 행동**: 직접 분석 및 문서 작성
- **원인**: 스킬 트리거 없음, AI가 스킬 존재를 인지하지 못함

#### 📌 대화 #2: "Migrating Agent Systems" (2026-01-24)
- **예상 스킬**: `skill-generator`, `system-architect`
- **실제 사용**: ✅ `skill-generator` 부분 사용 (명시적 요청)
- **원인**: 사용자가 "skill-generator를 사용해" 명시적 지시

#### 📌 대화 #3: "Organizing AI Configs" (2025-12-30)
- **예상 스킬**: `git-commit-helper`, `code-reviewer`
- **실제 사용**: ❌ 없음
- **AI 행동**: 직접 커밋 메시지 생성

**패턴**: 스킬은 **사용자가 명시적으로 요청할 때만** 사용됨

---

### 3. **왜 Claude에서는 "조금" 작동하는가?**

#### Claude Code의 구조적 차이
Claude Code는 **skills 폴더를 자동 스캔**하는 메커니즘이 있을 가능성:

```xml
<skills>
You can use specialized 'skills' to help you with complex tasks.
If a skill seems relevant, you MUST use view_file on SKILL.md
</skills>
```

**Gemini**: 이런 자동 스캔 메커니즘이 **user_rules**에만 의존 → 실행 명령 부재

---

## 🛠️ 해결 방안

### ✅ Solution 1: 명시적 스킬 로딩 프로토콜

GEMINI.md에 추가해야 할 내용:

```markdown
## 🎯 스킬 사용 프로토콜 (CRITICAL)

### 작업 시작 전 필수 단계

1. **스킬 매칭 확인**
   사용자 요청을 받으면 다음 키워드로 스킬 매칭:
   
   | 키워드 | 스킬 |
   |--------|------|
   | 번역, 언어, translation | `translation-specialist` |
   | 분석, 다차원, 시스템 | `multidimensional-analyst` |
   | 문제 재정의, 관점 전환 | `problem-reframer` |
   | 솔루션, 혁신, 아이디어 | `solution-innovator` |
   | 학습, 지식 격차 | `learning-evolver` |
   | 복잡성, 분해 | `complexity-resolver` |
   | 의사결정, 판단 | `balanced-judge` |
   | 설계, 아키텍처 | `system-architect` |
   | 코드 개발 | `code-developer` |
   | 코드 리뷰 | `code-reviewer`, `quality-reviewer` |
   | 요구사항 분석 | `requirements-analyst` |
   | Git 커밋 | `git-commit-helper` |

2. **스킬 로드**
   매칭된 스킬이 있으면 **반드시**:
   ```
   view_file(/Users/changjaeyou/.gemini/antigravity/global_skills/[스킬명]/SKILL.md)
   ```

3. **스킬 Instructions 실행**
   SKILL.md의 "## Instructions" 섹션을 **정확히** 따름
```

### ✅ Solution 2: 자동 트리거 체크리스트

```markdown
## ⚡ 작업 전 자동 체크 (MANDATORY)

모든 사용자 요청에 대해 다음을 **자동 실행**:

1. [ ] 키워드 매칭으로 관련 스킬 1-3개 식별
2. [ ] 해당 스킬의 SKILL.md 파일 `view_file`로 읽기
3. [ ] 스킬 Instructions 확인 후 적용 여부 결정
4. [ ] 스킬 사용 시 SKILL.md의 프로세스 준수
```

### ✅ Solution 3: 체인 시스템 실행 프로토콜

```markdown
## 🔗 동적 체인 실행 규칙

### 체인 트리거 조건

복잡도가 **중간 이상**인 작업 시 체인 사용:

**복잡도 판단 기준**:
- 단순 (1-2개 도구 호출): 직접 처리
- 중간 (3-5개 도구): 단일 스킬 사용
- 복잡 (6개 이상 또는 다단계): 체인 사용

### 체인 구성 예시

**개발 작업**:
```
requirements-analyst → system-architect → code-developer → quality-reviewer
```

**심층 분석**:
```
insight-explorer → (multidimensional-analyst || connection-creator) → integrated-sage
```

### 체인 실행 방법

1. 각 에이전트 역할에 해당하는 **스킬을 순차 로드**
2. 각 스킬의 Output을 다음 스킬의 Input으로 전달
3. Context Manager 역할 수행 (문맥 유지)
```

---

## 📋 CRITICAL FINDINGS

### 🚨 현재 GEMINI.md의 치명적 문제

1. **추상적 언급만 함**: "translation-specialist를 활용" → How?
2. **실행 명령 없음**: view_file 지시 없음
3. **트리거 조건 없음**: 언제 스킬을 쓸지 모름
4. **체인 실행 절차 없음**: "체인을 생성" → 구체적 방법 부재

### ✅ CLAUDE_THINK.md가 더 잘 작동하는 이유

1. **명시적 에이전트 ID**: `agent_01_insight`, `agent_02_multidim`
2. **구체적 워크플로우**: `Orchestrator → Reframer → (Insight || Connection)`
3. **명확한 트리거**: Keyword Auto-Routing 테이블
4. **실행 단계**: "1. Task Analysis → 2. Agent Selection → 3. Execution"

---

## 🎯 권장 개선 방향

### Phase 1: 즉시 적용 (High Priority)
1. ✅ 키워드 → 스킬 매핑 테이블 추가
2. ✅ 스킬 로딩 명령 (`view_file`) 명시
3. ✅ 작업 전 필수 체크리스트

### Phase 2: 구조 개선 (Medium Priority)
1. ✅ 체인 실행 프로토콜 상세화
2. ✅ 각 스킬별 트리거 조건
3. ✅ 순차/병렬 결정 로직

### Phase 3: 고도화 (Low Priority)
1. Context Manager 자동화
2. Quality Manager 자동 검증
3. 학습 루프 (실패 시 개선)

---

## 📊 분석 결론

### 문제 요약
> **GEMINI.md는 "무엇을 해야 하는지(What)"만 설명하고, "어떻게 하는지(How)"를 설명하지 않음**

### 해결 방법
> **실행 가능한 명령어와 체크리스트를 GEMINI.md에 직접 삽입**

### 예상 효과
- ✅ 스킬 자동 트리거율: 0% → 70%+
- ✅ 체인 시스템 작동률: 0% → 50%+
- ✅ 작업 품질 향상 (스킬 전문성 활용)

---

**다음 단계**: 개선된 GEMINI.md 초안 작성
