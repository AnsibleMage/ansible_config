#!/usr/bin/env python3
"""
Translation Specialist - Linguistic Analysis Helper

4-Layer Multi-dimensional Analysis 자동화 스크립트

Usage:
    python linguistic_analysis.py <text_file>
    python linguistic_analysis.py --text "번역할 텍스트"

Output:
    JSON 형식의 자동 판단 결과

Author: Translation Specialist Skill
Version: 1.0
Date: 2025-10-31
"""

import re
import json
import sys
from typing import Dict, List, Tuple
from collections import Counter


# ============================================================================
# 도메인별 키워드 사전
# ============================================================================

DOMAIN_LEXICON = {
    '공문/행정': {
        '필수': ['귀 기관', '상기', '제X조', '하오니', '붙임', '이에'],
        '보조': ['검토', '회신', '송부', '발신', '수신', '하시기 바랍니다'],
        '가중치': 2.0
    },
    '법률': {
        '필수': ['본 계약', '당사자', '단서', '할 것', '본 약관', '제\\d+조'],
        '보조': ['효력', '해지', '손해배상', '소송', '준거법', '합의'],
        '가중치': 2.0
    },
    '기술/IT': {
        '필수': ['API', 'RFC', 'ISO', '파라미터', 'parameter', 'endpoint'],
        '보조': ['버전', '설정', '프로토콜', '인증', '토큰', '배포', 'JSON', 'REST'],
        '가중치': 1.5
    },
    '의료': {
        '필수': ['처방', '투여', '부작용', 'mg', 'ml', '진단'],
        '보조': ['치료', '환자', '임상', 'ICD', '증상', '약물'],
        '가중치': 2.0
    },
    '마케팅': {
        '필수': ['지금', '바로', '특별', '한정', '무료', '할인'],
        '보조': ['혜택', '놓치지 마세요', '오늘만', '신청', '선착순', '이벤트'],
        '가중치': 1.0
    },
    '문학': {
        '필수': ['은유', '상징', '비유', '심상'],
        '보조': ['감정', '묘사', '대화', '서술', '인물', '배경'],
        '가중치': 1.0
    }
}


# 격식도 마커
FORMALITY_MARKERS = {
    'very_formal': ['귀하', '상기', '하시기 바랍니다', '본', '에 따라', '이에'],
    'formal': ['합니다', '입니다', '에 대해', '또한', '따라서'],
    'neutral': ['해요', '이에요', '그래서', '하지만', '그리고'],
    'informal': ['요', '네요', '여러분', '쉽게', '간단히'],
    'very_informal': ['야', 'ㅋㅋ', '대박', '완전', '진짜']
}


# Placeholder 패턴
PLACEHOLDER_PATTERNS = {
    'curly_single': r'\{(\w+)\}',
    'curly_double': r'\{\{(\w+)\}\}',
    'printf_style': r'%[sdfx]',
    'dollar': r'\$\{?(\w+)\}?',
    'angle': r'<(\w+)>',
    'numbered': r'\{(\d+)\}'
}


# ============================================================================
# Layer 1: Lexical Analysis
# ============================================================================

