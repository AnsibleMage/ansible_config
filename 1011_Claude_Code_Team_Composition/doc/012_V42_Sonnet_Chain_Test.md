# 012. V4.2 소넷 체인 시스템 검증 테스트

> **Version**: 1.2 | **작성**: 미르 (Cowork) | **실행**: 아리 (Claude Code Sonnet)
> **대상**: CLAUDE.md V4.2 + 011 개선안 | **프로젝트**: `ansible_config/7001_Dev Methodology/400_Rails8_Dev Methodology/Sample Project/ansiblemage_homepage`
> **프로젝트 타입**: Rails 8.0.4 + Hotwire/Turbo + Stimulus + Tailwind CSS
> **작성일**: 2026-02-08
> **목적**: V4.2 체인 시스템 + Teams 자율 전환 검증 (소넷 모델 중심)
> **V1.2 변경**: system_architect(13개 테스트별 재설계) + problem_reframer(7개 개선안) 통합. 프롬프트/예상결과를 실제 Rails 프로젝트 파일/기능 기반으로 재설계. 충돌 시 problem_reframer 우선.

---

## 프로젝트 구조 요약 (ansiblemage_homepage)

> 테스트 프롬프트가 참조하는 실제 파일 목록. 모든 경로는 `ansiblemage_homepage/` 루트 기준.

