# 🧠 메모리 자동 저장 - 새로운 접근법 제안

> **분석일**: 2026-02-04
> **분석자**: Cowork (외부 관점에서 Claude Code 시스템 분석)

---

## 1. 기존 시도와 실패 원인

### 시도한 방법들

| 방법 | 설명 | 결과 |
|------|------|------|
| **Stop Hook** | 응답 완료 후 Hook 실행 | ❌ 스키마 에러 (`hookSpecificOutput` 미지원) |
| **지침 기반** | CLAUDE.md에 규칙 추가 | △ 100% 보장 안 됨 (Claude 재량 의존) |
| **UserPromptSubmit** | 다음 프롬프트 시 이전 작업 알림 | △ 비직관적, 지연 발생 |

### 근본적 한계

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code 내부 한계                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Stop Hook = 응답 완료 "후" 실행                          │
│     → Claude에게 새 지시 주입 불가                           │
│     → hookSpecificOutput, additionalContext 미지원          │
│                                                             │
│  2. 응답 내에서 자기 자신에게 명령 불가                       │
│     → "이 응답 끝나면 XX해" 같은 메타 지시 불가               │
│                                                             │
│  3. 외부 프로세스 트리거 불가                                 │
│     → Hook은 정보 전달만, 외부 스크립트 실행 제한             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 핵심 발견: Claude Code 세션 데이터 구조

Cowork에서 Claude Code 내부 데이터에 접근할 수 있습니다!

### 데이터 위치

```
~/.claude/
├── projects/
│   └── -Users-changjaeyou/
│       ├── sessions-index.json     ← 모든 세션 메타데이터
│       ├── {sessionId}.jsonl       ← 세션별 전체 대화 로그
│       └── {sessionId}/
│           └── subagents/          ← 서브에이전트 로그
│
├── history.jsonl                   ← 모든 프롬프트 기록
└── memory/                         ← 메모리 저장소
```

### sessions-index.json 구조

```json
{
  "entries": [
    {
      "sessionId": "29d7e4df-...",
      "firstPrompt": "Rails 8 게임 개발...",
      "summary": "Rails 8 Game Dev Research",
      "messageCount": 21,
      "created": "2026-02-03T13:43:14.423Z",
      "modified": "2026-02-03T13:57:41.714Z"
    }
  ]
}
```

### {sessionId}.jsonl 구조

```jsonl
{"type":"user","message":{"content":"사용자 프롬프트..."}}
{"type":"assistant","content":[{"type":"text","text":"응답..."}]}
{"type":"tool_use","name":"WebSearch","input":{...}}
```

---

## 3. 새로운 접근법: "Session Memory Extractor"

### 핵심 아이디어

```
┌─────────────────────────────────────────────────────────────┐
│  기존: Claude Code 내부에서 자기 자신을 개선하려 함           │
│        → Hook 제한, 스키마 제한에 막힘                       │
│                                                             │
│  신규: Cowork가 외부에서 Claude Code 데이터를 분석           │
│        → 제한 없음, 100% 자동화 가능                         │
└─────────────────────────────────────────────────────────────┘
```

### 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                Session Memory Extractor                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ Claude Code │ ──► │  Session    │ ──► │   Cowork    │   │
│  │   세션 종료  │     │   Data      │     │  Extractor  │   │
│  └─────────────┘     │  (.jsonl)   │     └──────┬──────┘   │
│                      └─────────────┘            │          │
│                                                 ▼          │
│                                        ┌─────────────┐     │
│                                        │   Memory    │     │
│                                        │   Files     │     │
│                                        │  (.md)      │     │
│                                        └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 처리 흐름

```
1. 트리거 (선택 가능)
   ├── [A] Cowork Shortcut (정기 실행)
   ├── [B] 수동 호출 (/extract-memories)
   └── [C] 파일 감시 (launchd/cron)

2. sessions-index.json 스캔
   └── 마지막 추출 이후 새로운/수정된 세션 식별

3. 각 세션 분석
   ├── messageCount > 5 (의미 있는 세션)
   ├── summary 확인 (에러 세션 제외)
   └── 이미 추출된 세션 스킵

4. 세션 데이터 파싱 ({sessionId}.jsonl)
   ├── 사용자 프롬프트 추출
   ├── Claude 응답 핵심 추출
   ├── 사용된 도구/에이전트/스킬 추출
   └── 생성된 파일 목록 추출

5. 메모리 파일 생성
   └── ~/.claude/memory/YYMM_SEQ_keyword.md

6. 추출 기록 업데이트
   └── ~/.claude/memory/.extracted_sessions.json
```

---

## 4. 구현 옵션 비교

### Option A: Cowork Shortcut (추천)

