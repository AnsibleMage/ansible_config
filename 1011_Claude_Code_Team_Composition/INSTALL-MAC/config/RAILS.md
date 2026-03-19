# Rails 8 Development System

> 분리일: 2026-02-06 (CLAUDE.md V4.0)
> 자동 연관: 프롬프트에 "레일즈", "rails", "RAILS", "kamal", "바이브코딩" 감지 시 자동 참조

---

## 바이브코딩 철학

> 사용자는 요구사항만 제시, AI가 전체 개발 라이프사이클 자동화

## Rails 8 Skills (7개)

| 키워드 (KO/EN) | Tool | 기능 |
|----------------|------|------|
| Rails 초기화, new project | `/rails-init` | Rails 8 프로젝트 생성 및 초기 설정 |
| PRD, 요구사항 | `/rails-prd` | 요구사항 → PRD 문서 자동 생성 |
| 계획, 태스크 분해 | `/rails-plan` | PRD → 작업계획서 + TODO 생성 |
| 개발, TDD | `/rails-dev` | TDD 기반 개발 (RED-GREEN-REFACTOR) |
| 테스트, RSpec | `/rails-test` | 전체 테스트 + 품질 검증 |
| 배포, Kamal | `/rails-deploy` | Kamal 2 프로덕션 배포 |
| 검증, verify | `/rails-verify` | 프로덕션 헬스체크 및 스모크 테스트 |

## RailsDevChain 패턴

```
/rails-prd[-] → /rails-plan[-] → (/rails-dev[-] → /rails-test[-]) × N
→ /rails-deploy[-] → /rails-verify[-]
```

## 워크플로우 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                    Rails 8 바이브코딩 워크플로우                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 요구사항                                                     │
│       ↓                                                         │
│  /rails-prd ──→ docs/PRD.md (승인 대기)                          │
│       ↓                                                         │
│  /rails-plan ──→ docs/TaskPlan.md + TODO 리스트                  │
│       ↓                                                         │
│  ┌─────────────────────────────────┐                            │
│  │  /rails-dev (TDD 사이클)         │ ← 반복                     │
│  │    🔴 RED: 테스트 작성            │                            │
│  │    🟢 GREEN: 최소 구현            │                            │
│  │    🔵 REFACTOR: 코드 개선         │                            │
│  │       ↓                          │                            │
│  │  /rails-test (품질 검증)          │                            │
│  └─────────────────────────────────┘                            │
│       ↓                                                         │
│  /rails-deploy ──→ 프로덕션 배포 (Kamal 2)                       │
│       ↓                                                         │
│  /rails-verify ──→ 헬스체크 + 스모크 테스트                       │
│       ↓                                                         │
│  🎉 완료!                                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Rails 8 기술 스택

| 카테고리 | 기술 | 설명 |
|----------|------|------|
| **Framework** | Rails 8.0+ | One Person Framework |
| **Database** | PostgreSQL 16 | Primary DB |
| **Background Jobs** | Solid Queue | DB-based job processing |
| **Caching** | Solid Cache | DB-based caching |
| **WebSocket** | Solid Cable | DB-based Action Cable |
| **Deployment** | Kamal 2 + Thruster | Zero-downtime deploy |
| **Testing** | RSpec + Capybara | TDD/BDD |
| **Code Quality** | RuboCop + Brakeman | Linting + Security |

## 관련 문서

| 문서 | 위치 | 내용 |
|------|------|------|
| 방법론 개요 | `methodology/300_Vibe_Coding_Overview.md` | 전체 철학 및 워크플로우 |
| 환경 설정 | `methodology/301_Environment_Setup.md` | 맥북 개발 환경 구성 |
| 프로젝트 구조 | `methodology/302_Project_Structure.md` | Rails 8 폴더 구조 |
| TDD 프로세스 | `methodology/306_TDD_BDD_Process.md` | TDD/BDD 상세 가이드 |
| 배포 가이드 | `methodology/307_Deployment_Kamal2.md` | Kamal 2 배포 설정 |

## 템플릿

| 템플릿 | 위치 | 용도 |
|--------|------|------|
| PRD | `~/.claude/templates/rails8/PRD_Template.md` | 요구사항 문서 |
| TaskPlan | `~/.claude/templates/rails8/TaskPlan_Template.md` | 작업계획서 |
| Gemfile | `~/.claude/templates/rails8/Gemfile_Template` | 권장 Gemfile |
| deploy.yml | `~/.claude/templates/rails8/deploy_yml_Template.yml` | Kamal 설정 |
