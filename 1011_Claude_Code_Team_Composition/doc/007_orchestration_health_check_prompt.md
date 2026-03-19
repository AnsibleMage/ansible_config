# 오케스트레이션 시스템 종합 건강 검진 및 최적화

## 목적
CLAUDE.md V4.1 오케스트레이션 시스템의 모든 구성요소가 정확히 동기화되어 있는지 검증하고, 불일치나 비효율을 발견하면 수정한다.

## ⚠️ 핵심 원칙: "먼저 해치지 말라 (First, Do No Harm)"

1. **검증 우선**: 모든 항목을 먼저 읽고 분석한 후에만 수정한다
2. **백업 필수**: 수정 전 반드시 `.backup` 파일 생성 (예: `prompt_analyzer.py.healthcheck.backup`)
3. **한 번에 하나씩**: 여러 파일을 동시에 수정하지 않는다. 수정 → 검증 → 다음 파일
4. **로그 기록**: 모든 변경 사항을 `~/.claude/memory/`에 메모리로 저장
5. **현재 잘 작동하는 것은 건드리지 않는다**: 불일치가 발견되어도 실제 작동에 문제가 없으면 기록만 하고 수정하지 않는다
6. **되돌릴 수 있게**: 모든 수정은 되돌릴 수 있어야 한다

---

## 검사 대상 파일/폴더 목록

### 핵심 파일 (Core)
| # | 파일 | 역할 |
|---|------|------|
| C1 | `~/.claude/CLAUDE.md` | 마스터 설정, 통합 매핑 테이블, 체인 패턴 |
| C2 | `~/.claude/scripts/prompt_analyzer.py` | 4-Layer 분석 엔진 (Hook용) |
| C3 | `~/.claude/scripts/prompt_analyzer_mcp.py` | 4-Layer 분석 엔진 (MCP용) |
| C4 | `~/.claude/hooks/auto-analyze.sh` | UserPromptSubmit Hook V3.0 |
| C5 | `~/.claude/hooks/auto-memory-save.sh` | 메모리 자동 저장 Hook |
| C6 | `~/.claude/settings.json` | 전체 설정, 허용/차단 명령어, Hook 등록 |
| C7 | `~/.claude/settings.local.json` | 로컬 설정 |

### 에이전트 파일 (Agents)
| # | 파일 | 역할 |
|---|------|------|
| A1 | `~/.claude/agents/101_Insight_Explorer.md` | 패턴 발견, 관찰 |
| A2 | `~/.claude/agents/102_Multidimensional_Analyst.md` | 다차원 분석 |
| A3 | `~/.claude/agents/103_Connection_Creator.md` | 연결, 은유 |
| A4 | `~/.claude/agents/104_Problem_Reframer.md` | 관점 전환 |
| A5 | `~/.claude/agents/105_Solution_Innovator.md` | 혁신적 솔루션 |
| A6 | `~/.claude/agents/106_Insight_Amplifier.md` | 심화, Why/What-If |
| A7 | `~/.claude/agents/107_Learning_Evolver.md` | 학습, 메타인지 |
| A8 | `~/.claude/agents/108_Complexity_Resolver.md` | 복잡성 분해 |
| A9 | `~/.claude/agents/109_Balanced_Judge.md` | 의사결정, 판단 |
| A10 | `~/.claude/agents/110_Integrated_Sage.md` | 통합 지혜 |
| A11 | `~/.claude/agents/111_Requirements_Analyst.md` | 요구사항 분석 |
| A12 | `~/.claude/agents/112_System_Architect.md` | 아키텍처 설계 |
| A13 | `~/.claude/agents/113_Code_Developer.md` | TDD 개발 |
| A14 | `~/.claude/agents/114_Quality_Reviewer.md` | 코드 리뷰 |
| A15-A22 | `~/.claude/agents/doc-indexer.md` 외 7개 유틸리티 | 유틸리티 에이전트 |

### 기타 참조 파일
| # | 파일/폴더 | 역할 |
|---|-----------|------|
| R1 | `~/.claude/RAILS.md` | Rails 8 바이브코딩 설정 |
| R2 | `~/.claude/CHANGELOG.md` | 변경 이력 |
| R3 | `~/.claude/commands/` (13개 파일) | 슬래시 커맨드 정의 |
| R4 | `~/.claude/skills/` (18개 폴더) | 스킬 정의 |
| R5 | `~/.claude/scripts/chain_report_generator.py` | 체인 리포트 생성기 |
| R6 | `~/.claude/memory/` (55+ 파일) | 메모리 저장소 |
| R7 | `~/.claude/statusline.sh` | 상태바 스크립트 |
| R8 | `~/.claude/session-env/` | 세션 환경 설정 |

