## 관련 문서
- [[../CJ_AI_개발방법론|CJ_AI_개발방법론]] - 전체 방법론
- [[./Product_PRD_종이비행기날아라|Product PRD]] - 상위 PRD
- [[./Block_템플릿_통합|Block 템플릿]] - 템플릿 참조
- [[./Block1_Flight_Control|Block 1: Flight Control]] - 이전 Block (의존성)

---

# Block 2: 게임 코어 시스템 (Game Core)

**작성일:** 2025-11-08
**작성자:** AI (Claude Code) - TDD 전문 개발 에이전트
**버전:** 1.0
**상태:** 진행 중

**소속 Product:** [[./Product_PRD_종이비행기날아라|종이비행기 날아라]]

---

## 📋 Block 정의

**한 줄 요약:**
> 타임어택 게임의 핵심 로직으로, 코스(시작점/골인점/장애물)를 관리하고, 시간을 측정하며, 충돌을 감지하여 게임 상태를 제어하는 시스템

**담당 Features:** 3개
- Feature 2.1: 코스 관리 시스템 (Course Manager)
- Feature 2.2: 타이머 & 기록 시스템 (Timer & Record)
- Feature 2.3: 충돌 감지 & 게임 상태 관리 (Collision & State)

**완성 기준:**
- [ ] Feature 3개 Integration Test 모두 통과
- [ ] Block Module Test 통과
- [ ] PRD Success Metrics 달성:
  - [ ] 초기 로딩 시간 < 3초
  - [ ] FPS ≥ 60 (장애물 50개 이상 배치 시)
  - [ ] 타이머 정확도 ±10ms 이내

**예상 소요 시간:** 1주 (Feature 3개 × 2일 + Module TDD 1일)

**Block 1 의존성:**
- Block 1 (Flight Control)의 비행기 위치/속도 데이터 필요
- Block 1 완료 후 진행 권장

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 읽기 ✅
        ↓
단계 2: Block/Feature/Task 정의 (이 문서) ✅
        ↓
단계 3: Task 2.1.1 개발 (Unit TDD: Red-Green-Refactor-Mutation)
        ↓
단계 4: Task 2.1.2-2.1.5 개발 (동일)
        ↓
단계 5: ✅ Feature 2.1 Integration TDD 작성 ⬆️
        (Task 5개 결과 참고 + PRD 싱크)
        ↓
단계 6: Feature 2.2, 2.3 동일 반복
        ↓
단계 7: ✅ Block 2 Module TDD 작성 ⬆️
        (Feature 3개 결과 참고 + PRD 싱크)
```

**중요:**
- Task는 **Red-Green-Refactor-Mutation 4단계 모두 완료 후** 체크
- Feature Integration TDD는 **Task 5개 모두 완료 후** 작성 (Task 개발 중 작성 ❌)
- Block Module TDD는 **Feature 3개 Integration TDD 모두 완료 후** 작성 (Feature 개발 중 작성 ❌)

---

## 🛠️ 기술 스택 (Block 2)

```json
{
  "dependencies": {
    "zustand": "^4.4.7",
    "@react-three/rapier": "^1.2.1",
    "date-fns": "^3.0.0"
  }
}
```

**라이브러리 상세:**

| 라이브러리 | 버전 | 용도 | Feature 매핑 |
|-----------|------|------|-------------|
| `zustand` | ^4.4.7 | 경량 상태 관리 (게임 상태, 타이머, 코스) | Feature 2.1, 2.2, 2.3 |
| `@react-three/rapier` | ^1.2.1 | 고성능 충돌 감지 (장애물 50개 이상) | Feature 2.3 |
| `date-fns` | ^3.0.0 | 타이머 포맷팅 (mm:ss.ms) | Feature 2.2 |

**대체 옵션:**
- `@react-three/rapier` → Three.js 내장 `Raycaster` (장애물 < 50개 시 더 경량)
- **결정 기준**: 장애물 수에 따라 Task 2.3.1에서 선택

---

## Feature 2.1: 코스 관리 시스템 (Course Manager)

### Feature 2.1 정의

**한 줄 요약:**
> 시작점, 골인점, 장애물을 3D 공간에 배치하고, 코스 데이터를 로드/언로드하며, 프리뷰 및 미니맵을 제공하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: 초기 로딩 시간 < 3초 달성

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 2.1.1: 시작점/골인점 생성

**작업 목표:** 시작점과 골인점을 3D 메쉬로 생성하고 위치 설정

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t1-start-finish-points.ts`
- 테스트: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t1-start-finish-points.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 시작점 메쉬 생성 (초록색 링)
- [ ] 골인점 메쉬 생성 (빨간색 링)
- [ ] 위치 설정 (Vector3)

