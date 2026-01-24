# 세션 메모: Feature 4.5 Sound System 개발 (4/5 완료)

**날짜:** 2025-11-09 12:05-12:17
**세션 목표:** Feature 4.5 Sound & Effects System 완료 (Task 4.5.1~4.5.5)
**진행 상황:** Task 4.5.1~4.5.4 완료 (4/5), Task 4.5.5 대기 중

---

## 1. 작업 내용 요약

### ✅ Task 4.5.1: Audio Manager (12:05 완료)
- **Red:** AudioManager.test.ts (25 tests) - Howler.js 래퍼 테스트
- **Green:** AudioManager.ts (160줄) - loadSound/play/pause/stop/setVolume/dispose
- **Refactor:** clampVolume() private 메서드 추출, PRELOAD 상수 추가
- **Mutation:** 84.21% (목표 60% 대비 +24.21%p)
- **핵심:** Howler.js 래퍼, 비동기 loadSound (Promise), Master volume 패턴

### ✅ Task 4.5.2: Background Music (12:06 완료)
- **Red:** BackgroundMusic.test.ts (21 tests) - 메뉴/게임플레이 BGM
- **Green:** BackgroundMusic.ts (88줄) - playMenu/playGameplay, 자동 루프, 이전 음악 정지
- **Refactor:** LOOP_ENABLED 상수 추가
- **Mutation:** 95.24% (목표 60% 대비 +35.24%p)
- **핵심:** stopCurrent() 자동 정지, currentTrack 상태, Promise.all 병렬 로딩

### ✅ Task 4.5.3: Sound Effects (12:07 완료)
- **Red:** SoundEffects.test.ts (29 tests) - 5개 효과음 (engine/wind/collision/checkpoint/fanfare)
- **Green:** SoundEffects.ts (120줄) - 각 효과음별 play/stop 메서드
- **Refactor:** ALL_SOUND_KEYS 배열 추출, forEach DRY 패턴
- **Mutation:** 100.00% 🏆 (완벽!)
- **핵심:** forEach 일괄 처리, 동시 재생 지원

### ✅ Task 4.5.4: Volume Control Integration (12:15 완료)
- **Red:** volumeStore.test.ts (21 tests) - master/music/sfx 볼륨, localStorage 연동
- **Green:** volumeStore.ts (93줄) - Zustand 스토어, 자동 저장/복원
- **Refactor:** LocalStorage key 상수 추출 (MASTER_VOLUME_KEY 등)
- **Mutation:** 90.00% (목표 60% 대비 +30%p)
- **핵심:** clampVolume 헬퍼, parseFloat + isNaN 검증

### ⏳ Task 4.5.5: Audio Integration Test (대기 중)
- Feature 레벨 통합 테스트 예정
- AudioManager + BackgroundMusic + SoundEffects + VolumeStore 연동 검증

---

## 2. 핵심 결정사항

### Howler.js Mock 패턴 (Critical!)
```typescript
// ❌ 작동 안 함
vi.mock('howler', () => ({
  Howl: vi.fn().mockImplementation(() => ({ ... }))
}));

// ✅ 작동함
vi.mock('howler', () => ({
  Howl: vi.fn(function (this: any) {
    Object.assign(this, mockHowlInstance);
    return this;
  }) as any,
}));
```
**이유:** Vitest는 `new` 키워드로 생성자를 호출할 때 constructor function 패턴 필요

### LocalStorage Mock 패턴
```typescript
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value; },
    clear: () => { store = {}; },
  };
})();

Object.defineProperty(global, 'localStorage', {
  value: localStorageMock,
});
```
**이유:** Node 환경에는 localStorage가 없으므로 closure 패턴으로 mock 구현

### Stryker 설정 위치
- ❌ `/tmp/stryker_config.json` → NaN 에러, 멈춤
- ✅ `프로젝트_루트/stryker.conf.json` → 정상 작동
- **학습:** Stryker는 프로젝트 루트 기준으로 경로 해석

---

## 3. 기술적 패턴

