#!/usr/bin/env python3
"""
Claude Code 4-Layer Prompt Analyzer
사용자 프롬프트를 분석하여 적절한 에이전트/스킬/체인을 추천

Based on: translation-specialist 4-Layer 언어학적 분석
- Layer 1: Lexical (어휘) - 키워드, 도메인 용어
- Layer 2: Syntactic (통사) - 문장 구조, 요청 유형
- Layer 3: Discourse (담화) - 컨텍스트, 복잡도, 텍스트 구조
- Layer 4: Pragmatic (화용) - 실제 의도, 암묵적 요구

Usage:
    echo "프롬프트" | python prompt_analyzer.py
    python prompt_analyzer.py "프롬프트"

Version: 4.0 (V4.2 Improvement: Korean Keywords + Path Filter + Verb Priority + Simple Task + Urgency + Parallel Intent)
Updated: 2026-02-07
"""

import sys
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

# 체인 패턴 (A~J 전체 - V3.0, CLAUDE.md V4.0 동기화)
CHAIN_PATTERNS = {
    # A. SystemDesignChain (시스템 설계) — 가장 빈번한 작업
    "SystemDesignChain": [
        "시스템 설계", "system design", "아키텍처 설계",
        "architecture design", "체인 개선", "chain improvement",
        "claude.md", "구조 개선", "restructure",
        "설계 리뷰", "design review", "시스템 개선",
        "리팩토링", "refactoring", "최적화", "optimize",
    ],
    # B. AutomationChain (자동화 개발) — 두 번째 빈번
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
        "멀티플레이어", "랭킹", "리더보드", "상점", "인게임",
        "스폰", "레벨", "npc", "보스", "퀘스트", "인벤토리",
        "게임 로직", "게임 시스템", "luau",
    ],
    # D. DevChain (일반 개발)
    "DevChain": [
        "코드 개발", "code development", "api 설계",
        "api design", "시스템 구현", "system implementation",
        "새 기능", "new feature", "api 개발", "기능 개발",
        "기능 구현", "코드 작성", "백엔드 개발", "backend development",
        "tdd", "테스트", "리팩토링", "기능추가", "구현", "코딩",
        "단위 테스트", "통합 테스트", "엔드포인트",
    ],
    # E. ResearchChain (연구)
    "ResearchChain": [
        "조사", "research", "연구", "트렌드", "trend",
        "기술 분석", "적합성", "비교 분석",
        "리서치", "벤치마크", "성공요인", "사례연구",
        "비교분석", "장단점", "현황", "동향",
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
        "모달", "modal", "수집", "collect", "폼", "form", "입력", "제출",
    ],
    # H. MetaThinkChain (메타 사고 — ThinkChain+LearnChain+DecisionChain 통합)
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
    # J. HotfixChain (긴급 수정 — 구 FastTrack)
    "HotfixChain": [
        "버그 수정", "bug fix", "긴급 문제", "urgent issue",
        "빠른 수정", "quick fix", "핫픽스", "hotfix",
        "급한", "즉시", "당장", "긴급",
        "크래시", "실패", "오류", "에러", "간헐적",
        "crash", "error", "broken", "fails",
    ],
}

