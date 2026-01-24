## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [[./Feature_템플릿|Feature 템플릿]] - 중단위 레벨 (상위)
- [[./Block_템플릿|Block 템플릿]] - 블럭 레벨
- [[./Product_PRD_템플릿|Product PRD 템플릿]] - 제품 레벨
- [[../계층적_TDD_가이드|계층적 TDD 가이드]]

---

# Task: [작은단위 작업명]

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.1
**상태:** 대기 | 진행 중 | 완료

**소속 Feature:** [[Feature_[N]_기능명]]
**소속 Block:** [[Block_[N]_블럭명]]

---

## 🤖 AI 작성 가이드

> **역할 분담:** "인간은 코드를 안 봐도 된다"
> - **개발자 (5%)**: Feature 설계 검토 → 이 Task의 목표 이해 → 결과 확인 (테스트 통과 여부만)
> - **AI (95%)**: 이 문서 작성 → Red-Green-Refactor-Mutation 사이클 실행 → 코드 + 테스트 완성

### AI가 이 문서를 작성하는 방법

**입력:**
- **Feature 문서**: [[Feature_[N]_기능명]] 읽기 → 이 Task가 Feature에서 담당할 역할 파악
- **Task_템플릿.md**: 이 템플릿 구조 파악

**작업 흐름 (90분 표준):**

```
15분 | Red (테스트 작성)
       - Task_템플릿.md 읽고 이 문서 작성
       - Given-When-Then 구조로 테스트 작성
       - 테스트 실행 → 실패 확인 (🔴)

30분 | Green (최소 구현)
       - 테스트를 통과하는 최소한의 코드 작성
       - 하드코딩도 허용 (테스트만 통과하면 됨)
       - 테스트 실행 → 통과 확인 (🟢)

30분 | Refactor (품질 개선)
       - 코드 품질 개선 (네이밍, 중복 제거, 복잡도 감소)
       - SOLID 원칙 적용
       - 테스트 실행 → 여전히 통과 확인 (🔵)

15분 | Mutation (테스트 품질 검증)
       - 변이 테스트 실행
       - 변이 점수 >80% 확인
       - 살아남은 변이 분석 및 테스트 보완 (🧬)
```

**출력:**
- ✅ **이 Task 문서**: Task 정의, TDD 사이클 기록
- ✅ **소스 코드**: `src/[feature]/[task-name].ts` (90-100 lines)
- ✅ **테스트 코드**: `tests/[feature]/[task-name].test.ts` (50-70 lines)
- ✅ **품질 지표**: 커버리지 >90%, 변이 점수 >80%, 복잡도 <10

### 개발자는?

**작업 전 (5분):**
- ✅ Feature 문서에서 Task 목표 이해
- ✅ AI가 작성한 이 문서 빠르게 검토
- ✅ "이해했으니 진행해" 승인

**작업 후 (5분):**
- ✅ 테스트 통과 여부만 확인 (`npm test` 결과)
- ✅ 변이 점수 확인 (>80%인지만)
- ✅ 코드는 안 봐도 됨 (테스트가 품질을 보장)

**개발자 총 시간:** 10분 (전체의 10%)

**AI 총 시간:** 90분 (전체의 90%)

### Task 레벨의 핵심

> **가장 작은 TDD 사이클 = 프랙탈 TDD의 실행 단위**

- **계층 위치**: Product → Block → Feature → **Task (여기!)** ← 최하위 레벨
- **테스트 레벨**: **Unit Test** (가장 작은 단위 테스트)
- **시간 박스**: 90분 표준 (최대 2시간)
- **코드 크기**: 함수 1-3개, 100 lines 이하
- **품질 기준**: 변이 점수 >80% (테스트 품질의 진짜 지표)
- **CLEAR 적용**: Task 레벨에서도 Concise, Logical, Explicit, Adaptive, Reflective 원칙 적용
- **5단계 적용**: Task 레벨에서도 Recognize → Explore → Opposites → Select → Verify 사고 프로세스 적용

