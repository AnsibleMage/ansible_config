# Chain Usage Report System

> **작성일**: 2026-02-04
> **목적**: Claude Code 세션 로그 분석 → 체인/에이전트/스킬 사용 패턴 일일 리포트 자동 생성
> **구현자**: Cowork (외부 관찰자)

---

## 1. 시스템 개요

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Chain Usage Report System                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [데이터 소스]                                                        │
│  ~/.claude/projects/{project}/                                       │
│  ├── sessions-index.json     # 세션 메타데이터                        │
│  └── {sessionId}.jsonl       # 대화 로그                             │
│       │                                                              │
│       ↓                                                              │
│  ┌──────────────────────────────────────────┐                       │
│  │  chain_report_generator.py               │                       │
│  │                                          │                       │
│  │  1. 대상 날짜의 세션 필터링               │                       │
│  │  2. jsonl 파싱 → 메시지 추출             │                       │
│  │  3. 패턴 매칭으로 사용 데이터 추출        │                       │
│  │     • 체인: "📋 체인 구성:" 패턴          │                       │
│  │     • 에이전트: Task(subagent_type:...)  │                       │
│  │     • 스킬: /skill-name, Skill 도구      │                       │
│  │  4. 통계 집계                            │                       │
│  │  5. 마크다운 리포트 생성                  │                       │
│  └──────────────────────────────────────────┘                       │
│       │                                                              │
│       ↓                                                              │
│  [출력]                                                              │
│  ~/.claude/chainreport/YYMM_SEQ_daily_chain_report.md               │
│                                                                      │
│  예: 2602_001_daily_chain_report.md                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 파일 구조

```
~/.claude/
├── scripts/
│   └── chain_report_generator.py    # 리포트 생성 스크립트
│
└── chainreport/                      # 리포트 저장 폴더
    ├── 2602_001_daily_chain_report.md
    ├── 2602_002_daily_chain_report.md
    └── ...
```

---

## 3. 추출 대상 및 패턴

### 3.1 Chain 사용

| 패턴 | 예시 |
|------|------|
| `📋 체인 구성: {ChainName}` | 📋 체인 구성: DevChain |
| `Chain: {ChainName}` | Chain: ResearchChain |
| `{Name}Chain 실행` | SystemDesignChain 실행 |

**알려진 체인 목록**:
- SystemDesignChain, AutomationChain, GameDevChain
- DevChain, ResearchChain, DocChain+, WebDevChain+
- MetaThinkChain, RailsDevChain, HotfixChain, Direct

### 3.2 Agent 사용

```json
{
  "type": "tool_use",
  "name": "Task",
  "input": {
    "subagent_type": "system_architect",
    "model": "opus",
    "prompt": "..."
  }
}
```

**알려진 에이전트**:

| Agent | Model |
|-------|-------|
| multidimensional_analyst | opus |
| system_architect | opus |
| requirements_analyst | opus |
| integrated_sage | opus |
| code_developer | sonnet |
| quality_reviewer | sonnet |
| Explore | sonnet |
| Plan | opus |

### 3.3 Skill 사용

1. **사용자 직접 호출**: `/memory-save`, `/analyze`, `/docx` 등
2. **Skill 도구 호출**: `{"name": "Skill", "input": {"skill": "docx"}}`

---

## 4. 리포트 구조

```markdown
# 일일 Chain 사용 리포트

## 메타 정보
- **작성일**: YYYY-MM-DD
- **분석 기간**: YYYY-MM-DD (1일)
- **총 세션 수**: N개
- **요약**:
  - 가장 많이 사용한 체인: **{Name}** (N회)
  - 가장 많이 사용한 에이전트: **{Name}** (N회)
  - 가장 많이 사용한 스킬: **{Name}** (N회)

---

## Chain 사용 통계
| 순위 | Chain | 사용 횟수 | 비율 |

## Agent 사용 통계
| 순위 | Agent | Model | 사용 횟수 |
### 모델별 분포
- Opus: N회 (X%)
- Sonnet: N회 (Y%)

## Skill 사용 통계
| 순위 | Skill | 사용 횟수 |

## 세션 목록
| # | 세션 ID | 요약 | 메시지 수 |

## 시사점
- 자동 생성 인사이트
```

---

## 5. 사용법

### 기본 실행 (오늘 날짜)

```bash
python ~/.claude/scripts/chain_report_generator.py
```

### 특정 날짜 실행

```bash
python ~/.claude/scripts/chain_report_generator.py --date 2026-02-03
```

### Cowork에서 실행

```python
# Cowork 환경에서는 경로 변환 필요
CLAUDE_DIR = Path("/sessions/.../mnt/changjaeyou/.claude")
```

---

## 6. 첫 리포트 결과 (2026-02-03)

```
📊 Chain Usage Report Generator
분석 대상 날짜: 2026-02-03
--------------------------------------------------
발견된 세션: 5개
체인 사용: 2회
에이전트 사용: 9회
스킬 사용: 29회
--------------------------------------------------
```

| 항목 | Top 1 | 횟수 |
|------|-------|------|
| Chain | DocChain | 2회 |
| Agent | Explore | 6회 |
| Skill | /memory-save | 6회 |

**모델 분포**: Opus 22.2% / Sonnet 66.7%

---

## 7. 자동 인사이트 생성 로직

```python
insights = []

# 체인 사용 패턴
if not chain_usage:
    insights.append("체인 선언 패턴이 사용되지 않음 → Direct 모드")
elif top_chain == "Direct":
    insights.append("Direct 사용이 많음 → 체인 패턴 적용 권장")

# 모델 균형
if opus_count > sonnet_count * 2:
    insights.append("Opus 과다 사용 → Sonnet으로 비용 절감 가능")
elif sonnet_count > opus_count * 3:
    insights.append("Sonnet 과다 사용 → 복잡한 작업에 Opus 권장")

# 미사용 체인
unused = KNOWN_CHAINS - used_chains
if unused:
    insights.append(f"미사용 체인: {unused}")
```

---

## 8. 향후 확장 계획

| 기능 | 우선순위 | 설명 |
|------|----------|------|
| LaunchAgent 연동 | HIGH | 매일 23:00 자동 실행 |
| 주간/월간 리포트 | MEDIUM | `--period week` 옵션 |
| 트렌드 차트 | MEDIUM | 시간별 사용 변화 시각화 |
| CLAUDE.md 자동 개선 | LOW | 미사용 체인 제거 제안 |

---

## 9. 관련 문서

- [[Cowork_External_Observer_System]] - 외부 관찰자 시스템 아키텍처
- [[Auto_Memory_Save_Hook_V2_Implementation]] - Hook 시스템 구현
- [[Chain_System_V2.0_for_CLAUDE]] - Chain V2.0 업그레이드

---

## 10. 핵심 코드 (chain_report_generator.py)

**위치**: `~/.claude/scripts/chain_report_generator.py`

**주요 함수**:

| 함수 | 역할 |
|------|------|
| `get_sessions_for_date()` | 특정 날짜 세션 필터링 |
| `parse_jsonl_file()` | JSONL 파일 파싱 |
| `extract_chain_usage()` | 체인 사용 추출 |
| `extract_agent_usage()` | 에이전트 사용 추출 |
| `extract_skill_usage()` | 스킬 사용 추출 |
| `generate_report()` | 마크다운 리포트 생성 |
| `get_next_sequence_number()` | 파일명 시퀀스 계산 |

---

*이 시스템은 Cowork의 "외부 관찰자" 역할을 활용하여 Claude Code 세션을 분석합니다.*