**핵심 로직:**
```typescript
import { Mesh, RingGeometry, MeshBasicMaterial } from 'three';

// 시작점 (초록색 링)
const startRing = new Mesh(
  new RingGeometry(2, 2.5, 32),
  new MeshBasicMaterial({ color: 0x00ff00, side: DoubleSide })
);
startRing.position.set(0, 5, 0);
startRing.rotation.x = Math.PI / 2;

// 골인점 (빨간색 링)
const finishRing = new Mesh(
  new RingGeometry(2, 2.5, 32),
  new MeshBasicMaterial({ color: 0xff0000, side: DoubleSide })
);
finishRing.position.set(0, 5, -100);
finishRing.rotation.x = Math.PI / 2;
```

---

### Task 2.1.2: 장애물 배치 시스템

**작업 목표:** 다양한 형태의 장애물(큐브, 구, 실린더)을 배치하는 시스템

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t2-obstacle-placement.ts`
- 테스트: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t2-obstacle-placement.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 큐브/구/실린더 장애물 생성
- [ ] 랜덤 배치 또는 고정 배치
- [ ] 장애물 배열 반환

**핵심 로직:**
```typescript
interface Obstacle {
  type: 'box' | 'sphere' | 'cylinder';
  position: Vector3;
  size: Vector3;
  mesh: Mesh;
}

// 장애물 생성 팩토리
function createObstacle(type: string, position: Vector3): Obstacle {
  let geometry;
  if (type === 'box') geometry = new BoxGeometry(2, 2, 2);
  else if (type === 'sphere') geometry = new SphereGeometry(1, 16, 16);
  else geometry = new CylinderGeometry(1, 1, 3, 16);

  const mesh = new Mesh(
    geometry,
    new MeshStandardMaterial({ color: 0x888888 })
  );
  mesh.position.copy(position);

  return { type, position, size: new Vector3(2, 2, 2), mesh };
}

// 장애물 배치
const obstacles: Obstacle[] = [];
for (let i = 0; i < 20; i++) {
  const pos = new Vector3(
    Math.random() * 40 - 20,
    Math.random() * 10 + 5,
    -i * 5 - 10
  );
  obstacles.push(createObstacle('box', pos));
}
```

---

### Task 2.1.3: 코스 데이터 구조 정의

**작업 목표:** 코스 전체 데이터를 JSON으로 정의하고 타입 정의

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t3-course-data-structure.ts`
- 테스트: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t3-course-data-structure.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] CourseData 타입 정의
- [ ] JSON 스키마 검증
- [ ] 샘플 코스 3개 제공

