## 2. Orchestration System

> **모든 사용자 프롬프트에 대해 자동 실행**

### 2.1 Hook 분석 흐름

```
프롬프트 입력 → UserPromptSubmit Hook (auto-analyze.sh V3.0+)
    → prompt_analyzer.py V4.0 (4-Layer + 오탐 방지 + 신뢰도 + 한국어 40개+)
    → memory_recall (Qdrant 벡터 검색, 0.3초 상주 서버)
    → additionalContext로 결과 주입 → Claude가 체인 선택
```

**4-Layer 분석**: Lexical(키워드) → Syntactic(구조) → Discourse(복잡도) → Pragmatic(의도)

**오탐 방지 및 정밀 보정**:
- 컨텍스트 윈도우 분석 (키워드 주변 ±3단어 확인)
- "버전"→번역 오탐 방지 (주변 언어명 필수)
- "문서"→docx 오탐 방지 (동사 분석: "보여줘" vs "만들어")
- 제약 감지 ("작업하지 말고", "분석만", "먼저 보여줘")
- 메타 작업 감지 (CLAUDE.md, Hook → SystemDesignChain 우선)
- 상호 배제 (번역↔문서 충돌 방지)
- 신뢰도 점수 (0.95 화용 > 0.85 메타 > 0.8 키워드 > 0.5 fallback)
- 0.6 미만 필터링, 최대 3개 추천

**생략 조건**: 10자 미만, `/command` 형식, Teammate 세션
**수동 분석**: `/analyze <프롬프트>`

**이전 프롬프트 자동 저장**: 새 프롬프트 입력 시 Hook이 이전 프롬프트 메모리 저장 지시
**주의**: 마지막 프롬프트는 `/memory-save` 수동 저장 필요

### 2.2 Chain Selection

**Hook = 촉매(Catalyst)**: Hook은 "정확한 추천자"가 아닌 "체인 활성화 촉매" 역할. 체인의 존재를 상기시키는 것만으로 가치 있음.

```
Hook 추천 수신 → 아리 자체 분석 → {
  일치 → Hook 근거로 실행
  불일치 → 아리 판단 우선, 불일치 사유 1줄 출력
  Hook 미추천 → 아리 자율 판단
}
→ 체인 매칭 (A~J) → 매칭 시 실행
                  ↓ 실패
        동적 체인 생성 (Agent + Skill 조합)
```

**Teams 모드 분기 (적극 활용)**:
1. 프롬프트에 독립 병렬 2+ 작업 감지 → **Teams 기본** (체인 무관)
2. Teams 적합 체인(Research/GameDev/WebDev) 선택 시 → **Teams 우선 고려**
3. 앤이 "팀으로", "병렬로", "동시에" 명시 → **Teams 즉시 전환**
4. 순차 의존성 높거나 긴급 → Chain 유지

**Pre-execution Declaration**: `📋 체인 구성: [Chain name] → step1[model] → step2[model]`

**Simple Task Exception**: 단순 Q&A, 한 줄 수정, 파일 읽기, "간단히" 요청 시 체인 생략

### 2.3 통합 매핑 테이블 (Single Source of Truth)

> **Skill ↔ Agent ↔ Chain 일원화** — 이 테이블이 유일한 매핑 참조

#### Agents (subagent_type → model → chain)

