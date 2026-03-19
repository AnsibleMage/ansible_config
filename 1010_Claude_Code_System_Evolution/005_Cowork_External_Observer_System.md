# Cowork 외부 관찰자 시스템 (External Observer System)

> **작성일**: 2026-02-04
> **발견**: Cowork가 Claude Code의 "외부 관찰자"로서 시스템 개선 가능
> **핵심 인사이트**: 내부에서 불가능한 것을 외부에서 해결

---

## 1. 핵심 발견: 3가지 역량

### 1.1 Claude Code 세션 실시간 관찰

```
Cowork는 Claude Code의 대화 로그를 실시간으로 읽을 수 있다

~/.claude/projects/{project}/
├── sessions-index.json      # 세션 인덱스
└── {sessionId}.jsonl        # 대화 로그 (실시간 업데이트)
```

**의미**:
- Claude Code가 실행 중일 때도 대화 내용 분석 가능
- 세션 종료 후 자동 처리 가능
- 크로스 세션 컨텍스트 유지 가능

### 1.2 macOS LaunchAgents 제어

```
~/Library/LaunchAgents/
├── com.user.claude-session-archiver.plist   # 생성 가능
├── com.user.claude-daily-summary.plist      # 생성 가능
└── com.user.claude-system-optimizer.plist   # 생성 가능
```

**의미**:
- 맥북 시작/종료 시 자동 스크립트 실행
- 정기 예약 작업 (매일/매주)
- Claude Code와 독립적으로 백그라운드 작업

### 1.3 Claude Code 설정 외부 수정

```
Cowork가 수정 가능한 Claude Code 파일들:

~/.claude/
├── CLAUDE.md              # 가이드라인 (Cowork가 분석/개선)
├── settings.json          # 설정 (Hook, Permission 등)
├── hooks/                 # Hook 스크립트
├── commands/              # 슬래시 커맨드
├── scripts/               # 분석 스크립트
└── memory/                # 메모리 파일
```

**의미**:
- Claude Code가 자신을 개선하는 데 한계가 있음
- Cowork가 외부에서 분석 → 수정 → 검증 가능
- "메타 레벨" 시스템 최적화

---

## 2. 왜 "외부 관찰자"가 필요한가?

### Claude Code의 내부 한계

```
┌─────────────────────────────────────────────┐
│           Claude Code 내부                   │
│                                             │
│  ❌ 자신의 세션 로그를 실시간 분석 불가        │
│  ❌ 응답 완료 후 추가 작업 불가 (Stop Hook)    │
│  ❌ 맥북 시스템 레벨 작업 제한                │
│  ❌ 백그라운드에서 독립 작업 불가             │
│  ❌ 자신의 비효율을 객관적으로 보기 어려움     │
│                                             │
└─────────────────────────────────────────────┘
                    ↓
            외부 관찰자 필요
                    ↓
┌─────────────────────────────────────────────┐
│           Cowork (외부)                      │
│                                             │
│  ✅ 세션 로그 실시간 읽기                     │
│  ✅ 세션 종료 후에도 작업 가능                │
│  ✅ macOS LaunchAgents 생성/수정            │
│  ✅ 독립적 백그라운드 프로세스 실행           │
│  ✅ 객관적 시스템 분석 및 개선               │
│                                             │
└─────────────────────────────────────────────┘
```

### 비유: 의사와 환자

```
Claude Code = 환자 (자기 진단 한계)
Cowork = 의사 (외부에서 객관적 진단/치료)

환자가 자기 몸을 느낄 수는 있지만,
의사만큼 객관적으로 분석하고 처방할 수 없음
```

---

## 3. 실현 가능한 활용 사례

### 3.1 🧠 세션 종료 시 자동 메모리 추출

**문제**: Claude Code의 Stop Hook은 응답 후 추가 작업 불가

**해결**: Cowork + LaunchAgent

