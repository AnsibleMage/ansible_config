# 206_Debugging_Log_템플릿_Roblox

> **기반**: [[./203_VCR_개발방법론_v1.1|VCR 개발방법론 v1.1]]
> **용도**: 디버깅 과정 및 교훈 기록
> **작성 시점**: 개발 중 이슈 발생 시

---

<!-- AI_CONTEXT
Level: Task/Feature
Purpose: 디버깅 과정 문서화 및 교훈 축적
Importance: VCR Layer 5 (ITERATE & DOCUMENT) 핵심
-->

## 📋 프로젝트 정보

| 항목 | 내용 |
|:---|:---|
| **프로젝트명** | [프로젝트명] |
| **관련 Block** | Block [N] |
| **마지막 업데이트** | [날짜] |

---

## 🐛 이슈 목록

| # | 증상 | 상태 | 영향도 |
|:---:|:---|:---:|:---:|
| 1 | [증상 요약] | ✅ | 높음 |
| 2 | [증상 요약] | ✅ | 중간 |
| 3 | [증상 요약] | 🔄 | 낮음 |

---

## Issue #1: [증상 요약]

### 기본 정보
| 항목 | 내용 |
|:---|:---|
| **발생 시점** | [날짜/시간] |
| **관련 Feature** | Feature [N.M] |
| **영향도** | [높음/중간/낮음] |
| **상태** | ✅ 해결됨 |

### 증상
[무엇이 잘못되었는지 상세 설명]

```lua
-- 문제 발생 코드 (있다면)
```

### Output 로그
```
[에러 메시지 또는 경고 복사]
```

### 원인 분석
[왜 이 문제가 발생했는지 분석]

### 해결 방법
```lua
-- 수정된 코드
```

### 교훈
> 💡 [다음에 기억해야 할 핵심 포인트]

---

## Issue #2: [증상 요약]

### 기본 정보
| 항목 | 내용 |
|:---|:---|
| **발생 시점** | [날짜/시간] |
| **관련 Feature** | Feature [N.M] |
| **영향도** | [높음/중간/낮음] |
| **상태** | ✅ 해결됨 |

### 증상
[상세 설명]

### 원인 분석
[원인]

### 해결 방법
[해결]

### 교훈
> 💡 [교훈]

---

## Issue #3: [증상 요약]

(같은 형식으로 계속...)

---

## 📚 축적된 교훈 (Lessons Learned)

### Rojo 관련
- [ ] 대량 변경 시 Rojo serve 재시작 필요
- [ ] `.project.json` 경로 오류 주의
- [ ] [추가 교훈]

### Luau 코딩
- [ ] BrickColor 대신 Color3.fromRGB() 사용
- [ ] Guard Clauses로 조기 반환
- [ ] [추가 교훈]

### Studio 관련
- [ ] CanCollide vs Touched 이벤트 주의
- [ ] Anchored 설정 확인
- [ ] [추가 교훈]

### Server/Client
- [ ] RemoteEvent 양쪽 처리 필요
- [ ] Server Authority 원칙
- [ ] [추가 교훈]

---

## 🔧 자주 사용하는 디버깅 패턴

### 1. Print 디버깅
```lua
print("[DEBUG] Variable:", someVariable)
print("[DEBUG] Type:", typeof(someVariable))
print("[DEBUG] Function called at:", tick())
```

### 2. 조건부 로그
```lua
local DEBUG_MODE = true

local function debugLog(...)
    if DEBUG_MODE then
        print("[DEBUG]", ...)
    end
end
```

### 3. Output 필터링
- `[ERROR]` - 에러
- `[WARN]` - 경고
- `[DEBUG]` - 디버그
- `[INFO]` - 정보

---

## 📝 체크리스트 (디버깅 시작 전)

- [ ] Output 창 열기
- [ ] 에러 메시지 확인
- [ ] 관련 스크립트 위치 파악
- [ ] Rojo 동기화 상태 확인
- [ ] Play Mode vs Edit Mode 확인

---

**VCR Methodology v1.1 Template**
