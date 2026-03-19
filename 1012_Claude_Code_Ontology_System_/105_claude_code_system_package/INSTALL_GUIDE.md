# Claude Code System Package — 설치 가이드

> Version: 5.1.0 | 원본 시스템: 앤(An)의 Claude Code V5.1.0
> 이 패키지를 설치하면 앤의 오케스트레이션 시스템이 복제됩니다.

---

## 1. 패키지 개요

### 1.1 포함 구성요소

| 카테고리 | 파일 수 | 설명 |
|---------|--------|------|
| **config/** | 7 | CLAUDE.md(V5.1.0), REVIEW.md, RAILS.md, CHANGELOG.md, statusline.sh, settings.json.template |
| **rules/** | 2 | orchestration.md(체인 A~J, Teams, 워크플로우), memory-protocol.md(벡터 리콜 연동) |
| **agents/** | 20 | Primary 14개(101~114) + Eval/Review 6개 — 전부 Opus 모델 |
| **skills/** | 27 dirs | 공식 17개 + 커스텀 10개 + chains/ 2개(DevChain, SystemDesignChain) |
| **commands/** | 13 | 일반 6개 + Rails 7개 (skills/와 공존) |
| **hooks/** | 8 | auto-analyze, session-start, stop-cleanup, observability, memory-autoindex 등 |
| **scripts/** | 13 | prompt_analyzer, memory_embedder/indexer/mcp/recall, gate1~3_checker 등 |
| **workflow/** | 3 | research_template.md, plan_template.md, instances/.gitkeep |
| **eval/** | 2 | eval_test.json(25 TC), benchmark.json |
| **templates/** | 5 | Rails 8 프로젝트 템플릿 |

### 1.2 제외된 항목 (의도적)

| 항목 | 이유 |
|------|------|
| `~/.claude/memory/` 파일들 | 작업별 고유 데이터 — 복제 불필요 |
| `~/.claude/logs/` | 세션별 로그 — 자동 생성됨 |
| `~/.claude/plans/` | 세션별 플랜 — 자동 생성됨 |
| `~/.claude/venv/` | Python 가상환경 — 대상 시스템에서 별도 생성 |
| `~/.claude/qdrant_data/` | Qdrant 벡터 데이터 — 대상 시스템에서 별도 생성 |
| `~/.claude/plugins/` | 공식 플러그인 — Claude Code가 자동 관리 |
| `~/.claude/sessions/` | 세션 메타데이터 — 자동 생성됨 |

---

## 2. 설치 방법

### 2.1 자동 설치 (install.sh)

```bash
# 기본 설치 (타겟: ~/.claude)
bash install.sh

# 커스텀 경로
bash install.sh --target /path/to/.claude

# 온톨로지 서버 스킵 (벡터 메모리 없이 기본 기능만)
bash install.sh --skip-ontology

# 테스트 실행 (파일 복사 없이 계획만 출력)
bash install.sh --dry-run
```

### 2.2 Claude Code에게 설치 위임

> **이 섹션이 가장 중요합니다.** Claude Code에게 아래 프롬프트를 입력하면 설치가 자동 수행됩니다.

#### 설치 프롬프트 (Claude Code에 입력)

```
이 패키지를 설치해서 내 Claude Code 시스템을 구성해줘.

패키지 경로: [패키지가 있는 절대 경로]/105_claude_code_system_package/
타겟 경로: ~/.claude/

설치 순서:
1. install.sh를 읽고 이해해줘
2. bash install.sh 실행해줘
3. 설치 완료 후 검증 수행해줘
4. 온톨로지 서버가 필요하면 Phase 10 가이드를 따라 수동 설정해줘

설치 후 '안녕'이라고 입력하면 "🌟 안녕, 앤!" 이라고 응답해야 정상이야.
```

---

## 3. 설치 상세 — 10 Phase

### Phase 1: 디렉토리 구조 생성

```
~/.claude/
├── agents/          ← 서브에이전트 20개
├── skills/          ← 스킬 27개 + chains/
├── commands/        ← 슬래시 커맨드 13개
├── hooks/           ← Hook 스크립트 8개
├── scripts/         ← Python/Bash 스크립트 13개
├── rules/           ← 규칙 파일 2개 (자동 로드)
├── workflow/        ← 워크플로우 템플릿
│   ├── templates/
│   └── instances/
├── eval/            ← 평가 시스템
├── templates/       ← 프로젝트 템플릿
│   └── rails8/
├── memory/          ← 메모리 저장소 (빈 디렉토리)
├── logs/            ← 로그 (빈 디렉토리)
├── plans/           ← 플랜 모드 (빈 디렉토리)
└── teams/           ← Agent Teams (빈 디렉토리)
```

### Phase 2: 핵심 설정 파일

| 파일 | 설명 | 경로 치환 |
|------|------|----------|
| CLAUDE.md | V5.1.0 가이드라인 | 불필요 |
| REVIEW.md | 코드 리뷰 규칙 (Critical/Warning/Info) | 불필요 |
| RAILS.md | Rails 8 개발 방법론 | 불필요 |
| settings.json | Hook/권한/MCP 설정 | **`__CLAUDE_HOME__` → 실제 경로로 치환** |
| statusline.sh | 상태줄 포매터 | 불필요 |

### Phase 3~9: 컴포넌트 복사

각 카테고리 파일을 대상 디렉토리에 복사. Hook 스크립트는 `chmod +x` 실행 권한 부여. Hook 내부의 하드코딩된 경로(`/Users/changjaeyou/.claude`)를 대상 경로로 치환.

### Phase 10: 온톨로지 서버 (선택)

벡터 메모리 시스템을 사용하려면 추가 설정 필요:

#### Step 1: Python 가상환경

```bash
python3.11 -m venv ~/.claude/venv
~/.claude/venv/bin/pip install qdrant-client sentence-transformers fastmcp
```

> Python 3.11+ 필수. sentence-transformers가 `intfloat/multilingual-e5-large` 모델을 사용.

#### Step 2: Docker Qdrant

```bash
# Qdrant 컨테이너 시작
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v ~/.claude/qdrant_data:/qdrant/storage \
  qdrant/qdrant

# 상태 확인
curl http://localhost:6333/healthz
```

#### Step 3: 초기 인덱싱

```bash
# 메모리 파일이 있으면 전체 인덱싱
~/.claude/venv/bin/python3 ~/.claude/scripts/memory_indexer.py --all
```

#### Step 4: 리콜 서버 테스트

```bash
# 리콜 서버 수동 시작 (정상 시 SessionStart Hook이 자동 시작)
~/.claude/venv/bin/python3 ~/.claude/scripts/memory_recall_server.py &

# 상태 확인
curl http://localhost:18765/health
# 응답: {"status": "ok", "model": "multilingual-e5-large"}
```

---

## 4. 설치 후 검증

### 4.1 기본 검증 체크리스트

```bash
# 1. CLAUDE.md 존재
cat ~/.claude/CLAUDE.md | head -3
# 기대: # CLAUDE.md - Claude Code Integrated Guidelines V5.1.0

# 2. rules/ 자동 로드
ls ~/.claude/rules/
# 기대: memory-protocol.md  orchestration.md

# 3. agents/ 수
ls ~/.claude/agents/*.md | wc -l
# 기대: 20

# 4. hooks/ 실행 권한
ls -la ~/.claude/hooks/*.sh | awk '{print $1, $NF}'
# 기대: -rwxr-xr-x 각각

# 5. settings.json 유효성
python3 -c "import json; json.load(open('$HOME/.claude/settings.json')); print('OK')"
# 기대: OK

# 6. settings.json 경로 치환 확인
grep "__CLAUDE_HOME__" ~/.claude/settings.json
# 기대: (출력 없음 — 모든 __CLAUDE_HOME__이 실제 경로로 치환됨)
```

### 4.2 기능 검증

```
Claude Code 시작 → "안녕" 입력
기대 응답: "🌟 안녕, 앤!"

"시스템 상태 알려줘" 입력
기대: 체인 시스템, Hook 상태 정보 출력

"이 버그 빨리 고쳐줘" 입력
기대: HotfixChain [LOW] 선택
```

### 4.3 온톨로지 검증 (Phase 10 완료 시)

```bash
# Qdrant 상태
curl http://localhost:6333/healthz
# 기대: {"title":"ok"}

# 리콜 서버
curl http://localhost:18765/health
# 기대: {"status":"ok","model":"multilingual-e5-large"}

# 벡터 검색 테스트
curl "http://localhost:18765/recall?q=test&top_k=1"
# 기대: JSON 배열 (메모리 파일 있으면 결과, 없으면 [])
```

---

## 5. 시스템 아키텍처 요약

```
┌─ CLAUDE.md (V5.1.0) ─ Identity + Principles + Settings Reference ─┐
│                                                                      │
├─ rules/orchestration.md ─ 체인 A~J + Teams + 워크플로우 §2.6 ──────┤
├─ rules/memory-protocol.md ─ 벡터 리콜 + 자동 인덱싱 파이프라인 ────┤
│                                                                      │
├─ agents/ (20) ─ Primary 14 + Eval 3 + Reviewer 3 (전부 Opus) ──────┤
├─ skills/ (27) ─ 공식 17 + 커스텀 10 + chains/ 2 ───────────────────┤
├─ hooks/  (8)  ─ 9개 이벤트 (UserPrompt/Pre/PostTool/Session/Stop..) ┤
├─ scripts/ (13) ─ 분석기 + 메모리 파이프라인 + 게이트 체커 ──────────┤
│                                                                      │
├─ [선택] Qdrant (Docker:6333) ─ 벡터 DB, 1024차원 ──────────────────┤
├─ [선택] Recall Server (:18765) ─ 상주 HTTP 리콜 ───────────────────┤
└─ [선택] Python venv ─ sentence-transformers + qdrant-client ────────┘
```

---

## 6. 커스터마이징 가이드

### 6.1 Identity 변경

`config/CLAUDE.md` §1의 Identity 테이블 수정:
```markdown
| **AI Partner** | 아리 (Ari) | → 원하는 이름으로 변경
| **User** | 앤 (An) | → 사용자 이름으로 변경
```

### 6.2 모델 변경

전 에이전트가 Opus로 설정됨. Sonnet으로 변경하려면:
```bash
# agents/ 내 모든 파일
sed -i '' 's/model: opus/model: sonnet/g' ~/.claude/agents/*.md
```

### 6.3 체인 커스터마이징

`rules/orchestration.md` §2.4의 체인 패턴 수정. 새 체인 추가 시 `skills/chains/`에 스킬 파일도 생성.

### 6.4 Hook 비활성화

`settings.json`에서 해당 Hook의 배열을 `[]`로 변경:
```json
"TeammateIdle": []
```

---

## 7. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| "🌟 안녕, 앤!" 안 나옴 | CLAUDE.md 미로드 | Claude Code 재시작 |
| Hook 분석 안 됨 | auto-analyze.sh 경로 오류 | settings.json의 경로 확인 |
| 리콜 안 됨 | Qdrant/리콜 서버 미실행 | Docker + recall_server 시작 |
| Permission denied | Hook 실행 권한 없음 | `chmod +x ~/.claude/hooks/*.sh` |
| settings.json 오류 | JSON 구문 오류 | `python3 -c "import json; json.load(open('settings.json'))"` |

---

*Claude Code System Package V5.1.0 — Installation Guide*