**Task 5개 완료 → Feature Integration Test**
**Feature 3개 완료 → Block Module Test**
**Block 3개 완료 → Product E2E Test**

---

## 📋 계층 정보

```
제품 (Product): [제품명]
  └─ 블럭 [N]: [블럭명]
       └─ 중단위 [N]: [Feature명]
            └─ 🎯 작은단위 [N]: [이 Task]  ← 현재 레벨
```

**이 Task의 역할:**
- [한 문장으로: 이 Task가 Feature에서 담당하는 역할]

---

## 🎯 Task Definition (작업 정의)

### 한 문장 요약
> [이 Task를 한 문장으로 요약]

### 작업 목표
**달성할 것:**
- [목표 1]
- [목표 2]
- [목표 3]

**달성 기준:**
- [ ] [측정 가능한 기준 1]
- [ ] [측정 가능한 기준 2]
- [ ] [측정 가능한 기준 3]

### 범위 (Scope)
**포함:**
- [포함 항목 1]
- [포함 항목 2]

**제외:**
- [제외 항목 1] - [이유]

**제약 조건:**
- **시간:** 1-2시간 내 완료
- **복잡도:** Cyclomatic Complexity < 10
- **성능:** [성능 요구사항]

---

## 🧪 Unit TDD Cycle (단위 테스트 사이클)

> **프랙탈 TDD 최소 단위:** 작은단위는 **Unit Test**로 검증합니다.
> Red → Green → Refactor → Mutation 사이클을 엄격히 준수합니다.

### Phase 1: Red (실패 테스트 작성) 🔴

**테스트 우선 작성 (Test First):**

```typescript
// tests/[feature]/[task-name].test.ts
import { functionName } from '@/[feature]/[task-name]';

describe('Task: [작업명]', () => {
  describe('[기능 설명]', () => {
    it('should [예상 동작] when [조건]', () => {
      // Given (준비)
      const input = {
        // 테스트 입력 데이터
      };

      // When (실행)
      const result = functionName(input);

      // Then (검증)
      expect(result).toBe(expectedValue);
      expect(result).toHaveProperty('field', value);
    });
  });

  describe('[에러 케이스]', () => {
    it('should throw error when [잘못된 입력]', () => {
      // Given
      const invalidInput = { /* ... */ };

      // When & Then
      expect(() => {
        functionName(invalidInput);
      }).toThrow('[에러 메시지]');
    });
  });

  describe('[엣지 케이스]', () => {
    it('should handle empty input', () => {
      // Test edge case
    });

    it('should handle null/undefined', () => {
      // Test edge case
    });
  });
});
```

**실행 결과 (Red):**
```bash
npm test

❌ FAIL tests/[feature]/[task-name].test.ts
  Task: [작업명]
    ✕ should [예상 동작] when [조건] (2 ms)

● Task: [작업명] › should [예상 동작] when [조건]

  ReferenceError: functionName is not defined

Test Suites: 1 failed, 1 total
Tests:       1 failed, 1 total
```

**✅ Red 단계 완료 조건:**
- [ ] 테스트 코드가 실행된다 (문법 오류 없음)
- [ ] 테스트가 실패한다 (구현이 없으므로 당연)
- [ ] 실패 이유가 명확하다 ("기능 미구현")

---

### Phase 2: Green (최소 구현) 🟢

**테스트를 통과하는 최소한의 코드:**

```typescript
// src/[feature]/[task-name].ts

/**
 * [기능 설명]
 * @param input - [입력 설명]
 * @returns [출력 설명]
 */
export function functionName(input: InputType): OutputType {
  // 1단계: 입력 검증
  if (!input) {
    throw new Error('[에러 메시지]');
  }

  // 2단계: 최소 로직 (하드코딩도 허용!)
  // 테스트만 통과하면 됨
  const result = processInput(input);

  return result;
}

// Private helper (필요시)
function processInput(input: InputType): OutputType {
  // 실제 로직
  return {
    // 결과
  };
}
```

