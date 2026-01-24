## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]] - 전체 방법론
- [[./Product_PRD_종이비행기날아라|Product PRD]] - 상위 PRD
- [[./Block_템플릿_통합|Block 템플릿]] - 템플릿 참조

---

# Block 1: 비행 조작 시스템 (Flight Control)

**작성일:** 2025-11-08
**작성자:** AI (Claude Code) - TDD 전문 개발 에이전트
**버전:** 1.0
**상태:** 진행 중

**소속 Product:** [[./Product_PRD_종이비행기날아라|종이비행기 날아라]]

---

## 📋 Block 정의

**한 줄 요약:**
> 키보드/마우스 입력을 받아 3D 공간에서 종이비행기를 물리 법칙에 따라 조작하고, 카메라가 부드럽게 추적하는 비행 경험을 제공하는 시스템

**담당 Features:** 3개
- Feature 1.1: 입력 처리 시스템 (Input Handler)
- Feature 1.2: 비행 물리 엔진 (Flight Physics Engine)
- Feature 1.3: 카메라 시스템 (Camera System)

**완성 기준:**
- [ ] Feature 3개 Integration Test 모두 통과
- [ ] Block Module Test 통과
- [ ] PRD Success Metrics 달성:
  - [ ] 입력 응답 시간 < 16ms
  - [ ] FPS ≥ 60
  - [ ] 직관적 조작 (튜토리얼 없이 3회 시도 내 골인)

**예상 소요 시간:** 1주 (Feature 3개 × 2일 + Module TDD 1일)

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 읽기 ✅
        ↓
단계 2: Block/Feature/Task 정의 (이 문서) ✅
        ↓
단계 3: Task 1.1.1 개발 (Unit TDD: Red-Green-Refactor-Mutation)
        ↓
단계 4: Task 1.1.2-1.1.5 개발 (동일)
        ↓
단계 5: ✅ Feature 1.1 Integration TDD 작성 ⬆️
        (Task 5개 결과 참고 + PRD 싱크)
        ↓
단계 6: Feature 1.2, 1.3 동일 반복
        ↓
단계 7: ✅ Block 1 Module TDD 작성 ⬆️
        (Feature 3개 결과 참고 + PRD 싱크)
```

**중요:**
- Task는 **Red-Green-Refactor-Mutation 4단계 모두 완료 후** 체크
- Feature Integration TDD는 **Task 5개 모두 완료 후** 작성 (Task 개발 중 작성 ❌)
- Block Module TDD는 **Feature 3개 Integration TDD 모두 완료 후** 작성 (Feature 개발 중 작성 ❌)

---

## 🛠️ 기술 스택 (Block 1)

```json
{
  "dependencies": {
    "three": "^0.160.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.92.0",
    "cannon-es": "^0.20.0"
  }
}
```

**라이브러리 상세:**

| 라이브러리 | 버전 | 용도 | Feature 매핑 |
|-----------|------|------|-------------|
| `three` | ^0.160.0 | 3D 렌더링 엔진 | 전체 |
| `@react-three/fiber` | ^8.15.0 | React Three.js 통합, 이벤트 시스템 | Feature 1.1 |
| `@react-three/drei` | ^9.92.0 | 카메라 헬퍼 (OrbitControls, PerspectiveCamera) | Feature 1.3 |
| `cannon-es` | ^0.20.0 | 물리 엔진 (비행 역학, 중력, 관성) | Feature 1.2 |

---

## Feature 1.1: 입력 처리 시스템 (Input Handler)

### Feature 1.1 정의

**한 줄 요약:**
> 키보드(WASD, Arrow Keys)와 마우스 입력을 실시간으로 감지하고, 버퍼링 및 보간을 통해 부드럽고 정확한 비행 조작 신호를 생성하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: 입력 응답 시간 < 16ms 달성

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 1.1.1: 키보드 입력 감지

**작업 목표:** WASD 및 Arrow Keys 입력을 실시간으로 감지하고 상태로 저장

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t1-keyboard-input.ts`
- 테스트: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t1-keyboard-input.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] WASD, Arrow Keys 모두 감지
- [ ] keydown/keyup 이벤트 처리
- [ ] 동시 입력 지원 (예: W+A 동시 입력)