**핵심 로직:**
```typescript
interface CourseData {
  id: string;
  name: string;
  difficulty: 'easy' | 'medium' | 'hard';
  startPoint: { x: number; y: number; z: number };
  finishPoint: { x: number; y: number; z: number };
  obstacles: Array<{
    type: 'box' | 'sphere' | 'cylinder';
    position: { x: number; y: number; z: number };
    size: { x: number; y: number; z: number };
  }>;
  bestTime?: number; // 최고 기록 (ms)
}

// 샘플 코스
const course1: CourseData = {
  id: 'course-01',
  name: 'Tutorial Course',
  difficulty: 'easy',
  startPoint: { x: 0, y: 5, z: 0 },
  finishPoint: { x: 0, y: 5, z: -50 },
  obstacles: [
    { type: 'box', position: { x: 0, y: 5, z: -20 }, size: { x: 2, y: 2, z: 2 } },
    { type: 'sphere', position: { x: 5, y: 7, z: -30 }, size: { x: 1, y: 1, z: 1 } },
  ]
};
```

---

### Task 2.1.4: 코스 로드/언로드

**작업 목표:** 코스 데이터를 읽어 3D 씬에 로드하고, 언로드 시 메모리 정리

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t4-course-load-unload.ts`
- 테스트: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t4-course-load-unload.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 코스 로드 함수 (Scene에 추가)
- [ ] 코스 언로드 함수 (Scene에서 제거)
- [ ] 메모리 리크 방지

**핵심 로직:**
```typescript
import { Scene } from 'three';

// 코스 로드
function loadCourse(scene: Scene, courseData: CourseData): void {
  // 시작점/골인점 추가
  const startRing = createStartPoint(courseData.startPoint);
  const finishRing = createFinishPoint(courseData.finishPoint);
  scene.add(startRing);
  scene.add(finishRing);

  // 장애물 추가
  courseData.obstacles.forEach(obstacleData => {
    const obstacle = createObstacle(
      obstacleData.type,
      new Vector3(obstacleData.position.x, obstacleData.position.y, obstacleData.position.z)
    );
    scene.add(obstacle.mesh);
  });
}

// 코스 언로드
function unloadCourse(scene: Scene): void {
  // Scene에서 모든 코스 오브젝트 제거
  scene.children.forEach(child => {
    if (child.userData.isCourseObject) {
      scene.remove(child);
      // Geometry, Material dispose
      if (child instanceof Mesh) {
        child.geometry.dispose();
        (child.material as Material).dispose();
      }
    }
  });
}
```

---

### Task 2.1.5: 코스 프리뷰/미니맵

**작업 목표:** 코스 전체 레이아웃을 보여주는 미니맵 UI 컴포넌트

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t5-course-minimap.tsx`
- 테스트: `src/blocks/block2-game-core/features/f1-course-manager/tasks/t5-course-minimap.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] React 컴포넌트 렌더링
- [ ] 2D Canvas로 탑뷰 표시
- [ ] 비행기 위치 실시간 표시

**핵심 로직:**
```typescript
interface MinimapProps {
  courseData: CourseData;
  planePosition: Vector3;
}

// 미니맵 컴포넌트
function Minimap({ courseData, planePosition }: MinimapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 클리어
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 장애물 그리기 (회색 점)
    ctx.fillStyle = '#888';
    courseData.obstacles.forEach(obs => {
      ctx.fillRect(obs.position.x + 50, obs.position.z + 50, 2, 2);
    });

    // 비행기 위치 (파란색 점)
    ctx.fillStyle = '#00f';
    ctx.fillRect(planePosition.x + 50, planePosition.z + 50, 4, 4);
  }, [courseData, planePosition]);

  return <canvas ref={canvasRef} width={200} height={200} />;
}
```

---

### Feature 2.1 Integration Test

**작성 시점:** Task 2.1.1-2.1.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block2-game-core/features/f1-course-manager/f1-course-manager.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 코스 데이터 로드 → Scene에 추가 → 시작점/골인점/장애물 확인
2. **시나리오 2**: 코스 언로드 → Scene 정리 → 메모리 리크 없음
3. **시나리오 3**: 3개 코스 순차 로드 → 각 코스 정상 표시
4. **시나리오 4**: 미니맵 렌더링 → 코스 레이아웃 정확성
5. **시나리오 5**: 초기 로딩 시간 < 3초 검증 (PRD Metric)

**PRD 싱크 포인트:**
- [ ] 초기 로딩 시간 < 3초 달성
- [ ] 코스 정확히 로드됨
- [ ] 메모리 관리 정상

---

## Feature 2.2: 타이머 & 기록 시스템 (Timer & Record)

### Feature 2.2 정의

**한 줄 요약:**
> 게임 시작부터 골인까지의 시간을 측정하고, mm:ss.ms 포맷으로 표시하며, 로컬 및 서버에 최고 기록을 저장하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: 타이머 정확도 ±10ms

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 2.2.1: 타이머 시작/정지/리셋

**작업 목표:** 타이머 상태 관리 (시작, 정지, 리셋) 및 경과 시간 계산

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t1-timer-control.ts`
- 테스트: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t1-timer-control.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] start() 함수
- [ ] stop() 함수
- [ ] reset() 함수
- [ ] getElapsedTime() 함수