**실행 결과 (Green):**
```bash
npm test

✅ PASS tests/[feature]/[task-name].test.ts
  Task: [작업명]
    ✓ should [예상 동작] when [조건] (3 ms)
    ✓ should throw error when [잘못된 입력] (1 ms)
    ✓ should handle empty input (1 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        0.856 s
```

**✅ Green 단계 완료 조건:**
- [ ] 모든 테스트가 통과한다
- [ ] 코드가 간결하다 (불필요한 복잡도 없음)
- [ ] 테스트 커버리지 100% (이 Task에 한해)

---

### Phase 3: Refactor (개선) 🔵

**코드 품질 개선 (테스트 통과 유지):**

#### 리팩토링 체크리스트

**1. 네이밍 개선:**
```typescript
// ❌ Before
function fn(x) { /* ... */ }

// ✅ After
function calculateUserScore(userData: UserData): Score { /* ... */ }
```

**2. 중복 제거:**
```typescript
// ❌ Before
if (condition1) {
  // 로직 A
  doSomething();
}
if (condition2) {
  // 로직 A (중복!)
  doSomething();
}

// ✅ After
const shouldDoSomething = condition1 || condition2;
if (shouldDoSomething) {
  doSomething();
}
```

**3. 복잡도 감소:**
```typescript
// ❌ Before (복잡도: 8)
function processData(data) {
  if (data.type === 'A') {
    if (data.status === 'active') {
      // ...
    } else {
      // ...
    }
  } else if (data.type === 'B') {
    // ...
  }
}

// ✅ After (복잡도: 3)
const processors = {
  A: processTypeA,
  B: processTypeB,
};

function processData(data) {
  const processor = processors[data.type];
  return processor(data);
}
```

**4. 의존성 주입:**
```typescript
// ❌ Before (강한 결합)
class UserService {
  save(user) {
    const db = new Database();
    db.save(user);
  }
}

// ✅ After (느슨한 결합)
class UserService {
  constructor(private repository: UserRepository) {}

  save(user) {
    this.repository.save(user);
  }
}
```

**실행 결과 (Refactor):**
```bash
npm test

✅ PASS tests/[feature]/[task-name].test.ts (테스트 통과 유지!)

Code Quality:
- Complexity: 3 (Before: 7) ✅
- Duplication: 0% (Before: 15%) ✅
- Lines: 45 (Before: 67) ✅
```

**✅ Refactor 단계 완료 조건:**
- [ ] 모든 테스트 여전히 통과
- [ ] 복잡도 < 10
- [ ] 중복 코드 제거
- [ ] 네이밍 명확
- [ ] SOLID 원칙 준수

---

### Phase 4: Mutation (테스트 품질 검증) 🧬

**변이 테스트로 테스트 품질 확인:**

```bash
npm run test:mutation -- tests/[feature]/[task-name].test.ts
```

**변이 테스트 원리:**
```
1. 코드를 변이시킴 (Mutant 생성)
   예: `if (x > 0)` → `if (x >= 0)`
   예: `return a + b` → `return a - b`

2. 테스트 실행
   - 변이가 발견됨 (테스트 실패) → 좋은 테스트! ✅
   - 변이가 발견 안됨 (테스트 통과) → 테스트 부족! ❌

3. 변이 점수 계산
   변이 점수 = (죽인 변이 / 총 변이) * 100
```

**실행 결과:**
```
Mutation Testing Report
=======================

File: src/[feature]/[task-name].ts

생성된 변이: 15개
죽인 변이: 13개 (86.7%)
살아남은 변이: 2개 (13.3%)

변이 점수: 86.7% ✅ (목표: >80%)

살아남은 변이 상세:
┌─────┬──────────┬─────────────────┬──────────┐
│ ID  │ Line     │ Mutation        │ Status   │
├─────┼──────────┼─────────────────┼──────────┤
│ #1  │ 23       │ > changed to >= │ Survived │
│ #2  │ 45       │ || changed to &&│ Survived │
└─────┴──────────┴─────────────────┴──────────┘
```

**살아남은 변이 분석:**

