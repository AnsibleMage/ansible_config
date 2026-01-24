## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [[./Product_PRD_템플릿|Product PRD 템플릿]] - 제품 레벨
- [[./Block_템플릿|Block 템플릿]] - 블럭 레벨 (상위)
- [[./Task_템플릿|Task 템플릿]] - 작은단위 레벨 (하위)
- [[../계층적_TDD_가이드|계층적 TDD 가이드]]

---

# Feature: [중단위 기능명] ⭐

> **v2 핵심 혁신:** Feature 레벨은 사용자가 인식하는 완결된 기능 단위이자, AI가 가장 효과적으로 작동하는 레벨입니다.

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**상태:** 초안 | 진행 중 | 완료

**소속 블럭:** [[Block_[N]_블럭명]]
**User Story 참조:** [[PRD#Story-N]]

---

## 🤖 AI 작성 가이드

> **역할 분담:** "인간은 코드를 안 봐도 된다"
> - **개발자 (5%)**: Feature 설계 검토 → 피드백 → 결과 확인 (하루 30분)
> - **AI (95%)**: 이 문서 작성 → 5 Tasks 분해 → TDD 구현 → Integration Test (하루 8시간)

**AI가 이 문서를 작성하는 방법:**
1. **Block.md 읽기**: 이 Feature가 Block에서 담당할 역할 파악
2. **Feature_템플릿.md 읽기**: 이 템플릿 구조 파악
3. **기능 설계**: 5개 Task로 분해 (1-2시간 단위)
4. **Integration Test 계획**: 5개 Task 통합 시나리오 작성
5. **개발자 검토**: 문서를 개발자에게 제시 (15분)
6. **승인 후**: Task_템플릿.md로 이동하여 각 Task TDD 구현 시작

**개발자는:**
- ✅ Feature 설계 문서만 검토 (코드 안 봄) - 오전 15분
- ✅ Feature 완료 시 결과 확인 (Feature.md + Integration Test 결과) - 오후 30분
- ✅ 피드백 제공 시 AI가 즉시 수정

**AI 작업 흐름 (Feature 레벨):**
```
Day 1:
  09:00-11:00 | Feature 설계 (이 문서 작성)
  11:00-11:15 | 개발자 검토 → 승인
  11:15-12:30 | Task 1 TDD (Red-Green-Refactor-Mutation)
  14:00-15:30 | Task 2 TDD
  16:00-17:30 | Task 3 TDD

Day 2:
  09:00-10:30 | Task 4 TDD
  11:00-12:30 | Task 5 TDD
  14:00-17:00 | Integration Test + Refactor
  17:00-17:30 | 개발자 결과 확인 → 피드백 반영
```

**⭐ Feature 레벨이 중요한 이유:**
- **사용자 관점**: 사용자가 인식하는 완결된 기능 단위
- **관리 관점**: 1-2일 안에 완성 가능 (진행 추적 용이)
- **AI 관점**: 5개 Task = 컨텍스트 최적 크기 (7±2, Miller's Law)
- **v2 혁신**: v1은 Product-Task 2단계, v2는 Feature 추가로 관리성 대폭 향상

---

## 📋 계층 정보

```
제품 (Product)
  └─ 블럭 [N]: [블럭명]
       └─ 🎯 중단위 [N]: [이 기능]  ← 현재 레벨
            ├─ 작은단위 1: [Task 1]
            ├─ 작은단위 2: [Task 2]
            ├─ 작은단위 3: [Task 3]
            ├─ 작은단위 4: [Task 4]
            └─ 작은단위 5: [Task 5]
```

**이 중단위의 역할:**
- [한 문장으로: 이 중단위가 블럭에서 담당하는 역할]

---

## 🎯 Feature Definition (중단위 정의)

### 한 문장 요약
> [이 중단위 기능을 한 문장으로 요약]

### User Story
```
As a [사용자 역할]
I want [이 기능]
So that [달성하려는 목표/가치]
```

### 수용 기준 (Acceptance Criteria)
- [ ] **기준 1:** [측정 가능한 기준]
- [ ] **기준 2:** [측정 가능한 기준]
- [ ] **기준 3:** [측정 가능한 기준]

### 범위 (Scope)
**포함 (In Scope):**
- [포함 항목 1]
- [포함 항목 2]
- [포함 항목 3]

**제외 (Out of Scope):**
- [제외 항목 1] - [이유]
- [제외 항목 2] - [이유]

---

## 🧩 Task Breakdown (작은단위 분할)

> **중요:** 이 중단위는 **5개 작은단위 (Task)**로 구성됩니다.
> 각 작은단위는 1-2시간 내 완료 가능해야 합니다.

### Task 1: [작업명]
**목표:**
- [이 Task가 달성할 것]

**구현 내용:**
- [구체적 구현 내용]

**예상 시간:** 1-2시간

**핵심 테스트:**
```typescript
test('should [예상 동작]', () => {
  // Given
  const input = {...};
  // When
  const result = functionName(input);
  // Then
  expect(result).toBe(expected);
});
```

**의존성:**
- 선행 Task: 없음 | Task [N]
- 후행 Task: Task 2

**문서:** [[Task_01_작업명]]

---

### Task 2: [작업명]
**목표:**
- [이 Task가 달성할 것]

**구현 내용:**
- [구체적 구현 내용]

**예상 시간:** 1-2시간

**핵심 테스트:**
```typescript
test('should [예상 동작]', () => {
  // Test code
});
```

**의존성:**
- 선행 Task: Task 1
- 후행 Task: Task 3

**문서:** [[Task_02_작업명]]

---

### Task 3: [작업명]
**목표:**
- [이 Task가 달성할 것]

**구현 내용:**
- [구체적 구현 내용]

**예상 시간:** 1-2시간

**핵심 테스트:**
```typescript
test('should [예상 동작]', () => {
  // Test code
});
```

**의존성:**
- 선행 Task: Task 2
- 후행 Task: Task 4

**문서:** [[Task_03_작업명]]

---

### Task 4: [작업명]
**목표:**
- [이 Task가 달성할 것]

**구현 내용:**
- [구체적 구현 내용]

**예상 시간:** 1-2시간

**핵심 테스트:**
```typescript
test('should [예상 동작]', () => {
  // Test code
});
```

**의존성:**
- 선행 Task: Task 3
- 후행 Task: Task 5

**문서:** [[Task_04_작업명]]

---

### Task 5: [작업명]
**목표:**
- [이 Task가 달성할 것]

**구현 내용:**
- [구체적 구현 내용]

**예상 시간:** 1-2시간

**핵심 테스트:**
```typescript
test('should [예상 동작]', () => {
  // Test code
});
```

**의존성:**
- 선행 Task: Task 4
- 후행 Task: 없음 (Feature 통합 테스트)

**문서:** [[Task_05_작업명]]

---

## 🧪 Feature-Level TDD (중단위 통합 테스트)

> **프랙탈 TDD:** 작은단위에서 Unit Test를 했다면,
> 중단위에서는 **5개 Task가 통합되었을 때의 동작을 테스트**합니다.

### Red: Feature Integration Test 작성

**테스트 시나리오:**
```typescript
describe('Feature: [기능명]', () => {
  describe('통합 시나리오 1: [Happy Path]', () => {
    it('should [전체 기능이 정상 동작]', async () => {
      // Given: 5개 Task가 모두 완료된 상태
      const context = setupFeatureContext();

      // When: Feature 전체를 실행
      const result = await executeFeature(context, {
        // Feature input
      });

      // Then: Feature 수용 기준 충족
      expect(result.criterion1).toBe(true);
      expect(result.criterion2).toBe(true);
      expect(result.criterion3).toBe(true);
    });
  });

  describe('통합 시나리오 2: [Error Case]', () => {
    it('should [에러 상황을 올바르게 처리]', async () => {
      // Error handling test
    });
  });

  describe('통합 시나리오 3: [Edge Case]', () => {
    it('should [엣지 케이스 처리]', async () => {
      // Edge case test
    });
  });
});
```

**실행 결과 (Red):**
```bash
❌ FAIL: Feature: [기능명]
  - Task 01-05 미완성
  - Feature 통합 함수 미구현
```

---

### Green: 5개 Task 구현

**구현 순서:**

```
1. Task 1 TDD (Red-Green-Refactor) ✅
   └─ Unit Test 통과

2. Task 2 TDD (Red-Green-Refactor) ✅
   └─ Unit Test 통과

3. Task 3 TDD (Red-Green-Refactor) ✅
   └─ Unit Test 통과

4. Task 4 TDD (Red-Green-Refactor) ✅
   └─ Unit Test 통과

5. Task 5 TDD (Red-Green-Refactor) ✅
   └─ Unit Test 통과

6. Feature 통합 함수 구현 ✅
   └─ 5개 Task를 연결
```

**Feature 통합 코드 예시:**
```typescript
// feature/[기능명]/index.ts
export async function execute[기능명](input: FeatureInput): Promise<FeatureOutput> {
  // Task 1
  const step1Result = await task1(input);

  // Task 2
  const step2Result = await task2(step1Result);

  // Task 3
  const step3Result = await task3(step2Result);

  // Task 4
  const step4Result = await task4(step3Result);

  // Task 5
  const finalResult = await task5(step4Result);

  return finalResult;
}
```

**실행 결과 (Green):**
```bash
✅ PASS: Feature: [기능명]
  - 모든 통합 테스트 통과
  - Task 01-05 통합 성공
```

---

### Refactor: Feature 레벨 리팩토링

**리팩토링 포인트:**
- [ ] **Task 간 중복 제거**
  - [중복 코드 식별]
  - [공통 함수 추출]

- [ ] **Feature 레벨 추상화**
  - [인터페이스 명확화]
  - [의존성 주입]

- [ ] **에러 처리 통일**
  - [Feature 레벨 에러 핸들링]
  - [에러 메시지 일관성]

- [ ] **성능 최적화**
  - [병렬 처리 가능한 Task 식별]
  - [불필요한 중간 데이터 제거]

**리팩토링 후 검증:**
```bash
✅ PASS: 모든 테스트 통과 유지
✅ PASS: 복잡도 감소 (Before: [N] → After: [M])
✅ PASS: 중복 코드 제거 (Before: [N]줄 → After: [M]줄)
```

---

### Mutation: Feature 통합 테스트 품질 검증

**변이 테스트 실행:**
```bash
npm run test:mutation -- feature/[기능명]
```

**목표 변이 점수:** >80%

**결과 분석:**
```
생성된 변이: [N]개
죽인 변이: [M]개
살아남은 변이: [K]개
변이 점수: [M/N * 100]%
```

**살아남은 변이 분석:**
- 변이 1: [분석] - [조치: 허용 가능 | 테스트 추가 필요]
- 변이 2: [분석] - [조치: 허용 가능 | 테스트 추가 필요]

---

## 📊 Feature Metrics (중단위 메트릭)

### 품질 지표

| 지표 | 목표 | 현재 | 상태 |
|------|------|------|------|
| Unit Test 커버리지 | >90% | [%] | ✅/⚠️/❌ |
| Integration Test 커버리지 | >80% | [%] | ✅/⚠️/❌ |
| 변이 점수 (Feature 레벨) | >80% | [%] | ✅/⚠️/❌ |
| 복잡도 (평균) | <10 | [N] | ✅/⚠️/❌ |
| Task 완료율 | 5/5 | [N]/5 | [진행률]% |

### 진행 상황

```
Task 1: ✅ 완료 (실제: 1.5h, 예상: 1.5h)
Task 2: ✅ 완료 (실제: 2h, 예상: 1.5h)
Task 3: 🚧 진행 중 (50%)
Task 4: ⏳ 대기
Task 5: ⏳ 대기

전체 진행률: 50% (2.5/5 Task)
```

---

## 🔗 Dependencies (의존성)

### 선행 중단위
- [[Feature_[N-1]_기능명]] - [의존 관계 설명]

### 후행 중단위
- [[Feature_[N+1]_기능명]] - [의존 관계 설명]

### 외부 의존성
- **API:** [사용하는 외부 API]
- **라이브러리:** [사용하는 라이브러리]
- **데이터:** [필요한 데이터/DB]

---

## ⚠️ Risks & Issues (리스크 및 이슈)

### 현재 리스크

#### 리스크 1: [리스크 설명]
- **영향도:** 높음 | 중간 | 낮음
- **발생 확률:** 높음 | 중간 | 낮음
- **완화 전략:** [대응 방법]
- **담당자:** [이름]

### 발생한 이슈

#### Issue #1: [이슈 제목]
- **설명:** [문제 상세]
- **영향 Task:** Task [N]
- **상태:** Open | In Progress | Resolved
- **해결 방법:** [해결 방법]

---

## 📝 Daily Progress (일일 진행 기록)

### YYYY-MM-DD (오늘)
**작업 내용:**
- ✅ Task 1 완료 (Red-Green-Refactor)
- ✅ Task 2 완료 (Red-Green-Refactor)
- 🚧 Task 3 진행 중 (현재: Green 단계)

**소요 시간:** [시간]

**블로커:**
- 없음 | [블로커 내용]

**내일 계획:**
- [ ] Task 3 완료
- [ ] Task 4 시작

---

## ✅ Feature Completion Criteria (완료 기준)

### Task 완료
- [ ] Task 1: Unit Test 통과 + 변이 점수 >80%
- [ ] Task 2: Unit Test 통과 + 변이 점수 >80%
- [ ] Task 3: Unit Test 통과 + 변이 점수 >80%
- [ ] Task 4: Unit Test 통과 + 변이 점수 >80%
- [ ] Task 5: Unit Test 통과 + 변이 점수 >80%

### Feature 통합 완료
- [ ] Feature Integration Test 통과
- [ ] Feature 레벨 변이 점수 >80%
- [ ] 모든 수용 기준 충족
- [ ] 코드 리뷰 완료 (최소 1명)
- [ ] 문서 작성 완료

### 품질 검증
- [ ] Unit Test 커버리지 >90%
- [ ] Integration Test 커버리지 >80%
- [ ] 복잡도 평균 <10
- [ ] 성능 목표 달성 ([목표 값])
- [ ] 보안 검토 완료

---

## 🎓 Lessons Learned (교훈)

### ✅ 잘한 점
- [잘한 점 1]
- [잘한 점 2]
- [잘한 점 3]

### ⚠️ 개선 필요
- [개선점 1]
  - 원인: [근본 원인]
  - 개선 방법: [다음에 적용할 방법]

- [개선점 2]
  - 원인: [근본 원인]
  - 개선 방법: [다음에 적용할 방법]

### 💡 다음 Feature에 적용
- [적용 사항 1]
- [적용 사항 2]

---

## 🔍 Code Review Notes (코드 리뷰 노트)

**리뷰어:** [이름]
**리뷰일:** YYYY-MM-DD

### CLEAR 원칙 체크
- [ ] **Concise**: 각 Task가 간결한가? (복잡도 <10)
- [ ] **Logical**: Task 간 흐름이 논리적인가?
- [ ] **Explicit**: 의도가 명확한가? (네이밍, 주석)
- [ ] **Adaptive**: 변경이 용이한가? (의존성 주입)
- [ ] **Reflective**: 테스트가 충분한가? (커버리지 >90%)

### 코멘트
- [코멘트 1]
- [코멘트 2]
- [코멘트 3]

### 액션 아이템
- [ ] [수정 사항 1]
- [ ] [수정 사항 2]

---

## 📊 Final Report (최종 보고)

> **Feature 완료 시 작성**

### 완료 요약
**완료일:** YYYY-MM-DD
**총 소요 시간:** [실제]시간 (예상: [예상]시간)
**시간 편차:** +[N]시간 | -[N]시간 | 정확

### 최종 메트릭

| 지표 | 목표 | 달성 | 평가 |
|------|------|------|------|
| Unit Test 커버리지 | >90% | [%] | ✅/❌ |
| Integration Test 커버리지 | >80% | [%] | ✅/❌ |
| 변이 점수 | >80% | [%] | ✅/❌ |
| 복잡도 평균 | <10 | [N] | ✅/❌ |
| 버그 수 | 0개 | [N]개 | ✅/❌ |

### User Story 달성도
- ✅ 수용 기준 1: [달성 여부]
- ✅ 수용 기준 2: [달성 여부]
- ✅ 수용 기준 3: [달성 여부]

### 핵심 교훈
1. **[교훈 1]**
   - 상황: [어떤 상황?]
   - 학습: [무엇을 배웠나?]
   - 적용: [다음 Feature에 어떻게 적용?]

2. **[교훈 2]**
   - 상황: [어떤 상황?]
   - 학습: [무엇을 배웠나?]
   - 적용: [다음 Feature에 어떻게 적용?]

---

## 💡 Notes (참고 사항)

### CLEAR 원칙 체크
- [ ] **Concise**: 5개 Task로 명확히 분할
- [ ] **Logical**: Task 의존성이 명확
- [ ] **Explicit**: 각 Task의 목표와 테스트가 명시적
- [ ] **Adaptive**: Task 단위 조정 가능
- [ ] **Reflective**: Feature 레벨 회고 및 교훈 기록

### 계층적 TDD 매핑
- **이 문서는 "중단위 (Feature)" 레벨입니다.**
- 상위 계층: [[Block_[N]_블럭명]] (블럭 레벨)
- 하위 계층: [[Task_01_작업명]] ~ [[Task_05_작업명]] (작은단위 레벨)
- 프랙탈 TDD: 작은단위 Unit Test → 중단위 Integration Test

### 업데이트 주기
- **일일:** Daily Progress 작성
- **Task 완료 시:** 해당 Task 섹션 업데이트
- **Feature 완료 시:** Final Report 작성

---

**최종 업데이트:** YYYY-MM-DD HH:MM
**작성자:** [이름]
**다음 Feature:** [[Feature_[N+1]_기능명]]
