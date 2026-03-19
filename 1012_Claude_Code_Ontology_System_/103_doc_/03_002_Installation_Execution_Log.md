---
title: "V5.0 선행 설치 실행 로그 — 단계별 가이드 & 기록"
version: "1.0.0"
created: "2026-03-15"
updated: "2026-03-15"
tags: [claude-code, installation, execution-log, prerequisites, v5.0]
status: completed
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: 전체 선행 설치 완료 + 검증 올 그린

### 다음 작업 (TODO)
- [x] P1-1: Docker + Qdrant 설치 ✅
- [x] P1-2: Python venv + 패키지 설치 ✅ (pyenv 3.11.12 필요)
- [x] P1-3: 임베딩 모델 다운로드 ✅
- [x] P1-4: CLI 도구 (fswatch) ✅
- [x] P2: 디렉토리 4개 생성 ✅
- [x] P3: GitHub 계정 확인 ✅
- [x] P-검증: 전체 검증 올 그린 ✅
- [ ] **다음**: Phase 0 본작업 시작 (C3 CLAUDE.md 분리 + C4 Hook + C5 로그)

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 **설치 실행 로그**이다. 앤과 아리가 주고받은 내용을 순서대로 기록한다
> - 각 단계: 아리 가이드 → 앤 실행 → 결과 기록 → 오류 시 해결 과정도 기록
> - [[03_001_Prerequisites_Checklist|사전 준비 체크리스트]]가 설치 항목의 원본
> - 오류 발생 시 `### ❌ 오류 & 해결` 섹션에 상세 기록 → 향후 동일 오류 참조용

---

# V5.0 선행 설치 실행 로그

> **목적**: 선행 설치를 단계별로 실행하며, 가이드/명령어/결과/오류를 모두 기록
> **참조**: [[03_001_Prerequisites_Checklist|사전 준비 체크리스트 V1.2.0]]
> **실행 환경**: macOS, iTerm2 + tmux, Claude Code 동일 세션

---

## 실행 환경 확인

| 항목 | 값 |
|------|-----|
| OS | macOS Darwin |
| 터미널 | iTerm2 + tmux |
| Claude Code | 동일 tmux 세션 |
| 셸 | zsh |
| 시작 시간 | 2026-03-15 |

### 실행 주체 범례

| 아이콘 | 의미 |
|--------|------|
| 🖥️ | **터미널** — 앤이 tmux 별도 pane/탭에서 직접 실행 |
| 🤖 | **Claude Code** — 앤이 프롬프트로 지시, 아리가 실행 |
| 📋 | **아리 가이드** — 아리가 앤에게 다음 단계 안내 |
| ✅ | **성공** |
| ❌ | **오류 발생** → 해결 과정 기록 |

---

## Step 1: P1-1. Docker 확인 + Qdrant 설치

### 📋 아리 가이드

앤, 먼저 Docker가 실행 중인지 확인해야 합니다.

**🖥️ 터미널** (tmux 별도 pane에서) 아래 명령어를 실행해주세요:

```bash
docker info
```

**예상 결과**:
- ✅ 성공: `Server: Docker Desktop x.x.x` 등의 정보 출력
- ❌ 실패: `Cannot connect to the Docker daemon` → Docker Desktop 실행 필요

실패 시 이 명령어로 Docker Desktop을 실행하세요:
```bash
open /Applications/Docker.app
```
약 30초 대기 후 다시 `docker info` 실행.

---

### 앤 실행 결과

```
Client:
 Version:    28.3.0
 Context:    desktop-linux
 Plugins: (ai, buildx, cloud, compose, debug, desktop, extension, init, mcp, model, sbom, scout)

Server:
Cannot connect to the Docker daemon at unix:///Users/changjaeyou/.docker/run/docker.sock.
Is the docker daemon running?
```

**상태**: ⚠️ Client OK, Server 미실행

---

### ❌ 오류 & 해결

**오류**: Docker daemon 미실행 — Client v28.3.0 설치됨, Server 연결 불가
**해결**: Docker Desktop 앱 실행 필요

```bash
# 앤 실행:
open /Applications/Docker.app
# → 약 30초 대기 후 docker info 재실행
```

> [!note] 발견: Docker MCP Plugin v0.9.3
> `docker-mcp` 플러그인이 이미 설치되어 있음. 향후 C1 MCP 서버 연동 시 활용 가능성 검토.

---

**앤 실행**: `open /Applications/Docker.app` → Accept → Use recommended settings → Finish → Skip sign-in

**재확인 결과**:
```
docker info 2>/dev/null | grep "Server Version"
 Server Version: 28.3.0
```

