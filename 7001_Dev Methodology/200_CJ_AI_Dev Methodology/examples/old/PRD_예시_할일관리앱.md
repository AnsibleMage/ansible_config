## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [[../templates/PRD_템플릿|PRD 템플릿]]
- [[./DesignDoc_예시_할일관리앱|Design Doc (다음 단계)]]

---

# PRD: Simple Todo App

**작성일:** 2025-11-07
**작성자:** 김개발
**버전:** 1.0
**상태:** 승인됨

---

## 📋 계층 구조

```
🎯 제품 (Product): Simple Todo App  ← 현재 레벨
  ├─ 블럭 1: 할일 입력 관리
  │    ├─ 중단위 1-1: 입력 검증 (5 Task)
  │    │    ├─ Task 1-1-1: 빈 값 체크
  │    │    ├─ Task 1-1-2: 길이 제한 체크
  │    │    ├─ Task 1-1-3: 중복 체크
  │    │    ├─ Task 1-1-4: 텍스트 정규화
  │    │    └─ Task 1-1-5: DTO 변환
  │    ├─ 중단위 1-2: 저장 처리 (5 Task)
  │    │    ├─ Task 1-2-1: Zustand Store 설정
  │    │    ├─ Task 1-2-2: addTodo Action
  │    │    ├─ Task 1-2-3: LocalStorage Persist
  │    │    ├─ Task 1-2-4: 에러 핸들링
  │    │    └─ Task 1-2-5: 성공 피드백
  │    └─ 중단위 1-3: 입력 UI (5 Task)
  │         ├─ Task 1-3-1: Input 컴포넌트
  │         ├─ Task 1-3-2: 버튼 컴포넌트
  │         ├─ Task 1-3-3: Enter 키 핸들러
  │         ├─ Task 1-3-4: 포커스 관리
  │         └─ Task 1-3-5: 애니메이션
  │
  ├─ 블럭 2: 할일 상태 관리
  │    ├─ 중단위 2-1: 완료 토글 (5 Task)
  │    │    ├─ Task 2-1-1: toggleTodo Action
  │    │    ├─ Task 2-1-2: 상태 업데이트 로직
  │    │    ├─ Task 2-1-3: LocalStorage 동기화
  │    │    ├─ Task 2-1-4: 낙관적 업데이트
  │    │    └─ Task 2-1-5: 체크박스 UI
  │    ├─ 중단위 2-2: 삭제 처리 (5 Task)
  │    │    ├─ Task 2-2-1: deleteTodo Action
  │    │    ├─ Task 2-2-2: 삭제 확인 로직
  │    │    ├─ Task 2-2-3: LocalStorage 동기화
  │    │    ├─ Task 2-2-4: 애니메이션
  │    │    └─ Task 2-2-5: 삭제 버튼 UI
  │    └─ 중단위 2-3: 필터 & 정렬 (5 Task)
  │         ├─ Task 2-3-1: 필터 상태 관리
  │         ├─ Task 2-3-2: 정렬 로직
  │         ├─ Task 2-3-3: 필터 UI
  │         ├─ Task 2-3-4: 정렬 UI
  │         └─ Task 2-3-5: URL 쿼리 동기화
  │
  └─ 블럭 3: 할일 표시
       ├─ 중단위 3-1: 리스트 렌더링 (5 Task)
       │    ├─ Task 3-1-1: TodoList 컴포넌트
       │    ├─ Task 3-1-2: TodoItem 컴포넌트
       │    ├─ Task 3-1-3: 빈 상태 처리
       │    ├─ Task 3-1-4: 로딩 상태
       │    └─ Task 3-1-5: 가상화 (100+ 항목)
       ├─ 중단위 3-2: 스타일링 (5 Task)
       │    ├─ Task 3-2-1: CSS-in-JS 설정
       │    ├─ Task 3-2-2: 반응형 레이아웃
       │    ├─ Task 3-2-3: 다크 모드
       │    ├─ Task 3-2-4: 트랜지션
       │    └─ Task 3-2-5: 접근성 (a11y)
       └─ 중단위 3-3: 성능 최적화 (5 Task)
            ├─ Task 3-3-1: React.memo 적용
            ├─ Task 3-3-2: useCallback 최적화
            ├─ Task 3-3-3: 지연 로딩
            ├─ Task 3-3-4: 디바운스
            └─ Task 3-3-5: 번들 크기 최적화

총: 1 제품 = 3 블럭 = 9 중단위 = 45 작은단위
```

