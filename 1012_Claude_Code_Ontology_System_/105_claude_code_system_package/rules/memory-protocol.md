## 3. Memory & Protocol

### 응답 완료 프로토콜 (MANDATORY)

> **모든 의미 있는 작업 완료 시 실행**

1. **중복 확인**: 벡터 리콜된 메모리(additionalContext) + 최근 3개 파일명 확인 → 동일 주제면 기존 파일 업데이트
2. **저장 여부 판단**: 분석/설계/결정/인사이트 → 저장 O | 단순 Q&A/파일 읽기 → 저장 X
3. **파일 생성/수정**: frontmatter(name, description, type) 필수 포함 → `~/.claude/memory/` 에 저장
4. **자동 벡터화**: 저장 즉시 PostToolUse Hook이 Qdrant 자동 인덱싱 (백그라운드, 앤 대기 없음)
5. `💾 메모리 저장 완료` → `🌟 완료! 다음은 뭘 할까요?`

> **핵심 변화 (V5.1+)**: 메모리 저장 후 수동 인덱싱이 필요 없어짐. `memory-autoindex.sh` Hook이 Write 감지 → nohup 백그라운드 인덱싱 → ~3초 후 다음 프롬프트부터 리콜 가능.

**Teammate 세션**: 메모리 저장 절대 금지 (Race Condition 방지)

### 벡터 리콜 시스템 (자동)

> **프롬프트 입력 시 자동 실행** — 아리가 별도 조작할 필요 없음

```
프롬프트 입력 → auto-analyze.sh → recall_server:18765
→ Qdrant 코사인 유사도 검색 (threshold 0.7, top_k 3)
→ additionalContext로 관련 메모리 주입
→ 아리가 리콜된 메모리를 참조하여 응답 생성
```

| 구성요소 | 역할 | 자동/수동 |
|---------|------|----------|
| SessionStart Hook | 리콜 서버 시작 + 최근 메모리 3개 로드 | 자동 |
| auto-analyze.sh | 프롬프트 벡터화 → Qdrant 검색 → 리콜 결과 주입 | 자동 |
| memory-autoindex.sh | 메모리 저장 시 → Qdrant 벡터화 | 자동 |
| memory_index MCP | 수동 인덱싱 (재인덱싱, 전체 갱신) | 수동 |

### 에이전트/Teammate 메모리 격리 규칙 (MANDATORY)

⚠️ Task(서브에이전트) 및 Teammate 내에서:
- `~/.claude/memory/`에 파일 생성/수정 **절대 금지**
- 메모리 저장은 반드시 **리드(메인 세션)에서만** 수행
- 위반 시 중복/불완전 파일 발생 → 데이터 정합성 훼손
- 자동 인덱싱 Hook도 리드 세션의 Write만 감지 (Teammate Write는 memory/ 경로가 아니므로 안전)

### Memory System

> **위치**: `~/.claude/memory/`
> **벡터 DB**: Qdrant (localhost:6333, collection: `claude_memory`, 1024차원)

**파일명**: `YYMM_SEQ_keyword.md` (예: `2602_015_rails8_analysis.md`)

| 구성 | 설명 |
|------|------|
| YYMM | 연월 (2602 = 2026년 2월) |
| SEQ | 월별 시퀀스 001~999 (매월 리셋) |
| keyword | 작업 키워드 (snake_case) |

**중복 방지**: 저장 전 리콜 결과 + 최근 3개 확인 → 동일 주제면 기존 파일 업데이트

### 메모리 문서 구조 (벡터 검색 최적화)

> **핵심**: `##` 헤딩이 Qdrant 청크 분할 기준. 각 `##` 섹션이 독립 벡터로 저장됨.
> 따라서 각 섹션은 **해당 섹션만 읽어도 의미가 통하도록** 작성해야 함.

```markdown
---
name: [메모리 식별 이름 — Qdrant summary 필드로 저장]
description: [1줄 설명 — 벡터 검색 시 표시되는 요약]
type: [user | feedback | project | reference]
---

# [작업 제목]

## 사용자 프롬프트
[앤의 원문 — 이 섹션이 독립 청크로 벡터화됨]

## 메타 정보
- 작성일: YYYY-MM-DD
- 요약: [1~2줄 — 이 청크가 검색될 때 핵심 맥락 제공]
- 시사점: [향후 참조 시 중요한 포인트]

## 사용된 도구
- Chain: [사용된 체인명]
- Agents: [사용된 에이전트 목록]
- Skills: [사용된 스킬 목록]

## 내용
[본문 — 가장 큰 청크. 500자 초과 시 자동 분할됨]

## 관련 메모리
- `YYMM_SEQ_keyword.md` — [관계 설명]
```

#### frontmatter 필수 필드

| 필드 | 용도 | Qdrant 매핑 |
|------|------|-----------|
| `name` | 메모리 식별 | payload.summary |
| `description` | 리콜 시 표시되는 요약 | 검색 결과 미리보기 |
| `type` | 분류 (user/feedback/project/reference) | payload.tags |

> ⚠️ frontmatter가 없으면 indexer가 파일명에서 자동 추출하지만, **description이 없으면 리콜 결과에 요약이 빈칸**으로 표시됨. 반드시 작성.

### 벡터 저장 구조 (참고)

```
메모리 파일 1개 → N개 청크로 분할 → N개 벡터 포인트

청크 분할 기준:
- ## 헤딩 단위 (각 섹션 = 1 청크)
- 500자 초과 시 문장 단위 추가 분할
- 50자 미만 청크는 제외

관계 자동 탐색:
- 코사인 유사도 0.80+ → 관련 메모리로 연결
- memory_id 순번 비교 → precedes/follows 시간 관계
- 관계는 payload.related_to에 JSON 저장
```

### 메모리 생명주기

```
[생성] 아리가 .md 파일 Write
    ↓
[벡터화] memory-autoindex.sh → nohup 백그라운드 (~3초)
    ↓
[저장] Qdrant claude_memory 컬렉션에 포인트 upsert
    ↓
[리콜] 다음 프롬프트 입력 시 유사도 검색으로 자동 리콜
    ↓
[갱신] 동일 주제 재작업 시 기존 파일 업데이트 → 재벡터화 (같은 ID로 덮어쓰기)
    ↓
[탐색] memory_graph MCP로 관련 메모리 그래프 탐색 (hops 기반)
```
