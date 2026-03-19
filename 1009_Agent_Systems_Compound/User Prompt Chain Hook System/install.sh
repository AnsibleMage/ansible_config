#!/bin/bash
# ============================================================
# User Prompt Chain Hook System - Auto Installer
# ============================================================
#
# 이 스크립트는 4-Layer 프롬프트 분석 시스템을 자동으로 설치합니다.
#
# Usage: ./install.sh
#
# Version: 1.0
# Updated: 2026-02-04
# ============================================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  User Prompt Chain Hook System Installer${NC}"
echo -e "${BLUE}  4-Layer Prompt Analysis for Claude Code${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# 현재 스크립트 위치
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# ============================================================
# 1. 요구 사항 확인
# ============================================================

echo -e "${YELLOW}[1/6]${NC} 요구 사항 확인 중..."

# Python 3 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3가 설치되어 있지 않습니다.${NC}"
    echo "   설치: brew install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "   ✅ Python: $PYTHON_VERSION"

# jq 확인
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ jq가 설치되어 있지 않습니다.${NC}"
    echo "   설치: brew install jq"
    exit 1
fi
JQ_VERSION=$(jq --version 2>&1)
echo -e "   ✅ jq: $JQ_VERSION"

# Claude Code 확인 (선택적)
if command -v claude &> /dev/null; then
    echo -e "   ✅ Claude Code: 설치됨"
else
    echo -e "   ${YELLOW}⚠️  Claude Code CLI가 PATH에 없습니다 (계속 진행)${NC}"
fi

echo ""

# ============================================================
# 2. 디렉토리 생성
# ============================================================

echo -e "${YELLOW}[2/6]${NC} 디렉토리 생성 중..."

mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/scripts"

echo -e "   ✅ $CLAUDE_DIR/hooks"
echo -e "   ✅ $CLAUDE_DIR/scripts"
echo ""

# ============================================================
# 3. 파일 복사
# ============================================================

echo -e "${YELLOW}[3/6]${NC} 파일 복사 중..."

# Hook 스크립트 복사
if [ -f "$SCRIPT_DIR/hooks/auto-analyze.sh" ]; then
    cp "$SCRIPT_DIR/hooks/auto-analyze.sh" "$CLAUDE_DIR/hooks/"
    chmod +x "$CLAUDE_DIR/hooks/auto-analyze.sh"
    echo -e "   ✅ hooks/auto-analyze.sh"
else
    echo -e "${RED}❌ hooks/auto-analyze.sh 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# 분석기 스크립트 복사
if [ -f "$SCRIPT_DIR/scripts/prompt_analyzer.py" ]; then
    cp "$SCRIPT_DIR/scripts/prompt_analyzer.py" "$CLAUDE_DIR/scripts/"
    chmod +x "$CLAUDE_DIR/scripts/prompt_analyzer.py"
    echo -e "   ✅ scripts/prompt_analyzer.py"
else
    echo -e "${RED}❌ scripts/prompt_analyzer.py 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# MCP 서버 복사 (선택적)
if [ -f "$SCRIPT_DIR/scripts/prompt_analyzer_mcp.py" ]; then
    cp "$SCRIPT_DIR/scripts/prompt_analyzer_mcp.py" "$CLAUDE_DIR/scripts/"
    chmod +x "$CLAUDE_DIR/scripts/prompt_analyzer_mcp.py"
    echo -e "   ✅ scripts/prompt_analyzer_mcp.py"
fi

echo ""

# ============================================================
# 4. 경로 치환
# ============================================================

echo -e "${YELLOW}[4/6]${NC} 경로 설정 중..."

# auto-analyze.sh 내 경로를 현재 사용자 경로로 변경
sed -i '' "s|/Users/changjaeyou|$HOME|g" "$CLAUDE_DIR/hooks/auto-analyze.sh"
echo -e "   ✅ Hook 스크립트 경로 업데이트 완료"
echo ""

