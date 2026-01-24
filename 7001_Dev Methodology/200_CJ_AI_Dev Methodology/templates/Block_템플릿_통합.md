## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]] - 전체 방법론 (이론은 여기 참조)
- [[./Product_PRD_템플릿|Product PRD 템플릿]] - 상위 PRD (AI 작성 가이드 참조)

---

# Block [N]: [블럭명]

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**상태:** 대기 | 진행 중 | 완료

**소속 Product:** [[Product_PRD]]

---

## 📋 Block 정의

**한 줄 요약:**
> [이 Block이 Product에서 담당하는 핵심 역할을 한 문장으로]

**담당 Features:** 3개
- Feature 1: [기능명]
- Feature 2: [기능명]
- Feature 3: [기능명]

**완성 기준:**
- [ ] Feature 3개 Integration Test 모두 통과
- [ ] Block Module Test 통과
- [ ] PRD Success Metrics 달성

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 읽기
        ↓
단계 2: Block/Feature/Task 정의 (이 문서 작성)
        ↓
단계 3: Task 1 개발 (Unit TDD: Red-Green-Refactor-Mutation)
        ↓
단계 4: Task 2-5 개발 (동일)
        ↓
단계 5: ✅ Feature 1 Integration TDD 작성 ⬆️
        (Task 5개 결과 참고 + PRD 싱크)
        ↓
단계 6: Feature 2, 3 동일 반복
        ↓
단계 7: ✅ Block Module TDD 작성 ⬆️
        (Feature 3개 결과 참고 + PRD 싱크)
```

**중요:**
- Task는 **Red-Green-Refactor-Mutation 4단계 모두 완료 후** 체크
- Feature Integration TDD는 **Task 5개 모두 완료 후** 작성 (Task 개발 중 작성 ❌)
- Block Module TDD는 **Feature 3개 Integration TDD 모두 완료 후** 작성 (Feature 개발 중 작성 ❌)

---

## Feature 1: [기능명]

### Feature 1 정의

**한 줄 요약:**
> [이 Feature가 하는 일을 한 문장으로]

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 1: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/[feature]/[task-name].ts`
- 테스트: `tests/[feature]/[task-name].test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 2: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/[feature]/[task-name].ts`
- 테스트: `tests/[feature]/[task-name].test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 3: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/[feature]/[task-name].ts`
- 테스트: `tests/[feature]/[task-name].test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/[feature]/[task-name].ts`
- 테스트: `tests/[feature]/[task-name].test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 5: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/[feature]/[task-name].ts`
- 테스트: `tests/[feature]/[task-name].test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### ✅ Feature 1 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후
>
> **목적**: Task 결과를 참고하여 **PRD Success Metrics와 싱크**

**작성 전 확인:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] Task 1-5 변이 점수 모두 >80%
- [ ] [[Product_PRD]] Success Metrics 확인 완료

**Integration Test 체크리스트:**

1. **Task 간 연동 시나리오 작성**
   - [ ] Task 1 → Task 2 연동 시나리오
   - [ ] Task 2 → Task 3 연동 시나리오
   - [ ] Task 3 → Task 4 연동 시나리오
   - [ ] Task 4 → Task 5 연동 시나리오
   - [ ] 전체 통합 시나리오 (1→5 흐름)

2. **PRD Success Metrics 싱크**
   - [ ] PRD에 정의된 Feature 1 성공 지표 확인
   - [ ] Integration Test가 해당 지표를 검증하는지 확인
   - [ ] 누락된 지표가 있으면 테스트 추가

3. **Integration Test 코드 작성**
   - [ ] `tests/[feature-1]/integration.test.ts` 작성
   - [ ] Given-When-Then 구조로 작성
   - [ ] 실패 케이스 포함

4. **Integration Test 실행**
   - [ ] `npm test -- tests/[feature-1]/integration.test.ts`
   - [ ] 모든 테스트 통과 확인

**테스트 파일:** `tests/[feature-1]/integration.test.ts`

**통과 기준:**
- [ ] 모든 Integration Test 통과 (100%)
- [ ] PRD Success Metrics 달성 확인
- [ ] Task 5개 결과가 Feature로 통합됨

---

## Feature 2: [기능명]

### Feature 2 정의

**한 줄 요약:**
> [이 Feature가 하는 일을 한 문장으로]

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성

**예상 소요 시간:** 2일

---

### Task 1: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### Task 2: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### Task 3: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### Task 4: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### Task 5: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### ✅ Feature 2 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] Task 간 연동 시나리오 작성
- [ ] PRD Success Metrics 싱크
- [ ] Integration Test 코드 작성 (`tests/[feature-2]/integration.test.ts`)
- [ ] Integration Test 실행 → 통과

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] PRD Success Metrics 달성

---

## Feature 3: [기능명]

### Feature 3 정의

**한 줄 요약:**
> [이 Feature가 하는 일을 한 문장으로]

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성

**예상 소요 시간:** 2일

---

### Task 1: [작업명]

**작업 목표:** [한 문장으로]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/[feature]/[task].ts`, `tests/[feature]/[task].test.ts`

---

### Task 2: [작업명]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분

---

### Task 3: [작업명]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분

---

### Task 4: [작업명]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분

---

### Task 5: [작업명]

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분

---

### ✅ Feature 3 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] Task 간 연동 시나리오 작성
- [ ] PRD Success Metrics 싱크
- [ ] Integration Test 코드 작성 (`tests/[feature-3]/integration.test.ts`)
- [ ] Integration Test 실행 → 통과

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] PRD Success Metrics 달성

---