### DRY 패턴: forEach + 상수 배열
```typescript
// Before (10줄 반복)
stopAll(): void {
  this.audioManager.stop(ENGINE_SOUND_KEY);
  this.audioManager.stop(WIND_SOUND_KEY);
  this.audioManager.stop(COLLISION_KEY);
  this.audioManager.stop(CHECKPOINT_KEY);
  this.audioManager.stop(RESULT_FANFARE_KEY);
}

// After (4줄, DRY)
private static readonly ALL_SOUND_KEYS = [
  SoundEffects.ENGINE_SOUND_KEY, /* ... */
];

stopAll(): void {
  SoundEffects.ALL_SOUND_KEYS.forEach((key) => {
    this.audioManager.stop(key);
  });
}
```

### Volume Clamping 패턴
```typescript
const clampVolume = (volume: number): number => {
  return Math.max(MIN_VOLUME, Math.min(MAX_VOLUME, volume));
};
```
**장점:** 0-1 범위 자동 보장, 여러 곳에서 재사용

### Promise.all 병렬 로딩
```typescript
async loadAll(): Promise<boolean> {
  const results = await Promise.all([
    this.audioManager.loadSound(key1, path1),
    this.audioManager.loadSound(key2, path2),
  ]);
  return results.every((result) => result === true);
}
```
**장점:** 순차 로딩 대비 N배 빠름, every()로 전체 성공 검증

---

## 4. Mutation Testing 결과

| Task | Mutation Score | Survived | 비고 |
|------|----------------|----------|------|
| 4.5.1 AudioManager | 84.21% | 3 | console.error 메시지 (정상) |
| 4.5.2 BackgroundMusic | 95.24% | 1 | if (this.currentTrack) 경계값 (정상) |
| 4.5.3 SoundEffects | 100.00% | 0 | 완벽! 🏆 |
| 4.5.4 VolumeStore | 90.00% | 2 | fallback 문자열 (정상) |

**평균:** 92.36% (목표 60% 대비 +32.36%p)

---

## 5. 파일 구조

```
src/blocks/block4-ui-ux/features/f5-sound-system/
├── core/
│   ├── AudioManager.ts (160줄) ✅
│   └── AudioManager.test.ts (227줄, 25 tests) ✅
├── music/
│   ├── BackgroundMusic.ts (88줄) ✅
│   └── BackgroundMusic.test.ts (177줄, 21 tests) ✅
├── sfx/
│   ├── SoundEffects.ts (120줄) ✅
│   └── SoundEffects.test.ts (206줄, 29 tests) ✅
├── state/
│   ├── volumeStore.ts (93줄) ✅
│   └── volumeStore.test.ts (177줄, 21 tests) ✅
└── f5-sound-system.integration.test.ts (대기 중) ⏳
```

**총 줄 수:** 1,248줄 (구현 461줄 + 테스트 787줄)
**테스트 커버리지:** 100% (모든 Task)

---

## 6. 다음 단계

### Task 4.5.5: Audio Integration Test
**목표:** Feature 레벨 통합 테스트

**테스트 시나리오 (예상):**
1. **초기화 시나리오**
   - AudioManager 생성 → BackgroundMusic/SoundEffects 연결
   - VolumeStore에서 저장된 볼륨 복원

2. **음악 재생 시나리오**
   - 메뉴 BGM 재생 → 게임플레이 BGM 전환 (자동 정지 확인)
   - 마스터 볼륨 변경 → 모든 오디오에 적용 확인

3. **효과음 재생 시나리오**
   - 여러 효과음 동시 재생
   - SFX 볼륨 변경 → 효과음에만 적용 확인

4. **볼륨 저장/복원 시나리오**
   - 볼륨 변경 → LocalStorage 저장 확인
   - 페이지 새로고침 시뮬레이션 → 복원 확인

5. **리소스 정리 시나리오**
   - dispose() 호출 → 모든 리소스 정리 확인

**예상 테스트 수:** ~15개
**예상 소요 시간:** 90분 (TDD 4단계)

---

## 7. 작업 진행률

**전체 진행률:** 98.6% (69/70 Tasks)