**핵심 로직:**
```typescript
class Timer {
  private startTime: number | null = null;
  private endTime: number | null = null;
  private isRunning: boolean = false;

  start(): void {
    this.startTime = performance.now();
    this.isRunning = true;
  }

  stop(): void {
    if (!this.isRunning) return;
    this.endTime = performance.now();
    this.isRunning = false;
  }

  reset(): void {
    this.startTime = null;
    this.endTime = null;
    this.isRunning = false;
  }

  getElapsedTime(): number {
    if (!this.startTime) return 0;
    const endTime = this.endTime || performance.now();
    return endTime - this.startTime;
  }
}
```

---

### Task 2.2.2: 시간 포맷팅 (mm:ss.ms)

**작업 목표:** 밀리초를 mm:ss.ms 포맷으로 변환 (date-fns 사용)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t2-time-formatting.ts`
- 테스트: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t2-time-formatting.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] mm:ss.ms 포맷 반환
- [ ] 경계값 테스트 (0ms, 3600000ms 등)

**핵심 로직:**
```typescript
import { format } from 'date-fns';

function formatTime(milliseconds: number): string {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const ms = Math.floor((milliseconds % 1000) / 10); // 2자리

  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(ms).padStart(2, '0')}`;
}

// 예시: 65432ms → "01:05.43"
```

---

### Task 2.2.3: 로컬 기록 저장 (LocalStorage)

**작업 목표:** 코스별 최고 기록을 LocalStorage에 저장/로드

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t3-local-record.ts`
- 테스트: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t3-local-record.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] saveRecord(courseId, time) 함수
- [ ] getRecord(courseId) 함수
- [ ] JSON 직렬화/역직렬화

**핵심 로직:**
```typescript
interface RecordData {
  courseId: string;
  bestTime: number; // ms
  timestamp: number;
}

// 기록 저장
function saveRecord(courseId: string, time: number): void {
  const records: RecordData[] = JSON.parse(
    localStorage.getItem('flightRecords') || '[]'
  );

  const existingIndex = records.findIndex(r => r.courseId === courseId);
  const newRecord: RecordData = {
    courseId,
    bestTime: time,
    timestamp: Date.now()
  };

  if (existingIndex >= 0) {
    // 기존 기록보다 빠르면 갱신
    if (time < records[existingIndex].bestTime) {
      records[existingIndex] = newRecord;
    }
  } else {
    records.push(newRecord);
  }

  localStorage.setItem('flightRecords', JSON.stringify(records));
}

// 기록 로드
function getRecord(courseId: string): number | null {
  const records: RecordData[] = JSON.parse(
    localStorage.getItem('flightRecords') || '[]'
  );
  const record = records.find(r => r.courseId === courseId);
  return record ? record.bestTime : null;
}
```

---

### Task 2.2.4: 최고 기록 관리

**작업 목표:** 현재 기록과 최고 기록 비교 및 갱신 로직

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t4-best-record.ts`
- 테스트: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t4-best-record.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 최고 기록 비교 함수
- [ ] 신기록 여부 반환

