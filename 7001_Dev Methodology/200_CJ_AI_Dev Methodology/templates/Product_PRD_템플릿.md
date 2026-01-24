## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]] - 전체 방법론 (이론은 여기 참조)
- [[./Block_템플릿_통합|Block 템플릿 (통합)]] - Block + Feature + Task 통합 템플릿 (하위, 실무용)
- [[../계층적_TDD_가이드|계층적 TDD 가이드]]

---

# Product PRD: [제품명]

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.1
**상태:** 초안 | 검토 중 | 승인됨

---

## 🤖 AI 작성 가이드

> **역할 분담:** "인간은 코드를 안 봐도 된다"
> - **개발자 (5%)**: 아이디어 제공 → 이 문서 검토 → 피드백 → 승인
> - **AI (95%)**: 이 문서 작성 → 3 Blocks 분해 → 9 Features 분해 → 45 Tasks 분해 → 코드 구현

**AI가 이 문서를 작성하는 방법:**
1. **개발자 프롬프트 분석**: "할일 관리 앱 만들어줘" 등 아이디어 추출
2. **Product_PRD_템플릿.md 읽기**: 이 템플릿 구조 파악
3. **문서 작성**: 템플릿을 채워서 실제 PRD 생성
4. **계층 분해**: 3 Blocks → 9 Features → 45 Tasks로 자동 분해
5. **개발자 검토**: 문서를 개발자에게 제시
6. **피드백 반영**: 개발자 피드백 받아 수정
7. **승인 후**: [[Block_템플릿_통합|Block_템플릿_통합.md]]로 이동하여 각 Block 개발 시작

**개발자는:**
- ✅ 이 문서만 읽고 검토 (코드 안 봄)
- ✅ Success Metrics 달성 여부만 확인 (E2E Test 결과로)
- ✅ 아이디어와 피드백만 제공

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 작성 (이 문서)
        ↓
단계 2: Block 1-3 정의 (Block_템플릿_통합.md)
        ↓
단계 3: Block 1 개발 (Feature 1-3, Task 1-5 각각)
        ↓  (피라미드: Task → Feature Integration → Block Module)
단계 4: Block 2 개발 (동일)
        ↓
단계 5: Block 3 개발 (동일)
        ↓
단계 6: ✅ Product E2E TDD 작성 ⬆️
        (Block 3개 결과 참고 + PRD Success Metrics 싱크)
```

**중요:**
- Block은 **Feature 3개 Integration TDD + Block Module TDD 모두 완료 후** 체크
- Product E2E TDD는 **Block 3개 모두 완료 후** 작성 (Block 개발 중 작성 ❌)
- PRD Success Metrics 싱크는 E2E TDD 작성 시 필수

---

## 📋 계층 구조

```
🎯 제품 (Product): [제품명]  ← 현재 레벨
  ├─ 블럭 1: [블럭명]
  │    ├─ 중단위 1-1: [Feature명]
  │    │    ├─ 작은단위 1-1-1: [Task]
  │    │    ├─ 작은단위 1-1-2: [Task]
  │    │    ├─ 작은단위 1-1-3: [Task]
  │    │    ├─ 작은단위 1-1-4: [Task]
  │    │    └─ 작은단위 1-1-5: [Task]
  │    ├─ 중단위 1-2: [Feature명] (5 Task)
  │    └─ 중단위 1-3: [Feature명] (5 Task)
  │
  ├─ 블럭 2: [블럭명]
  │    ├─ 중단위 2-1: [Feature명] (5 Task)
  │    ├─ 중단위 2-2: [Feature명] (5 Task)
  │    └─ 중단위 2-3: [Feature명] (5 Task)
  │
  └─ 블럭 3: [블럭명]
       ├─ 중단위 3-1: [Feature명] (5 Task)
       ├─ 중단위 3-2: [Feature명] (5 Task)
       └─ 중단위 3-3: [Feature명] (5 Task)

