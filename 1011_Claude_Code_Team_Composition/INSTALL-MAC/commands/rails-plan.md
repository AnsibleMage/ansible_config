# /rails-plan - 작업계획서 생성

승인된 PRD를 기반으로 작업계획서(Task Plan)를 생성하고 TODO 리스트를 만듭니다.

## 트리거
- "작업계획 만들어줘", "태스크 분해", "TODO 생성"

## 실행 단계

### 1. PRD 분석

`docs/PRD.md` 읽기:
- 사용자 스토리 추출
- 데이터 모델 확인
- 마일스톤 확인

### 2. 마일스톤 정의

```markdown
| ID | 마일스톤 | 설명 | 스프린트 |
|----|---------|------|---------|
| M1 | 기본 인프라 | 프로젝트 설정, 인증 | Sprint 1 |
| M2 | 핵심 기능 | 주요 CRUD | Sprint 2-3 |
| M3 | 부가 기능 | 추가 기능 | Sprint 4 |
| M4 | 배포 | 프로덕션 | Sprint 5 |
```

### 3. 스프린트 분해

각 마일스톤을 1-2주 스프린트로 분해

### 4. 태스크 생성

각 사용자 스토리를 구현 태스크로 분해:

```markdown
### T[X.Y]: [태스크명]

**Sprint**: [N]
**우선순위**: P0/P1/P2
**의존성**: T[X.Z]

**설명**:
[상세 설명]

**수용 기준**:
- [ ] [기준 1]
- [ ] [기준 2]

**테스트 케이스**:
```ruby
# 예상 테스트
```

**예상 파일**:
- [파일 경로]
```

### 5. 의존성 분석

```
T1.1 ──► T1.2 ──► T1.3 ──► T1.4
                     │
                     └──► T1.5 (병렬)
```

### 6. 작업계획서 생성

`docs/TaskPlan.md` 파일 생성

### 7. Claude Code TODO 생성

TaskCreate 도구로 각 태스크를 TODO로 생성:

```javascript
// 예시
TaskCreate({
  subject: "T1.1: 프로젝트 초기화",
  description: "Rails 8 프로젝트 생성 및 기본 설정\n\n수용 기준:\n- [ ] rails new 실행\n- [ ] Git 초기화",
  activeForm: "프로젝트 초기화 중"
})
```

의존성 설정:
```javascript
TaskUpdate({
  taskId: "2",
  addBlockedBy: ["1"]
})
```

### 8. 사용자 확인

```
작업계획서를 생성했습니다: docs/TaskPlan.md

요약:
- 마일스톤: 4개
- 스프린트: 5개
- 태스크: [N]개

TODO 리스트가 생성되었습니다.
확인 후 `/rails-dev`로 개발을 시작합니다.

주요 의존성:
- 인증 완료 후 → 핵심 기능
- DB 설정 → 모델 작업
```

## 태스크 분해 원칙

### INVEST 원칙

- **I**ndependent: 독립적으로 완료 가능
- **N**egotiable: 구현 방법 유연
- **V**aluable: 완료 시 가치 제공
- **E**stimable: 작업량 추정 가능
- **S**mall: 1일 이내 완료
- **T**estable: 테스트 가능한 기준

### TDD 기반 분해

1. 테스트 작성 태스크
2. 구현 태스크
3. 리팩토링 태스크

## 템플릿 위치

`~/.claude/templates/rails8/TaskPlan_Template.md`

## 다음 단계

작업계획 승인 후:
- `/rails-dev "T1.1: 프로젝트 초기화"` 로 개발 시작
- TODO 리스트에서 태스크 순서대로 진행
