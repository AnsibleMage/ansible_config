## 관련 문서
- [[./CJ_AI_개발방법론|CJ_AI_개발방법론]] - 전체 방법론 (이론은 여기 참조)
- [[./Product_PRD_종이비행기날아라|Product PRD]] - 상위 PRD (Block 4 배경 및 전체 아키텍처)
- [[./.claude_memos/evolution/EVOLUTION_v1.1_to_v1.2_Block4_Addition|진화 보고서]] - Block 4 추가 결정 과정

---

# Block 4: UI/UX Integration (UI/UX 통합 시스템)

**작성일:** 2025-11-09
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**상태:** 설계 중

**소속 Product:** [[Product_PRD_종이비행기날아라]]

---

## 📋 Block 정의

**한 줄 요약:**
> Clean Architecture의 Presentation Layer로서 Block 1-3의 도메인 로직을 사용자에게 시각적/청각적으로 전달하는 UI/UX 통합 시스템

**아키텍처 위치:**
- **Domain Layer (Block 1-3)**: 비행 조작, 게임 코어, 소셜 시스템 (비즈니스 로직)
- **Presentation Layer (Block 4)**: UI/UX Integration (사용자 인터페이스) ← **현재 Block**

**담당 Features:** 5개
- Feature 4.1: Main Menu Screen (메인 메뉴 화면)
- Feature 4.2: Game Play HUD (게임 플레이 HUD)
- Feature 4.3: Result Screen (결과 화면)
- Feature 4.4: 3D Environment Integration (3D 환경 통합)
- Feature 4.5: Sound & Effects System (사운드 및 이펙트 시스템)

**완성 기준:**
- [ ] Feature 5개 Integration Test 모두 통과
- [ ] Block Module Test 통과
- [ ] PRD Success Metrics 달성
  - [ ] 초기 로딩 시간 < 3초
  - [ ] FPS ≥ 60
  - [ ] 입력 응답 시간 < 16ms

**Block 4 특징:**
- **상태 통합**: Zustand를 통해 Block 1-3의 상태를 UI에 연결
- **3D + HTML 하이브리드**: Three.js Canvas 위에 React HTML UI 오버레이
- **반응형 아님**: Desktop Web 전용 (1280x720 이상)

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 읽기 ✅
        ↓
단계 2: Block 4 설계 문서 작성 (이 문서) ⏳
        ↓
단계 3: Feature 4.1 → Task 1-5 개발 (Unit TDD: Red-Green-Refactor-Mutation)
        ↓
단계 4: Feature 4.1 Integration TDD 작성 ⬆️
        (Task 5개 결과 참고 + PRD 싱크)
        ↓
단계 5: Feature 4.2 ~ 4.5 동일 반복
        ↓
단계 6: ✅ Block 4 Module TDD 작성 ⬆️
        (Feature 5개 결과 참고 + PRD 싱크)
        ↓
단계 7: Product E2E TDD 업데이트
        (Block 1-4 전체 통합, UI 시나리오 추가)