**상태**: ✅ Docker Server 28.3.0 정상 실행

---

## Step 2: Qdrant 컨테이너 설치

> ⚠️ Step 1 완료 후 진행

### 📋 아리 가이드

Docker가 실행 중이면, Qdrant를 설치합니다.

**🖥️ 터미널**에서 아래 명령어를 **순서대로** 실행해주세요:

```bash
# 1. Qdrant 이미지 다운로드
docker pull qdrant/qdrant

# 2. 데이터 볼륨 디렉토리 생성
mkdir -p ~/.claude/qdrant_data

# 3. Qdrant 컨테이너 실행
docker run -d --name qdrant \
  -p 6333:6333 \
  -v ~/.claude/qdrant_data:/qdrant/storage \
  --restart unless-stopped \
  qdrant/qdrant

# 4. 실행 확인
docker ps | grep qdrant

# 5. 건강 체크
curl http://localhost:6333/healthz
```

**예상 결과**:
- `docker ps`: qdrant 컨테이너가 `Up` 상태
- `curl healthz`: 응답 반환 (빈 응답 또는 `ok`)

---

### 앤 실행 결과

```
$ mkdir -p ~/.claude/qdrant_data
$ docker run -d --name qdrant -p 6333:6333 -v ~/.claude/qdrant_data:/qdrant/storage --restart unless-stopped qdrant/qdrant

latest: Pulling from qdrant/qdrant (8 layers)
Status: Downloaded newer image for qdrant/qdrant:latest
Container ID: 4386a7c9fda7

$ docker ps | grep qdrant
4386a7c9fda7   qdrant/qdrant   Up 32 seconds   0.0.0.0:6333->6333/tcp

$ curl http://localhost:6333/healthz
healthz check passed
```

**상태**: ✅ 성공 — Qdrant 실행 중, 포트 6333, healthz 통과

---

### ❌ 오류 & 해결 (발생 시 기록)

> 오류 없음. 한 번에 성공.

**참고 — 흔한 오류 1**: `port 6333 already in use`
```bash
# 해결: 사용 중인 프로세스 확인
lsof -i :6333
# 또는 다른 포트 사용
docker run -d --name qdrant -p 6334:6333 ...
```

**흔한 오류 2**: `Conflict. The container name "/qdrant" is already in use`
```bash
# 해결: 기존 컨테이너 삭제 후 재실행
docker rm -f qdrant
# 다시 docker run 실행
```

---

## Step 3: P1-2. Python 가상환경 + 패키지 설치

> ⚠️ Step 2 완료 후 진행

### 📋 아리 가이드

Python 가상환경을 만들어 시스템 Python과 격리합니다.

**🖥️ 터미널**에서 아래 명령어를 **순서대로** 실행해주세요:

```bash
# 1. 가상환경 생성
python3 -m venv ~/.claude/venv

# 2. 가상환경 활성화
source ~/.claude/venv/bin/activate

# 3. pip 업그레이드
pip install --upgrade pip

# 4. 패키지 설치 (3개)
pip install sentence-transformers qdrant-client fastmcp

# 5. 설치 확인 (3개 모두 OK 출력되어야 함)
python3 -c "from sentence_transformers import SentenceTransformer; print('✅ sentence-transformers OK')"
python3 -c "from qdrant_client import QdrantClient; print('✅ qdrant-client OK')"
python3 -c "from fastmcp import FastMCP; print('✅ fastmcp OK')"
```

**예상 결과**: 3개 모두 `✅ ... OK` 출력

> [!warning] 설치 시간
> `sentence-transformers`는 `torch` 의존성 포함 (~2GB). 네트워크 속도에 따라 5~15분 소요.

---

### 앤 실행 결과

```
$ python3 -m venv ~/.claude/venv
$ source ~/.claude/venv/bin/activate
$ pip install --upgrade pip → Successfully installed pip-26.0.1
$ pip install sentence-transformers qdrant-client fastmcp

sentence-transformers: Downloading (OK)
qdrant-client: Downloading v1.16.1 (OK)
fastmcp: ERROR - No matching distribution found

ERROR: Could not find a version that satisfies the requirement fastmcp
(다수 패키지가 Requires-Python >=3.10 표시)
```

**상태**: ❌ 오류 — Python 3.9.6이 fastmcp의 최소 요구(3.10+)를 충족하지 못함

---

### ❌ 오류 & 해결