# ============================================================
# 5. settings.json 설정
# ============================================================

echo -e "${YELLOW}[5/6]${NC} settings.json 설정 중..."

SETTINGS_FILE="$CLAUDE_DIR/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    # 기존 설정 백업
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%Y%m%d%H%M%S)"
    echo -e "   ✅ 기존 설정 백업 완료"

    # UserPromptSubmit Hook이 이미 있는지 확인
    if jq -e '.hooks.UserPromptSubmit' "$SETTINGS_FILE" > /dev/null 2>&1; then
        echo -e "   ${YELLOW}⚠️  UserPromptSubmit Hook이 이미 존재합니다. 스킵합니다.${NC}"
    else
        # UserPromptSubmit Hook 추가
        TEMP_FILE=$(mktemp)
        jq --arg hook_path "$CLAUDE_DIR/hooks/auto-analyze.sh" \
           '.hooks.UserPromptSubmit = [{"hooks": [{"type": "command", "command": $hook_path}]}]' \
           "$SETTINGS_FILE" > "$TEMP_FILE"
        mv "$TEMP_FILE" "$SETTINGS_FILE"
        echo -e "   ✅ UserPromptSubmit Hook 추가 완료"
    fi
else
    # 새 settings.json 생성
    if [ -f "$SCRIPT_DIR/templates/settings.json.template" ]; then
        cp "$SCRIPT_DIR/templates/settings.json.template" "$SETTINGS_FILE"
        sed -i '' "s|YOUR_USERNAME|$(whoami)|g" "$SETTINGS_FILE"
        echo -e "   ✅ 새 settings.json 생성 완료"
    else
        # 최소 설정 생성
        cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_DIR/hooks/auto-analyze.sh"
          }
        ]
      }
    ]
  }
}
EOF
        echo -e "   ✅ 최소 settings.json 생성 완료"
    fi
fi

echo ""

# ============================================================
# 6. 설치 확인
# ============================================================

echo -e "${YELLOW}[6/6]${NC} 설치 확인 중..."

# Hook 테스트
echo -e "   테스트: Hook 스크립트..."
TEST_RESULT=$(echo '{"prompt": "테스트 프롬프트입니다 분석해줘"}' | "$CLAUDE_DIR/hooks/auto-analyze.sh" 2>&1)

if echo "$TEST_RESULT" | grep -q "4-LAYER PROMPT ANALYSIS"; then
    echo -e "   ✅ Hook 스크립트 정상 동작"
else
    echo -e "   ${YELLOW}⚠️  Hook 테스트 실패 (수동 확인 필요)${NC}"
fi

# 분석기 테스트
echo -e "   테스트: 분석기 스크립트..."
ANALYZER_RESULT=$(echo "React로 투두리스트 만들어줘" | python3 "$CLAUDE_DIR/scripts/prompt_analyzer.py" 2>&1)

if echo "$ANALYZER_RESULT" | grep -q "RECOMMENDATION"; then
    echo -e "   ✅ 분석기 스크립트 정상 동작"
else
    echo -e "   ${YELLOW}⚠️  분석기 테스트 실패 (수동 확인 필요)${NC}"
fi

echo ""

# ============================================================
# 완료
# ============================================================

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  ✅ 설치 완료!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "설치된 파일:"
echo "  - $CLAUDE_DIR/hooks/auto-analyze.sh"
echo "  - $CLAUDE_DIR/scripts/prompt_analyzer.py"
echo "  - $CLAUDE_DIR/settings.json"
echo ""
echo -e "${BLUE}다음 단계:${NC}"
echo "  1. Claude Code를 재시작하세요"
echo "  2. 아무 프롬프트나 입력하여 분석 결과를 확인하세요"
echo ""
echo -e "문제가 있으면 ${YELLOW}INSTALL.md${NC}의 문제 해결 섹션을 참조하세요."
echo ""
echo -e "Made with 🎵 by Ari & An"
echo ""
