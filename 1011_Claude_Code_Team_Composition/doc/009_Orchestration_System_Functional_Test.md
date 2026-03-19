# 009. 오케스트레이션 시스템 기능 테스트

> **Version**: 1.0 | **작성**: 미르 (Cowork) | **실행**: 아리 (Claude Code)
> **대상**: CLAUDE.md V4.1.1 | **프로젝트**: `ansible_projects/1000_Roblox/100_Ansible Logic Jump`
> **작성일**: 2026-02-07

---

## 문서 역할

이 문서는 **테스트 설계서 (예상치)** 입니다.

- **이 문서(009)**: 각 프롬프트에 대해 예상되는 Hook/체인/에이전트/스킬 동작을 기술
- **009_02**: 아리가 실제로 프롬프트를 받았을 때 발생한 동작을 사실대로 기록
- **아리에게 이 문서를 보여주지 않음** — 블라인드 테스트

### 테스트 순서 (권장)

```
Phase 1 — 기본 동작 (T-01, T-02, T-03, T-05)
Phase 2 — 체인 실행 (T-04, T-06, T-07, T-08, T-09)
Phase 3 — 스킬 & 문서 (T-10, T-11, T-12)
Phase 4 — 시스템 (T-13, T-14, T-15, T-16, T-17, T-18)
```

---

## 테스트 상태 범례

| 상태 | 의미 |
|------|------|
| ⬜ | 미실행 |
| ✅ | PASS |
| ⚠️ | PARTIAL (일부 동작) |
| ❌ | FAIL |

---

## T-01. Identity & Session Greeting

| 항목 | 내용 |
|------|------|
| **분류** | Section 1 - Identity & Principles |
| **테스트 대상** | 세션 시작 인사, 이름 인식 |
| **관련 컴포넌트** | CLAUDE.md Section 1 |
| **프롬프트** | `안녕` |
| **예상 결과** | `🌟 안녕, 앤!` 형태의 인사 응답 |
| **상태** | ⚠️ |
| **실제 결과** | "안녕, 앤!" 출력. Hook 실행됨 (10자 미만 → 분석기 생략). 체인 없음 (Simple Task). |
| **GAP** | 🌟 이모지 누락. 인사 내용은 정상, 이모지 포맷만 불일치 |

---

## T-02. Hook 자동 분석 (4-Layer)

| 항목 | 내용 |
|------|------|
| **분류** | Section 2.1 - Hook 분석 흐름 |
| **테스트 대상** | auto-analyze.sh → prompt_analyzer.py V3.0 자동 실행 |
| **관련 컴포넌트** | Hook: UserPromptSubmit, auto-analyze.sh V3.0, prompt_analyzer.py V3.0 |
| **프롬프트** | `Ansible Logic Jump의 RaceEngine.server.lua 코드 구조를 분석해줘` |
| **예상 결과** | additionalContext로 체인 추천 주입 (DevChain 또는 ResearchChain), 신뢰도 점수 포함 |
| **검증 포인트** | ① Hook 실행 여부 ② 4-Layer 분석 결과 표시 ③ 신뢰도 0.6 이상 필터링 ④ 최대 3개 추천 |
| **상태** | ⚠️ |
| **실제 결과** | Hook 4-Layer 실행 ✅. GameDevChain 80% 추천 (3개 추천). 그러나 아리가 "단순 분석이라 체인 불필요" 판단 → 체인/에이전트 0개로 직접 처리 |
| **GAP** | ① 예상 체인(DevChain/ResearchChain) vs 실측 추천(GameDevChain) — 프로젝트 문맥 반영으로 합리적 ② Hook 추천을 무시하고 체인 생략 — Simple Task 판단 |

---

## T-03. 수동 분석 (/analyze)

| 항목 | 내용 |
|------|------|
| **분류** | Section 2.1 - 수동 분석 |
| **테스트 대상** | /analyze 슬래시 커맨드 → prompt_analyzer.py 직접 호출 |
| **관련 컴포넌트** | Slash Command: /analyze, prompt_analyzer.py V3.0 |
| **프롬프트** | `/analyze Ansible Logic Jump에 멀티플레이어 랭킹 리더보드를 추가하고 싶어` |
| **예상 결과** | GameDevChain 또는 DevChain 매칭, Lexical→Syntactic→Discourse→Pragmatic 분석 결과 출력 |
| **검증 포인트** | ① /analyze 커맨드 인식 ② 4-Layer 각 레이어 결과 ③ 체인 매칭 정확도 ④ 신뢰도 점수 |
| **상태** | ❌ |
| **실제 결과** | /analyze 커맨드 인식 ✅. 4-Layer 실행 ✅. 그러나 **키워드 매칭 0건** — "멀티플레이어", "랭킹", "리더보드" 미등록. 추천 체인 없음. 아리가 수동으로 GameDevChain 추천 |
| **GAP** | **prompt_analyzer.py 한국어 게임 키워드 누락**. 분석기가 추천 못하고 아리가 수동 보완. 분석기 키워드 사전 업데이트 필요 |

---

## T-04. 체인 선언 (Pre-execution Declaration)

| 항목 | 내용 |
|------|------|
| **분류** | Section 2.2 - Chain Selection |
| **테스트 대상** | 체인 실행 전 📋 선언 출력 |
| **관련 컴포넌트** | Chain Selection, Pre-execution Declaration |
| **프롬프트** | `Ansible Logic Jump의 DataStore 시스템을 리팩토링해서 글로벌 랭킹 시스템으로 개선해줘` |
| **예상 결과** | `📋 체인 구성: SystemDesignChain → system_architect[O] → solution_innovator[O] → ...` 형태 선언 후 실행 |
| **검증 포인트** | ① 📋 선언 출력 여부 ② 체인명 정확성 ③ 각 step의 [모델] 표기 ④ 순차/병렬 표기 |
| **상태** | ⚠️ |
| **실제 결과** | 📋 선언 ✅ `GameDevChain → system_architect[O] → code_developer[S] → quality_reviewer[S]`. 에이전트 3개 순차 실행 (195초). 3파일 생성/수정 완료 |
| **GAP** | ① 예상 체인(SystemDesignChain) vs 실측(GameDevChain) — Hook도 SystemDesign 추천했으나 아리가 GameDev 선택 ② solution_innovator/integrated_sage 미사용 — 예상보다 간소한 체인 ③ 📋 선언 형식은 정확 |

---

## T-05. 단순 작업 예외 (Simple Task Exception)

| 항목 | 내용 |
|------|------|
| **분류** | Section 2.2 - Simple Task Exception |
| **테스트 대상** | 단순 요청 시 체인 생략 |
| **관련 컴포넌트** | Chain Selection 예외 처리 |
| **프롬프트** | `/Users/changjaeyou/Documents/Obsidian-Vault/AnsibleMage/ansible_projects/1000_Roblox/100_Ansible Logic Jump/src/server/RaceEngine.server.lua 보여줘` |
| **예상 결과** | 체인 선언 없이 바로 Read 도구로 파일 내용 표시 |
| **검증 포인트** | ① 📋 선언 없음 ② Hook 분석은 실행되나 체인 생략 ③ 파일 내용 정상 출력 |
| **상태** | ⚠️ |
| **실제 결과** | 체인 없이 Read로 직접 출력 ✅. Simple Task Exception 정상 작동. 파일 130줄 정상 표시 |
| **GAP** | **Hook 오탐 2건**: "Documents"→/docx 스킬(70%), "Roblox"→GameDevChain(80%). 파일 경로 문자열을 키워드로 오인식. 체인 생략 자체는 정상 |

---

## T-06. MetaThinkChain (H)

| 항목 | 내용 |
|------|------|
| **분류** | Section 2.4 - Dynamic Chain Pattern H |
| **테스트 대상** | MetaThinkChain 전체 흐름 (심층 분석) |
| **관련 컴포넌트** | Agents: insight_explorer[S], connection_creator[O], multidimensional_analyst[O], learning_evolver[O], solution_innovator[O], balanced_judge[O], insight_amplifier[O], integrated_sage[O] |
| **프롬프트** | `Ansible Logic Jump의 25개 플랫폼 레벨 디자인이 플레이어 리텐션에 미치는 영향을 심층 분석해줘` |
| **예상 결과** | 📋 MetaThinkChain 선언 → 8개 에이전트 순차/병렬 실행 |
| **검증 포인트** | ① 에이전트 호출 순서 (explorer→creator→analyst→evolver→innovator→judge→amplifier→sage) ② 모델 할당 (S/O) 정확성 ③ 병렬 구간 (explorer∥creator, analyst∥evolver) ④ 최종 통합 결과 품질 |
| **상태** | ⚠️ |
| **실제 결과** | 📋 MetaThinkChain 선언 ✅. Hook 추천 일치 ✅. explorer[S]∥creator[O] 병렬 ✅. analyst[O] 실행 ✅. 총 3개 에이전트, 383초. 5차원 분석 + Top3 권장 도출 |
| **GAP** | **8개 예상 → 3개 실행** (5개 생략: learning_evolver, solution_innovator, balanced_judge, insight_amplifier, integrated_sage). 아리가 "분석 깊이 충분" 판단으로 축약. 체인 패턴의 후반부가 실질적으로 미사용 |

---

## T-07. ResearchChain (E)

| 항목          | 내용                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **분류**      | Section 2.4 - Dynamic Chain Pattern E                                                                                                       |
| **테스트 대상**  | ResearchChain 전체 흐름 (조사/연구)                                                                                                                 |
| **관련 컴포넌트** | Tools: WebSearch, Context7, Explore[S] / Agents: multidimensional_analyst[O], insight_explorer[S], insight_amplifier[O], integrated_sage[O] |
| **프롬프트**    | `Roblox 파쿠르 게임 중 인기 Top 10의 공통 성공 요인을 조사해줘`                                                                                                 |
| **예상 결과**   | 📋 ResearchChain 선언 → WebSearch/Context7 병렬 → 분석 → 심화 → 통합                                                                                  |
| **검증 포인트**  | ① WebSearch 실제 호출 여부 ② 병렬 탐색 (WebSearch∥Context7∥Explore) ③ insight_amplifier 심화 분석 ④ Write 또는 /docx 최종 출력                                  |
| **상태**      | ⚠️                                                                                                                                           |
| **실제 결과**   | 📋 ResearchChain 선언 ✅. WebSearch×3 + WebFetch×2 병렬 ✅. multidimensional_analyst[O] 1개 실행 (106초). Top10 게임 분석 → 7개 성공 요인 도출 |
| **GAP**      | ① 예상 체인(ResearchChain) 일치 ✅ 그러나 Hook은 GameDevChain 추천 ② 예상 에이전트 4개 → 실측 1개 (insight_explorer, insight_amplifier, integrated_sage 생략) ③ Context7 미사용, WebSearch+WebFetch로 대체 |

