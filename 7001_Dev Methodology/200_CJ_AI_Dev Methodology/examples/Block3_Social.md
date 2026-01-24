# Block 3: Social System (소셜 시스템)

**작성일:** 2025-11-08
**작성자:** AI (Claude Code) - 개발자 검토 후 승인
**버전:** 1.0
**상태:** 대기

**소속 Product:** 종이비행기 날아라 (Fly Paper Plane)

---

## 📋 Block 정의

**한 줄 요약:**
> 이메일 기반 간편 인증과 실시간 리더보드를 통해 전 세계 플레이어와 경쟁하는 소셜 시스템

**담당 Features:** 3개
- Feature 3.1: 이메일 인증 시스템 (Email Authentication)
- Feature 3.2: 리더보드 표시 시스템 (Leaderboard Display)
- Feature 3.3: 개인 기록 관리 시스템 (Personal Record Manager)

**완성 기준:**
- [ ] Feature 3개 Integration Test 모두 통과
- [ ] Block Module Test 통과
- [ ] PRD Success Metrics 달성
  - [ ] 리더보드 조회 시간 < 1초
  - [ ] 이메일 입력 → 게임 시작 < 3초
  - [ ] 재방문율 30% 이상 (로컬스토리지 이메일 자동 입력)

---

## 🔄 작업 흐름 (피라미드)

> **핵심**: 아래에서 위로 올라가며 개발 → 테스트 작성

```
단계 1: PRD 읽기
        ↓
단계 2: Block/Feature/Task 정의 (이 문서 작성)
        ↓
단계 3: Task 3.1.1 개발 (Unit TDD: Red-Green-Refactor-Mutation)
        ↓
단계 4: Task 3.1.2-3.1.5 개발 (동일)
        ↓
단계 5: ✅ Feature 3.1 Integration TDD 작성 ⬆️
        (Task 5개 결과 참고 + PRD 싱크)
        ↓
단계 6: Feature 3.2, 3.3 동일 반복
        ↓
단계 7: ✅ Block 3 Module TDD 작성 ⬆️
        (Feature 3개 결과 참고 + PRD 싱크)
```

**중요:**
- Task는 **Red-Green-Refactor-Mutation 4단계 모두 완료 후** 체크
- Feature Integration TDD는 **Task 5개 모두 완료 후** 작성 (Task 개발 중 작성 ❌)
- Block Module TDD는 **Feature 3개 Integration TDD 모두 완료 후** 작성 (Feature 개발 중 작성 ❌)

---

## 🎯 Block 3 Success Metrics (PRD 연결)

| 지표 | 목표 | 측정 방법 | 관련 Feature |
|------|------|----------|-------------|
| **리더보드 조회 시간** | < 1초 | API 응답 시간 측정 | Feature 3.2 |
| **이메일 입력 → 게임 시작** | < 3초 | 폼 제출 → 로딩 완료 시간 | Feature 3.1 |
| **재방문율** | 30% 이상 | 로컬스토리지 이메일 재확인 | Feature 3.1 |
| **리더보드 등록 수** | 100명 이상 | DB 기록 수 (출시 후 2주) | Feature 3.3 |

---

## 📦 기술 스택 (Block 3 전용)

| 라이브러리 | 버전 | 용도 | Feature 매핑 |
|-----------|------|------|-------------|
| `axios` | ^1.6.0 | HTTP 클라이언트 (리더보드 API) | Feature 3.2, 3.3 |
| `react-hook-form` | ^7.49.0 | 폼 검증 (이메일 입력) | Feature 3.1 |
| `zod` | ^3.22.0 | 스키마 검증 (이메일 형식) | Feature 3.1 |
| `@tanstack/react-query` | ^5.14.0 | 서버 상태 관리 (리더보드 폴링 5초) | Feature 3.2, 3.3 |
| `zustand` | ^4.4.7 | 로컬 상태 관리 (인증 상태) | Feature 3.1 |

**설치 명령:**
```bash
npm install axios react-hook-form zod @tanstack/react-query zustand
```

---

## Feature 3.1: 이메일 인증 시스템 (Email Authentication)

### Feature 3.1 정의

**한 줄 요약:**
> 이메일만으로 즉시 게임 시작할 수 있는 간편 인증 시스템 (비밀번호 없음)

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] 이메일 입력 → 게임 시작 < 3초
  - [ ] 재방문 시 이메일 자동 입력 (로컬스토리지)

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 3.1.1: 이메일 입력 폼 UI

**작업 목표:** React Hook Form을 사용한 이메일 입력 폼 컴포넌트 생성

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f1-email-auth/tasks/t1-email-form.tsx`
- 테스트: `src/blocks/block3-social/features/f1-email-auth/tasks/t1-email-form.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t1-email-form.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { emailSchema } from './email-schema'; // Task 3.1.2에서 정의

interface EmailFormProps {
  onSubmit: (email: string) => void;
  defaultEmail?: string;
}

export function EmailForm({ onSubmit, defaultEmail }: EmailFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(emailSchema),
    defaultValues: { email: defaultEmail || '' }
  });

  return (
    <form onSubmit={handleSubmit((data) => onSubmit(data.email))}>
      <input
        {...register('email')}
        type="email"
        placeholder="Enter your email"
        data-testid="email-input"
      />
      {errors.email && <span data-testid="email-error">{errors.email.message}</span>}
      <button type="submit" data-testid="submit-button">Start Game</button>
    </form>
  );
}
```

**테스트 시나리오:**
1. **폼 렌더링**: 이메일 입력 필드와 제출 버튼이 표시됨
2. **기본값 설정**: `defaultEmail` prop이 입력 필드에 자동 입력됨
3. **유효성 검증**: 잘못된 이메일 입력 시 에러 메시지 표시
4. **제출 이벤트**: 유효한 이메일 입력 후 `onSubmit` 콜백 호출

**의존성:**
- `react-hook-form` ^7.49.0
- `@hookform/resolvers` (zod resolver)

---

### Task 3.1.2: 이메일 형식 검증 (Zod Schema)

**작업 목표:** Zod를 사용한 이메일 형식 검증 스키마 정의

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f1-email-auth/tasks/t2-email-schema.ts`
- 테스트: `src/blocks/block3-social/features/f1-email-auth/tasks/t2-email-schema.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t2-email-schema.ts
import { z } from 'zod';

export const emailSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email format')
    .max(100, 'Email is too long')
    .refine(
      (email) => !email.includes('+'),
      'Plus signs are not allowed'
    )
});

export type EmailFormData = z.infer<typeof emailSchema>;

// 단독 검증 함수 (테스트 용이성)
export function validateEmail(email: string): {
  valid: boolean;
  error?: string
} {
  const result = emailSchema.safeParse({ email });
  return {
    valid: result.success,
    error: result.success ? undefined : result.error.errors[0].message
  };
}
```