| subagent_type | Model | Primary Chain | Role |
|---------------|-------|---------------|------|
| `insight_explorer` | **O** | MetaThinkChain, ResearchChain | 패턴 발견, 관찰 |
| `multidimensional_analyst` | **O** | ResearchChain, MetaThinkChain | 다차원 분석 |
| `connection_creator` | **O** | MetaThinkChain | 연결, 은유 |
| `problem_reframer` | **O** | SystemDesignChain, MetaThinkChain | 관점 전환 |
| `solution_innovator` | **O** | MetaThinkChain, SystemDesignChain | 혁신적 솔루션 |
| `insight_amplifier` | **O** | MetaThinkChain, ResearchChain | 심화, Why/What-If |
| `learning_evolver` | **O** | MetaThinkChain | 학습, 메타인지 |
| `complexity_resolver` | **O** | HotfixChain | 복잡성 분해 |
| `balanced_judge` | **O** | MetaThinkChain | 의사결정, 판단 |
| `integrated_sage` | **O** | SystemDesignChain, ResearchChain, MetaThinkChain | 통합 지혜 |
| `requirements_analyst` | **O** | AutomationChain, DevChain, DocChain+, GameDevChain, WebDevChain+ | 요구사항 |
| `system_architect` | **O** | SystemDesignChain, DevChain, GameDevChain, WebDevChain+ | 아키텍처 설계 |
| `code_developer` | **O** | AutomationChain, DevChain, GameDevChain, HotfixChain | TDD 개발 |
| `quality_reviewer` | **O** | 거의 모든 체인 (마지막 단계) | 코드 리뷰 (범용) |
| `logic-reviewer` | **O** | DevChain, SystemDesignChain, WebDevChain+, AutomationChain, GameDevChain | 논리적 정합성 전문 리뷰 |
| `security-reviewer` | **O** | DevChain, SystemDesignChain, WebDevChain+, AutomationChain, GameDevChain | OWASP 보안 취약점 리뷰 |
| `edge-case-reviewer` | **O** | DevChain, SystemDesignChain, WebDevChain+, AutomationChain, GameDevChain | 엣지케이스/경계값 리뷰 |
| `grader` | **O** | (평가 루프 — A3) | eval_test.json 기반 채점 |
| `comparator` | **O** | (평가 루프 — A3) | 블라인드 버전 비교, 회귀 감지 |
| `eval-analyzer` | **O** | (평가 루프 — A3) | 실패 근본 원인 분석 |

#### Skills (/ command)

| Skill | 트리거 키워드 | Chain |
|-------|-------------|-------|
| `/translation-specialist` | 번역, 영어 버전, 한국어로 | - (독립) |
| `/docx` | Word, docx, 워드 | DocChain+ |
| `/pdf` | PDF, 추출 | DocChain+ |
| `/pptx` | PowerPoint, 프레젠테이션 | DocChain+ |
| `/xlsx` | Excel, 스프레드시트 | DocChain+ |
| `/doc-coauthoring` | 협업 문서, 공동 작성 | DocChain+ (Collab) |
| `/frontend-design` | 프론트엔드, UI | WebDevChain+, GameDevChain |
| `/web-artifacts-builder` | React, shadcn, 아티팩트 | WebDevChain+ |
| `/webapp-testing` | Playwright, e2e 테스트 | WebDevChain+ |
| `/mcp-builder` | MCP, protocol | AutomationChain |
| `/canvas-design` | 시각 디자인, 포스터 | (독립) |
| `/theme-factory` | 테마, 팔레트 | WebDevChain+ |
| `/algorithmic-art` | 알고리즘 아트, p5.js | (독립) |
| `/brand-guidelines` | 브랜드, Anthropic 스타일 | WebDevChain+ |
| `/slack-gif-creator` | GIF, Slack | (독립) |
| `/rails-*` (7개) | Rails, 레일즈, Kamal | RailsDevChain |
| `/claude-api` | Claude API, SDK, anthropic | DevChain |
| `/claude-strategy` | 사용전략, 개발전략 | (독립) |
| `/vibe-dev` | 바이브 개발, 새 프로젝트 | DevChain (독립 사이클) |
| `/commit-push` | 커밋, 푸시, git push | (마무리 단계) |
| `/pr-review` | PR 리뷰, 커밋 리뷰 | (독립) |
| `/project-review` | 프로젝트 리뷰, 전체 리뷰 | (독립) |
| `/memory-save` | 메모리 저장, 기록 | (독립) |
| `/readme-gen` | README, 리드미 | (독립) |
| `/internal-comms` | 보고서, 상태 업데이트, 뉴스레터 | DocChain+ |

#### Exploration Tools

| Tool | Model | 용도 |
|------|-------|------|
| `Explore` | **O** | 코드베이스 탐색 |
| `Plan` | **O** | 계획, 전략 설계 |
| `general-purpose` | **O** | 다목적 검색 |

### 2.4 Dynamic Chain Patterns V2.0 (A~J)

> **Notation**: [O] = opus (전 에이전트 통일), [-] = main session
> → = 순차, ∥ = 병렬

> ⚠️ **임의 축약 금지**: 체인 선택 후, 정의된 모든 에이전트를 순서대로 실행한다.
> - "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
> - 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
> - 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다

#### Effort Level 분화 (C8)

