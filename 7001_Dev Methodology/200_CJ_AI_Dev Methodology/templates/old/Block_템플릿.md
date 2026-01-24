## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [[./Product_PRD_템플릿|Product PRD 템플릿]] - 제품 레벨 (상위)
- [[./Feature_템플릿|Feature 템플릿]] - 중단위 레벨 (하위)
- [[./Task_템플릿|Task 템플릿]] - 작은단위 레벨
- [[../계층적_TDD_가이드|계층적 TDD 가이드]]

---

# Block: [블럭명]

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**상태:** 초안 | 진행 중 | 완료

**소속 제품:** [[Product_PRD|제품명]]
**Goal 참조:** [[Product_PRD#Goal-N]]

---

## 🤖 AI 작성 가이드

> **역할 분담:** "인간은 코드를 안 봐도 된다"
> - **개발자 (5%)**: Block 설계 검토 → 피드백 → Feature 단위 진행 확인 (문서로)
> - **AI (95%)**: 이 문서 작성 → 3 Features 분해 → 15 Tasks 구현 → Module Test

**AI가 이 문서를 작성하는 방법:**
1. **Product_PRD.md 읽기**: 이 Block이 제품에서 담당할 역할 파악
2. **Block_템플릿.md 읽기**: 이 템플릿 구조 파악
3. **블럭 설계**: 3개 Feature로 분해 (비즈니스 임팩트 중심)
4. **아키텍처 설계**: SOLID 원칙 적용, Feature 간 의존성 정의
5. **개발자 검토**: 문서를 개발자에게 제시
6. **승인 후**: Feature_템플릿.md로 이동하여 각 Feature 상세 설계

**개발자는:**
- ✅ Block 설계 문서만 검토 (코드 안 봄)
- ✅ Feature 단위 완료 시 결과 확인 (Feature.md + Integration Test 결과)
- ✅ Block 전체 완료 시 Module Test 결과 확인

**AI 작업 흐름 (Block 레벨):**
```
Day 1: Block 설계 (이 문서 작성) → 개발자 검토 → 승인
Day 2-3: Feature 1 설계 + 구현 (5 Tasks TDD)
Day 4-5: Feature 2 설계 + 구현 (5 Tasks TDD)
Day 6-7: Feature 3 설계 + 구현 (5 Tasks TDD)
Day 8-9: Block 통합 (Module Test) + Refactor
```

---

## 📋 계층 정보

```
제품 (Product): [제품명]
  └─ 🎯 블럭 [N]: [이 블럭]  ← 현재 레벨
       ├─ 중단위 1: [Feature 1]
       │    ├─ 작은단위 1-1: [Task]
       │    ├─ 작은단위 1-2: [Task]
       │    ├─ 작은단위 1-3: [Task]
       │    ├─ 작은단위 1-4: [Task]
       │    └─ 작은단위 1-5: [Task]
       │
       ├─ 중단위 2: [Feature 2]
       │    ├─ 작은단위 2-1: [Task]
       │    ├─ 작은단위 2-2: [Task]
       │    ├─ 작은단위 2-3: [Task]
       │    ├─ 작은단위 2-4: [Task]
       │    └─ 작은단위 2-5: [Task]
       │
       └─ 중단위 3: [Feature 3]
            ├─ 작은단위 3-1: [Task]
            ├─ 작은단위 3-2: [Task]
            ├─ 작은단위 3-3: [Task]
            ├─ 작은단위 3-4: [Task]
            └─ 작은단위 3-5: [Task]

총: 1 블럭 = 3 중단위 = 15 작은단위
```

**이 블럭의 역할:**
- [한 문장으로: 이 블럭이 제품에서 담당하는 핵심 역할]

---

## 🎯 Block Definition (블럭 정의)

### 한 문장 요약
> [이 블럭을 한 문장으로 요약]

### 블럭 목표
**핵심 가치:**
- [이 블럭이 제공하는 핵심 가치 1]
- [이 블럭이 제공하는 핵심 가치 2]
- [이 블럭이 제공하는 핵심 가치 3]

**비즈니스 임팩트:**
- [비즈니스 지표 1]: [목표 값]
- [비즈니스 지표 2]: [목표 값]
- [비즈니스 지표 3]: [목표 값]

### 범위 (Scope)
**포함 (In Scope):**
- [포함 항목 1]
- [포함 항목 2]
- [포함 항목 3]

**제외 (Out of Scope):**
- [제외 항목 1] - [이유]
- [제외 항목 2] - [이유]

---

## 🏗️ Architecture (블럭 아키텍처)

### 시스템 구조

```mermaid
graph TB
    subgraph "Block: [블럭명]"
        F1[Feature 1:<br/>[기능명]]
        F2[Feature 2:<br/>[기능명]]
        F3[Feature 3:<br/>[기능명]]
    end

    subgraph "외부 시스템"
        EXT1[External System 1]
        EXT2[External System 2]
    end

    F1 --> F2
    F2 --> F3
    F1 -.optional.-> F3

    F1 --> EXT1
    F3 --> EXT2

    style F1 fill:#e1f5ff
    style F2 fill:#fff4e1
    style F3 fill:#f0ffe1
```

### 모듈 설계 원칙

**SOLID 원칙 적용:**
- **S**RP: 각 Feature는 단일 책임
- **O**CP: Feature 확장 가능, 수정 불필요
- **L**SP: Feature 간 인터페이스 일관성
- **I**SP: Feature 간 최소한의 인터페이스
- **D**IP: Feature는 추상화에 의존

**의존성 방향:**
```
Feature 3 (최상위)
  ↓ depends on
Feature 2 (중간)
  ↓ depends on
Feature 1 (기반)
```

---

## 🧩 Feature Breakdown (중단위 분할)

> **중요:** 이 블럭은 **3개 중단위 (Feature)**로 구성됩니다.
> 각 중단위는 5개 작은단위로 구성되며, 하나의 User Story를 구현합니다.

### Feature 1: [기능명] (기반 기능)

**User Story:**
```
As a [역할]
I want [기능]
So that [목표]
```

**핵심 책임:**
- [책임 1]
- [책임 2]
- [책임 3]

**인터페이스:**
```typescript
interface Feature1Interface {
  execute(input: Input1): Promise<Output1>;
  validate(data: Data1): ValidationResult;
}
```

**Task 구성:** (5개)
1. Task 1-1: [작업명] (1-2h)
2. Task 1-2: [작업명] (1-2h)
3. Task 1-3: [작업명] (1-2h)
4. Task 1-4: [작업명] (1-2h)
5. Task 1-5: [작업명] (1-2h)

**예상 시간:** 5-10시간

**의존성:**
- 선행 Feature: 없음
- 후행 Feature: Feature 2, Feature 3

**문서:** [[Feature_01_기능명]]

---

### Feature 2: [기능명] (핵심 기능)

**User Story:**
```
As a [역할]
I want [기능]
So that [목표]
```

**핵심 책임:**
- [책임 1]
- [책임 2]
- [책임 3]

**인터페이스:**
```typescript
interface Feature2Interface {
  execute(input: Input2): Promise<Output2>;
  // Feature 1의 Output1을 사용
  process(output1: Output1): Promise<Output2>;
}
```

**Task 구성:** (5개)
1. Task 2-1: [작업명] (1-2h)
2. Task 2-2: [작업명] (1-2h)
3. Task 2-3: [작업명] (1-2h)
4. Task 2-4: [작업명] (1-2h)
5. Task 2-5: [작업명] (1-2h)

**예상 시간:** 5-10시간

**의존성:**
- 선행 Feature: Feature 1
- 후행 Feature: Feature 3

**문서:** [[Feature_02_기능명]]

---

### Feature 3: [기능명] (고급 기능)

**User Story:**
```
As a [역할]
I want [기능]
So that [목표]
```

**핵심 책임:**
- [책임 1]
- [책임 2]
- [책임 3]

**인터페이스:**
```typescript
interface Feature3Interface {
  execute(input: Input3): Promise<Output3>;
  // Feature 1, 2의 출력을 통합
  integrate(output1: Output1, output2: Output2): Promise<Output3>;
}
```

**Task 구성:** (5개)
1. Task 3-1: [작업명] (1-2h)
2. Task 3-2: [작업명] (1-2h)
3. Task 3-3: [작업명] (1-2h)
4. Task 3-4: [작업명] (1-2h)
5. Task 3-5: [작업명] (1-2h)

**예상 시간:** 5-10시간

**의존성:**
- 선행 Feature: Feature 1, Feature 2
- 후행 Feature: 없음 (Block 통합)

**문서:** [[Feature_03_기능명]]

---

## 🧪 Block-Level TDD (블럭 모듈 테스트)

> **프랙탈 TDD:** Feature에서 Integration Test를 했다면,
> 블럭에서는 **3개 Feature가 통합된 모듈 전체의 동작을 테스트**합니다.

### Red: Block Module Test 작성

**테스트 시나리오:**
```typescript
describe('Block: [블럭명]', () => {
  describe('모듈 통합 시나리오 1: [전체 블럭 동작]', () => {
    it('should [블럭 전체가 정상 동작]', async () => {
      // Given: 3개 Feature가 모두 완료된 상태
      const blockContext = setupBlockContext();

      // When: Block 전체를 실행
      const result = await executeBlock(blockContext, {
        // Block input
      });

      // Then: Block 목표 달성
      expect(result.businessImpact1).toBeGreaterThan(targetValue1);
      expect(result.businessImpact2).toBeGreaterThan(targetValue2);
      expect(result.businessImpact3).toBeGreaterThan(targetValue3);
    });
  });

  describe('모듈 통합 시나리오 2: [Feature 간 연동]', () => {
    it('should [Feature 1 → Feature 2 → Feature 3 데이터 흐름]', async () => {
      // Given
      const input = createTestInput();

      // When
      const feature1Output = await feature1.execute(input);
      const feature2Output = await feature2.process(feature1Output);
      const feature3Output = await feature3.integrate(feature1Output, feature2Output);

      // Then
      expect(feature3Output).toMatchBlockGoals();
    });
  });

  describe('모듈 통합 시나리오 3: [에러 전파]', () => {
    it('should [Feature 에러가 Block 레벨에서 올바르게 처리됨]', async () => {
      // Error propagation test
    });
  });

  describe('모듈 성능 테스트', () => {
    it('should [Block 전체가 성능 목표 달성]', async () => {
      const startTime = Date.now();

      await executeBlock(largeInput);

      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(performanceTarget);
    });
  });
});
```

**실행 결과 (Red):**
```bash
❌ FAIL: Block: [블럭명]
  - Feature 01-03 미완성
  - Block 통합 로직 미구현
```

---

### Green: 3개 Feature 구현

**구현 순서:**

```
1. Feature 1 완료 (5개 Task TDD) ✅
   └─ Feature 1 Integration Test 통과

2. Feature 2 완료 (5개 Task TDD) ✅
   └─ Feature 2 Integration Test 통과
   └─ Feature 1 → Feature 2 연동 확인

3. Feature 3 완료 (5개 Task TDD) ✅
   └─ Feature 3 Integration Test 통과
   └─ Feature 1,2 → Feature 3 통합 확인

4. Block 통합 함수 구현 ✅
   └─ 3개 Feature를 조율
```

**Block 통합 코드 예시:**
```typescript
// block/[블럭명]/index.ts
export class [블럭명]Block {
  constructor(
    private feature1: Feature1Interface,
    private feature2: Feature2Interface,
    private feature3: Feature3Interface
  ) {}

  async execute(input: BlockInput): Promise<BlockOutput> {
    // Feature 1: 기반 처리
    const feature1Result = await this.feature1.execute(input.part1);

    // Feature 2: 핵심 처리 (Feature 1 결과 활용)
    const feature2Result = await this.feature2.process(feature1Result);

    // Feature 3: 통합 처리 (Feature 1, 2 결과 통합)
    const feature3Result = await this.feature3.integrate(
      feature1Result,
      feature2Result
    );

    return {
      businessImpact1: this.calculateImpact1(feature3Result),
      businessImpact2: this.calculateImpact2(feature3Result),
      businessImpact3: this.calculateImpact3(feature3Result),
    };
  }

  // Block 레벨 에러 핸들링
  private handleBlockError(error: Error, context: Context): BlockError {
    // 어떤 Feature에서 에러가 발생했는지 추적
    // Block 레벨 복구 전략 적용
    return new BlockError(error, context);
  }
}
```

**실행 결과 (Green):**
```bash
✅ PASS: Block: [블럭명]
  - 모든 모듈 테스트 통과
  - Feature 01-03 통합 성공
  - 성능 목표 달성
```

---

### Refactor: Block 레벨 리팩토링

**리팩토링 포인트:**
- [ ] **Feature 간 중복 제거**
  - [공통 로직 식별]
  - [공통 모듈 추출]

- [ ] **아키텍처 패턴 적용**
  - [적용할 패턴: Strategy | Factory | Observer | ...]
  - [패턴 적용 위치]

- [ ] **성능 최적화**
  - [병렬 처리 가능한 Feature 식별]
  - [캐싱 전략]
  - [리소스 풀링]

- [ ] **에러 처리 강화**
  - [Feature 에러 → Block 에러 매핑]
  - [복구 전략 구현]
  - [로깅 및 모니터링]

**리팩토링 후 검증:**
```bash
✅ PASS: 모든 테스트 통과 유지
✅ PASS: 성능 20% 향상 (Before: [N]ms → After: [M]ms)
✅ PASS: 코드 중복 50% 감소
✅ PASS: 복잡도 감소 (Before: [N] → After: [M])
```

---

### Mutation: Block 모듈 테스트 품질 검증

**변이 테스트 실행:**
```bash
npm run test:mutation -- block/[블럭명]
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

## 📊 Block Metrics (블럭 메트릭)

### 품질 지표

| 지표 | 목표 | 현재 | 상태 |
|------|------|------|------|
| Feature 완료율 | 3/3 | [N]/3 | [진행률]% |
| Unit Test 커버리지 | >90% | [%] | ✅/⚠️/❌ |
| Integration Test 커버리지 | >80% | [%] | ✅/⚠️/❌ |
| Module Test 커버리지 | >75% | [%] | ✅/⚠️/❌ |
| 변이 점수 (Block 레벨) | >80% | [%] | ✅/⚠️/❌ |
| 평균 복잡도 | <10 | [N] | ✅/⚠️/❌ |
| 성능 (Block 전체) | <[목표]ms | [실제]ms | ✅/⚠️/❌ |

### 진행 상황

```
Feature 1: ✅ 완료 (5/5 Task, 실제: 8h, 예상: 7.5h)
Feature 2: ✅ 완료 (5/5 Task, 실제: 9h, 예상: 7.5h)
Feature 3: 🚧 진행 중 (3/5 Task, 60%)

전체 진행률: 86% (13/15 Task)
예상 완료: [날짜] (현재 기준 +2일)
```

### 비즈니스 임팩트 추적

| 지표 | 목표 | 현재 | 달성률 |
|------|------|------|--------|
| [비즈니스 지표 1] | [목표] | [현재] | [%] |
| [비즈니스 지표 2] | [목표] | [현재] | [%] |
| [비즈니스 지표 3] | [목표] | [현재] | [%] |

---

## 🔗 Dependencies (의존성)

### 선행 블럭
- [[Block_[N-1]_블럭명]] - [의존 관계 설명]

### 후행 블럭
- [[Block_[N+1]_블럭명]] - [의존 관계 설명]

### 외부 시스템 의존성
- **시스템 A:** [연동 내용] - [담당자]
- **시스템 B:** [연동 내용] - [담당자]

### 공유 라이브러리
- **라이브러리 A:** [버전] - [사용 이유]
- **라이브러리 B:** [버전] - [사용 이유]

---

## ⚠️ Risks & Issues (리스크 및 이슈)

### 현재 리스크

#### 리스크 1: [리스크 설명]
- **영향도:** 높음 | 중간 | 낮음
- **발생 확률:** 높음 | 중간 | 낮음
- **영향 Feature:** Feature [N]
- **완화 전략:** [대응 방법]
- **담당자:** [이름]
- **상태:** Monitoring | Mitigating | Resolved

### 발생한 이슈

#### Issue #1: [이슈 제목]
- **설명:** [문제 상세]
- **영향 Feature:** Feature [N]
- **발견일:** YYYY-MM-DD
- **우선순위:** Critical | High | Medium | Low
- **상태:** Open | In Progress | Resolved
- **해결 방법:** [해결 방법]
- **해결일:** YYYY-MM-DD

---

## 📝 Weekly Progress (주간 진행 기록)

### Week [N] (YYYY-MM-DD ~ YYYY-MM-DD)

**완료 Feature:**
- ✅ Feature 1 (5 Task)
- ✅ Feature 2 (5 Task)

**진행 중:**
- 🚧 Feature 3 (3/5 Task)

**다음 주 계획:**
- [ ] Feature 3 완료 (2 Task 남음)
- [ ] Block 통합 테스트
- [ ] Block 리팩토링

**블로커:**
- 없음 | [블로커 내용]

**주간 통계:**
- 완료 Task: 13/15 (86%)
- 평균 Task 소요 시간: [시간] (예상: 1.5h)
- 시간 예측 정확도: [%]

---

## ✅ Block Completion Criteria (완료 기준)

### Feature 완료
- [ ] Feature 1: Integration Test 통과 + 변이 점수 >80%
- [ ] Feature 2: Integration Test 통과 + 변이 점수 >80%
- [ ] Feature 3: Integration Test 통과 + 변이 점수 >80%

### Block 통합 완료
- [ ] Block Module Test 통과
- [ ] Block 레벨 변이 점수 >80%
- [ ] Feature 간 연동 검증 완료
- [ ] 성능 목표 달성 (<[목표]ms)
- [ ] 코드 리뷰 완료 (최소 2명)

### 품질 검증
- [ ] Unit Test 커버리지 >90%
- [ ] Integration Test 커버리지 >80%
- [ ] Module Test 커버리지 >75%
- [ ] 복잡도 평균 <10
- [ ] 보안 검토 완료
- [ ] 문서 완성

### 비즈니스 검증
- [ ] 비즈니스 지표 1 달성
- [ ] 비즈니스 지표 2 달성
- [ ] 비즈니스 지표 3 달성

---

## 🎓 Lessons Learned (교훈)

### ✅ 잘한 점
- [잘한 점 1]
- [잘한 점 2]
- [잘한 점 3]

### ⚠️ 개선 필요
- [개선점 1]
  - 원인: [근본 원인]
  - 개선 방법: [다음 Block에 적용할 방법]

- [개선점 2]
  - 원인: [근본 원인]
  - 개선 방법: [다음 Block에 적용할 방법]

### 💡 다음 Block에 적용
- [적용 사항 1]
- [적용 사항 2]

---

## 🔍 Architecture Review (아키텍처 리뷰)

**리뷰어:** [이름]
**리뷰일:** YYYY-MM-DD

### 아키텍처 원칙 체크
- [ ] **모듈 독립성**: 각 Feature가 독립적으로 동작 가능
- [ ] **인터페이스 명확성**: Feature 간 계약이 명확
- [ ] **의존성 방향**: 상위 Feature가 하위 Feature에 의존
- [ ] **확장성**: 새로운 Feature 추가 용이
- [ ] **테스트 가능성**: 각 Feature를 독립적으로 테스트 가능

### 설계 패턴 적용
- [ ] [패턴 1]: [적용 위치] - [적절성 평가]
- [ ] [패턴 2]: [적용 위치] - [적절성 평가]

### 개선 제안
- [제안 1]
- [제안 2]

---

## 📊 Final Report (최종 보고)

> **Block 완료 시 작성**

### 완료 요약
**완료일:** YYYY-MM-DD
**총 소요 시간:** [실제]시간 (예상: [예상]시간)
**시간 편차:** +[N]시간 | -[N]시간 | 정확

### 최종 메트릭

| 지표 | 목표 | 달성 | 평가 |
|------|------|------|------|
| Feature 완료율 | 3/3 | [N]/3 | ✅/❌ |
| Unit Test 커버리지 | >90% | [%] | ✅/❌ |
| Integration Test 커버리지 | >80% | [%] | ✅/❌ |
| Module Test 커버리지 | >75% | [%] | ✅/❌ |
| 변이 점수 | >80% | [%] | ✅/❌ |
| 복잡도 평균 | <10 | [N] | ✅/❌ |
| 성능 | <[목표]ms | [실제]ms | ✅/❌ |

### 비즈니스 임팩트 달성도
- ✅ [비즈니스 지표 1]: [목표] → [달성]
- ✅ [비즈니스 지표 2]: [목표] → [달성]
- ⚠️ [비즈니스 지표 3]: [목표] → [달성] (부분 달성, 이유: [설명])

### 아키텍처 결정 회고
**주요 아키텍처 결정:**
1. **[결정 1]**
   - 선택: [선택한 방법]
   - 결과: [효과적이었는가?]
   - 교훈: [다음에 적용할 점]

2. **[결정 2]**
   - 선택: [선택한 방법]
   - 결과: [효과적이었는가?]
   - 교훈: [다음에 적용할 점]

### 핵심 교훈
1. **[교훈 1]**
   - 상황: [어떤 상황?]
   - 학습: [무엇을 배웠나?]
   - 적용: [다음 Block에 어떻게 적용?]

---

## 💡 Notes (참고 사항)

### CLEAR 원칙 체크
- [ ] **Concise**: 3개 Feature로 명확히 분할
- [ ] **Logical**: Feature 의존성이 논리적
- [ ] **Explicit**: 각 Feature의 역할과 인터페이스가 명시적
- [ ] **Adaptive**: Feature 단위 교체/확장 가능
- [ ] **Reflective**: Block 레벨 회고 및 아키텍처 개선

### 계층적 TDD 매핑
- **이 문서는 "블럭 (Block)" 레벨입니다.**
- 상위 계층: [[Product_PRD]] (제품 레벨)
- 하위 계층: [[Feature_01]], [[Feature_02]], [[Feature_03]] (중단위 레벨)
- 프랙탈 TDD: Feature Integration Test → Block Module Test

### 업데이트 주기
- **주간:** Weekly Progress 작성
- **Feature 완료 시:** 해당 Feature 섹션 업데이트
- **Block 완료 시:** Final Report 작성

---

**최종 업데이트:** YYYY-MM-DD HH:MM
**작성자:** [이름]
**다음 Block:** [[Block_[N+1]_블럭명]]
