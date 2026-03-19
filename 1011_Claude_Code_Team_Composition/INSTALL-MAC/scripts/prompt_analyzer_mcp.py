#!/usr/bin/env python3
"""
Claude Code Prompt Analyzer MCP Server

이 MCP 서버는 사용자 프롬프트를 4-Layer 분석하여
적절한 에이전트/스킬/체인을 추천합니다.

설치:
1. pip install mcp (또는 python3 -m venv ~/.claude/mcp-env && ~/.claude/mcp-env/bin/pip install mcp)
2. claude mcp add prompt-analyzer python ~/.claude/scripts/prompt_analyzer_mcp.py

사용:
Claude Code가 자동으로 analyze_prompt 도구를 호출합니다.

Version: 4.1 (V4.1 Full Sync — Chain/Agent/Skill/오탐방지/신뢰도)
Synced with: prompt_analyzer.py V3.0 + CLAUDE.md V4.1
Updated: 2026-02-07
"""

import re
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prompt-analyzer")

# ============================================================
# 키워드 매핑 데이터베이스 (prompt_analyzer.py V3.0 동기화)
# ============================================================

SKILL_KEYWORDS = {
    # 번역 관련
    "/translation-specialist": [
        "번역", "translation", "다국어", "multilingual",
        "영어로", "한국어로", "일본어로", "중국어로",
        "english", "korean", "japanese", "chinese",
        "언어 변환", "language", "localization", "현지화",
        "영문", "국문", "버전", "version",
    ],
    # 문서 관련
    "/docx": ["word", "docx", "문서", "document", "워드"],
    "/pdf": ["pdf", "추출", "extract pdf"],
    "/pptx": ["powerpoint", "pptx", "프레젠테이션", "presentation", "슬라이드", "slide"],
    "/xlsx": ["excel", "xlsx", "스프레드시트", "spreadsheet", "엑셀"],
    "/doc-coauthoring": ["협업 문서", "collaborative", "공동 작성", "co-authoring"],
    # 디자인 관련
    "/canvas-design": ["시각 디자인", "visual design", "캔버스", "canvas", "포스터", "poster", "아트"],
    "/frontend-design": ["프론트엔드", "frontend", "ui", "인터페이스", "interface", "웹 디자인"],
    "/theme-factory": ["테마", "theme", "스타일", "style", "팔레트", "palette"],
    "/algorithmic-art": ["알고리즘 아트", "algorithmic art", "p5.js", "제너레이티브", "generative"],
    "/brand-guidelines": ["브랜드", "brand", "anthropic 스타일", "anthropic style"],
    "/slack-gif-creator": ["gif", "slack gif", "애니메이션", "animation"],
    # 개발 관련
    "/webapp-testing": ["playwright", "웹앱 테스트", "webapp test", "e2e 테스트"],
    "/web-artifacts-builder": ["react", "아티팩트", "artifact", "shadcn"],
    "/mcp-builder": ["mcp", "mcp 서버", "model context protocol"],
    # Rails 관련
    "/rails-init": ["rails 초기화", "rails new", "레일즈 프로젝트"],
    "/rails-prd": ["prd", "요구사항 문서", "product requirements"],
    "/rails-plan": ["작업계획", "task plan", "태스크 분해"],
    "/rails-dev": ["rails 개발", "tdd 개발", "레일즈 구현"],
    "/rails-test": ["rspec", "rails 테스트", "레일즈 테스트"],
    "/rails-deploy": ["kamal", "배포", "deploy", "프로덕션 배포"],
    "/rails-verify": ["검증", "verify", "헬스체크", "스모크 테스트"],
    # 기타
    "/skill-creator": ["스킬 생성", "skill creation", "스킬 만들기", "create skill"],
    "/internal-comms": ["내부 커뮤니케이션", "internal comms", "보고서", "report"],
    "/memory-save": ["메모리 저장", "memory save", "기억 저장"],
}