```

**중요:**
- Task는 **Red-Green-Refactor-Mutation 4단계 모두 완료 후** 체크
- Feature Integration TDD는 **Task 5개 모두 완료 후** 작성 (Task 개발 중 작성 ❌)
- Block Module TDD는 **Feature 5개 Integration TDD 모두 완료 후** 작성 (Feature 개발 중 작성 ❌)

---

## 🎨 Block 4 기술 스택

### UI Framework
| 기술 | 버전 | 용도 | 결정 상태 |
|------|------|------|----------|
| React | 18.2.0 | UI 컴포넌트 프레임워크 | ✅ 확정 |
| TypeScript | 5.3.0 | 타입 안전성 | ✅ 확정 |

### Styling
| 기술 | 버전 | 용도 | 결정 상태 |
|------|------|------|----------|
| **Tailwind CSS** | ^3.3.0 | UI 스타일링 | ✅ 확정 |
| PostCSS | ^8.4.0 | CSS 전처리 | ✅ 확정 |
| Autoprefixer | ^10.4.0 | 브라우저 호환성 | ✅ 확정 |

**결정 근거:**
- 번들 크기: ~10KB (gzip 압축 후)
- 런타임 오버헤드: 0 (빌드 타임 생성)
- AI 친화성: 높음 (클래스명 직관적)
- 개발 속도: 빠름
- 웹 브라우저 즉시 로딩: 최적화

### Animation
| 기술 | 버전 | 용도 | 결정 상태 |
|------|------|------|----------|
| **CSS Transitions** | 네이티브 | UI 전환 애니메이션 | ✅ 확정 |
| CSS Animations | 네이티브 | 키프레임 애니메이션 | ✅ 확정 |

**결정 근거:**
- 번들 크기: 0KB (브라우저 네이티브)
- 성능: GPU 가속 지원
- 개발 편의성: Tailwind CSS transition 유틸리티 활용
- 충분한 품질: 간단한 전환 효과에 적합
- Framer Motion 제외: 번들 크기 최적화 우선

### 3D & Audio
| 기술 | 버전 | 용도 | 결정 상태 |
|------|------|------|----------|
| Three.js | 0.160.0 | 3D 렌더링 (기존) | ✅ 확정 |
| @react-three/fiber | 8.15.0 | React Three.js 통합 (기존) | ✅ 확정 |
| @react-three/drei | 9.92.0 | 유틸리티 (Environment, Sky) | ✅ 확정 |
| **GLTF/GLB** | - | 3D 모델 포맷 | ✅ 확정 |
| **Howler.js** | ^2.2.0 | 오디오 관리 라이브러리 | ✅ 확정 |

**결정 근거 (Howler.js 선택):**
- 번들 크기: ~10KB (gzip 압축 후)
- 개발 편의성: Web Audio API보다 간단한 API
- 크로스 브라우저 호환성: 자동 처리
- 볼륨 조절: 간편한 fade/volume API
- AI 친화성: 직관적인 메서드명

### State Management
| 기술 | 버전 | 용도 | 결정 상태 |
|------|------|------|----------|
| Zustand | 4.4.7 | 전역 상태 관리 (기존) | ✅ 확정 |

**Zustand 연결 구조:**
```typescript
// Block 1-3의 상태를 Block 4 UI에 연결
const gameState = useGameStore(); // Block 2 (Game Core)
const flightState = useFlightStore(); // Block 1 (Flight Control)
const socialState = useSocialStore(); // Block 3 (Social)

// Block 4 UI 컴포넌트에서 사용
<GameHUD
  speed={flightState.currentSpeed}
  time={gameState.elapsedTime}
  checkpoint={gameState.currentCheckpoint}
