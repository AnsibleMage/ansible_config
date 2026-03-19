# 013. Prompt Analyzer 4-Layer Complete Implementation

> prompt_analyzer.py V2.1 - 완전한 4-Layer 언어학적 분석 시스템

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| **버전** | V2.1 |
| **위치** | `~/.claude/scripts/prompt_analyzer.py` |
| **구현일** | 2026-02-04 |
| **기반** | translation-specialist 4-Layer 구조 |

---

## 1. 4-Layer 분석 구조

### 개요

```
사용자 프롬프트 입력
        ↓
┌───────────────────────────────────────┐
│ Layer 1: Lexical (어휘 분석)           │
│   - 키워드 매칭                        │
│   - 스킬/에이전트/체인 후보 추출        │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ Layer 2: Syntactic (통사 분석)         │
│   - 문장 구조 분석                     │
│   - 요청 유형 판별 (질문/명령/요청)     │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ Layer 3: Discourse (담화 분석) 🆕      │
│   - 복잡도 판단 (high/medium/low)      │
│   - 컨텍스트 참조 감지                 │
│   - 작업 범위 추정                     │
└───────────────────────────────────────┘
        ↓
┌───────────────────────────────────────┐
│ Layer 4: Pragmatic (화용 분석)         │
│   - 실제 의도 파악                     │
│   - 언어 변환 감지                     │
│   - 긴급도 판단                        │
└───────────────────────────────────────┘
        ↓
추천 생성 (스킬/에이전트/체인 + 우선순위)
```

### Layer별 상세

| Layer | 분석 항목 | 출력 |
|-------|----------|------|
| **Lexical** | 키워드, 도메인 용어 | `skills[]`, `agents[]`, `chains[]` |
| **Syntactic** | 문장 구조, 마커 | `type`, `word_count`, `has_code_block` |
| **Discourse** | 컨텍스트, 복잡도 | `complexity`, `scope`, `is_multi_step` |
| **Pragmatic** | 의도, 긴급도 | `intents[]`, `urgency`, `language_conversion` |

---

## 2. Layer 3: Discourse 분석 (신규 구현)

### 복잡도 지표

| 수준 | 키워드 |
|------|--------|
| **high** | "복잡", "complex", "아키텍처", "시스템", "전체", "다단계" |
| **medium** | "몇 가지", "several", "여러", "기능", "모듈" |
| **low** | "간단", "simple", "하나", "빠르게", "briefly" |

### 컨텍스트 참조 패턴

| 패턴 | 유형 | 예시 |
|------|------|------|
| `이전\|앞서\|위에서\|아까` | `previous_mention` | "이전에 작업하던 프로젝트" |
| `계속\|이어서\|추가로` | `continuation` | "계속 진행해줘" |
| `그것\|그거\|저것\|이것` | `pronoun_reference` | "그거 수정해줘" |
| `위 내용\|해당\|그\|저` | `demonstrative` | "그 파일 열어줘" |

### 작업 범위

| 범위 | 감지 키워드 |
|------|------------|
| **project** | "전체", "entire", "모든", "all", "프로젝트" |
| **multiple** | "여러", "multiple", "몇", "several" |
| **single** | (기본값) |

### 다단계 작업 감지

```python
multi_step_indicators = [
    "그리고", "다음", "그 후", "먼저",
    "and then", "after that", "first", "then"
]
```

---

## 3. V2.1 버그 수정

### 긴급도 감지 확장

**이전 (V2.0)**:
```python
["급해", "urgent", "빨리", "quickly", "asap", "지금 바로"]
```

**이후 (V2.1)**:
```python
[
    "급해", "급한", "급하게", "급히", "urgent", "urgently",
    "빨리", "quickly", "asap", "지금 바로", "당장", "즉시",
    "immediately", "right now", "긴급", "emergency"
]
```

### 번역 오탐지 수정

**문제**: "API 문서를 PDF로 만들어줘"가 번역 의도로 잘못 감지됨

**원인**: `(.+)로\s*(만들어|변환|바꿔)` 패턴이 "PDF로 만들어"를 매칭

**해결**: 언어 키워드가 있을 때만 번역 감지

```python
# 이전
r"(.+)로\s*(만들어|변환|바꿔)"

# 이후
r"(영어|한국어|일본어|중국어|english|korean|japanese|chinese)로\s*(만들어|변환|바꿔)"
```

---

## 4. 체인 패턴 (11개)

### 기존 체인 (A~I)