**변이 #1 (Line 23: `>` → `>=`):**
- **분석:** 경계값 테스트 누락
- **조치:** ✅ 경계값 테스트 추가 필요
- **테스트 추가:**
  ```typescript
  it('should handle boundary value (x = 0)', () => {
    expect(functionName(0)).toBe(expectedBoundaryResult);
  });
  ```

**변이 #2 (Line 45: `||` → `&&`):**
- **분석:** 논리 연산자 변경 감지 못함
- **조치:** ⚠️ 허용 가능 (해당 로직은 동일한 결과)
- **근거:** 두 조건이 동시에 만족하는 경우가 테스트 범위 밖

**재테스트 (변이 #1 테스트 추가 후):**
```
변이 점수: 93.3% ✅ (14/15 죽임)
```

**✅ Mutation 단계 완료 조건:**
- [ ] 변이 점수 > 80%
- [ ] 살아남은 변이 분석 완료
- [ ] 필요한 테스트 추가 완료

---

## 📊 Task Metrics (작업 메트릭)

### 품질 지표

| 지표 | 목표 | 현재 | 상태 |
|------|------|------|------|
| Unit Test 통과 | 100% | [%] | ✅/❌ |
| 테스트 커버리지 | >90% | [%] | ✅/⚠️/❌ |
| 변이 점수 | >80% | [%] | ✅/⚠️/❌ |
| Cyclomatic Complexity | <10 | [N] | ✅/⚠️/❌ |
| 코드 라인 수 | <100 | [N] | ✅/⚠️/❌ |
| 중복 코드 | 0% | [%] | ✅/⚠️/❌ |

### 시간 추적

| 단계 | 예상 시간 | 실제 시간 | 차이 |
|------|----------|----------|------|
| Red | 15분 | [실제]분 | [±]분 |
| Green | 30분 | [실제]분 | [±]분 |
| Refactor | 30분 | [실제]분 | [±]분 |
| Mutation | 15분 | [실제]분 | [±]분 |
| **총계** | **90분** | **[실제]분** | **[±]분** |

---

## 🔗 Dependencies (의존성)

### 선행 Task
- [[Task_[N-1]_작업명]] - [의존 내용]
  - 필요한 출력: [Output Type]
  - 의존 이유: [설명]

### 후행 Task
- [[Task_[N+1]_작업명]] - [의존 내용]
  - 제공할 출력: [Output Type]
  - 연결 방식: [설명]

### 외부 라이브러리
- **라이브러리 A:** [버전] - [사용 함수]
- **라이브러리 B:** [버전] - [사용 클래스]

---

## 💻 Implementation Details (구현 상세)

### 입력/출력 인터페이스

```typescript
// Input Type
interface TaskInput {
  field1: string;
  field2: number;
  field3?: boolean; // optional
}

// Output Type
interface TaskOutput {
  result: string;
  status: 'success' | 'failure';
  metadata?: Record<string, any>;
}
```

### 핵심 알고리즘

```typescript
/**
 * [알고리즘 설명]
 *
 * 시간 복잡도: O(n)
 * 공간 복잡도: O(1)
 */
function coreAlgorithm(input: TaskInput): TaskOutput {
  // Step 1: [단계 설명]
  const step1Result = processStep1(input);

  // Step 2: [단계 설명]
  const step2Result = processStep2(step1Result);

  // Step 3: [단계 설명]
  return finalizeResult(step2Result);
}
```

### 에러 처리

```typescript
// 커스텀 에러 클래스
class TaskError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: any
  ) {
    super(message);
    this.name = 'TaskError';
  }
}

// 에러 처리 예시
try {
  const result = executaTask(input);
} catch (error) {
  if (error instanceof TaskError) {
    // Task 레벨 에러 처리
    handleTaskError(error);
  } else {
    // 예상치 못한 에러
    throw error;
  }
}
```

---

## 🔍 Code Review Checklist (코드 리뷰 체크리스트)

### CLEAR 원칙

- [ ] **Concise (간결성)**
  - 함수가 한 가지 일만 하는가?
  - 불필요한 코드가 없는가?
  - 중복이 제거되었는가?

- [ ] **Logical (논리성)**
  - 코드 흐름이 명확한가?
  - 조건문 로직이 이해하기 쉬운가?
  - 부작용(side effect)이 명시적인가?

- [ ] **Explicit (명시성)**
  - 변수명이 의도를 명확히 나타내는가?
  - 매직 넘버/문자열이 없는가?
  - 주석이 필요한 복잡한 로직은 없는가?

- [ ] **Adaptive (적응성)**
  - 요구사항 변경 시 수정이 용이한가?
  - 의존성이 추상화되어 있는가?
  - 확장 가능한 구조인가?

- [ ] **Reflective (성찰성)**
  - 테스트가 충분한가? (커버리지 >90%)
  - 변이 테스트를 통과하는가? (변이 점수 >80%)
  - 피드백을 반영할 방법이 있는가?

### TDD 원칙

- [ ] **Red-Green-Refactor 순서 준수**
  - 테스트를 먼저 작성했는가?
  - 최소 구현으로 통과시켰는가?
  - 리팩토링 후에도 테스트가 통과하는가?

- [ ] **테스트 품질**
  - Given-When-Then 구조를 따르는가?
  - 테스트가 독립적인가? (순서 무관)
  - 테스트 이름이 명확한가?

- [ ] **변이 테스트**
  - 변이 점수 >80%를 달성했는가?
  - 살아남은 변이를 분석했는가?

---

## ⚠️ Issues & Blockers (이슈 및 블로커)

### 현재 이슈

#### Issue #1: [이슈 제목]
- **설명:** [문제 상세]
- **발견 시점:** [Red | Green | Refactor | Mutation]
- **영향도:** Critical | High | Medium | Low
- **상태:** Open | In Progress | Resolved
- **해결 방법:** [해결 방법]

### 블로커

- **있음:** [블로커 상세]
  - 원인: [무엇이 막고 있는가?]
  - 해결 방법: [어떻게 해결?]
  - 예상 해결 시간: [시간]

- **없음:** 정상 진행 중

---

## 🎓 Lessons Learned (교훈)

### ✅ 잘한 점
- [잘한 점 1]
- [잘한 점 2]

### ⚠️ 개선 필요
- [개선점 1]
  - 원인: [근본 원인]
  - 다음 Task 적용: [어떻게 개선?]

### 💡 발견한 패턴
- [패턴 1]: [설명]
- [패턴 2]: [설명]

---

## ✅ Task Completion Criteria (완료 기준)

### TDD 사이클 완료
- [ ] Red: 테스트 작성 및 실패 확인
- [ ] Green: 최소 구현으로 테스트 통과
- [ ] Refactor: 코드 품질 개선
- [ ] Mutation: 변이 점수 >80%

### 품질 기준
- [ ] 모든 Unit Test 통과 (100%)
- [ ] 테스트 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] Cyclomatic Complexity <10
- [ ] 중복 코드 0%
- [ ] ESLint/Prettier 규칙 통과