AGENT_KEYWORDS = {
    # 인지 에이전트
    "multidimensional_analyst": [
        "분석", "analysis", "다차원", "multidimensional",
        "시스템 사고", "systems thinking", "심층 분석"
    ],
    "insight_explorer": [
        "인사이트", "insight", "패턴", "pattern",
        "관찰", "observation", "발견"
    ],
    "connection_creator": [
        "연결", "connection", "관계", "relationship",
        "은유", "metaphor", "비유"
    ],
    "problem_reframer": [
        "문제 재정의", "reframe", "관점 전환",
        "perspective shift", "다른 각도"
    ],
    "solution_innovator": [
        "솔루션", "solution", "혁신", "innovation",
        "아이디어", "idea", "창의", "creative"
    ],
    "insight_amplifier": [
        "심화", "deepen", "질문", "question",
        "why", "what-if", "왜"
    ],
    "learning_evolver": [
        "학습", "learning", "지식 격차", "knowledge gap",
        "메타인지", "metacognition", "공부"
    ],
    "complexity_resolver": [
        "복잡성", "complexity", "분해", "decompose",
        "시스템 해체", "breakdown", "단순화"
    ],
    "balanced_judge": [
        "의사결정", "decision", "판단", "judgment",
        "균형", "balance", "비교"
    ],
    "integrated_sage": [
        "통합", "integration", "지혜", "wisdom",
        "윤리", "ethics", "종합", "synthesis"
    ],
    # 역할 에이전트
    "requirements_analyst": [
        "요구사항", "requirements", "비즈니스 분석",
        "business analysis", "기능 정의"
    ],
    "system_architect": [
        "설계", "design", "아키텍처", "architecture",
        "clean", "solid", "구조 설계"
    ],
    "code_developer": [
        "개발", "develop", "코드", "code",
        "tdd", "구현", "implement", "코딩"
    ],
    "quality_reviewer": [
        "리뷰", "review", "코드 검토", "code review",
        "품질", "quality", "피드백"
    ],
    # 탐색 에이전트
    "Explore": [
        "코드베이스 탐색", "explore codebase", "파일 검색",
        "file search", "코드 찾기"
    ],
    "Plan": [
        "계획", "plan", "전략 설계", "strategy design",
        "구현 계획", "implementation plan"
    ],
}

# 체인 패턴 (A~J 전체 — CLAUDE.md V4.1 동기화)
CHAIN_PATTERNS = {
    # A. SystemDesignChain (시스템 설계)
    "SystemDesignChain": [
        "시스템 설계", "system design", "아키텍처 설계",
        "architecture design", "체인 개선", "chain improvement",
        "claude.md", "구조 개선", "restructure",
        "설계 리뷰", "design review", "시스템 개선",
        "리팩토링", "refactoring", "최적화", "optimize",
    ],
    # B. AutomationChain (자동화 개발)
    "AutomationChain": [
        "hook", "hooks", "mcp", "mcp 서버", "mcp server",
        "자동화", "automation", "스크립트", "script",
        "커스텀 커맨드", "custom command", "slash command",
        "워크플로우 자동화", "workflow automation",
    ],
    # C. GameDevChain (게임 개발)
    "GameDevChain": [
        "roblox", "로블록스", "게임 개발", "game development",
        "lua", "three.js", "webgl", "phaser",
        "게임 엔진", "game engine", "roblox studio",
    ],
    # D. DevChain (일반 개발)
    "DevChain": [
        "코드 개발", "code development", "api 설계",
        "api design", "시스템 구현", "system implementation",
        "새 기능", "new feature", "api 개발", "기능 개발",
        "기능 구현", "코드 작성", "백엔드 개발", "backend development",
    ],
    # E. ResearchChain (연구)
    "ResearchChain": [
        "조사", "research", "연구", "트렌드", "trend",
        "기술 분석", "적합성", "비교 분석",
    ],
    # F. DocChain+ (문서 — Solo/Collab 통합)
    "DocChain+": [
        "문서 생성", "create document", "문서 편집",
        "edit document", "문서 변환", "convert",
        "협업 문서", "collaborative document",
        "긴 형식 문서", "long-form document",
        "공동 작성", "co-authoring",
        "보고서", "report", "보고서 작성", "보고서 생성",
    ],
    # G. WebDevChain+ (웹 개발 — 디자인 통합)
    "WebDevChain+": [
        "웹 아티팩트", "web artifact", "프론트엔드 개발",
        "frontend dev", "웹앱 테스트", "webapp testing",
        "웹 디자인", "web design", "ui/ux",
        "시각 디자인", "visual design", "브랜딩", "branding",
    ],
    # H. MetaThinkChain (메타 사고)
    "MetaThinkChain": [
        "복잡한 분석", "complex analysis", "다차원적 관점",
        "multi-perspective", "창의적 솔루션", "creative solution",
        "심층 사고", "deep thinking", "메타 사고", "meta thinking",
        "새 기술 학습", "learn new tech", "지식 격차",
        "knowledge gap", "공부", "study", "배우기",
        "복잡한 의사결정", "complex decision", "리스크 평가",
        "risk assessment", "심층 분석",
        "혁신적", "innovative", "새로운 아이디어", "대안", "alternative",
        "왜", "what-if", "심화 분석", "깊이", "근본", "root cause",
    ],
    # I. RailsDevChain (Rails 8)
    "RailsDevChain": [
        "rails", "레일즈", "ruby on rails", "rails 8",
        "kamal", "바이브코딩", "vibe coding",
    ],
    # J. HotfixChain (긴급 수정)
    "HotfixChain": [
        "버그 수정", "bug fix", "긴급 문제", "urgent issue",
        "빠른 수정", "quick fix", "핫픽스", "hotfix",
        "급한", "즉시", "당장", "긴급",
    ],
}