**핵심 로직:**
```typescript
// 입력 상태 타입 정의
interface KeyboardState {
  forward: boolean;   // W, ArrowUp
  backward: boolean;  // S, ArrowDown
  left: boolean;      // A, ArrowLeft
  right: boolean;     // D, ArrowRight
}

// 이벤트 리스너 등록
// 상태 업데이트 (명시적 boolean)
// 메모리 리크 방지 (cleanup)
```

---

### Task 1.1.2: 마우스 입력 처리

**작업 목표:** 마우스 이동 및 클릭을 감지하여 카메라 회전/비행 방향 조정 신호 생성

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t2-mouse-input.ts`
- 테스트: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t2-mouse-input.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 마우스 이동 델타 계산
- [ ] 마우스 클릭 감지
- [ ] Pointer Lock API 지원 (옵션)

**핵심 로직:**
```typescript
// 마우스 상태 타입
interface MouseState {
  deltaX: number;  // 수평 이동량
  deltaY: number;  // 수직 이동량
  isClicked: boolean;
}

// mousemove 이벤트 처리
// 델타 계산 및 정규화
// Pointer Lock 처리 (옵션)
```

---

### Task 1.1.3: 입력 버퍼링 & 보간

**작업 목표:** 입력 신호를 버퍼에 저장하고 보간하여 부드러운 움직임 제공

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t3-input-buffering.ts`
- 테스트: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t3-input-buffering.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 입력 큐 구현 (FIFO)
- [ ] Lerp (선형 보간) 구현
- [ ] 프레임 독립적 보간 (delta time)

**핵심 로직:**
```typescript
// 버퍼 타입
interface InputBuffer {
  queue: InputSnapshot[];
  maxSize: number;
}

// Lerp 함수
function lerp(start: number, end: number, t: number): number {
  return start + (end - start) * t;
}

// 버퍼에서 값 읽기 및 보간
```

---

### Task 1.1.4: 입력 매핑 설정

**작업 목표:** 사용자 키 설정을 저장하고 런타임에 변경 가능한 입력 매핑 시스템 구현

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t4-input-mapping.ts`
- 테스트: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t4-input-mapping.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 키 매핑 저장/로드 (LocalStorage)
- [ ] 기본 설정 제공
- [ ] 중복 키 방지

**핵심 로직:**
```typescript
// 매핑 타입
interface InputMapping {
  forward: string[];   // ['W', 'ArrowUp']
  backward: string[];
  left: string[];
  right: string[];
}

// 매핑 검증
// LocalStorage 저장/로드
// 런타임 변경 지원
```

---

### Task 1.1.5: 입력 UI 피드백

**작업 목표:** 현재 입력 상태를 시각적으로 표시하는 UI 컴포넌트 (디버그/학습용)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t5-input-ui-feedback.tsx`
- 테스트: `src/blocks/block1-flight-control/features/f1-input-handler/tasks/t5-input-ui-feedback.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] React 컴포넌트 렌더링
- [ ] 입력 상태 실시간 표시
- [ ] 토글 가능 (on/off)

**핵심 로직:**
```typescript
// UI 컴포넌트
interface InputFeedbackProps {
  keyboardState: KeyboardState;
  mouseState: MouseState;
  visible: boolean;
}

// 활성화된 키 하이라이트
// FPS 카운터 통합 (옵션)
```

---

### Feature 1.1 Integration Test

**작성 시점:** Task 1.1.1-1.1.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block1-flight-control/features/f1-input-handler/f1-input-handler.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 키보드 입력 → 버퍼링 → 보간 → UI 피드백 전체 흐름
2. **시나리오 2**: 마우스 입력 → 델타 계산 → 상태 업데이트
3. **시나리오 3**: 입력 매핑 변경 → 런타임 적용 → LocalStorage 저장
4. **시나리오 4**: 동시 입력 (키보드+마우스) → 충돌 없음
5. **시나리오 5**: 입력 응답 시간 < 16ms 검증 (PRD Metric)

**PRD 싱크 포인트:**
- [ ] 입력 응답 시간 < 16ms 달성
- [ ] 모든 입력 디바이스 정상 작동
- [ ] UI 피드백 정확성

---

## Feature 1.2: 비행 물리 엔진 (Flight Physics Engine)

### Feature 1.2 정의

**한 줄 요약:**
> cannon-es 물리 엔진을 사용하여 종이비행기의 추력, 항력, 양력, 중력, 관성을 시뮬레이션하고 현실감 있는 비행 역학을 구현하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: FPS ≥ 60 달성

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 1.2.1: 물리 엔진 초기화

**작업 목표:** cannon-es World 생성 및 기본 설정 (중력, 시간 단계)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t1-physics-init.ts`
- 테스트: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t1-physics-init.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] cannon-es World 생성
- [ ] 중력 설정 (Vec3)
- [ ] 시간 단계 설정 (1/60초)