```
장점:
  ✅ 정기 실행 가능 (매일/매주)
  ✅ Cowork UI에서 관리
  ✅ 수동 트리거도 가능
  ✅ 설정 변경 용이

단점:
  ⚠️ Cowork 실행 필요
  ⚠️ 실시간 아님 (배치 처리)

구현:
  /create-shortcut "memory-extract" → Python 스크립트 실행
```

### Option B: Python 스크립트 + Cron

```
장점:
  ✅ Cowork 없이도 실행
  ✅ 시스템 수준 자동화
  ✅ 더 세밀한 스케줄링

단점:
  ⚠️ macOS launchd 설정 필요
  ⚠️ 디버깅 어려움

구현:
  ~/Library/LaunchAgents/com.claude.memory-extractor.plist
  → Python 스크립트 정기 실행
```

### Option C: MCP 서버 확장

```
장점:
  ✅ Claude Code에서 직접 호출 가능
  ✅ 실시간 처리 가능

단점:
  ⚠️ 기존 MCP 서버 수정 필요
  ⚠️ 복잡도 증가

구현:
  prompt-analyzer MCP에 extract_memories 도구 추가
```

---

## 5. 추천 구현: Cowork Shortcut + Python

### 이유

1. **외부에서 처리** → Claude Code 제한 우회
2. **정기 실행** → 누락 없이 모든 세션 처리
3. **관리 용이** → Cowork에서 실행/중지/수정
4. **증분 처리** → 이미 추출된 세션 스킵

### Python 스크립트 설계

```python
# ~/.claude/scripts/memory_extractor.py

"""
Session Memory Extractor
- sessions-index.json 스캔
- 새로운 세션 식별
- .jsonl 파싱
- 메모리 파일 생성
"""

import json
from pathlib import Path
from datetime import datetime

class MemoryExtractor:
    def __init__(self):
        self.claude_dir = Path.home() / ".claude"
        self.memory_dir = self.claude_dir / "memory"
        self.extracted_file = self.memory_dir / ".extracted_sessions.json"

    def scan_sessions(self):
        """sessions-index.json에서 처리 대상 세션 식별"""

    def parse_session(self, session_id):
        """세션 .jsonl 파싱하여 핵심 정보 추출"""

    def generate_memory(self, session_data):
        """메모리 파일 생성"""

    def run(self):
        """메인 실행 흐름"""
```

### Cowork Shortcut 설정

```yaml
name: memory-extract
description: Claude Code 세션에서 메모리 자동 추출
schedule: daily  # 또는 manual
command: python3 ~/.claude/scripts/memory_extractor.py
```

---

## 6. 메모리 추출 기준

### 추출 대상 (저장 O)

| 기준 | 설명 |
|------|------|
| messageCount ≥ 5 | 의미 있는 대화 |
| summary ≠ 에러 메시지 | 정상 완료된 세션 |
| 도구 사용 있음 | 실제 작업 수행 |
| 파일 생성/수정 | 결과물 있음 |

### 제외 대상 (저장 X)

| 기준 | 설명 |
|------|------|
| messageCount < 5 | 단순 대화 |
| summary = "API Error" | 에러 세션 |
| 도구 사용 없음 | 단순 Q&A |
| /exit, /init만 | 세션 관리 명령 |

---

## 7. 예상 효과

### Before (지침 기반)

```
저장률: ~40% (Claude 재량에 의존)
누락: 중요한 작업도 저장 안 될 수 있음
일관성: 낮음 (세션마다 다름)
```

### After (Session Memory Extractor)

```
저장률: 100% (자동 추출)
누락: 없음 (모든 의미 있는 세션 처리)
일관성: 높음 (동일한 로직으로 처리)
```

---

## 8. 다음 단계

### 즉시 실행 가능

1. **Python 스크립트 작성** - 세션 파싱 및 메모리 생성
2. **테스트** - 기존 세션 데이터로 검증
3. **Cowork Shortcut 생성** - 정기 실행 설정

### 추후 확장

1. **증분 업데이트** - 같은 주제 세션 통합
2. **키워드 자동 추출** - AI 기반 요약
3. **관련 메모리 연결** - 자동 [[링크]] 생성

---

## 9. 결론

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  "내부에서 자기 자신을 개선하는 한계"                         │
│                    ↓                                        │
│  "외부(Cowork)에서 내부(Claude Code) 데이터를 분석"          │
│                                                             │
│  이것이 바로 앤이 말한 "코워크니까 건드릴 수 있는 것"          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Stop Hook이 실패한 이유**: Claude Code가 자기 응답 완료 후 자기에게 명령할 수 없음
**새로운 접근이 성공하는 이유**: Cowork가 외부에서 데이터를 읽고 처리함

---

*제안: Cowork Session Memory Extractor | 2026-02-04*