# 화용적 분석을 위한 의도 패턴
INTENT_PATTERNS = {
    "translation": [
        r"(영어|한국어|일본어|중국어|english|korean|japanese|chinese)로\s*(만들어|변환|바꿔)",
        r"(영어|한국어|일본어|중국어|english|korean|japanese|chinese)\s*버전",
        r"영어.+한국어|한국어.+영어",
        r"번역",
        r"translate",
    ],
    "creation": [
        r"만들어|생성|작성|새로",
        r"create|generate|write|new",
    ],
    "analysis": [
        r"분석|검토|리뷰|조사",
        r"analyze|review|examine|research",
    ],
    "modification": [
        r"수정|변경|업데이트|고쳐",
        r"modify|change|update|edit|fix",
    ],
    "question": [
        r"뭐야|어떻게|왜|무엇|어디",
        r"what|how|why|where|which",
    ],
    "deployment": [
        r"배포|deploy|릴리즈|release",
        r"프로덕션|production|운영",
    ],
}

# 담화 분석을 위한 복잡도 지표
COMPLEXITY_INDICATORS = {
    "high": [
        "복잡", "complex", "어려운", "difficult",
        "다단계", "multi-step", "전체", "entire",
        "아키텍처", "architecture", "시스템", "system"
    ],
    "medium": [
        "몇 가지", "several", "여러", "multiple",
        "기능", "feature", "모듈", "module"
    ],
    "low": [
        "간단", "simple", "하나", "one", "single",
        "빠르게", "quickly", "briefly", "간략"
    ]
}

# ============================================================
# 제약 감지 패턴 (A-2-4)
# ============================================================

CONSTRAINT_PATTERNS = {
    "no_implementation": [
        r"작업하지\s*말고", r"구현하지\s*말고", r"코딩하지\s*말고",
        r"개발하지\s*말고", r"수정하지\s*말고",
        r"don'?t\s+(implement|code|build|develop)",
    ],
    "analysis_only": [
        r"분석만", r"분석\s*먼저", r"검토만", r"리뷰만",
        r"only\s+analy", r"just\s+analy",
    ],
    "show_first": [
        r"먼저\s*보여", r"보여\s*주기만", r"문서로만?\s*보여",
        r"show\s+first", r"just\s+show",
    ],
    "plan_only": [
        r"계획만", r"계획\s*먼저", r"설계만", r"전략만",
        r"plan\s+only", r"plan\s+first",
    ],
}

# ============================================================
# 메타 작업 키워드 (A-2-5)
# ============================================================