| Effort | 체인 | 행동 |
|--------|------|------|
| **HIGH** | SystemDesignChain (A), ResearchChain (E), MetaThinkChain (H) | 에이전트 전원 완전 실행, 다차원 분석, Why/What-If |
| **MEDIUM** | AutomationChain (B), GameDevChain (C), DevChain (D), DocChain+ (F), WebDevChain+ (G), RailsDevChain (I) | 구현 품질 + 테스트 커버리지 확보 |
| **LOW** | HotfixChain (J) | 최소 진단 → 최소 변경 → 즉시 검증 |

> **Pre-execution Declaration 형식**: `📋 체인 구성: [Chain name] [EFFORT] → step1 → step2`

#### A. SystemDesignChain (시스템 설계) — Effort: HIGH
```
(Explore[O] ∥ Read[-]) → (system_architect[O] ∥ problem_reframer[O])
→ [research.md] → [plan.md + 인간 승인(필수)]
→ solution_innovator[O] → integrated_sage[O]
→ (Edit[-] ∥ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]))
```
> CLAUDE.md 업데이트, 체인 개선, 아키텍처 설계
> 트리거: "시스템 설계", "아키텍처", "체인 개선" | **메타 작업 자동 감지**
> **스킬 파일**: `skills/chains/system-design.md` (7단계 상세)

#### B. AutomationChain (자동화 개발) — Effort: MEDIUM
```
requirements_analyst[O] → (WebSearch[∥] ∥ Context7[∥])
→ code_developer[O] → (Bash[-] ∥ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]))
```
> Hook, MCP, 커스텀 커맨드, 스크립트 개발

#### C. GameDevChain (게임 개발) — Effort: MEDIUM
```
requirements_analyst[O] →
( (system_architect[O] → code_developer[O])[Roblox] ∥
  (system_architect[O] → /frontend-design[-])[Web] )
→ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O])
```
> Roblox + Web 듀얼 트랙 게임 개발

