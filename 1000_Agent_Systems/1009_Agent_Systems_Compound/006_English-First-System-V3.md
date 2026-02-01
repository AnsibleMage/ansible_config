# CLAUDE.md V3.0: English-First System

## 개요

Claude Code의 영어 처리 최적화를 활용하여 시스템 프롬프트를 영어 우선으로 전환하면서, 한국어 사용자 경험을 유지하는 이중언어 트리거 시스템.

## 핵심 변경사항

### 1. 시스템 프롬프트 영어화

| 구분 | V2.x (이전) | V3.0 (현재) |
|------|-------------|-------------|
| 섹션 헤더 | 한국어/영어 혼용 | 영어 |
| 설명문 | 한국어 | 영어 |
| 에이전트 설명 | 한국어 | 영어 |
| 체인 패턴 정의 | 한국어 | 영어 |

### 2. 이중언어 트리거 키워드

모든 매핑 테이블에 한국어와 영어 키워드 병기:

```markdown
| Keywords (KO/EN) | Agent | Model |
|------------------|-------|-------|
| 요구사항/requirements, 분석/analysis | requirements_analyst | opus |
| 아키텍처/architecture, 설계/design | system_architect | opus |
| 코드/code, 개발/develop, TDD | code_developer | sonnet |
```

### 3. 언어 원칙 유지

```markdown
### Language Principles
- **Output/Reports**: Korean (한국어)
- **Code/Technical terms**: English acceptable
- **File/Variable names**: Keep original
```

## 이중언어 트리거 전체 목록

### Cognitive Agents (인지 에이전트)

| 한국어 | English | Agent | Model |
|--------|---------|-------|-------|
| 통찰, 패턴, 창의 | insight, pattern, creative | insight_explorer | sonnet |
| 다차원, 시스템 분석 | multidimensional, system analysis | multidimensional_analyst | opus |
| 연결, 관계, 메타포 | connection, relation, metaphor | connection_creator | sonnet |
| 재정의, 관점 전환 | reframe, perspective shift | problem_reframer | opus |
| 혁신, 아이디어 | innovation, ideation | solution_innovator | sonnet |
| 심화, 확장, Why | deepen, amplify, Why | insight_amplifier | sonnet |
| 학습, 지식 격차 | learning, knowledge gap | learning_evolver | sonnet |
| 복잡성, 분해 | complexity, decompose | complexity_resolver | opus |
| 판단, 균형, 평가 | judgment, balance, evaluate | balanced_judge | opus |
| 통합, 윤리, 지혜 | integrate, ethics, wisdom | integrated_sage | opus |

### Role Agents (역할 에이전트)

| 한국어 | English | Agent | Model |
|--------|---------|-------|-------|
| 요구사항, 분석, 비즈니스 | requirements, analysis, business | requirements_analyst | opus |
| 아키텍처, 설계, SOLID | architecture, design, SOLID | system_architect | opus |
| 코드, 개발, TDD | code, develop, TDD | code_developer | sonnet |
| 리뷰, 품질, 테스트 | review, quality, test | quality_reviewer | sonnet |

### Chain Patterns (체인 패턴)

| 한국어 | English | Chain |
|--------|---------|-------|
| 개발, 기능, 구현 | dev, feature, implement | DevChain |
| 사고, 분석, 이해 | think, analyze, understand | ThinkChain |
| 빠른, 간단, 수정 | quick, simple, fix | FastTrack |
| 학습, 연구, 탐구 | learn, research, study | LearnChain |
| 결정, 선택, 전략 | decide, choose, strategy | DecisionChain |
| 문서, 정리, 기록 | document, organize, record | DocChain |
| 디자인, UI, UX | design, UI, UX | DesignChain |
| 웹, 프론트, 백엔드 | web, front, backend | WebDevChain |
| 협업, 팀, 리뷰 | collaborate, team, review | CollabChain |

## 동작 방식

### 입력 처리 흐름

```
사용자 입력 (한국어 또는 영어)
        ↓
4-Layer Prompt Analysis
        ↓
Bilingual Keyword Matching
(한국어 키워드 OR 영어 키워드)
        ↓
Chain/Agent Selection
        ↓
Execution (English system prompts)
        ↓
Output (한국어)
```

### 예시

**한국어 입력**:
```
"이 시스템의 요구사항을 분석해줘"
→ 키워드 매칭: "요구사항", "분석"
→ Agent: requirements_analyst (opus)
→ 실행 후 한국어로 결과 출력
```

**영어 입력**:
```
"Analyze the requirements for this system"
→ Keyword matching: "requirements", "analyze"
→ Agent: requirements_analyst (opus)
→ Execute and output in Korean
```

## 장점

1. **인식 정확도 향상**: Claude Code가 영어 프롬프트를 더 정확하게 처리
2. **처리 속도 개선**: 해석 오버헤드 감소
3. **사용자 경험 유지**: 한국어 키워드로 동일하게 사용 가능
4. **유연성**: 언어에 관계없이 동일한 기능 트리거
5. **일관성**: 입력 언어와 무관하게 동일한 시스템 동작

## 버전 히스토리

| Version | Date | Changes |
|---------|------|---------|
| V1.0 | - | Original Korean system |
| V2.0 | 2026-02-01 | GEMINI 5.1 integration |
| V2.1 | 2026-02-01 | Model mapping (opus/sonnet) |
| V2.2 | 2026-02-01 | Dynamic Chain Orchestration |
| V2.3 | 2026-02-01 | PARALLEL-FIRST optimization |
| V3.0 | 2026-02-01 | English-first with bilingual triggers |

## 관련 문서

- [[CLAUDE.md]] - 메인 설정 파일
- [[Dynamic-Chain-Orchestration-System]] - 동적 체인 시스템
- [[Parallel-Execution-Optimization]] - 병렬 실행 최적화
- [[Claude-Code-Model-Auto-Switching-Analysis]] - 모델 전환 분석

## Tags

#claude-code #english-first #bilingual #optimization #v3.0