---

## 검증 체크리스트

### Phase 1: 읽기 전용 감사 (Read-Only Audit)
> 이 단계에서는 아무것도 수정하지 않는다. 불일치만 기록한다.

#### 1A. CLAUDE.md ↔ prompt_analyzer.py 동기화
- [ ] 체인 이름 10개 (A~J) 가 prompt_analyzer.py에 모두 정확히 존재하는가?
  - SystemDesignChain, AutomationChain, GameDevChain, DevChain, ResearchChain, DocChain+, WebDevChain+, MetaThinkChain, RailsDevChain, HotfixChain
- [ ] 각 체인의 트리거 키워드가 CLAUDE.md 설명과 일치하는가?
- [ ] AGENT_CHAIN_FALLBACK 매핑이 CLAUDE.md 통합 매핑 테이블과 일치하는가?
- [ ] MUTUAL_EXCLUSION 규칙이 CLAUDE.md에 기술된 것과 일치하는가?
- [ ] 신뢰도 점수 체계 (0.95 화용 > 0.85 메타 > 0.8 키워드 > 0.5 fallback)가 코드에 반영되어 있는가?
- [ ] 오탐 방지 로직 ("버전"→번역, "문서"→docx 등)이 코드에 존재하는가?
- [ ] 0.6 미만 필터링, 최대 3개 추천 로직이 코드에 존재하는가?

#### 1B. CLAUDE.md ↔ prompt_analyzer_mcp.py 동기화
- [ ] 위 1A의 모든 항목이 MCP 버전에도 동일하게 반영되어 있는가?
- [ ] MCP 버전의 체인 이름이 V4.1 기준으로 업데이트되어 있는가? (구 체인명 잔존 여부)
- [ ] 두 analyzer 간 로직 차이가 있다면 의도된 것인가?

#### 1C. CLAUDE.md 통합 매핑 테이블 ↔ Agent 파일
- [ ] 매핑 테이블의 14개 에이전트가 agents/ 폴더에 모두 존재하는가?
- [ ] 각 에이전트의 `name:` 필드가 매핑 테이블의 subagent_type과 일치하는가?
- [ ] 각 에이전트의 `model:` 필드가 매핑 테이블의 Model (S/O)과 일치하는가?
  - 특히 확인: connection_creator(O), learning_evolver(O), solution_innovator(O), insight_amplifier(O)
- [ ] 제거된 에이전트 (115_Quality_Manager, 116_Context_Manager)가 agents/ 폴더에 없는 것을 확인
- [ ] 제거된 에이전트 참조가 prompt_analyzer.py, prompt_analyzer_mcp.py, CLAUDE.md 어디에도 남아있지 않은가?

#### 1D. CLAUDE.md ↔ settings.json
- [ ] UserPromptSubmit Hook 등록이 auto-analyze.sh를 가리키는가?
- [ ] PostToolUse, PreToolUse Hook이 settings.json에 정확히 등록되어 있는가?
- [ ] MCP 설정에 prompt-analyzer가 등록되어 있는가?
- [ ] Agent Teams 환경변수 (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)가 설정되어 있는가?
- [ ] defaultMode: "plan"이 설정되어 있는가?
- [ ] statusLine 설정이 statusline.sh를 가리키는가?
- [ ] 허용 명령어 52개가 실제로 52개인가?
- [ ] 차단 명령어 12개가 실제로 12개인가?
- [ ] slash commands 6개 (/commit-push, /pr-review, /project-review, /memory-save, /readme-gen, /analyze)가 settings와 commands/ 폴더 양쪽에 존재하는가?

#### 1E. Hook 파이프라인 검증
- [ ] auto-analyze.sh가 prompt_analyzer.py를 올바른 경로로 호출하는가?
- [ ] auto-analyze.sh V3.0의 teammate 감지 로직이 존재하는가?
- [ ] auto-analyze.sh의 생략 조건 (10자 미만, /command, teammate)이 구현되어 있는가?
- [ ] auto-memory-save.sh가 올바르게 작동하는 경로를 참조하는가?
- [ ] SESSION_ID별 상태 파일 분리가 구현되어 있는가?

