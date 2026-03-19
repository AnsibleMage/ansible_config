# Usage Examples

## Example 1: Web App from Idea

**User**: `/vibe-dev 할 일 관리 웹앱 만들고 싶어`

**Phase 1: INVESTIGATE**
```
AI: 5가지 질문
  1. 핵심 기능 3가지는? (CRUD, 마감일, 카테고리?)
  2. 주요 사용자는? (개인? 팀?)
  3. 기술 제약이나 선호 스택은?
  4. 예상 사용자 규모는?
  5. MVP 완성 목표 시기는?
User: "혼자 쓸 거고, React 좋아해. 나머지 알아서 해줘"
AI: WebSearch → 유사 서비스 분석 → 기술 스택 추천
AI: doc/00_investigation.md 작성
AI: "조사 결과를 확인해주세요. Phase 2로 진행할까요?"
User: "진행해"
```

**Phase 2: DEFINE**
```
AI: doc/01_PRD.md 작성 → User 승인 요청
User: "좋아 진행해"
AI: doc/02~06 순차 생성 (workplan, architecture, impl_spec, ui_spec, test_spec)
```

**Phase 3: DEVELOP**
```
Stage 0: npx create-next-app → Gate ✅
Stage 1: types + constants + fixtures → Gate ✅
Stage 2: CRUD 로직 TDD → Gate ✅
Stage 3: React 컴포넌트 → Gate ✅
Stage 4: 통합 → Gate ✅
Stage 5: 테스트 → Gate ✅
Stage 6: 접근성 + 빌드 → Gate ✅
```

**Phase 4: REPORT**
```
AI: doc/08_review.md + doc/09_final_report.md 작성
AI: "프로젝트 완료! 총 6개 문서, 15개 소스 파일, 테스트 통과율 100%"
```

---

## Example 2: CLI Tool (No UI)

**User**: `/vibe-dev skip-ui JSON 파일을 CSV로 변환하는 CLI 도구`

**Phase 1: INVESTIGATE** (UI 스킵 플래그 인식)
```
AI: 3가지 질문 (입력 형식, 출력 옵션, 에러 처리)
AI: doc/00_investigation.md (CLI 도구로 분류)
```

**Phase 2: DEFINE**
```
doc/01_PRD.md (CLI 중심)
doc/02_workplan.md
doc/03_architecture.md (bin/, lib/ 구조)
doc/04_impl_spec.md (commander.js args, transform functions)
doc/05_ui_spec.md → SKIPPED
doc/06_test_spec.md (경계값: 빈 JSON, 중첩 객체, 대용량)
```

**Phase 3: DEVELOP**
```
Stage 3: CLI command handlers (UI 대신)
Stage 6: man page + npm publish config (deploy 대신)
```

---

## Example 3: Resume Existing Project

**User**: `/vibe-dev resume`

```
AI: doc/.vibe-dev-state.md 확인
    → Phase 3, Stage 2 Gate 통과 상태
AI: "Stage 2(Core Logic) 완료 확인. Stage 3(Interface)로 진행할까요?"
User: "진행해"
AI: Stage 3 시작
```

**State file not found fallback:**
```
AI: doc/ 폴더 스캔
    → doc/00~06 존재, 소스코드 있음
AI: Gate 검사 → Stage 1 Gate 통과, Stage 2 일부만 완료
AI: "Stage 2(Core Logic) 중간 상태입니다. 이어서 진행할까요?"
```

---

## Example 4: Report Only

**User**: `/vibe-dev report-only`

```
AI: 코드베이스 분석 → doc/ 존재 확인
AI: Phase 4 즉시 시작
    → AI Self-Review (각 문서 점수)
    → Cross-Reference Verification
    → doc/08_review.md + doc/09_final_report.md 작성
AI: "리뷰 완료. 종합 점수 8.5/10"
```

---

## Example 5: API Server

**User**: `/vibe-dev REST API 서버 만들어줘. 사용자 인증이랑 게시판 CRUD`

**Phase 2 차이점:**
```
doc/04_impl_spec.md:
  - Route definitions (GET /api/posts, POST /api/auth/login, ...)
  - Middleware specs (auth, validation, error handler)
  - DB schema (users, posts tables)

doc/05_ui_spec.md → SKIPPED (API only)
```

**Phase 3 차이점:**
```
Stage 3: Route handlers + middleware (UI 컴포넌트 대신)
Stage 6: Swagger/OpenAPI docs + deploy config
```

---

## Example 6: Skip Phase 1

**User**: `/vibe-dev skip-phase1 이미 조사는 다 했어. Next.js + Supabase로 블로그 만들 거야`

```
AI: Phase 2 즉시 시작
AI: "기술 스택이 정해져 있으니 PRD부터 작성합니다."
AI: doc/01_PRD.md 작성 (Next.js + Supabase 전제)
```

---

## Trigger Patterns

| User Says | Action |
|-----------|--------|
| `/vibe-dev [아이디어]` | Phase 1 from start |
| `/vibe-dev skip-phase1 [설명]` | Phase 2 from start |
| `/vibe-dev skip-ui [설명]` | Phase 1, doc/05 skipped |
| `/vibe-dev resume` | Detect and continue |
| `/vibe-dev report-only` | Phase 4 only |
| `바이브 개발 [아이디어]` | Same as /vibe-dev |
| `새 프로젝트 시작하고 싶어` | Phase 1 from start |