#### D. DevChain (일반 개발) — Effort: MEDIUM
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[O] ∥ Context7[∥])
→ [research.md] → [plan.md + 승인 게이트]
→ code_developer[O] → ((logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O]) ∥ Bash[테스트][-])
```
> 일반 소프트웨어 개발, 코딩, TDD
> **스킬 파일**: `skills/chains/dev-chain.md` (7단계 상세, 복잡도 분기 포함)

#### E. ResearchChain (연구) — Effort: HIGH
```
(WebSearch[∥] ∥ Context7[∥] ∥ Explore[O]) →
(multidimensional_analyst[O] ∥ insight_explorer[O]) →
insight_amplifier[O] → integrated_sage[O] → Write[-] | /docx[-]
```
> 기술 분석, 적합성 조사, 트렌드 연구

#### F. DocChain+ (문서) — Effort: MEDIUM
```
[Solo]   requirements_analyst[O] → /docx|/pdf|/pptx|/xlsx[-] → quality_reviewer[O]
[Collab] /doc-coauthoring[-] → /docx|/pdf|/pptx[-] → quality_reviewer[O]
```
> 문서 생성 (단독/협업 모드)

#### G. WebDevChain+ (웹 개발) — Effort: MEDIUM
```
requirements_analyst[O] → (system_architect[O] ∥ Explore[O] ∥ /brand-guidelines[-])
→ (/theme-factory[-] → /frontend-design[-]) → /webapp-testing[-]
→ (logic-reviewer[O] ∥ security-reviewer[O] ∥ edge-case-reviewer[O])
```
> 웹 애플리케이션 개발 (디자인 포함)

#### H. MetaThinkChain (메타 사고) — Effort: HIGH
```
(insight_explorer[O] ∥ connection_creator[O]) →
(multidimensional_analyst[O] ∥ learning_evolver[O]) →
solution_innovator[O] →
balanced_judge[O] | problem_reframer[O] →
insight_amplifier[O] → integrated_sage[O]
```
> 심층 분석, 의사결정, 학습, Why/What-If

#### I. RailsDevChain (Rails 8) — Effort: MEDIUM
```
/rails-prd[-] → /rails-plan[-] → (/rails-dev[-] → /rails-test[-]) × N
→ /rails-deploy[-] → /rails-verify[-]
```
> Rails 8 바이브코딩 풀 사이클
> **상세**: `~/.claude/RAILS.md` (레일즈/rails/RAILS/kamal/바이브코딩 감지 시 자동 참조)

#### J. HotfixChain (긴급 수정) — Effort: LOW
```
(complexity_resolver[O] ∥ Explore[O] ∥ Grep[-]) → code_developer[O]
→ (Bash[테스트][-] ∥ quality_reviewer[O])
```
> 긴급 버그 수정, 핫픽스

#### Chain Selection Matrix

| 작업 유형 | 체인 | 키 에이전트 | 스킬 파일 | 리뷰어 |
|----------|------|-----------|----------|--------|
| 시스템/아키텍처 | SystemDesignChain | system_architect, solution_innovator, integrated_sage | `chains/system-design.md` ✅ | 3종 병렬 |
| 자동화/Hook/MCP | AutomationChain | requirements_analyst, code_developer | 미구현 | 3종 병렬 |
| 게임 (Roblox/Web) | GameDevChain | 듀얼 트랙 병렬 | 미구현 | 3종 병렬 |
| 일반 개발 | DevChain | requirements→architect→developer | `chains/dev-chain.md` ✅ | 3종 병렬 |
| 연구/조사 | ResearchChain | multidimensional_analyst, insight_amplifier | 미구현 | — |
| 문서 생성 | DocChain+ | Solo/Collab 모드 선택 | 미구현 | — |
| 웹 개발 | WebDevChain+ | 디자인 통합 | 미구현 | 3종 병렬 |
| 심층 사고 | MetaThinkChain | solution_innovator, insight_amplifier, integrated_sage | 미구현 | — |
| Rails 8 | RailsDevChain | 바이브코딩 풀 사이클 | 미구현 | — |
| 긴급 수정 | HotfixChain | complexity_resolver | 미구현 | quality_reviewer 단독 |

### 2.5 Agent Teams 통합

> **환경변수**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (settings.json)
> **원칙**: 독립 병렬 작업 2개+ 감지 시 Teams를 **기본값**으로 사용한다.

#### Teams 자동 트리거 조건 (적극 활용)

> ⚠️ 아래 조건 중 **하나라도** 해당하면 Teams 모드를 **우선 고려**한다.

| 트리거 | 예시 | Teams 구성 |
|--------|------|-----------|
| **다중 파일 탐색** | "A와 B를 각각 분석해줘" | Teammate A(파일 A) + Teammate B(파일 B) |
| **독립 리서치 2+** | "프레임워크 X와 Y를 비교해줘" | Researcher X + Researcher Y → Lead 통합 |
| **병렬 생성** | "문서 3개 동시에 만들어줘" | Writer 1 + Writer 2 + Writer 3 |
| **탐색+구현 분리** | "기존 코드 분석하면서 새 기능 설계해줘" | Explorer(탐색) + Architect(설계) |
| **리뷰 병렬화** | 코드 리뷰 단계 | logic-reviewer + security-reviewer + edge-case-reviewer |
| **앤 명시 요청** | "팀으로 해줘", "병렬로", "동시에" | 앤 지시에 따른 구성 |

#### Chain ↔ Teams 선택 기준

| 작업 특성 | 권장 | 이유 |
|----------|------|------|
| 독립 병렬 가능 | **Agent Teams (기본)** | 각 teammate 독립 작업 → 속도 2~3x |
| 순차 의존성 높음 | Chain | step간 결과 전달 필요 |
| 탐색+설계 혼합 | **Hybrid (적극)** | Teams(탐색) → Chain(설계) |
| 긴급/빠른 완결 | Chain | Teams 오버헤드 과다 |
| 단순 작업 | 직행 | Teams/Chain 모두 불필요 |

#### Teams 전환 적합도

| 체인 | Teams 전환 | 구성 | 트리거 |
|------|-----------|------|--------|
| ResearchChain | **적합** | Researcher / Analyst / Synthesizer | 조사 대상 2+ |
| GameDevChain | **적합** | Roblox Dev / Web Dev | 듀얼 트랙 |
| WebDevChain+ | **적합** | Design / Frontend / Testing | 디자인+개발 분리 |
| SystemDesignChain | **하이브리드** | Teams(탐색) → Chain(설계) | 탐색 범위 넓을 때 |
| DevChain | **조건부** | research 병렬 탐색 가능 | 파일 3개+ 탐색 시 |
| HotfixChain | **부적합** | 순차 우선 | — |
| RailsDevChain | **부적합** | rails-* 스킬 순차 | — |

#### 구체적 Teams 구성 패턴

**패턴 1: 병렬 탐색 (가장 빈번)**
```
Lead: 작업 분배 → Teammate A: 영역 1 탐색 → 결과 보고
                → Teammate B: 영역 2 탐색 → 결과 보고
