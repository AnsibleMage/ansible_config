#!/Users/changjaeyou/.claude/mcp-env/bin/python3.12
"""
Claude Code Prompt Analyzer MCP Server

이 MCP 서버는 사용자 프롬프트를 4-Layer 분석하여
적절한 에이전트/스킬/체인을 추천합니다.

설치:
1. pip install mcp
2. claude mcp add prompt-analyzer python /Users/changjaeyou/.claude/scripts/prompt_analyzer_mcp.py

사용:
Claude Code가 자동으로 analyze_prompt 도구를 호출합니다.
"""

import re
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prompt-analyzer")

# ============================================================
# 키워드 매핑 데이터베이스
# ============================================================

SKILL_KEYWORDS = {
    "/translation-specialist": [
        "번역", "translation", "다국어", "multilingual",
        "영어로", "한국어로", "일본어로", "중국어로",
        "english", "korean", "japanese", "chinese",
        "언어 변환", "language", "localization", "현지화",
        "영문", "국문", "버전", "version",
    ],
    "/docx": ["word", "docx", "문서", "document", "워드"],
    "/pdf": ["pdf", "추출", "extract"],
    "/pptx": ["powerpoint", "pptx", "프레젠테이션", "presentation", "슬라이드", "slide"],
    "/xlsx": ["excel", "xlsx", "스프레드시트", "spreadsheet", "엑셀"],
    "/doc-coauthoring": ["협업 문서", "collaborative", "공동 작성", "co-authoring"],
    "/canvas-design": ["시각 디자인", "visual design", "캔버스", "canvas", "포스터", "poster"],
    "/frontend-design": ["프론트엔드", "frontend", "ui", "인터페이스", "interface"],
    "/theme-factory": ["테마", "theme", "스타일", "style", "팔레트", "palette"],
    "/algorithmic-art": ["알고리즘 아트", "algorithmic art", "p5.js", "제너레이티브", "generative"],
    "/brand-guidelines": ["브랜드", "brand", "anthropic 스타일", "anthropic style"],
    "/slack-gif-creator": ["gif", "slack", "애니메이션", "animation"],
    "/webapp-testing": ["테스트", "test", "playwright", "자동화", "automation"],
    "/web-artifacts-builder": ["react", "아티팩트", "artifact", "shadcn"],
    "/mcp-builder": ["mcp", "서버", "server", "프로토콜", "protocol"],
    "/skill-creator": ["스킬 생성", "skill creation", "스킬 만들기", "create skill"],
    "/internal-comms": ["내부 커뮤니케이션", "internal comms", "보고서", "report"],
}

AGENT_KEYWORDS = {
    "multidimensional_analyst": ["분석", "analysis", "다차원", "multidimensional", "시스템 사고"],
    "insight_explorer": ["인사이트", "insight", "패턴", "pattern", "관찰"],
    "connection_creator": ["연결", "connection", "관계", "relationship", "은유", "metaphor"],
    "problem_reframer": ["문제 재정의", "reframe", "관점 전환", "perspective shift"],
    "solution_innovator": ["솔루션", "solution", "혁신", "innovation", "아이디어", "창의"],
    "insight_amplifier": ["심화", "deepen", "질문", "why", "what-if"],
    "learning_evolver": ["학습", "learning", "지식 격차", "knowledge gap"],
    "complexity_resolver": ["복잡성", "complexity", "분해", "decompose"],
    "balanced_judge": ["의사결정", "decision", "판단", "judgment", "균형"],
    "integrated_sage": ["통합", "integration", "지혜", "wisdom", "윤리"],
    "requirements_analyst": ["요구사항", "requirements", "비즈니스 분석"],
    "system_architect": ["설계", "design", "아키텍처", "architecture", "clean", "solid"],
    "code_developer": ["개발", "develop", "코드", "code", "tdd", "구현"],
    "quality_reviewer": ["리뷰", "review", "코드 검토", "품질", "quality"],
    "Explore": ["코드베이스 탐색", "explore codebase", "파일 검색"],
    "Plan": ["계획", "plan", "전략 설계", "구현 계획"],
}