**테스트 시나리오:**
1. **유효한 이메일**: `"user@example.com"` → valid: true
2. **빈 문자열**: `""` → valid: false, error: "Email is required"
3. **잘못된 형식**: `"invalid"` → valid: false, error: "Invalid email format"
4. **너무 긴 이메일**: 100자 초과 → valid: false
5. **Plus 기호 포함**: `"user+test@example.com"` → valid: false (PRD 요구사항)

**의존성:**
- `zod` ^3.22.0

---

### Task 3.1.3: 로컬스토리지 저장/로드

**작업 목표:** 이메일을 로컬스토리지에 저장하고 재방문 시 자동 로드

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f1-email-auth/tasks/t3-local-storage.ts`
- 테스트: `src/blocks/block3-social/features/f1-email-auth/tasks/t3-local-storage.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t3-local-storage.ts
const EMAIL_STORAGE_KEY = 'fly_paper_plane_email';

export function saveEmailToStorage(email: string): void {
  try {
    localStorage.setItem(EMAIL_STORAGE_KEY, email);
  } catch (error) {
    console.error('Failed to save email to localStorage', error);
  }
}

export function loadEmailFromStorage(): string | null {
  try {
    return localStorage.getItem(EMAIL_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to load email from localStorage', error);
    return null;
  }
}

export function clearEmailFromStorage(): void {
  try {
    localStorage.removeItem(EMAIL_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear email from localStorage', error);
  }
}

// 재방문 여부 확인 (Success Metrics 측정용)
export function isReturningUser(): boolean {
  return loadEmailFromStorage() !== null;
}
```

**테스트 시나리오:**
1. **저장 성공**: `saveEmailToStorage("user@example.com")` → 로컬스토리지에 저장됨
2. **로드 성공**: `loadEmailFromStorage()` → "user@example.com" 반환
3. **초기 상태**: 저장된 이메일 없을 때 → null 반환
4. **삭제 성공**: `clearEmailFromStorage()` → 로컬스토리지에서 삭제됨
5. **재방문 확인**: 저장된 이메일 있음 → `isReturningUser()` true

**의존성:**
- 없음 (브라우저 기본 API)

---

### Task 3.1.4: 인증 상태 관리 (Zustand Store)

**작업 목표:** Zustand를 사용한 이메일 인증 상태 관리

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f1-email-auth/tasks/t4-auth-store.ts`
- 테스트: `src/blocks/block3-social/features/f1-email-auth/tasks/t4-auth-store.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t4-auth-store.ts
import { create } from 'zustand';
import { saveEmailToStorage, loadEmailFromStorage, clearEmailFromStorage } from './t3-local-storage';

interface AuthState {
  email: string | null;
  isAuthenticated: boolean;
  login: (email: string) => void;
  logout: () => void;
  loadFromStorage: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  email: null,
  isAuthenticated: false,

  login: (email: string) => {
    saveEmailToStorage(email);
    set({ email, isAuthenticated: true });
  },

  logout: () => {
    clearEmailFromStorage();
    set({ email: null, isAuthenticated: false });
  },

  loadFromStorage: () => {
    const email = loadEmailFromStorage();
    if (email) {
      set({ email, isAuthenticated: true });
    }
  }
}));
```

**테스트 시나리오:**
1. **초기 상태**: email: null, isAuthenticated: false
2. **로그인**: `login("user@example.com")` → 상태 업데이트 + 로컬스토리지 저장
3. **로그아웃**: `logout()` → 상태 초기화 + 로컬스토리지 삭제
4. **스토리지 로드**: `loadFromStorage()` → 로컬스토리지에서 이메일 복원
5. **재방문 시나리오**: 저장된 이메일 있을 때 `loadFromStorage()` → 자동 로그인

**의존성:**
- `zustand` ^4.4.7
- Task 3.1.3 (로컬스토리지)

---

### Task 3.1.5: 이메일 인증 UI 컴포넌트 통합

**작업 목표:** Feature 3.1의 모든 Task를 통합한 완전한 이메일 인증 UI

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f1-email-auth/index.tsx`
- 테스트: `src/blocks/block3-social/features/f1-email-auth/index.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// index.tsx (Feature 3.1 통합)
import { useEffect } from 'react';
import { EmailForm } from './tasks/t1-email-form';
import { useAuthStore } from './tasks/t4-auth-store';

interface EmailAuthProps {
  onAuthSuccess: (email: string) => void;
}

export function EmailAuth({ onAuthSuccess }: EmailAuthProps) {
  const { email, isAuthenticated, login, loadFromStorage } = useAuthStore();

  // 컴포넌트 마운트 시 로컬스토리지에서 이메일 로드
  useEffect(() => {
    loadFromStorage();
  }, [loadFromStorage]);

  // 이미 인증된 경우 콜백 호출
  useEffect(() => {
    if (isAuthenticated && email) {
      onAuthSuccess(email);
    }
  }, [isAuthenticated, email, onAuthSuccess]);

  const handleEmailSubmit = (submittedEmail: string) => {
    login(submittedEmail);
  };

  return (
    <div data-testid="email-auth-container">
      <h1>Fly Paper Plane</h1>
      <EmailForm
        onSubmit={handleEmailSubmit}
        defaultEmail={email || undefined}
      />
    </div>
  );
}
```

**테스트 시나리오:**
1. **첫 방문**: 로컬스토리지 비어있음 → 이메일 입력 폼 표시
2. **이메일 제출**: 유효한 이메일 입력 → `onAuthSuccess` 콜백 호출
3. **재방문**: 로컬스토리지에 이메일 있음 → 자동으로 `onAuthSuccess` 호출
4. **기본값 표시**: 재방문 시 이메일 입력 필드에 저장된 이메일 자동 입력
5. **전체 플로우**: 제출 → 로그인 → 콜백 → 로컬스토리지 저장

**의존성:**
- Task 3.1.1 (EmailForm)
- Task 3.1.4 (useAuthStore)

---

### 📊 Feature 3.1 Integration Test

> **⚠️ 작성 시점**: Task 3.1.1 ~ 3.1.5 모두 완료 후

**목적:** Feature 3.1의 5개 Task가 통합되어 PRD 요구사항을 달성하는지 검증

**파일:**
- `src/blocks/block3-social/features/f1-email-auth/f1-email-auth.integration.test.tsx`

**테스트 시나리오:**

#### 시나리오 1: 첫 방문 사용자 인증 플로우
```typescript
describe('Feature 3.1 Integration: 첫 방문 사용자', () => {
  it('should complete email authentication flow for new user', async () => {
    // Given: 로컬스토리지 비어있음
    localStorage.clear();
    const onAuthSuccess = vi.fn();

    // When: 컴포넌트 렌더링
    render(<EmailAuth onAuthSuccess={onAuthSuccess} />);

    // Then: 이메일 입력 폼 표시
    expect(screen.getByTestId('email-input')).toBeInTheDocument();

    // When: 유효한 이메일 입력 및 제출
    await userEvent.type(screen.getByTestId('email-input'), 'user@example.com');
    await userEvent.click(screen.getByTestId('submit-button'));

    // Then: onAuthSuccess 콜백 호출
    expect(onAuthSuccess).toHaveBeenCalledWith('user@example.com');

    // Then: 로컬스토리지에 저장됨
    expect(localStorage.getItem('fly_paper_plane_email')).toBe('user@example.com');
  });
});
```

#### 시나리오 2: 재방문 사용자 자동 로그인
```typescript
describe('Feature 3.1 Integration: 재방문 사용자', () => {
  it('should auto-login returning user from localStorage', async () => {
    // Given: 로컬스토리지에 이메일 저장됨
    localStorage.setItem('fly_paper_plane_email', 'returning@example.com');
    const onAuthSuccess = vi.fn();

    // When: 컴포넌트 렌더링
    render(<EmailAuth onAuthSuccess={onAuthSuccess} />);

    // Then: 자동으로 onAuthSuccess 호출 (3초 이내)
    await waitFor(() => {
      expect(onAuthSuccess).toHaveBeenCalledWith('returning@example.com');
    }, { timeout: 3000 });

    // Then: 입력 필드에 이메일 자동 입력
    expect(screen.getByTestId('email-input')).toHaveValue('returning@example.com');
  });
});
```

#### 시나리오 3: 잘못된 이메일 입력 검증
```typescript
describe('Feature 3.1 Integration: 이메일 검증', () => {
  it('should show error for invalid email', async () => {
    const onAuthSuccess = vi.fn();
    render(<EmailAuth onAuthSuccess={onAuthSuccess} />);

    // When: 잘못된 이메일 입력
    await userEvent.type(screen.getByTestId('email-input'), 'invalid');
    await userEvent.click(screen.getByTestId('submit-button'));

    // Then: 에러 메시지 표시
    expect(screen.getByTestId('email-error')).toHaveTextContent('Invalid email format');

    // Then: onAuthSuccess 호출되지 않음
    expect(onAuthSuccess).not.toHaveBeenCalled();
  });
});
```

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] Task 5개 Unit Test 모두 통과
- [ ] 커버리지 >90%
- [ ] PRD Success Metrics 달성
  - [ ] 이메일 입력 → 게임 시작 < 3초
  - [ ] 재방문 시 자동 로그인 동작

---

## Feature 3.2: 리더보드 표시 시스템 (Leaderboard Display)

### Feature 3.2 정의

**한 줄 요약:**
> 전 세계 Top 100 순위를 실시간으로 표시하고 내 순위를 하이라이트하는 리더보드 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] 리더보드 조회 시간 < 1초
  - [ ] 5초 간격 실시간 업데이트

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 3.2.1: 리더보드 API 인터페이스

**작업 목표:** Axios를 사용한 리더보드 API 클라이언트 정의

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f2-leaderboard/tasks/t1-api-client.ts`
- 테스트: `src/blocks/block3-social/features/f2-leaderboard/tasks/t1-api-client.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t1-api-client.ts
import axios, { AxiosInstance } from 'axios';

export interface LeaderboardEntry {
  rank: number;
  email: string;
  time: number; // milliseconds
  timestamp: string; // ISO 8601
}

export interface LeaderboardResponse {
  entries: LeaderboardEntry[];
  total: number;
  myRank?: number;
}

class LeaderboardApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:3000') {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async getLeaderboard(limit: number = 100): Promise<LeaderboardResponse> {
    const response = await this.client.get<LeaderboardResponse>('/leaderboard', {
      params: { limit }
    });
    return response.data;
  }

  async getMyRank(email: string): Promise<number | null> {
    const response = await this.client.get<{ rank: number | null }>('/leaderboard/rank', {
      params: { email }
    });
    return response.data.rank;
  }
}

export const leaderboardApi = new LeaderboardApiClient();
```

**테스트 시나리오:**
1. **Top 100 조회**: `getLeaderboard(100)` → 100개 항목 반환
2. **네트워크 에러**: API 실패 시 에러 throw
3. **타임아웃**: 5초 초과 시 타임아웃 에러
4. **내 순위 조회**: `getMyRank("user@example.com")` → 순위 번호 반환
5. **순위 없음**: 기록 없는 이메일 → null 반환

**의존성:**
- `axios` ^1.6.0

---

### Task 3.2.2: React Query 설정 (5초 폴링)

**작업 목표:** React Query를 사용한 리더보드 데이터 폴링 및 캐싱

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f2-leaderboard/tasks/t2-query-hooks.ts`
- 테스트: `src/blocks/block3-social/features/f2-leaderboard/tasks/t2-query-hooks.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t2-query-hooks.ts
import { useQuery } from '@tanstack/react-query';
import { leaderboardApi, LeaderboardResponse } from './t1-api-client';

const LEADERBOARD_QUERY_KEY = 'leaderboard';
const REFETCH_INTERVAL = 5000; // 5초 폴링 (PRD 요구사항)

export function useLeaderboard(enabled: boolean = true) {
  return useQuery<LeaderboardResponse>({
    queryKey: [LEADERBOARD_QUERY_KEY],
    queryFn: () => leaderboardApi.getLeaderboard(100),
    refetchInterval: enabled ? REFETCH_INTERVAL : false,
    staleTime: 4000, // 4초 후 stale 처리
    gcTime: 60000, // 1분 캐시 유지
    enabled
  });
}

export function useMyRank(email: string | null, enabled: boolean = true) {
  return useQuery<number | null>({
    queryKey: [LEADERBOARD_QUERY_KEY, 'rank', email],
    queryFn: () => email ? leaderboardApi.getMyRank(email) : Promise.resolve(null),
    enabled: enabled && email !== null,
    refetchInterval: enabled && email !== null ? REFETCH_INTERVAL : false
  });
}
```

**테스트 시나리오:**
1. **초기 로딩**: 첫 렌더링 시 API 호출
2. **5초 폴링**: 5초마다 자동 refetch
3. **비활성화**: `enabled: false` → 폴링 중단
4. **에러 핸들링**: API 실패 시 `error` 상태 반환
5. **캐싱**: 동일 쿼리 키 → 캐시 데이터 재사용

**의존성:**
- `@tanstack/react-query` ^5.14.0
- Task 3.2.1 (API Client)

---

### Task 3.2.3: Top 100 리스트 렌더링

**작업 목표:** 리더보드 데이터를 테이블 형태로 렌더링하는 컴포넌트

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f2-leaderboard/tasks/t3-leaderboard-list.tsx`
- 테스트: `src/blocks/block3-social/features/f2-leaderboard/tasks/t3-leaderboard-list.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t3-leaderboard-list.tsx
import { LeaderboardEntry } from './t1-api-client';

interface LeaderboardListProps {
  entries: LeaderboardEntry[];
  currentUserEmail?: string;
}

export function LeaderboardList({ entries, currentUserEmail }: LeaderboardListProps) {
  const formatTime = (milliseconds: number): string => {
    const seconds = (milliseconds / 1000).toFixed(2);
    return `${seconds}s`;
  };

  return (
    <table data-testid="leaderboard-table">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Email</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry) => (
          <tr
            key={entry.rank}
            data-testid={`leaderboard-row-${entry.rank}`}
            className={entry.email === currentUserEmail ? 'highlight' : ''}
          >
            <td>{entry.rank}</td>
            <td>{entry.email}</td>
            <td>{formatTime(entry.time)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**테스트 시나리오:**
1. **데이터 렌더링**: 100개 항목 → 100개 행 렌더링
2. **시간 포맷**: 30000ms → "30.00s" 표시
3. **빈 리스트**: entries: [] → 빈 테이블 표시
4. **키 고유성**: 각 행의 key가 고유함
5. **현재 사용자 하이라이트**: `currentUserEmail` 매칭 시 클래스 추가 (Task 3.2.4에서 상세 처리)

**의존성:**
- Task 3.2.1 (LeaderboardEntry 타입)

---

### Task 3.2.4: 내 순위 하이라이트

**작업 목표:** 리더보드에서 현재 사용자의 순위를 시각적으로 강조

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f2-leaderboard/tasks/t4-rank-highlight.tsx`
- 테스트: `src/blocks/block3-social/features/f2-leaderboard/tasks/t4-rank-highlight.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t4-rank-highlight.tsx
import { useEffect, useRef } from 'react';

interface RankHighlightProps {
  entries: { rank: number; email: string }[];
  currentUserEmail: string | null;
  onRankFound?: (rank: number) => void;
}

export function RankHighlight({ entries, currentUserEmail, onRankFound }: RankHighlightProps) {
  const highlightRef = useRef<HTMLDivElement>(null);

  const myEntry = entries.find((entry) => entry.email === currentUserEmail);

  useEffect(() => {
    if (myEntry && highlightRef.current) {
      // 스크롤하여 내 순위 표시
      highlightRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
      onRankFound?.(myEntry.rank);
    }
  }, [myEntry, onRankFound]);

  if (!myEntry) {
    return (
      <div data-testid="no-rank-message">
        You are not in the Top 100 yet!
      </div>
    );
  }

  return (
    <div ref={highlightRef} data-testid="my-rank-highlight">
      <p>Your Rank: <strong>#{myEntry.rank}</strong></p>
    </div>
  );
}
```

**테스트 시나리오:**
1. **순위 찾기**: `currentUserEmail` 매칭 → 순위 표시
2. **순위 없음**: Top 100에 없음 → "You are not in the Top 100 yet!" 메시지
3. **스크롤**: 내 순위로 자동 스크롤
4. **콜백 호출**: `onRankFound(rank)` 호출
5. **null 이메일**: `currentUserEmail: null` → 메시지 표시 안 함

**의존성:**
- Task 3.2.3 (LeaderboardList)

---

### Task 3.2.5: 리더보드 UI 컴포넌트

**작업 목표:** Feature 3.2의 모든 Task를 통합한 완전한 리더보드 UI

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f2-leaderboard/index.tsx`
- 테스트: `src/blocks/block3-social/features/f2-leaderboard/index.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// index.tsx (Feature 3.2 통합)
import { useLeaderboard } from './tasks/t2-query-hooks';
import { LeaderboardList } from './tasks/t3-leaderboard-list';
import { RankHighlight } from './tasks/t4-rank-highlight';

interface LeaderboardProps {
  currentUserEmail: string | null;
  enabled?: boolean;
}

export function Leaderboard({ currentUserEmail, enabled = true }: LeaderboardProps) {
  const { data, isLoading, error } = useLeaderboard(enabled);

  if (isLoading) {
    return <div data-testid="leaderboard-loading">Loading leaderboard...</div>;
  }

  if (error) {
    return <div data-testid="leaderboard-error">Failed to load leaderboard</div>;
  }

  if (!data || data.entries.length === 0) {
    return <div data-testid="leaderboard-empty">No records yet!</div>;
  }

  return (
    <div data-testid="leaderboard-container">
      <h2>Top 100 Leaderboard</h2>
      <RankHighlight entries={data.entries} currentUserEmail={currentUserEmail} />
      <LeaderboardList entries={data.entries} currentUserEmail={currentUserEmail} />
    </div>
  );
}
```

**테스트 시나리오:**
1. **로딩 상태**: 초기 로딩 → "Loading leaderboard..." 표시
2. **에러 상태**: API 실패 → "Failed to load leaderboard" 표시
3. **빈 리더보드**: 데이터 없음 → "No records yet!" 표시
4. **정상 렌더링**: 100개 항목 → 테이블 + 하이라이트 표시
5. **5초 폴링**: 5초 후 자동 refetch

**의존성:**
- Task 3.2.2 (useLeaderboard)
- Task 3.2.3 (LeaderboardList)
- Task 3.2.4 (RankHighlight)

---

### 📊 Feature 3.2 Integration Test

> **⚠️ 작성 시점**: Task 3.2.1 ~ 3.2.5 모두 완료 후

**목적:** Feature 3.2의 5개 Task가 통합되어 PRD 요구사항을 달성하는지 검증

**파일:**
- `src/blocks/block3-social/features/f2-leaderboard/f2-leaderboard.integration.test.tsx`

**테스트 시나리오:**

#### 시나리오 1: 리더보드 조회 < 1초 (PRD Success Metrics)
```typescript
describe('Feature 3.2 Integration: 리더보드 조회 성능', () => {
  it('should load leaderboard within 1 second', async () => {
    const startTime = performance.now();

    render(<Leaderboard currentUserEmail="user@example.com" />);

    // Wait for data to appear
    await waitFor(() => {
      expect(screen.getByTestId('leaderboard-table')).toBeInTheDocument();
    });

    const endTime = performance.now();
    const duration = endTime - startTime;

    expect(duration).toBeLessThan(1000); // < 1초
  });
});
```

#### 시나리오 2: 5초 간격 실시간 업데이트 (PRD 요구사항)
```typescript
describe('Feature 3.2 Integration: 실시간 업데이트', () => {
  it('should refetch leaderboard every 5 seconds', async () => {
    vi.useFakeTimers();
    const apiSpy = vi.spyOn(leaderboardApi, 'getLeaderboard');

    render(<Leaderboard currentUserEmail="user@example.com" />);

    // 초기 호출
    await waitFor(() => expect(apiSpy).toHaveBeenCalledTimes(1));

    // 5초 후
    vi.advanceTimersByTime(5000);
    await waitFor(() => expect(apiSpy).toHaveBeenCalledTimes(2));

    // 10초 후
    vi.advanceTimersByTime(5000);
    await waitFor(() => expect(apiSpy).toHaveBeenCalledTimes(3));

    vi.useRealTimers();
  });
});
```

#### 시나리오 3: 내 순위 하이라이트 및 스크롤
```typescript
describe('Feature 3.2 Integration: 내 순위 하이라이트', () => {
  it('should highlight and scroll to my rank', async () => {
    const mockData = {
      entries: Array.from({ length: 100 }, (_, i) => ({
        rank: i + 1,
        email: i === 49 ? 'me@example.com' : `user${i}@example.com`,
        time: 30000 + i * 100,
        timestamp: new Date().toISOString()
      })),
      total: 100
    };

    vi.spyOn(leaderboardApi, 'getLeaderboard').mockResolvedValue(mockData);

    render(<Leaderboard currentUserEmail="me@example.com" />);

    await waitFor(() => {
      expect(screen.getByTestId('my-rank-highlight')).toBeInTheDocument();
    });

    expect(screen.getByTestId('my-rank-highlight')).toHaveTextContent('Your Rank: #50');
  });
});
```

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] Task 5개 Unit Test 모두 통과
- [ ] 커버리지 >90%
- [ ] PRD Success Metrics 달성
  - [ ] 리더보드 조회 < 1초
  - [ ] 5초 간격 자동 업데이트

---

## Feature 3.3: 개인 기록 관리 시스템 (Personal Record Manager)

### Feature 3.3 정의

**한 줄 요약:**
> 플레이어의 기록을 서버에 제출하고 개인 최고 기록을 관리하는 시스템

**완성 기준:**
- [ ] Task 5개 Unit Test 모두 통과
- [ ] Feature Integration Test 통과
- [ ] PRD Success Metrics 일부 달성
  - [ ] 골인 즉시 기록 전송
  - [ ] 기록 갱신 시 "New Record!" 애니메이션

**예상 소요 시간:** 2일 (Task 5개 × 90분 + Integration 1-2시간)

---

### Task 3.3.1: 기록 제출 API (Axios POST)

**작업 목표:** Axios를 사용한 플레이 기록 제출 API 클라이언트

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f3-record-manager/tasks/t1-submit-api.ts`
- 테스트: `src/blocks/block3-social/features/f3-record-manager/tasks/t1-submit-api.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t1-submit-api.ts
import axios, { AxiosInstance } from 'axios';

export interface RecordSubmission {
  email: string;
  time: number; // milliseconds
  timestamp: string; // ISO 8601
}

export interface RecordSubmissionResponse {
  success: boolean;
  rank: number;
  isNewRecord: boolean;
  previousBest?: number;
}

class RecordApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:3000') {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async submitRecord(record: RecordSubmission): Promise<RecordSubmissionResponse> {
    const response = await this.client.post<RecordSubmissionResponse>('/records', record);
    return response.data;
  }
}

export const recordApi = new RecordApiClient();
```

**테스트 시나리오:**
1. **기록 제출 성공**: `submitRecord(...)` → 성공 응답 반환
2. **신기록 달성**: `isNewRecord: true` + `previousBest` 값 확인
3. **네트워크 에러**: API 실패 시 에러 throw
4. **타임아웃**: 5초 초과 시 타임아웃 에러
5. **잘못된 데이터**: 유효하지 않은 입력 → 400 에러

**의존성:**
- `axios` ^1.6.0

---

### Task 3.3.2: 개인 기록 조회 API (Axios GET)

**작업 목표:** 플레이어의 개인 기록 히스토리 조회 API

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f3-record-manager/tasks/t2-fetch-api.ts`
- 테스트: `src/blocks/block3-social/features/f3-record-manager/tasks/t2-fetch-api.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t2-fetch-api.ts
import axios, { AxiosInstance } from 'axios';

export interface PersonalRecord {
  id: string;
  email: string;
  time: number;
  timestamp: string;
  rank: number;
}

export interface PersonalRecordsResponse {
  records: PersonalRecord[];
  bestTime: number | null;
  totalAttempts: number;
}

class PersonalRecordsApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:3000') {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async getPersonalRecords(email: string): Promise<PersonalRecordsResponse> {
    const response = await this.client.get<PersonalRecordsResponse>('/records/personal', {
      params: { email }
    });
    return response.data;
  }
}