Lead: 결과 통합 → 다음 단계
```

**패턴 2: 병렬 생성**
```
Lead: 템플릿/지시 배포 → Teammate A: 문서 1 작성 → 완료 보고
                       → Teammate B: 문서 2 작성 → 완료 보고
                       → Teammate C: 문서 3 작성 → 완료 보고
Lead: 품질 통합 검토
```

**패턴 3: 병렬 리뷰 (B1)**
```
Lead: 코드 diff 배포 → logic-reviewer: 논리 검토
                     → security-reviewer: 보안 검토
                     → edge-case-reviewer: 엣지 검토
Lead: 리포트 통합 (Critical/Warning/Info)
```

**패턴 4: 하이브리드 (탐색→설계)**
```
[Teams Phase] Lead → Teammate A: 코드베이스 탐색
                   → Teammate B: 외부 자료 조사
[Chain Phase] Lead: research.md 통합 → plan.md 작성 → 구현
```

#### 동시성 보호

| 위험 | 감지 | 해결 |
|------|------|------|
| Hook 중복 | teammate 환경변수 | `auto-analyze.sh` V3.0 자동 스킵 |
| Memory Race | Lead 세션 검증 | Lead만 저장, Teammate 전달만 |
| 상태 파일 경합 | SESSION_ID 충돌 | SESSION_ID별 분리 |
| **Teammate 무응답** | **spawn 후 합리적 타임아웃(기본 120초) 무메시지** | **shutdown_request → Lead 직접 수행 or 재spawn** |
| **Teammate 정체** | **task in_progress 장시간(기본 300초) 무진행** | **Lead 상태 확인 → 필요시 재할당** |

#### Teammate 행동 규칙

1. **메모리 저장 금지** — 결과를 Lead에게 전달
2. **4-Layer 분석 스킵** — Hook이 자동 감지
3. **Chain 실행 가능** — 독립 작동
4. **착수 보고 의무** — spawn 후 합리적 시간(기본 30초) 내 Lead에게 첫 메시지 전송
5. **장애 시 자동 대체** — 무응답 Teammate는 Lead가 shutdown 후 직접 수행
6. **감지 조건**: `CLAUDE_CODE_AGENT_TEAM_ROLE = "teammate"`

### 2.6 워크플로우 통합 (research → plan → 구현)

> **원칙**: 체인을 교체하지 않는다. 체인 **내부**에 research→plan 단계를 삽입한다.
> **템플릿**: `~/.claude/workflow/templates/` (research_template.md, plan_template.md)
> **검증**: `~/.claude/scripts/gate1_checker.sh` (Gate 1 자동 검증)
> **리뷰 규칙**: `~/.claude/REVIEW.md` (Critical/Warning/Info)

#### 복잡도 분기 기준

| 복잡도 | 기준 | 워크플로우 | 적용 체인 |
|--------|------|-----------|----------|
| **단순** | 한 줄 수정, 파일 읽기, Q&A | 기존 체인 직행 (워크플로우 생략) | HotfixChain, 단순 Q&A |
| **중규모** | 파일 3개+ 수정, 새 기능 | research.md + plan.md (인간 게이트 조건부) | DevChain, AutomationChain |
| **대규모** | 아키텍처 변경, 신규 시스템 | 전체 3단계 + 인간 승인 필수 | SystemDesignChain, WebDevChain+, GameDevChain |

#### 인간 승인 게이트 (Gate 2)

- plan.md의 `Status: draft | approved | rejected`가 게이트 잠금 장치
- `Status: approved` 전까지 code_developer 실행 금지
- 앤의 "응 진행해줘", "좋아", "ㅇㅇ" → approved
- "수정해줘" → draft 유지 + 수정 반영
- "아니야" → rejected

#### 워크플로우 미적용 체인

| 체인 | 이유 |
|------|------|
| ResearchChain | 연구 자체가 목적 (research.md 내재적) |
| DocChain+ | 문서 생성에 불필요 |
| MetaThinkChain | 사고 자체가 목적 |
| HotfixChain | 긴급성 우선 |
| RailsDevChain | rails-prd/rails-plan이 이미 동등한 역할 수행 |