META_WORK_KEYWORDS = [
    "claude.md", "claude md", "hooks", "hook 개발", "hook 수정",
    "auto-analyze", "prompt_analyzer", "체인 시스템", "chain system",
    "settings.json", "설정 파일", "오케스트레이션", "orchestration",
    "에이전트 시스템", "agent system", "메모리 시스템", "memory system",
    "slash command", "커스텀 커맨드", "워크플로우 설계",
]

# ============================================================
# 상호 배제 그룹 (A-2-6)
# ============================================================

MUTUAL_EXCLUSION_GROUPS = {
    "document_creation": {"/docx", "/pdf", "/pptx", "/xlsx"},
    "translation": {"/translation-specialist"},
    "thinking": {
        "multidimensional_analyst", "insight_explorer", "balanced_judge",
        "integrated_sage", "solution_innovator", "insight_amplifier"
    },
    "development": {"code_developer", "system_architect"},
}

# ============================================================
# 컨텍스트 기반 오탐 방지 필터 (A-2-2, A-2-3)
# ============================================================

TRANSLATION_CONTEXT_REQUIRED = {"버전", "version"}
LANGUAGE_NAMES = {
    "영어", "한국어", "일본어", "중국어", "프랑스어", "독일어", "스페인어",
    "english", "korean", "japanese", "chinese", "french", "german", "spanish",
}

DOC_CONTEXT_KEYWORDS = {"문서"}
DOC_CREATION_VERBS = {"만들어", "생성", "작성", "변환", "내보내", "export", "만들"}
DOC_NON_CREATION_VERBS = {"보여", "확인", "읽어", "찾아", "검색", "열어", "보기"}

# 에이전트 → 체인 fallback (V4.1)
AGENT_CHAIN_FALLBACK = {
    "solution_innovator": "MetaThinkChain",
    "insight_amplifier": "MetaThinkChain",
}


# ============================================================
# 유틸리티 함수
# ============================================================

def get_context_window(prompt: str, keyword: str, window_size: int = 3) -> str:
    """키워드 주변 ±window_size 단어를 추출하여 컨텍스트 분석"""
    words = prompt.split()
    keyword_lower = keyword.lower()
    for i, word in enumerate(words):
        if keyword_lower in word.lower():
            start = max(0, i - window_size)
            end = min(len(words), i + window_size + 1)
            return " ".join(words[start:end])
    return ""


def detect_constraints(prompt: str) -> dict:
    """명시적 제약 조건 감지 (A-2-4)"""
    prompt_lower = prompt.lower()
    detected = []

    for constraint_type, patterns in CONSTRAINT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                detected.append(constraint_type)
                break

    return {
        "constraints": detected,
        "has_constraints": len(detected) > 0,
        "suppress_implementation": any(c in detected for c in ("no_implementation", "plan_only")),
        "suppress_action": any(c in detected for c in ("show_first", "analysis_only")),
    }


def detect_meta_work(prompt: str) -> dict:
    """Claude 시스템 자체 작업 감지 (A-2-5)"""
    prompt_lower = prompt.lower()
    detected_keywords = [kw for kw in META_WORK_KEYWORDS if kw in prompt_lower]
    is_meta = len(detected_keywords) > 0

    return {
        "is_meta_work": is_meta,
        "meta_keywords": detected_keywords,
        "recommended_chain": "SystemDesignChain" if is_meta else None,
    }


def filter_skill_by_context(prompt: str, skill: str, keyword: str) -> bool:
    """컨텍스트 기반 스킬 필터링 - True면 유지, False면 제거"""
    if skill == "/translation-specialist" and keyword in TRANSLATION_CONTEXT_REQUIRED:
        context = get_context_window(prompt, keyword)
        return any(lang in context.lower() for lang in LANGUAGE_NAMES)

    if skill == "/docx" and keyword in DOC_CONTEXT_KEYWORDS:
        context = get_context_window(prompt, keyword, window_size=4)
        has_creation = any(v in context for v in DOC_CREATION_VERBS)
        has_non_creation = any(v in context for v in DOC_NON_CREATION_VERBS)
        if has_non_creation and not has_creation:
            return False

    return True


