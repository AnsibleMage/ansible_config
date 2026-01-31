# GEMINI.md 개선 구현 계획

## 문제 요약

2일간 사용 결과, GEMINI.md의 스킬과 체인 시스템이 작동하지 않는 문제 확인:
- **Gemini**: 스킬 자동 트리거 0%
- **Claude**: 명시적 요청 시에만 부분 작동
- **근본 원인**: "무엇을 해야 하는지(What)"만 설명, "어떻게 하는지(How)" 누락

상세 분석은 [`skill_usage_analysis.md`](file:///Users/changjaeyou/.gemini/antigravity/brain/acb7c941-252d-452c-ae77-688a90dbd93f/skill_usage_analysis.md) 참조.

---

## 사용자 검토 필요 사항

> [!IMPORTANT]
> 다음 변경사항은 GEMINI.md의 작동 방식을 근본적으로 바꿉니다:
> 
> 1. **AI가 모든 요청마다 자동으로 스킬을 검색하도록 강제**
> 2. **키워드 기반 스킬 매칭 테이블 추가** (21개 스킬)
> 3. **필수 체크리스트 추가** (스킬 사용 전 view_file 강제)
>
> 이로 인해 AI의 응답 시간이 약간 증가할 수 있으나, 스킬 활용률은 0% → 70%+ 향상 예상됩니다.

---

## 제안 변경사항

### 1. 스킬 로딩 프로토콜 추가

#### [NEW] SKILL_PROTOCOL.md 섹션 추가

```markdown
## 🎯 스킬 자동 로딩 프로토콜 (MANDATORY)

### 📋 작업 전 필수 체크리스트

**모든 사용자 요청에 대해 다음을 자동 실행**:

1. [ ] 아래 키워드 매핑 테이블로 관련 스킬 1-3개 식별
2. [ ] 해당 스킬의 SKILL.md 파일을 `view_file`로 읽기
3. [ ] SKILL.md의 Instructions 확인 후 적용 여부 결정
4. [ ] 스킬 사용 시 SKILL.md의 프로세스 정확히 따름

### 🗺️ 키워드 → 스킬 매핑 테이블

| 키워드 패턴 | 스킬 경로 | 우선순위 |
|------------|-----------|---------|
| 번역, 언어, translation, 다국어 | `translation-specialist` | HIGH |
| 분석, 다차원, 시스템 사고, 관점 | `multidimensional-analyst` | HIGH |
| 인사이트, 패턴, 관찰, 발견 | `insight-explorer` | MEDIUM |
| 연결, 관계, 은유, 유추 | `connection-creator` | MEDIUM |
| 문제 재정의, 관점 전환, 프레이밍 | `problem-reframer` | HIGH |
| 솔루션, 혁신, 아이디어, 창의 | `solution-innovator` | HIGH |
| 심화, 질문, Why, What-If | `insight-amplifier` | MEDIUM |
| 학습, 지식 격차, 메타인지 | `learning-evolver` | MEDIUM |
| 복잡성, 분해, 시스템 해체 | `complexity-resolver` | HIGH |
| 의사결정, 판단, 균형 | `balanced-judge` | HIGH |
| 통합, 지혜, 윤리, 종합 | `integrated-sage` | MEDIUM |
| 요구사항, 분석, 비즈니스 | `requirements-analyst` | HIGH |
| 설계, 아키텍처, Clean, SOLID | `system-architect` | HIGH |
| 개발, 코드, TDD, 구현 | `code-developer` | HIGH |
| 리뷰, 품질, 테스트, 보안 | `code-reviewer` OR `quality-reviewer` | HIGH |
| 백엔드, API, 데이터베이스 | `backend-developer` | HIGH |
| Git, 커밋, 버전관리 | `git-commit-helper` | MEDIUM |
| 품질 관리, 검증, 프로세스 | `quality-manager` | MEDIUM |
| 문맥, 컨텍스트, 전달 | `context-manager` | LOW |
| 스킬 생성, 메타 | `skill-generator` | LOW |

### 🔧 스킬 로딩 명령

스킬이 매칭되면 **반드시** 다음 명령 실행:
```
view_file(/Users/changjaeyou/.gemini/antigravity/global_skills/[스킬명]/SKILL.md)
```

예시:
- 번역 요청 → `view_file(/Users/changjaeyou/.gemini/antigravity/global_skills/translation-specialist/SKILL.md)`
- 시스템 설계 → `view_file(/Users/changjaeyou/.gemini/antigravity/global_skills/system-architect/SKILL.md)`
```

---

### 2. 체인 시스템 실행 프로토콜 추가

#### [MODIFY] 동적 체인 패턴 섹션 개선

**현재 (추상적)**:
```markdown
### A. 개발 실행 체인 (DevChain)
> `Architect` (설계) → `Developer` (구현) → `Reviewer` (검증)
```

**개선 (실행 가능)**:
```markdown
### A. 개발 실행 체인 (DevChain)

**트리거 조건**: 코드 개발, API 설계, 시스템 구현 키워드

**실행 절차**:
1. `view_file` → `requirements-analyst/SKILL.md` → Instructions 실행
2. Output을 Input으로 → `system-architect/SKILL.md` → Instructions 실행
3. Output을 Input으로 → `code-developer/SKILL.md` → Instructions 실행
4. Output을 Input으로 → `quality-reviewer/SKILL.md` → Instructions 실행

**병렬 실행 예시** (복수 기능 개발):
```
(Developer[기능A] || Developer[기능B] || Developer[기능C]) → Reviewer
```

**Context 전달 예시**:
```yaml
# requirements-analyst Output
requirements:
  functional: [FR1, FR2, FR3]
  non_functional: {performance: "< 100ms", security: "OWASP Top 10"}

# → system-architect Input으로 사용
# → diagram + architecture_decisions 생성

# → code-developer Input으로 사용
# → 실제 코드 구현

# → quality-reviewer Input으로 사용
# → 품질 검증
```
```

---

### 3. 복잡도 기반 자동 분기 추가

#### [NEW] 복잡도 판단 로직

```markdown
## ⚖️ 복잡도 기반 작업 분기

모든 요청에 대해 먼저 복잡도를 판단하고 전략 선택:

| 복잡도 | 기준 | 전략 | 예시 |
|--------|------|------|------|
| **단순** | - 1-2개 도구 호출<br>- 명확한 답변 가능 | 직접 처리<br>(스킬 불필요) | "Python 리스트 정렬 방법" |
| **중간** | - 3-5개 도구<br>- 단일 전문성 필요 | **단일 스킬** 사용 | "Rails API 설계 원칙" |
| **복잡** | - 6개 이상 도구<br>- 다단계 사고<br>- 여러 전문성 필요 | **체인** 사용 | "결제 시스템 설계 및 구현" |

### 자동 판단 체크리스트

요청을 받으면:
1. [ ] 필요한 도구 호출 횟수 예측 (1-2 / 3-5 / 6+)
2. [ ] 단일 전문성으로 해결 가능? (Yes → 스킬 1개 / No → 체인)
3. [ ] 다단계 절차 필요? (Yes → 체인 / No → 스킬 또는 직접)
4. [ ] 위 표에 따라 전략 선택 및 실행
```

---

## 검증 계획

### 자동 테스트
- ❌ 해당 없음 (설정 파일이므로 자동 테스트 불가)

### 수동 검증

#### Test Case 1: 번역 요청
**입력**:
```
"다음을 영어로 번역해주세요: 귀하께 감사드립니다."
```

**기대 동작**:
1. ✅ "번역" 키워드 감지
2. ✅ `translation-specialist/SKILL.md` 자동 `view_file`
3. ✅ 4-Layer Analysis 또는 직역 모드 실행
4. ✅ 스킬 Instructions에 따른 출력

**검증 방법**: 새 대화 시작 → 번역 요청 → AI가 자동으로 SKILL.md를 읽는지 확인

---

#### Test Case 2: 시스템 설계 요청
**입력**:
```
"마이크로서비스 결제 시스템을 설계해주세요."
```

**기대 동작**:
1. ✅ 복잡도 판단: **복잡** (다단계 + 여러 전문성)
2. ✅ DevChain 트리거
3. ✅ 순차 스킬 로딩:
   - `requirements-analyst/SKILL.md`
   - `system-architect/SKILL.md`
   - `code-developer/SKILL.md` (optional)
4. ✅ 각 스킬의 Output을 다음 Input으로 전달

**검증 방법**: 새 대화 → 복잡한 시스템 설계 요청 → 체인 실행 여부 확인

---

#### Test Case 3: 간단한 질문
**입력**:
```
"Python에서 리스트를 정렬하는 방법은?"
```

**기대 동작**:
1. ✅ 복잡도 판단: **단순**
2. ✅ 스킬 사용 없이 직접 답변
3. ✅ 불필요한 SKILL.md 로딩 없음

**검증 방법**: 간단한 질문 → 즉시 답변하는지 확인 (오버헤드 없음)

---

## 구현 순서

1. **[HIGH]** 키워드 매핑 테이블 + 필수 체크리스트 추가
   - 파일: `GEMINI.md` L17 직후 삽입
   - 스킬 자동 트리거의 핵심

2. **[HIGH]** 복잡도 판단 로직 추가
   - 파일: `GEMINI.md` L42 (워크플로우 엔진) 안에 삽입
   - 불필요한 스킬 로딩 방지

3. **[MEDIUM]** 체인 실행 프로토콜 상세화
   - 파일: `GEMINI.md` L72-85 (동적 체인 패턴) 전면 재작성
   - 추상적 설명을 실행 가능한 명령으로 변경

4. **[LOW]** 예시 및 트러블슈팅 가이드 추가
   - 파일: `GEMINI.md` 말미
   - 사용자가 디버깅 가능하도록

---

## 예상 효과

### 정량적 개선
- ✅ 스킬 자동 사용률: **0% → 70%+**
- ✅ 체인 시스템 작동률: **0% → 50%+**
- ✅ 응답 품질: **+30%** (전문 스킬 활용)

### 정성적 개선
- ✅ 사용자가 명시적으로 "○○ 스킬 사용해" 요청 불필요
- ✅ 복잡한 작업에서 자동으로 다단계 전문가 협업
- ✅ CLAUDE_THINK.md와 동등한 자동화 수준 달성

### 잠재적 이슈
- ⚠️ 모든 요청마다 키워드 매칭 → 약간의 오버헤드
- ⚠️ 복잡도 판단 실수 시 불필요한 스킬 로딩
- 💡 해결책: 복잡도 판단 로직을 명확히 하여 오판 최소화

---

## 다음 단계

1. ✅ 사용자 승인 대기
2. 승인 후 → EXECUTION 모드로 전환
3. GEMINI.md 개선 구현
4. 수동 테스트 3가지 실행
5. Walkthrough 작성

---

**질문사항**:
1. 모든 요청마다 키워드 매칭을 실행하는 오버헤드가 허용 가능한가요?
2. 체인 실행 시 중간 Output을 사용자에게 보여줄까요, 아니면 최종 결과만 보여줄까요?
3. 특정 스킬을 비활성화하거나 우선순위를 조정하고 싶은 것이 있나요?