**권장 구조:**
- 1개 제품 = 3개 블럭
- 1개 블럭 = 3개 중단위 (Feature)
- 1개 중단위 = 5개 작은단위 (Task)
- 1개 작은단위 = 1-2시간 작업

**예상 일정:**
- Task: 1-2시간
- Feature (5 Tasks): 1-2일
- Block (3 Features): 3-7일
- Product (3 Blocks): 2-4주

---

## 📋 Overview (개요)

### 한 문장 요약
> 개인 사용자가 할일을 간단하게 관리할 수 있는 미니멀한 웹 애플리케이션

### 배경 및 동기
**문제:**
- 기존 할일 관리 앱들은 너무 복잡하고 기능이 많아 사용하기 부담스러움
- 단순히 "해야 할 일"만 빠르게 기록하고 체크하고 싶은 사용자 니즈 존재
- 모바일보다 데스크톱에서 작업하는 사용자를 위한 간편한 도구 부족

**기회:**
- 미니멀리즘 트렌드 - 단순함에 가치를 두는 사용자층 증가
- 웹 기반이므로 설치 불필요, 모든 기기에서 접근 가능
- TDD + AI(Claude Code)를 활용한 고품질 코드로 빠른 개발 가능

### 목표 사용자
- **주 사용자:** 개인 생산성을 추구하는 데스크톱 사용자 (25-40세)
- **부 사용자:** 간단한 할일 관리가 필요한 모든 웹 사용자

---

## 🎯 Goals & Non-Goals (범위)

### ✅ Goals (할 것)

**핵심 기능 (Must-Have):**
1. **할일 추가** - 텍스트 입력으로 새 할일 생성
2. **할일 완료 체크** - 체크박스로 완료 상태 토글
3. **할일 삭제** - 필요 없는 할일 제거

**부가 기능 (Nice-to-Have):**
- 할일 정렬 (최신순/오래된순)
- 다크 모드 지원

### ❌ Non-Goals (하지 않을 것)

**명시적 제외 항목:**
- 사용자 인증/로그인 - 로컬 스토리지만 사용, 계정 불필요
- 공유 기능 - 개인용으로 한정
- 마감일/알림 - 단순함 유지를 위해 제외
- 카테고리/태그 - 복잡도 증가 방지

**향후 고려 사항:**
- v2.0에서 사용자 계정 및 클라우드 동기화 고려
- v2.0에서 할일 우선순위 기능 고려

---

## 📖 User Stories (사용자 스토리)

### Story 1: 할일 빠르게 추가하기
```
As a 바쁜 직장인
I want 할일을 빠르게 입력하고 저장
So that 머릿속 생각을 즉시 기록할 수 있다
```

**수용 기준:**
- [ ] 입력창에 텍스트 입력 후 Enter 키 또는 "추가" 버튼 클릭 시 할일이 목록에 추가됨
- [ ] 빈 텍스트는 추가되지 않음 (유효성 검사)
- [ ] 추가 후 입력창은 자동으로 비워짐 (다음 입력 준비)
- [ ] 응답 시간 < 200ms

**우선순위:** 높음

---

### Story 2: 완료한 할일 체크하기
```
As a 사용자
I want 완료한 할일을 체크
So that 무엇을 완료했는지 시각적으로 확인할 수 있다
```