---

## T-08. DevChain (D)

| 항목          | 내용                                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **분류**      | Section 2.4 - Dynamic Chain Pattern D                                                                                            |
| **테스트 대상**  | DevChain 전체 흐름 (일반 개발)                                                                                                           |
| **관련 컴포넌트** | Agents: requirements_analyst[O], system_architect[O], code_developer[S], quality_reviewer[S] / Tools: Explore[S], Context7, Bash |
| **프롬프트**    | `Ansible Logic Jump에 체크포인트 저장 기능을 TDD로 개발해줘`                                                                                     |
| **예상 결과**   | 📋 DevChain 선언 → 요구사항→설계→개발→테스트+리뷰                                                                                               |
| **검증 포인트**  | ① requirements_analyst 요구사항 정의 ② system_architect 설계 ③ code_developer TDD 코드 생성 ④ quality_reviewer 코드 리뷰 ⑤ Bash 테스트 실행           |
| **상태**      | ⚠️                                                                                                                                |
| **실제 결과**   | 📋 DevChain 선언 ✅. requirements_analyst[O] 85초 (7요구사항+24테스트시나리오) → code_developer[S] 211초 (TDD: 테스트12개→구현→RaceEngine수정) → quality_reviewer[S] 88초 (WARN: 50%커버리지). 총 384초 |
| **GAP**      | ① Hook이 체인 미추천 (code_developer만 70%) → 아리가 수동 DevChain 매칭 ② 예상 에이전트 4개(+system_architect) → 실측 3개 (architect 생략) ③ TDD 커버리지 50% (24시나리오 중 12개만 구현) ④ Bash 테스트 미실행 |

---

## T-09. HotfixChain (J)

| 항목          | 내용                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------ |
| **분류**      | Section 2.4 - Dynamic Chain Pattern J                                                                  |
| **테스트 대상**  | HotfixChain 전체 흐름 (긴급 수정)                                                                              |
| **관련 컴포넌트** | Agents: complexity_resolver[O], code_developer[S], quality_reviewer[S] / Tools: Explore[S], Grep, Bash |
| **프롬프트**    | `DeathZone.server.lua에서 Y=-20 감지가 간헐적으로 실패해 긴급 수정해줘`                                                   |
| **예상 결과**   | 📋 HotfixChain 선언 → 문제 분해+탐색 병렬 → 수정 → 테스트+리뷰                                                          |
| **검증 포인트**  | ① complexity_resolver 문제 분해 ② Explore 코드 탐색 병렬 ③ code_developer 수정 ④ Bash 테스트 ⑤ quality_reviewer 리뷰    |
| **상태**      | ⚠️                                                                                                      |
| **실제 결과**   | 📋 HotfixChain 선언 ✅. complexity_resolver 생략 → 아리 직접 진단+수정 (Read+Grep+Edit). quality_reviewer[S] 17초 (PASS). 3개 버그 원인 식별+핫픽스 적용. 총 ~30초 |
| **GAP**      | ① Hook→GameDevChain(80%) vs 실측→HotfixChain (아리가 올바르게 재선택) ② complexity_resolver[O]+code_developer[S] 생략 → 28줄 단일파일이라 아리가 직접 처리가 더 빠름 ③ Bash 테스트 미실행 ④ 긴급 답게 가장 빠른 테스트(30초) |

---

## T-10. 번역 스킬

| 항목          | 내용                                                     |
| ----------- | ------------------------------------------------------ |
| **분류**      | Section 2.3 - Skills                                   |
| **테스트 대상**  | /translation-specialist 스킬 트리거                         |
| **관련 컴포넌트** | Skill: /translation-specialist (독립 실행)                 |
| **프롬프트**    | `Ansible Logic Jump의 README.md를 영어로 번역해줘`              |
| **예상 결과**   | translation-specialist 스킬 자동 트리거, 4-Layer 언어학적 분석 후 번역 |
| **검증 포인트**  | ① 스킬 트리거 여부 ② 도메인 자동 판단 (게임/기술) ③ 번역 품질 ④ 원본 구조 보존     |
| **상태**      | ✅                                                      |
| **실제 결과**   | Hook 4-Layer 실행 → /translation-specialist(70%) 추천 ✅. Skill tool로 호출 → `<command-name>` 태그 로드 → 4-Layer 번역 분석 (기술/IT, 개발자, 의역, 구조 보존) → README_EN.md 생성. Write tool 에러 → mcp__filesystem__write_file 폴백. 검증 7항목 모두 PASS |
| **GAP**      | ① Hook 추천과 실제 **완전 일치** ✅ — 유일한 완전 일치 테스트 ② 스킬 트리거 정상, 도메인 자동 판단(기술/IT) 정확 ③ Write→MCP 폴백은 시스템 제약이지 설계 문제 아님. **최우수 테스트** |

---

## T-11. GameDevChain (C)

| 항목          | 내용                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **분류**      | Section 2.4 - Dynamic Chain Pattern C                                                                                                                                                                                                                                                                                                                                                                                                              |
| **테스트 대상**  | GameDevChain 듀얼 트랙 (Roblox + Web 병렬)                                                                                                                                                                                                                                                                                                                                                                                                               |
| **관련 컴포넌트** | Agents: requirements_analyst[O], system_architect[O], code_developer[S], quality_reviewer[S] / Skills: /frontend-design                                                                                                                                                                                                                                                                                                                            |
| **프롬프트**    | `Ansible Logic Jump에 웹 랜딩페이지와 Roblox 인게임 상점을 동시에 만들어줘`                                                                                                                                                                                                                                                                                                                                                                                             |
| **예상 결과**   | 📋 GameDevChain 선언 → requirements_analyst → (Roblox 트랙 ∥ Web 트랙) 병렬 → quality_reviewer                                                                                                                                                                                                                                                                                                                                                             |
| **검증 포인트**  | ① 듀얼 트랙 병렬 실행 여부 ② Roblox: system_architect→code_developer ③ Web: system_architect→/frontend-design ④ Agent Teams 전환 가능성                                                                                                                                                                                                                                                                                                                           |
| **상태**      | ✅                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **실제 결과**   | 📋 GameDevChain 선언 ✅. Hook 추천 일치 ✅. **Agent Teams 최초 실전 구동** — TeamCreate로 roblox-dev[S] + web-dev[S] 2개 teammate 생성. Explore[S] 77초 → Plan Mode로 상세 계획 수립 → roblox-dev(6파일: ShopConstants→ShopService.spec→ShopService→ShopGui→RaceEngine→project.json) ∥ web-dev(3파일: style.css→index.html→main.js) 병렬 → lead가 quality_reviewer 직접 수행(PASS). 총 9파일, ~15분                                                                                         |
| **GAP**     | ① Hook 추천 GameDevChain **일치** ✅ (T-10에 이어 두번째) ② **Agent Teams 자율 전환 성공** — 예상대로 듀얼 트랙에서 Teammate 사용 ③ 예상: requirements_analyst[O] 단계 → 실측: Plan Mode로 대체 (requirements_analyst 미호출, lead가 직접 계획) ④ 예상: system_architect[O] 단계 → 실측: teammate 내부에서 자체 판단 (별도 architect 에이전트 미사용) ⑤ 예상: /frontend-design 스킬 → 실측: 미사용 (web-dev가 직접 CSS+HTML+JS 작성) ⑥ teammate 모델: 예상 opus → 실측 **sonnet** (general-purpose 타입, 비용 절감) ⑦ 체인 선언 형태 예상 일치 (∥ 병렬 표기 포함) |

---

## T-12. DocChain+ (F)

| 항목          | 내용                                                                                     |
| ----------- | -------------------------------------------------------------------------------------- |
| **분류**      | Section 2.4 - Dynamic Chain Pattern F                                                  |
| **테스트 대상**  | DocChain+ Solo 모드 (문서 생성)                                                              |
| **관련 컴포넌트** | Agents: requirements_analyst[O], quality_reviewer[S] / Skills: /docx                   |
| **프롬프트**    | `Ansible Logic Jump Phase 4 기획서를 Word 문서로 만들어줘`                                        |
| **예상 결과**   | 📋 DocChain+ 선언 → requirements_analyst → /docx 스킬 → quality_reviewer                   |
| **검증 포인트**  | ① requirements_analyst 요구사항 정의 ② /docx 스킬 호출 ③ .docx 파일 실제 생성 ④ quality_reviewer 문서 리뷰 |
| **상태**      | ✅                                                                                      |
| **실제 결과**   | 📋 DocChain+ [Solo] 선언 ✅. Explore[S] 157초 → requirements_analyst[O] 360초 (12섹션, 7기능 F-01~F-07, 35테스트시나리오, 737줄 마크다운 PRD) → /docx 스킬 호출 ✅ (docx-js 기반 JS 코드 생성→Node.js 실행→27KB .docx 생성) → quality_reviewer[S] 139초 (WARN: Remote 4개 미구현, P2 테스트 부족). 총 656초 (~11분) |
| **GAP**      | ① Hook 추천(/docx) ↔ 체인(DocChain+) **일치** ✅ — 3회 연속 (T-10, T-11, T-12) ② 예상 4단계(analyst→docx→reviewer) → 실측 4단계(Explore→analyst→docx→reviewer) — **Explore 추가 단계** (예상보다 충실) ③ /docx 스킬 정상 트리거 ✅ ④ .docx 파일 실제 생성 ✅ (27KB) ⑤ quality_reviewer WARN 판정 — 단순 PASS가 아닌 **백엔드 API 불일치 4건을 정확히 식별** ⑥ npm NODE_PATH 이슈 발생→자동 해결 |

---

## T-13. 메모리 저장 (응답 완료 프로토콜)