def analyze_lexical(text: str) -> Dict:
    """어휘 분석: 도메인 키워드, 격식도, TTR, Placeholder"""

    # 1. 도메인 키워드 매칭
    domain_scores = {}
    for domain, lexicon in DOMAIN_LEXICON.items():
        score = 0
        for keyword in lexicon['필수']:
            # 정규식으로 매칭 (예: 제\d+조)
            matches = len(re.findall(keyword, text, re.IGNORECASE))
            score += matches * lexicon['가중치']

        for keyword in lexicon['보조']:
            matches = len(re.findall(keyword, text, re.IGNORECASE))
            score += matches * (lexicon['가중치'] * 0.5)

        if score > 0:
            domain_scores[domain] = score

    # 상위 3개 도메인
    top_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    # 2. 격식도 측정
    formality_score = 0
    formality_level = 'neutral'

    for level, markers in FORMALITY_MARKERS.items():
        level_count = sum(1 for marker in markers if marker in text)
        if level == 'very_formal' and level_count > 0:
            formality_score = 10
            formality_level = level
        elif level == 'formal' and level_count > 0 and formality_score < 8:
            formality_score = 8
            formality_level = level
        elif level == 'neutral' and level_count > 0 and formality_score < 6:
            formality_score = 6
            formality_level = level
        elif level == 'informal' and level_count > 0 and formality_score < 4:
            formality_score = 4
            formality_level = level
        elif level == 'very_informal' and level_count > 0 and formality_score < 2:
            formality_score = 2
            formality_level = level

    # 3. Type Token Ratio (TTR)
    words = re.findall(r'\w+', text)
    unique_words = set(words)
    ttr = len(unique_words) / len(words) if words else 0

    # 4. 독자 지시어
    audience_markers = {
        '공공기관': ['귀 기관', '귀하'],
        '일반 사용자': ['여러분', '당신'],
        '전문가': []  # 간접적으로 판단
    }

    detected_audience = None
    for audience, markers in audience_markers.items():
        if any(marker in text for marker in markers):
            detected_audience = audience
            break

    # 5. Placeholder 검출
    placeholders = {}
    for pattern_name, regex in PLACEHOLDER_PATTERNS.items():
        matches = re.findall(regex, text)
        if matches:
            placeholders[pattern_name] = {
                'count': len(matches),
                'examples': matches[:3]
            }

    has_placeholders = len(placeholders) > 0

    return {
        'domain_scores': dict(top_domains),
        'top_domain': top_domains[0][0] if top_domains else None,
        'top_domain_score': top_domains[0][1] if top_domains else 0,
        'formality_score': formality_score,
        'formality_level': formality_level,
        'ttr': round(ttr, 2),
        'audience_hint': detected_audience,
        'has_placeholders': has_placeholders,
        'placeholders': placeholders
    }


# ============================================================================
# Layer 2: Syntactic Analysis
# ============================================================================