```bash
# ~/Library/LaunchAgents/com.user.claude-session-extractor.plist

맥북 종료 시 (또는 주기적으로):
1. ~/.claude/projects/ 스캔
2. 마지막 세션 로그 분석
3. 중요 내용 자동 추출
4. ~/.claude/memory/ 에 저장
```

**구현 시나리오**:
```
[하루 종료]
     ↓
LaunchAgent 실행
     ↓
오늘의 Claude Code 세션들 스캔
     ↓
중요 대화/결정/코드 자동 추출
     ↓
메모리 파일 자동 생성
     ↓
[다음 날 Claude Code가 컨텍스트로 활용]
```

### 3.2 📊 일일/주간 대화 요약 자동 생성

```bash
# 매일 23:00 실행
# ~/scripts/claude-daily-summary.sh

1. 오늘의 모든 세션 로그 수집
2. Cowork/Claude API로 요약 생성
3. 저장: ~/.claude/summaries/2026-02-04_daily.md

내용:
- 오늘 작업한 프로젝트들
- 주요 결정 사항
- 발견된 문제/해결책
- 내일 이어서 할 작업
```

### 3.3 🔍 Claude Code 사용 패턴 분석

```
주간 리포트 자동 생성:

┌─────────────────────────────────────┐
│  앤(An)의 Claude Code 사용 분석      │
│  2026-02-01 ~ 2026-02-07           │
├─────────────────────────────────────┤
│  총 세션: 45회                      │
│  평균 세션 길이: 23분               │
│  가장 많이 사용한 체인: DevChain     │
│  가장 많이 사용한 에이전트: opus     │
│  미사용 체인: MetaThinkChain        │
│                                    │
│  [개선 제안]                        │
│  - MetaThinkChain 제거 권장         │
│  - WebDevChain 사용 증가 추세       │
│  - HotfixChain 트리거 키워드 추가   │
└─────────────────────────────────────┘
```

### 3.4 ⚡ CLAUDE.md 자동 최적화 제안

```
Cowork 분석 → CLAUDE.md 개선안 생성

주기적으로:
1. CLAUDE.md 읽기
2. 최근 세션 로그와 비교
3. 비효율/중복/미사용 항목 탐지
4. 개선안 제안 또는 자동 수정
```

**예시 발견**:
```
🔍 CLAUDE.md V3.8 분석 결과:

[중복 발견]
- Skill Mapping (271-337줄) ↔ Agent System (341-375줄)
  → 테이블 통합 권장

[미사용 탐지]
- MetaThinkChain: 최근 30일 사용 0회
  → 제거 또는 트리거 수정 권장

[비대화]
- Rails 8 섹션: 80줄 (전체의 9.5%)
  → 별도 파일로 분리 권장
```

### 3.5 🔄 크로스 세션 컨텍스트 유지

**문제**: Claude Code 세션이 종료되면 컨텍스트 손실

**해결**:
```
세션 A 종료
     ↓
Cowork가 세션 A 로그 분석
     ↓
핵심 컨텍스트 추출 → context_bridge.md
     ↓
세션 B 시작 시 Hook으로 주입
     ↓
세션 B가 세션 A의 컨텍스트 이어받음
```

### 3.6 🛡️ 시스템 헬스 체크

```bash
# 매주 월요일 09:00 실행
# ~/scripts/claude-health-check.sh

체크 항목:
1. CLAUDE.md 문법 오류
2. Hook 스크립트 실행 권한
3. 메모리 파일 중복/비대화
4. settings.json 스키마 유효성
5. 디스크 사용량 (세션 로그)

결과 → ~/.claude/health/2026-02-04_health.md
```

---

## 4. LaunchAgent 구현 예시

### 4.1 세션 아카이버

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.an.claude-session-archiver</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/changjaeyou/.claude/scripts/session-archiver.sh</string>
    </array>

    <!-- 매일 23:00 실행 -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/tmp/claude-archiver.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/claude-archiver-error.log</string>