/>
```

---

## Feature 4.1: Main Menu Screen (메인 메뉴 화면)

### Feature 4.1 정의

**한 줄 요약:**
> 게임 시작, 설정, 리더보드 프리뷰 기능을 제공하는 메인 메뉴 화면

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] 초기 로딩 시간 < 3초 (메뉴 화면 표시까지)

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

**UI/UX 요구사항:**
- 로블록스 스타일의 간결한 메뉴
- 3D 배경 (종이비행기가 날아다니는 애니메이션)
- 반응형 버튼 (호버 효과)
- 부드러운 화면 전환 (Framer Motion 사용 검토)

---

### Task 4.1.1: Menu Layout Component

**작업 목표:** 메인 메뉴의 React 컴포넌트 구조 및 레이아웃 구현

**기능 상세:**
- 중앙 정렬 레이아웃 (Flexbox or Grid)
- 타이틀: "Fly Paper Plane" (폰트: 귀여운 sans-serif)
- 버튼 영역: Start, Settings, Leaderboard
- 3D 배경 컨테이너 (Three.js Canvas)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
  - `<MainMenu />` 렌더링 테스트
  - 타이틀 존재 확인
  - 버튼 3개 존재 확인
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
  - MainMenu.tsx 기본 구조
  - Tailwind CSS or Styled Components 적용
- [ ] **Refactor (30min)**: 품질 개선 → `npm test` 여전히 통과 🔵
  - 레이아웃 코드 정리
  - CLEAR 원칙 적용
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block4-ui-ux/features/f1-main-menu/components/MainMenu.tsx`
- 테스트: `src/blocks/block4-ui-ux/features/f1-main-menu/components/MainMenu.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.1.2: Start Button Component

**작업 목표:** 게임 시작 버튼 구현 및 게임 상태 전환 트리거

**기능 상세:**
- "Start Game" 버튼 컴포넌트
- 클릭 시 `useGameStore().startGame()` 호출 (Block 2 연동)
- 호버 효과 (색상 변화, 크기 확대)
- 로딩 상태 표시 (게임 로딩 중)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
  - 버튼 클릭 시 startGame() 호출 확인
  - 로딩 상태 UI 변경 확인
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
  - StartButton.tsx 구현
  - Zustand 연동
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
  - 재사용 가능한 Button 컴포넌트로 추상화
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block4-ui-ux/features/f1-main-menu/components/StartButton.tsx`
- 테스트: `src/blocks/block4-ui-ux/features/f1-main-menu/components/StartButton.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.1.3: Settings Panel Component

**작업 목표:** 볼륨 및 그래픽 옵션 설정 패널 구현

**기능 상세:**
- Settings 버튼 클릭 시 모달/패널 열기
- 볼륨 슬라이더 3개: Master, Music, SFX (0-100%)
- 그래픽 옵션: Low, Medium, High (드롭다운)
- 설정 저장: LocalStorage에 저장

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
  - 패널 열기/닫기 동작
  - 슬라이더 값 변경
  - LocalStorage 저장 확인
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
  - SettingsPanel.tsx 구현
  - 상태 관리 (useState)
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
  - 슬라이더 컴포넌트 재사용
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block4-ui-ux/features/f1-main-menu/components/SettingsPanel.tsx`
- 테스트: `src/blocks/block4-ui-ux/features/f1-main-menu/components/SettingsPanel.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.1.4: Leaderboard Preview Component

**작업 목표:** 상위 10명의 리더보드 미리보기 표시

**기능 상세:**
- Leaderboard 버튼 클릭 시 모달 열기
- `useSocialStore().getTopRecords(10)` 호출 (Block 3 연동)
- 표 형식: Rank, Email, Time
- 로딩 스피너 (데이터 로딩 중)
- 빈 데이터 처리 ("아직 기록이 없습니다")

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
  - 리더보드 데이터 가져오기
  - 표 렌더링 (10개 행)
  - 로딩/빈 데이터 UI
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
  - LeaderboardPreview.tsx 구현
  - Zustand 연동 (Block 3)
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
  - 테이블 컴포넌트 재사용
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block4-ui-ux/features/f1-main-menu/components/LeaderboardPreview.tsx`
- 테스트: `src/blocks/block4-ui-ux/features/f1-main-menu/components/LeaderboardPreview.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.1.5: Menu Animation & Transition

**작업 목표:** 메뉴 화면 진입/나가기 애니메이션 구현

**기능 상세:**
- Framer Motion 사용 (검토 후 결정)
- Fade In 애니메이션 (메뉴 로딩 시)
- Slide Out 애니메이션 (Start 클릭 시)
- 부드러운 전환 (300ms easing)

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → 실패 확인 🔴
  - 애니메이션 클래스 적용 확인
  - Framer Motion variants 테스트
- [ ] **Green (30분)**: 최소 구현 → 통과 확인 🟢
  - Motion 컴포넌트 적용
  - variants 정의
- [ ] **Refactor (30분)**: 품질 개선 → 여전히 통과 🔵
  - 애니메이션 상수 분리
- [ ] **Mutation (15분)**: 변이 점수 >80% 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block4-ui-ux/features/f1-main-menu/animations/menuTransitions.ts`
- 테스트: `src/blocks/block4-ui-ux/features/f1-main-menu/animations/menuTransitions.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### ✅ Feature 4.1 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후
>
> **목적**: Task 결과를 참고하여 **PRD Success Metrics와 싱크**

**작성 전 확인:**
- [ ] Task 4.1.1-4.1.5 Unit Test 모두 통과
- [ ] Task 4.1.1-4.1.5 변이 점수 모두 >80%
- [ ] [[Product_PRD_종이비행기날아라]] Success Metrics 확인 완료

**Integration Test 체크리스트:**

1. **Task 간 연동 시나리오 작성**
   - [ ] 메뉴 로딩 → 버튼 3개 렌더링 (Task 1)
   - [ ] Start 버튼 클릭 → 게임 시작 (Task 2, Block 2 연동)
   - [ ] Settings 버튼 → 패널 열기 → 설정 변경 (Task 3)
   - [ ] Leaderboard 버튼 → 데이터 로딩 → 표 표시 (Task 4, Block 3 연동)
   - [ ] 전체 전환 애니메이션 동작 (Task 5)

2. **PRD Success Metrics 싱크**
   - [ ] PRD에 정의된 Feature 4.1 성공 지표 확인
     - 초기 로딩 시간 < 3초
   - [ ] Integration Test가 해당 지표를 검증하는지 확인
   - [ ] 누락된 지표가 있으면 테스트 추가

3. **Integration Test 코드 작성**
   - [ ] `src/blocks/block4-ui-ux/features/f1-main-menu/integration.test.tsx` 작성
   - [ ] Given-When-Then 구조로 작성
   - [ ] 실패 케이스 포함 (네트워크 에러, 빈 데이터)

4. **Integration Test 실행**
   - [ ] `npm test -- src/blocks/block4-ui-ux/features/f1-main-menu/integration.test.tsx`
   - [ ] 모든 테스트 통과 확인

**테스트 파일:** `src/blocks/block4-ui-ux/features/f1-main-menu/integration.test.tsx`

**통과 기준:**
- [ ] 모든 Integration Test 통과 (100%)
- [ ] PRD Success Metrics 달성 확인
- [ ] Task 5개 결과가 Feature로 통합됨

---

## Feature 4.2: Game Play HUD (게임 플레이 HUD)

### Feature 4.2 정의

**한 줄 요약:**
> 게임 플레이 중 실시간 정보(속도, 시간, 체크포인트)를 표시하는 HUD 오버레이

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] 입력 응답 시간 < 16ms (HUD 업데이트)
  - [ ] FPS ≥ 60 (HUD가 성능에 영향 없음)

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

**UI/UX 요구사항:**
- Three.js Canvas 위 HTML 오버레이 (absolute positioning)
- 반투명 배경 (가독성 유지)
- 최소한의 UI (플레이에 방해되지 않게)
- 실시간 업데이트 (60fps)

---

### Task 4.2.1: Speed Indicator Component

**작업 목표:** 현재 비행 속도를 실시간 표시

**기능 상세:**
- `useFlightStore().currentSpeed` 구독 (Block 1 연동)
- 숫자 표시: "150 km/h" 형식
- 색상 변화: 느림(파란색) → 빠름(빨간색)
- 위치: 화면 좌상단

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f2-game-hud/components/SpeedIndicator.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.2.2: Timer Display Component

**작업 목표:** 경과 시간 표시

**기능 상세:**
- `useGameStore().elapsedTime` 구독 (Block 2 연동)
- 포맷: "MM:SS.mmm" (분:초.밀리초)
- 위치: 화면 상단 중앙
- 크고 선명한 폰트

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f2-game-hud/components/TimerDisplay.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.2.3: Checkpoint Counter Component

**작업 목표:** 체크포인트 진행도 표시

**기능 상세:**
- `useGameStore().currentCheckpoint` 및 `totalCheckpoints` 구독 (Block 2 연동)
- 표시: "3/10" (현재/전체)
- 체크포인트 통과 시 강조 애니메이션
- 위치: 화면 우상단

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f2-game-hud/components/CheckpointCounter.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.2.4: Best Time Ghost Component

**작업 목표:** 이전 최고 기록 표시 (선택적)

**기능 상세:**
- `useSocialStore().personalBestTime` 구독 (Block 3 연동)
- 현재 시간 vs 최고 기록 비교
- 색상: 더 빠르면 녹색, 느리면 빨간색
- 위치: 타이머 아래

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f2-game-hud/components/BestTimeGhost.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### Task 4.2.5: HUD Overlay Integration

**작업 목표:** HUD 컴포넌트들을 Three.js Canvas 위에 오버레이

**기능 상세:**
- HTML div를 Canvas 위에 absolute positioning
- z-index 관리
- 성능 최적화 (React.memo, useMemo)
- 60fps 유지 확인

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f2-game-hud/components/HUDOverlay.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

---

### ✅ Feature 4.2 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] HUD 전체 렌더링 시나리오
- [ ] 실시간 데이터 업데이트 (60fps)
- [ ] PRD Success Metrics 싱크
  - [ ] FPS ≥ 60 (HUD 포함)
  - [ ] 입력 응답 < 16ms
- [ ] Integration Test 코드 작성 (`src/blocks/block4-ui-ux/features/f2-game-hud/integration.test.tsx`)
- [ ] Integration Test 실행 → 통과

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] PRD Success Metrics 달성

---

## Feature 4.3: Result Screen (결과 화면)

### Feature 4.3 정의

**한 줄 요약:**
> 게임 완료 후 결과(시간, 순위)를 표시하고 재시작/메뉴 옵션을 제공하는 화면

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성

**예상 소요 시간:** 1일 (Feature 4.1과 유사한 구조)

---

### Task 4.3.1: Time Result Display

**작업 목표:** 완주 시간 표시

**기능 상세:**
- `useGameStore().finalTime` 표시
- 크고 선명한 폰트
- 애니메이션 (숫자 카운트업)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f3-result-screen/components/TimeResult.tsx`