**수용 기준:**
- [ ] 각 할일 항목 옆에 체크박스 존재
- [ ] 체크박스 클릭 시 완료 상태 토글
- [ ] 완료된 할일은 취소선 스타일 적용
- [ ] 상태 변경 즉시 로컬 스토리지에 저장

**우선순위:** 높음

---

### Story 3: 불필요한 할일 삭제하기
```
As a 사용자
I want 필요 없는 할일을 삭제
So that 목록을 깔끔하게 유지할 수 있다
```

**수용 기준:**
- [ ] 각 할일 항목 옆에 "삭제" 버튼 존재
- [ ] 삭제 버튼 클릭 시 확인 없이 즉시 삭제 (undo 기능 없음)
- [ ] 삭제 후 목록에서 즉시 제거
- [ ] 로컬 스토리지에서도 삭제

**우선순위:** 높음

---

### Story 4: 할일 목록 정렬하기
```
As a 사용자
I want 할일을 최신순 또는 오래된순으로 정렬
So that 원하는 순서로 할일을 볼 수 있다
```

**수용 기준:**
- [ ] 정렬 드롭다운 메뉴 제공 (최신순/오래된순)
- [ ] 정렬 변경 시 즉시 목록 재정렬
- [ ] 정렬 기본값: 최신순

**우선순위:** 중간

---

## 📊 Success Metrics (성공 지표)

### 정량적 목표

| 지표 | 목표 | 측정 방법 | 기준일 |
|------|------|----------|--------|
| 초기 로딩 시간 | < 1초 | Lighthouse 측정 | MVP 완료 시 |
| 할일 추가 응답 시간 | < 200ms | Performance API 측정 | MVP 완료 시 |
| 테스트 커버리지 | > 90% | Jest Coverage 보고서 | MVP 완료 시 |
| 변이 점수 | > 80% | Stryker 보고서 | MVP 완료 시 |
| 모바일 반응성 | 100% | 3가지 화면 크기 테스트 | MVP 완료 시 |

### 정성적 목표
- 사용자가 3초 이내에 첫 할일을 추가할 수 있음
- UI가 직관적이어서 별도 설명 없이 사용 가능

### 완료 기준 (Definition of Done)
- [ ] 모든 User Story의 수용 기준 충족
- [ ] 테스트 커버리지 > 90%, 변이 점수 > 80%
- [ ] Chrome, Firefox, Safari 브라우저에서 동작 확인
- [ ] 반응형 디자인 적용 (모바일, 태블릿, 데스크톱)
- [ ] 접근성 기준 AA 등급 달성 (WCAG 2.1)

---

## 🚧 Constraints (제약 조건)

### 기술적 제약
- **기술 스택:** React 18 + TypeScript, Node.js 18+, PostgreSQL 14+
- **성능:** 초기 로딩 < 1초, 할일 추가/삭제 < 200ms
- **호환성:** Chrome 100+, Firefox 90+, Safari 15+
- **보안:** HTTPS 필수, XSS/CSRF 방어
- **데이터 저장:** 로컬 스토리지 (5MB 제한)

### 비즈니스 제약
- **예산:** 개발 비용 없음 (개인 프로젝트)
- **일정:** 3주 내 MVP 완성 (2025-11-28까지)
- **리소스:** 1인 개발 (주말 8시간 + 평일 저녁 2시간)

### 외부 의존성
- 없음 (외부 API 사용 안 함)

---

## ⚠️ Risks (리스크)

### 높은 리스크 (High)

**리스크 1:** 일정 지연 (3주는 타이트한 일정)
- **영향:** MVP 출시 지연
- **확률:** 중간
- **완화 계획:**
  - 핵심 기능 3개만 집중 (추가/체크/삭제)
  - Nice-to-Have 기능은 우선순위 낮춤
  - 주간 진행 체크포인트 설정

### 중간 리스크 (Medium)