**핵심 로직:**
```typescript
function isNewRecord(courseId: string, currentTime: number): boolean {
  const bestTime = getRecord(courseId);
  return bestTime === null || currentTime < bestTime;
}

function updateBestRecord(courseId: string, time: number): {
  isNewRecord: boolean;
  improvement?: number; // ms
} {
  const oldRecord = getRecord(courseId);
  const isNew = isNewRecord(courseId, time);

  if (isNew) {
    saveRecord(courseId, time);
    return {
      isNewRecord: true,
      improvement: oldRecord ? oldRecord - time : undefined
    };
  }

  return { isNewRecord: false };
}
```

---

### Task 2.2.5: 타이머 UI 컴포넌트

**작업 목표:** 현재 시간, 최고 기록을 표시하는 React UI 컴포넌트

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t5-timer-ui.tsx`
- 테스트: `src/blocks/block2-game-core/features/f2-timer-record/tasks/t5-timer-ui.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 현재 시간 표시
- [ ] 최고 기록 표시
- [ ] 신기록 애니메이션 (옵션)

**핵심 로직:**
```typescript
interface TimerUIProps {
  currentTime: number; // ms
  bestTime: number | null; // ms
  isNewRecord: boolean;
}

function TimerUI({ currentTime, bestTime, isNewRecord }: TimerUIProps) {
  return (
    <div className="timer-ui">
      <div className="current-time">
        <span>Time: </span>
        <span className={isNewRecord ? 'new-record' : ''}>
          {formatTime(currentTime)}
        </span>
      </div>
      {bestTime !== null && (
        <div className="best-time">
          <span>Best: </span>
          <span>{formatTime(bestTime)}</span>
        </div>
      )}
    </div>
  );
}
```

---

### Feature 2.2 Integration Test

**작성 시점:** Task 2.2.1-2.2.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block2-game-core/features/f2-timer-record/f2-timer-record.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 타이머 시작 → 경과 → 정지 → 포맷팅 정확성
2. **시나리오 2**: 최초 플레이 → 기록 저장 → LocalStorage 확인
3. **시나리오 3**: 2번째 플레이 (더 빠름) → 신기록 갱신
4. **시나리오 4**: 2번째 플레이 (더 느림) → 기록 유지
5. **시나리오 5**: 타이머 정확도 ±10ms 검증 (PRD Metric)

**PRD 싱크 포인트:**
- [ ] 타이머 정확도 ±10ms
- [ ] LocalStorage 정상 작동
- [ ] UI 표시 정확성

---

## Feature 2.3: 충돌 감지 & 게임 상태 관리 (Collision & State)

### Feature 2.3 정의

**한 줄 요약:**
> 비행기와 장애물/골인점의 충돌을 감지하고, 게임 상태(Idle/Playing/Finished/Crashed)를 관리하며, 상태 전환 로직을 제어하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics: FPS ≥ 60 (장애물 50개 이상 시)

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 2.3.1: 충돌 감지 시스템 (Raycaster or Rapier)

**작업 목표:** Raycaster 또는 Rapier를 선택하여 충돌 감지 구현

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t1-collision-detection.ts`
- 테스트: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t1-collision-detection.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] Raycaster 구현 (기본)
- [ ] Rapier 구현 (옵션, 장애물 >50개 시)
- [ ] 충돌 이벤트 반환

**핵심 로직 (Raycaster):**
```typescript
import { Raycaster, Vector3, Mesh } from 'three';

function checkCollision(
  planePosition: Vector3,
  planeDirection: Vector3,
  obstacles: Mesh[]
): { collided: boolean; object?: Mesh } {
  const raycaster = new Raycaster(planePosition, planeDirection, 0, 2);
  const intersects = raycaster.intersectObjects(obstacles);

  if (intersects.length > 0) {
    return { collided: true, object: intersects[0].object as Mesh };
  }

  return { collided: false };
}
```

**핵심 로직 (Rapier 대체):**
```typescript
import { RigidBody, Collider } from '@react-three/rapier';

