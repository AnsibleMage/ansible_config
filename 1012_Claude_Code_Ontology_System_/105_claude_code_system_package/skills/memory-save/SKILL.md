---
name: memory-save
description: Save the current session's work to ~/.claude/memory/ with deduplication and YYMM_SEQ_keyword.md naming.
user-invocable: true
allowed-tools: [Read, Write, Glob]
---

현재 세션의 작업 내용을 `~/.claude/memory/` 폴더에 기록해주세요.

## 저장 내용
$ARGUMENTS (저장할 내용 요약 또는 키워드)

## 수행 작업
1. `~/.claude/memory/` 폴더 존재 확인 (없으면 생성)
2. **최근 메모리 3개 읽기** (중복 방지)
   - 최근 파일 목록 확인
   - 각 파일의 제목/요약 확인
   - 현재 작업과 중복 여부 판단
3. **중복 시**: 기존 파일에 내용 추가/업데이트 (새 파일 생성 X)
4. **새 내용 시**: 다음 순번으로 새 파일 생성 (YYMM_SEQ 형식)
5. `~/.claude/memory/YYMM_SEQ_keyword.md` 저장
6. 저장 완료 보고 (💾 메모리 저장 완료)

## 문서 형식 (필수)
```markdown
# [작업 제목]

## 사용자 프롬프트
> [원본 요청]

## 메타 정보
- **작성일**: YYYY-MM-DD
- **요약**: [1-2문장]
- **시사점**: [핵심 인사이트]

## 사용된 도구

### Chain
[사용된 체인 패턴 또는 "Direct (단순 작업)"]
예: `DevChain`, `ThinkChain`, `FastTrack`, `Direct`

### Agents
[사용된 서브에이전트 목록]
예:
- `system_architect` [opus]
- `code_developer` [sonnet]
- 없음 (직접 처리)

### Skills
[사용된 슬래시 스킬 목록]
예:
- `/frontend-design`
- `/pdf`
- 없음

### Tools
[사용된 기본 도구]
예:
- `Read` - 파일 읽기
- `Edit` - 파일 수정
- `Bash` - 명령 실행
- `WebSearch` - 웹 검색

## 내용
[상세 작업 내용 및 결과]

## 관련 메모리
[연관된 이전 메모리 파일 링크]
예: [[2602_001_xxx]], [[2602_002_xxx]]
```

## 파일명 규칙
- **형식**: `YYMM_SEQ_keyword.md`
- **YYMM**: 연월 (예: `2602` = 2026년 2월)
- **SEQ**: 월별 시퀀스 (001~999, 매월 리셋)
- **keyword**: 작업 키워드 (snake_case)

**예시**:
```
2602_020_skills_analysis.md
2602_021_hook_fix.md
2603_001_new_project.md  # 3월 첫 번째 (리셋)
```

## 중복 방지 규칙
- **저장 전 반드시** 최근 메모리 3개를 읽어 중복 확인
- 동일 주제/작업이면 기존 파일에 "## 추가 내용" 섹션으로 업데이트
- 완전히 새로운 주제일 때만 새 파일 생성
- 세션 내 여러 번 저장 시 하나로 통합

## 중요
- **사용된 도구** 섹션은 반드시 포함해야 함
- Chain/Agents/Skills/Tools 중 사용하지 않은 항목도 "없음"으로 명시
- 미래 AI가 맥락을 이해할 수 있도록 상세히 기록
