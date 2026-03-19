# Memory File Template

> 메모리 파일 작성 시 사용하는 템플릿

---

## 파일명 규칙

```
YYMM_SEQ_keyword.md
```

예시: `2602_015_rails8_analysis.md`

---

## 템플릿

```markdown
# [작업 제목]

## 사용자 프롬프트
> [원본 요청 - 그대로 복사]

## 메타 정보
- **작성일**: YYYY-MM-DD
- **요약**: [작업 내용 1-2 문장 요약]
- **시사점**: [핵심 인사이트 또는 배운 점]

## 사용된 도구
### Chain
[사용 체인명 또는 "Direct" (체인 미사용 시)]

### Agents
- [사용한 에이전트 목록]
- 없으면 "없음"

### Skills
- [사용한 스킬 목록 (/, /docx 등)]
- 없으면 "없음"

### Tools
- [사용한 기본 도구 (Bash, Read, Write, Grep, Glob 등)]

## 내용
[상세 작업 내용]

### 주요 결과
[핵심 결과물 또는 산출물]

### 결정 사항
[내린 결정이 있다면 기록]

### 학습 내용
[새롭게 알게 된 내용]

## 관련 메모리
[[관련_메모리_파일명]]
```

---

## 작성 예시

```markdown
# Rails 8 프로젝트 구조 분석

## 사용자 프롬프트
> Rails 8 프로젝트 구조를 분석하고 Solid Queue 설정을 확인해줘

## 메타 정보
- **작성일**: 2026-02-04
- **요약**: Rails 8 프로젝트의 폴더 구조와 Solid Queue 설정 분석
- **시사점**: Solid Queue는 config/solid_queue.yml로 설정하며, 별도 Redis 불필요

## 사용된 도구
### Chain
DevChain

### Agents
- system_architect
- code_developer

### Skills
- 없음

### Tools
- Glob
- Read
- Grep

## 내용
### 주요 결과
- app/ 구조 Rails 8 표준 준수
- Solid Queue 설정 완료
- Background job 3개 정의됨

### 결정 사항
- Sidekiq → Solid Queue 마이그레이션 완료
- Redis 의존성 제거

### 학습 내용
- Solid Queue는 PostgreSQL 기반으로 동작
- mission_control-jobs gem으로 모니터링 가능

## 관련 메모리
[[2602_010_solid_queue_setup]]
[[2602_008_rails8_migration]]
```

---

## 작성 가이드

### 제목
- 명확하고 구체적으로
- 검색 가능한 키워드 포함

### 사용자 프롬프트
- 원본 그대로 복사
- `>` 인용 형식 사용

### 메타 정보
- **요약**: 한 줄로 핵심 전달
- **시사점**: 다른 작업에 적용 가능한 인사이트

### 사용된 도구
- 실제 사용한 것만 기록
- 체인은 CLAUDE.md의 A~K 체인명 사용

### 내용
- 구조화하여 작성
- 나중에 참조하기 쉽게

### 관련 메모리
- Obsidian 위키링크 형식 `[[파일명]]`
- 연관 작업 연결