CHAIN_PATTERNS = {
    "DevChain": ["코드 개발", "code development", "api 설계", "시스템 구현"],
    "ThinkChain": ["복잡한 분석", "complex analysis", "다차원적 관점", "창의적 솔루션"],
    "FastTrack": ["버그 수정", "bug fix", "긴급 문제", "urgent issue", "빠른 수정"],
    "LearnChain": ["새 기술 학습", "learn new tech", "지식 격차", "공부"],
    "DecisionChain": ["복잡한 의사결정", "complex decision", "리스크 평가"],
    "DocChain": ["문서 생성", "create document", "문서 편집", "변환"],
    "DesignChain": ["시각 디자인", "visual design", "브랜딩", "ui 디자인"],
    "WebDevChain": ["웹 아티팩트", "web artifact", "프론트엔드", "웹앱 테스트"],
    "CollabChain": ["긴 형식 문서", "long-form document", "반복 협업"],
}

INTENT_PATTERNS = {
    "translation": [
        r"(.+)로\s*(만들어|변환|바꿔)",
        r"(.+)\s*버전",
        r"영어.+한국어|한국어.+영어",
        r"번역",
        r"translate",
    ],
    "creation": [r"만들어|생성|작성", r"create|generate|write"],
    "analysis": [r"분석|검토|리뷰", r"analyze|review|examine"],
    "modification": [r"수정|변경|업데이트", r"modify|change|update|edit"],
}


def analyze_lexical(prompt: str) -> dict:
    """어휘적 분석"""
    prompt_lower = prompt.lower()
    result = {"skills": [], "agents": [], "chains": []}

    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                result["skills"].append({"name": skill, "keyword": keyword})
                break

    for agent, keywords in AGENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                result["agents"].append({"name": agent, "keyword": keyword})
                break

    for chain, keywords in CHAIN_PATTERNS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                result["chains"].append({"name": chain, "keyword": keyword})
                break

    return result


def analyze_pragmatic(prompt: str) -> dict:
    """화용적 분석"""
    prompt_lower = prompt.lower()
    result = {
        "intents": [],
        "language_conversion": False,
        "source_lang": None,
        "target_lang": None,
    }

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                result["intents"].append(intent)
                break

    # 언어 변환 감지
    lang_patterns = [
        (r"영어.+한국어|english.+korean", "영어", "한국어"),
        (r"한국어.+영어|korean.+english", "한국어", "영어"),
        (r"영어를.+한국어로", "영어", "한국어"),
        (r"한국어\s*버전", None, "한국어"),
        (r"english\s*version", None, "영어"),
    ]

    for pattern, src, tgt in lang_patterns:
        if re.search(pattern, prompt_lower):
            result["language_conversion"] = True
            result["source_lang"] = src
            result["target_lang"] = tgt
            if "translation" not in result["intents"]:
                result["intents"].append("translation")
            break

    return result


@mcp.tool()
def analyze_prompt(prompt: str) -> dict:
    """
    사용자 프롬프트를 4-Layer 분석하여 적절한 에이전트/스킬/체인을 추천합니다.

    이 도구는 모든 사용자 요청에 대해 먼저 호출하여
    최적의 처리 방법을 결정하는 데 사용됩니다.

    Args:
        prompt: 분석할 사용자 프롬프트

    Returns:
        분석 결과 및 추천 (skills, agents, chain, priority, reasoning)
    """
    lexical = analyze_lexical(prompt)
    pragmatic = analyze_pragmatic(prompt)

    # 추천 생성
    recommendation = {
        "recommended_skills": [],
        "recommended_agents": [],
        "recommended_chain": None,
        "priority": "MEDIUM",
        "reasoning": [],
        "analysis": {
            "lexical": lexical,
            "pragmatic": pragmatic,
        }
    }

    # 화용적 분석 우선
    if pragmatic.get("language_conversion") or "translation" in pragmatic.get("intents", []):
        recommendation["recommended_skills"].append("/translation-specialist")
        recommendation["reasoning"].append(
            f"🔴 HIGH PRIORITY: 번역 의도 감지 ({pragmatic.get('source_lang', '?')} → {pragmatic.get('target_lang', '?')})"
        )
        recommendation["priority"] = "HIGH"

    # 어휘적 분석 추가
    for skill in lexical.get("skills", []):
        if skill["name"] not in recommendation["recommended_skills"]:
            recommendation["recommended_skills"].append(skill["name"])
            recommendation["reasoning"].append(f"키워드 '{skill['keyword']}' → {skill['name']}")

    for agent in lexical.get("agents", []):
        recommendation["recommended_agents"].append(agent["name"])
        recommendation["reasoning"].append(f"키워드 '{agent['keyword']}' → {agent['name']}")

    if lexical.get("chains"):
        recommendation["recommended_chain"] = lexical["chains"][0]["name"]
        recommendation["reasoning"].append(f"체인 매칭: {lexical['chains'][0]['name']}")

    return recommendation


if __name__ == "__main__":
    mcp.run()