**리스크 2:** 브라우저 호환성 이슈
- **영향:** 특정 브라우저에서 동작 불안정
- **확률:** 낮음
- **완화 계획:**
  - React 사용으로 크로스 브라우저 이슈 최소화
  - 주요 브라우저 3개에서 수동 테스트

**리스크 3:** 로컬 스토리지 용량 초과
- **영향:** 할일 추가 불가
- **확률:** 낮음 (5MB 충분)
- **완화 계획:**
  - 할일 개수 제한 (최대 500개)
  - 용량 초과 시 경고 메시지

### 낮은 리스크 (Low)

**리스크 4:** React 버전 업데이트로 인한 Breaking Change
- **영향:** 빌드 실패
- **확률:** 낮음
- **완화 계획:**
  - package.json에 정확한 버전 명시
  - 개발 기간 동안 버전 고정

---

## 📅 Timeline (일정)

| 마일스톤 | 완료 기준 | 예상 일정 | 담당자 |
|---------|---------|----------|--------|
| 요구사항 확정 | PRD 승인 | 2025-11-07 | 김개발 |
| 설계 완료 | Design Doc 승인 | 2025-11-10 | 김개발 |
| 개발 완료 | 모든 테스트 통과 | 2025-11-24 | 김개발 |
| 배포 | Vercel/Netlify 배포 | 2025-11-28 | 김개발 |

---

## 🧪 E2E Test Plan (제품 레벨 테스트)

> **프랙탈 TDD 최상위:** 제품 레벨에서는 **E2E (End-to-End) 테스트**로 검증합니다.
> 3개 블럭이 통합되어 사용자 관점에서 정상 동작하는지 확인합니다.

### E2E 테스트 전략

**테스트 범위:**
- **범위:** 제품 전체 사용자 워크플로우
- **환경:** 실제 브라우저 (Playwright)
- **데이터:** LocalStorage 기반

**테스트 레벨:**
```
제품 레벨 (E2E Test) ← 이 PRD가 검증하는 레벨
  ↓
블럭 레벨 (Module Test)
  ↓
중단위 레벨 (Feature Integration Test)
  ↓
작은단위 레벨 (Unit Test)
```

---

### 주요 E2E 시나리오

#### 시나리오 1: 할일 전체 워크플로우 (Happy Path)

**테스트 케이스 ID:** E2E-001

**사용자 스토리:**
```
As a 사용자
I want to 할일을 추가하고, 완료 체크하고, 삭제하는 전체 흐름을 실행
So that 할일 관리 앱이 정상 동작함을 확인
```

**테스트 스텝:**
1. **Block 1 동작**: 할일 "프로젝트 설계" 추가 → LocalStorage에 저장 확인
2. **Block 2 동작**: 완료 체크박스 클릭 → 취소선 스타일 적용 확인
3. **Block 3 동작**: 삭제 버튼 클릭 → 리스트에서 제거 확인

**검증 포인트:**
- [ ] Block 1 (입력 관리) → Block 2 (상태 관리) 데이터 흐름 정상
- [ ] Block 2 (상태 관리) → Block 3 (표시) 데이터 흐름 정상
- [ ] 최종 결과: 할일이 추가되고, 완료되고, 삭제됨
- [ ] 성능 목표 달성 (응답 시간 < 200ms)