#### 1F. 체인 패턴 ↔ 에이전트 가용성
- [ ] 각 체인(A~J)에서 참조하는 모든 에이전트가 실제로 agents/ 폴더에 존재하는가?
- [ ] 각 체인에서 참조하는 모든 스킬이 skills/ 폴더에 존재하는가?
- [ ] 각 체인에서 참조하는 탐색 도구 (Explore, Plan, general-purpose)가 유효한 subagent_type인가?

#### 1G. Skills ↔ CLAUDE.md
- [ ] CLAUDE.md에 나열된 스킬 16개+가 skills/ 폴더에 모두 존재하는가?
- [ ] 각 스킬의 트리거 키워드가 prompt_analyzer.py에 반영되어 있는가?
- [ ] rails 관련 커맨드 7개 (/rails-prd, /rails-plan, /rails-dev, /rails-test, /rails-deploy, /rails-verify, /rails-init)가 commands/ 폴더에 존재하는가?

#### 1H. chain_report_generator.py 동기화
- [ ] chain_report_generator.py가 V4.1의 10개 체인을 모두 알고 있는가?
- [ ] 에이전트 모델 매핑이 CLAUDE.md와 일치하는가? (이전에 insight_amplifier sonnet→opus 수정 있었음)

#### 1I. settings.local.json 정크 퍼미션 감사
> settings.local.json은 "허용" 클릭 시 자동 누적되는 파일이다. 대부분 일회성 허용이 영구 잔존한 것.

- [ ] **중복 퍼미션 식별**: settings.json에 이미 있는 것과 겹치는 항목 찾기
  - 예: `Bash(head:*)`, `Bash(cat:*)`, `Bash(ls:*)`, `Bash(python3:*)`, `Bash(git fetch:*)` 등 — settings.json에 이미 존재
- [ ] **일회성 테스트 명령어 식별**: 한 번 쓰고 필요 없는 것들
  - 예: 특정 `git commit -m "..."` 전체 메시지가 퍼미션으로 저장된 것
  - 예: `CLAUDE_CODE_AGENT_TEAM_ROLE="teammate" ...` 테스트 명령어
  - 예: `Bash(for:*)`, `Bash(do)`, `Bash(then)`, `Bash(fi)`, `Bash(done)`, `Bash(else)` — 쉘 구문이 개별 퍼미션으로 잡힌 것
- [ ] **불필요한 WebFetch 도메인 퍼미션 식별**: 일회성 웹 조회가 영구 퍼미션으로 남은 것
  - 예: `WebFetch(domain:twitter-thread.com)`, `WebFetch(domain:jetthoughts.com)` 등 — 한 번 조사하고 다시 쓸 일 없는 도메인
- [ ] **유지해야 할 퍼미션 분류**:
  - 유지 ✅: `mcp__context7__*`, `mcp__prompt-analyzer__analyze_prompt`, `mcp__filesystem__*` (사용 중인 MCP), `WebSearch`
  - 유지 ✅: `Bash(brew:*)`, `Bash(chmod:*)`, `Bash(jq:*)`, `Bash(sort:*)`, `Bash(xargs:*)`, `Bash(printf:*)`, `Bash(env:*)` — settings.json에 없는 유용한 명령어
  - 제거 🗑️: 나머지 중복 및 일회성 항목
- [ ] 정리된 settings.local.json 초안 작성 (수정 전 백업 필수)

#### 1J. MCP 서버 감사
- [ ] `claude mcp list`로 현재 등록된 MCP 서버 확인
- [ ] 각 MCP 서버가 실제로 사용되고 있는지 확인:
  - `prompt-analyzer` MCP: prompt_analyzer_mcp.py 기반 — 사용 여부?
  - `context7` MCP: Context7 라이브러리 문서 조회 — 사용 여부?
  - `filesystem` MCP: 파일시스템 접근 — settings.local.json에 6개 퍼미션 존재, 필요한가?
- [ ] 미사용 MCP 서버가 있다면 제거 후보로 표시
- [ ] `~/.claude/mcp-env/` 가상환경이 정상인지 확인 (pip 패키지 목록)

### Phase 2: 불일치 리포트
> Phase 1 완료 후, 발견된 모든 불일치를 하나의 리포트로 정리한다.