| ID | 체인 | 키워드 |
|----|------|--------|
| A | DevChain | "개발", "새 기능", "feature" |
| B | ThinkChain | "심층 분석", "다차원", "사고" |
| C | FastTrack | "긴급", "버그 수정", "급한" |
| D | LearnChain | "학습", "배우", "이해" |
| E | DecisionChain | "결정", "선택", "판단" |
| F | DocChain | "문서", "document", "작성" |
| G | DesignChain | "디자인", "UI", "시각" |
| H | WebDevChain | "웹", "프론트엔드", "React" |
| I | CollabChain | "협업", "공동 작성", "coauthoring" |

### 신규 체인 (J~K)

| ID | 체인 | 키워드 |
|----|------|--------|
| **J** | RailsDevChain | "rails", "레일즈", "ruby on rails", "kamal", "바이브코딩" |
| **K** | ResearchChain | "조사", "research", "연구", "트렌드", "비교 분석" |

---

## 5. 테스트 결과

### 테스트 케이스

| # | 프롬프트 | 기대 결과 | 실제 결과 | 상태 |
|---|----------|----------|----------|------|
| 1 | "이 문서를 영어로 번역해줘" | `/translation-specialist` HIGH | ✓ | ✅ |
| 2 | "Rails 8로 블로그 앱 만들어줘" | `RailsDevChain` | ✓ | ✅ |
| 3 | "다차원적으로 분석해줘" | `multidimensional_analyst` | ✓ | ✅ |
| 4 | "안녕" | (매칭 없음) | ✓ | ✅ |
| 5 | "급한 작업이야" | urgency: high | ✓ | ✅ |
| 6 | "API 문서를 PDF로 만들어줘" | `/pdf` (번역 X) | ✓ | ✅ |
| 7 | "최신 React 트렌드 조사" | `ResearchChain` | ✓ | ✅ |
| 8 | "이 문서를 영어로 만들어줘" | `/translation-specialist` | ✓ | ✅ |

### 테스트 명령어

```bash
cd ~/.claude/scripts
python3 prompt_analyzer.py "테스트할 프롬프트"
```

---

## 6. 출력 형식

### 예시 출력

```
============================================================
🔍 4-LAYER PROMPT ANALYSIS
============================================================

📝 [1] 어휘적 분석 (Lexical)
   에이전트 감지: system_architect, code_developer

📐 [2] 통사적 분석 (Syntactic)
   요청 유형: command
   단어 수: 11

💬 [3] 담화 분석 (Discourse)
   복잡도: high
   작업 범위: project
   📎 컨텍스트 참조: previous_mention

🎯 [4] 화용적 분석 (Pragmatic)
   긴급도: high

============================================================
💡 RECOMMENDATION
============================================================
   📌 권장 에이전트: system_architect, code_developer

   우선순위: HIGH

   근거:
   - ⚡ 긴급 요청 감지
   - 📊 복잡도: high, 범위: project
   - 키워드 '설계' → system_architect
   - 키워드 '개발' → code_developer
============================================================
```

---

## 7. Hook 연동

### UserPromptSubmit Hook

```bash
# ~/.claude/hooks/auto-analyze.sh
#!/bin/bash
PROMPT="$1"

# 10자 미만 또는 슬래시 명령어는 생략
if [ ${#PROMPT} -lt 10 ] || [[ "$PROMPT" == /* ]]; then
    exit 0
fi

# 4-Layer 분석 실행
RESULT=$(python3 ~/.claude/scripts/prompt_analyzer.py "$PROMPT" 2>/dev/null)

# additionalContext로 주입
echo "{\"additionalContext\": \"$RESULT\"}"
```

### 생략 조건

| 조건 | 이유 |
|------|------|
| 10자 미만 | 단순 인사, 확인 등 |
| `/command` 형식 | 슬래시 명령어는 이미 명시적 |

---

## 관련 문서

- [[011_Stop-Hook-Auto-Memory-Save-System]] - Hook 시스템 아키텍처
- [[012_Skills-vs-Subagent-Structural-Analysis]] - Skills vs Subagent 비교
- [[CLAUDE.md]] - 통합 가이드라인 V3.6
- [[009_UserPromptSubmit-Hook-Auto-Analysis]] - UserPromptSubmit Hook 상세

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-03 | 2.0 | 4-Layer 구조 구현 (Discourse 추가) |
| 2026-02-04 | 2.1 | 긴급도 키워드 확장, 번역 오탐지 수정 |

---

*Prompt Analyzer 4-Layer Complete Implementation - V2.1 (2026-02-04)*