**핵심 로직:**
```typescript
import * as CANNON from 'cannon-es';

// World 초기화
const world = new CANNON.World();
world.gravity.set(0, -9.82, 0); // 중력 (m/s²)
world.broadphase = new CANNON.NaiveBroadphase();
world.solver.iterations = 10;

// 시간 단계
const fixedTimeStep = 1 / 60;
```

---

### Task 1.2.2: 비행기 리지드바디 생성

**작업 목표:** 종이비행기의 물리 바디 (질량, 형태, 관성) 생성

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t2-plane-rigidbody.ts`
- 테스트: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t2-plane-rigidbody.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] Body 생성 (Box 또는 Convex)
- [ ] 질량 설정 (0.1kg, 가벼움)
- [ ] 초기 위치/회전 설정

**핵심 로직:**
```typescript
// 비행기 바디
const planeShape = new CANNON.Box(new CANNON.Vec3(0.5, 0.1, 0.2));
const planeBody = new CANNON.Body({
  mass: 0.1,
  shape: planeShape,
  position: new CANNON.Vec3(0, 5, 0)
});

world.addBody(planeBody);
```

---

### Task 1.2.3: 비행 역학 구현

**작업 목표:** 추력, 항력, 양력 계산 및 적용

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t3-flight-dynamics.ts`
- 테스트: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t3-flight-dynamics.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 추력 계산 (입력 → 힘)
- [ ] 항력 계산 (속도 제곱)
- [ ] 양력 계산 (속도 × 각도)

**핵심 로직:**
```typescript
// 추력 (Thrust)
const thrust = new CANNON.Vec3(0, 0, -forwardInput * thrustForce);
planeBody.applyLocalForce(thrust, new CANNON.Vec3(0, 0, 0));

// 항력 (Drag)
const velocity = planeBody.velocity;
const drag = velocity.scale(-dragCoefficient * velocity.length());
planeBody.applyForce(drag, planeBody.position);

// 양력 (Lift)
const lift = new CANNON.Vec3(0, liftCoefficient * Math.abs(velocity.z), 0);
planeBody.applyForce(lift, planeBody.position);
```

---

### Task 1.2.4: 중력 및 관성 처리

**작업 목표:** 중력 적용 및 각운동량/선운동량 댐핑

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t4-gravity-inertia.ts`
- 테스트: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t4-gravity-inertia.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 중력 영향 확인
- [ ] 선운동량 댐핑 (linearDamping)
- [ ] 각운동량 댐핑 (angularDamping)

**핵심 로직:**
```typescript
// 댐핑 설정 (공기 저항)
planeBody.linearDamping = 0.1;  // 0-1 (1=즉시 정지)
planeBody.angularDamping = 0.3;

// 중력은 World에서 자동 적용됨
```

---

### Task 1.2.5: 물리 시뮬레이션 업데이트 루프

**작업 목표:** 프레임마다 물리 엔진 업데이트 및 Three.js 동기화

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t5-physics-loop.ts`
- 테스트: `src/blocks/block1-flight-control/features/f2-flight-physics/tasks/t5-physics-loop.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] requestAnimationFrame 사용
- [ ] delta time 계산
- [ ] Three.js 위치/회전 동기화

**핵심 로직:**
```typescript
// 업데이트 루프
function update(deltaTime: number) {
  // 물리 시뮬레이션 (고정 시간 단계)
  world.step(fixedTimeStep, deltaTime, 3);

  // Three.js 동기화
  planeMesh.position.copy(planeBody.position);
  planeMesh.quaternion.copy(planeBody.quaternion);
}

