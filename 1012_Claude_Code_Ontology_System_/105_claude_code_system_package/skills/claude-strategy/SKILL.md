---
name: claude-strategy
description: "프로젝트에 최적화된 Claude Code 사용전략 문서를 자동 생성한다. CLAUDE.md의 체인(Chain), 에이전트(Agent), 스킬(Skill), Agent Teams, Hook을 프로젝트 특성에 매핑하여 개발 효율을 극대화하는 전략을 수립한다. 사용 시점: (1) 새 프로젝트 시작 전 개발 전략 수립, (2) 기존 프로젝트에 Claude Code 활용 계획 추가, (3) '사용전략', '개발전략', 'Claude Code 전략', '클로드코드 전략' 요청 시. /claude-strategy 또는 /strategy로 호출."
---

# Claude Code Usage Strategy Generator

프로젝트 특성을 분석하고, CLAUDE.md의 오케스트레이션 시스템을 매핑하여 최적화된 사용전략 문서를 생성한다.

## Arguments

$ARGUMENTS (프로젝트명, 프로젝트 폴더 경로, 또는 간략 설명)

## Workflow

### Phase 1: Context Gathering (정보 수집)

1. **CLAUDE.md 읽기** — `~/.claude/CLAUDE.md` Section 2 (Orchestration System) 확인
   - 사용 가능한 체인 (A~J)
   - 에이전트 매핑 테이블
   - 스킬/커맨드 목록
   - Agent Teams 규칙
   - Hook 설정

2. **프로젝트 문서 읽기** — 현재 작업 디렉토리의 기존 문서 탐색
   - 기획/요구사항 문서 (PRD, 스펙)
   - 기술 스택 정보
   - 기존 코드 구조 (`src/`, `app/`, `lib/` 등)
   - 테스트 관련 파일

3. **대화 컨텍스트 확인** — 현재 세션에서 논의된 프로젝트 정보 활용

### Phase 2: Project Analysis (프로젝트 분석)

4. **작업 유형 분류** — 프로젝트의 모든 작업을 7가지 유형으로 분류:
   - 초기화 / 핵심 로직 / UI 개발 / 통합 / 테스트 / 디자인 / 배포 / 버그수정

5. **의존성 분석** — 작업 간 순차/병렬 관계를 ASCII 의존성 맵으로 시각화
   - `★ 병렬 가능` 표시로 Teams 적합 구간 식별

6. **최적 도구 매핑** — 각 작업에 체인/에이전트/스킬을 매핑
   - CLAUDE.md Section 2.4 Chain Selection Matrix 기준

### Phase 3: Strategy Document Generation (전략 문서 생성)

7. **strategy-template.md 참조** — `references/strategy-template.md`를 읽어 12섹션 구조 확인

8. **전략 문서 작성** — 프로젝트 폴더에 마크다운으로 생성

   **필수 12개 섹션**:
   1. 프로젝트 특성 → Claude Code 매핑 (작업분류표 + 의존성맵)
   2. 체인 선택 전략 (Phase별 체인 + 트리거 키워드)
   3. 에이전트 활용 전략 (모델별 비용최적화 + 직접실행 판단)
   4. Agent Teams 전략 (병렬구간 + 팀구성 + 주의사항)
   5. 스킬 활용 전략 (Phase별 스킬 + 조합 패턴)
   6. 슬래시 커맨드 전략 (사용 시점 + 빈도)
   7. Hook 활용 전략 (Hook별 효과)
   8. 프롬프트 설계 전략 (템플릿 + 의도적 프롬프트 예시)
   9. 세션 관리 전략 (세션 분할 + 시작/종료 프로토콜)
   10. 개발 순서 로드맵 (Phase별 + 커밋 전략)
   11. 비용/속도 최적화 요약
   12. 프롬프트 작성 전 체크리스트

### Phase 4: Output (출력)

9. **파일 저장** — `{프로젝트폴더}/claude_code_strategy.md` 또는 사용자 지정 경로
10. **요약 보고** — 핵심 전략 3줄 요약 출력

## Key Mapping Rules

### Chain Selection Logic

| 프로젝트 작업 특성 | 체인 | 근거 |
|------------------|------|------|
| TDD 코딩, 함수 구현 | DevChain | requirements→architect→developer |
| UI/프론트엔드 개발 | WebDevChain+ | 디자인 통합 |
| 조사/분석 | ResearchChain | 다차원 분석 |
| 문서 생성 | DocChain+ | Solo/Collab |
| 시스템 설계 | SystemDesignChain | architect+sage |
| 긴급 수정 | HotfixChain | complexity_resolver |
| Rails 8 | RailsDevChain | 바이브코딩 풀사이클 |
| 게임 개발 | GameDevChain | 듀얼 트랙 |
| 심층 사고/의사결정 | MetaThinkChain | 6-agent 파이프라인 |
| Hook/MCP/스크립트 | AutomationChain | 자동화 |

### Teams Suitability

| 조건 | 판단 |
|------|------|
| 독립 병렬 가능 2+ 작업 | **Teams 적합** |
| 순차 의존 작업 | **Chain 유지** |
| 탐색+설계 혼합 | **Hybrid** (Teams→Chain) |
| 긴급/단일 | **Chain** |

### Cost Optimization

- **Opus(O)**: 설계/분석/요구사항 — 정확도 우선
- **Sonnet(S)**: 코딩/리뷰/탐색 — 속도 우선
- Teams 병렬 시 시간 40~50% 절감
- 문서 참조로 프롬프트 토큰 축소

## References

- **전략 템플릿**: [strategy-template.md](references/strategy-template.md) — 12섹션 상세 구조와 placeholder