def analyze_syntactic(text: str) -> Dict:
    """통사 분석: 문장 길이, 수동태, 구조"""

    # 1. 문장 분리
    sentences = re.split(r'[.!?。]\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 2. 평균 문장 길이
    sentence_lengths = [len(s.split()) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    # 3. 수동태 비율 (한국어 간이 검출)
    passive_markers = ['되다', '되는', '되었', '당하다', '받다']
    passive_count = sum(1 for marker in passive_markers if marker in text)
    passive_ratio = passive_count / len(sentences) if sentences else 0

    # 4. 구조적 마커
    has_numbering = bool(re.search(r'^\s*\d+\.', text, re.MULTILINE) or
                         re.search(r'[가-하]\.', text) or
                         re.search(r'[①-⑳]', text))

    has_table = '|' in text and text.count('|') > 4

    has_sections = bool(re.search(r'^#+\s', text, re.MULTILINE))  # Markdown headers

    # 5. 조항 구조 (법률)
    has_articles = bool(re.search(r'제\d+조', text))

    return {
        'avg_sentence_length': round(avg_sentence_length, 1),
        'num_sentences': len(sentences),
        'passive_ratio': round(passive_ratio, 2),
        'has_numbering': has_numbering,
        'has_table': has_table,
        'has_sections': has_sections,
        'has_articles': has_articles
    }


# ============================================================================
# Layer 3: Discourse Analysis
# ============================================================================

def analyze_discourse(text: str) -> Dict:
    """담화 분석: 텍스트 구조, 화용 기능"""

    structure = 'unknown'

    # 구조 패턴 감지
    if re.search(r'(수신|발신|제목):', text) and '붙임' in text:
        structure = 'official_notice'
    elif re.search(r'제\d+조', text) and ('본 계약' in text or '본 약관' in text):
        structure = 'legal_contract'
    elif re.search(r'(API|endpoint|파라미터)', text) and re.search(r'예시:', text):
        structure = 'technical_manual'
    elif ('지금' in text or '바로' in text) and ('할인' in text or '이벤트' in text):
        structure = 'marketing_copy'

    # 화용적 기능
    pragmatic_functions = []
    if re.search(r'(하시오|할 것|must|shall)', text):
        pragmatic_functions.append('directive')
    if re.search(r'(입니다|이다|is|are)', text):
        pragmatic_functions.append('informative')
    if re.search(r'(하세요|해보세요|should|can)', text):
        pragmatic_functions.append('persuasive')
    if re.search(r'(네요|구나|wow|great)', text):
        pragmatic_functions.append('expressive')

    # 문화 특정 표현 (간단한 감지)
    cultural_references = bool(re.search(r'(속담|관용구|ㅋㅋ|ㅎㅎ)', text))

    return {
        'structure': structure,
        'pragmatic_functions': pragmatic_functions,
        'cultural_references': cultural_references
    }


# ============================================================================
# Layer 4: Pragmatic Analysis
# ============================================================================

def analyze_pragmatic(text: str) -> Dict:
    """화용 분석: 화행, 공손 전략"""

    # Speech Acts
    speech_acts = []
    if re.search(r'(선언|발표|hereby declare)', text):
        speech_acts.append('declaration')
    if re.search(r'(약속|보장|promise|guarantee)', text):
        speech_acts.append('commitment')
    if re.search(r'(명령|요청|order|request)', text):
        speech_acts.append('directive')
    if re.search(r'(감사|사과|thank|sorry)', text):
        speech_acts.append('expressive')

    # 공손 전략
    politeness_strategy = 'neutral'
    if '귀하' in text or '하시기 바랍니다' in text:
        politeness_strategy = 'negative_politeness'
    elif '우리' in text or '함께' in text:
        politeness_strategy = 'positive_politeness'
    elif re.search(r'(하시오|금지|do not)', text):
        politeness_strategy = 'bald_on_record'

    # 맥락 의존도 (대명사 빈도)
    pronouns = len(re.findall(r'(이|그|저|it|they|this|that)\s', text))
    context_dependency = 'high' if pronouns > 5 else 'medium' if pronouns > 2 else 'low'

    return {
        'speech_acts': speech_acts,
        'politeness_strategy': politeness_strategy,
        'context_dependency': context_dependency
    }


# ============================================================================
# 통합 결정 알고리즘
# ============================================================================

def apply_decision_rules(lex, syn, dis, prag) -> Dict:
    """우선순위 규칙 적용하여 최종 스펙 결정"""

    spec = {
        'domain': None,
        'audience': None,
        'quality_mode': None,
        'format': None
    }
    confidence = {}

    # === 도메인 결정 ===
    # 우선순위 1: Discourse structure
    if dis['structure'] != 'unknown':
        structure_map = {
            'legal_contract': '법률',
            'official_notice': '공문/행정',
            'technical_manual': '기술/IT',
            'marketing_copy': '마케팅'
        }
        spec['domain'] = structure_map.get(dis['structure'], None)
        confidence['domain'] = 'high' if spec['domain'] else 'medium'

    # 우선순위 2: Lexical keywords
    elif lex['top_domain'] and lex['top_domain_score'] > 5:
        spec['domain'] = lex['top_domain']
        confidence['domain'] = 'medium' if lex['top_domain_score'] > 5 else 'low'
    else:
        spec['domain'] = lex['top_domain'] if lex['top_domain'] else '일반'
        confidence['domain'] = 'low'

    # === 독자 결정 ===
    # 우선순위 1: 명시적 지시어
    if lex['audience_hint']:
        spec['audience'] = lex['audience_hint']
        confidence['audience'] = 'high'

    # 우선순위 2: Placeholder (LLM/MT)
    elif lex['has_placeholders'] and syn['avg_sentence_length'] < 20:
        spec['audience'] = 'LLM/MT'
        confidence['audience'] = 'high'

    # 우선순위 3: Formality + Syntax
    elif lex['formality_score'] > 8 and syn['avg_sentence_length'] > 25:
        spec['audience'] = '전문가'
        confidence['audience'] = 'medium'

    # 우선순위 4: Readability
    elif lex['ttr'] > 0.7 and syn['avg_sentence_length'] < 15:
        spec['audience'] = '일반 사용자'
        confidence['audience'] = 'medium'

    else:
        spec['audience'] = '일반 사용자'
        confidence['audience'] = 'low'

    # === 품질모드 결정 ===
    # 우선순위 1: Pragmatic speech acts
    if 'declaration' in prag['speech_acts']:
        spec['quality_mode'] = '직역'
        confidence['quality_mode'] = 'high'
    elif 'expressive' in prag['speech_acts'] or 'persuasive' in dis['pragmatic_functions']:
        spec['quality_mode'] = '트랜스크리에이션'
        confidence['quality_mode'] = 'high'

    # 우선순위 2: Domain-based
    elif spec['domain'] in ['법률', '공문/행정']:
        spec['quality_mode'] = '직역'
        confidence['quality_mode'] = 'high'
    elif spec['domain'] in ['마케팅', '문학']:
        spec['quality_mode'] = '트랜스크리에이션'
        confidence['quality_mode'] = 'high'

    # 우선순위 3: Cultural references
    elif dis['cultural_references']:
        spec['quality_mode'] = '트랜스크리에이션'
        confidence['quality_mode'] = 'medium'

    # Default
    else:
        spec['quality_mode'] = '의역'
        confidence['quality_mode'] = 'low'

    # === 형식 결정 ===
    if re.search(r'(공증|notarized|certified)', text):
        spec['format'] = '인증 필요'
        confidence['format'] = 'high'
    elif syn['has_numbering'] or syn['has_table'] or syn['has_articles']:
        spec['format'] = '구조 보존'
        confidence['format'] = 'high'
    elif lex['has_placeholders']:
        spec['format'] = 'Placeholder 보존'
        confidence['format'] = 'high'
    elif spec['domain'] in ['법률', '공문/행정'] and spec['audience'] == '공공기관':
        spec['format'] = 'Bilingual Table 권장'
        confidence['format'] = 'medium'
    else:
        spec['format'] = '형식 제약 없음'
        confidence['format'] = 'high'

    spec['confidence'] = confidence
    return spec


# ============================================================================
# 메인 함수
# ============================================================================

def auto_detect_translation_spec(text: str) -> Dict:
    """4-Layer Analysis 실행 및 자동 스펙 결정"""

    # 1. 4-Layer 분석
    lexical = analyze_lexical(text)
    syntactic = analyze_syntactic(text)
    discourse = analyze_discourse(text)
    pragmatic = analyze_pragmatic(text)

    # 2. 통합 결정
    spec = apply_decision_rules(lexical, syntactic, discourse, pragmatic)

    # 3. 전체 결과 구성
    result = {
        'spec': spec,
        'analysis': {
            'lexical': lexical,
            'syntactic': syntactic,
            'discourse': discourse,
            'pragmatic': pragmatic
        }
    }

    return result


# ============================================================================
# CLI 인터페이스
# ============================================================================

def main():
    """CLI 메인 함수"""

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python linguistic_analysis.py <text_file>")
        print("  python linguistic_analysis.py --text \"번역할 텍스트\"")
        sys.exit(1)

    # 텍스트 읽기
    if sys.argv[1] == '--text':
        if len(sys.argv) < 3:
            print("Error: --text 옵션에는 텍스트가 필요합니다")
            sys.exit(1)
        text = sys.argv[2]
    else:
        # 파일 읽기
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: 파일을 찾을 수 없습니다: {sys.argv[1]}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: 파일 읽기 실패: {e}")
            sys.exit(1)

    # 분석 실행
    result = auto_detect_translation_spec(text)

    # JSON 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    # text 변수를 전역으로 정의 (apply_decision_rules에서 사용)
    text = ""
    main()