### 문서화
- [ ] 코드 주석 작성 (JSDoc)
- [ ] README 업데이트 (필요시)
- [ ] 이 Task 문서 완성

### 리뷰
- [ ] 코드 리뷰 완료 (최소 1명)
- [ ] CLEAR 원칙 체크 완료
- [ ] TDD 원칙 준수 확인

---

## 📝 Code Example (코드 예시)

### 최종 코드

```typescript
// src/[feature]/[task-name].ts

/**
 * [기능 설명]
 *
 * @example
 * const result = functionName({ field1: 'test', field2: 42 });
 * console.log(result.status); // 'success'
 *
 * @param input - [입력 설명]
 * @returns [출력 설명]
 * @throws {TaskError} [에러 조건]
 */
export function functionName(input: TaskInput): TaskOutput {
  // Input validation
  validateInput(input);

  // Core logic
  const processed = processInput(input);

  // Return result
  return {
    result: processed.value,
    status: 'success',
    metadata: {
      timestamp: Date.now(),
    },
  };
}

// Helper functions (private)
function validateInput(input: TaskInput): void {
  if (!input.field1) {
    throw new TaskError('field1 is required', 'INVALID_INPUT');
  }
  if (typeof input.field2 !== 'number') {
    throw new TaskError('field2 must be a number', 'INVALID_INPUT');
  }
}

function processInput(input: TaskInput): ProcessedData {
  // Implementation
  return {
    value: `${input.field1}-${input.field2}`,
  };
}
```