# 화용적 분석을 위한 의도 패턴
INTENT_PATTERNS = {
    "translation": [
        # 언어 변환 패턴만 감지 (PDF, Word 등 파일 형식 제외)
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

# "버전" 오탐 방지: 주변에 언어명이 있어야 번역 추천
TRANSLATION_CONTEXT_REQUIRED = {"버전", "version"}
LANGUAGE_NAMES = {
    "영어", "한국어", "일본어", "중국어", "프랑스어", "독일어", "스페인어",
    "english", "korean", "japanese", "chinese", "french", "german", "spanish",
}

# "문서" 오탐 방지: 동사에 따라 분기
DOC_CONTEXT_KEYWORDS = {"문서"}
DOC_CREATION_VERBS = {"만들어", "생성", "작성", "변환", "내보내", "export", "만들"}
DOC_NON_CREATION_VERBS = {"보여", "확인", "읽어", "찾아", "검색", "열어", "보기"}


# ============================================================
# 유틸리티 함수
# ============================================================

def preprocess_prompt(prompt: str) -> str:
    """파일 경로를 [PATH]로 치환하여 키워드 오탐 방지 (Q4-2)"""
    # /path/to/file.ext, ~/path/to/file, ./relative/path 패턴
    path_pattern = r'(?:~|\.)?/[\w\-./]+\.\w+'
    return re.sub(path_pattern, '[PATH]', prompt)


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


def detect_constraints(prompt: str) -> Dict:
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


def detect_meta_work(prompt: str) -> Dict:
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
    """컨텍스트 기반 스킬 필터링 - True면 유지, False면 제거 (A-2-2, A-2-3)"""
    # A-2-2: "버전/version" → 주변 언어명 확인 필수
    if skill == "/translation-specialist" and keyword in TRANSLATION_CONTEXT_REQUIRED:
        context = get_context_window(prompt, keyword)
        return any(lang in context.lower() for lang in LANGUAGE_NAMES)

    # A-2-3: "문서" → 동사 분석
    if skill == "/docx" and keyword in DOC_CONTEXT_KEYWORDS:
        context = get_context_window(prompt, keyword, window_size=4)
        has_creation = any(v in context for v in DOC_CREATION_VERBS)
        has_non_creation = any(v in context for v in DOC_NON_CREATION_VERBS)
        if has_non_creation and not has_creation:
            return False  # "문서로 보여줘" → 문서 생성 아님

    return True  # 기본: 유지


def apply_mutual_exclusion(skills: list, primary_intent: Optional[str]) -> list:
    """상호 배제 규칙 적용 (A-2-6)"""
    skill_names = {s[0] for s in skills}

    # 번역 감지 시 문서 생성 스킬 제거
    if skill_names & MUTUAL_EXCLUSION_GROUPS["translation"]:
        skills = [s for s in skills if s[0] not in MUTUAL_EXCLUSION_GROUPS["document_creation"]]

    return skills


# ============================================================
# Layer 1: Lexical Analysis (어휘 분석)
# ============================================================

def analyze_lexical(prompt: str) -> Dict:
    """어휘 분석: 키워드, 도메인 용어 추출"""
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


# ============================================================
# Layer 2: Syntactic Analysis (통사 분석)
# ============================================================

def analyze_syntactic(prompt: str) -> Dict:
    """통사 분석: 문장 구조, 요청 유형"""

    # 질문형
    is_question = any(q in prompt for q in [
        "?", "뭐야", "어떻게", "왜", "무엇", "어디", "언제",
        "how", "what", "why", "where", "when", "which"
    ])

    # 명령형
    is_command = any(c in prompt for c in [
        "해줘", "해", "만들어", "생성", "작성", "실행", "보여줘",
        "create", "make", "do", "run", "show", "build"
    ])

    # 요청형
    is_request = any(r in prompt for r in [
        "줄래", "줄 수", "가능해", "부탁", "원해",
        "please", "could you", "can you", "would you"
    ])

    # 문장 길이 분석
    words = prompt.split()
    word_count = len(words)

    # 구조적 마커
    has_numbering = bool(re.search(r'^\s*\d+\.', prompt, re.MULTILINE) or
                         re.search(r'[①-⑳]', prompt))
    has_code_block = '```' in prompt or '`' in prompt
    has_url = bool(re.search(r'https?://', prompt))

    return {
        "type": "question" if is_question else "command" if is_command else "request" if is_request else "statement",
        "is_question": is_question,
        "is_command": is_command,
        "is_request": is_request,
        "word_count": word_count,
        "has_numbering": has_numbering,
        "has_code_block": has_code_block,
        "has_url": has_url,
    }


# ============================================================
# Layer 3: Discourse Analysis (담화 분석)
# ============================================================

def analyze_discourse(prompt: str) -> Dict:
    """담화 분석: 컨텍스트, 복잡도, 텍스트 구조"""
    prompt_lower = prompt.lower()

    # 복잡도 판단
    complexity = "medium"  # 기본값

    for level, indicators in COMPLEXITY_INDICATORS.items():
        for indicator in indicators:
            if indicator in prompt_lower:
                complexity = level
                break
        if complexity != "medium":
            break

    # 컨텍스트 참조 감지 (이전 대화 참조)
    context_references = []
    context_patterns = [
        (r"이전|앞서|위에서|아까", "previous_mention"),
        (r"계속|이어서|추가로", "continuation"),
        (r"그것|그거|저것|이것", "pronoun_reference"),
        (r"위 내용|해당|그|저", "demonstrative"),
    ]

    for pattern, ref_type in context_patterns:
        if re.search(pattern, prompt_lower):
            context_references.append(ref_type)

    has_context_dependency = len(context_references) > 0

    # 작업 범위 추정
    scope = "single"  # 기본값
    if any(word in prompt_lower for word in ["전체", "entire", "모든", "all", "프로젝트", "project"]):
        scope = "project"
    elif any(word in prompt_lower for word in ["여러", "multiple", "몇", "several"]):
        scope = "multiple"

    # 다단계 작업 감지
    multi_step_indicators = [
        "그리고", "다음", "그 후", "먼저", "and then", "after that", "first", "then"
    ]
    is_multi_step = any(ind in prompt_lower for ind in multi_step_indicators)

    # Q4-6: 병렬 의도 감지 — Teams 적합성 판단
    parallel_indicators = [
        "동시에", "병렬로", "함께", "각각", "separately",
        "in parallel", "concurrently", "simultaneously",
        "한편으로는", "다른 한편으로는",
    ]
    has_parallel_intent = any(ind in prompt_lower for ind in parallel_indicators)

    # 독립 작업 2+ 감지 (번호 매기기 or "A와 B" 패턴)
    numbered_tasks = len(re.findall(r'^\s*\d+[.)]', prompt, re.MULTILINE))
    if numbered_tasks >= 2:
        has_parallel_intent = True

    return {
        "complexity": complexity,
        "context_references": context_references,
        "has_context_dependency": has_context_dependency,
        "scope": scope,
        "is_multi_step": is_multi_step,
        "has_parallel_intent": has_parallel_intent,
    }


# ============================================================
# Layer 4: Pragmatic Analysis (화용 분석)
# ============================================================

def analyze_pragmatic(prompt: str) -> Dict:
    """화용 분석: 실제 의도, 암묵적 필요"""
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

    # Q4-4: Simple Task 판별 — 체인 추천 억제
    simple_task = False
    SIMPLE_VERBS = ["보여줘", "읽어줘", "열어줘", "보여", "읽어", "열어", "확인해줘", "알려줘"]
    if any(v in prompt_lower for v in SIMPLE_VERBS) and len(prompt.split()) < 15:
        simple_task = True

    # 긴급도 감지
    urgency = "normal"
    urgency_high_words = [
        "급해", "급한", "급하게", "급히", "urgent", "urgently",
        "빨리", "quickly", "asap", "지금 바로", "당장", "즉시",
        "immediately", "right now", "긴급", "emergency"
    ]
    urgency_low_words = ["나중에", "천천히", "여유", "later", "take your time"]

    if any(word in prompt_lower for word in urgency_high_words):
        urgency = "high"
    elif any(word in prompt_lower for word in urgency_low_words):
        urgency = "low"

    return {
        "intents": detected_intents,
        "language_conversion": language_conversion,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "urgency": urgency,
        "simple_task": simple_task,
    }


# ============================================================
# 추천 생성
# ============================================================

def generate_recommendation(prompt: str, lexical: Dict, syntactic: Dict, discourse: Dict, pragmatic: Dict) -> Dict:
    """분석 결과를 종합하여 추천 생성 (V3.0: 오탐 방지 + 신뢰도 점수)"""
    recommendations = {
        "skills": [],
        "agents": [],
        "chain": None,
        "chain_confidence": 0.0,
        "priority": "MEDIUM",
        "reasoning": [],
        "constraints": [],
        "filtered_out": [],
        "skill_scores": {},   # A-3-1: {skill: confidence}
        "agent_scores": {},   # A-3-1: {agent: confidence}
    }

    # === Phase 0: 제약 감지 + 메타 작업 감지 (A-2-4, A-2-5) ===
    constraints = detect_constraints(prompt)
    meta = detect_meta_work(prompt)

    # Q4-3: 동사 우선 로직 — 동사가 체인 선택을 오버라이드
    prompt_lower = prompt.lower()
    verb_chain_override = None
    VERB_PRIORITY_MAP = {
        "조사": "ResearchChain", "리서치": "ResearchChain",
        "분석해": "MetaThinkChain", "분석해줘": "MetaThinkChain",
        "긴급 수정": "HotfixChain", "핫픽스": "HotfixChain",
        "긴급 패치": "HotfixChain",
    }
    for verb, chain in VERB_PRIORITY_MAP.items():
        if verb in prompt_lower:
            verb_chain_override = chain
            break

    if constraints["has_constraints"]:
        recommendations["constraints"] = constraints["constraints"]
        recommendations["reasoning"].append(f"🚫 제약 감지: {', '.join(constraints['constraints'])}")

    if meta["is_meta_work"]:
        recommendations["reasoning"].append(f"🔧 메타 작업 감지: {', '.join(meta['meta_keywords'][:3])}")

    # === 우선순위 1: 화용적 분석 (실제 의도) — 신뢰도 0.95 ===
    if pragmatic.get("language_conversion"):
        recommendations["skills"].append("/translation-specialist")
        recommendations["skill_scores"]["/translation-specialist"] = 0.95
        recommendations["reasoning"].append(
            f"🔴 번역 의도 감지: {pragmatic.get('source_lang') or '원문'} → {pragmatic.get('target_lang') or '번역문'}"
        )
        recommendations["priority"] = "HIGH"

    if pragmatic.get("urgency") == "high":
        recommendations["priority"] = "HIGH"
        recommendations["reasoning"].append("⚡ 긴급 요청 감지")

    # === 우선순위 2: 담화 분석 (복잡도/범위) ===
    if discourse.get("complexity") == "high" or discourse.get("scope") == "project":
        recommendations["priority"] = "HIGH"
        recommendations["reasoning"].append(f"📊 복잡도: {discourse.get('complexity')}, 범위: {discourse.get('scope')}")

    if discourse.get("is_multi_step"):
        recommendations["reasoning"].append("🔗 다단계 작업 감지")

    # Q4-6: 병렬 의도 → Teams 적합성 추천
    TEAMS_SUITABLE_CHAINS = {"ResearchChain", "GameDevChain", "WebDevChain+"}
    if discourse.get("has_parallel_intent"):
        recommendations["reasoning"].append("🔀 병렬 의도 감지 → Teams 모드 검토 권장")

    # === 우선순위 3: 어휘적 분석 + 컨텍스트 필터링 — 신뢰도 0.7 ===
    for skill, keyword in lexical.get("skills", []):
        if skill in [s for s in recommendations["skills"]]:
            continue
        # 컨텍스트 기반 오탐 필터링
        if not filter_skill_by_context(prompt, skill, keyword):
            recommendations["filtered_out"].append(f"{skill} (키워드 '{keyword}' 오탐 필터링)")
            continue
        recommendations["skills"].append(skill)
        recommendations["skill_scores"].setdefault(skill, 0.7)
        recommendations["reasoning"].append(f"키워드 '{keyword}' → {skill}")

    for agent, keyword in lexical.get("agents", []):
        # A-2-4: 제약 조건 시 implementation 에이전트 억제
        if constraints["suppress_implementation"] and agent == "code_developer":
            recommendations["filtered_out"].append(f"{agent} (제약: 구현 억제)")
            continue
        if constraints["suppress_action"] and agent == "code_developer":
            recommendations["filtered_out"].append(f"{agent} (제약: 행동 억제)")
            continue
        recommendations["agents"].append(agent)
        recommendations["agent_scores"].setdefault(agent, 0.7)
        recommendations["reasoning"].append(f"키워드 '{keyword}' → {agent}")

    # === 우선순위 4: 상호 배제 (A-2-6) ===
    skill_tuples = [(s, "") for s in recommendations["skills"]]
    filtered_tuples = apply_mutual_exclusion(skill_tuples, None)
    excluded = set(recommendations["skills"]) - {s[0] for s in filtered_tuples}
    if excluded:
        recommendations["filtered_out"].extend([f"{s} (상호 배제)" for s in excluded])
    recommendations["skills"] = [s[0] for s in filtered_tuples]

    # === 우선순위 4.5: 에이전트 → 체인 fallback ===
    AGENT_CHAIN_FALLBACK = {
        "solution_innovator": "MetaThinkChain",
        "insight_amplifier": "MetaThinkChain",
    }
    for agent in recommendations["agents"]:
        if agent in AGENT_CHAIN_FALLBACK and not recommendations["chain"]:
            fallback_chain = AGENT_CHAIN_FALLBACK[agent]
            recommendations["chain"] = fallback_chain
            recommendations["chain_confidence"] = 0.7
            recommendations["reasoning"].append(f"체인 fallback: {agent} → {fallback_chain}")
            break

    # === 우선순위 5: 체인 추천 ===
    # A-2-5: 메타 작업이면 SystemDesignChain 강제 — 신뢰도 0.85
    if meta["is_meta_work"]:
        recommendations["chain"] = "SystemDesignChain"
        recommendations["chain_confidence"] = 0.85
        recommendations["reasoning"].append("체인: SystemDesignChain (메타 작업 우선)")
    # Q4-3: 동사 우선 오버라이드 — 키워드보다 동사가 우선
    elif verb_chain_override:
        recommendations["chain"] = verb_chain_override
        recommendations["chain_confidence"] = 0.9
        recommendations["reasoning"].append(f"체인: {verb_chain_override} (동사 우선 +0.2)")
    elif lexical.get("chains"):
        recommendations["chain"] = lexical["chains"][0][0]
        recommendations["chain_confidence"] = 0.8
        recommendations["reasoning"].append(f"체인 매칭: {lexical['chains'][0][0]}")

    # 담화 복잡도 기반 fallback 체인 추천 — 신뢰도 0.5
    if not recommendations["chain"]:
        if discourse.get("complexity") == "high":
            if "analysis" in pragmatic.get("intents", []):
                recommendations["chain"] = "MetaThinkChain"
                recommendations["chain_confidence"] = 0.5
            elif "creation" in pragmatic.get("intents", []):
                recommendations["chain"] = "DevChain"
                recommendations["chain_confidence"] = 0.5
        elif discourse.get("complexity") == "low":
            if "modification" in pragmatic.get("intents", []):
                recommendations["chain"] = "HotfixChain"
                recommendations["chain_confidence"] = 0.5

    # Q4-4: Simple Task면 체인 추천 억제
    if pragmatic.get("simple_task") and recommendations["chain"]:
        recommendations["filtered_out"].append(f"{recommendations['chain']} (Simple Task — 체인 불필요)")
        recommendations["chain"] = None
        recommendations["chain_confidence"] = 0.0
        recommendations["reasoning"].append("🔹 Simple Task 감지 → 체인 추천 억제")

    # Q4-5: urgency=high → HotfixChain 강제 승격
    if pragmatic.get("urgency") == "high" and recommendations["chain"] != "HotfixChain":
        if not meta["is_meta_work"]:  # 메타 작업이면 SystemDesignChain 유지
            recommendations["chain"] = "HotfixChain"
            recommendations["chain_confidence"] = 0.95
            recommendations["reasoning"].append("⚡ HotfixChain 강제 승격 (urgency=high)")

    # A-2-4: 제약 조건 시 체인 조정
    if constraints["suppress_implementation"] and recommendations["chain"] in ("DevChain", "HotfixChain"):
        recommendations["chain"] = "SystemDesignChain"
        recommendations["chain_confidence"] = 0.75
        recommendations["reasoning"].append("체인 조정: 제약으로 인해 SystemDesignChain 전환")

    # === A-3-2: 0.6 미만 추천 필터링 ===
    MIN_CONFIDENCE = 0.6
    recommendations["skills"] = [
        s for s in recommendations["skills"]
        if recommendations["skill_scores"].get(s, 0.7) >= MIN_CONFIDENCE
    ]
    recommendations["agents"] = [
        a for a in recommendations["agents"]
        if recommendations["agent_scores"].get(a, 0.7) >= MIN_CONFIDENCE
    ]
    if recommendations["chain"] and recommendations["chain_confidence"] < MIN_CONFIDENCE:
        recommendations["filtered_out"].append(
            f"{recommendations['chain']} (신뢰도 {recommendations['chain_confidence']:.1f} < {MIN_CONFIDENCE})"
        )
        recommendations["chain"] = None
        recommendations["chain_confidence"] = 0.0

    # === A-3-3: 최대 3개 추천 제한 ===
    MAX_RECOMMENDATIONS = 3
    all_items = []
    for s in recommendations["skills"]:
        all_items.append(("skill", s, recommendations["skill_scores"].get(s, 0.7)))
    for a in recommendations["agents"]:
        all_items.append(("agent", a, recommendations["agent_scores"].get(a, 0.7)))
    if recommendations["chain"]:
        all_items.append(("chain", recommendations["chain"], recommendations["chain_confidence"]))

    # 신뢰도 높은 순으로 정렬 후 상위 3개만 유지
    all_items.sort(key=lambda x: x[2], reverse=True)
    kept = all_items[:MAX_RECOMMENDATIONS]
    kept_skills = {item[1] for item in kept if item[0] == "skill"}
    kept_agents = {item[1] for item in kept if item[0] == "agent"}
    kept_chain = {item[1] for item in kept if item[0] == "chain"}

    for s in recommendations["skills"]:
        if s not in kept_skills:
            recommendations["filtered_out"].append(f"{s} (추천 3개 초과)")
    for a in recommendations["agents"]:
        if a not in kept_agents:
            recommendations["filtered_out"].append(f"{a} (추천 3개 초과)")

    recommendations["skills"] = [s for s in recommendations["skills"] if s in kept_skills]
    recommendations["agents"] = [a for a in recommendations["agents"] if a in kept_agents]
    if recommendations["chain"] and recommendations["chain"] not in kept_chain:
        recommendations["filtered_out"].append(f"{recommendations['chain']} (추천 3개 초과)")
        recommendations["chain"] = None

    # Q4-6: Teams 적합성 추천 추가
    if discourse.get("has_parallel_intent") and recommendations["chain"] in TEAMS_SUITABLE_CHAINS:
        recommendations["teams_recommendation"] = True
        recommendations["reasoning"].append(f"🏢 Teams 모드 추천: {recommendations['chain']}은 Teams 적합 체인 + 병렬 의도 감지")
    else:
        recommendations["teams_recommendation"] = False

    return recommendations


# ============================================================
# 메인 분석 함수
# ============================================================

def analyze_prompt(prompt: str) -> str:
    """메인 분석 함수 - 4-Layer 분석 실행"""

    # Q4-2: 파일 경로 전처리 (lexical 분석 전에 적용)
    cleaned_prompt = preprocess_prompt(prompt)

    # 4-Layer 분석 실행
    lexical = analyze_lexical(cleaned_prompt)
    syntactic = analyze_syntactic(prompt)  # 원본 사용 (구조 분석)
    discourse = analyze_discourse(prompt)  # 원본 사용 (복잡도 분석)
    pragmatic = analyze_pragmatic(prompt)  # 원본 사용 (의도 분석)

    # 추천 생성
    recommendation = generate_recommendation(prompt, lexical, syntactic, discourse, pragmatic)

    # 결과 포맷팅
    output = []
    output.append("=" * 60)
    output.append("🔍 4-LAYER PROMPT ANALYSIS")
    output.append("=" * 60)

    # Layer 1: 어휘적 분석
    output.append("\n📝 [1] 어휘적 분석 (Lexical)")
    if lexical["skills"]:
        output.append(f"   스킬 감지: {', '.join([s[0] for s in lexical['skills']])}")
    if lexical["agents"]:
        output.append(f"   에이전트 감지: {', '.join([a[0] for a in lexical['agents']])}")
    if lexical["chains"]:
        output.append(f"   체인 감지: {', '.join([c[0] for c in lexical['chains']])}")
    if not any([lexical["skills"], lexical["agents"], lexical["chains"]]):
        output.append("   (직접 키워드 매칭 없음)")

    # Layer 2: 통사적 분석
    output.append(f"\n📐 [2] 통사적 분석 (Syntactic)")
    output.append(f"   요청 유형: {syntactic['type']}")
    output.append(f"   단어 수: {syntactic['word_count']}")
    if syntactic['has_code_block']:
        output.append("   📦 코드 블록 포함")
    if syntactic['has_url']:
        output.append("   🔗 URL 포함")

    # Layer 3: 담화 분석
    output.append(f"\n💬 [3] 담화 분석 (Discourse)")
    output.append(f"   복잡도: {discourse['complexity']}")
    output.append(f"   작업 범위: {discourse['scope']}")
    if discourse['has_context_dependency']:
        output.append(f"   📎 컨텍스트 참조: {', '.join(discourse['context_references'])}")
    if discourse['is_multi_step']:
        output.append("   🔗 다단계 작업")
    if discourse.get('has_parallel_intent'):
        output.append("   🔀 병렬 의도 감지")

    # Layer 4: 화용적 분석
    output.append(f"\n🎯 [4] 화용적 분석 (Pragmatic)")
    if pragmatic["intents"]:
        output.append(f"   감지된 의도: {', '.join(pragmatic['intents'])}")
    if pragmatic["language_conversion"]:
        output.append(f"   🔴 언어 변환 감지: {pragmatic['source_lang'] or '?'} → {pragmatic['target_lang']}")
    output.append(f"   긴급도: {pragmatic['urgency']}")
    if pragmatic.get('simple_task'):
        output.append("   🔹 Simple Task 감지 → 체인 불필요")

    # 추천
    output.append(f"\n" + "=" * 60)
    output.append("💡 RECOMMENDATION")
    output.append("=" * 60)

    if recommendation["skills"]:
        skill_strs = []
        for s in recommendation["skills"]:
            score = recommendation["skill_scores"].get(s, 0.7)
            skill_strs.append(f"{s} ({score:.0%})")
        output.append(f"   📌 권장 스킬: {', '.join(skill_strs)}")
    if recommendation["agents"]:
        agent_strs = []
        for a in recommendation["agents"]:
            score = recommendation["agent_scores"].get(a, 0.7)
            agent_strs.append(f"{a} ({score:.0%})")
        output.append(f"   📌 권장 에이전트: {', '.join(agent_strs)}")
    if recommendation["chain"]:
        output.append(f"   📌 권장 체인: {recommendation['chain']} ({recommendation['chain_confidence']:.0%})")
    if recommendation.get("teams_recommendation"):
        output.append(f"   🏢 Teams 모드 추천: 병렬 작업 감지 — Agent Teams 활용 권장")

    output.append(f"\n   우선순위: {recommendation['priority']}")

    if recommendation.get("constraints"):
        output.append(f"\n   🚫 제약: {', '.join(recommendation['constraints'])}")

    if recommendation.get("filtered_out"):
        output.append(f"\n   🔇 오탐 필터링:")
        for filtered in recommendation["filtered_out"]:
            output.append(f"   - {filtered}")

    if recommendation["reasoning"]:
        output.append("\n   근거:")
        for reason in recommendation["reasoning"]:
            output.append(f"   - {reason}")

    output.append("=" * 60)

    return "\n".join(output)


# ============================================================
# CLI 인터페이스
# ============================================================

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