총: 1 제품 = 3 블럭 = 9 중단위 = 45 작은단위
```

**권장 구조:**
- 1개 제품 = 3개 블럭
- 1개 블럭 = 3개 중단위 (Feature)
- 1개 중단위 = 5개 작은단위 (Task)
- 1개 작은단위 = 1-2시간 작업

---

## 📋 Overview (개요)

### 한 문장 요약
> [이 프로젝트를 한 문장으로 요약하세요]

### 배경 및 동기
**문제:**
- [해결하려는 핵심 문제가 무엇인가?]
- [현재 어떤 어려움이 있는가?]

**기회:**
- [이 프로젝트가 제공할 가치는?]
- [비즈니스 임팩트는?]

### 목표 사용자
- **주 사용자:** [사용자 페르소나]
- **부 사용자:** [추가 사용자]

---

## 🎯 Goals & Non-Goals (범위)

### ✅ Goals (할 것)

**핵심 기능 (Must-Have):**
1. [기능 1] - [간단한 설명]
2. [기능 2] - [간단한 설명]
3. [기능 3] - [간단한 설명]

**부가 기능 (Nice-to-Have):**
- [기능 A] - [간단한 설명]
- [기능 B] - [간단한 설명]

### ❌ Non-Goals (하지 않을 것)

**명시적 제외 항목:**
- [제외 1] - [제외 이유]
- [제외 2] - [제외 이유]

**향후 고려 사항:**
- [미래 버전에서 고려할 항목]

---

## 📖 User Stories (사용자 스토리)

### Story 1: [스토리 제목]
```
As a [역할]
I want [기능]
So that [혜택/이유]
```

**수용 기준:**
- [ ] [기준 1]
- [ ] [기준 2]
- [ ] [기준 3]

**우선순위:** 높음 | 중간 | 낮음

---

### Story 2: [스토리 제목]
```
As a [역할]
I want [기능]
So that [혜택/이유]
```

**수용 기준:**
- [ ] [기준 1]
- [ ] [기준 2]

**우선순위:** 높음 | 중간 | 낮음

---

### Story 3: [스토리 제목]
```
As a [역할]
I want [기능]
So that [혜택/이유]
```

**수용 기준:**
- [ ] [기준 1]
- [ ] [기준 2]

**우선순위:** 높음 | 중간 | 낮음

---

## 📊 Success Metrics (성공 지표)

### 정량적 목표

| 지표 | 목표 | 측정 방법 | 기준일 |
|------|------|----------|--------|
| [지표 1] | [목표 값] | [어떻게 측정?] | [언제까지?] |
| [지표 2] | [목표 값] | [어떻게 측정?] | [언제까지?] |
| [지표 3] | [목표 값] | [어떻게 측정?] | [언제까지?] |

### 정성적 목표
- [목표 1]
- [목표 2]

### 완료 기준 (Definition of Done)
- [ ] 모든 User Story의 수용 기준 충족
- [ ] 정량적 목표 달성
- [ ] [추가 기준 1]
- [ ] [추가 기준 2]

---

## 🤖 AI 인프라 체크리스트

> **상세 내용**: [[../doc/연구자료_AI코드생성인프라_20251108|AI 코드 생성 인프라 연구자료]] 참조
>
> **핵심 철학:** "인간은 문서만, AI는 문서+그래프+코드 모두"

### 3가지 핵심 인프라

AI가 효율적으로 작업하기 위해 필요한 최소한의 인프라:

**1. 계층적 RAG 스택**
- [ ] 코드를 3계층(구조·로직·상세)으로 자동 청킹
- [ ] 벡터 DB 연동 (Pinecone/Weaviate)
- [ ] 쿼리 유형별 계층 선택 라우터

**2. 최소 컨텍스트 원칙**
- [ ] 파일당 200줄 이하 강제 (ESLint)
- [ ] 함수당 50줄 이하 강제
- [ ] 의존성 명시화 (`@requires` 주석)

**3. 문서-코드 동기화**
- [ ] Obsidian 문서 → 코드 자동 생성
- [ ] git commit → 문서 자동 업데이트
- [ ] 문서-코드 불일치 검출 (CI/CD)

**구현 우선순위:**
- **Phase 1 (필수)**: 문서-코드 동기화 (AI가 이 PRD 읽고 코드 생성)
- **Phase 2 (권장)**: 최소 컨텍스트 린트 규칙
- **Phase 3 (선택)**: 계층적 RAG 스택 (팀 규모 5명+ 시)

---

## 🚧 Constraints (제약 조건)

### 기술적 제약
- **기술 스택:** [사용 기술/프레임워크]
- **성능:** [응답시간, 처리량 등]
- **호환성:** [브라우저, 디바이스, OS]
- **보안:** [보안 요구사항]

### 비즈니스 제약
- **예산:** [예산 범위]
- **일정:** [마감 기한]
- **리소스:** [팀 크기, 역할]

### 외부 의존성
- [의존하는 외부 시스템/API]
- [의존하는 팀/부서]

---

## ⚠️ Risks (리스크)

### 높은 리스크 (High)

**리스크 1:** [리스크 설명]
- **영향:** [무엇이 문제가 되는가?]
- **확률:** 높음 | 중간 | 낮음
- **완화 계획:** [어떻게 대응할 것인가?]

### 중간 리스크 (Medium)

**리스크 2:** [리스크 설명]
- **영향:** [무엇이 문제가 되는가?]
- **확률:** 높음 | 중간 | 낮음
- **완화 계획:** [어떻게 대응할 것인가?]

### 낮은 리스크 (Low)

**리스크 3:** [리스크 설명]
- **영향:** [무엇이 문제가 되는가?]
- **확률:** 높음 | 중간 | 낮음
- **완화 계획:** [어떻게 대응할 것인가?]

---

## 📅 Timeline (일정)

| 마일스톤 | 완료 기준 | 예상 일정 | 담당자 |
|---------|---------|----------|--------|
| 요구사항 확정 | PRD 승인 | [날짜] | [이름] |
| 블럭 1 완료 | 3 Feature 완료 | [날짜] | [이름] |
| 블럭 2 완료 | 3 Feature 완료 | [날짜] | [이름] |
| 블럭 3 완료 | 3 Feature 완료 | [날짜] | [이름] |
| E2E 테스트 완료 | 모든 시나리오 통과 | [날짜] | [이름] |
| 프로덕션 배포 | 제품 출시 | [날짜] | [이름] |

---

## 📊 Block 진행 현황

> **실시간 업데이트**: Block 개발 진행 중 업데이트

| Block | Feature 진행 | Module Test | 전체 상태 | 완료 예정일 |
|-------|-------------|-------------|----------|------------|
| **Block 1: [블럭명]** | [N/3] | 대기/완료 | ⏳/✅ | YYYY-MM-DD |
| **Block 2: [블럭명]** | [N/3] | 대기/완료 | ⏳/✅ | YYYY-MM-DD |
| **Block 3: [블럭명]** | [N/3] | 대기/완료 | ⏳/✅ | YYYY-MM-DD |
| **Product E2E TDD** | - | 대기/완료 | ⏳/✅ | YYYY-MM-DD |

**전체 진행률:** [N/10]
- Block Module Test: [N/3]
- Product E2E Test: [N/1]
- 총 Feature: [N/9] (3 Blocks × 3 Features)
- 총 Task: [N/45] (9 Features × 5 Tasks)

**예상 완료 시간:** 3-4주
- Block 1: 1주
- Block 2: 1주
- Block 3: 1주
- Product E2E TDD: 1-2일

---

## ✅ E2E Test Plan (제품 레벨 테스트)

> **⚠️ 작성 시점**: Block 3개 모두 완료 후
>
> **목적**: Block 결과를 참고하여 **PRD Success Metrics와 싱크**

**작성 전 확인:**
- [ ] Block 1-3 Module Test 모두 통과
- [ ] Block 1-3 PRD Success Metrics 달성 확인
- [ ] 전체 Success Metrics 목표 확인 완료

**E2E Test 체크리스트:**

1. **Block 간 연동 시나리오 작성**
   - [ ] Block 1 → Block 2 연동 시나리오
   - [ ] Block 2 → Block 3 연동 시나리오
   - [ ] Block 1 → Block 3 연동 시나리오 (있다면)
   - [ ] 전체 통합 시나리오 (Block 1→2→3 흐름)

2. **PRD Success Metrics 싱크**
   - [ ] PRD에 정의된 Product 성공 지표 확인
   - [ ] E2E Test가 해당 지표를 검증하는지 확인
   - [ ] 누락된 지표가 있으면 테스트 추가

3. **E2E Test 코드 작성**
   - [ ] `e2e/product/[product-name].test.ts` 작성
   - [ ] Given-When-Then 구조로 작성
   - [ ] 실패 케이스 포함
   - [ ] 성능 테스트 포함

4. **E2E Test 실행**
   - [ ] `npm run test:e2e`
   - [ ] 모든 테스트 통과 확인

**테스트 파일:** `e2e/product/[product-name].test.ts`

**통과 기준:**
- [ ] 모든 E2E Test 통과 (100%)
- [ ] PRD Success Metrics 달성 확인
- [ ] Block 3개 결과가 Product로 통합됨

---

### E2E 테스트 전략

> **프랙탈 TDD 최상위:** 제품 레벨에서는 **E2E (End-to-End) 테스트**로 검증합니다.
> 3개 블럭이 통합되어 사용자 관점에서 정상 동작하는지 확인합니다.

**테스트 범위:**
- **범위:** 제품 전체 사용자 워크플로우
- **환경:** 프로덕션과 동일한 환경
- **데이터:** 실제와 유사한 테스트 데이터

**테스트 레벨 (피라미드 최상단):**
```
제품 레벨 (E2E Test) ⬆️ ← 현재 레벨 (Block 3개 완료 후 작성)
  ↑