**자동화 코드 (Playwright):**
```typescript
import { test, expect } from '@playwright/test';

describe('E2E: Simple Todo App - 전체 워크플로우', () => {
  test('사용자가 할일을 추가하고 완료하고 삭제할 수 있다', async ({ page }) => {
    // Given: 사용자가 앱을 연다
    await page.goto('http://localhost:3000');

    // When: Block 1 - 할일 입력 관리
    const input = page.locator('[data-testid="todo-input"]');
    await input.fill('프로젝트 설계');
    await page.click('[data-testid="add-button"]');

    // Then: Block 1 검증 - 할일이 추가됨
    const todoItem = page.locator('[data-testid="todo-item-1"]');
    await expect(todoItem).toHaveText('프로젝트 설계');

    // LocalStorage에 저장되었는지 확인
    const localStorage = await page.evaluate(() =>
      JSON.parse(window.localStorage.getItem('todos') || '[]')
    );
    expect(localStorage).toHaveLength(1);
    expect(localStorage[0].text).toBe('프로젝트 설계');

    // When: Block 2 - 할일 상태 관리 (완료 체크)
    await page.click('[data-testid="todo-1-checkbox"]');

    // Then: Block 2 검증 - 완료 스타일 적용
    await expect(todoItem).toHaveClass(/completed/);
    await expect(todoItem).toHaveCSS('text-decoration', 'line-through');

    // When: Block 2 - 삭제 처리
    await page.click('[data-testid="todo-1-delete"]');

    // Then: Block 3 검증 - 리스트에서 제거됨
    await expect(todoItem).not.toBeVisible();
    const emptyState = page.locator('[data-testid="empty-state"]');
    await expect(emptyState).toBeVisible();
    await expect(emptyState).toHaveText('할일이 없습니다');

    // Final: Success Metrics 검증
    // 1. 성능: 각 동작이 200ms 이내 (Playwright 자동 측정)
    // 2. 정확성: 모든 동작이 예상대로 수행됨 ✅
  });
});
```

---

#### 시나리오 2: 다중 할일 관리 (Batch Operations)

**테스트 케이스 ID:** E2E-002

**목적:** 여러 할일을 추가하고 필터/정렬 기능이 3개 블럭 통합에서 정상 동작하는지 확인

**테스트 스텝:**
1. 할일 3개 추가 (Block 1)
2. 2개 완료 체크 (Block 2)
3. 필터: "완료됨" 선택 → 2개만 표시 (Block 2 + Block 3)
4. 정렬: "최신순" 선택 → 순서 변경 확인 (Block 2 + Block 3)

**검증 포인트:**
- [ ] 다중 입력이 정상 처리됨 (Block 1)
- [ ] 필터링 로직이 표시에 반영됨 (Block 2 → Block 3)
- [ ] 정렬이 실시간 업데이트됨 (Block 2 → Block 3)
- [ ] 100개 할일에서도 성능 유지 (< 1초)

**자동화 코드:**
```typescript
test('다중 할일 추가 및 필터/정렬 동작', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Given: 할일 3개 추가
  const todos = ['디자인 작업', '코드 리뷰', '배포 준비'];
  for (const todo of todos) {
    await page.fill('[data-testid="todo-input"]', todo);
    await page.click('[data-testid="add-button"]');
  }

  // When: 2개 완료 체크
  await page.click('[data-testid="todo-1-checkbox"]');
  await page.click('[data-testid="todo-2-checkbox"]');

  // Then: 3개 모두 표시됨 (미완료 + 완료)
  const items = page.locator('[data-testid^="todo-item-"]');
  await expect(items).toHaveCount(3);

  // When: 필터 - "완료됨"만 보기
  await page.selectOption('[data-testid="filter-select"]', 'completed');

  // Then: 2개만 표시됨
  await expect(items).toHaveCount(2);

  // When: 정렬 - "최신순"
  await page.selectOption('[data-testid="sort-select"]', 'newest');

  // Then: 순서가 역순으로 변경됨
  const firstItem = page.locator('[data-testid="todo-item-1"]');
  await expect(firstItem).toHaveText('코드 리뷰');
});
```

---

#### 시나리오 3: 에러 복구 워크플로우

**테스트 케이스 ID:** E2E-003

**목적:** 블럭 레벨 에러가 제품 레벨에서 올바르게 처리되는지 확인

**테스트 스텝:**
1. 빈 값 입력 시도 (Block 1 에러)
2. 에러 메시지 표시 확인 (Block 1 피드백)
3. 100자 초과 입력 (Block 1 검증)
4. LocalStorage 용량 모의 초과 (Block 2 에러)