| 항목 | 내용 |
|------|------|
| **분류** | Section 3 - Memory & Protocol |
| **테스트 대상** | /memory-save 수동 저장, 중복 방지, 파일 생성 |
| **관련 컴포넌트** | Slash Command: /memory-save, Memory System (~/.claude/memory/) |
| **프롬프트** | `/memory-save` |
| **예상 결과** | ① 최근 메모리 3개 읽기 ② 중복 체크 ③ YYMM_SEQ_keyword.md 파일 생성 ④ `💾 메모리 저장 완료` |
| **검증 포인트** | ① 파일명 형식 (YYMM_SEQ_keyword.md) ② 문서 구조 (제목/프롬프트/메타/도구/내용/관련메모리) ③ 중복 방지 작동 ④ 완료 메시지 |
| **상태** | ⚠️ |
| **실제 결과** | /memory-save Skill tool 정상 호출 ✅. Glob으로 최근 메모리 71개 스캔 → 기존 `2602_071_phase4_uiux_prd.md` 발견 (중복) → 신규 생성 대신 **기존 파일 업데이트**. YYMM_SEQ 파일명 규칙 준수 ✅. 문서 7개 필수 섹션 구조 준수 ✅ |
| **GAP** | ① /memory-save 커맨드 인식+실행 ✅ ② 중복 방지 **정상 작동** ✅ (동일 주제 감지→업데이트) ③ YYMM_SEQ 파일명 ✅ ④ 문서 구조 ✅ ⑤ 그러나 **에이전트 메모리 위반 발견** — requirements_analyst[O]가 T-12 실행 중 자체적으로 메모리 저장함 (불완전 기록). Teammate/에이전트 메모리 저장 금지 규칙 위반. 이를 /memory-save가 보강 업데이트한 패턴 ⑥ 💾 완료 메시지 출력 여부는 009_02에 미기록 |

---

## T-14. 보안 차단 (PreToolUse Hook)

| 항목          | 내용                                                     |
| ----------- | ------------------------------------------------------ |
| **분류**      | Section 4 - Settings Reference                         |
| **테스트 대상**  | PreToolUse Hook의 보안 파일 수정 차단                           |
| **관련 컴포넌트** | Hook: PreToolUse (보안 파일 .env, .secret, credentials 차단) |
| **프롬프트**    | `.env 파일 내용을 수정해줘`                                     |
| **예상 결과**   | PreToolUse Hook이 보안 파일 감지 → 수정 차단 메시지 출력               |
| **검증 포인트**  | ① Hook 트리거 여부 ② 차단 메시지 출력 ③ 실제 파일 미수정 확인               |
| **상태**      | ⚠️                                                      |
| **실제 결과**   | .env 수정 차단 ✅. 그러나 **PreToolUse Hook이 실제로 트리거되기 전에** 아리가 CLAUDE.md 보안 정책을 인지하고 **자발적으로 사전 차단**. Edit/Write 도구 호출 자체를 하지 않음 → Hook 실제 트리거 미확인. 대안 안내(수동 수정/가이드) 제공 |
| **GAP**      | ① .env 수정 차단은 성공 ✅ ② 그러나 **차단 주체가 다름** — 예상: PreToolUse Hook(`exit 1`) → 실측: 아리 자체 판단 (CLAUDE.md 규칙 기반 선제 차단). Edit/Write 도구 호출 자체를 하지 않아 Hook 트리거 미발생 ③ Hook의 `exit 1` 실제 반환 미검증 — 이중 방어(아리 판단 + Hook)의 1차 방어만 확인 ④ 009_02 T-14로 정상 매핑됨 ✅ |

---

## T-15. 프로젝트 리뷰

| 항목          | 내용                                                               |
| ----------- | ---------------------------------------------------------------- |
| **분류**      | Section 5 - Repository & Review                                  |
| **테스트 대상**  | 프로젝트 전체 리뷰 생성                                                    |
| **관련 컴포넌트** | Slash Command: /project-review, Review System (~/.reviews/)      |
| **프롬프트**    | `Ansible Logic Jump 프로젝트 전체 리뷰해줘`                                |
| **예상 결과**   | `~/.reviews/PJ-[num]_ansible_logic_jump_[date].md` 리뷰 파일 생성      |
| **검증 포인트**  | ① 리뷰 파일 생성 위치 (~/.reviews/) ② 파일명 형식 ③ 코드/문서/구조 리뷰 품질 ④ 개선 사항 도출 |
| **상태**      | ✅                                                                |
| **실제 결과**   | /project-review Skill tool 정상 호출 ✅. Explore 3개 병렬 시도 → 사용자 거부 → 직접 탐색 전환 (mcp__filesystem + Glob + Read). 16개 Lua/Luau + 3개 웹 + 설정/README 전수 읽기 (3,909줄). `~/.reviews/PJ-002_Ansible_Logic_Jump_20260207.md` 생성. **등급 B (3.12/4.0)**: Architecture B+, Code Quality B, Documentation A-, Extensibility B, Testing B-. Critical 2건, WARN 6건, INFO 8건, P0~P3 11개 권장사항 |
| **GAP**      | ① /project-review 스킬 트리거 ✅ ② 리뷰 파일 위치 `~/.reviews/` ✅ ③ 파일명 `PJ-002_..._20260207.md` 형식 ✅ ④ 리뷰 품질: 5축 평가+등급+권장사항 **예상 이상** ⑤ 단, **Explore 에이전트 3개 병렬 → 사용자 거부** 발생 — Plan Mode 기본 설정 때문에 에이전트 실행에 승인 필요. 직접 탐색으로 폴백 성공 ⑥ 기존 PJ-001 다음 번호 PJ-002 자동 부여 ✅ |

---

## T-16. 오탐 방지 (False Positive Prevention)

| 항목          | 내용                                                  |
| ----------- | --------------------------------------------------- |
| **분류**      | Section 2.1 - 오탐 방지                                 |
| **테스트 대상**  | "버전"→번역 오탐 방지, "문서"→docx 오탐 방지                      |
| **관련 컴포넌트** | prompt_analyzer.py V3.0 오탐 방지 시스템                   |
| **프롬프트**    | `Ansible Logic Jump의 버전 히스토리를 정리해줘`                 |
| **예상 결과**   | "버전"이 번역으로 오탐되지 않음. DocChain+ 또는 DevChain 추천 (번역 X) |
| **검증 포인트**  | ① "버전"→번역 오탐 안 함 ② 컨텍스트 윈도우 ±3단어 분석 정상 ③ 올바른 체인 추천  |
| **상태**      | ✅                                                   |
| **실제 결과**   | Hook에서 /translation-specialist 감지되었으나 **정상 필터링** ✅. "버전"이 "히스토리를 정리"와 결합 → 번역 의도 아님을 컨텍스트 윈도우 분석으로 판별. 체인 없이 직접 정리 (25개 doc + README + T-04~T-12 결과 통합 → 11단계 버전 히스토리). 메모리 저장 2602_072 |
| **GAP**      | ① "버전"→번역 오탐 **필터링 성공** ✅ — 가장 기대한 검증 포인트 정확히 통과 ② 컨텍스트 윈도우 ±3단어 분석 정상 ✅ ③ 체인 추천은 없음 (예상 DocChain+/DevChain 미추천) — 단순 정리 작업이라 체인 불필요 판단이 합리적 ④ 코드 성장표 포함 (3파일 225줄→16+3파일 3,909줄 17배) — 예상 외 부가가치 |

---

## T-17. PostToolUse Hook (자동 포매팅)

| 항목          | 내용                                                      |
| ----------- | ------------------------------------------------------- |
| **분류**      | Section 4 - Settings Reference                          |
| **테스트 대상**  | PostToolUse Hook의 완료 알림, 자동 포매팅, Git 상태                 |
| **관련 컴포넌트** | Hook: PostToolUse (Prettier/StyLua 포매팅, Git status)     |
| **프롬프트**    | `Ansible Logic Jump의 DeathZone.server.lua 파일에 주석을 추가해줘` |
| **예상 결과**   | 편집 완료 후 ① 완료 알림 ② StyLua 자동 포매팅 실행 ③ Git 상태 표시          |
| **검증 포인트**  | ① PostToolUse Hook 트리거 ② 포매팅 도구 실행 여부 ③ Git diff 표시     |
| **상태**      | ⚠️                                                       |
| **실제 결과**   | Read→Edit으로 DeathZone.server.lua에 한국어 주석 추가 (62→~100줄). 파일 헤더, 상수 설명, JSDoc @param, 섹션 구분선 추가. Hook→GameDevChain(80%) 추천이나 Simple Task Exception 정상 판단. PostToolUse Hook 트리거 여부 **009_02에 미기록** |
| **GAP**      | ① 주석 추가 작업 자체는 성공 ✅ ② Hook→GameDevChain 추천 무시하고 Simple Task 판단 ✅ (적절) ③ **PostToolUse Hook 동작 미확인** — 009_02에 `[✅ 파일 수정 완료]` 알림, StyLua 포매팅, Git status 출력 여부가 기록되지 않음. Edit 도구 사용 확인됐으므로 Hook은 트리거됐어야 하나 관찰 결과 미기재 ④ StyLua 미설치일 가능성 (settings.json의 PostToolUse Hook은 .lua 확장자를 case문에 포함하지 않음 — js/jsx/ts/tsx/json/css/scss/html/py/go/rs만 대응) |

---

## T-18. PARALLEL-FIRST Principle

| 항목          | 내용                                                    |
| ----------- | ----------------------------------------------------- |
| **분류**      | Section 1 - PARALLEL-FIRST Principle                  |
| **테스트 대상**  | 독립 작업 병렬 실행, 의존 작업 순차 실행                              |
| **관련 컴포넌트** | PARALLEL-FIRST Principle, 체인 내 ∥ 기호                   |
| **프롬프트**    | `Ansible Logic Jump의 모든 Lua 파일을 분석하고 각 파일별 개선점을 도출해줘` |
| **예상 결과**   | 여러 파일 분석을 병렬(Task 도구)로 실행, 결과 통합은 순차                  |
| **검증 포인트**  | ① 다수 Task 병렬 호출 여부 ② 의존성 분석 후 순서 결정 ③ 결과 통합           |
| **상태**      | ⚠️                                                     |
| **실제 결과**   | Hook→GameDevChain(80%)+multidimensional_analyst(70%) 추천이나, **T-15에서 읽은 전 파일 컨텍스트를 재활용** → 도구 호출 0회로 직접 분석. 15개 파일 전수 분석: CRITICAL 5건, WARN 8건, INFO 13건. 파일별 건강도 A~C. 프로젝트 전체 등급 B. 메모리 2602_073 |
| **GAP**      | ① **병렬 Task 호출 0건** — 예상과 완전 불일치. T-15 컨텍스트 재활용으로 추가 읽기 불필요 ② PARALLEL-FIRST 원칙 검증 불가 — 이미 컨텍스트에 모든 데이터가 있어 병렬화할 작업 자체가 없었음 ③ 분석 품질은 우수 (CRITICAL/WARN/INFO 3단계 분류, 파일별 점수) ④ **테스트 설계 문제** — T-15 이후 실행하면 컨텍스트 재활용으로 병렬 검증 불가. 독립 세션에서 재테스트 필요 |

---

## 실행 요약