| 계층 | 파일 | 설명 | 참조 테스트 |
|------|------|------|-----------|
| **컨트롤러** | `app/controllers/posts_controller.rb` (21줄) | 블로그 목록/상세, `user_liked?` 메서드 (L14-19) | T-04, T-18 |
| | `app/controllers/pages_controller.rb` | 홈/About/Projects 정적 페이지 | T-18 |
| | `app/controllers/comments_controller.rb` | 댓글 CRUD + Turbo Stream | T-18 |
| | `app/controllers/likes_controller.rb` (58줄) | 좋아요 생성/삭제, `set_post` (L40-42), `find_user_like` (L51-56) | T-04, T-17, T-18 |
| | `app/controllers/sessions_controller.rb` | GitHub OAuth 세션 관리 | T-18 |
| | `app/controllers/admin/posts_controller.rb` | 관리자 글 CRUD | T-18 |
| **모델** | `app/models/post.rb` | Post(slug/published/likes_count), `published`/`recent` 스코프 | T-04 |
| | `app/models/user.rb` | User(GitHub OAuth) | - |
| | `app/models/comment.rb` | Comment(post_id/user_id/content) | - |
| | `app/models/like.rb` | Like(IP+User 이중 체계), 유니크 검증 | T-04 |
| **뷰 (pages)** | `app/views/pages/home.html.erb` | 히어로 + CTA + 최신글 3개 | T-06 |
| | `app/views/pages/about.html.erb` | 프로필 + 기술스택 | T-06 |
| | `app/views/pages/projects.html.erb` | GitHub 프로젝트 갤러리 | T-06 |
| **뷰 (posts)** | `app/views/posts/index.html.erb` | 블로그 카드 목록 | T-06, T-11 |
| | `app/views/posts/show.html.erb` | 상세 + 댓글 섹션(#comments) + 좋아요 | T-02, T-06, T-08 |
| | `app/views/posts/_post_card.html.erb` | 카드 파셜 | - |
| | `app/views/posts/_like_button.html.erb` | 좋아요 버튼 파셜 | - |
| | `app/views/posts/_like_count.html.erb` | 좋아요 카운트 파셜 | - |
| **뷰 (comments)** | `app/views/comments/_comment.html.erb` | 댓글 개별 파셜 | T-08 |
| | `app/views/comments/_form.html.erb` | 댓글 입력 폼 | T-08 |
| | `app/views/comments/create.turbo_stream.erb` | Turbo Stream 생성 | - |
| | `app/views/comments/destroy.turbo_stream.erb` | Turbo Stream 삭제 | - |
| **뷰 (admin)** | `app/views/admin/posts/index.html.erb` | 관리자 글 목록 | - |
| | `app/views/admin/posts/new.html.erb`, `edit.html.erb`, `_form.html.erb` | 관리자 글 작성/편집 | - |
| **뷰 (shared)** | `app/views/shared/_navbar.html.erb` | 네비게이션 바 | T-11 |
| | `app/views/shared/_footer.html.erb` | 푸터 | - |
| | `app/views/shared/_pixel_mage.html.erb`, `_pixel_mage_large.html.erb` | 픽셀 캐릭터 | - |
| **Stimulus** | `app/javascript/controllers/flash_controller.js` | 플래시 메시지 자동 닫기 | T-08 |
| | `app/javascript/controllers/mobile_menu_controller.js` (33줄) | 모바일 메뉴 토글, `static targets = ["menu", "openIcon", "closeIcon"]`, `toggle()` L10 | T-09 |
| **헬퍼** | `app/helpers/markdown_helper.rb` (54줄) | `PixelCodeRenderer` + `PixelTheme` (Redcarpet + Rouge) | T-05 |
| **라우트** | `config/routes.rb` (25줄) | `root → pages#home`, `resources :posts → :likes, :comments`, `namespace :admin` | - |
| **문서** | `doc/PRD.md` | M1~M4 마일스톤, US-01~US-07 사용자 스토리 | T-13 |
| | `doc/TaskPlan.md` | 작업 계획서 | - |

---

## 테스트 배경

### V4.1.1 → V4.2 주요 개선사항

| 개선 | 내용 | 검증 테스트 |
|------|------|-----------|
| **Q1. Hook = 촉매** | Hook 추천 불일치 시 아리 판단 우선, 근거 1줄 출력 | T-02, T-04, T-09 |
| **Q2. 임의 축약 금지** | 체인 선택 후 정의된 모든 에이전트 순서대로 실행 | T-04, T-06, T-07, T-08 |
| **Q3. Teams 자율 전환** | 병렬 의도 감지 → Teams 모드 자동 평가 | T-07, T-11 |
| **Q4. prompt_analyzer V4.0** | 한국어 키워드 ~40개, 동사 우선, Simple Task 판별, HotfixChain 긴급 승격 | T-03, T-05, T-09 |
| **Q5. 즉시 수정** | YAML 블록 스칼라, PostToolUse Lua, 에이전트 메모리 격리 | T-13, T-17 |

### 소넷 모델 특성

| 항목 | 특성 | 테스트 초점 |
|------|------|-----------|
| **모델** | Sonnet 4.5 (claude-sonnet-4-5-20250929) | 체인 에이전트 활용이 핵심 |
| **속도** | Opus보다 2~3배 빠름 | 체인 전체 실행 시간 관찰 |
| **비용** | Opus의 1/5 수준 | 에이전트 수 vs 품질 트레이드오프 |
| **강점** | 일반 개발, 빠른 반복 | DevChain, WebDevChain+, HotfixChain |
| **약점** | 고도의 추론, 전략 설계 | MetaThinkChain, SystemDesignChain 품질 관찰 |

**핵심**: 소넷은 에이전트를 더 적극적으로 활용해야 함 → **체인 축약 금지(Q2)가 더 중요**

---

## 테스트 방법

1. **블라인드 테스트**: 아리에게 이 문서를 보여주지 않음
2. **사용자(앤) 프롬프트 입력**: 각 테스트 프롬프트를 자연스럽게 입력
3. **아리 자연 응답**: CLAUDE.md V4.2 규칙에 따라 응답
4. **결과 기록**: 009_02 형식으로 `013_V42_Sonnet_Test_Results.md`에 사실 그대로 기록
5. **비교 분석**: 예상치(이 문서) vs 실측치(013) GAP 분석

---

## 결과 기입 규칙

각 테스트의 결과를 아래 항목에 맞춰 빠짐없이 기록:

| 기록 항목 | 설명 |
|-----------|------|
| **입력 프롬프트** | 사용자가 입력한 정확한 프롬프트 |
| **Hook 반응** | auto-analyze.sh / prompt_analyzer.py 실행 여부 및 출력 내용 |
| **체인 선택** | 선택된 체인명 (없으면 "없음") + Hook 불일치 시 근거 1줄 |
| **체인 선언** | 선언 출력 여부 및 내용 |
| **사용된 에이전트** | subagent_type 목록 + 각 모델 (S/O) + 소요 시간(초) |
| **사용된 스킬** | 트리거된 / command 목록 (없으면 "없음") |
| **사용된 도구** | Read, Write, Edit, Bash, WebSearch, Context7, Grep, Glob 등 |
| **Teams 활성화** | 예/아니오 + 전환 이유 (병렬 의도, 독립 작업, 듀얼 트랙 등) |
| **Teammate 구성** | teammate 타입, 모델, 역할, TaskCreate 수, 소요 시간 |
| **Hook 후처리** | PostToolUse, PreToolUse Hook 동작 여부 및 내용 |
| **최종 출력** | 응답의 핵심 내용 요약 (3줄 이내) |
| **특이사항** | 오류, 경고, 예상 외 동작, 체인 축약 발생 여부 |

---

## 테스트 상태 범례

| 상태 | 의미 |
|------|------|
| ⬜ | 미실행 |
| ✅ | PASS (예상과 완전 일치) |
| ⚠️ | PARTIAL (일부 동작, GAP 존재) |
| ❌ | FAIL (핵심 기능 미작동) |

---

## Phase 1: 기본 동작 검증

### T-01. Identity & Session Greeting

| 항목 | 내용 |
|------|------|
| **테스트 대상** | Section 1 - Identity 인사 형식 |
| **V4.1.1 결과** | ⚠️ -- "안녕, 앤!" 출력, 이모지 누락 |
| **V4.2 개선** | 없음 (문서 형식 명확화만) |
| **기존 프롬프트** | `안녕` |
| **새 프롬프트** | `안녕` |
| **변경사항** | 변경 없음 -- 프로젝트 무관 테스트 |
| **예상 결과** | 인사 형태 응답, Hook 10자 미만 생략, 체인 없음 |
| **검증 포인트** | (1) 인사 이모지 포함 여부 (2) Hook 생략 조건 정상 작동 |
| **상태** | ⬜ |

---

### T-02. Hook = 촉매 역할 (Q1 검증)

| 항목             | 내용                                                                                             |
| -------------- | ---------------------------------------------------------------------------------------------- |
| **테스트 대상**     | Section 2.2 - Hook 의사결정 프로세스                                                                   |
| **V4.1.1 결과**  | ⚠️ -- Hook 추천 무시, 근거 미명시                                                                       |
| **V4.2 개선**    | Hook 불일치 시 **아리 판단 우선 + 불일치 사유 1줄 출력** 명시                                                      |
| **기존 프롬프트**    | `AnsibleMage 웹사이트의 app/views/pages/home.html.erb 뷰 구조를 분석해줘`                                   |
| **새 프롬프트**     | `posts/show.html.erb의 댓글 섹션 레이아웃 구조를 분석해줘`                                                     |
| **변경 근거**      | 실제 존재하는 `posts/show.html.erb`에 댓글 섹션(#comments)이 구현되어 있어, 단순 구조 분석으로 Simple Task 판별을 테스트하기에 적합 |
| **예상 Hook 추천** | WebDevChain+ (80%), DevChain (70%)                                                             |
| **예상 결과**      | 체인 없음 (Simple Task) + **불일치 근거 1줄**: "단순 뷰 구조 분석으로 체인 불필요"                                     |
| **검증 포인트**     | (1) Hook 추천 발생 (2) 아리가 다른 판단 시 **근거 1줄 명시** (3) Simple Task 판별 정상                              |
| **상태**         | ⬜                                                                                              |

---

### T-03. 한국어 키워드 매칭 (Q4-1 검증)

| 항목            | 내용                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **테스트 대상**    | prompt_analyzer.py V4.0 한국어 키워드 ~40개 추가                                                                                        |
| **V4.1.1 결과** | ❌ -- "멀티플레이어", "랭킹", "리더보드" 미감지, 추천 0건                                                                                         |
| **V4.2 개선**   | 웹 키워드 추가: "피드백", "수집", "폼", "입력", "제출", "모달" 등                                                                                 |
| **기존 프롬프트**   | `/analyze AnsibleMage 블로그에 독자 피드백 수집 폼을 추가하고 싶어`                                                                               |
| **새 프롬프트**    | `/analyze 블로그 글 상세 페이지에 독자 피드백 수집 모달 폼을 추가하고 싶어`                                                                               |
| **변경 근거**     | "블로그 글 상세 페이지" = `posts/show.html.erb`, "모달 폼" = Stimulus + Turbo Stream 조합. "피드백", "수집", "모달", "폼" 한국어 키워드 4개 동시 포함으로 매칭률 극대화 |
| **예상 결과**     | WebDevChain+ (70%+) 또는 DevChain (70%), code_developer (70%) 감지                                                                 |
| **검증 포인트**    | (1) 한국어 키워드 매칭 성공 (2) 체인 추천 신뢰도 0.6 이상 (3) /analyze 정상 실행                                                                      |
| **상태**        | ⬜                                                                                                                              |

---

### T-05. 파일 경로 오탐 방지 (Q4-2 검증)

| 항목            | 내용                                                                                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | prompt_analyzer.py V4.0 파일 경로 전처리                                                                                                                                                           |
| **V4.1.1 결과** | ⚠️ -- "Documents" → /docx 오탐, "Roblox" → GameDevChain 오탐                                                                                                                                    |
| **V4.2 개선**   | 파일 경로 `[PATH]` 전처리, 키워드 매칭 제외                                                                                                                                                               |
| **기존 프롬프트**   | `app/controllers/posts_controller.rb 보여줘`                                                                                                                                                   |
| **새 프롬프트**    | `app/helpers/markdown_helper.rb 보여줘`                                                                                                                                                        |
| **변경 근거**     | `markdown_helper.rb`는 실제 존재하는 파일(54줄)로 Redcarpet + Rouge 커스텀 렌더러(`PixelCodeRenderer` + `PixelTheme`)를 포함. "markdown"이 포함되어 있어 DocChain+ 오탐 가능성을 추가로 검증 가능. 파일 경로 내 키워드가 체인 추천에 영향을 주지 않아야 함 |
| **예상 결과**     | Hook 추천 없음 또는 최소화, Simple Task Exception 정상, Read 직접 실행                                                                                                                                     |
| **검증 포인트**    | (1) "markdown" 경로 문자열 오탐 방지 (2) /docx, DocChain+ 미추천 (3) 파일 읽기 성공                                                                                                                           |
| **상태**        | ⬜                                                                                                                                                                                           |

---

## Phase 2: 체인 축약 금지 검증 (Q2 핵심)

### T-04. DevChain 전체 실행 (Q2 검증)

| 항목            | 내용                                                                                                                                                                                                                                                                                                 |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | Section 2.4 - 임의 축약 금지 원칙                                                                                                                                                                                                                                                                          |
| **V4.1.1 결과** | ⚠️ -- 3/3 에이전트 실행 (100%), 하지만 solution_innovator/integrated_sage 미사용                                                                                                                                                                                                                               |
| **V4.2 개선**   | **"충분하다"는 자의적 판단으로 후반부 생략 금지** 명시                                                                                                                                                                                                                                                                  |
| **기존 프롬프트**   | `AnsibleMage 블로그의 posts_controller.rb에서 중복된 로직을 helper로 리팩토링해줘`                                                                                                                                                                                                                                    |
| **새 프롬프트**    | `posts_controller.rb와 likes_controller.rb에서 중복되는 set_post, user_liked?/find_user_like 로직을 concern으로 리팩토링해줘`                                                                                                                                                                                        |
| **변경 근거**     | `posts_controller.rb` L7(`Post.find_by!(slug: params[:id])`)와 `likes_controller.rb` L41(`Post.find_by!(slug: params[:post_id])`)에 실제 동일한 slug 기반 Post 조회 로직이 중복. `user_liked?`(posts L14-19)와 `find_user_like`(likes L51-56)도 유사한 IP/User 이중 판별 로직. ActiveSupport::Concern으로의 추출이 자연스러운 실제 리팩토링 과제 |
| **예상 체인**     | DevChain                                                                                                                                                                                                                                                                                           |
| **예상 에이전트**   | requirements_analyst[O] → (system_architect[O] ∥ Explore[S] ∥ Context7[∥]) → code_developer[S] → (quality_reviewer[S] ∥ Bash[테스트][-])                                                                                                                                                              |
| **검증 포인트**    | (1) **requirements_analyst 포함** (V4.1.1에서 생략됨) (2) 4개 전체 순차 실행 (3) 축약 없음                                                                                                                                                                                                                           |
| **상태**        | ⬜                                                                                                                                                                                                                                                                                                  |

---

### T-06. MetaThinkChain 전체 실행 (Q2 핵심)

| 항목            | 내용                                                                                                                                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | Section 2.4 - MetaThinkChain 8단계 전체 실행                                                                                                                                                                            |
| **V4.1.1 결과** | ⚠️ -- 8개 중 3개만 실행 (37.5%)                                                                                                                                                                                         |
| **V4.2 개선**   | **체인 축소가 필요하면 앤이 체인 정의 자체를 수정** -- 아리는 선택한 체인의 단계를 생략할 권한 없음                                                                                                                                                      |
| **기존 프롬프트**   | `AnsibleMage 웹사이트의 5개 주요 페이지 UI/UX가 사용자 체류 시간에 미치는 영향을 심층 분석해줘`                                                                                                                                                   |
| **새 프롬프트**    | `AnsibleMage 홈페이지의 home, about, projects, posts/index, posts/show 5개 페이지가 방문자 체류 시간과 재방문율에 미치는 UX 요인을 심층 분석해줘`                                                                                                    |
| **변경 근거**     | 5개 페이지를 실제 파일명으로 특정함. `home.html.erb`(히어로+CTA+최신글), `about.html.erb`(프로필+기술스택), `projects.html.erb`(GitHub 갤러리), `posts/index.html.erb`(블로그 목록), `posts/show.html.erb`(상세+댓글+좋아요). 각 페이지의 실제 UI 구성요소가 UX 분석 대상이 됨 |
| **예상 체인**     | MetaThinkChain                                                                                                                                                                                                    |
| **예상 에이전트**   | (insight_explorer[S] ∥ connection_creator[O]) → (multidimensional_analyst[O] ∥ learning_evolver[O]) → solution_innovator[O] → balanced_judge[O] → insight_amplifier[O] → integrated_sage[O]                       |
| **검증 포인트**    | (1) **8개 에이전트 전체 실행** (V4.1.1: 3개만) (2) 병렬 구간 (explorer ∥ creator, analyst ∥ evolver) (3) 모델 할당 정확 (S/O) (4) 축약 없음                                                                                                |
| **Sonnet 고려** | 8개 전체 실행 시 ~15~20분 소요 예상, learning_evolver/solution_innovator/insight_amplifier 품질 관찰                                                                                                                             |
| **상태**        | ⬜                                                                                                                                                                                                                 |

---

### T-07. ResearchChain 전체 실행 + Teams 전환 (Q2 + Q3)

| 항목               | 내용                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **테스트 대상**       | ResearchChain 4단계 전체 실행 + Teams 적합성 평가                                                                                                                             |
| **V4.1.1 결과**    | ⚠️ -- 4개 중 1개만 실행 (25%), Teams 미사용                                                                                                                                 |
| **V4.2 개선**      | (1) 4개 전체 실행 (2) **Teams 자동 평가 분기** (병렬 의도 감지)                                                                                                                     |
| **기존 프롬프트**      | `Claude AI 도구 소개 웹사이트 중 인기 Top 10의 공통 성공 요인을 조사해줘`                                                                                                                 |
| **새 프롬프트**       | `Rails 8 + Hotwire 기반 개인 블로그 사이트 중 성공 사례 Top 10의 공통 UX 패턴과 기술 스택을 조사해줘`                                                                                            |
| **변경 근거**        | ansiblemage_homepage가 Rails 8 + Hotwire 블로그이므로, 동일 기술 스택의 성공 사례 조사는 프로젝트에 직접 적용 가능한 현실적 리서치 과제. Turbo Stream, Stimulus, Tailwind CSS 등 실제 사용 중인 기술과의 비교 분석이 자연스러움  |
| **예상 체인**        | ResearchChain                                                                                                                                                      |
| **예상 에이전트**      | (WebSearch[∥] ∥ Context7[∥] ∥ Explore[S]) → (multidimensional_analyst[O] ∥ insight_explorer[S]) → insight_amplifier[O] → integrated_sage[O] → Write[-] or /docx[-] |
| **Teams 전환 가능성** | 독립 병렬 가능 (Top 10 사이트 개별 조사) → Teammate x3~5 (각 사이트별 researcher)                                                                                                    |
| **검증 포인트**       | (1) **4개 에이전트 전체 실행** (V4.1.1: 1개만) (2) Teams 전환 여부 (병렬 의도 약함 → Chain 유지가 적절) (3) WebSearch 병렬 실행 (4) insight_amplifier/integrated_sage 포함                         |
| **상태**           | ⬜                                                                                                                                                                  |

---

### T-08. DevChain system_architect 포함 (Q2 검증)

| 항목            | 내용                                                                                                                                                                                                                                                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | DevChain 4단계 전체 실행 (architect 포함)                                                                                                                                                                                                                                                                                          |
| **V4.1.1 결과** | ⚠️ -- 4개 중 3개 실행 (75%), system_architect 생략                                                                                                                                                                                                                                                                                |
| **V4.2 개선**   | **정의된 모든 에이전트 순서대로 실행** -- architect 생략 금지                                                                                                                                                                                                                                                                                 |
| **기존 프롬프트**   | `AnsibleMage 웹사이트에 다크모드 전환 기능을 Stimulus controller로 TDD 개발해줘`                                                                                                                                                                                                                                                              |
| **새 프롬프트**    | `posts/show.html.erb에 Stimulus controller로 댓글 실시간 미리보기 기능을 TDD 개발해줘`                                                                                                                                                                                                                                                       |
| **변경 근거**     | `posts/show.html.erb`에 이미 댓글 폼(`comments/_form.html.erb`)이 존재하고, Stimulus 패턴(`flash_controller.js`, `mobile_menu_controller.js`)도 프로젝트에 확립됨. 새 `comment_preview_controller.js`를 Stimulus + Markdown 렌더링 조합으로 TDD 개발하는 것은 실제 필요한 기능이면서 아키텍처 설계(마크다운 파싱 클라이언트 vs 서버, Turbo Stream 연동 방식)가 필요하여 system_architect 포함을 검증하기에 적합 |
| **예상 체인**     | DevChain                                                                                                                                                                                                                                                                                                                   |
| **예상 에이전트**   | requirements_analyst[O] → **system_architect[O]** → code_developer[S] → (quality_reviewer[S] ∥ Bash[테스트][-])                                                                                                                                                                                                               |
| **검증 포인트**    | (1) **system_architect[O] 포함** (V4.1.1에서 생략됨) (2) 4개 전체 순차 실행 (3) TDD 순서 준수 (요구 → 설계 → 개발 → 리뷰)                                                                                                                                                                                                                            |
| **상태**        | ⬜                                                                                                                                                                                                                                                                                                                          |

---

### T-09. HotfixChain 긴급 우선순위 (Q4-5 검증)

| 항목 | 내용 |
|------|------|
| **테스트 대상** | prompt_analyzer.py V4.0 HotfixChain 긴급 우선순위 (urgency=high → 0.95 강제 승격) |
| **V4.1.1 결과** | ⚠️ -- Hook → GameDevChain(80%) 추천, 아리가 HotfixChain 재선택 |
| **V4.2 개선** | **"긴급" 키워드 감지 시 HotfixChain 0.95 강제 승격** → 다른 체인 우선순위 억제 |
| **기존 프롬프트** | `mobile_menu_controller.js에서 메뉴 토글이 간헐적으로 실패해 긴급 수정해줘` |
| **새 프롬프트** | `mobile_menu_controller.js의 toggle() 메서드에서 menuTarget이 null로 간헐적 에러 발생, 긴급 수정해줘` |
| **변경 근거** | `mobile_menu_controller.js`의 실제 코드에서 `this.menuTarget`은 Stimulus target으로 `static targets = ["menu", "openIcon", "closeIcon"]`(L4)에 정의됨. `toggle()`(L10)에서 `this.menuTarget.classList`를 직접 접근하므로, DOM 타이밍 이슈로 target이 undefined가 되는 것은 Stimulus에서 실제 발생 가능한 버그. 구체적 메서드명과 에러 증상을 명시하여 자연스러운 긴급 수정 요청 |
| **예상 Hook 추천** | **HotfixChain (95%)** (V4.1.1: WebDevChain+ 80%) |
| **예상 체인** | HotfixChain |
| **예상 에이전트** | (complexity_resolver[O] ∥ Explore[S] ∥ Grep[-]) → code_developer[S] → (Bash[테스트][-] ∥ quality_reviewer[S]) |
| **검증 포인트** | (1) Hook이 **HotfixChain 최우선 추천** (2) complexity_resolver[O] 실행 (V4.1.1 생략됨) (3) Bash 테스트 실행 |
| **Sonnet 고려** | 단일 컴포넌트 버그라면 complexity_resolver 생략이 더 빠를 수 있음 -- 작은 파일(33줄)에 에이전트 과도 여부 관찰 |
| **상태** | ⬜ |

---

## Phase 3: Teams 자율 전환 검증 (Q3)

### T-11. WebDevChain+ 듀얼 트랙 Teams 전환 (Q3 검증)

| 항목              | 내용                                                                                                                                                                                                                                 |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**      | Section 2.2 - Teams 모드 자율 전환                                                                                                                                                                                                       |
| **V4.1.1 결과**   | ✅ -- Teams 최초 실전 성공 (roblox-dev + web-dev)                                                                                                                                                                                         |
| **V4.2 개선**     | **Section 2.2 Teams 분기 명시화**: "Teams 적합 체인이면서 독립 병렬 가능한 2+ 작업 → Teams 전환"                                                                                                                                                          |
| **기존 프롬프트**     | `AnsibleMage에 프로젝트 갤러리 페이지와 About 상세 페이지를 동시에 만들어줘`                                                                                                                                                                                |
| **새 프롬프트**      | `블로그에 태그 필터링 기능과 검색 기능을 동시에 개발해줘. 태그는 posts/index에, 검색은 navbar에 추가`                                                                                                                                                                |
| **변경 근거**       | `posts/index.html.erb`에 태그 필터링 추가와 `shared/_navbar.html.erb`에 검색 기능 추가는 완전히 독립적인 작업. 태그 필터링은 Post 모델에 tags 컬럼 + 뷰 필터 UI, 검색은 Stimulus controller + Turbo Frame 구성이 필요. "동시에" 키워드로 병렬 의도 명시. 두 작업이 서로 다른 파일을 건드리므로 Teams 듀얼 트랙에 이상적 |
| **예상 체인**       | WebDevChain+ (Teams 모드)                                                                                                                                                                                                            |
| **예상 Teams 구성** | Plan Mode → Explore[S] → TeamCreate: tag-filter-dev[S] + search-dev[S] → TaskCreate xN → quality_reviewer (Lead 직접)                                                                                                                |
| **검증 포인트**      | (1) "동시에" 키워드 감지 → Teams 전환 (2) 듀얼 트랙 병렬 (태그 필터링 + 검색) (3) teammate 모델: sonnet (4) Lead가 quality_reviewer 직접 수행                                                                                                                    |
| **Sonnet 고려**   | Plan Mode 품질 (sonnet lead), teammate 작업 품질 (sonnet), 총 소요 시간                                                                                                                                                                       |
| **상태**          | ⬜                                                                                                                                                                                                                                  |

---

## Phase 4: 시스템 보호 검증

### T-13. 에이전트 메모리 격리 (Q5-3 검증)

| 항목            | 내용                                                                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | Section 3 - 에이전트/Teammate 메모리 격리 규칙                                                                                                                                                               |
| **V4.1.1 결과** | ⚠️ -- requirements_analyst[O]가 자체 메모리 저장 (위반)                                                                                                                                                     |
| **V4.2 개선**   | **에이전트 시스템 프롬프트에 메모리 금지 규칙 추가**: "Task/Teammate 내에서 `~/.claude/memory/` 생성/수정 절대 금지"                                                                                                              |
| **기존 프롬프트**   | `AnsibleMage 웹사이트 Phase 2 기획서를 Word 문서로 만들어줘`                                                                                                                                                     |
| **새 프롬프트**    | `ansiblemage_homepage Phase 2 기획서를 Word 문서로 만들어줘. Phase 2는 PRD.md의 M3(상호작용) + M4(완성) 마일스톤 기반`                                                                                                     |
| **변경 근거**     | `doc/PRD.md`에 실제 정의된 마일스톤 M3(좋아요+OAuth+댓글, L440-443)과 M4(Projects+Admin+애니메이션+배포, L445-449)를 참조. 실제 존재하는 기획 문서를 기반으로 Word 생성 요청이므로 requirements_analyst가 PRD.md를 읽고 분석하는 과정에서 메모리 격리 규칙 준수 여부를 검증 |
| **예상 체인**     | DocChain+ [Solo]                                                                                                                                                                                  |
| **예상 에이전트**   | requirements_analyst[O] → /docx[-] → quality_reviewer[S]                                                                                                                                          |
| **검증 포인트**    | (1) requirements_analyst[O] 메모리 저장 **하지 않음** (2) /memory-save 수동 실행 시에만 저장 (3) 중복 방지 정상 작동                                                                                                        |
| **상태**        | ⬜                                                                                                                                                                                                 |

---

### T-17. PostToolUse Hook Ruby 포매팅 (Q5-2 검증)

| 항목            | 내용                                                                                                                                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **테스트 대상**    | PostToolUse Hook에 Ruby 포매팅 (settings.json case문)                                                                                                                                                                                |
| **V4.1.1 결과** | ⚠️ -- Lua 파일 편집 후 PostToolUse 미트리거 (case문에 lua 없음)                                                                                                                                                                              |
| **V4.2 개선**   | **settings.json PostToolUse case문에 Ruby 포함**                                                                                                                                                                                    |
| **기존 프롬프트**   | `AnsibleMage의 comments_controller.rb 파일에 주석을 추가해줘`                                                                                                                                                                              |
| **새 프롬프트**    | `likes_controller.rb의 find_user_like 메서드에 각 분기별 설명 주석을 추가해줘`                                                                                                                                                                    |
| **변경 근거**     | `likes_controller.rb`의 `find_user_like` 메서드(L51-56)는 `current_user` 존재 여부에 따라 User 기반(L53) 또는 IP 기반(L55)으로 Like를 조회하는 2개 분기를 가짐. 각 분기에 주석을 추가하는 것은 단순 Edit 작업으로, PostToolUse Hook 트리거 여부를 순수하게 검증 가능. 실제 코드 위치가 명확하여 편집 대상이 확실함 |
| **예상 결과**     | Edit 완료 → PostToolUse Hook 트리거 → RuboCop 포매팅 시도 (미설치면 스킵) → `[완료 알림]` 출력                                                                                                                                                        |
| **검증 포인트**    | (1) PostToolUse Hook 트리거 확인 (2) RuboCop 실행 여부 (미설치 가능성) (3) 완료 알림 출력                                                                                                                                                            |
| **상태**        | ⬜                                                                                                                                                                                                                               |

---

## Phase 5: PARALLEL-FIRST 검증 (독립 세션)

### T-18. PARALLEL-FIRST 병렬 실행 (독립 세션)

| 항목            | 내용                                                                                                                                                                                                                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **테스트 대상**    | Section 1 - PARALLEL-FIRST Principle                                                                                                                                                                                                                                                                         |
| **V4.1.1 결과** | ⚠️ -- T-15 컨텍스트 재활용으로 병렬 검증 불가 (설계 문제)                                                                                                                                                                                                                                                                       |
| **V4.2 개선**   | 없음 (테스트 설계 개선 필요)                                                                                                                                                                                                                                                                                            |
| **기존 프롬프트**   | `AnsibleMage의 모든 ERB 뷰 파일을 분석하고 각 파일별 개선점을 도출해줘`                                                                                                                                                                                                                                                             |
| **새 프롬프트**    | `ansiblemage_homepage의 6개 컨트롤러 파일을 각각 분석하고 파일별 코드 품질 개선점을 도출해줘`                                                                                                                                                                                                                                              |
| **변경 근거**     | 6개 컨트롤러(`posts_controller.rb`, `pages_controller.rb`, `comments_controller.rb`, `likes_controller.rb`, `sessions_controller.rb`, `admin/posts_controller.rb`)는 서로 독립적인 파일이므로 병렬 분석이 가능. ERB 뷰 파일보다 컨트롤러가 개수가 적고(6개) 각 파일의 역할이 명확하여 병렬 Task 분배를 검증하기에 더 적합. 각 파일의 코드 품질(N+1 쿼리, 인증 처리, 에러 핸들링 등)을 독립적으로 분석 가능 |
| **예상 결과**     | (1) 의존성 분석 → 독립 작업 식별 (2) 다수 Task 병렬 호출 (파일별 분석) (3) 결과 통합 순차                                                                                                                                                                                                                                                |
| **검증 포인트**    | (1) **Task 병렬 호출 확인** (V4.1.1: 컨텍스트 재활용으로 0건) (2) 독립 세션에서 실행 (3) 병렬 구간 명확                                                                                                                                                                                                                                    |
| **주의**        | **독립 세션에서 실행** -- 이전 테스트 컨텍스트 없이 새 세션 시작                                                                                                                                                                                                                                                                     |
| **상태**        | ⬜                                                                                                                                                                                                                                                                                                            |

---

## 실행 순서 (권장)

```
Phase 1 (기본 동작): T-01, T-02, T-03, T-05
Phase 2 (체인 축약 금지): T-04, T-06, T-07, T-08, T-09  <- **소넷 핵심**
Phase 3 (Teams 전환): T-11
Phase 4 (시스템 보호): T-13, T-17
Phase 5 (독립): T-18 (새 세션)
```

**총 테스트**: 13개 (V4.1.1 18개 → 통과 5개 제외)

---

## 변경 추적표 (V1.1 → V1.2)

| 테스트 | V1.1 프롬프트 (기존) | V1.2 프롬프트 (신규) | 변경 유형 | 변경 근거 요약 |
|--------|---------------------|---------------------|----------|--------------|
| T-01 | `안녕` | `안녕` | 변경 없음 | 프로젝트 무관 테스트 |
| T-02 | `...home.html.erb 뷰 구조를 분석해줘` | `posts/show.html.erb의 댓글 섹션 레이아웃 구조를 분석해줘` | 파일 특정 + 범위 구체화 | show.html.erb에 실제 댓글 섹션 존재, Simple Task 판별 강화 |
| T-03 | `...블로그에 독자 피드백 수집 폼을 추가하고 싶어` | `블로그 글 상세 페이지에 독자 피드백 수집 모달 폼을 추가하고 싶어` | "모달" 키워드 추가 | "피드백"+"수집"+"모달"+"폼" 4개 한국어 키워드 동시 매칭 |
| T-04 | `...posts_controller.rb에서 중복된 로직을 helper로 리팩토링해줘` | `posts_controller.rb와 likes_controller.rb에서 중복되는 set_post, user_liked?/find_user_like 로직을 concern으로 리팩토링해줘` | 실제 중복 로직 특정 | L7/L41 slug 조회 중복, L14-19/L51-56 IP/User 판별 중복 확인됨 |
| T-05 | `app/controllers/posts_controller.rb 보여줘` | `app/helpers/markdown_helper.rb 보여줘` | "markdown" 오탐 검증 강화 | PixelCodeRenderer+PixelTheme 포함, DocChain+ 오탐 유발 가능 |
| T-06 | `...5개 주요 페이지 UI/UX가 사용자 체류 시간에 미치는 영향을 심층 분석해줘` | `...home, about, projects, posts/index, posts/show 5개 페이지가 방문자 체류 시간과 재방문율에 미치는 UX 요인을 심층 분석해줘` | 5개 페이지 실제 파일명으로 특정 | 실제 ERB 파일과 1:1 매칭, UI 구성요소 분석 가능 |
| T-07 | `Claude AI 도구 소개 웹사이트 중 인기 Top 10의 공통 성공 요인을 조사해줘` | `Rails 8 + Hotwire 기반 개인 블로그 사이트 중 성공 사례 Top 10의 공통 UX 패턴과 기술 스택을 조사해줘` | 프로젝트 기술 스택 맞춤 | 동일 스택(Rails 8+Hotwire+Tailwind) 비교 분석 가능 |
| T-08 | `...다크모드 전환 기능을 Stimulus controller로 TDD 개발해줘` | `posts/show.html.erb에 Stimulus controller로 댓글 실시간 미리보기 기능을 TDD 개발해줘` | 기존 Stimulus 패턴 활용 | 댓글 폼+Stimulus 패턴 존재, 마크다운 파싱 아키텍처 결정 필요 |
| T-09 | `mobile_menu_controller.js에서 메뉴 토글이 간헐적으로 실패해 긴급 수정해줘` | `mobile_menu_controller.js의 toggle() 메서드에서 menuTarget이 null로 간헐적 에러 발생, 긴급 수정해줘` | 실제 코드의 메서드/타겟명 구체화 | toggle() L10, static targets L4, menuTarget 직접 접근 확인됨 |
| T-11 | `...프로젝트 갤러리 페이지와 About 상세 페이지를 동시에 만들어줘` | `블로그에 태그 필터링 기능과 검색 기능을 동시에 개발해줘. 태그는 posts/index에, 검색은 navbar에 추가` | 이미 존재하는 페이지 대신 신규 기능 2개 병렬 | posts/index와 _navbar.html.erb는 독립 파일, 완전 병렬 가능 |
| T-13 | `...Phase 2 기획서를 Word 문서로 만들어줘` | `...Phase 2 기획서를 Word 문서로 만들어줘. Phase 2는 PRD.md의 M3(상호작용) + M4(완성) 마일스톤 기반` | PRD.md 실제 마일스톤 참조 명시 | M3(L440-443), M4(L445-449) 실제 존재 확인됨 |
| T-17 | `...comments_controller.rb 파일에 주석을 추가해줘` | `likes_controller.rb의 find_user_like 메서드에 각 분기별 설명 주석을 추가해줘` | 구체적 메서드/위치 특정 | find_user_like L51-56, current_user 분기 2개 확인됨 |
| T-18 | `...모든 ERB 뷰 파일을 분석하고 각 파일별 개선점을 도출해줘` | `...6개 컨트롤러 파일을 각각 분석하고 파일별 코드 품질 개선점을 도출해줘` | 컨트롤러 6개로 범위 한정 | 6개 컨트롤러 독립적 병렬 분석 가능, ERB보다 병렬성 강화 |

---

## 성공 기준 (V4.2 목표)

| 지표 | V4.1.1 | V4.2 목표 | 비고 |
|------|:---:|:---:|------|
| PASS | 5건 (27.8%) | **12건+ (67%+)** | 이 테스트에서는 13개 중 9건+ 목표 (69%) |
| FAIL | 1건 | **0건** | T-03 한국어 키워드 해결 필수 |
| Hook 정확도 | 38.5% | **60%+** | Q4-1~Q4-6 개선으로 향상 |
| 체인 축약 방지 | 61.8% 실행율 | **100%** | Q2 핵심 -- 정의대로 전체 실행 |
| Teams 활성화 | 1/3 (33%) | **2/3 (50%+)** | T-07, T-11 Teams 전환 |
| 에이전트 실행율 | 61.8% | **100%** | 소넷은 에이전트 활용이 핵심 |

---

## 소넷 특화 관찰 포인트

| 항목 | 관찰 내용 |
|------|----------|
| **MetaThinkChain (T-06)** | 8개 에이전트 전체 실행 시 품질 vs 소요 시간 트레이드오프. learning_evolver[O], solution_innovator[O], insight_amplifier[O] 추론 품질 |
| **Teams (T-11)** | sonnet lead + sonnet teammate 품질. Plan Mode 품질. 태그 필터링 + 검색 듀얼 트랙 병렬 효율 |
| **체인 축약 (T-04~T-09)** | **소넷이 "충분하다" 판단으로 체인 축약하려는 경향 관찰** -- Q2 원칙 준수 여부 핵심 |
| **전체 소요 시간** | V4.1.1 대비 V4.2 소요 시간 변화 (에이전트 수 증가로 시간 증가 예상) |

---

## 비교 분석 방법

```
012 (이 문서)          →  예상치 (V4.2 개선 반영)
013_V42_Sonnet_Test_Results.md  →  실측치 (소넷 실제 동작)
비교 분석              →  미르(Cowork)가 GAP 분석 → 추가 개선안 도출
```

**핵심 질문**: 소넷 모델에서 체인 축약 금지(Q2)가 실제로 작동하는가? 에이전트를 끝까지 활용하는가?

---

*작성: 미르 (Cowork) | V4.2 소넷 체인 시스템 검증 V1.2 -- system_architect + problem_reframer 통합, Rails 프로젝트 기반 프롬프트 재설계*