export const personalRecordsApi = new PersonalRecordsApiClient();
```

**테스트 시나리오:**
1. **개인 기록 조회**: `getPersonalRecords("user@example.com")` → 기록 리스트 반환
2. **최고 기록**: `bestTime` 필드가 가장 짧은 시간
3. **시도 횟수**: `totalAttempts` 필드가 정확함
4. **기록 없음**: 첫 플레이어 → `records: []`, `bestTime: null`, `totalAttempts: 0`
5. **네트워크 에러**: API 실패 시 에러 throw

**의존성:**
- `axios` ^1.6.0

---

### Task 3.3.3: 기록 비교 로직 (현재 vs 최고)

**작업 목표:** 현재 기록과 최고 기록을 비교하여 개선 여부 판단

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f3-record-manager/tasks/t3-compare-logic.ts`
- 테스트: `src/blocks/block3-social/features/f3-record-manager/tasks/t3-compare-logic.test.ts`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t3-compare-logic.ts
export interface RecordComparison {
  isNewRecord: boolean;
  currentTime: number;
  bestTime: number | null;
  improvement: number | null; // milliseconds (음수: 개선, 양수: 악화)
  improvementPercent: number | null; // percentage
}

export function compareRecords(
  currentTime: number,
  previousBest: number | null
): RecordComparison {
  // 첫 기록인 경우
  if (previousBest === null) {
    return {
      isNewRecord: true,
      currentTime,
      bestTime: currentTime,
      improvement: null,
      improvementPercent: null
    };
  }

  // 신기록 달성
  const isNewRecord = currentTime < previousBest;
  const improvement = isNewRecord ? previousBest - currentTime : currentTime - previousBest;
  const improvementPercent = (improvement / previousBest) * 100;

  return {
    isNewRecord,
    currentTime,
    bestTime: isNewRecord ? currentTime : previousBest,
    improvement: isNewRecord ? improvement : -improvement, // 음수: 개선
    improvementPercent: isNewRecord ? improvementPercent : -improvementPercent
  };
}