def apply_mutual_exclusion(skills: list) -> list:
    """상호 배제 규칙 적용 (A-2-6)"""
    skill_names = set(skills)

    if skill_names & MUTUAL_EXCLUSION_GROUPS["translation"]:
        skills = [s for s in skills if s not in MUTUAL_EXCLUSION_GROUPS["document_creation"]]

    return skills


# ============================================================
# 4-Layer 분석 함수
# ============================================================

def analyze_lexical(prompt: str) -> dict:
    """Layer 1: 어휘적 분석"""
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


def analyze_syntactic(prompt: str) -> dict:
    """Layer 2: 통사적 분석"""
    is_question = any(q in prompt for q in [
        "?", "뭐야", "어떻게", "왜", "무엇", "어디", "언제",
        "how", "what", "why", "where", "when", "which"
    ])
    is_command = any(c in prompt for c in [
        "해줘", "해", "만들어", "생성", "작성", "실행", "보여줘",
        "create", "make", "do", "run", "show", "build"
    ])
    is_request = any(r in prompt for r in [
        "줄래", "줄 수", "가능해", "부탁", "원해",
        "please", "could you", "can you", "would you"
    ])

    return {
        "type": "question" if is_question else "command" if is_command else "request" if is_request else "statement",
        "word_count": len(prompt.split()),
        "has_code_block": '```' in prompt or '`' in prompt,
        "has_url": bool(re.search(r'https?://', prompt)),
    }


def analyze_discourse(prompt: str) -> dict:
    """Layer 3: 담화 분석"""
    prompt_lower = prompt.lower()

    complexity = "medium"
    for level, indicators in COMPLEXITY_INDICATORS.items():
        for indicator in indicators:
            if indicator in prompt_lower:
                complexity = level
                break
        if complexity != "medium":
            break

    scope = "single"
    if any(word in prompt_lower for word in ["전체", "entire", "모든", "all", "프로젝트", "project"]):
        scope = "project"
    elif any(word in prompt_lower for word in ["여러", "multiple", "몇", "several"]):
        scope = "multiple"

    is_multi_step = any(ind in prompt_lower for ind in [
        "그리고", "다음", "그 후", "먼저", "and then", "after that", "first", "then"
    ])

    return {
        "complexity": complexity,
        "scope": scope,
        "is_multi_step": is_multi_step,
    }