// useFrame 훅 (React Three Fiber)
useFrame((state, delta) => {
  update(delta);
});
```

---

### Feature 1.2 Integration Test

**작성 시점:** Task 1.2.1-1.2.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block1-flight-control/features/f2-flight-physics/f2-flight-physics.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 물리 엔진 초기화 → 비행기 바디 생성 → World 추가
2. **시나리오 2**: 입력 → 추력 적용 → 속도 변화 확인
3. **시나리오 3**: 중력 작용 → 낙하 확인 → 양력으로 상승
4. **시나리오 4**: 60FPS 유지 (1000 프레임 시뮬레이션)
5. **시나리오 5**: Three.js 동기화 정확성

**PRD 싱크 포인트:**
- [ ] FPS ≥ 60 달성
- [ ] 비행 역학 현실감 검증
- [ ] 물리 시뮬레이션 안정성

---

## Feature 1.3: 카메라 시스템 (Camera System)

### Feature 1.3 정의

**한 줄 요약:**
> 비행기를 부드럽게 추적하고, 사용자가 설정한 오프셋과 각도 제한을 유지하며, lerp/slerp로 자연스러운 카메라 이동을 제공하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: 직관적 카메라 (플레이어 피드백)

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 1.3.1: 카메라 초기 설정

**작업 목표:** PerspectiveCamera 생성 및 기본 파라미터 설정

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t1-camera-init.ts`
- 테스트: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t1-camera-init.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] PerspectiveCamera 생성
- [ ] FOV, aspect, near, far 설정
- [ ] 초기 위치/회전

**핵심 로직:**
```typescript
import { PerspectiveCamera } from 'three';

// 카메라 생성
const camera = new PerspectiveCamera(
  75,                        // fov
  window.innerWidth / window.innerHeight, // aspect
  0.1,                       // near
  1000                       // far
);

camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
```

---

### Task 1.3.2: 카메라 추적 로직

**작업 목표:** 비행기 위치를 따라가는 카메라 로직 구현

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30min)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t2-camera-follow.ts`
- 테스트: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t2-camera-follow.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 타겟(비행기) 추적
- [ ] lookAt 업데이트

**핵심 로직:**
```typescript
// 추적 로직
function followTarget(camera: Camera, target: Object3D) {
  // 타겟 위치 + 오프셋
  const targetPosition = target.position.clone();

  // 카메라가 타겟을 바라봄
  camera.lookAt(targetPosition);
}
```

---

### Task 1.3.3: 카메라 오프셋 및 거리 조절

**작업 목표:** 비행기로부터의 오프셋 (뒤쪽, 위쪽) 설정 및 거리 조절

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t3-camera-offset.ts`
- 테스트: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t3-camera-offset.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 오프셋 벡터 설정
- [ ] 거리 조절 (줌 in/out)

**핵심 로직:**
```typescript
// 오프셋 설정
const offset = new Vector3(0, 3, 8); // (x, y, z)
// x: 좌/우, y: 위/아래, z: 앞/뒤

// 카메라 위치 = 타겟 위치 + 회전된 오프셋
const rotatedOffset = offset.applyQuaternion(target.quaternion);
camera.position.copy(target.position).add(rotatedOffset);
```

---

### Task 1.3.4: 카메라 스무스 이동

**작업 목표:** lerp/slerp를 사용한 부드러운 카메라 이동

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t4-camera-smooth.ts`
- 테스트: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t4-camera-smooth.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] lerp (위치 보간)
- [ ] slerp (회전 보간, 옵션)

**핵심 로직:**
```typescript
// Lerp (선형 보간)
camera.position.lerp(targetPosition, lerpFactor);

// lerpFactor = 1 - Math.pow(0.001, deltaTime)
// deltaTime이 크면 빠르게, 작으면 부드럽게
```

---

### Task 1.3.5: 카메라 제약 조건

**작업 목표:** 카메라 경계, 각도 제한, 충돌 방지

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t5-camera-constraints.ts`
- 테스트: `src/blocks/block1-flight-control/features/f3-camera-system/tasks/t5-camera-constraints.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 최소/최대 거리 제한
- [ ] 각도 제한 (pitch, yaw)
- [ ] 지면 충돌 방지

**핵심 로직:**
```typescript
// 거리 제한
const distance = camera.position.distanceTo(target.position);
if (distance < minDistance) {
  camera.position.setLength(minDistance);
}
if (distance > maxDistance) {
  camera.position.setLength(maxDistance);
}

