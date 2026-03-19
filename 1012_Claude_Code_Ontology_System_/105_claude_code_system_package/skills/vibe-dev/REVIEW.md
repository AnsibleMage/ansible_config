# vibe-dev 스킬 품질 리뷰

> 리뷰 일자: 2026-02-13
> 리뷰 대상: `~/.claude/skills/vibe-dev/` (V1.0)
> 리뷰어: quality_reviewer

---

## 종합 평가

| 평가 차원 | 점수 | 핵심 소견 |
|----------|------|----------|
| 구조 완성도 | 9/10 | 4단계 완전 구성, 참조 분리 우수 |
| 명확성 | 8/10 | 명확하나 일부 애매한 분기 존재 |
| 일관성 | 7/10 | 문서 번호/이름 불일치 발견 |
| 실용성 | 8/10 | 다양한 프로젝트 지원, 실제 적용 가능 |
| Progressive Disclosure | 9/10 | SKILL.md 간결, 참조 구조 탁월 |
| 범용성 | 8/10 | 범용적이나 웹 편향 존재 |
| 누락 사항 | 6/10 | 사용 예시, 롤백, CLI 부족 |

**종합 점수: 8.1/10**

---

## 1. 구조 완성도 (9/10)

### 강점
- 4단계 프레임워크 완전 구성: Investigate, Define, Develop, Report
- 단계별 상세 문서 분리: phase1~4 + zero-guess + templates
- Entry Point Detection 테이블: 사용자 상태별 진입점 5개
- Stage/Gate 시스템: 7단계 개발 + Gate 기준 명확

### 약점
- Phase 1 스킵 시 흐름 불명확: `/vibe-dev skip-phase1` 사용 시 Phase 2 진입 과정 미기술
- 중단/재개 프로토콜 부재: `/vibe-dev resume`이 체크포인트를 찾는 방법 미명시

---

## 2. 명확성 (8/10)

### 강점
- Zero-Guess Protocol: 3 Mechanisms + 5 Forbidden Actions 구체적
- Templates 예시 풍부: PRD~Test Spec 5개 템플릿 제공
- Gate 기준 검증 가능: "runs without errors", "compiles clean", "tests pass"

### 약점
- "Reasonable assumptions" 판단 기준 없음 (phase1-investigate.md)
- Teams 병렬 조건 "if independent" 독립성 판단 기준 부재
- Cross-reference 표기법 혼용: `[[doc]] §section` vs `[[doc/03]]`

---

## 3. 일관성 (7/10) — Critical

### Critical 이슈: 문서 번호 불일치

현재 (충돌):
```
doc/00_PRD.md          # 00번
doc/00_workplan.md     # 00번 충돌!
doc/01_investigation.md
```

제안 (정규화):
```
doc/00_investigation.md      # Phase 1
doc/01_PRD.md                # Phase 2 시작
doc/02_workplan.md
doc/03_architecture.md
doc/04_impl_spec.md
doc/05_ui_spec.md (optional)
doc/06_test_spec.md
doc/07_ai_strategy.md (optional)
doc/08_review.md             # Phase 4
doc/09_final_report.md
```

### Minor 이슈
- "implementation spec" vs "impl spec" 축약 혼재
- "doc" vs "document" vs "spec" 혼재

---

## 4. 실용성 (8/10)

### 강점
- 프로젝트 타입 6종 지원: Web/CLI/API/Game/Mobile/Library
- TDD 통합: Stage 2 Core Logic
- Batch 전략: 3-5 related functions per batch
- Hotfix 프로토콜: spec 우선 수정

### 약점
- UI 없는 프로젝트: Stage 3 처리 방식 불명확
- Legacy 프로젝트: Phase 4만 진입 가능? 중간 진입 불가?

### 필요: 프로젝트 타입별 매핑 테이블
| Type | Stage 1 | Stage 3 | Stage 6 |
|------|---------|---------|---------|
| Web App | Types + Components | UI per doc/04 | a11y + deploy |
| CLI | Types + Commands | Arg parsing | man page + publish |
| API | Types + Schemas | Routes + middleware | Swagger + deploy |
| Library | Types + Exports | Public API only | Docs + npm publish |

---

## 5. Progressive Disclosure (9/10)

### 강점
- SKILL.md 103줄, 핵심만 제공
- `See [references/X.md]` 일관된 참조 패턴
- 템플릿 분리: document-templates.md로 코드 블록 격리

### 약점
- SKILL.md 체인 통합 테이블 (라인 88-95)이 CLAUDE.md와 중복 가능

---

## 6. 범용성 (8/10)

### 강점
- 프레임워크 비의존적: "framework CLI" 일반 용어
- 언어 중립적 템플릿

### 웹 편향 흔적
- UI Spec 별도 문서 (doc/04), CLI는 doc/03에 포함
- Stage 6 "accessibility audit (if UI)" 웹만 언급
- Teams 예시 `components/` `routes/` 웹 디렉토리

---

## 7. 누락 사항 (6/10)

### Critical 누락
- 사용 예시 부재: 실제 프롬프트 → 실행 흐름 데모 없음
- 에러 복구 프로토콜: Gate 실패 시 복구 프로세스 추상적
- 문서 버전 관리: PRD/Spec 변경 시 규칙 없음

### Major 누락
- Checkpoint 파일 형식: resume 시 읽는 파일 미정의
- Teams 구성 예시: "Teammate A/B" 추상적
- 보안 고려사항: API key, credentials 포함 위험 경고 없음

### Minor 누락
- 테스트 커버리지 목표 기준 없음
- 다국어 지원: 한국어/영어 혼재, 선택 기준 없음

---

## 8. 개선 제안 (우선순위별)

### P0 (Critical) — 즉시 수정

| 작업 | 소요 | 파일 |
|------|------|------|
| 문서 번호 재정렬 | 30분 | 전체 파일 |
| Resume protocol 작성 | 1시간 | checkpoint-protocol.md (신규) |

### P1 (High) — 1주일 내

| 작업 | 소요 | 파일 |
|------|------|------|
| Usage examples 작성 | 2시간 | usage-examples.md (신규) |
| 프로젝트 타입별 가이드 | 1시간 | phase3-develop.md 확장 |

### P2 (Medium) — 점진적

| 작업 | 소요 | 파일 |
|------|------|------|
| Error recovery playbook | 1시간 | error-recovery.md (신규) |
| Security section 추가 | 30분 | phase2-define.md 확장 |
| 커버리지 목표 추가 | 30분 | document-templates.md 확장 |

---

## 긍정적 평가

- **Zero-Guess Protocol**: AI 환각(hallucination) 방어를 문서 기반 검증으로 체계화
- **Stage/Gate 시스템**: 품질 검증을 자동화 가능한 형태로 정의
- **Progressive Disclosure 모범**: SKILL.md → references/ 분리가 표준적
- **Template 실용성**: 5개 문서 템플릿이 즉시 사용 가능 수준
- **Entry Point Detection**: 사용자 상태별 자동 진입이 UX 우수

---

## 결론

vibe-dev 스킬은 **8.1/10 수준의 잘 설계된 AI 개발 방법론**. Zero-Guess Protocol과 Stage/Gate 시스템이 핵심 강점. P0 개선(문서 번호 + Resume protocol, 약 1.5시간)만 완료하면 프로덕션 사용 가능. CLI/라이브러리 프로젝트 실전 테스트 권장.