def analyze_pragmatic(prompt: str) -> dict:
    """Layer 4: 화용적 분석"""
    prompt_lower = prompt.lower()
    detected_intents = []

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                detected_intents.append(intent)
                break

    language_conversion = False
    source_lang = None
    target_lang = None

    lang_patterns = [
        (r"영어.+한국어|english.+korean", "영어", "한국어"),
        (r"한국어.+영어|korean.+english", "한국어", "영어"),
        (r"영어를.+한국어로", "영어", "한국어"),
        (r"한국어\s*버전", None, "한국어"),
        (r"영어\s*버전", None, "영어"),
        (r"일본어\s*버전", None, "일본어"),
        (r"중국어\s*버전", None, "중국어"),
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

    urgency = "normal"
    if any(word in prompt_lower for word in [
        "급해", "급한", "급하게", "급히", "urgent", "urgently",
        "빨리", "quickly", "asap", "지금 바로", "당장", "즉시",
        "immediately", "right now", "긴급", "emergency"
    ]):
        urgency = "high"
    elif any(word in prompt_lower for word in ["나중에", "천천히", "여유", "later", "take your time"]):
        urgency = "low"

    return {
        "intents": detected_intents,
        "language_conversion": language_conversion,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "urgency": urgency,
    }


# ============================================================
# MCP 도구
# ============================================================

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
    # 4-Layer 분석
    lexical = analyze_lexical(prompt)
    syntactic = analyze_syntactic(prompt)
    discourse = analyze_discourse(prompt)
    pragmatic = analyze_pragmatic(prompt)

    # Phase 0: 제약 감지 + 메타 작업 감지
    constraints = detect_constraints(prompt)
    meta = detect_meta_work(prompt)

    recommendation = {
        "recommended_skills": [],
        "recommended_agents": [],
        "recommended_chain": None,
        "chain_confidence": 0.0,
        "priority": "MEDIUM",
        "reasoning": [],
        "constraints": [],
        "filtered_out": [],
        "skill_scores": {},
        "agent_scores": {},
        "analysis": {
            "lexical": lexical,
            "syntactic": syntactic,
            "discourse": discourse,
            "pragmatic": pragmatic,
        }
    }

    if constraints["has_constraints"]:
        recommendation["constraints"] = constraints["constraints"]
        recommendation["reasoning"].append(f"제약 감지: {', '.join(constraints['constraints'])}")

    if meta["is_meta_work"]:
        recommendation["reasoning"].append(f"메타 작업 감지: {', '.join(meta['meta_keywords'][:3])}")

    # === 우선순위 1: 화용적 분석 — 신뢰도 0.95 ===
    if pragmatic.get("language_conversion"):
        recommendation["recommended_skills"].append("/translation-specialist")
        recommendation["skill_scores"]["/translation-specialist"] = 0.95
        recommendation["reasoning"].append(
            f"번역 의도 감지: {pragmatic.get('source_lang') or '원문'} → {pragmatic.get('target_lang') or '번역문'}"
        )
        recommendation["priority"] = "HIGH"

    if pragmatic.get("urgency") == "high":
        recommendation["priority"] = "HIGH"
        recommendation["reasoning"].append("긴급 요청 감지")

    # === 우선순위 2: 담화 분석 ===
    if discourse.get("complexity") == "high" or discourse.get("scope") == "project":
        recommendation["priority"] = "HIGH"
        recommendation["reasoning"].append(f"복잡도: {discourse.get('complexity')}, 범위: {discourse.get('scope')}")

    # === 우선순위 3: 어휘적 분석 + 컨텍스트 필터링 — 신뢰도 0.7 ===
    for skill_info in lexical.get("skills", []):
        skill_name = skill_info["name"]
        keyword = skill_info["keyword"]
        if skill_name in recommendation["recommended_skills"]:
            continue
        if not filter_skill_by_context(prompt, skill_name, keyword):
            recommendation["filtered_out"].append(f"{skill_name} (키워드 '{keyword}' 오탐 필터링)")
            continue
        recommendation["recommended_skills"].append(skill_name)
        recommendation["skill_scores"].setdefault(skill_name, 0.7)
        recommendation["reasoning"].append(f"키워드 '{keyword}' → {skill_name}")

    for agent_info in lexical.get("agents", []):
        agent_name = agent_info["name"]
        keyword = agent_info["keyword"]
        if constraints["suppress_implementation"] and agent_name == "code_developer":
            recommendation["filtered_out"].append(f"{agent_name} (제약: 구현 억제)")
            continue
        if constraints["suppress_action"] and agent_name == "code_developer":
            recommendation["filtered_out"].append(f"{agent_name} (제약: 행동 억제)")
            continue
        recommendation["recommended_agents"].append(agent_name)
        recommendation["agent_scores"].setdefault(agent_name, 0.7)
        recommendation["reasoning"].append(f"키워드 '{keyword}' → {agent_name}")

    # === 우선순위 4: 상호 배제 ===
    excluded_before = set(recommendation["recommended_skills"])
    recommendation["recommended_skills"] = apply_mutual_exclusion(recommendation["recommended_skills"])
    excluded = excluded_before - set(recommendation["recommended_skills"])
    if excluded:
        recommendation["filtered_out"].extend([f"{s} (상호 배제)" for s in excluded])

    # === 우선순위 4.5: 에이전트 → 체인 fallback ===
    for agent in recommendation["recommended_agents"]:
        if agent in AGENT_CHAIN_FALLBACK and not recommendation["recommended_chain"]:
            fallback_chain = AGENT_CHAIN_FALLBACK[agent]
            recommendation["recommended_chain"] = fallback_chain
            recommendation["chain_confidence"] = 0.7
            recommendation["reasoning"].append(f"체인 fallback: {agent} → {fallback_chain}")
            break

    # === 우선순위 5: 체인 추천 ===
    if meta["is_meta_work"]:
        recommendation["recommended_chain"] = "SystemDesignChain"
        recommendation["chain_confidence"] = 0.85
        recommendation["reasoning"].append("체인: SystemDesignChain (메타 작업 우선)")
    elif lexical.get("chains"):
        recommendation["recommended_chain"] = lexical["chains"][0]["name"]
        recommendation["chain_confidence"] = 0.8
        recommendation["reasoning"].append(f"체인 매칭: {lexical['chains'][0]['name']}")

    # 담화 복잡도 기반 fallback — 신뢰도 0.5
    if not recommendation["recommended_chain"]:
        if discourse.get("complexity") == "high":
            if "analysis" in pragmatic.get("intents", []):
                recommendation["recommended_chain"] = "MetaThinkChain"
                recommendation["chain_confidence"] = 0.5
            elif "creation" in pragmatic.get("intents", []):
                recommendation["recommended_chain"] = "DevChain"
                recommendation["chain_confidence"] = 0.5
        elif discourse.get("complexity") == "low":
            if "modification" in pragmatic.get("intents", []):
                recommendation["recommended_chain"] = "HotfixChain"
                recommendation["chain_confidence"] = 0.5

    # 제약 조건 시 체인 조정
    if constraints["suppress_implementation"] and recommendation["recommended_chain"] in ("DevChain", "HotfixChain"):
        recommendation["recommended_chain"] = "SystemDesignChain"
        recommendation["chain_confidence"] = 0.75
        recommendation["reasoning"].append("체인 조정: 제약으로 인해 SystemDesignChain 전환")

    # === 0.6 미만 추천 필터링 ===
    MIN_CONFIDENCE = 0.6
    recommendation["recommended_skills"] = [
        s for s in recommendation["recommended_skills"]
        if recommendation["skill_scores"].get(s, 0.7) >= MIN_CONFIDENCE
    ]
    recommendation["recommended_agents"] = [
        a for a in recommendation["recommended_agents"]
        if recommendation["agent_scores"].get(a, 0.7) >= MIN_CONFIDENCE
    ]
    if recommendation["recommended_chain"] and recommendation["chain_confidence"] < MIN_CONFIDENCE:
        recommendation["filtered_out"].append(
            f"{recommendation['recommended_chain']} (신뢰도 {recommendation['chain_confidence']:.1f} < {MIN_CONFIDENCE})"
        )
        recommendation["recommended_chain"] = None
        recommendation["chain_confidence"] = 0.0

    # === 최대 3개 추천 제한 ===
    MAX_RECOMMENDATIONS = 3
    all_items = []
    for s in recommendation["recommended_skills"]:
        all_items.append(("skill", s, recommendation["skill_scores"].get(s, 0.7)))
    for a in recommendation["recommended_agents"]:
        all_items.append(("agent", a, recommendation["agent_scores"].get(a, 0.7)))
    if recommendation["recommended_chain"]:
        all_items.append(("chain", recommendation["recommended_chain"], recommendation["chain_confidence"]))

    all_items.sort(key=lambda x: x[2], reverse=True)
    kept = all_items[:MAX_RECOMMENDATIONS]
    kept_skills = {item[1] for item in kept if item[0] == "skill"}
    kept_agents = {item[1] for item in kept if item[0] == "agent"}
    kept_chain = {item[1] for item in kept if item[0] == "chain"}

    for s in recommendation["recommended_skills"]:
        if s not in kept_skills:
            recommendation["filtered_out"].append(f"{s} (추천 3개 초과)")
    for a in recommendation["recommended_agents"]:
        if a not in kept_agents:
            recommendation["filtered_out"].append(f"{a} (추천 3개 초과)")

    recommendation["recommended_skills"] = [s for s in recommendation["recommended_skills"] if s in kept_skills]
    recommendation["recommended_agents"] = [a for a in recommendation["recommended_agents"] if a in kept_agents]
    if recommendation["recommended_chain"] and recommendation["recommended_chain"] not in kept_chain:
        recommendation["filtered_out"].append(f"{recommendation['recommended_chain']} (추천 3개 초과)")
        recommendation["recommended_chain"] = None

    return recommendation


if __name__ == "__main__":
    mcp.run()