// Rapier는 자동으로 충돌 이벤트 발생
// onCollisionEnter, onCollisionExit 이벤트 사용
```

---

### Task 2.3.2: 게임 상태 머신 (Idle/Playing/Finished/Crashed)

**작업 목표:** 게임 상태를 관리하는 상태 머신 (State Machine) 구현

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t2-game-state-machine.ts`
- 테스트: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t2-game-state-machine.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 4가지 상태 정의
- [ ] 상태 전환 로직
- [ ] 유효하지 않은 전환 방지

**핵심 로직:**
```typescript
type GameState = 'idle' | 'playing' | 'finished' | 'crashed';

class GameStateMachine {
  private state: GameState = 'idle';

  getState(): GameState {
    return this.state;
  }

  start(): void {
    if (this.state === 'idle') {
      this.state = 'playing';
    }
  }

  finish(): void {
    if (this.state === 'playing') {
      this.state = 'finished';
    }
  }

  crash(): void {
    if (this.state === 'playing') {
      this.state = 'crashed';
    }
  }

  reset(): void {
    this.state = 'idle';
  }
}
```

---

### Task 2.3.3: 장애물 충돌 처리

**작업 목표:** 장애물과 충돌 시 게임 상태를 'crashed'로 변경

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t3-obstacle-collision.ts`
- 테스트: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t3-obstacle-collision.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 장애물 충돌 감지
- [ ] 상태 머신 호출 (crash())
- [ ] 충돌 효과 (옵션: 파티클, 사운드)

**핵심 로직:**
```typescript
function handleObstacleCollision(
  planePosition: Vector3,
  obstacles: Mesh[],
  stateMachine: GameStateMachine
): void {
  const collision = checkCollision(planePosition, new Vector3(0, 0, -1), obstacles);

  if (collision.collided) {
    stateMachine.crash();
    // 옵션: 충돌 효과
    console.log('Crashed into obstacle!');
  }
}
```

---

### Task 2.3.4: 골인 감지 및 처리

**작업 목표:** 골인점 통과 시 게임 상태를 'finished'로 변경 및 기록 저장

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t4-finish-detection.ts`
- 테스트: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t4-finish-detection.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 골인점 통과 감지
- [ ] 타이머 정지
- [ ] 기록 저장

**핵심 로직:**
```typescript
function handleFinishDetection(
  planePosition: Vector3,
  finishPoint: Vector3,
  timer: Timer,
  stateMachine: GameStateMachine,
  courseId: string
): void {
  const distance = planePosition.distanceTo(finishPoint);

  // 골인점과 거리 2 이내면 통과
  if (distance < 2) {
    timer.stop();
    const time = timer.getElapsedTime();
    stateMachine.finish();

    // 기록 저장
    const result = updateBestRecord(courseId, time);
    if (result.isNewRecord) {
      console.log(`New Record! ${formatTime(time)}`);
    }
  }
}
```

---

### Task 2.3.5: 게임 리셋 로직

**작업 목표:** 게임을 초기 상태로 되돌리는 리셋 함수

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t5-game-reset.ts`
- 테스트: `src/blocks/block2-game-core/features/f3-collision-state/tasks/t5-game-reset.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10
- [ ] 비행기 위치 리셋
- [ ] 타이머 리셋
- [ ] 상태 머신 리셋

**핵심 로직:**
```typescript
function resetGame(
  planeBody: CANNON.Body,
  startPoint: Vector3,
  timer: Timer,
  stateMachine: GameStateMachine
): void {
  // 비행기 위치/속도 리셋
  planeBody.position.set(startPoint.x, startPoint.y, startPoint.z);
  planeBody.velocity.set(0, 0, 0);
  planeBody.angularVelocity.set(0, 0, 0);
  planeBody.quaternion.set(0, 0, 0, 1);

  // 타이머 리셋
  timer.reset();

  // 상태 리셋
  stateMachine.reset();
}
```