블럭 레벨 (Module Test) ⬆️ (Feature 3개 완료 후 작성)
  ↑
중단위 레벨 (Integration Test) ⬆️ (Task 5개 완료 후 작성)
  ↑
작은단위 레벨 (Unit Test) ⬇️ (개발과 동시에 작성)
```

---

### 주요 E2E 시나리오

#### 시나리오 1: [주요 사용자 워크플로우 - Happy Path]

**테스트 케이스 ID:** E2E-001

**사용자 스토리:**
```
As a [사용자 역할]
I want to [전체 워크플로우]
So that [비즈니스 가치]
```

**테스트 스텝:**
1. [Step 1]: [사용자 행동] → [예상 결과]
2. [Step 2]: [사용자 행동] → [예상 결과]
3. [Step 3]: [사용자 행동] → [예상 결과]

**검증 포인트:**
- [ ] 블럭 1 → 블럭 2 데이터 흐름 정상
- [ ] 블럭 2 → 블럭 3 데이터 흐름 정상
- [ ] 최종 결과가 Success Metrics 달성
- [ ] 성능 목표 달성 (< [N]초)

**자동화 코드 (예시):**
```typescript
describe('E2E: [워크플로우명]', () => {
  it('should complete entire user journey successfully', async () => {
    // Given: 초기 상태
    await setupE2EEnvironment();

    // When: 사용자 워크플로우 실행
    await page.goto('/start');
    await page.click('[data-testid="start-button"]');

    // Block 1 동작
    await page.fill('[data-testid="input-1"]', 'test data');
    await page.click('[data-testid="submit-1"]');

    // Block 2 동작
    await page.waitForSelector('[data-testid="result-1"]');
    await page.click('[data-testid="continue-button"]');

    // Block 3 동작
    await page.fill('[data-testid="input-3"]', 'final data');
    await page.click('[data-testid="finish-button"]');

    // Then: 최종 결과 검증
    const finalResult = await page.textContent('[data-testid="final-result"]');
    expect(finalResult).toContain('Success');

    // Success Metrics 검증
    const metrics = await getProductMetrics();
    expect(metrics.goal1).toBeGreaterThan(targetValue1);
    expect(metrics.goal2).toBeGreaterThan(targetValue2);
  });
});
```

---

#### 시나리오 2: [에러 복구 워크플로우]

**테스트 케이스 ID:** E2E-002

**목적:** 블럭 레벨 에러가 제품 레벨에서 올바르게 처리되는지 확인

**테스트 스텝:**
1. [정상 시작]
2. [블럭 2에서 에러 발생 시뮬레이션]
3. [에러 복구 메커니즘 동작]
4. [사용자에게 적절한 피드백]

**검증 포인트:**
- [ ] 에러 메시지가 사용자 친화적
- [ ] 데이터 손실 없음
- [ ] 복구 후 워크플로우 계속 가능

---

#### 시나리오 3: [성능 테스트]

**테스트 케이스 ID:** E2E-003

**목적:** 제품 전체의 성능 목표 달성 확인

**테스트 스텝:**
1. [대량 데이터 입력]
2. [전체 워크플로우 실행]
3. [응답 시간 측정]

**검증 포인트:**
- [ ] 전체 워크플로우 완료 시간 < [N]초
- [ ] 각 블럭 응답 시간 < [M]초
- [ ] 동시 사용자 [K]명 처리 가능

---

### E2E 테스트 자동화

**도구:**
- **E2E Framework:** Playwright | Cypress | Selenium
- **성능 측정:** Lighthouse | WebPageTest
- **모니터링:** Datadog | New Relic

**CI/CD 통합:**
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Environment
        run: npm install
      - name: Run E2E Tests
        run: npm run test:e2e
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-test-results
          path: test-results/
```

