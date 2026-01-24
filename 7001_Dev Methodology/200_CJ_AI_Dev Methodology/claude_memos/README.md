# Claude Code AI Memory System

## 📌 개요

이 폴더는 **Claude Code AI의 프로젝트 메모리 시스템**입니다.
모든 작업 세션의 컨텍스트를 자동으로 기록하고, 프로젝트 진화 과정을 학습 가능한 형태로 보존합니다.

## 📁 폴더 구조

```
.claude_memos/
├─ sessions/          # 세션별 자동 메모
│  └─ 20251108_173800.md
├─ work_logs/         # 일일 작업 로그
│  └─ 2025-11-08.md
└─ evolution/         # 진화 보고서 (마일스톤)
   └─ Block1_Flight_Control_v1.md
```

## 🎯 메모리 타입

### 1. Session Memo (세션 메모)
- **용도**: 모든 작업 세션의 실시간 기록
- **생성**: 세션 종료 시 자동 (1-2분)
- **트리거**: `"메모해줘"` 또는 자동
- **파일명**: `YYYYMMDD_HHMMSS.md`

### 2. Work Log (작업 로그)
- **용도**: Task 완료 시 실시간 자동 기록 (누적)
- **생성**: Task 1개 완료 시마다 자동 append
- **트리거**: **자동 (TODO를 completed로 변경 시)**
- **파일명**: `YYYY-MM-DD.md`

### 3. Evolution Report (진화 보고서)
- **용도**: 마일스톤 달성 시 상세 진화 과정 분석
- **생성**: 주요 단계 완료 시 (1-2시간)
- **트리거**: `"진화 보고서 작성해줘"`
- **파일명**: `[topic]_v[N].md`

## 🚀 사용법

### ⚡ 자동 기록 (트리거 불필요)

**Work Log (작업 로그):**
```
Task 완료 → TodoWrite에서 "completed"로 변경
→ 즉시 자동 append (.claude_memos/work_logs/YYYY-MM-DD.md)

예시:
TodoWrite([
  {content: "Task 1.1.1: Keyboard Input", status: "completed", ...}
])
→ 2025-11-08.md에 Task 1.1.1 내용 자동 추가 (사용자 트리거 불필요!)
```

### 📝 수동 기록 (사용자 트리거)

**세션 메모 생성:**
```
사용자: "메모해줘" 또는 "작업내용을 메모해줘"
Claude: .claude_memos/sessions/20251108_190000.md 생성
```

**진화 보고서 생성:**
```
사용자: "Block 1 진화 보고서 작성해줘"
Claude: .claude_memos/evolution/Block1_Flight_Control_v1.md 생성
```

### 📖 메모 읽기 (컨텍스트 로드)

**세션 메모 읽기:**
```
사용자: "지난 세션 메모 읽어줘"
Claude: 최근 세션 메모를 읽고 이전 작업 컨텍스트 이해
```

**작업 로그 확인:**
```
사용자: "오늘 작업 로그 보여줘"
Claude: .claude_memos/work_logs/2025-11-08.md 읽기

사용자: "이번 주 작업 로그 요약해줘"
Claude: 이번 주 모든 work_logs 분석 및 요약
```

## 🤖 AI 에이전트 통합

**메모리 시스템 에이전트 역할 분담:**

### 1. Work Log → **개발 에이전트 직접 작성** ⚡
- **담당**: 코딩 전문 에이전트 (code_developer)
- **방식**: Task 완료 시 자동 append
- **이유**: Task 개발 과정을 가장 잘 아는 사람
- **에이전트 불필요** - 개발 중 즉시 기록

### 2. Session Memo → **`session-memo-writer` 에이전트** 📝
- **담당**: 세션 메모 자동 생성 전문가
- **방식**: "메모해줘" 트리거 시 호출
- **역할**: 세션 전체의 큰 그림 파악, 간결한 요약
- **출력**: .claude_memos/sessions/YYYYMMDD_HHMMSS.md

### 3. Evolution Report → **`memory-report-generator` 에이전트** 🧬
- **담당**: AI 기억 시스템 전문가
- **방식**: "진화 보고서 작성해줘" 트리거 시 호출
- **역할**: "왜 이렇게 진화했는가" 심층 분석
- **출력**: .claude_memos/evolution/[topic]_v[N].md
- **특징**: Work Log + Session Memo 모두 분석하여 통찰 도출

**글로벌 CLAUDE.md 에이전트와 연계:**
- 글로벌 에이전트 (requirements_analyst, system_architect 등)가 생성한 결과물이 이 메모리 시스템에 자동 기록됨
- 세션 간 컨텍스트 연속성 보장

## 🔒 보안 및 Git 관리

**중요:** 이 폴더는 `.gitignore`에 추가되어 있습니다.
- 세션 메모에는 민감한 작업 내용, 설계 결정사항이 포함될 수 있음
- 로컬 개발 환경에서만 유지
- Git 커밋 대상이 아님

## 📚 참고 문서

- **프로젝트 CLAUDE.md**: AI Memory System 섹션 참조
- **글로벌 CLAUDE.md**: AI 에이전트 시스템 전체 구조
- **CJ_AI_개발방법론.md**: 4-Layer Fractal TDD 개발 방법론

## 🌟 Best Practices

1. **세션 메모는 가볍게**: 1-2분 내로 빠르게 기록
2. **작업 로그는 구조화**: 일관된 포맷으로 통합
3. **진화 보고서는 심층적**: "왜?"에 집중, 실패도 포함
4. **타임스탬프 활용**: 모든 메모에 정확한 시간 기록
5. **컨텍스트 체인**: 이전 메모 참조로 연결성 유지

## 📖 Example Workflow

```
# 아침: 새 세션 시작 (09:00)
"지난 세션 메모 읽어줘"
→ 어제 작업 컨텍스트 이해

"오늘 작업 로그 보여줘"
→ 이미 완료된 Task 확인

# 작업 중: Task 1.1.1 개발 (09:30-10:30)
Task 1.1.1: Keyboard Input Handler TDD
→ TodoWrite로 "completed"로 변경
→ ⚡ Work Log 자동 append (트리거 불필요!)

# 작업 중: Task 1.1.2 개발 (10:45-12:00)
Task 1.1.2: Touch Input Handler TDD
→ TodoWrite로 "completed"로 변경
→ ⚡ Work Log 자동 append (누적)

# 점심: 중간 체크포인트 (12:30)
"작업내용을 메모해줘"
→ 오전 작업 세션 메모 생성

# 저녁: 하루 마무리 (18:00)
"메모해줘"
→ 오후 작업 세션 메모 생성
(Work Log는 이미 Task마다 자동 기록됨)

# 주말: Block 1 완료
"Block 1 진화 보고서 작성해줘"
→ 1주일간의 Work Log + Session Memo 분석
```

---

**생성일**: 2025-11-08
**버전**: v1.0
**프로젝트**: 7100_Fly_paper_plane (종이비행기 날아라)
**시스템**: Claude Code AI Memory System