// 지면 충돌 방지
if (camera.position.y < groundHeight + 1) {
  camera.position.y = groundHeight + 1;
}
```

---

### Feature 1.3 Integration Test

**작성 시점:** Task 1.3.1-1.3.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block1-flight-control/features/f3-camera-system/f3-camera-system.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 카메라 초기화 → 비행기 추적 → 오프셋 적용
2. **시나리오 2**: 비행기 급격한 회전 → 카메라 스무스 추적
3. **시나리오 3**: 비행기 급강하 → 카메라 지면 충돌 방지
4. **시나리오 4**: 거리 제한 (줌 in/out) 정상 작동
5. **시나리오 5**: 60FPS 유지 (카메라 업데이트 성능)

**PRD 싱크 포인트:**
- [ ] 직관적 카메라 (플레이어 테스트)
- [ ] FPS ≥ 60 유지
- [ ] 카메라 버그 없음 (떨림, 뚫림 등)

---

## Block 1 Module Test

**작성 시점:** Feature 1.1, 1.2, 1.3 Integration Test 모두 완료 후 ⬆️

**파일:** `src/blocks/block1-flight-control/block1.module.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 전체 흐름 (입력 → 물리 → 카메라)
   - 키보드 입력 → 물리 엔진 추력 적용 → 비행기 이동 → 카메라 추적
2. **시나리오 2**: 성능 테스트
   - 1000 프레임 시뮬레이션 → FPS ≥ 60 유지
3. **시나리오 3**: 경계 테스트
   - 최대 속도, 최대 높이 도달 → 정상 작동
4. **시나리오 4**: 충돌 없음
   - 입력 시스템 ↔ 물리 엔진 ↔ 카메라 간 충돌 없음
5. **시나리오 5**: PRD Success Metrics 검증
   - 입력 응답 시간 < 16ms
   - FPS ≥ 60
   - 직관적 조작 (튜토리얼 없이 3회 시도 내 골인 가능 - 수동 테스트)

**PRD 싱크 포인트:**
- [ ] 입력 응답 시간 < 16ms
- [ ] FPS ≥ 60
- [ ] 직관적 조작 검증 (베타 테스터 피드백)
- [ ] Block 1 완성 기준 모두 충족

---

## 📊 Block 1 완료 체크리스트

### Feature 완료
- [ ] Feature 1.1: 입력 처리 시스템 (Task 5개 + Integration TDD)
- [ ] Feature 1.2: 비행 물리 엔진 (Task 5개 + Integration TDD)
- [ ] Feature 1.3: 카메라 시스템 (Task 5개 + Integration TDD)

### 테스트 완료
- [ ] Task Unit Tests 15개 모두 통과
- [ ] Feature Integration Tests 3개 모두 통과
- [ ] Block Module Test 통과
- [ ] 커버리지 > 90%
- [ ] Mutation Score > 80%

### PRD Success Metrics
- [ ] 입력 응답 시간 < 16ms
- [ ] FPS ≥ 60
- [ ] 직관적 조작 (튜토리얼 없이 3회 시도 내 골인)

### 품질 기준
- [ ] 모든 파일 < 200줄
- [ ] 모든 함수 < 50줄
- [ ] 복잡도 < 10
- [ ] ESLint 오류 0개
- [ ] Prettier 적용

---

## 🚀 다음 단계

Block 1 완료 후:
1. **Block 2: Game Core System 설계** (`doc/Block2_Game_Core.md`)
2. **Block 3: Social System 설계** (`doc/Block3_Social.md`)
3. **개발 킥오프** - "개발 시작해" 트리거
4. **Block 1 Feature 1 Task 1 TDD 개발 시작**

---

**문서 버전:** 1.0
**마지막 업데이트:** 2025-11-08
**작성자:** Claude Code (TDD 전문 개발 에이전트)