**오류**: `fastmcp`가 Python 3.10+ 필요. 현재 macOS 기본 Python은 3.9.6.
**근본 원인**: macOS Monterey/Ventura 기본 Python이 3.9.x로 고정되어 있음.
**해결**: `pyenv`로 Python 3.11 설치 → venv 재생성

---

## Step 3-b: Python 3.11 설치 (pyenv)

### 📋 아리 가이드

Python 3.9.6이 너무 오래됐습니다. `pyenv`로 3.11을 설치합니다.

**🖥️ 터미널**에서 순서대로 실행해주세요:

```bash
# 1. 기존 venv 삭제 (3.9로 만든 것)
deactivate
rm -rf ~/.claude/venv

# 2. pyenv 설치 (이미 있으면 스킵)
brew install pyenv

# 3. Python 3.11 설치
pyenv install 3.11.12

# 4. 이 셸에서 3.11 사용
eval "$(pyenv init -)"
pyenv shell 3.11.12

# 5. 버전 확인
python3 --version
# → Python 3.11.12 이어야 함
```

여기까지 실행하고 `python3 --version` 결과를 알려주세요!

### 앤 실행 결과 (Step 3-b 포함)

```
# Python 3.9.6 → fastmcp 설치 실패 (Requires-Python >=3.10)
# → pyenv로 Python 3.11.12 설치 → venv 재생성

$ brew install pyenv → pyenv 2.6.26 설치 완료
$ pyenv install 3.11.12 → Installed Python-3.11.12
$ eval "$(pyenv init -)" && pyenv shell 3.11.12
$ python3 --version → Python 3.11.12
$ ~/.pyenv/versions/3.11.12/bin/python3 -m venv ~/.claude/venv
$ source ~/.claude/venv/bin/activate
$ pip install --upgrade pip → pip-26.0.1
$ pip install sentence-transformers qdrant-client fastmcp

Successfully installed:
  sentence-transformers-5.3.0
  qdrant-client-1.17.1
  fastmcp-3.1.1
  torch-2.10.0
  (+ 74개 의존성 패키지)

$ python3 -c "..." 확인:
  ✅ sentence-transformers OK
  ✅ qdrant-client OK
  ✅ fastmcp OK
```

**상태**: ✅ 성공 — Python 3.11.12 + venv + 3개 패키지 설치 완료

---

## Step 4: P1-3. 임베딩 모델 다운로드

> ⚠️ Step 3 완료 후 진행 (venv 활성화 상태 유지)

### 📋 아리 가이드

임베딩 모델을 다운로드합니다. **약 1.1GB**이므로 시간이 좀 걸립니다.

**🖥️ 터미널** (venv 활성화 상태에서):

```bash
# venv가 활성화되어 있는지 확인 (프롬프트 앞에 (venv) 표시)
which python3
# → ~/.claude/venv/bin/python3 이어야 함

# 모델 다운로드 + 차원 확인
python3 -c "
from sentence_transformers import SentenceTransformer
print('모델 다운로드 중... (약 1.1GB)')
model = SentenceTransformer('intfloat/multilingual-e5-large')
dim = model.get_sentence_embedding_dimension()
print(f'✅ Model loaded: {dim} dims')

# 테스트 임베딩
vec = model.encode('테스트 메모리 검색')
print(f'✅ 벡터 생성 성공: {len(vec)} 차원, 첫 3값: {vec[:3]}')
"
```

**예상 결과**:
```
모델 다운로드 중... (약 1.1GB)
✅ Model loaded: 1024 dims
✅ 벡터 생성 성공: 1024 차원, 첫 3값: [0.023, -0.015, ...]
```

---

### 앤 실행 결과

터미널에서 들여쓰기/줄바꿈 오류 발생 → **🤖 Claude Code에서 직접 실행**

```
$ ~/.claude/venv/bin/python3 -c "..."

다운로드 중...
Loading weights: 100%|██████████| 391/391
Model loaded: 1024 dims
벡터 생성: 1024 차원
```

**상태**: ✅ 성공 — multilingual-e5-large 1024차원 임베딩 정상 동작

---

### ❌ 오류 & 해결

**오류 1**: 터미널에서 여러 줄 python3 -c 실행 시 `IndentationError: unexpected indent`
**원인**: 복사-붙여넣기 시 들여쓰기가 포함됨
**해결**: Claude Code Bash 도구로 직접 실행 (줄바꿈 없는 한 줄 명령)
**교훈**: 향후 여러 줄 Python은 `.py` 파일로 저장 후 실행하는 것이 안전