export function formatImprovement(comparison: RecordComparison): string {
  if (comparison.improvement === null) {
    return 'First record!';
  }

  const sign = comparison.improvement > 0 ? '+' : '';
  const seconds = (Math.abs(comparison.improvement) / 1000).toFixed(2);
  const percent = Math.abs(comparison.improvementPercent!).toFixed(1);

  if (comparison.isNewRecord) {
    return `New record! -${seconds}s (${percent}% faster)`;
  } else {
    return `${sign}${seconds}s (${percent}% slower)`;
  }
}
```

**테스트 시나리오:**
1. **첫 기록**: `previousBest: null` → `isNewRecord: true`, `improvement: null`
2. **신기록**: `currentTime: 25000, previousBest: 30000` → `isNewRecord: true`, `improvement: 5000`
3. **악화**: `currentTime: 35000, previousBest: 30000` → `isNewRecord: false`, `improvement: -5000`
4. **개선율 계산**: 5초 개선 (30s → 25s) → `improvementPercent: 16.67%`
5. **포맷팅**: "New record! -5.00s (16.7% faster)"

**의존성:**
- 없음 (순수 함수)

---

### Task 3.3.4: 기록 갱신 알림 ("New Record!")

**작업 목표:** 신기록 달성 시 애니메이션 알림 컴포넌트

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f3-record-manager/tasks/t4-new-record-alert.tsx`
- 테스트: `src/blocks/block3-social/features/f3-record-manager/tasks/t4-new-record-alert.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// t4-new-record-alert.tsx
import { useEffect, useState } from 'react';
import { RecordComparison } from './t3-compare-logic';

interface NewRecordAlertProps {
  comparison: RecordComparison;
  onDismiss?: () => void;
  duration?: number; // milliseconds
}

export function NewRecordAlert({
  comparison,
  onDismiss,
  duration = 3000
}: NewRecordAlertProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (!comparison.isNewRecord) {
      setVisible(false);
      return;
    }

    const timer = setTimeout(() => {
      setVisible(false);
      onDismiss?.();
    }, duration);

    return () => clearTimeout(timer);
  }, [comparison.isNewRecord, duration, onDismiss]);

  if (!visible || !comparison.isNewRecord) {
    return null;
  }

  return (
    <div
      data-testid="new-record-alert"
      className="new-record-alert"
      style={{
        animation: 'bounce 0.5s ease-in-out',
        backgroundColor: '#4CAF50',
        color: 'white',
        padding: '20px',
        borderRadius: '8px',
        textAlign: 'center'
      }}
    >
      <h2>🎉 New Record! 🎉</h2>
      <p data-testid="improvement-text">
        {comparison.improvement !== null && (
          <>Improved by {(comparison.improvement / 1000).toFixed(2)}s ({comparison.improvementPercent?.toFixed(1)}% faster)</>
        )}
      </p>
    </div>
  );
}
```