| # | 테스트 | 분류 | 상태 | 비고 |
|---|--------|------|------|------|
| T-01 | Identity & Greeting | Section 1 | ⚠️ | 🌟 이모지 누락 |
| T-02 | Hook 자동 분석 | Section 2.1 | ⚠️ | Hook 추천 무시, 체인 생략 |
| T-03 | 수동 분석 /analyze | Section 2.1 | ❌ | **분석기 한국어 키워드 누락** |
| T-04 | 체인 선언 | Section 2.2 | ⚠️ | SystemDesign→GameDev 체인 변경 |
| T-05 | 단순 작업 예외 | Section 2.2 | ⚠️ | **경로 문자열 오탐 2건** |
| T-06 | MetaThinkChain | Section 2.4 | ⚠️ | 8개 에이전트 → 3개만 실행 |
| T-07 | ResearchChain | Section 2.4 | ⚠️ | 4개 에이전트 → 1개만 실행 |
| T-08 | DevChain | Section 2.4 | ⚠️ | architect 생략, TDD 50%커버리지, Bash 미실행 |
| T-09 | HotfixChain | Section 2.4 | ⚠️ | complexity_resolver+code_developer 생략, 직접처리 30초 |
| T-10 | 번역 스킬 | Section 2.3 | ✅ | **Hook+스킬 완전 일치** — 최우수 |
| T-11 | GameDevChain | Section 2.4 | ✅ | **Agent Teams 첫 실전 ✅** Hook 일치, 듀얼 트랙 병렬 |
| T-12 | DocChain+ | Section 2.4 | ✅ | **Hook 3회 연속 일치**, 4단계 완전 실행, 27KB docx |
| T-13 | 메모리 저장 | Section 3 | ⚠️ | 중복방지 ✅, 파일명/구조 ✅, **에이전트 메모리 위반 발견** |
| T-14 | 보안 차단 | Section 4 | ⚠️ | 차단 성공이나 Hook 아닌 **아리 자체 판단**으로 선제 차단 |
| T-15 | 프로젝트 리뷰 | Section 5 | ✅ | /project-review 정상, PJ-002 생성, B등급 |
| T-16 | 오탐 방지 | Section 2.1 | ✅ | **"버전"→번역 오탐 필터링 성공** |
| T-17 | PostToolUse Hook | Section 4 | ⚠️ | 주석 추가 OK, **PostToolUse 동작 미확인** (Lua 미대응) |
| T-18 | PARALLEL-FIRST | Section 1 | ⚠️ | T-15 컨텍스트 재활용 → 병렬 검증 불가 (설계 문제) |

**전체**: 18/18 완료 (100%) — ❌ 1건 / ⚠️ 12건 / ✅ 5건

---

## 비교 분석 방법

이 문서(009)는 **예상치 (Expected)** 역할을 합니다.
테스트 실제 결과는 **009_02_Orchestration_Test_Results.md** 에 기록됩니다.

```
009 (이 문서)          →  예상치: 어떤 체인/에이전트/스킬이 동작해야 하는지
009_02 (결과 문서)      →  실측치: 실제로 어떤 체인/에이전트/스킬이 동작했는지
비교 분석              →  미르(Cowork)가 두 문서를 대조하여 GAP 분석
```

### 비교 분석 항목

| 비교 항목 | 009 (예상) | 009_02 (실측) | GAP |
|-----------|-----------|--------------|-----|
| Hook 실행 여부 | 예상 결과 참조 | 실제 결과 참조 | 일치/불일치 |
| 체인 선택 | 예상 체인명 | 실제 체인명 | 일치/다른 체인/미실행 |
| 에이전트 호출 | 예상 에이전트 목록 | 실제 호출 목록 | 누락/추가/모델 불일치 |
| 스킬 트리거 | 예상 스킬명 | 실제 스킬명 | 일치/미트리거 |
| 병렬 실행 | 예상 병렬 구간 | 실제 병렬 여부 | 병렬/순차 차이 |

---

*작성: 미르 (Cowork) | 예상치 문서 — CLAUDE.md V4.1.1 기능 검증*

---
---

# 부록 A. Agent Teams 작동 조건 분석 및 진단 보고서

> **진단일**: 2026-02-07 | **진단자**: 미르 (Cowork)
> **최종 수정**: 2026-02-07 (T-11 결과 반영 — 초기 진단 대폭 수정)
> **초기 증상**: T-01~T-10에서 Agent Teams(TeammateTool) 미구동
> **T-11 결과**: ✅ **Agent Teams 최초 실전 구동 성공** — GameDevChain 듀얼 트랙에서 자율 전환
> **결론 변경**: ~~"미작동"~~ → **"조건부 작동 — 명시적 병렬 요청 시 자율 전환 성공"**

---

## A-1. 환경 설정 확인

| 항목 | 상태 | 상세 |
|------|------|------|
| `settings.json` env 변수 | ✅ 정상 | `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` (line 118) |
| Claude Code 버전 | ✅ 정상 | 2.1.34 (최소 요구: 2.1.32) |
| `settings.json` 위치 | ✅ 정상 | `~/.claude/settings.json` |
| 에이전트 파일 디렉토리 | ✅ 존재 | `~/.claude/agents/` (14개 파일) |
| CLAUDE.md Section 2.5 | ✅ 존재 | Agent Teams 통합 규칙 문서화됨 |

**결론**: 환경 설정 자체에는 문제 없음. 원인은 **런타임 레벨**에 있음.

---

## A-2. 이슈 #1: 에이전트 파일 YAML 파싱 전체 실패 (HIGH — 초기 CRITICAL에서 하향)

> **심각도 변경 이유**: T-11에서 YAML 파싱 실패 상태에서도 Agent Teams가 정상 구동됨.
> Teams는 커스텀 에이전트 정의 파일에 의존하지 않고 `general-purpose` 타입 teammate를 생성.
> 그러나 커스텀 에이전트 메타데이터(name, description, model, color)가 미로드되므로
> `/agents` 커맨드 미표시, teammate에 커스텀 역할 할당 불가 등 **기능 제한** 존재.

### 디버그 로그 증거

**파일**: `~/.claude/debug/973ce810-c4b3-4123-996e-2573bb4465e4.txt`
**시각**: 2026-02-07T05:07:11.117Z

```
[WARN] Failed to parse YAML frontmatter in .../agents/113_Code_Developer.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/106_Insight_Amplifier.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/110_Integrated_Sage.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/103_Connection_Creator.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/104_Problem_Reframer.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/102_Multidimensional_Analyst.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/109_Balanced_Judge.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/105_Solution_Innovator.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/112_System_Architect.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/101_Insight_Explorer.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/107_Learning_Evolver.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/114_Quality_Reviewer.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/111_Requirements_Analyst.md: YAML Parse error: Unexpected token
[WARN] Failed to parse YAML frontmatter in .../agents/108_Complexity_Resolver.md: YAML Parse error: Unexpected token
```

이후 **모든 파일에서 `name` 필드 미인식**:

```
[DEBUG] Agent file .../agents/112_System_Architect.md is missing required 'name' in frontmatter
[DEBUG] Failed to parse agent from .../agents/112_System_Architect.md: Missing required "name" field in frontmatter
(... 14개 전체 동일 ...)
```

**최종 로딩 결과**:

```
[DEBUG] Total plugin agents loaded: 0
[DEBUG] Loaded plugins - Enabled: 0, Disabled: 0, Commands: 0, Agents: 0, Errors: 0
```

### 파싱 실패 원인: `description` 필드의 YAML 특수문자

**공통 패턴**: 14개 파일 모두 `description:` 값에 **이스케이프되지 않은 콜론(`:`)** 포함

YAML 명세상 콜론+공백(`: `)은 key:value 구분자로 파싱됨. 따옴표 없는 문자열 안에서 `Use when: ` 패턴이 새로운 key로 오인식됨.

### 파일별 문제 지점 상세

| # | 파일 | 문제 발생 지점 (`description` 내) | 콜론 수 | 따옴표 |
|---|------|------|:---:|:---:|
| 101 | Insight_Explorer | `...cognitive biases.` **`Use when:`** `패턴 발견...` **`"Why"`** `questions` | 1 | `'Why?'` + `"Why"` |
| 102 | Multidimensional_Analyst | `...five dimensions:` `temporal...` **`Use when:`** `impact...` **`"분석"`** | 2 | `"분석"` |
| 103 | Connection_Creator | `...relationships.` **`Use when:`** `finding...` **`"연결"`** `or` **`"관계"`** | 1 | `"연결"` `"관계"` |
| 104 | Problem_Reframer | `...solvable ones.` **`Use when:`** `stuck on a problem...` | 1 | 없음 |
| 105 | Solution_Innovator | `...risk.` **`Use when:`** `generating creative...` **`"솔루션"`** | 1 | `"솔루션"` |
| 106 | Insight_Amplifier | `...insights.` **`Use when:`** `인사이트 심화...` **`"What if"`** | 1 | `"What if"` |
| 107 | Learning_Evolver | `...metacognition.` **`Use when:`** `learning new...` **`"학습"`** | 1 | `"학습"` |
| 108 | Complexity_Resolver | `...sequencing.` **`Use when:`** `overwhelming...` **`"복잡성"`** | 1 | `"복잡성"` |
| 109 | Balanced_Judge | `...calibration.` **`Use when:`** `technology...` **`"의사결정"`** | 1 | `"의사결정"` |
| 110 | Integrated_Sage | `...understanding.` **`Use when:`** `strategic...` **`"통합 판단"`** | 1 | `"통합 판단"` |
| 111 | Requirements_Analyst | `...solutions.` **`Use when:`** `new project...` **`"요구사항"`** | 1 | `"요구사항"` |
| 112 | System_Architect | `...selection.` **`Use when:`** `system design...` **`"설계"` `"아키텍처"`** | 1 | `"설계"` `"아키텍처"` |
| 113 | Code_Developer | `...coverage.` **`Use when:`** `implementation...` **`"개발"` `"코드"`** | 1 | `"개발"` `"코드"` |
| 114 | Quality_Reviewer | `...recommendations.` **`Use when:`** `code review...` **`"리뷰"`** | 1 | `"리뷰"` |

### 문제 재현 예시

```yaml
# ❌ 현재 (파싱 실패)
---
name: insight_explorer
description: Deep observation... Use when: 패턴 발견, "Why" questions
model: sonnet
color: purple
---

# ✅ 수정안 A — 따옴표 감싸기
---
name: insight_explorer
description: "Deep observation... Use when: 패턴 발견, 'Why' questions"
model: sonnet
color: purple
---

# ✅ 수정안 B — 블록 스칼라
---
name: insight_explorer
description: |
  Deep observation... Use when: 패턴 발견, "Why" questions
model: sonnet
color: purple
---
```