---

### Feature 2.3 Integration Test

**작성 시점:** Task 2.3.1-2.3.5 모두 완료 후 ⬆️

**파일:** `src/blocks/block2-game-core/features/f3-collision-state/f3-collision-state.integration.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 게임 시작 → 비행 → 장애물 충돌 → 'crashed' 상태
2. **시나리오 2**: 게임 시작 → 비행 → 골인 통과 → 'finished' 상태
3. **시나리오 3**: 장애물 50개 배치 → FPS ≥ 60 유지 (PRD Metric)
4. **시나리오 4**: 리셋 후 재시작 → 정상 작동
5. **시나리오 5**: 충돌 감지 정확도 (false positive 없음)

**PRD 싱크 포인트:**
- [ ] FPS ≥ 60 (장애물 50개 이상)
- [ ] 충돌 감지 정확성
- [ ] 게임 상태 전환 정상

---

## Block 2 Module Test

**작성 시점:** Feature 2.1, 2.2, 2.3 Integration Test 모두 완료 후 ⬆️

**파일:** `src/blocks/block2-game-core/block2.module.test.ts`

**테스트 시나리오:**
1. **시나리오 1**: 전체 게임 흐름 (코스 로드 → 게임 시작 → 비행 → 골인)
   - 코스 로드 → 타이머 시작 → 비행 → 골인 감지 → 타이머 정지 → 기록 저장
2. **시나리오 2**: 충돌 시나리오
   - 게임 시작 → 장애물 충돌 → 'crashed' 상태 → 리셋 → 재시작
3. **시나리오 3**: 성능 테스트
   - 장애물 50개 → 1000 프레임 시뮬레이션 → FPS ≥ 60
4. **시나리오 4**: 기록 갱신
   - 1회차 플레이 (60초) → 2회차 플레이 (50초) → 신기록 저장 확인
5. **시나리오 5**: PRD Success Metrics 검증
   - 초기 로딩 < 3초
   - FPS ≥ 60
   - 타이머 정확도 ±10ms

**PRD 싱크 포인트:**
- [ ] 초기 로딩 시간 < 3초
- [ ] FPS ≥ 60 (장애물 50개 이상)
- [ ] 타이머 정확도 ±10ms
- [ ] Block 2 완성 기준 모두 충족

---

## 📊 Block 2 완료 체크리스트

### Feature 완료
- [ ] Feature 2.1: 코스 관리 시스템 (Task 5개 + Integration TDD)
- [ ] Feature 2.2: 타이머 & 기록 시스템 (Task 5개 + Integration TDD)
- [ ] Feature 2.3: 충돌 감지 & 게임 상태 관리 (Task 5개 + Integration TDD)

### 테스트 완료
- [ ] Task Unit Tests 15개 모두 통과
- [ ] Feature Integration Tests 3개 모두 통과
- [ ] Block Module Test 통과
- [ ] 커버리지 > 90%
- [ ] Mutation Score > 80%

### PRD Success Metrics
- [ ] 초기 로딩 시간 < 3초
- [ ] FPS ≥ 60 (장애물 50개 이상)
- [ ] 타이머 정확도 ±10ms

### 품질 기준
- [ ] 모든 파일 < 200줄
- [ ] 모든 함수 < 50줄
- [ ] 복잡도 < 10
- [ ] ESLint 오류 0개
- [ ] Prettier 적용

---

## 🚀 다음 단계

Block 2 완료 후:
1. **Block 3: Social System 설계** (`doc/Block3_Social.md`)
2. **개발 킥오프** - "개발 시작해" 트리거
3. **Block 1 → Block 2 → Block 3 순차 개발**

---

**문서 버전:** 1.0
**마지막 업데이트:** 2025-11-08
**작성자:** Claude Code (TDD 전문 개발 에이전트)