**테스트 시나리오:**
1. **신기록 표시**: `isNewRecord: true` → 알림 표시
2. **자동 숨김**: 3초 후 → 알림 사라짐
3. **콜백 호출**: `onDismiss` 호출
4. **신기록 아님**: `isNewRecord: false` → 알림 표시 안 함
5. **개선 정보**: 개선 시간과 퍼센트 표시

**의존성:**
- Task 3.3.3 (RecordComparison)

---

### Task 3.3.5: 기록 관리 UI 컴포넌트

**작업 목표:** Feature 3.3의 모든 Task를 통합한 완전한 기록 관리 UI

**TDD 체크리스트:**
- [ ] **Red (15분)**: 테스트 작성 → `npm test` 실패 확인 🔴
- [ ] **Green (30분)**: 최소 구현 → `npm test` 통과 확인 🟢
- [ ] **Refactor (30분)**: 품질 개선 → `npm test` 여전히 통과 🔵
- [ ] **Mutation (15분)**: 변이 점수 >80% 확인 🧬

**실제 시간:** [기록]분

**파일:**
- 소스: `src/blocks/block3-social/features/f3-record-manager/index.tsx`
- 테스트: `src/blocks/block3-social/features/f3-record-manager/index.test.tsx`

**완료 조건:**
- [ ] Unit Test 통과
- [ ] 커버리지 >90%
- [ ] 변이 점수 >80%
- [ ] 복잡도 <10

