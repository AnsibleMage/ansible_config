#!/usr/bin/env python3
"""
Claude Code 4-Layer Prompt Analyzer
사용자 프롬프트를 분석하여 적절한 에이전트/스킬/체인을 추천

Usage:
    echo "프롬프트" | python prompt_analyzer.py
    python prompt_analyzer.py "프롬프트"
"""

import sys
import json
import re
from typing import Dict, List, Tuple, Optional

# ============================================================
# 키워드 매핑 데이터베이스
# ============================================================

SKILL_KEYWORDS = {
    # 번역 관련 - 다양한 표현 포함
    "/translation-specialist": [
        "번역", "translation", "다국어", "multilingual",
        "영어로", "한국어로", "일본어로", "중국어로",
        "english", "korean", "japanese", "chinese",
        "언어 변환", "language", "localization", "현지화",
        "영문", "국문", "버전", "version",  # "한국어 버전" 감지
    ],
    # 문서 관련
    "/docx": ["word", "docx", "문서", "document", "워드"],
    "/pdf": ["pdf", "추출", "extract"],
    "/pptx": ["powerpoint", "pptx", "프레젠테이션", "presentation", "슬라이드", "slide"],
    "/xlsx": ["excel", "xlsx", "스프레드시트", "spreadsheet", "엑셀"],
    "/doc-coauthoring": ["협업 문서", "collaborative", "공동 작성", "co-authoring"],
    # 디자인 관련
    "/canvas-design": ["시각 디자인", "visual design", "캔버스", "canvas", "포스터", "poster"],
    "/frontend-design": ["프론트엔드", "frontend", "ui", "인터페이스", "interface"],
    "/theme-factory": ["테마", "theme", "스타일", "style", "팔레트", "palette"],
    "/algorithmic-art": ["알고리즘 아트", "algorithmic art", "p5.js", "제너레이티브", "generative"],
    "/brand-guidelines": ["브랜드", "brand", "anthropic 스타일", "anthropic style"],
    "/slack-gif-creator": ["gif", "slack", "애니메이션", "animation"],
    # 개발 관련
    "/webapp-testing": ["테스트", "test", "playwright", "자동화", "automation"],
    "/web-artifacts-builder": ["react", "아티팩트", "artifact", "shadcn"],
    "/mcp-builder": ["mcp", "서버", "server", "프로토콜", "protocol"],
    # 기타
    "/skill-creator": ["스킬 생성", "skill creation", "스킬 만들기", "create skill"],
    "/internal-comms": ["내부 커뮤니케이션", "internal comms", "보고서", "report"],
}

AGENT_KEYWORDS = {
    # 인지 에이전트
    "multidimensional_analyst": ["분석", "analysis", "다차원", "multidimensional", "시스템 사고", "systems thinking"],
    "insight_explorer": ["인사이트", "insight", "패턴", "pattern", "관찰", "observation"],
    "connection_creator": ["연결", "connection", "관계", "relationship", "은유", "metaphor"],
    "problem_reframer": ["문제 재정의", "reframe", "관점 전환", "perspective shift"],
    "solution_innovator": ["솔루션", "solution", "혁신", "innovation", "아이디어", "idea", "창의", "creative"],
    "insight_amplifier": ["심화", "deepen", "질문", "question", "why", "what-if"],
    "learning_evolver": ["학습", "learning", "지식 격차", "knowledge gap", "메타인지", "metacognition"],
    "complexity_resolver": ["복잡성", "complexity", "분해", "decompose", "시스템 해체", "breakdown"],
    "balanced_judge": ["의사결정", "decision", "판단", "judgment", "균형", "balance"],
    "integrated_sage": ["통합", "integration", "지혜", "wisdom", "윤리", "ethics", "종합", "synthesis"],
    # 역할 에이전트
    "requirements_analyst": ["요구사항", "requirements", "비즈니스 분석", "business analysis"],
    "system_architect": ["설계", "design", "아키텍처", "architecture", "clean", "solid"],
    "code_developer": ["개발", "develop", "코드", "code", "tdd", "구현", "implement"],
    "quality_reviewer": ["리뷰", "review", "코드 검토", "code review", "품질", "quality"],
    "quality_manager": ["품질 관리", "quality management", "검증", "verification", "프로세스", "process"],
    # 탐색 에이전트
    "Explore": ["코드베이스 탐색", "explore codebase", "파일 검색", "file search"],
    "Plan": ["계획", "plan", "전략 설계", "strategy design", "구현 계획", "implementation plan"],
}