**검증 포인트:**
- [ ] 에러 메시지가 사용자 친화적 (Block 1)
- [ ] 데이터 손실 없음 (Block 1 → Block 2)
- [ ] 복구 후 워크플로우 계속 가능
- [ ] 에러 상태에서도 UI 안정적 (Block 3)

**자동화 코드:**
```typescript
test('입력 에러 처리 및 복구', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // When: 빈 값 입력
  await page.click('[data-testid="add-button"]');

  // Then: 에러 메시지 표시
  const errorMsg = page.locator('[data-testid="error-message"]');
  await expect(errorMsg).toBeVisible();
  await expect(errorMsg).toHaveText('할일을 입력해주세요');

  // When: 유효한 입력
  await page.fill('[data-testid="todo-input"]', '정상 할일');
  await page.click('[data-testid="add-button"]');

  // Then: 정상 추가 및 에러 메시지 사라짐
  await expect(errorMsg).not.toBeVisible();
  const item = page.locator('[data-testid="todo-item-1"]');
  await expect(item).toBeVisible();
});
```

---

#### 시나리오 4: 성능 테스트 (100+ 할일)

**테스트 케이스 ID:** E2E-004

**목적:** 제품 전체의 성능 목표 달성 확인

**테스트 스텝:**
1. 100개 할일 추가 (자동화)
2. 전체 워크플로우 실행 (추가, 체크, 필터, 정렬, 삭제)
3. 응답 시간 측정

**검증 포인트:**
- [ ] 100개 항목 로딩 시간 < 1초
- [ ] 각 동작 응답 시간 < 200ms
- [ ] 가상화로 렌더링 최적화 확인
- [ ] 메모리 누수 없음

---

### E2E 테스트 자동화

**도구:**
- **E2E Framework:** Playwright (브라우저 자동화)
- **성능 측정:** Lighthouse, Web Vitals
- **모니터링:** Sentry (프로덕션 에러 추적)

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
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Dependencies
        run: npm ci
      - name: Build
        run: npm run build
      - name: Run E2E Tests
        run: npm run test:e2e
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-test-results
          path: test-results/
```

**실행 명령:**
```bash
# 로컬 실행
npm run test:e2e

# 특정 시나리오만
npm run test:e2e -- --grep "E2E-001"

# Headed 모드 (브라우저 보이기)
npm run test:e2e -- --headed

# 느린 동작 (디버깅용)
npm run test:e2e -- --slow-mo 1000
```

---

## 🔗 References (참고 자료)

### 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]]
- [[../templates/PRD_템플릿|PRD 템플릿]]

### 외부 링크
- [React 공식 문서](https://react.dev)
- [Jest Testing Best Practices](https://jestjs.io/docs/en/getting-started)
- [Stryker Mutator 가이드](https://stryker-mutator.io)

---

## ✅ Approval (승인)

### 검토자
- [x] Tech Lead - 김개발 - 2025-11-07

### 승인자
- [x] Product Owner - 김개발 - 2025-11-07

---

## 📝 Change Log (변경 이력)

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2025-11-07 | 초안 작성 및 승인 | 김개발 |

---

## 💡 Notes (참고 사항)

### CLEAR 원칙 체크
- [x] **Concise**: 2.5 페이지 (✅ 목표: 2-3 페이지)
- [x] **Logical**: Goals → Stories → Metrics 순서 논리적
- [x] **Explicit**: 명확한 숫자 목표 (<200ms, >90% 등)
- [x] **Adaptive**: Non-Goals로 범위 명확히 제한
- [x] **Reflective**: Success Metrics로 검증 가능

### 5단계 프로세스 매핑
- **이 문서는 5단계의 "1. Recognize (명확히 인식)"에 해당합니다.**
- 다음 단계: [[./DesignDoc_예시_할일관리앱|Design Doc (Explore, Opposites, Select)]]

---

**작성 완료일:** 2025-11-07
**다음 리뷰:** 2025-12-07