**참고 — 흔한 오류**: `OSError: Can't load tokenizer for 'intfloat/multilingual-e5-large'`
```bash
# 해결: 네트워크 문제 → HuggingFace 접속 확인
curl -s https://huggingface.co | head -1
# VPN 사용 중이면 해제 후 재시도
```

---

## Step 5: P1-4. CLI 도구 설치

> ⚠️ 선택 사항 — 건너뛸 수 있음

### 📋 아리 가이드

**🖥️ 터미널**:

```bash
# fswatch — 파일 변경 감시 (C1 자동 인덱싱에 사용)
brew install fswatch

# 확인
fswatch --version
```

**예상 결과**: `fswatch X.X.X` 버전 출력

---

### 앤 실행 결과

```
$ brew install fswatch
🍺 /opt/homebrew/Cellar/fswatch/1.18.3: 50 files, 1.3MB
```

**상태**: ✅ 성공 — fswatch 1.18.3

---

## Step 6: P2. 디렉토리 4개 생성

### 📋 아리 가이드

이 단계는 **🤖 Claude Code에서 실행**하겠습니다. 앤이 아래 프롬프트를 입력해주세요:

> **프롬프트**: "아래 디렉토리 4개를 생성해줘: ~/.claude/rules/, ~/.claude/logs/, ~/.claude/skills/chains/, ~/.claude/qdrant_data/"

또는 **🖥️ 터미널**에서 직접:

```bash
mkdir -p ~/.claude/rules ~/.claude/logs ~/.claude/skills/chains ~/.claude/qdrant_data
ls -la ~/.claude/ | grep -E "rules|logs|skills|qdrant"
```

**예상 결과**: 4개 디렉토리가 목록에 표시

---

### 앤 실행 결과

**🤖 Claude Code에서 실행**:

```
$ mkdir -p ~/.claude/rules ~/.claude/logs ~/.claude/skills/chains ~/.claude/qdrant_data
✅ 4개 디렉토리 생성 완료
  ~/.claude/logs
  ~/.claude/qdrant_data
  ~/.claude/rules
  ~/.claude/skills/chains
```

**상태**: ✅ 성공 — 4개 디렉토리 생성

---

## Step 7: P3. GitHub 계정 확인

### 📋 아리 가이드

**🖥️ 터미널** 또는 **🤖 Claude Code**:

```bash
gh auth status
```

**예상 결과**:
```
github.com
  ✓ Logged in to github.com account XXX
```

---

### 앤 실행 결과

**🤖 Claude Code에서 실행**:

```
$ gh auth status
github.com
  ✓ Logged in to github.com account AnsibleMage (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token scopes: 'delete_repo', 'gist', 'read:org', 'repo', 'workflow'
```

**상태**: ✅ 성공 — GitHub AnsibleMage 계정 로그인 확인

---

## Step 8: P-검증. 전체 검증 스크립트

> ⚠️ Step 1~7 모두 완료 후 실행

### 📋 아리 가이드

모든 선행 작업이 완료되었는지 한 번에 검증합니다.

**🖥️ 터미널**:

```bash
echo "=== V5.0 선행 작업 검증 ==="
echo ""
echo "[P1-1] Docker + Qdrant..."
docker info > /dev/null 2>&1 && echo "  ✅ Docker 실행 중" || echo "  ❌ Docker 미실행"
curl -s http://localhost:6333/healthz > /dev/null 2>&1 && echo "  ✅ Qdrant 응답" || echo "  ❌ Qdrant 미응답"

VENV_PY="$HOME/.claude/venv/bin/python3"
echo "[P1-2] Python 패키지..."
$VENV_PY -c "from sentence_transformers import SentenceTransformer" 2>/dev/null && echo "  ✅ sentence-transformers" || echo "  ❌ sentence-transformers"
$VENV_PY -c "from qdrant_client import QdrantClient" 2>/dev/null && echo "  ✅ qdrant-client" || echo "  ❌ qdrant-client"
$VENV_PY -c "from fastmcp import FastMCP" 2>/dev/null && echo "  ✅ fastmcp" || echo "  ❌ fastmcp"

echo "[P1-3] 임베딩 모델..."
$VENV_PY -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large')" 2>/dev/null && echo "  ✅ multilingual-e5-large" || echo "  ❌ 모델 미다운로드"

echo "[P1-4] CLI..."
command -v fswatch > /dev/null && echo "  ✅ fswatch" || echo "  ⚠️ fswatch (선택)"

echo "[P2] 디렉토리..."
[ -d ~/.claude/rules ] && echo "  ✅ rules/" || echo "  ❌ rules/"
[ -d ~/.claude/logs ] && echo "  ✅ logs/" || echo "  ❌ logs/"
[ -d ~/.claude/skills/chains ] && echo "  ✅ skills/chains/" || echo "  ❌ skills/chains/"
[ -d ~/.claude/qdrant_data ] && echo "  ✅ qdrant_data/" || echo "  ❌ qdrant_data/"

echo "[P3] 계정..."
gh auth status > /dev/null 2>&1 && echo "  ✅ GitHub 로그인" || echo "  ❌ GitHub 미로그인"

echo ""
echo "=== 검증 완료 ==="
```