CHAIN_PATTERNS = {
    "DevChain": ["코드 개발", "code development", "api 설계", "api design", "시스템 구현", "system implementation"],
    "ThinkChain": ["복잡한 분석", "complex analysis", "다차원적 관점", "multi-perspective", "창의적 솔루션", "creative solution"],
    "FastTrack": ["버그 수정", "bug fix", "긴급 문제", "urgent issue", "빠른 수정", "quick fix"],
    "LearnChain": ["새 기술 학습", "learn new tech", "지식 격차", "knowledge gap", "공부", "study"],
    "DecisionChain": ["복잡한 의사결정", "complex decision", "리스크 평가", "risk assessment"],
    "DocChain": ["문서 생성", "create document", "문서 편집", "edit document", "변환", "convert"],
    "DesignChain": ["시각 디자인", "visual design", "브랜딩", "branding", "ui 디자인"],
    "WebDevChain": ["웹 아티팩트", "web artifact", "프론트엔드", "frontend", "웹앱 테스트", "webapp testing"],
    "CollabChain": ["긴 형식 문서", "long-form document", "반복 협업", "iterative collaboration"],
}

# 화용적 분석을 위한 의도 패턴
INTENT_PATTERNS = {
    "translation": [
        r"(.+)로\s*(만들어|변환|바꿔)",  # "한국어로 만들어"
        r"(.+)\s*버전",  # "한국어 버전"
        r"영어.+한국어|한국어.+영어",  # 언어 간 변환
        r"번역",
        r"translate",
    ],
    "creation": [
        r"만들어|생성|작성",
        r"create|generate|write",
    ],
    "analysis": [
        r"분석|검토|리뷰",
        r"analyze|review|examine",
    ],
    "modification": [
        r"수정|변경|업데이트",
        r"modify|change|update|edit",
    ],
}


def analyze_lexical(prompt: str) -> Dict:
    """어휘적 분석: 키워드, 도메인 용어 추출"""
    prompt_lower = prompt.lower()

    matched_skills = []
    matched_agents = []
    matched_chains = []

    # 스킬 매칭
    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                matched_skills.append((skill, keyword))
                break

    # 에이전트 매칭
    for agent, keywords in AGENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                matched_agents.append((agent, keyword))
                break

    # 체인 매칭
    for chain, keywords in CHAIN_PATTERNS.items():
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                matched_chains.append((chain, keyword))
                break

    return {
        "skills": matched_skills,
        "agents": matched_agents,
        "chains": matched_chains,
    }


def analyze_syntactic(prompt: str) -> Dict:
    """통사적 분석: 문장 구조, 요청 유형"""
    # 질문형
    is_question = any(q in prompt for q in ["?", "뭐야", "어떻게", "왜", "무엇", "how", "what", "why"])

    # 명령형
    is_command = any(c in prompt for c in ["해줘", "해", "만들어", "생성", "작성", "create", "make", "do"])

    # 요청형
    is_request = any(r in prompt for r in ["줄래", "줄 수", "가능해", "부탁", "please", "could you"])

    return {
        "type": "question" if is_question else "command" if is_command else "request" if is_request else "statement",
        "is_question": is_question,
        "is_command": is_command,
        "is_request": is_request,
    }


def analyze_pragmatic(prompt: str) -> Dict:
    """화용적 분석: 실제 의도, 암묵적 필요"""
    prompt_lower = prompt.lower()

    detected_intents = []

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                detected_intents.append(intent)
                break

    # 특수 패턴 감지: 언어 변환
    language_conversion = False
    source_lang = None
    target_lang = None

    # "영어 → 한국어" 패턴 감지
    lang_patterns = [
        (r"영어.+한국어|english.+korean", "영어", "한국어"),
        (r"한국어.+영어|korean.+english", "한국어", "영어"),
        (r"영어를.+한국어로", "영어", "한국어"),
        (r"한국어\s*버전", None, "한국어"),  # "한국어 버전" = 번역 필요
        (r"english\s*version", None, "영어"),
    ]

    for pattern, src, tgt in lang_patterns:
        if re.search(pattern, prompt_lower):
            language_conversion = True
            source_lang = src
            target_lang = tgt
            if "translation" not in detected_intents:
                detected_intents.append("translation")
            break

    return {
        "intents": detected_intents,
        "language_conversion": language_conversion,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }


def generate_recommendation(lexical: Dict, syntactic: Dict, pragmatic: Dict) -> Dict:
    """분석 결과를 종합하여 추천 생성"""
    recommendations = {
        "skills": [],
        "agents": [],
        "chain": None,
        "priority": "MEDIUM",
        "reasoning": [],
    }

    # 화용적 분석 우선 (실제 의도가 가장 중요)
    if pragmatic.get("language_conversion") or "translation" in pragmatic.get("intents", []):
        recommendations["skills"].append("/translation-specialist")
        recommendations["reasoning"].append(
            f"🔴 번역 의도 감지: {pragmatic.get('source_lang', '?')} → {pragmatic.get('target_lang', '?')}"
        )
        recommendations["priority"] = "HIGH"

    # 어휘적 분석 결과 추가
    for skill, keyword in lexical.get("skills", []):
        if skill not in recommendations["skills"]:
            recommendations["skills"].append(skill)
            recommendations["reasoning"].append(f"키워드 '{keyword}' → {skill}")

    for agent, keyword in lexical.get("agents", []):
        recommendations["agents"].append(agent)
        recommendations["reasoning"].append(f"키워드 '{keyword}' → {agent}")

    # 체인 추천
    if lexical.get("chains"):
        recommendations["chain"] = lexical["chains"][0][0]
        recommendations["reasoning"].append(f"체인 매칭: {lexical['chains'][0][0]}")

    return recommendations


def analyze_prompt(prompt: str) -> str:
    """메인 분석 함수"""
    # 4-Layer 분석 실행
    lexical = analyze_lexical(prompt)
    syntactic = analyze_syntactic(prompt)
    pragmatic = analyze_pragmatic(prompt)

    # 추천 생성
    recommendation = generate_recommendation(lexical, syntactic, pragmatic)

    # 결과 포맷팅
    output = []
    output.append("=" * 60)
    output.append("🔍 4-LAYER PROMPT ANALYSIS")
    output.append("=" * 60)

    # 어휘적 분석
    output.append("\n📝 [1] 어휘적 분석 (Lexical)")
    if lexical["skills"]:
        output.append(f"   스킬 감지: {', '.join([s[0] for s in lexical['skills']])}")
    if lexical["agents"]:
        output.append(f"   에이전트 감지: {', '.join([a[0] for a in lexical['agents']])}")
    if lexical["chains"]:
        output.append(f"   체인 감지: {', '.join([c[0] for c in lexical['chains']])}")
    if not any([lexical["skills"], lexical["agents"], lexical["chains"]]):
        output.append("   (직접 키워드 매칭 없음)")

    # 통사적 분석
    output.append(f"\n📐 [2] 통사적 분석 (Syntactic)")
    output.append(f"   요청 유형: {syntactic['type']}")

    # 화용적 분석
    output.append(f"\n🎯 [3] 화용적 분석 (Pragmatic)")
    if pragmatic["intents"]:
        output.append(f"   감지된 의도: {', '.join(pragmatic['intents'])}")
    if pragmatic["language_conversion"]:
        output.append(f"   🔴 언어 변환 감지: {pragmatic['source_lang'] or '?'} → {pragmatic['target_lang']}")

    # 추천
    output.append(f"\n" + "=" * 60)
    output.append("💡 RECOMMENDATION")
    output.append("=" * 60)

    if recommendation["skills"]:
        output.append(f"   📌 권장 스킬: {', '.join(recommendation['skills'])}")
    if recommendation["agents"]:
        output.append(f"   📌 권장 에이전트: {', '.join(recommendation['agents'])}")
    if recommendation["chain"]:
        output.append(f"   📌 권장 체인: {recommendation['chain']}")

    output.append(f"\n   우선순위: {recommendation['priority']}")

    if recommendation["reasoning"]:
        output.append("\n   근거:")
        for reason in recommendation["reasoning"]:
            output.append(f"   - {reason}")

    output.append("=" * 60)

    return "\n".join(output)


if __name__ == "__main__":
    # 입력 받기
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = sys.stdin.read().strip()

    if prompt:
        result = analyze_prompt(prompt)
        print(result)
    else:
        print("Usage: echo '프롬프트' | python prompt_analyzer.py")
        print("   or: python prompt_analyzer.py '프롬프트'")