---

### Task 4.3.2: Record Comparison

**작업 목표:** 개인 최고 기록 비교

**기능 상세:**
- 현재 기록 vs 최고 기록
- "New Record!" 표시 (신기록 시)
- 차이 표시: "+0.5s" or "-0.3s"

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f3-result-screen/components/RecordComparison.tsx`

---

### Task 4.3.3: Leaderboard Position

**작업 목표:** 전체 순위 표시

**기능 상세:**
- `useSocialStore().submitRecord()` 호출 후 순위 가져오기
- "You ranked #5!" 표시
- 상위 3명 특별 표시 (메달)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f3-result-screen/components/LeaderboardPosition.tsx`

---

### Task 4.3.4: Retry/Exit Buttons

**작업 목표:** 재시작 및 메뉴 돌아가기 버튼

**기능 상세:**
- "Retry" 버튼 → `useGameStore().restartGame()`
- "Main Menu" 버튼 → 메인 메뉴로 전환
- 버튼 호버 효과

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f3-result-screen/components/ResultButtons.tsx`

---

### Task 4.3.5: Result Animation

**작업 목표:** 축하 효과 애니메이션

**기능 상세:**
- 신기록 시 파티클 효과 (confetti)
- Fade In 애니메이션
- 사운드 효과 트리거 (Feature 4.5 연동)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f3-result-screen/animations/resultAnimations.ts`