```
Block 4: UI/UX System
├── Feature 4.4: 3D Environment Integration ✅ (15/15)
└── Feature 4.5: Sound & Effects System ⏳ (4/5)
    ├── Task 4.5.1: Audio Manager ✅
    ├── Task 4.5.2: Background Music ✅
    ├── Task 4.5.3: Sound Effects ✅
    ├── Task 4.5.4: Volume Control Integration ✅
    └── Task 4.5.5: Audio Integration Test ⏳
```

---

## 8. 트러블슈팅 기록

### 문제 1: Howler mock "is not a constructor" 에러
- **원인:** `vi.fn().mockImplementation()` 패턴은 constructor 지원 안 함
- **해결:** `vi.fn(function (this: any) { ... })` 패턴 사용
- **영향:** Task 4.5.1, 4.5.2, 4.5.3 모두 동일 패턴 적용

### 문제 2: Stryker NaN 에러 및 멈춤
- **원인:** `/tmp` 경로의 config 파일이 프로젝트 context 인식 실패
- **해결:** 프로젝트 루트에 `stryker.conf.json` 배치
- **학습:** Stryker는 프로젝트 루트 기준 상대 경로 사용

### 문제 3: LocalStorage undefined (Node 환경)
- **원인:** Node.js에는 browser API인 localStorage 없음
- **해결:** Closure 패턴으로 mock 구현 후 global에 정의
- **학습:** Browser API는 테스트 환경에서 명시적 mock 필요

---

## 9. 학습 내용

### Howler.js 사용법
- `new Howl({ src, preload })` 생성
- `on('load')`, `on('loaderror')` 이벤트 기반 로딩
- `play()`, `pause()`, `stop()` 제어
- `volume()`, `loop()` 설정
- `unload()` 리소스 정리

### Zustand 사용법
- `create<T>((set) => ({ ... }))` 타입 안전 스토어
- `set()` 함수로 상태 업데이트
- `useStore.getState()` 테스트에서 직접 접근
- `useStore.setState()` 테스트 초기화

### Mutation Testing 인사이트
- Console.log/error는 mutation 대상이지만 kill 불필요 (정상)
- Fallback 문자열 변경은 survived 가능 (정상)
- 100% score는 어렵지만 90%+ 충분히 달성 가능
- Static mutants (상수)는 성능 저하 원인

---

## 10. 품질 지표

| 지표 | 목표 | 실제 | 결과 |
|------|------|------|------|
| 테스트 커버리지 | >90% | 100% | ✅ |
| Mutation Score | >60% | 92.36% | ✅ |
| 파일 크기 | <200줄 | 평균 115줄 | ✅ |
| 복잡도 | <10 | <5 | ✅ |
| TDD 준수 | Red-Green-Refactor-Mutation | 4/4 단계 | ✅ |

---

## 11. 다음 세션 체크리스트

- [ ] Task 4.5.5: Audio Integration Test 시작
- [ ] 15개 통합 테스트 시나리오 작성 (Red)
- [ ] Feature 통합 구현 (Green)
- [ ] Refactor 적용
- [ ] Mutation Testing (목표 >80%)
- [ ] Feature 4.5 완료 후 Block 4 Module Test 시작

**예상 남은 시간:** 2시간 (Task 4.5.5: 90분, Block Test: 30분)

---

## 12. 참고 사항

### PRD 싱크 확인 완료 항목
- ✅ Howler.js 기반 오디오 관리 (~10KB)
- ✅ 메뉴/게임플레이 배경음악 자동 루프
- ✅ 5개 효과음 (engine/wind/collision/checkpoint/fanfare)
- ✅ 마스터/음악/효과음 독립 볼륨 제어
- ✅ LocalStorage 볼륨 저장/복원
- ⏳ 통합 테스트 (다음 Task)

### 기술 스택
- Howler.js 2.2.4 (오디오 라이브러리)
- Zustand 4.4.7 (상태 관리)
- Vitest 1.0.0 (테스팅)
- Stryker 8.x (Mutation Testing)

---

**세션 종료 시각:** 2025-11-09 12:17
**다음 세션 시작 예정:** Task 4.5.5 Audio Integration Test
