# 008. MCP Prompt Analyzer Server

> 4-Layer 프롬프트 분석을 자동화하는 MCP 서버

---

## 개요

CLAUDE.md에 명시된 4-Layer 분석이 실제로 적용되지 않는 문제를 해결하기 위해 구현된 MCP (Model Context Protocol) 서버입니다.

### 문제 배경

| 문제 | 설명 |
|------|------|
| 강제성 없음 | 문서의 지침은 "권장사항"일 뿐 강제 실행 불가 |
| 키워드 한계 | 모든 표현을 트리거로 등록 불가 |
| 화용적 분석 미적용 | "한국어 버전" = 번역 의도인데 감지 안 됨 |

### 해결책

Python MCP 서버로 `analyze_prompt` 도구를 제공하여 Claude가 자동으로 프롬프트를 분석할 수 있게 함.

---

## 설치 구성

### 파일 구조

```
~/.claude/
├── mcp-env/                          # Python 3.12 가상환경
│   ├── bin/
│   │   ├── python3.12               # Python 인터프리터
│   │   └── pip                      # 패키지 관리자
│   └── lib/python3.12/site-packages/
│       └── mcp/                     # MCP 패키지
├── scripts/
│   ├── prompt_analyzer.py           # CLI 분석기
│   └── prompt_analyzer_mcp.py       # MCP 서버 (메인)
└── commands/
    └── analyze.md                   # /analyze 슬래시 커맨드
```

### 설치 명령어

```bash
# 1. Python 3.12 설치 (mcp 요구사항: Python 3.10+)
brew install python@3.12

# 2. 가상환경 생성
/opt/homebrew/bin/python3.12 -m venv ~/.claude/mcp-env

# 3. mcp 패키지 설치
~/.claude/mcp-env/bin/pip install mcp

# 4. MCP 서버 등록
claude mcp add prompt-analyzer ~/.claude/mcp-env/bin/python3.12 -- ~/.claude/scripts/prompt_analyzer_mcp.py
```

### 등록 확인

```bash
claude mcp list
# 출력: prompt-analyzer: ✓ Connected
```

---

## 분석기 기능

### 4-Layer 분석

| Layer | 분석 내용 | 추출 정보 |
|-------|----------|----------|
| **Lexical** | 키워드 매칭 | 스킬, 에이전트, 체인 후보 |
| **Syntactic** | 문장 구조 | 요청 유형 (생성/분석/수정) |
| **Discourse** | 컨텍스트 | 체인 복잡도 |
| **Pragmatic** | 실제 의도 | 암묵적 번역/변환 감지 |

### 키워드 매핑 데이터베이스

#### Skills (18개)

| 스킬 | 감지 키워드 |
|------|------------|
| `/translation-specialist` | 번역, translation, 다국어, ~버전, ~로 만들어 |
| `/docx` | word, docx, 문서, document |
| `/pdf` | pdf, 추출, extract |
| `/pptx` | powerpoint, pptx, 프레젠테이션, 슬라이드 |
| `/xlsx` | excel, xlsx, 스프레드시트 |
| `/frontend-design` | 프론트엔드, frontend, ui, 인터페이스 |
| `/canvas-design` | 시각 디자인, 캔버스, 포스터 |
| `/mcp-builder` | mcp, 서버, 프로토콜 |
| 기타 | ... |

#### Agents (17개)

| 에이전트 | 감지 키워드 |
|---------|------------|
| `multidimensional_analyst` | 분석, analysis, 다차원, 시스템 사고 |
| `system_architect` | 설계, design, 아키텍처, clean, solid |
| `code_developer` | 개발, develop, 코드, tdd, 구현 |
| `quality_reviewer` | 리뷰, review, 코드 검토, 품질 |
| 기타 | ... |

#### Chains (9개)

| 체인 | 감지 키워드 |
|------|------------|
| `DevChain` | 코드 개발, api 설계, 시스템 구현 |
| `ThinkChain` | 복잡한 분석, 다차원적 관점, 창의적 솔루션 |
| `FastTrack` | 버그 수정, 긴급 문제, 빠른 수정 |
| `DocChain` | 문서 생성, 문서 편집, 변환 |
| 기타 | ... |

### 화용적 분석 패턴

```python
INTENT_PATTERNS = {
    "translation": [
        r"(.+)로\s*(만들어|변환|바꿔)",   # "한국어로 만들어"
        r"(.+)\s*버전",                   # "한국어 버전"
        r"영어.+한국어|한국어.+영어",      # 언어 변환
        r"번역", r"translate",
    ],
    "creation": [r"만들어|생성|작성", r"create|generate|write"],
    "analysis": [r"분석|검토|리뷰", r"analyze|review|examine"],
    "modification": [r"수정|변경|업데이트", r"modify|change|update|edit"],
}
```

---

## 사용법

### 1. MCP 도구 자동 호출

Claude가 필요시 `analyze_prompt` 도구를 직접 호출:

```
analyze_prompt("영어를 만들고 한국어 버전을 만들어줘")
```

### 2. 슬래시 커맨드

```
/analyze 영어를 만들고 한국어 버전을 만들어줘
```

### 3. CLI 직접 실행

```bash
python3 ~/.claude/scripts/prompt_analyzer.py "프롬프트"
```

---

## 테스트 결과

### 테스트 케이스

| 테스트 | 입력 | 결과 |
|--------|------|------|
| 번역 의도 | "영어를 만들고 한국어 버전을 만들어줘" | ✅ `/translation-specialist`, Priority: HIGH |
| 문서 생성 | "Word 문서로 보고서 작성해줘" | ✅ `/docx`, `/internal-comms` |
| 개발 작업 | "API 설계하고 TDD로 개발해줘" | ✅ `system_architect`, `code_developer`, DevChain |
| 분석 작업 | "시스템을 다차원적으로 분석해줘" | ✅ `multidimensional_analyst` |
| 디자인 | "UI 프론트엔드 디자인해줘" | ✅ `/frontend-design`, WebDevChain |

### 출력 예시

```json
{
  "recommended_skills": ["/translation-specialist"],
  "recommended_agents": [],
  "recommended_chain": null,
  "priority": "HIGH",
  "reasoning": [
    "🔴 HIGH PRIORITY: 번역 의도 감지 (영어 → 한국어)"
  ]
}
```

---

## 설정 파일

### ~/.claude.json (MCP 서버 등록)

```json
{
  "mcpServers": {
    "prompt-analyzer": {
      "type": "stdio",
      "command": "/Users/changjaeyou/.claude/mcp-env/bin/python3.12",
      "args": [
        "/Users/changjaeyou/.claude/scripts/prompt_analyzer_mcp.py"
      ]
    }
  }
}
```

---

## 관련 문서

- [[007_Claude-Code-Settings-Configuration]] - Claude Code 설정 가이드
- [[004_Dynamic-Chain-Orchestration-System]] - 동적 체인 오케스트레이션
- [[CLAUDE.md]] - 통합 가이드라인

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-01 | 1.0 | 초기 구현 및 문서화 |