---

### ✅ Feature 4.3 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] 결과 화면 전체 플로우
  - 게임 종료 → 결과 표시 → 순위 제출 → 버튼 동작
- [ ] PRD Success Metrics 싱크
- [ ] Integration Test 작성 및 실행

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] PRD Success Metrics 달성

---

## Feature 4.4: 3D Environment Integration (3D 환경 통합)

### Feature 4.4 정의

**한 줄 요약:**
> Three.js 3D 환경(Skybox, Lighting, Course Model, Particle Effects)을 통합하여 몰입감 있는 게임 환경 제공

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] FPS ≥ 60 (3D 환경 포함)

**예상 소요 시간:** 2-3일 (3D 모델 로딩 및 최적화)

---

### Task 4.4.1: Skybox Setup

**작업 목표:** GLTF Environment를 이용한 Skybox 설정

**기능 상세:**
- @react-three/drei의 `<Environment>` 사용
- Preset: "sunset" or "city" 선택
- HDR 환경 맵 (선택적)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f4-3d-environment/components/Skybox.tsx`

---

### Task 4.4.2: Lighting System

**작업 목표:** DirectionalLight, AmbientLight 설정

**기능 상세:**
- DirectionalLight (태양광 시뮬레이션)
- AmbientLight (전반적인 밝기)
- 그림자 활성화
- 시간대별 조명 변화 (낮/밤)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f4-3d-environment/components/LightingSystem.tsx`

---

### Task 4.4.3: Course Model Loading

**작업 목표:** GLTF 코스 모델 로드 및 배치

**기능 상세:**
- GLTF Loader로 코스 모델 로드
- Block 2 (Game Core)의 코스 데이터와 동기화
- LOD (Level of Detail) 적용 (성능 최적화)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f4-3d-environment/components/CourseModel.tsx`

---

### Task 4.4.4: Particle Effects

**작업 목표:** 구름, 바람 파티클 효과

**기능 상세:**
- PointsMaterial을 이용한 구름 파티클
- 바람 효과 (비행기 주변)
- 성능 최적화 (파티클 수 제한)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f4-3d-environment/effects/ParticleEffects.tsx`

---

### Task 4.4.5: Environment State Management

**작업 목표:** 낮/밤 전환 및 환경 상태 관리

**기능 상세:**
- Zustand로 환경 상태 관리
- 낮/밤 전환 애니메이션
- 설정에서 시간대 선택 가능

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f4-3d-environment/state/environmentStore.ts`

---

### ✅ Feature 4.4 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] 3D 환경 전체 로딩 및 렌더링
- [ ] 성능 테스트 (FPS ≥ 60)
- [ ] PRD Success Metrics 싱크
- [ ] Integration Test 작성 및 실행

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] FPS ≥ 60 달성

---

## Feature 4.5: Sound & Effects System (사운드 및 이펙트 시스템)

### Feature 4.5 정의

**한 줄 요약:**
> Web Audio API 기반 오디오 관리 시스템으로 배경 음악 및 효과음 재생

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성

**예상 소요 시간:** 1-2일

---

### Task 4.5.1: Audio Manager

**작업 목표:** Web Audio API 래퍼 클래스 구현

**기능 상세:**
- AudioContext 관리
- 오디오 파일 로드 및 디코드
- 볼륨 조절 (Master, Music, SFX)
- 오디오 재생/정지/일시정지

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f5-sound-system/core/AudioManager.ts`

---

### Task 4.5.2: Background Music

**작업 목표:** 배경 음악 재생

**기능 상세:**
- 메인 메뉴 음악
- 게임 플레이 음악
- 자동 루프
- 페이드 인/아웃 전환

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f5-sound-system/music/BackgroundMusic.ts`

---

### Task 4.5.3: Sound Effects

**작업 목표:** 효과음 재생

**기능 상세:**
- 엔진 소리 (비행 중)
- 바람 소리
- 충돌 소리
- 체크포인트 통과 소리
- 동시 재생 지원

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f5-sound-system/sfx/SoundEffects.ts`

---

### Task 4.5.4: Volume Control

**작업 목표:** 볼륨 조절 시스템

