# User Prompt Chain Hook System

> Claude Code 4-Layer 프롬프트 자동 분석 및 체인 오케스트레이션 시스템

---

## 개요

이 시스템은 사용자의 모든 프롬프트를 자동으로 4-Layer 언어학적 분석하여 최적의 에이전트, 스킬, 체인을 추천합니다.

```
사용자 프롬프트 입력
        ↓
┌───────────────────────────────────────┐
│ UserPromptSubmit Hook (자동 실행)      │
│   ~/.claude/hooks/auto-analyze.sh     │
│   → prompt_analyzer.py 호출           │
│   → 4-Layer 분석 수행                 │
│   → additionalContext로 결과 주입     │
└───────────────────────────────────────┘
        ↓
Claude가 분석 결과를 컨텍스트로 수신
        ↓
최적 체인 선택 및 실행
```

---

## 4-Layer 분석

| Layer | Analysis | 분석 내용 |
|-------|----------|----------|
| **Lexical** | 어휘 분석 | 키워드, 도메인 용어 → Agent/Skill 후보 |
| **Syntactic** | 통사 분석 | 문장 구조, 명령/질문/요청 유형 → 태스크 유형 |
| **Discourse** | 담화 분석 | 컨텍스트, 이전 대화 참조 → 체인 복잡도 |
| **Pragmatic** | 화용 분석 | 실제 의도, 기대 결과 → 암묵적 번역/변환 감지 |

---

## 자동 감지 패턴

| 패턴 | 감지 예시 | 자동 추천 |
|------|----------|----------|
| **번역 의도** | "영어 버전", "한국어로 만들어" | `/translation-specialist` (HIGH) |
| **문서 생성** | "Word", "pdf", "pptx", "보고서" | `/docx`, `/pdf`, `/pptx` |
| **개발 작업** | "설계", "개발", "TDD", "API" | `system_architect`, `code_developer` |
| **분석 작업** | "분석", "다차원", "시스템 사고" | `multidimensional_analyst` |
| **디자인** | "UI", "프론트엔드", "포스터" | `/frontend-design`, `/canvas-design` |
| **Rails 개발** | "rails", "레일즈", "kamal" | `RailsDevChain` |
| **연구/조사** | "조사", "research", "트렌드" | `ResearchChain` |

---

## 지원 체인 (11개)

| 체인 | 용도 | 구성 |
|------|------|------|
| **DevChain** | 코드 개발 | requirements → architect → developer → reviewer |
| **ThinkChain** | 심층 사고 | explorer → analyst → sage |
| **FastTrack** | 긴급 수정 | resolver → developer → reviewer |
| **LearnChain** | 학습 | evolver → analyst → amplifier |
| **DecisionChain** | 의사결정 | reframer → analyst + judge → sage |
| **DocChain** | 문서 생성 | 유형 식별 → /docx, /pdf, /pptx |
| **DesignChain** | 디자인 | brand → canvas + theme |
| **WebDevChain** | 웹 개발 | requirements → architect → frontend → testing |
| **CollabChain** | 협업 문서 | doc-coauthoring → export |
| **RailsDevChain** | Rails 8 | PRD → plan → dev → test → deploy → verify |
| **ResearchChain** | 연구/조사 | WebSearch → analyst → write |

---

## 파일 구조

```
User Prompt Chain Hook System/
├── README.md                 # 이 문서
├── INSTALL.md               # 상세 설치 가이드
├── install.sh               # 자동 설치 스크립트
├── hooks/
│   └── auto-analyze.sh      # UserPromptSubmit Hook
├── scripts/
│   ├── prompt_analyzer.py   # 4-Layer 분석기 (CLI)
│   └── prompt_analyzer_mcp.py # MCP 서버 버전
├── templates/
│   └── settings.json.template # Claude Code 설정 템플릿
└── examples/
    └── analysis-example.md  # 분석 결과 예시
```

---

## 빠른 설치

```bash
# 1. 이 폴더로 이동
cd "User Prompt Chain Hook System"

# 2. 설치 스크립트 실행
chmod +x install.sh
./install.sh

# 3. Claude Code 재시작
```

---

## 수동 설치

자세한 수동 설치 방법은 [INSTALL.md](./INSTALL.md)를 참조하세요.

---

## 사용 예시

### 입력
```
투두리스트 앱을 React와 TypeScript로 개발해줘.
Zustand로 상태 관리하고 Tailwind CSS 쓸 거야.
```

### 자동 분석 결과
```
============================================================
🔍 4-LAYER PROMPT ANALYSIS
============================================================

📝 [1] 어휘적 분석 (Lexical)
   스킬 감지: /web-artifacts-builder, /frontend-design
   에이전트 감지: code_developer, system_architect

📐 [2] 통사적 분석 (Syntactic)
   요청 유형: command
   단어 수: 15

💬 [3] 담화 분석 (Discourse)
   복잡도: medium
   작업 범위: project

🎯 [4] 화용적 분석 (Pragmatic)
   감지된 의도: creation
   긴급도: normal

============================================================
💡 RECOMMENDATION
============================================================
   📌 권장 스킬: /web-artifacts-builder, /frontend-design
   📌 권장 에이전트: system_architect, code_developer
   📌 권장 체인: DevChain

   우선순위: MEDIUM
============================================================
```

### Claude 응답
```
📋 체인 구성: DevChain
   → system_architect[O] → code_developer[S] → quality_reviewer[S]

투두리스트 앱 설계를 시작합니다...
```

---

## 요구 사항

- **macOS** (또는 bash 지원 Linux)
- **Python 3.8+**
- **Claude Code CLI** (최신 버전)
- **jq** (JSON 파싱용)

---

## 문제 해결

### Hook이 동작하지 않을 때

1. settings.json 경로 확인: `~/.claude/settings.json`
2. Hook 스크립트 실행 권한: `chmod +x ~/.claude/hooks/auto-analyze.sh`
3. Python 경로 확인: `which python3`

### 분석 결과가 나오지 않을 때

수동으로 분석기 테스트:
```bash
echo "테스트 프롬프트" | python3 ~/.claude/scripts/prompt_analyzer.py
```

---

## 버전 정보

- **Version**: 2.1
- **Updated**: 2026-02-04
- **Based on**: translation-specialist 4-Layer 언어학적 분석

---

## 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

*Made with 🎵 by Ari & An*
