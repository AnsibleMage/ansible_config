# Memory Save Protocol 적용 가이드

> Claude Code에 메모리 저장 프로토콜 적용하기

## 사전 요구사항

- Claude Code CLI 설치
- `~/.claude/` 폴더 존재

---

## Step 1: 메모리 폴더 생성

```bash
mkdir -p ~/.claude/memory
```

---

## Step 2: CLAUDE.md 설정 확인

`~/.claude/CLAUDE.md` 파일에 다음 섹션이 포함되어야 합니다:

### 응답 완료 프로토콜 섹션

```markdown
## 🏁 응답 완료 프로토콜 (MANDATORY)

> **모든 의미 있는 작업 완료 시, 응답 마지막에 실행**

작업 완료
    ↓
1. 최근 메모리 3개 읽기 (중복 방지)
    ↓
2. 저장 여부 판단
   - 새로운 지식/인사이트?
   - 중요한 결정/변경?
   - 이전 메모리와 중복?
    ↓
3. 중복이면 기존 파일 업데이트
   새 내용이면 새 파일 생성
    ↓
💾 메모리 저장 완료
```

### 저장 기준 섹션

```markdown
**저장 기준**:
| 저장 O | 저장 X |
|--------|--------|
| 분석/설계 결과 | 단순 Q&A |
| 새로운 구현 | 파일 읽기만 |
| 중요한 결정 | 간단한 수정 |
| 학습/인사이트 | 반복 작업 |
```

### 메모리 시스템 섹션

```markdown
## 📦 Memory System

> **위치**: `~/.claude/memory/`

### 파일명 규칙

YYMM_SEQ_keyword.md

| 구성 요소 | 설명 |
|----------|------|
| YYMM | 연월 (2602 = 2026년 2월) |
| SEQ | 월별 시퀀스 (001~999) |
| keyword | 작업 키워드 (snake_case) |
```

---

## Step 3: /memory-save 스킬 생성 (선택)

수동 저장을 위한 스킬 설정:

### 파일 위치

```
~/.claude/commands/memory-save.md
```

### 내용

```markdown
현재 작업 내용을 메모리에 저장합니다.

## 저장 프로세스

1. ~/.claude/memory/ 폴더의 최근 파일 3개 확인
2. 중복 여부 판단
3. 새 파일 생성 또는 기존 파일 업데이트

## 파일명 규칙

YYMM_SEQ_keyword.md
- YYMM: 현재 연월
- SEQ: 월별 시퀀스 (다음 번호)
- keyword: 작업 키워드

## 문서 구조

# [작업 제목]

## 사용자 프롬프트
> [원본]

## 메타 정보
- 작성일: YYYY-MM-DD
- 요약: [1-2 문장]
- 시사점: [인사이트]

## 사용된 도구
- Chain: [체인명]
- Agents: [에이전트]
- Skills: [스킬]
- Tools: [도구]

## 내용
[상세 내용]

## 관련 메모리
[[xxx]]
```

---

## Step 4: 적용 확인

### 메모리 폴더 확인

```bash
ls -la ~/.claude/memory/
```

### CLAUDE.md 확인

```bash
grep -A 5 "응답 완료 프로토콜" ~/.claude/CLAUDE.md
```

### 테스트

Claude Code에서 분석 작업 수행 후, 응답 마지막에 메모리 저장이 되는지 확인:

```
🎵 완료! 다음은 뭘 할까요?
```

---

## 문제 해결

### 메모리가 저장되지 않는 경우

1. `~/.claude/memory/` 폴더 존재 확인
2. CLAUDE.md에 프로토콜 섹션 포함 확인
3. 저장 기준 충족 여부 확인 (단순 Q&A는 저장 X)

### 중복 파일이 생기는 경우

1. 최근 메모리 3개 확인 로직 동작 확인
2. 동일 주제 판단 기준 명확화

### 파일명 시퀀스 오류

```bash
# 최신 시퀀스 확인
ls ~/.claude/memory/$(date +%y%m)_*.md | tail -1
```

---

## 권장 사용 패턴

### 분석 작업 후

```
사용자: "이 코드베이스 분석해줘"
Claude: [분석 수행]
Claude: [메모리 저장]
Claude: 🎵 완료! 다음은 뭘 할까요?
```

### 설계 작업 후

```
사용자: "API 설계해줘"
Claude: [설계 수행]
Claude: [메모리 저장]
Claude: 🎵 완료! 다음은 뭘 할까요?
```

### 수동 저장

```
사용자: /memory-save
Claude: [현재 컨텍스트 저장]
```

---

## 폴더 구조

적용 후 예상 구조:

```
~/.claude/
├── CLAUDE.md              # 프로토콜 포함
├── memory/                # 메모리 저장소
│   ├── 2602_001_xxx.md
│   ├── 2602_002_xxx.md
│   └── ...
├── commands/
│   └── memory-save.md     # 수동 저장 스킬
└── ...
```

---

## 관련 문서

- [README.md](./README.md) - 시스템 개요
- [CLAUDE.md](~/.claude/CLAUDE.md) - 전체 가이드라인