## ✅ Block Module TDD

> **⚠️ 작성 시점**: Feature 3개 완료 후
>
> **목적**: Feature 결과를 참고하여 **PRD Success Metrics와 싱크**

**작성 전 확인:**
- [ ] Feature 1-3 Integration Test 모두 통과
- [ ] Feature 1-3 PRD Success Metrics 달성 확인
- [ ] [[Product_PRD]] 전체 Success Metrics 확인

**Module Test 체크리스트:**

1. **Feature 간 연동 시나리오 작성**
   - [ ] Feature 1 → Feature 2 연동 시나리오
   - [ ] Feature 2 → Feature 3 연동 시나리오
   - [ ] Feature 1 → Feature 3 연동 시나리오
   - [ ] 전체 통합 시나리오 (Feature 1→2→3 흐름)

2. **SOLID 원칙 검증**
   - [ ] **Single Responsibility**: 각 모듈이 하나의 책임만
   - [ ] **Open/Closed**: 확장에는 열려있고 수정에는 닫혀있음
   - [ ] **Liskov Substitution**: 하위 타입이 상위 타입을 대체 가능
   - [ ] **Interface Segregation**: 클라이언트별 인터페이스 분리
   - [ ] **Dependency Inversion**: 구체가 아닌 추상에 의존

3. **PRD Success Metrics 싱크**
   - [ ] PRD에 정의된 Block 성공 지표 확인
   - [ ] Module Test가 해당 지표를 검증하는지 확인
   - [ ] 누락된 지표가 있으면 테스트 추가

4. **Module Test 코드 작성**
   - [ ] `tests/[block]/module.test.ts` 작성
   - [ ] Given-When-Then 구조로 작성
   - [ ] 실패 케이스 포함
   - [ ] 성능 테스트 포함 (필요시)

5. **Module Test 실행**
   - [ ] `npm test -- tests/[block]/module.test.ts`
   - [ ] 모든 테스트 통과 확인

**테스트 파일:** `tests/[block]/module.test.ts`

**통과 기준:**
- [ ] 모든 Module Test 통과 (100%)
- [ ] SOLID 원칙 준수 확인
- [ ] PRD Success Metrics 달성 확인
- [ ] Feature 3개 결과가 Block으로 통합됨

---

## 📊 작업 진행 현황

| 항목 | Task 진행 | Integration/Module | 전체 상태 |
|------|-----------|-------------------|----------|
| **Feature 1** | [N/5] | 대기/완료 | ⏳/✅ |
| **Feature 2** | [N/5] | 대기/완료 | ⏳/✅ |
| **Feature 3** | [N/5] | 대기/완료 | ⏳/✅ |
| **Block Module TDD** | - | 대기/완료 | ⏳/✅ |

**전체 진행률:** [N/19]
- Task: [N/15] (Feature 3개 × Task 5개)
- Integration TDD: [N/3] (Feature 3개)
- Module TDD: [N/1] (Block 1개)

**예상 완료 시간:** 6-7일
- Feature 1: 2일
- Feature 2: 2일
- Feature 3: 2일
- Block Module TDD: 0.5일

---

## 📝 작업 로그

### YYYY-MM-DD
- **시간**: HH:MM - HH:MM
- **작업**: [Feature N, Task N]
- **상태**: Red/Green/Refactor/Mutation
- **이슈**: [발견된 이슈]
- **해결**: [해결 방법]

### YYYY-MM-DD
- **시간**: HH:MM - HH:MM
- **작업**: [작업 내용]
- **상태**: [상태]

---

## ⚠️ 주의사항

### 작업 순서 엄수
1. ❌ Feature Integration TDD를 Task 완료 전에 작성하지 마세요
2. ❌ Block Module TDD를 Feature 완료 전에 작성하지 마세요
3. ✅ 피라미드 순서: Task 개발 → Feature TDD → Block TDD

### PRD 싱크 필수
- Feature Integration TDD 작성 시 → PRD Success Metrics 확인
- Block Module TDD 작성 시 → PRD Success Metrics 확인
- 싱크가 안 맞으면 → PRD 수정 or Test 수정

### 품질 기준
- Task: 변이 점수 >80%
- Feature Integration: 모든 Test 통과
- Block Module: SOLID + 모든 Test 통과

---

**작성일:** YYYY-MM-DD
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**최종 업데이트:** YYYY-MM-DD HH:MM

---

## 📚 버전 이력

### v1.0 (2025-11-08)
**목적:** Block + Feature + Task 3개 템플릿 통합

**핵심 변경:**
1. **피라미드 작업 흐름 반영**
   - Task 개발 (Unit TDD) → Feature Integration TDD → Block Module TDD
   - 아래에서 위로 올라가는 구조

2. **PRD 싱크 포인트 명시**
   - Feature Integration TDD: Task 결과 + PRD 싱크
   - Block Module TDD: Feature 결과 + PRD 싱크

3. **중복 제거**
   - 이론 설명 제거 (CJ_AI_개발방법론.md 참조)
   - AI 작성 가이드 제거 (Product_PRD_템플릿.md 참조)
   - 체크리스트 중심으로 간소화

4. **실무 중심**
   - 개발하면서 채워나가는 문서
   - 작업 진행 현황 추적
   - 작업 로그 기록

**구조:**
- Block 정의
- Feature 1-3 (각 Task 1-5 + Integration TDD)
- Block Module TDD
- 작업 진행 현황

**참조 문서:**
- [[../CJ_AI_개발방법론]] - 이론 및 방법론
- [[./Product_PRD_템플릿]] - AI 작성 가이드
