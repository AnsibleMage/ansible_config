#!/bin/bash
# ============================================================
# Claude Code System Package — Installer V5.1.0
# ============================================================
# 앤(An)의 Claude Code 오케스트레이션 시스템을 새 환경에 설치
#
# 사용법:
#   bash install.sh [--target ~/.claude] [--skip-ontology] [--dry-run]
#
# 옵션:
#   --target <path>     설치 경로 (기본: ~/.claude)
#   --skip-ontology     온톨로지 서버(Qdrant/venv) 설정 스킵
#   --dry-run           실제 파일 복사 없이 계획만 출력
#   --force             기존 파일 덮어쓰기 (기본: 백업 후 덮어쓰기)
# ============================================================

set -e

# 기본값
TARGET="$HOME/.claude"
SKIP_ONTOLOGY=false
DRY_RUN=false
FORCE=false
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 인자 파싱
while [[ $# -gt 0 ]]; do
    case $1 in
        --target) TARGET="$2"; shift 2 ;;
        --skip-ontology) SKIP_ONTOLOGY=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        --force) FORCE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "============================================================"
echo " Claude Code System Package Installer V5.1.0"
echo "============================================================"
echo " 설치 경로: $TARGET"
echo " 온톨로지: $([ "$SKIP_ONTOLOGY" = true ] && echo 'SKIP' || echo 'INSTALL')"
echo " 모드: $([ "$DRY_RUN" = true ] && echo 'DRY RUN' || echo 'LIVE')"
echo "============================================================"
echo ""

# ---- Phase 1: 디렉토리 생성 ----
echo "[Phase 1] 디렉토리 구조 생성..."

DIRS=(
    "$TARGET"
    "$TARGET/agents"
    "$TARGET/skills"
    "$TARGET/commands"
    "$TARGET/hooks"
    "$TARGET/scripts"
    "$TARGET/rules"
    "$TARGET/workflow/templates"
    "$TARGET/workflow/instances"
    "$TARGET/eval"
    "$TARGET/templates/rails8"
    "$TARGET/memory"
    "$TARGET/logs"
    "$TARGET/plans"
    "$TARGET/teams"
)

for dir in "${DIRS[@]}"; do
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY] mkdir -p $dir"
    else
        mkdir -p "$dir"
    fi
done
echo "  ✅ $([ "$DRY_RUN" = true ] && echo '(dry)' || echo 'Done')"

# ---- Phase 2: 핵심 설정 파일 ----
echo "[Phase 2] 핵심 설정 파일 복사..."

copy_file() {
    local src="$1"
    local dst="$2"
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY] $src → $dst"
        return
    fi
    if [ -f "$dst" ] && [ "$FORCE" != true ]; then
        cp "$dst" "${dst}.bak.$(date +%Y%m%d%H%M%S)"
        echo "  ⚠️  기존 파일 백업: ${dst}.bak.*"
    fi
    cp "$src" "$dst"
}

# CLAUDE.md, REVIEW.md, RAILS.md, CHANGELOG.md, statusline.sh
for f in CLAUDE.md REVIEW.md RAILS.md CHANGELOG.md statusline.sh; do
    if [ -f "$SCRIPT_DIR/config/$f" ]; then
        copy_file "$SCRIPT_DIR/config/$f" "$TARGET/$f"
    fi
done

# settings.json — 경로 치환
if [ -f "$SCRIPT_DIR/config/settings.json.template" ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY] settings.json.template → $TARGET/settings.json (경로 치환)"
    else
        sed "s|__CLAUDE_HOME__|$TARGET|g" "$SCRIPT_DIR/config/settings.json.template" > "$TARGET/settings.json"
        echo "  ✅ settings.json (경로: $TARGET)"
    fi
fi
echo "  ✅ 핵심 설정 완료"

# ---- Phase 3: Rules ----
echo "[Phase 3] Rules 복사..."
for f in "$SCRIPT_DIR/rules/"*.md; do
    [ -f "$f" ] && copy_file "$f" "$TARGET/rules/$(basename "$f")"
done
echo "  ✅ $(ls "$SCRIPT_DIR/rules/"*.md 2>/dev/null | wc -l | tr -d ' ') files"

# ---- Phase 4: Agents ----
echo "[Phase 4] Agents 복사..."
for f in "$SCRIPT_DIR/agents/"*.md; do
    [ -f "$f" ] && copy_file "$f" "$TARGET/agents/$(basename "$f")"
done
echo "  ✅ $(ls "$SCRIPT_DIR/agents/"*.md 2>/dev/null | wc -l | tr -d ' ') agents"

# ---- Phase 5: Skills ----
echo "[Phase 5] Skills 복사..."
if [ "$DRY_RUN" = true ]; then
    echo "  [DRY] cp -r skills/* → $TARGET/skills/"
else
    cp -r "$SCRIPT_DIR/skills/"* "$TARGET/skills/" 2>/dev/null || true
fi
echo "  ✅ $(ls -d "$SCRIPT_DIR/skills/"*/ 2>/dev/null | wc -l | tr -d ' ') skill dirs"