</dict>
</plist>
```

### 4.2 시스템 시작 시 컨텍스트 로더

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.an.claude-context-loader</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/changjaeyou/.claude/scripts/context-loader.sh</string>
    </array>

    <!-- 로그인 시 실행 -->
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

---

## 5. 아키텍처: Cowork + Claude Code 협력 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    macOS System Level                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  LaunchAgents (백그라운드)                               │   │
│  │  • 일일 세션 아카이브                                    │   │
│  │  • 주간 사용 패턴 분석                                   │   │
│  │  • 시스템 헬스 체크                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                     File System Layer                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ~/.claude/                                              │   │
│  │  ├── CLAUDE.md        ← Cowork 분석/수정                 │   │
│  │  ├── memory/          ← 자동 메모리 생성                 │   │
│  │  ├── summaries/       ← 일일/주간 요약                   │   │
│  │  ├── health/          ← 헬스 체크 리포트                 │   │
│  │  └── projects/        → Cowork 실시간 읽기               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                    ↕                          ↕
┌─────────────────────────┐      ┌─────────────────────────────┐
│    Claude Code          │      │        Cowork               │
│    (내부 실행자)         │      │        (외부 관찰자)         │
│                         │      │                             │
│  • 사용자 요청 처리      │ ←─→ │  • 세션 로그 분석            │
│  • 코드 개발            │      │  • 시스템 최적화 제안        │
│  • Hook 실행            │      │  • LaunchAgent 관리         │
│  • 메모리 활용          │      │  • CLAUDE.md 개선           │
│                         │      │                             │
│  [한계]                 │      │  [역할]                     │
│  • 자기 분석 어려움     │      │  • 객관적 분석              │
│  • 응답 후 작업 불가    │      │  • 시스템 레벨 작업         │
│  • 백그라운드 불가      │      │  • 백그라운드 자동화        │
└─────────────────────────┘      └─────────────────────────────┘
```

---

## 6. 실행 로드맵

### Phase 1: 기반 구축 (즉시 가능)

| 항목 | 설명 | 상태 |
|------|------|------|
| 세션 로그 분석 | Cowork로 jsonl 파일 분석 | ✅ 검증됨 |
| CLAUDE.md 분석 | 비효율/중복 탐지 | ✅ 검증됨 |
| 메모리 자동 생성 | Cowork → memory/ 저장 | ✅ 검증됨 |

### Phase 2: 자동화 (LaunchAgent)

| 항목 | 설명 | 우선순위 |
|------|------|----------|
| 일일 세션 아카이버 | 매일 23:00 실행 | HIGH |
| 시스템 헬스 체크 | 매주 월요일 | MEDIUM |
| 컨텍스트 브릿지 | 세션 간 컨텍스트 유지 | HIGH |

### Phase 3: 고급 기능

| 항목 | 설명 | 복잡도 |
|------|------|--------|
| 자동 최적화 제안 | 사용 패턴 기반 | 중간 |
| 크로스 세션 학습 | 장기 패턴 인식 | 높음 |
| 자가 개선 루프 | Cowork ↔ Claude Code | 높음 |

---

## 7. 결론: 외부 관찰자의 가치

```
"내부에서 자신을 완전히 이해할 수 없다"
- 괴델의 불완전성 정리와 유사한 원리

Claude Code는 자신의 시스템을 어느 정도 분석할 수 있지만,
외부 관찰자(Cowork)가 있을 때 더 객관적이고 완전한 개선이 가능하다.

┌─────────────────────────────────────┐
│  Claude Code + Cowork = 완전한 시스템  │
│                                     │
│  내부 실행 + 외부 관찰 = 자가 개선 루프 │
└─────────────────────────────────────┘
```

---

## 관련 문서

- [[Auto_Memory_Save_Hook_V2_Implementation]]
- [[Chain_System_V2.0_for_CLAUDE]]
- [[Memory_Auto_Save_Solution_Proposal]]
- [[An_Profile_and_Chain_Upgrade_Report]]