**예상 결과**: 모든 항목이 ✅

---

### 앤 실행 결과

**🤖 Claude Code에서 실행**:

```
=== V5.0 선행 작업 검증 ===

[P1-1] Docker + Qdrant...
  ✅ Docker 실행 중
  ✅ Qdrant 응답
[P1-2] Python 패키지...
  ✅ sentence-transformers
  ✅ qdrant-client
  ✅ fastmcp
[P1-3] 임베딩 모델...
  ✅ multilingual-e5-large
[P1-4] CLI...
  ✅ fswatch
[P2] 디렉토리...
  ✅ rules/
  ✅ logs/
  ✅ skills/chains/
  ✅ qdrant_data/
[P3] 계정...
  ✅ GitHub 로그인

=== 검증 완료 ===
```

**상태**: ✅ **전체 검증 통과 — 올 그린!**

---

## 최종 결과 요약

| Step | 작업 | 상태 | 실행 주체 | 비고 |
|------|------|------|----------|------|
| 1 | Docker 확인 | ✅ | 🖥️ 터미널 | Server 28.3.0, Accept+Finish 필요 |
| 2 | Qdrant 설치 | ✅ | 🖥️ 터미널 | 포트 6333, healthz 통과 |
| 3 | Python venv + 패키지 | ✅ | 🖥️ 터미널 | 3.9.6 오류 → pyenv 3.11.12로 해결 |
| 4 | 임베딩 모델 | ✅ | 🤖 Claude Code | 터미널 IndentationError → CC에서 실행 |
| 5 | CLI (fswatch) | ✅ | 🖥️ 터미널 | 1.18.3 |
| 6 | 디렉토리 4개 | ✅ | 🤖 Claude Code | rules, logs, chains, qdrant_data |
| 7 | GitHub 계정 | ✅ | 🤖 Claude Code | AnsibleMage 계정 |
| 8 | 전체 검증 | ✅ | 🤖 Claude Code | **올 그린** |

**전체 선행 완료 여부**: ✅ **완료!** → Phase 0 시작 가능

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[03_001_Prerequisites_Checklist#2. 선행 작업 체크리스트|선행 체크리스트]] — 설치 항목 원본
- [[03_001_Prerequisites_Checklist#7. 충돌 예상 지점|충돌 예상]] — 설치 중 주의사항
- [[02_001_C1_Ontology_Memory_Deep_Design#3.1 벡터 DB: Qdrant 선정|Qdrant 선정 근거]] — 왜 Qdrant인지

### 역참조 (Backlinks)
- [[01_001_Improvement_Direction_Overview#5. 실행 순서 권고|Phase 0]] — 선행 완료 후 Phase 0 시작

### 관련 주제 (Topic Links)
- [[02_001_C1_Ontology_Memory_Deep_Design#4.7 저장 용량 추정|용량 추정]] — Qdrant 디스크 사용량 참조
- [[02_001_C1_Ontology_Memory_Deep_Design#3.2 임베딩 모델|임베딩 모델]] — multilingual-e5-large 선정 이유

---

## Release Notes

### v1.0.0 (2026-03-15)
- 초기 작성: 8단계 설치 실행 로그 구조 생성
- 각 단계: 📋 아리 가이드 → 앤 실행 결과 → ❌ 오류 & 해결 구조
- 흔한 오류 사전 기록 (Docker 포트 충돌, Python 빌드 에러, 네트워크 등)
- 최종 결과 요약 테이블 + 검증 스크립트
> **프롬프트:** "설치는 내가 너에게 1번부터 순서대로 어떻게 어느걸 실행해야할지 묻고 넌 나에게 대답해줘 그럼 내가 그걸 터미널이나 클로드코드에서 실행해달라고 해. 난 터미널에서 한걸 너에게 알려주고 확인해 달라고 할거야. 내가 너에게 입력한 프롬프트를 시작으로 너가 나에게 준 가이드. 내가 다시 너에게 준 실행결과 혹은 클로드코드 실행 결과를 문서에 저장할 수 있게 순서별로 해당 섹션을 추가해줘"