### 최종 테스트

```typescript
// tests/[feature]/[task-name].test.ts

describe('Task: [작업명]', () => {
  describe('정상 동작', () => {
    it('should process valid input successfully', () => {
      const input = { field1: 'test', field2: 42 };
      const result = functionName(input);

      expect(result.status).toBe('success');
      expect(result.result).toBe('test-42');
    });
  });

  describe('에러 처리', () => {
    it('should throw error when field1 is missing', () => {
      expect(() => {
        functionName({ field1: '', field2: 42 });
      }).toThrow('field1 is required');
    });

    it('should throw error when field2 is not a number', () => {
      expect(() => {
        functionName({ field1: 'test', field2: 'invalid' as any });
      }).toThrow('field2 must be a number');
    });
  });

  describe('엣지 케이스', () => {
    it('should handle optional field3', () => {
      const input = { field1: 'test', field2: 42, field3: true };
      const result = functionName(input);

      expect(result.status).toBe('success');
    });
  });
});
```

---

## 💡 Notes (참고 사항)

### CLEAR 원칙 체크
- [ ] **Concise**: 함수가 간결하고 한 가지 일만 함
- [ ] **Logical**: 코드 흐름이 논리적이고 순차적
- [ ] **Explicit**: 의도가 명확하게 드러남
- [ ] **Adaptive**: 변경이 용이한 구조
- [ ] **Reflective**: 테스트로 지속적 검증

### 계층적 TDD 매핑
- **이 문서는 "작은단위 (Task)" 레벨입니다.**
- 상위 계층: [[Feature_[N]_기능명]] (중단위 레벨)
- 프랙탈 TDD: 작은단위 Unit Test → 중단위 Integration Test
- **가장 작은 TDD 사이클:** Red-Green-Refactor-Mutation

### 작업 시간 가이드
- **Red (15분)**: 테스트 작성
- **Green (30분)**: 최소 구현
- **Refactor (30분)**: 품질 개선
- **Mutation (15분)**: 테스트 품질 검증
- **총 90분 (1.5시간)**: 표준 Task 시간

### 다음 Task 연결
- **Feature 내 순서:** Task 1 → Task 2 → ... → Task 5
- **Task 5 완료 후:** Feature Integration Test로 이동

---

**최종 업데이트:** YYYY-MM-DD HH:MM
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**다음 Task:** [[Task_[N+1]_작업명]]

---

## 📚 버전 이력

### v1.1 (2025-11-08)
**변경 사항:**
1. **🤖 AI 작성 가이드** 섹션 추가
   - 역할 분담 패러다임 명시 (개발자 5% vs AI 95%)
   - Red-Green-Refactor-Mutation 90분 표준 워크플로우 추가
   - 개발자 역할 명확화 (작업 전 5분, 작업 후 5분)
   - Task 레벨의 핵심 강조 (최하위 레벨, Unit Test, 프랙탈 TDD 실행 단위)
2. **작성자 필드 변경**: "AI (Claude Code) - 개발자 검토 후 승인"
3. [[../CJ_AI_개발방법론|CJ_AI_개발방법론]] 마스터 문서와 일관성 확보

**목적:** "인간은 코드를 안 봐도 된다" 패러다임을 템플릿에 반영

### v1.0 (초기 버전)
- 기본 Task 템플릿 구조 정의
- TDD 4단계 사이클 (Red-Green-Refactor-Mutation) 상세 가이드
- 품질 지표 및 완료 기준 명시