**기능 상세:**
- Master 볼륨 (전체)
- Music 볼륨 (배경 음악)
- SFX 볼륨 (효과음)
- Zustand로 상태 관리
- LocalStorage 연동 (설정 저장)

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f5-sound-system/state/volumeStore.ts`

---

### Task 4.5.5: Sound Integration Test

**작업 목표:** 사운드 시스템 통합 테스트

**기능 상세:**
- 모든 오디오 파일 로드 확인
- 볼륨 조절 동작 확인
- 게임 이벤트와 사운드 연동 확인

**TDD 체크리스트:**
- [ ] Red 🔴 | Green 🟢 | Refactor 🔵 | Mutation 🧬

**실제 시간:** [기록]분
**파일:** `src/blocks/block4-ui-ux/features/f5-sound-system/integration.test.ts`

---

### ✅ Feature 4.5 Integration TDD

> **⚠️ 작성 시점**: Task 5개 완료 후

**Integration Test 체크리스트:**
- [ ] Task 1-5 Unit Test 모두 통과
- [ ] 사운드 시스템 전체 동작 확인
- [ ] 게임 이벤트와 사운드 연동
- [ ] PRD Success Metrics 싱크
- [ ] Integration Test 작성 및 실행

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] 사운드가 게임 성능에 영향 없음

---

## ✅ Block 4 Module TDD

> **⚠️ 작성 시점**: Feature 5개 완료 후
>
> **목적**: Feature 결과를 참고하여 **PRD Success Metrics와 싱크**

**작성 전 확인:**
- [ ] Feature 4.1-4.5 Integration Test 모두 통과
- [ ] Feature 4.1-4.5 PRD Success Metrics 달성 확인
- [ ] [[Product_PRD_종이비행기날아라]] 전체 Success Metrics 확인

**Module Test 체크리스트:**

1. **Feature 간 연동 시나리오 작성**
   - [ ] Feature 4.1 (Menu) → Feature 4.2 (HUD) 전환
   - [ ] Feature 4.2 (HUD) → Feature 4.3 (Result) 전환
   - [ ] Feature 4.4 (3D Environment)가 모든 화면에서 동작
   - [ ] Feature 4.5 (Sound)가 모든 이벤트에 반응
   - [ ] 전체 통합 시나리오 (Menu → Game → Result → Menu)

2. **SOLID 원칙 검증**
   - [ ] **Single Responsibility**: 각 컴포넌트가 하나의 책임만
   - [ ] **Open/Closed**: 새 화면 추가 시 기존 코드 수정 불필요
   - [ ] **Liskov Substitution**: 컴포넌트 대체 가능성
   - [ ] **Interface Segregation**: Props 인터페이스 분리
   - [ ] **Dependency Inversion**: Zustand Store 추상화

3. **PRD Success Metrics 싱크**
   - [ ] PRD에 정의된 Block 4 성공 지표 확인
     - [ ] 초기 로딩 시간 < 3초
     - [ ] FPS ≥ 60
     - [ ] 입력 응답 시간 < 16ms
   - [ ] Module Test가 해당 지표를 검증하는지 확인
   - [ ] 누락된 지표가 있으면 테스트 추가

4. **Module Test 코드 작성**
   - [ ] `src/blocks/block4-ui-ux/module.test.tsx` 작성
   - [ ] Given-When-Then 구조로 작성
   - [ ] 실패 케이스 포함
   - [ ] 성능 테스트 포함 (FPS, 로딩 시간)

5. **Module Test 실행**
   - [ ] `npm test -- src/blocks/block4-ui-ux/module.test.tsx`
   - [ ] 모든 테스트 통과 확인

**테스트 파일:** `src/blocks/block4-ui-ux/module.test.tsx`

**통과 기준:**
- [ ] 모든 Module Test 통과 (100%)
- [ ] SOLID 원칙 준수 확인
- [ ] PRD Success Metrics 달성 확인
- [ ] Feature 5개 결과가 Block으로 통합됨

---

## 📊 작업 진행 현황

| 항목 | Task 진행 | Integration/Module | 전체 상태 |
|------|-----------|-------------------|----------|
| **Feature 4.1** | [0/5] | 대기 | ⏳ |
| **Feature 4.2** | [0/5] | 대기 | ⏳ |
| **Feature 4.3** | [0/5] | 대기 | ⏳ |
| **Feature 4.4** | [0/5] | 대기 | ⏳ |
| **Feature 4.5** | [0/5] | 대기 | ⏳ |
| **Block Module TDD** | - | 대기 | ⏳ |

**전체 진행률:** [0/31]
- Task: [0/25] (Feature 5개 × Task 5개)
- Integration TDD: [0/5] (Feature 5개)
- Module TDD: [0/1] (Block 1개)

**예상 완료 시간:** 11-14일
- Feature 4.1: 2일
- Feature 4.2: 2일
- Feature 4.3: 1일
- Feature 4.4: 2-3일
- Feature 4.5: 1-2일
- Block Module TDD: 1일
- Product E2E TDD 업데이트: 1일

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

### 기술 결정 완료 ✅
- [x] **Styling**: Tailwind CSS (확정)
- [x] **Audio**: Howler.js (확정)
- [x] **Animation**: CSS Transitions/Animations (확정, Framer Motion 제외)

---

## 📦 Block 4 에셋 & 라이브러리 준비

> **목적**: Block 4 개발 시작 전 필요한 UI 에셋 및 라이브러리 사전 확보
>
> **원칙**: PRD 정의 에셋과 중복 없이, Block 4 전용 에셋만 추가

### 🎨 Block 4 디자인 에셋

#### UI 그래픽 에셋

**1. 아이콘 세트**
- **소스**: Lucide Icons (React 컴포넌트)
- **용도**: 버튼 아이콘, HUD 아이콘
- **필요 아이콘**:
  - Play (시작 버튼)
  - Settings (설정)
  - Trophy (리더보드)
  - RotateCcw (재시작)
  - Home (메인 메뉴)
  - Volume2, VolumeX (볼륨 조절)
- **라이선스**: MIT
- **설치**: `npm install lucide-react`

**2. UI 배경 이미지 (선택적)**
- **메뉴 배경**: CSS 그라디언트로 생성 (에셋 불필요)
- **파티클 텍스처**: Three.js PointsMaterial (코드 생성)

#### 오디오 에셋

**배경 음악 (2개)**
1. **메인 메뉴 음악** (`menu-bgm.mp3`)
   - 소스: Pixabay Music (무료 CC0)
   - 길이: 2-3분 (루프 가능)
   - 분위기: 밝고 경쾌한
   - 링크: https://pixabay.com/music/search/upbeat/

2. **게임 플레이 음악** (`gameplay-bgm.mp3`)
   - 소스: Pixabay Music (무료 CC0)
   - 길이: 3-5분 (루프 가능)
   - 분위기: 긴장감 있는
   - 링크: https://pixabay.com/music/search/action/

**효과음 (5개)**
1. `engine-sound.mp3` - 비행 엔진 소리
2. `wind-sound.mp3` - 바람 소리
3. `collision.mp3` - 충돌음
4. `checkpoint.mp3` - 체크포인트 통과음
5. `result-fanfare.mp3` - 결과 화면 팡파레

- **소스**: Pixabay Sound Effects (무료 CC0)
- **포맷**: MP3 (Howler.js가 OGG로 자동 폴백)
- **링크**: https://pixabay.com/sound-effects/

#### 폰트

**UI 폰트 (PRD에서 이미 정의됨)**
- **Press Start 2P** (Google Fonts) - PRD에서 확보 완료 ✅
- **용도**: 게임 타이틀, 타이머, 점수 표시
- **위치**: `public/assets/fonts/PressStart2P-Regular.ttf`

**추가 폰트 불필요** (Press Start 2P로 충분)

---

### 🛠️ Block 4 라이브러리

#### 필수 라이브러리

```json
{
  "dependencies": {
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "howler": "^2.2.0",
    "lucide-react": "^0.300.0"
  },
  "devDependencies": {
    "@types/howler": "^2.2.0"
  }
}
```

**라이브러리 상세:**

| 라이브러리 | 버전 | 용도 | 번들 크기 |
|-----------|------|------|----------|
| `tailwindcss` | ^3.3.0 | UI 스타일링 | ~10KB (gzip) |
| `postcss` | ^8.4.0 | CSS 전처리 | 0KB (dev) |
| `autoprefixer` | ^10.4.0 | 브라우저 호환성 | 0KB (dev) |
| `howler` | ^2.2.0 | 오디오 관리 | ~10KB |
| `lucide-react` | ^0.300.0 | React 아이콘 | ~5KB (tree-shake) |

**총 번들 크기 증가**: ~25KB (gzip)

---

### 📥 설치 스크립트

#### Block 4 라이브러리 설치

```bash
#!/bin/bash
# install-block4-dependencies.sh