- [ ] 불일치 목록 작성 (파일, 위치, 현재값, 기대값, 심각도: Critical/Major/Minor)
- [ ] 각 불일치에 대한 수정 방안 제안
- [ ] 수정 시 다른 곳에 영향을 미치는지 의존성 분석
- [ ] 리포트를 사용자에게 보고하고 수정 승인 받기

### Phase 3: 수정 실행 (승인 후)
> 사용자 승인 후에만 실행한다.

- [ ] 수정 대상 파일별 백업 생성 (`.healthcheck.backup`)
- [ ] Critical 불일치 먼저 수정
- [ ] 각 수정 후 즉시 검증:
  - prompt_analyzer.py 수정 시 → `python3 prompt_analyzer.py "테스트 프롬프트"` 실행하여 에러 없는지 확인
  - prompt_analyzer_mcp.py 수정 시 → 동일한 테스트
  - auto-analyze.sh 수정 시 → `bash -n auto-analyze.sh` 문법 검증
  - settings.json 수정 시 → `python3 -c "import json; json.load(open('settings.json'))"` JSON 유효성 확인
- [ ] Major 불일치 수정
- [ ] Minor 불일치 수정 (선택적)

### Phase 4: 통합 검증
> 모든 수정 완료 후 전체 시스템이 정상 작동하는지 확인한다.

- [ ] 프롬프트 분석 테스트 (5가지 시나리오):
  1. `"시스템 아키텍처를 설계해줘"` → SystemDesignChain 매칭 확인
  2. `"이 버그 급하게 고쳐줘"` → HotfixChain 매칭 확인
  3. `"Rails 8으로 새 프로젝트 시작"` → RailsDevChain 매칭 확인
  4. `"이 문서를 영어로 번역해줘"` → translation-specialist 매칭 + DocChain 오탐 아님 확인
  5. `"왜 이 접근법이 최선인지 심층 분석해줘"` → MetaThinkChain 매칭 확인
- [ ] `/analyze` 커맨드 작동 확인
- [ ] 메모리 저장 프로토콜 동작 확인 (최근 3개 읽기 → 중복 검사 → 저장)
- [ ] settings.json 유효성 최종 확인
- [ ] 모든 에이전트 파일의 YAML frontmatter가 유효한지 확인

### Phase 5: 문서화
- [ ] 발견된 불일치 + 수정 내역을 메모리에 저장 (`2602_0XX_orchestration_health_check.md`)
- [ ] CLAUDE.md의 Change History에 건강 검진 결과 기록
- [ ] 불필요한 백업 파일 정리 (수정이 성공적으로 검증된 경우)

---

## 추가 최적화 검토 (Optional)

아래는 "불일치 수정"이 아니라 "개선 가능 사항"이다. 발견만 하고 별도 리포트로 제출한다.

- [ ] 유틸리티 에이전트 8개 (doc-indexer, knowledge-mapper, link-doctor, meeting-note-wizard, memory-report-generator, project-dashboard, session-memo-writer, worklog-analyzer)가 실제로 사용되고 있는가? (Nov 8 2025 생성 이후 미사용 가능성. 체인에 포함되지 않고, CLAUDE.md에도 미참조)
- [ ] prompt_analyzer.py의 코드 크기 (36KB)가 과도하지 않은가? 불필요한 코드가 있는가?
- [ ] debug/ 폴더에 24MB+ 디버그 로그 — 정리 필요한가?
- [ ] prompt_analyzer.py.v21.backup, CLAUDE.md.v39.backup 등 구버전 백업 파일 정리 필요한가?
- [ ] session-env/ 폴더의 오래된 세션 정리 필요한가?
- [ ] settings.json의 SessionStart Hook — `echo '🚀 Claude Code 세션 시작'` 만 하는데 실질적 가치가 있는가?
- [ ] settings.json의 PreToolUse Bash Hook — `echo '[🔵 실행 예정]'` 이 모든 Bash 명령 전에 실행되면서 불필요한 출력을 만들고 있지 않은가?

---

## 결과물

1. **건강 검진 리포트** (메모리 저장): 전체 체크 결과, 불일치 목록, 수정 내역
2. **수정된 파일 목록**: 변경 전/후 diff
3. **검증 로그**: Phase 4 테스트 결과

---

*이 검진은 기존 시스템을 파괴하지 않으면서 동기화 상태만 확인하고, 실제 문제가 있는 것만 최소한으로 수정하는 것이 목표입니다.*