# ---- Phase 6: Commands ----
echo "[Phase 6] Commands 복사..."
for f in "$SCRIPT_DIR/commands/"*; do
    [ -f "$f" ] && copy_file "$f" "$TARGET/commands/$(basename "$f")"
done
echo "  ✅ $(ls "$SCRIPT_DIR/commands/"* 2>/dev/null | wc -l | tr -d ' ') commands"

# ---- Phase 7: Hooks ----
echo "[Phase 7] Hooks 복사 + 실행 권한..."
for f in "$SCRIPT_DIR/hooks/"*.sh; do
    [ -f "$f" ] && copy_file "$f" "$TARGET/hooks/$(basename "$f")"
done
if [ "$DRY_RUN" != true ]; then
    chmod +x "$TARGET/hooks/"*.sh 2>/dev/null
fi

# Hook 내부 경로 치환
if [ "$DRY_RUN" != true ]; then
    for f in "$TARGET/hooks/"*.sh; do
        if grep -q "/Users/changjaeyou" "$f" 2>/dev/null; then
            sed -i '' "s|/Users/changjaeyou/.claude|$TARGET|g" "$f" 2>/dev/null || true
        fi
    done
fi
echo "  ✅ $(ls "$SCRIPT_DIR/hooks/"*.sh 2>/dev/null | wc -l | tr -d ' ') hooks"

# ---- Phase 8: Scripts ----
echo "[Phase 8] Scripts 복사..."
for f in "$SCRIPT_DIR/scripts/"*; do
    [ -f "$f" ] && copy_file "$f" "$TARGET/scripts/$(basename "$f")"
done
if [ "$DRY_RUN" != true ]; then
    chmod +x "$TARGET/scripts/"*.sh 2>/dev/null || true
fi
echo "  ✅ $(ls "$SCRIPT_DIR/scripts/"* 2>/dev/null | wc -l | tr -d ' ') scripts"

# ---- Phase 9: Workflow + Eval + Templates ----
echo "[Phase 9] Workflow, Eval, Templates..."
cp "$SCRIPT_DIR/workflow/templates/"*.md "$TARGET/workflow/templates/" 2>/dev/null || true
touch "$TARGET/workflow/instances/.gitkeep"
cp "$SCRIPT_DIR/eval/"*.json "$TARGET/eval/" 2>/dev/null || true
cp "$SCRIPT_DIR/templates/rails8/"* "$TARGET/templates/rails8/" 2>/dev/null || true
echo "  ✅ Done"

# ---- Phase 10: 온톨로지 서버 (선택) ----
if [ "$SKIP_ONTOLOGY" = true ]; then
    echo "[Phase 10] 온톨로지 설정 SKIP (--skip-ontology)"
else
    echo "[Phase 10] 온톨로지 서버 설정 가이드..."
    echo ""
    echo "  📋 온톨로지 서버 수동 설정이 필요합니다:"
    echo ""
    echo "  Step 1: Python 가상환경 생성"
    echo "    python3.11 -m venv $TARGET/venv"
    echo "    $TARGET/venv/bin/pip install qdrant-client sentence-transformers fastmcp"
    echo ""
    echo "  Step 2: Docker Qdrant 시작"
    echo "    docker run -d --name qdrant -p 6333:6333 -v $TARGET/qdrant_data:/qdrant/storage qdrant/qdrant"
    echo ""
    echo "  Step 3: 초기 메모리 인덱싱"
    echo "    $TARGET/venv/bin/python3 $TARGET/scripts/memory_indexer.py --all"
    echo ""
    echo "  Step 4: 리콜 서버 테스트"
    echo "    curl http://localhost:6333/healthz"
    echo "    $TARGET/venv/bin/python3 $TARGET/scripts/memory_recall_server.py &"
    echo "    curl 'http://localhost:18765/health'"
    echo ""
fi

# ---- 검증 ----
echo ""
echo "============================================================"
echo " 설치 검증"
echo "============================================================"

PASS=true
check() {
    if [ -e "$1" ]; then
        echo "  ✅ $2"
    else
        echo "  ❌ $2 — $1"
        PASS=false
    fi
}

check "$TARGET/CLAUDE.md" "CLAUDE.md (V5.1.0)"
check "$TARGET/settings.json" "settings.json"
check "$TARGET/rules/orchestration.md" "orchestration.md"
check "$TARGET/rules/memory-protocol.md" "memory-protocol.md"
check "$TARGET/hooks/auto-analyze.sh" "auto-analyze.sh"
check "$TARGET/hooks/session-start.sh" "session-start.sh"
check "$TARGET/scripts/prompt_analyzer.py" "prompt_analyzer.py"
check "$TARGET/agents" "agents/ 디렉토리"
check "$TARGET/skills" "skills/ 디렉토리"

echo ""
if [ "$PASS" = true ]; then
    echo "🎉 설치 완료! Claude Code를 재시작하세요."
else
    echo "⚠️  일부 항목이 누락되었습니다. 로그를 확인하세요."
fi

echo ""
echo "  다음 단계:"
echo "  1. Claude Code 재시작 (새 설정 로드)"
echo "  2. '안녕' 입력하여 시스템 정상 동작 확인"
echo "  3. 온톨로지 필요 시 Phase 10 가이드 수동 실행"
echo ""