echo "📦 Block 4 UI/UX 라이브러리 설치 중..."

# Tailwind CSS 설치
npm install -D tailwindcss postcss autoprefixer

# Tailwind 초기화
npx tailwindcss init -p

# Howler.js 설치
npm install howler
npm install -D @types/howler

# Lucide Icons 설치
npm install lucide-react

echo "✅ Block 4 라이브러리 설치 완료"
```

#### Tailwind CSS 설정

**tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        game: ['"Press Start 2P"', 'cursive'],
      },
      colors: {
        'roblox-blue': '#0066FF',
        'roblox-green': '#00FF00',
      },
    },
  },
  plugins: [],
}
```

**src/index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Press Start 2P 폰트 로드 (PRD에서 확보한 에셋) */
@font-face {
  font-family: 'Press Start 2P';
  src: url('/assets/fonts/PressStart2P-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

/* 게임 스타일 전역 설정 */
body {
  margin: 0;
  font-family: 'Press Start 2P', cursive;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}
```

---

### 🎨 에셋 디렉토리 구조

```
public/
├── assets/
│   ├── fonts/
│   │   └── PressStart2P-Regular.ttf        # ✅ PRD에서 확보 완료
│   ├── models/
│   │   ├── paper-plane.glb                 # ✅ PRD에서 확보 완료
│   │   └── obstacles/                      # ✅ PRD에서 확보 완료
│   └── audio/                              # 🆕 Block 4 추가
│       ├── music/
│       │   ├── menu-bgm.mp3
│       │   └── gameplay-bgm.mp3
│       └── sfx/
│           ├── engine-sound.mp3
│           ├── wind-sound.mp3
│           ├── collision.mp3
│           ├── checkpoint.mp3
│           └── result-fanfare.mp3
```

**추가 폴더 생성 스크립트:**
```bash
mkdir -p public/assets/audio/music
mkdir -p public/assets/audio/sfx
```

---

### 📋 에셋 확보 체크리스트

#### PRD 에셋 (이미 확보 완료) ✅
- [x] Press Start 2P 폰트
- [x] 종이비행기 3D 모델 (paper-plane.glb)
- [x] 장애물 에셋 (Kenney.nl City Kit)

#### Block 4 추가 에셋 (✅ 확보 완료)
- [x] 메인 메뉴 배경 음악 (menu-bgm.ogg) - placeholder
- [x] 게임 플레이 음악 (gameplay-bgm.ogg) - placeholder
- [x] 엔진 소리 (engine-sound.ogg) - placeholder
- [x] 바람 소리 (wind-sound.ogg) - placeholder
- [x] 충돌음 (collision.ogg) - ✅ Kenney Impact Sounds
- [x] 체크포인트 통과음 (checkpoint.ogg) - ✅ Kenney UI Audio
- [x] 결과 팡파레 (result-fanfare.ogg) - placeholder

#### Block 4 라이브러리 (✅ 설치 완료)
- [x] Tailwind CSS + PostCSS + Autoprefixer
- [x] Howler.js + @types/howler
- [x] Lucide React Icons

---

### ⚠️ 중복 확인 완료

**PRD와 중복 없음:**
- ✅ 3D 모델: PRD 에셋 재사용 (paper-plane.glb, obstacles)
- ✅ 폰트: PRD 에셋 재사용 (Press Start 2P)
- ✅ Three.js 라이브러리: PRD에서 이미 설치됨
- ✅ React/Zustand: PRD에서 이미 설치됨

**Block 4 전용 추가사항:**
- 🆕 오디오 파일 7개 (음악 2 + 효과음 5)
- 🆕 Tailwind CSS (UI 스타일링)
- 🆕 Howler.js (오디오 관리)
- 🆕 Lucide Icons (UI 아이콘)

---

**작성일:** 2025-11-09
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**최종 업데이트:** 2025-11-09 00:30

---

## 📚 버전 이력

### v1.0 (2025-11-09)
**목적:** Block 4 (UI/UX Integration) 설계 문서 초안 작성

**핵심 내용:**
1. **Clean Architecture 적용**
   - Domain Layer (Block 1-3)와 Presentation Layer (Block 4) 분리
   - Zustand를 통한 상태 연결

2. **5개 Features 상세 정의**
   - Feature 4.1: Main Menu Screen (5 Tasks)
   - Feature 4.2: Game Play HUD (5 Tasks)
   - Feature 4.3: Result Screen (5 Tasks)
   - Feature 4.4: 3D Environment Integration (5 Tasks)
   - Feature 4.5: Sound & Effects System (5 Tasks)

3. **기술 스택 결정**
   - React + TypeScript + Three.js (확정)
   - Styling: Tailwind CSS vs Styled Components (검토 중)
   - Audio: Web Audio API vs Howler.js (검토 중)
   - Animation: Framer Motion (선택적)

4. **피라미드 TDD 전략**
   - Task Unit Test → Feature Integration TDD → Block Module TDD
   - PRD Success Metrics 싱크 포인트 명시

**참조 문서:**
- [[./Product_PRD_종이비행기날아라]] - Block 4 배경 및 전체 아키텍처
- [[./CJ_AI_개발방법론]] - 이론 및 방법론
- [[./.claude_memos/evolution/EVOLUTION_v1.1_to_v1.2_Block4_Addition]] - Block 4 추가 결정 과정