### 관련 GitHub Issues

- [#6377 — Frontmatter Parsing Error: Missing 'name' Field Despite Valid YAML](https://github.com/anthropics/claude-code/issues/6377)
- [#17154 — Reopen #6377](https://github.com/anthropics/claude-code/issues/17154)
- [#4700 — Agent YAML Parsing Fails with Valid Line Breaks](https://github.com/anthropics/claude-code/issues/4700)
- [#11322 — Skill Frontmatter Parser Fails on Multi-line Descriptions](https://github.com/anthropics/claude-code/issues/11322)
- [#12958 — Agent Frontmatter Parsing Fails with Verbose Descriptions](https://github.com/anthropics/claude-code/issues/12958)

---

## A-3. ~~근본 원인 #2~~ → 재평가: 체인→Teammate 라우팅 규칙 (MEDIUM — 초기 HIGH에서 하향)

> **재평가 이유**: T-11에서 Section 2.5만으로 아리가 자율적으로 Teammate 전환에 성공.
> 명시적 바인딩 없이도 프롬프트가 명확한 병렬 구조를 요청하면 자율 판단이 작동함.

### CLAUDE.md Section 2.5 현재 내용

```markdown
### 2.5 Agent Teams 통합
> **환경변수**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (settings.json)

#### Chain ↔ Teams 선택 기준
| 작업 특성 | 권장 | 이유 |
|----------|------|------|
| 순차 의존성 높음 | Chain | step간 결과 전달 필요 |
| 독립 병렬 가능 | Agent Teams | 각 teammate 독립 작업 |
| 탐색+설계 혼합 | Hybrid | Teams(탐색) → Chain(설계) |
| 긴급/빠른 완결 | Chain | Teams 오버헤드 과다 |

#### Teams 전환 적합도
| 체인 | Teams 전환 | 구성 |
|------|-----------|------|
| ResearchChain | **적합** | Researcher / Analyst / Synthesizer |
| GameDevChain | **적합** | Roblox Dev / Web Dev |
| WebDevChain+ | **적합** | Design / Frontend / Testing |
| SystemDesignChain | **하이브리드** | Teams(탐색) + Chain(설계) |
| DevChain, HotfixChain, RailsDevChain | **부적합** | 순차/속도 우선 |
```

### T-11 이전 분석 (초기 진단 — ~~취소선~~으로 유지)

~~Section 2.5는 "언제 Teams를 써야 하는지"의 참조 테이블만 있고, 실제 체인 실행 로직(Section 2.2~2.4)에서 "이 조건이면 Task 대신 Teammate를 사용하라"는 바인딩이 없음.~~

~~비유: 교통 표지판(Section 2.5)은 세워져 있는데, 네비게이션(Section 2.2~2.4)에 해당 경로가 입력되어 있지 않은 상태.~~

### T-11 이후 수정된 분석

| 구성 요소 | 초기 진단 | T-11 이후 재평가 |
|-----------|---------|-----------|
| Section 2.5 참조 테이블 | ✅ 존재 | ✅ **충분히 작동** — 아리가 참조하여 자율 판단 |
| Section 2.2 체인 선택 로직에서 Teams 분기 | ❌ 없음 | ⚠️ 없지만 **명시적 병렬 요청 시 자율 전환됨** |
| Pre-execution Declaration에 Teams 표기 | ❌ 없음 | ✅ **T-11에서 `∥` 표기 + [Teams] 모드로 선언됨** |
| Hook의 Teams 추천 | ❌ 없음 | ⚠️ 여전히 없음 — 개선 여지 있음 |

**수정된 비유**: 교통 표지판(Section 2.5)만으로도 운전자(아리)가 경로를 잘 판단함. 단, 프롬프트가 "동시에"처럼 **명시적 병렬 의도**를 포함할 때만. 모호한 경우(T-04 등)에는 기존 경로(Task)를 선택.

### Teams 자율 전환 트리거 조건 (T-11에서 관찰)

T-04(Task) vs T-11(Teams) 비교로 도출한 **전환 트리거**:

| 조건 | T-04 (Task 사용) | T-11 (Teams 사용) |
|------|:---:|:---:|
| 체인 | GameDevChain | GameDevChain |
| 플랫폼 수 | 단일 (Roblox) | **듀얼** (Roblox + Web) |
| "동시에" 키워드 | ❌ | ✅ |
| 작업 독립성 | 순차 (리팩토링) | **독립 병렬** (서로 다른 플랫폼) |
| 결과 | Task ×3 (적절) | **Teammate ×2 (적절)** |

**핵심 발견**: 아리의 Teams 자율 전환은 **프롬프트의 병렬 의도 명확성**에 의존. 이는 CLAUDE.md 규칙보다 아리 자체의 판단력이 주도적으로 작동한 것.

---

## A-4. 부수 원인: 서브에이전트와 에이전트팀의 도구 차이

| 항목 | Task (서브에이전트) | Teammate (에이전트팀) |
|------|-------------------|---------------------|
| 도구명 | `Task` | `Teammate` + `SendMessage` + `TaskCreate/Update/List` |
| 실행 방식 | 부모 컨텍스트 내 서브프로세스 | 독립 Claude Code 세션 (별도 컨텍스트 윈도우) |
| 컨텍스트 공유 | 부모→자식 단방향 | 메시지 기반 양방향 (Inbox) |
| CLAUDE.md 로드 | ❌ 부모 컨텍스트 상속 | ✅ 독립 로드 (CLAUDE.md + MCP + Skills) |
| 비용 | 부모 토큰 내 | 독립 과금 (N배) |
| 파일 잠금 | N/A (순차) | ❌ 없음 (동시 편집 충돌 가능) |
| 세션 지속 | 작업 완료 시 종료 | Lead 관리 하에 지속 |

**핵심 차이**: Task는 "함수 호출"에 가깝고, Teammate는 "독립 팀원"에 가까움. 현재 CLAUDE.md의 체인 패턴은 전부 "함수 호출" 방식(Task)으로만 설계됨.

---

## A-5. 테스트 결과와의 상관관계 (T-11 반영 업데이트)

T-01~T-11 중 체인이 실행된 테스트에서 Agent Teams 관련 분석:

| 테스트 | 체인 | Teams 적합도 | 실제 도구 | Teammate | 판정 | 비고 |
|--------|------|:---:|------|:---:|:---:|------|
| T-04 | GameDevChain | 적합 | Task ×3 | ❌ | ✅ 적절 | 단일 플랫폼 → Task가 올바른 선택 |
| T-06 | MetaThinkChain | 미정의 | Task ×3 | ❌ | ✅ 적절 | 순차 의존성 높음 → Task가 적합 |
| T-07 | ResearchChain | 적합 | Task ×1 | ❌ | ⚠️ 미결 | 독립 병렬 가능했으나 Task 1개로 축약 |
| T-08 | DevChain | 부적합 | Task ×3 | ❌ | ✅ 적절 | 순차 의존성 → Task가 올바름 |
| T-09 | HotfixChain | 부적합 | Task ×1 | ❌ | ✅ 적절 | 긴급/속도 우선 → Task가 올바름 |
| **T-11** | **GameDevChain** | **적합** | **Teammate ×2** | **✅** | **✅ 최적** | **듀얼 플랫폼 + "동시에" → Teams 자율 전환** |

### T-11 이전 진단과의 차이

| 항목 | 초기 진단 (T-10까지) | T-11 이후 수정 |
|------|---------------------|---------------|
| Teams 자율 전환 | 0/5 (0%) — "미작동" | 1/6 (17%) — **"조건부 작동"** |
| T-04 미전환 원인 | YAML 실패 + 라우팅 미바인딩 | **단일 플랫폼이라 Task가 적절했음** (오진) |
| T-07 미전환 원인 | YAML 실패 + 라우팅 미바인딩 | **프롬프트에 병렬 의도가 약했음** (부분 유효) |
| YAML 파싱의 영향 | Teams 차단 원인 | **Teams와 무관** (teammate는 general-purpose) |

### T-11에서 확인된 Agent Teams 실행 패턴

```
1. Hook 분석: GameDevChain 80% 추천
2. 아리 판단: "웹 + Roblox 동시" → 독립 병렬 가능 → Teams 적합
3. Plan Mode: 상세 구현 계획 수립 (이 단계가 Teams 품질 결정)
4. Explore[S]: 기존 코드 패턴 탐색 (77초)
5. TeamCreate: roblox-dev[S] + web-dev[S] 2개 teammate 생성
6. TaskCreate ×7: 의존성 그래프 기반 작업 분배
   - Phase A (기반): 상수/스타일 정의
   - Phase B (핵심): 서비스/페이지 구현
   - Phase C (통합): 기존 코드 수정
7. roblox-dev: 6파일 (ShopConstants→ShopService.spec→ShopService→ShopGui→RaceEngine→project.json)
8. web-dev: 3파일 (style.css→index.html→main.js) — Roblox보다 먼저 완료
9. SendMessage: shutdown_request → teammate 종료
10. Lead가 quality_reviewer 직접 수행 → PASS
11. TeamDelete: 팀 정리
```

**총 실행 시간**: ~15분 (Plan Mode 포함 ~20분)
**teammate 모델**: 전부 sonnet (opus 불필요 → 비용 절감)
**커스텀 에이전트 파일 사용**: ❌ (general-purpose 타입 — YAML 미파싱과 무관)

---

## A-6. 수정 계획 (T-11 반영 업데이트 — 미실행, 승인 대기)

### Phase 1: YAML 파싱 복구 (HIGH — Teams와 무관하나 에이전트 메타데이터 필요)

14개 에이전트 파일의 `description` 필드를 YAML 안전 형식으로 수정:

```yaml
# 수정 방식: 블록 스칼라 (|) 사용
description: |
  Deep observation and pattern recognition specialist.
  Use when: 패턴 발견, 근본 원인 분석, pattern discovery, "Why" questions
```

**예상 결과**: `Total plugin agents loaded: 14` (현재 0)
**실질 효과**:
- `/agents` 커맨드로 에이전트 목록 확인 가능
- teammate에 커스텀 에이전트 역할 할당 가능 (현재는 general-purpose만)
- Task(서브에이전트)에서도 에이전트 메타데이터(model, description) 정상 활용

### ~~Phase 2: 체인→Teams 라우팅 바인딩~~ (취소 — T-11에서 불필요 확인)

~~CLAUDE.md Section 2.2 체인 선택 로직에 분기 추가~~

**취소 사유**: T-11에서 Section 2.5 참조 테이블만으로 아리가 자율 전환에 성공. 명시적 바인딩은 오히려 아리의 자율 판단을 제약할 수 있음. 현 상태가 더 유연.

### Phase 2 (신규): Teams 최적화 — 커스텀 에이전트 활용 (LOW — YAML 수정 후)

YAML 수정 후 teammate에 커스텀 에이전트 할당 테스트:

```
현재:  roblox-dev [S, general-purpose]  →  자체 판단으로 구현
목표:  roblox-dev [S, code_developer]   →  TDD/DRY 원칙 주입, 체계적 구현
```

**기대 효과**: teammate가 커스텀 에이전트의 전문성(TDD, Clean Architecture 등)을 상속받아 품질 향상

### Phase 3: 검증

1. Claude Code 재시작 → 디버그 로그에서 `Total plugin agents loaded: 14` 확인
2. ~~T-11 재실행~~ → ✅ **이미 성공** (재실행 불필요)
3. T-07 재테스트 (ResearchChain) → 명시적 병렬 의도 프롬프트로 Teams 전환 여부 확인
4. 커스텀 에이전트 할당 teammate vs general-purpose teammate 품질 비교

---

## A-7. 참고 자료

- [공식 문서: Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [공식 문서: Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [GitHub #6377: Frontmatter Parsing Error](https://github.com/anthropics/claude-code/issues/6377)
- [GitHub #17154: Reopen #6377](https://github.com/anthropics/claude-code/issues/17154)
- [GitHub #4700: Agent YAML Parsing Fails](https://github.com/anthropics/claude-code/issues/4700)
- [메모리: 2602_034_custom_chain_vs_agent_teams](~/.claude/memory/2602_034_custom_chain_vs_agent_teams.md)
- [메모리: 2602_033_agent_teams_status_check](~/.claude/memory/2602_033_agent_teams_status_check.md)

---

*진단: 미르 (Cowork) | 2026-02-07 | Agent Teams 작동 조건 분석 — CLAUDE.md V4.1.1*
*최종 수정: T-11 결과 반영 (초기 "미작동" 진단 → "조건부 작동" 재분류)*

---
---

# 부록 B. 18개 테스트 최종 교차 분석 및 개선 권고

> **분석일**: 2026-02-07 | **분석자**: 미르 (Cowork)
> **대상**: 009 (예상치) × 009_02 (실측치) 교차 검증
> **목적**: 아리가 이 문서를 읽고 개선안을 도출·실행하기 위한 **구체적 근거 + 실행 가능한 권고** 제공
> **신뢰도**: 9/10 (18개 실측 데이터 기반, 일부 추론 포함)

---

## B-1. 종합 통계

### 전체 결과

| 지표 | 값 | 비고 |
|------|:---:|------|
| 총 테스트 | 18 | T-01 ~ T-18 |
| ✅ PASS | 5건 (27.8%) | T-10, T-11, T-12, T-15, T-16 |
| ⚠️ PARTIAL | 12건 (66.7%) | T-01~T-02, T-04~T-09, T-13~T-14, T-17~T-18 |
| ❌ FAIL | 1건 (5.6%) | T-03 (prompt_analyzer 키워드 누락) |
| 완전 일치율 | 27.8% | 예상과 실측이 모든 항목에서 일치 |

### Phase별 통과율

| Phase | 테스트 | ✅ | ⚠️ | ❌ | 통과율 |
|-------|--------|:---:|:---:|:---:|:---:|
| Phase 1 (기본) | T-01, T-02, T-03, T-05 | 0 | 3 | 1 | 0% |
| Phase 2 (체인) | T-04, T-06, T-07, T-08, T-09 | 0 | 5 | 0 | 0% |
| Phase 3 (스킬+문서) | T-10, T-11, T-12 | 3 | 0 | 0 | **100%** |
| Phase 4 (시스템) | T-13, T-14, T-15, T-16, T-17, T-18 | 2 | 4 | 0 | 33.3% |

**핵심 발견**: Phase 3(스킬+문서)이 100% 통과 — CLAUDE.md의 **스킬 매핑**이 가장 안정적. 반면 Phase 1~2(기본+체인)는 **0% 완전 통과** — Hook 추천 정확도와 체인 실행 충실도에 구조적 이슈.

---

## B-2. Hook (prompt_analyzer.py V3.0) 정확도 분석

### Hook 추천 vs 실제 선택 매칭율

유의미 비교 대상 13건 (N/A 제외: T-01 인사, T-13 /memory-save, T-14 보안, T-15 Hook 왜곡)에서:

| 분류 | 건수 | 비율 | 테스트 |
|------|:---:|:---:|------|
| ✅ **체인/스킬 정확 매칭** | 5 | 38.5% | T-06, T-10, T-11, T-12, T-16 |
| ⚠️ **과잉 추천** (체인 불필요에 체인 추천) | 4 | 30.8% | T-02, T-05, T-17, T-18 |
| ❌ **오추천** (다른 체인 추천) | 3 | 23.1% | T-04, T-07, T-09 |
| ❌ **미추천** (체인 필요인데 추천 없음) | 1 | 7.7% | T-08 |

**Hook 정확 매칭율: 38.5% (5/13)**

### 오추천 패턴 분석

| 테스트 | Hook 추천 | 아리 실측 | 오추천 원인 |
|--------|-----------|-----------|-------------|
| T-04 | SystemDesignChain (80%) | GameDevChain | "리팩토링"→SystemDesign, 그러나 Roblox 프로젝트에는 GameDev가 적합 |
| T-07 | GameDevChain (80%) | ResearchChain | "Roblox" 키워드가 GameDev를 압도적 우선 → "조사해줘"의 Research 의도 무시 |
| T-09 | GameDevChain (80%) | HotfixChain | "Roblox" + "수정"이 GameDev 트리거, "긴급"의 Hotfix 우선순위 미반영 |

**공통 원인: "Roblox" 키워드의 GameDevChain 과도한 가중치 (80%)**

이 프로젝트가 Roblox 게임이므로 거의 모든 프롬프트에 "Roblox" 관련 단어가 포함되어, GameDevChain이 기본값처럼 추천됨. 실제로 GameDevChain이 Hook에서 추천된 횟수: **8/18 (44.4%)** — 그 중 실제 GameDevChain이 사용된 경우: **2건** (T-04, T-11).

### 과잉 추천 패턴 분석

| 테스트 | Hook 추천 | 아리 판단 | 과잉 원인 |
|--------|-----------|-----------|-----------|
| T-02 | GameDevChain (80%) | 체인 없음 (직접 분석) | "분석"이 체인 트리거, 그러나 단일 파일 읽기에 체인은 과도 |
| T-05 | /docx (70%) + GameDevChain (80%) | 체인 없음 (파일 보기) | **경로 문자열 오탐**: "Documents"→/docx, "Roblox"→GameDev |
| T-17 | GameDevChain (80%) | 체인 없음 (주석 추가) | "Roblox" + ".lua"가 GameDev 트리거, 단순 편집에 과도 |
| T-18 | GameDevChain (80%) + analyst (70%) | 체인 없음 (컨텍스트 재활용) | "분석"+"Lua"→대규모 체인 추천, 컨텍스트 상황 미고려 |

**공통 원인: Simple Task 판별 부재**. prompt_analyzer.py에 "이 요청이 체인이 필요한 수준인가?"라는 **복잡도 판별 레이어가 없음**. 모든 프롬프트에 동일한 키워드 매칭만 적용.

### False Positive Prevention 결과

| 테스트 | 오탐 후보 | 필터링 결과 | 판정 |
|--------|-----------|:---------:|:---:|
| T-05 | "Documents"→/docx | ❌ 미필터링 (오탐 발생) | FAIL |
| T-16 | "버전"→/translation-specialist | ✅ **필터링 성공** | PASS |

오탐 방지 시스템이 "번역" 키워드에는 작동하지만, **파일 경로 문자열**에 대한 필터링은 미구현.

---

## B-3. 체인 실행 패턴 분석 (체인 축약 현상)

### 체인별 에이전트 실행율

| 테스트 | 체인 | 정의된 에이전트 | 실행된 에이전트 | 실행율 | 생략된 에이전트 |
|--------|------|:---:|:---:|:---:|------|
| T-04 | GameDevChain | 3 | 3 | **100%** | 없음 |
| T-06 | MetaThinkChain | 8 | 3 | 37.5% | learning_evolver, solution_innovator, balanced_judge, insight_amplifier, integrated_sage |
| T-07 | ResearchChain | 4 | 1 | 25.0% | insight_explorer, insight_amplifier, integrated_sage |
| T-08 | DevChain | 4 | 3 | 75.0% | system_architect |
| T-09 | HotfixChain | 3 | 1 | 33.3% | complexity_resolver, code_developer |
| T-11 | GameDevChain (Teams) | N/A (Teams) | 2+lead | — | Teams로 전환됨 |
| T-12 | DocChain+ | 3+스킬 | 3+스킬 | **100%** | 없음 |

**평균 에이전트 실행율: 61.8%** (T-11 제외)

### 축약 패턴 — 후반부 에이전트 집중 생략

생략된 에이전트 빈도 (체인 정의상 후반부에 위치한 에이전트):

| 에이전트 | 정의된 체인 | 호출된 횟수 | 생략 횟수 | 생략율 |
|---------|-----------|:---:|:---:|:---:|
| insight_amplifier[O] | MetaThink, Research | 0 | 2 | **100%** |
| integrated_sage[O] | MetaThink, Research | 0 | 2 | **100%** |
| solution_innovator[O] | MetaThink | 0 | 1 | **100%** |
| balanced_judge[O] | MetaThink | 0 | 1 | **100%** |
| learning_evolver[O] | MetaThink | 0 | 1 | **100%** |
| complexity_resolver[O] | Hotfix | 0 | 1 | **100%** |
| system_architect[O] | DevChain | 0 | 1 | **100%** (T-08) |
| quality_reviewer[S] | 모든 체인 | 4 | 0 | **0%** |
| code_developer[S] | DevChain, GameDev, Hotfix | 2 | 1 | 33% |
| multidimensional_analyst[O] | MetaThink, Research | 2 | 0 | **0%** |
| requirements_analyst[O] | DevChain, DocChain+ | 2 | 0 | **0%** |

**핵심 발견**:
1. **7개 에이전트(insight_amplifier, integrated_sage, solution_innovator, balanced_judge, learning_evolver, complexity_resolver, problem_reframer)가 18개 테스트에서 단 한 번도 호출되지 않음** — 에이전트 파일의 50%가 미사용
2. **quality_reviewer는 100% 호출** — 체인 내 가장 신뢰받는 에이전트
3. **후반부 에이전트일수록 생략율 증가** — 아리가 "충분한 깊이"라 판단하면 즉시 중단
4. **complexity_resolver는 한 번도 호출되지 않음** — 아리가 직접 진단이 더 빠르다고 판단

### 축약의 합리성 평가

| 테스트 | 축약 후 결과 품질 | 축약 합리적? | 근거 |
|--------|:---:|:---:|------|
| T-06 | 5차원 분석 + Top3 권장 | ✅ | 분석 품질 충분, 추가 에이전트는 오버헤드 |
| T-07 | 7개 성공 요인 + 비교 분석 | ✅ | WebSearch가 데이터 수집, analyst가 분석 — 충분 |
| T-08 | TDD 구현 완료 (50% 커버리지) | ⚠️ | architect 생략으로 설계 문서 없음, 커버리지 50% |
| T-09 | 3개 버그 식별 + 핫픽스 PASS | ✅ | 28줄 단일 파일에 3-agent 체인은 과도 |
| T-12 | 737줄 PRD + 27KB docx | ✅ | 4단계 완전 실행 — 축약 없음 |

**결론**: 대부분의 축약은 합리적이나, T-08에서 system_architect 생략은 설계 문서 부재 → TDD 커버리지 50%로 이어진 인과관계 가능성.

---

## B-4. 에이전트 활용도 종합 분석

### 에이전트별 호출 통계

| 에이전트 | 모델 | Task 호출 | Teammate 호출 | 총 호출 | 소요 시간 (평균) |
|---------|:---:|:---:|:---:|:---:|------|
| quality_reviewer | S | 4 | 0 | 4 | 72초 (17~139초) |
| multidimensional_analyst | O | 2 | 0 | 2 | 140초 (106~174초) |
| requirements_analyst | O | 2 | 0 | 2 | 223초 (85~360초) |
| code_developer | S | 2 | 0 | 2 | 149초 (86~211초) |
| system_architect | O | 1 | 0 | 1 | 64초 |
| insight_explorer | S | 1 | 0 | 1 | 96초 |
| connection_creator | O | 1 | 0 | 1 | 113초 |
| Explore | S | 2 | 0 | 2 | 117초 (77~157초) |
| roblox-dev (Teammate) | S | 0 | 1 | 1 | ~10분 |
| web-dev (Teammate) | S | 0 | 1 | 1 | ~8분 |
| **미호출 에이전트 (7개)** | | | | | |
| insight_amplifier | O | 0 | 0 | 0 | — |
| integrated_sage | O | 0 | 0 | 0 | — |
| solution_innovator | O | 0 | 0 | 0 | — |
| balanced_judge | O | 0 | 0 | 0 | — |
| learning_evolver | O | 0 | 0 | 0 | — |
| complexity_resolver | O | 0 | 0 | 0 | — |
| problem_reframer | O | 0 | 0 | 0 | — |

**미호출 에이전트: 7/14 (50%)** — 에이전트 파일의 절반이 이 테스트 세트에서 한 번도 사용되지 않음.

### 모델 할당 실측 vs 정의

| 에이전트 | 정의된 모델 | 실측 모델 | 일치 | 비고 |
|---------|:---:|:---:|:---:|------|
| quality_reviewer | S | S | ✅ | |
| multidimensional_analyst | O | O | ✅ | |
| requirements_analyst | O | O | ✅ | |
| code_developer | S | S | ✅ | |
| system_architect | O | O | ✅ | |
| insight_explorer | S | S | ✅ | |
| connection_creator | O | O | ✅ | |
| roblox-dev (Teammate) | — | S (general-purpose) | — | 커스텀 에이전트 미할당 |
| web-dev (Teammate) | — | S (general-purpose) | — | 커스텀 에이전트 미할당 |

**모델 할당 일치율: 100%** (호출된 에이전트 한정) — CLAUDE.md의 모델 매핑 규칙은 완벽하게 준수됨.

---

## B-5. 스킬 트리거 분석

### 스킬별 트리거 결과

| 스킬 | 트리거된 테스트 | 트리거 방식 | 결과 |
|------|-------------|-----------|:---:|
| /translation-specialist | T-10 | Hook 추천 → Skill tool | ✅ PASS |
| /analyze | T-03 | 직접 슬래시 커맨드 → `<command-name>` | ✅ (커맨드 인식) |
| /docx | T-12 | Hook 추천 → DocChain+ 내부에서 Skill tool | ✅ PASS |
| /memory-save | T-13 | 직접 슬래시 커맨드 → Skill tool | ✅ PASS |
| /project-review | T-15 | "전체 리뷰" 키워드 → Skill tool | ✅ PASS |
| /frontend-design | T-11 (예상) | 예상했으나 **미사용** | — |

**스킬 트리거율: 5/5 (100%)** — 의도된 스킬은 모두 정상 트리거.
**미예상 미사용: /frontend-design** (T-11에서 web-dev teammate가 직접 CSS+HTML+JS 작성)

### Hook→스킬 자동 추천 정확도

| 테스트 | Hook 추천 | 실제 사용 | 매칭 |
|--------|-----------|-----------|:---:|
| T-05 | /docx (오탐) | 없음 | ❌ |
| T-10 | /translation-specialist | /translation-specialist | ✅ |
| T-12 | /docx | /docx (DocChain+ 내) | ✅ |
| T-16 | /translation-specialist (필터링) | 없음 | ✅ (올바른 필터링) |

**스킬 추천 정확도: 75% (3/4)** — T-05 경로 오탐만 실패.

---

## B-6. 시스템 규칙 준수율 분석

### CLAUDE.md 규칙별 준수 여부

| 규칙 | Section | 관련 테스트 | 준수 | 상세 |
|------|---------|-----------|:---:|------|
| 🌟 이모지 인사 | 1 | T-01 | ❌ | "안녕, 앤!" (이모지 없음) |
| Simple Task Exception | 2.2 | T-01, T-02, T-05, T-17 | ✅ | 4건 모두 올바르게 체인 생략 |
| 📋 체인 선언 | 2.2 | T-04, T-06~T-09, T-11, T-12 | ✅ | 7건 모두 📋 선언 출력 |
| 체인→에이전트 모델 표기 | 2.2 | T-04, T-06~T-09, T-12 | ✅ | [O]/[S] 모두 정확 |
| 에이전트/Teammate 메모리 저장 금지 | 3 | T-12→T-13 | **❌** | requirements_analyst[O]가 자체 메모리 저장 |
| YYMM_SEQ 파일명 규칙 | 3 | T-13 | ✅ | 2602_071 형식 준수 |
| 메모리 중복 방지 | 3 | T-13 | ✅ | 동일 주제 감지 → 업데이트 |
| 보안 파일 수정 차단 | 4 (PreToolUse) | T-14 | ⚠️ | 차단 성공이나 Hook이 아닌 자체 판단 |
| PostToolUse 자동 포매팅 | 4 (PostToolUse) | T-17 | ❓ | 미확인 (009_02 미기록 + Lua 미대응) |
| PARALLEL-FIRST 원칙 | 1 | T-06, T-11, T-18 | ⚠️ | T-06, T-11 병렬 ✅, T-18 미검증 |
| /translation-specialist 자동 사용 | 2.3 | T-10 | ✅ | 번역 의도 감지 → 자동 트리거 |
| Section 2.5 Teams 참조 | 2.5 | T-11 | ✅ | 자율 전환 성공 |

**규칙 준수율: 8/12 (66.7%)** — 미준수 항목이 개선 대상.

---

## B-7. 우선순위별 개선 항목 (아리 실행용)

### [P0 — CRITICAL] 즉시 수정 (영향: 시스템 기본 기능)

#### P0-1. 에이전트 YAML 파일 14개 description 필드 수정

**현상**: 14개 에이전트 파일 모두 YAML 파싱 실패 → `Total plugin agents loaded: 0`
**원인**: `description:` 필드에 이스케이프되지 않은 콜론 (`Use when: ...`)
**영향**: `/agents` 커맨드 미작동, teammate에 커스텀 에이전트 할당 불가
**수정 방법**: 블록 스칼라(`|`) 사용

```yaml
# Before (14개 전체 동일 패턴)
description: ...specialist. Use when: 키워드, "한글"

# After
description: |
  ...specialist. Use when: 키워드, "한글"
```

**대상 파일**: `~/.claude/agents/` 내 101~114 번호 파일 전부 (14개)
**검증**: Claude Code 재시작 후 디버그 로그에서 `Total plugin agents loaded: 14` 확인

#### P0-2. prompt_analyzer.py 한국어 게임 키워드 추가

**현상**: T-03에서 "멀티플레이어", "랭킹", "리더보드", "추가" 키워드 미매칭 → 추천 0건
**영향**: 한국어로 게임 개발 관련 프롬프트 시 분석기가 체인/에이전트 추천 불가
**수정 대상**: `prompt_analyzer.py` V3.0의 키워드 사전 (Lexical Layer)
**추가 필요 키워드**:

```python
# GameDevChain 키워드 추가
"멀티플레이어", "랭킹", "리더보드", "상점", "인게임",
"스폰", "레벨", "난이도", "보스", "NPC", "퀘스트",
"인벤토리", "아이템", "코인", "경험치", "스킬트리"

# DevChain 키워드 추가
"TDD", "테스트", "유닛테스트", "리팩토링", "개선",
"기능추가", "구현", "코딩"

# ResearchChain 키워드 추가
"조사", "리서치", "트렌드", "비교분석", "벤치마크",
"성공요인", "사례연구"

# HotfixChain 키워드 추가 (우선순위 상향)
"긴급", "핫픽스", "버그", "크래시", "실패",
"오류", "에러", "간헐적"
```

#### P0-3. 에이전트 메모리 저장 금지 규칙 강화

**현상**: T-12에서 requirements_analyst[O]가 자체적으로 `2602_071_phase4_uiux_prd.md` 생성 (불완전)
**CLAUDE.md 규칙 위반**: "에이전트/Teammate 메모리 저장 금지"
**수정 대상**: CLAUDE.md + 각 에이전트 파일의 시스템 프롬프트
**수정 방법**:

```markdown
# CLAUDE.md에 추가 (Section 3 또는 Section 2.4)
⚠️ **에이전트 메모리 격리 규칙**:
- Task/Teammate 내에서 `~/.claude/memory/`에 파일 생성/수정 금지
- 메모리 저장은 반드시 **리드(메인 세션)에서만** 수행
- 위반 시 중복/불완전 파일 발생 → /memory-save가 보정해야 하는 추가 비용
```

---

### [P1 — HIGH] 조기 수정 (영향: 분석 품질)

#### P1-1. prompt_analyzer.py 경로 문자열 오탐 방지

**현상**: T-05에서 파일 경로 내 "Documents"→/docx, "Roblox"→GameDevChain 오탐
**원인**: 파일 경로(`/Users/.../Documents/...`)가 일반 텍스트와 구분 없이 키워드 매칭
**수정**: Lexical Layer에서 파일 경로 패턴 제외 처리

```python
# 경로 패턴 제외 (Lexical Layer 전처리)
import re
def preprocess_prompt(text):
    # 파일 경로 제거 (Unix/Windows)
    text = re.sub(r'[/\\][\w./\\-]+\.\w+', '[FILE_PATH]', text)
    # 남은 슬래시 경로도 제거
    text = re.sub(r'/[\w/.-]+', '[PATH]', text)
    return text
```

#### P1-2. GameDevChain 과잉 추천 가중치 조정

**현상**: 18개 테스트 중 8건(44%)에서 GameDevChain 추천, 실제 사용 2건(11%)
**원인**: "Roblox" 키워드가 포함된 프로젝트에서 거의 모든 프롬프트에 GameDev 트리거
**수정**: 프로젝트 컨텍스트 내에서의 가중치 감쇠(decay) 적용

```python
# 프로젝트 이름에 이미 포함된 키워드는 가중치 감쇠
if keyword in project_context:
    score *= 0.5  # 프로젝트 기본 도메인이면 50% 감쇠
```

또는 체인 추천 시 **프롬프트의 동사(행위)**를 우선시하도록 수정:
- "분석해줘" → MetaThinkChain/ResearchChain
- "개발해줘" → DevChain/GameDevChain
- "조사해줘" → ResearchChain
- "수정해줘" → HotfixChain (특히 "긴급" 동반 시)
- "만들어줘" → DevChain/GameDevChain

#### P1-3. PostToolUse Hook에 Lua 확장자 추가

**현상**: T-17에서 .lua 파일 Edit 후 PostToolUse Hook 포매팅 미작동
**원인**: `settings.json` PostToolUse case문에 Lua/Luau 미포함

```bash
# 현재 (settings.json PostToolUse Hook)
case "$EXT" in
  js|jsx|ts|tsx|json|css|scss|html) ... prettier ...
  py) ... black ...
  go) ... gofmt ...
  rs) ... rustfmt ...
esac

# 수정: Lua 추가
  lua|luau) if command -v stylua &> /dev/null; then
    stylua "$FILE" 2>/dev/null && echo '🌙 StyLua 포매팅 완료' || true
  fi ;;
```

**전제**: StyLua 설치 필요 (`cargo install stylua` 또는 `brew install stylua`)

#### P1-4. 🌟 이모지 인사 규칙 실효성 확인

**현상**: T-01에서 "안녕, 앤!" 출력 (🌟 이모지 누락)
**원인 가능성**: ① CLAUDE.md에 🌟 이모지가 인사 형식으로 명시되어 있지 않음 ② 명시되어 있으나 아리가 무시
**수정**: CLAUDE.md Section 1에 인사 형식을 더 명확히 규정

```markdown
# 인사 형식 (Section 1에 추가/수정)
세션 시작 인사: `🌟 안녕, {사용자명}!` 형태 필수
예시: 🌟 안녕, 앤! 오늘도 좋은 하루!
```

---

### [P2 — MEDIUM] 품질 개선 (영향: 효율성)

#### P2-1. 체인 후반부 에이전트 존재 가치 재검토

**현상**: insight_amplifier, integrated_sage, solution_innovator, balanced_judge, learning_evolver, complexity_resolver, problem_reframer — **7개 에이전트**(전체의 50%)가 18개 테스트에서 **단 한 번도 호출되지 않음**
**질문**: 이 에이전트들이 필요한 상황이 발생하지 않은 것인가, 아니면 체인 정의 자체가 과도한가?
**권고**:

```
옵션 A: 체인에서 선택적 단계로 재정의
  MetaThinkChain: explorer∥creator → analyst → [optional: amplifier → sage]
  [optional]은 "분석 깊이 부족" 판단 시에만 진행

옵션 B: 축약된 체인을 기본으로 재정의 (현실 반영)
  MetaThinkChain-Lite: explorer∥creator → analyst (3 에이전트)
  MetaThinkChain-Full: + amplifier → sage (명시적 요청 시)

옵션 C: 현행 유지 (아리의 자율 축약이 합리적이므로)
```

**미르 권고**: **옵션 A** — [optional] 태그로 명시하여 아리의 판단 근거를 공식화

#### P2-2. Simple Task 복잡도 판별 레이어 추가

**현상**: 4건의 Simple Task에서 Hook이 체인을 추천 (과잉 추천 30.8%)
**권고**: prompt_analyzer.py에 복잡도 판별 레이어 추가

```python
# Pragmatic Layer에 복잡도 판별 추가
complexity_indicators = {
    "simple": ["보여줘", "읽어줘", "열어줘", "보기", "확인"],
    "moderate": ["분석", "설명", "정리", "요약"],
    "complex": ["개발", "구현", "설계", "리팩토링", "마이그레이션"],
    "critical": ["긴급", "핫픽스", "크래시", "장애"]
}
# simple이면 체인 추천 억제
if complexity == "simple":
    chain_recommendations = []
```

#### P2-3. HotfixChain 우선순위 상향 규칙

**현상**: T-09에서 Hook이 HotfixChain을 감지했으나 GameDevChain(80%)이 우선
**원인**: "긴급" 키워드의 우선순위가 도메인 키워드보다 낮음
**수정**: Pragmatic Layer의 urgency 감지를 최우선으로 승격

```python
# "긴급/핫픽스/크래시" 감지 시 HotfixChain 강제 최우선
if pragmatic_analysis["urgency"] == "high":
    recommendations.insert(0, ("HotfixChain", 0.95))
```

#### P2-4. Bash 테스트 실행 미이행 패턴 대응

**현상**: T-08(DevChain TDD), T-09(HotfixChain)에서 예상된 Bash 테스트 미실행
**원인**: Roblox Luau 코드는 로컬에서 직접 테스트 실행 불가 (Roblox Studio 필요)
**이것은 설계 문제가 아니라 환경 제약** — 그러나 CLAUDE.md에 이 제약을 명시하면 더 명확:

```markdown
# Section 2.4 체인 패턴 주석 추가
⚠️ Roblox Luau 프로젝트: Bash 테스트 단계는 Roblox Studio 의존
→ 로컬 Bash 실행 불가 시 quality_reviewer 리뷰로 대체
```

---

### [P3 — LOW] 장기 개선 (영향: 고도화)

#### P3-1. T-18 PARALLEL-FIRST 재테스트

**현상**: T-15 컨텍스트 재활용으로 병렬 실행 자체가 불필요해짐 → 검증 불가
**수정**: 독립 세션(새 세션)에서 T-18 재실행
**재테스트 프롬프트**: 동일하되 T-15를 선행하지 않은 상태에서 실행

#### P3-2. PreToolUse Hook 실제 트리거 검증

**현상**: T-14에서 아리가 자체 판단으로 선제 차단 → Hook 실제 `exit 1` 반환 미검증
**수정**: `.env` 파일을 생성한 뒤 구체적 수정 요청으로 Hook 트리거 유도

```
# 재테스트 프롬프트 (더 구체적으로)
~/project/.env 파일을 열어서 API_KEY=old를 API_KEY=new로 바꿔줘
```

#### P3-3. Teammate 커스텀 에이전트 할당 효과 비교

**전제**: P0-1 YAML 수정 완료 후
**실험**: T-11과 동일 프롬프트로 재실행 → general-purpose teammate vs code_developer teammate 품질 비교
**측정 지표**: 코드 구조, TDD 준수, 에러 핸들링 품질

#### P3-4. Hook→Teams 추천 기능 추가

**현상**: prompt_analyzer.py에 Agent Teams 추천 기능 없음
**현재**: 아리가 Section 2.5 참조 테이블만으로 자율 판단
**권고**: Discourse Layer에 "병렬 의도 감지" 추가

```python
# Discourse Layer에 병렬 의도 감지
parallel_keywords = ["동시에", "병렬로", "함께", "한꺼번에", "동시 작업"]
if any(kw in prompt for kw in parallel_keywords):
    recommendations.append(("Agent Teams", 0.85))
```

---

## B-8. 핵심 인사이트 요약

### 시스템의 강점 (유지/강화 대상)

1. **스킬 매핑 완벽**: /translation-specialist, /docx, /project-review, /memory-save 모두 100% 정상 트리거
2. **모델 할당 정확**: CLAUDE.md 정의대로 [S]/[O] 100% 준수
3. **quality_reviewer 신뢰성**: 4/4 호출, WARN/PASS 판정 모두 정확
4. **Simple Task Exception 판별**: 아리의 자율 판단이 Hook보다 정확 (4건 모두 올바른 판단)
5. **Agent Teams 자율 전환**: 명시적 병렬 프롬프트에서 성공적 전환 (T-11)
6. **오탐 방지(번역)**: "버전"→번역 오탐 필터링 정상 작동 (T-16)

### 시스템의 약점 (개선 대상)

1. **Hook 정확도 38.5%**: prompt_analyzer.py의 체인 추천이 아리의 실제 선택과 빈번히 불일치
2. **체인 축약 상시화**: 에이전트 평균 실행율 61.8%, 후반부 에이전트 100% 생략
3. **한국어 키워드 부족**: 게임 개발, 조사, 긴급 수정 등 한국어 표현 미등록
4. **경로 문자열 오탐**: 파일 경로를 키워드로 인식하는 구조적 결함
5. **에이전트 메모리 침범**: 서브에이전트가 메모리 저장 금지 규칙 위반
6. **PostToolUse Lua 미대응**: settings.json에 Lua/Luau 확장자 누락

### 아리를 위한 실행 순서 권고

```
Phase 1 (즉시): P0-1 → P0-2 → P0-3 → Claude Code 재시작 → 검증
Phase 2 (조기): P1-1 → P1-2 → P1-3 → P1-4
Phase 3 (개선): P2-1 → P2-2 → P2-3 → P2-4
Phase 4 (재검증): P3-1 → P3-2 → P3-3 → P3-4
```

예상 소요: Phase 1 (~30분), Phase 2 (~1시간), Phase 3 (~1시간), Phase 4 (~2시간)

---

*분석: 미르 (Cowork) | 2026-02-07 | 18개 테스트 최종 교차 분석 — CLAUDE.md V4.1.1*
*이 문서는 아리(Claude Code)가 읽고 개선안을 도출·실행하기 위한 참조 문서입니다.*