**구현 상세:**
```typescript
// index.tsx (Feature 3.3 통합)
import { useMutation, useQuery } from '@tanstack/react-query';
import { recordApi, RecordSubmission } from './tasks/t1-submit-api';
import { personalRecordsApi } from './tasks/t2-fetch-api';
import { compareRecords } from './tasks/t3-compare-logic';
import { NewRecordAlert } from './tasks/t4-new-record-alert';
import { useState } from 'react';

interface RecordManagerProps {
  email: string;
  currentTime?: number; // 골인 시 전달
}

export function RecordManager({ email, currentTime }: RecordManagerProps) {
  const [showAlert, setShowAlert] = useState(false);

  // 개인 기록 조회
  const { data: personalRecords } = useQuery({
    queryKey: ['personalRecords', email],
    queryFn: () => personalRecordsApi.getPersonalRecords(email),
    enabled: !!email
  });

  // 기록 제출
  const submitMutation = useMutation({
    mutationFn: (record: RecordSubmission) => recordApi.submitRecord(record),
    onSuccess: (response) => {
      if (response.isNewRecord) {
        setShowAlert(true);
      }
    }
  });

  // 골인 시 자동 제출
  useEffect(() => {
    if (currentTime && email) {
      submitMutation.mutate({
        email,
        time: currentTime,
        timestamp: new Date().toISOString()
      });
    }
  }, [currentTime, email]);

  if (!personalRecords) {
    return <div>Loading your records...</div>;
  }

  const comparison = currentTime
    ? compareRecords(currentTime, personalRecords.bestTime)
    : null;

  return (
    <div data-testid="record-manager">
      <h3>Your Records</h3>
      <p>Best Time: {personalRecords.bestTime ? `${(personalRecords.bestTime / 1000).toFixed(2)}s` : 'N/A'}</p>
      <p>Total Attempts: {personalRecords.totalAttempts}</p>

      {comparison && showAlert && (
        <NewRecordAlert
          comparison={comparison}
          onDismiss={() => setShowAlert(false)}
        />
      )}

      <ul data-testid="records-list">
        {personalRecords.records.map((record) => (
          <li key={record.id}>
            {(record.time / 1000).toFixed(2)}s - Rank #{record.rank}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**테스트 시나리오:**
1. **개인 기록 표시**: 최고 기록 + 시도 횟수 표시
2. **골인 시 자동 제출**: `currentTime` prop 전달 → API 호출
3. **신기록 알림**: `isNewRecord: true` → 알림 표시
4. **기록 리스트**: 모든 기록 시간순 표시
5. **첫 플레이**: 기록 없음 → "N/A" 표시

**의존성:**
- Task 3.3.1 (submitRecord)
- Task 3.3.2 (getPersonalRecords)
- Task 3.3.3 (compareRecords)
- Task 3.3.4 (NewRecordAlert)

---

### 📊 Feature 3.3 Integration Test

> **⚠️ 작성 시점**: Task 3.3.1 ~ 3.3.5 모두 완료 후

**목적:** Feature 3.3의 5개 Task가 통합되어 PRD 요구사항을 달성하는지 검증

**파일:**
- `src/blocks/block3-social/features/f3-record-manager/f3-record-manager.integration.test.tsx`

**테스트 시나리오:**

#### 시나리오 1: 골인 즉시 기록 전송 (PRD 요구사항)
```typescript
describe('Feature 3.3 Integration: 골인 즉시 기록 전송', () => {
  it('should submit record immediately on finish', async () => {
    const apiSpy = vi.spyOn(recordApi, 'submitRecord');

    render(<RecordManager email="user@example.com" currentTime={30000} />);

    await waitFor(() => {
      expect(apiSpy).toHaveBeenCalledWith({
        email: 'user@example.com',
        time: 30000,
        timestamp: expect.any(String)
      });
    });
  });
});
```

#### 시나리오 2: 신기록 달성 시 "New Record!" 애니메이션
```typescript
describe('Feature 3.3 Integration: 신기록 알림', () => {
  it('should show "New Record!" alert when breaking record', async () => {
    // Mock: 이전 최고 기록 35초
    vi.spyOn(personalRecordsApi, 'getPersonalRecords').mockResolvedValue({
      records: [],
      bestTime: 35000,
      totalAttempts: 5
    });

    // Mock: 신기록 30초
    vi.spyOn(recordApi, 'submitRecord').mockResolvedValue({
      success: true,
      rank: 10,
      isNewRecord: true,
      previousBest: 35000
    });

    render(<RecordManager email="user@example.com" currentTime={30000} />);

    await waitFor(() => {
      expect(screen.getByTestId('new-record-alert')).toBeInTheDocument();
    });

    expect(screen.getByTestId('improvement-text')).toHaveTextContent('5.00s');
  });
});
```

#### 시나리오 3: 개인 기록 히스토리 표시
```typescript
describe('Feature 3.3 Integration: 개인 기록 히스토리', () => {
  it('should display personal record history', async () => {
    vi.spyOn(personalRecordsApi, 'getPersonalRecords').mockResolvedValue({
      records: [
        { id: '1', email: 'user@example.com', time: 30000, timestamp: '2025-11-08T10:00:00Z', rank: 10 },
        { id: '2', email: 'user@example.com', time: 35000, timestamp: '2025-11-08T09:00:00Z', rank: 20 }
      ],
      bestTime: 30000,
      totalAttempts: 2
    });

    render(<RecordManager email="user@example.com" />);

    await waitFor(() => {
      expect(screen.getByText('Best Time: 30.00s')).toBeInTheDocument();
    });

    expect(screen.getByText('Total Attempts: 2')).toBeInTheDocument();
    expect(screen.getByTestId('records-list').children).toHaveLength(2);
  });
});
```

**통과 기준:**
- [ ] 모든 Integration Test 통과
- [ ] Task 5개 Unit Test 모두 통과
- [ ] 커버리지 >90%
- [ ] PRD Success Metrics 달성
  - [ ] 골인 즉시 기록 전송
  - [ ] 신기록 시 "New Record!" 알림

---

## 🏗️ Block 3 Module Test

> **⚠️ 작성 시점**: Feature 3.1, 3.2, 3.3 Integration Test 모두 완료 후

**목적:** Block 3의 3개 Feature가 통합되어 전체 소셜 시스템으로 동작하는지 검증

**파일:**
- `src/blocks/block3-social/block3.module.test.tsx`

**테스트 시나리오:**

### 시나리오 1: 이메일 인증 → 게임 → 리더보드 전체 플로우

```typescript
describe('Block 3 Module Test: 전체 소셜 시스템', () => {
  it('should complete full social flow: auth → play → leaderboard', async () => {
    // Feature 3.1: 이메일 인증
    render(<EmailAuth onAuthSuccess={(email) => console.log(email)} />);
    await userEvent.type(screen.getByTestId('email-input'), 'player@example.com');
    await userEvent.click(screen.getByTestId('submit-button'));

    // Feature 3.3: 기록 제출 (골인 시뮬레이션)
    render(<RecordManager email="player@example.com" currentTime={30000} />);
    await waitFor(() => {
      expect(recordApi.submitRecord).toHaveBeenCalled();
    });

    // Feature 3.2: 리더보드 확인
    render(<Leaderboard currentUserEmail="player@example.com" />);
    await waitFor(() => {
      expect(screen.getByTestId('leaderboard-table')).toBeInTheDocument();
    });
  });
});
```

### 시나리오 2: 재방문 사용자 → 자동 로그인 → 리더보드

```typescript
describe('Block 3 Module Test: 재방문 사용자', () => {
  it('should auto-login and show leaderboard for returning user', async () => {
    // Given: 로컬스토리지에 이메일 저장됨
    localStorage.setItem('fly_paper_plane_email', 'returning@example.com');

    // Feature 3.1: 자동 로그인
    const onAuthSuccess = vi.fn();
    render(<EmailAuth onAuthSuccess={onAuthSuccess} />);
    await waitFor(() => {
      expect(onAuthSuccess).toHaveBeenCalledWith('returning@example.com');
    });

    // Feature 3.2: 리더보드 즉시 표시
    render(<Leaderboard currentUserEmail="returning@example.com" />);
    await waitFor(() => {
      expect(screen.getByTestId('my-rank-highlight')).toBeInTheDocument();
    });
  });
});
```

### 시나리오 3: PRD Success Metrics 검증

```typescript
describe('Block 3 Module Test: PRD Success Metrics', () => {
  it('should achieve all PRD success metrics', async () => {
    // Metric 1: 이메일 입력 → 게임 시작 < 3초
    const startTime = performance.now();
    render(<EmailAuth onAuthSuccess={() => {}} />);
    await userEvent.type(screen.getByTestId('email-input'), 'user@example.com');
    await userEvent.click(screen.getByTestId('submit-button'));
    const authTime = performance.now() - startTime;
    expect(authTime).toBeLessThan(3000);

    // Metric 2: 리더보드 조회 < 1초
    const leaderboardStart = performance.now();
    render(<Leaderboard currentUserEmail="user@example.com" />);
    await waitFor(() => {
      expect(screen.getByTestId('leaderboard-table')).toBeInTheDocument();
    });
    const leaderboardTime = performance.now() - leaderboardStart;
    expect(leaderboardTime).toBeLessThan(1000);

    // Metric 3: 재방문율 측정 (로컬스토리지 확인)
    expect(localStorage.getItem('fly_paper_plane_email')).not.toBeNull();
  });
});
```

**통과 기준:**
- [ ] 모든 Module Test 통과
- [ ] Feature 3개 Integration Test 모두 통과
- [ ] PRD Success Metrics 달성
  - [ ] 이메일 입력 → 게임 시작 < 3초
  - [ ] 리더보드 조회 < 1초
  - [ ] 재방문율 30% (로컬스토리지 이메일 재사용)

---

## 📦 Block 3 Dependencies (의존성)

### Block 간 의존성

**Block 3은 Block 2에 의존:**
- Block 2의 타이머 시스템에서 골인 시간 수신
- Block 2의 게임 상태 (Finished)에서 기록 제출 트리거

```typescript
// Block 2 → Block 3 데이터 흐름
interface GameFinishEvent {
  email: string;        // Block 3 Feature 3.1에서 제공
  finishTime: number;   // Block 2 Feature 2.2에서 측정
}