---

## 🔗 References (참고 자료)

### 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [기존 시스템 문서]
- [경쟁사 분석]

### 외부 링크
- [관련 기술 문서]
- [참고한 리서치 자료]

---

## ✅ Approval (승인)

### 검토자
- [ ] [역할 1] - [이름] - [날짜]
- [ ] [역할 2] - [이름] - [날짜]

### 승인자
- [ ] [역할] - [이름] - [날짜]

---

## 📝 Change Log (변경 이력)

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.1 | 2025-11-08 | 피라미드 작업 흐름 반영, E2E TDD 작성 시점 명시, Block 진행 현황 추적 추가 | AI (Claude Code) |
| 1.0 | YYYY-MM-DD | 초안 작성 | [이름] |

---

## 💡 Notes (참고 사항)

### CLEAR 원칙 체크
- [ ] **Concise**: 2-3 페이지 이내 (✅ 현재 페이지 수: ___)
- [ ] **Logical**: Goals → Stories → Metrics 순서 논리적
- [ ] **Explicit**: 모호한 표현 없음 ("빠르게" → "< 200ms")
- [ ] **Adaptive**: Non-Goals로 범위 유연성 확보
- [ ] **Reflective**: Success Metrics로 검증 가능

### 계층적 TDD 매핑
- **이 문서는 "제품 (Product)" 레벨입니다.**
- 하위 계층: [[./Block_템플릿_통합|Block_템플릿_통합]] (Feature + Task 포함)
- 프랙탈 TDD 피라미드:
  ```
  제품 E2E Test ⬆️ (Block 3개 완료 후 작성)
    ↑
  블럭 Module Test ⬆️ (Feature 3개 완료 후 작성)
    ↑
  중단위 Integration Test ⬆️ (Task 5개 완료 후 작성)
    ↑
  작은단위 Unit Test ⬇️ (개발과 동시에 작성)
  ```