// Block 2에서 골인 이벤트 발생 시
onGameFinish((event: GameFinishEvent) => {
  // Block 3 Feature 3.3: 기록 제출
  recordApi.submitRecord({
    email: event.email,
    time: event.finishTime,
    timestamp: new Date().toISOString()
  });
});
```

### 외부 의존성

**Backend API (미구현):**
- `POST /records`: 기록 제출
- `GET /leaderboard`: Top 100 조회
- `GET /leaderboard/rank`: 내 순위 조회
- `GET /records/personal`: 개인 기록 조회

**환경 변수:**
```bash
# .env.local
VITE_API_URL=http://localhost:3000  # 개발 환경
VITE_API_URL=https://api.flypaperplane.com  # 프로덕션
```

---

## 🎯 Block 3 완료 체크리스트

### Task 체크리스트 (15개)

**Feature 3.1: 이메일 인증 시스템**
- [ ] Task 3.1.1: 이메일 입력 폼 UI
- [ ] Task 3.1.2: 이메일 형식 검증 (Zod)
- [ ] Task 3.1.3: 로컬스토리지 저장/로드
- [ ] Task 3.1.4: 인증 상태 관리 (Zustand)
- [ ] Task 3.1.5: 이메일 인증 UI 통합

**Feature 3.2: 리더보드 표시 시스템**
- [ ] Task 3.2.1: 리더보드 API 인터페이스
- [ ] Task 3.2.2: React Query 설정 (5초 폴링)
- [ ] Task 3.2.3: Top 100 리스트 렌더링
- [ ] Task 3.2.4: 내 순위 하이라이트
- [ ] Task 3.2.5: 리더보드 UI 컴포넌트

**Feature 3.3: 개인 기록 관리 시스템**
- [ ] Task 3.3.1: 기록 제출 API (Axios POST)
- [ ] Task 3.3.2: 개인 기록 조회 API (Axios GET)
- [ ] Task 3.3.3: 기록 비교 로직 (현재 vs 최고)
- [ ] Task 3.3.4: 기록 갱신 알림 ("New Record!")
- [ ] Task 3.3.5: 기록 관리 UI 컴포넌트

### Feature Integration Test (3개)
- [ ] Feature 3.1 Integration Test
- [ ] Feature 3.2 Integration Test
- [ ] Feature 3.3 Integration Test

### Block Module Test (1개)
- [ ] Block 3 Module Test (3개 Feature 통합)

### PRD Success Metrics
- [ ] 이메일 입력 → 게임 시작 < 3초
- [ ] 리더보드 조회 시간 < 1초
- [ ] 리더보드 5초 간격 실시간 업데이트
- [ ] 재방문율 30% 이상 (로컬스토리지 이메일)
- [ ] 리더보드 등록 수 100명 이상 (출시 후 2주)

---

## 📄 파일 구조 (AI 최적화)

```
src/blocks/block3-social/
├─ features/
│  ├─ f1-email-auth/
│  │  ├─ tasks/
│  │  │  ├─ t1-email-form.tsx
│  │  │  ├─ t1-email-form.test.tsx
│  │  │  ├─ t2-email-schema.ts
│  │  │  ├─ t2-email-schema.test.ts
│  │  │  ├─ t3-local-storage.ts
│  │  │  ├─ t3-local-storage.test.ts
│  │  │  ├─ t4-auth-store.ts
│  │  │  └─ t4-auth-store.test.ts
│  │  ├─ index.tsx (Feature 3.1 통합)
│  │  └─ f1-email-auth.integration.test.tsx
│  │
│  ├─ f2-leaderboard/
│  │  ├─ tasks/
│  │  │  ├─ t1-api-client.ts
│  │  │  ├─ t1-api-client.test.ts
│  │  │  ├─ t2-query-hooks.ts
│  │  │  ├─ t2-query-hooks.test.ts
│  │  │  ├─ t3-leaderboard-list.tsx
│  │  │  ├─ t3-leaderboard-list.test.tsx
│  │  │  ├─ t4-rank-highlight.tsx
│  │  │  └─ t4-rank-highlight.test.tsx
│  │  ├─ index.tsx (Feature 3.2 통합)
│  │  └─ f2-leaderboard.integration.test.tsx
│  │
│  └─ f3-record-manager/
│     ├─ tasks/
│     │  ├─ t1-submit-api.ts
│     │  ├─ t1-submit-api.test.ts
│     │  ├─ t2-fetch-api.ts
│     │  ├─ t2-fetch-api.test.ts
│     │  ├─ t3-compare-logic.ts
│     │  ├─ t3-compare-logic.test.ts
│     │  ├─ t4-new-record-alert.tsx
│     │  └─ t4-new-record-alert.test.tsx
│     ├─ index.tsx (Feature 3.3 통합)
│     └─ f3-record-manager.integration.test.tsx
│
├─ index.ts (Block 3 Module)
└─ block3.module.test.tsx
```

---

## 🚀 다음 단계

**Block 3 설계 완료 후:**

1. **개발 킥오프 (사용자 트리거: "개발 시작해")**
   - 5단계 초기화 스크립트 실행
   - 프로젝트 구조 생성
   - 의존성 설치
   - 첫 Red Test 작성

2. **TDD 개발 순서 (피라미드):**
   ```
   Block 1 → Feature 1.1 → Task 1.1.1 (Red-Green-Refactor-Mutation)
   → Task 1.1.2 ~ 1.1.5
   → Feature 1.1 Integration TDD ⬆️
   → Feature 1.2, 1.3
   → Block 1 Module TDD ⬆️
   → Block 2, 3
   → Product E2E TDD ⬆️
   ```

3. **최종 목표:**
   - 모든 PRD Success Metrics 달성
   - 테스트 커버리지 >90%
   - Mutation Score >80%
   - 프로덕션 배포 준비 완료

---

**작성 완료일:** 2025-11-08
**다음 작업:** "개발 시작해" 트리거 대기
**블럭 상태:** 설계 완료 → 대기