- **5단계 프로세스:** 이 문서는 "1. Recognize (명확히 인식)" 단계입니다.

---

**작성 완료일:** YYYY-MM-DD
**다음 리뷰:** YYYY-MM-DD

---

## 📚 버전 이력

### v1.1 (2025-11-08)
**목적:** 피라미드 작업 흐름 반영

**핵심 변경:**
1. **작업 흐름 (피라미드) 섹션 추가**
   - PRD → Block 개발 → E2E TDD 작성 (아래→위)
   - "Block 3개 완료 후 E2E TDD 작성" 명시

2. **E2E Test Plan 강화**
   - "⚠️ 작성 시점: Block 3개 완료 후" 추가
   - E2E Test 체크리스트 추가 (Block 간 연동, PRD 싱크)
   - 테스트 레벨 피라미드 시각화

3. **Block 진행 현황 섹션 추가**
   - Block 1-3 진행 상황 추적 표
   - 전체 진행률 계산 (Feature, Task, Module Test, E2E Test)
   - 예상 완료 시간 (3-4주)

4. **문서 간 일관성**
   - [[Block_템플릿_통합]] 링크로 변경
   - 피라미드 구조 일관성 확보

**참조 문서:**
- [[./Block_템플릿_통합]] - 하위 레벨 통합 템플릿
- [[../CJ_AI_개발방법론]] - 이론 및 방법론

### v1.0 (초기 버전)
- 기본 PRD 템플릿 구조 정의
- Success Metrics, User Stories, Timeline
- E2E Test Plan (기본)
