---
name: translation-specialist
description: 문맥 기반 자동 분석을 통해 최적의 번역 전략을 선택하고 실행하는 전문 번역 스킬. 사용자가 명시적으로 번역 스펙을 제공하거나, 텍스트만 제공 시 4-Layer 언어학적 분석(어휘→통사→담화→화용)으로 도메인/독자/품질모드/형식을 자동 판단. 공문, 법률, 기술, 마케팅, 문학 등 모든 도메인 지원. Nida의 Functional Equivalence, ISO 17100, ASD-STE100 표준 기반.
---

# Translation Specialist

학술적으로 검증된 방법론 기반 전문 번역 스킬입니다. 명시적 스펙이 있으면 그대로 사용하고, 없으면 4-Layer Multi-dimensional Analysis를 통해 자동으로 최적의 번역 전략을 결정합니다.

## 핵심 역량

### 1. 자동 번역 전략 결정
- **4-Layer Analysis**: Lexical → Syntactic → Discourse → Pragmatic 순차 분석
- **우선순위 규칙**: 명확한 신호부터 모호한 신호까지 체계적 판단
- **확신도 시스템**: 판단의 신뢰도를 high/medium/low로 투명하게 공개

### 2. 지원 도메인 (6가지)
- 공문/행정: 격식, 인증, 구조 보존
- 법률: 정확성, 법률 용어, 조항 대응
- 기술/IT: 용어 일관성, placeholder 보존, MT-friendly
- 의료: 전문 용어, 정확한 용량/단위
- 마케팅: 창의적 번역, 문화 적응, 톤 유지
- 문학: 작가 의도, 문체, 감정 전달

### 3. 번역 전략 (4가지)
- **직역 (Literal)**: 법률, 공문, 기술 설정값 - 구조와 형식 유지
- **의역 (Functional Equivalence)**: 일반 문서 - 독자 이해 우선
- **트랜스크리에이션**: 마케팅, 문학 - 창의적 재창조, 문화 적응
- **MT 후편집**: 대량 번역 - 속도와 일관성 우선

### 4. 학술적 근거
- Eugene Nida (2024): Functional Equivalence 이론
- ISO 17100:2015: 번역 서비스 국제 표준
- ASD-STE100:2025: Simplified Technical English (AI가 읽는 문서)
- WMT24: Claude 3.5 Sonnet 최고 성능 (11개 중 9개 1위)

## 번역 프로세스

### Phase 1: 스펙 결정

#### Option A: 사용자가 명시적 스펙 제공 시
```yaml
# 사용자 제공 예시
domain: 공문/행정
audience: 공공기관
quality_mode: 직역
format: bilingual table
```
→ **제공된 스펙을 최우선으로 사용** (자동 판단 생략)

#### Option B: 스펙 없이 텍스트만 제공 시
→ **4-Layer Analysis 자동 실행**

### Phase 2: 4-Layer Multi-dimensional Analysis

텍스트를 4개 층위에서 순차적으로 분석:

#### Layer 1: Lexical Analysis (어휘 분석)
**분석 항목:**
- 도메인별 키워드 빈도 (공문: "귀 기관", "상기" / 법률: "본 계약", "당사자" / 기술: "API", "parameter")
- 격식도 측정 (0-10점): formal markers vs informal markers
- Type Token Ratio (TTR): 용어 반복도 (전문가 vs 일반 독자)
- 독자 지시어: "귀하" (공공기관), "여러분" (일반 사용자)

**판단:**
→ 도메인 후보 3개 추출
→ 독자 유형 추정
→ 확신도 부여

#### Layer 2: Syntactic Analysis (통사 분석)
**분석 항목:**
- 평균 문장 길이: <15 (일반), 15-25 (전문가), >25 (공공기관)
- 수동태 비율: >30% (공문/법률), <10% (일반)
- 명사화 비율: 높음 (학술), 낮음 (구어)
- 구조적 마커: 번호 체계 (1., 가., ①), 표, 조항 → 구조 보존 필수

**판단:**
→ 독자 유형 정교화
→ 품질모드 힌트
→ 형식 요구사항 파악

#### Layer 3: Discourse Analysis (담화 분석)
**분석 항목:**
- 텍스트 구조 패턴: legal_contract (제X조), official_notice (수신/발신), technical_manual (목차/절차)
- 화용적 기능: directive (지시), informative (정보), persuasive (설득), expressive (표현)
- 문화 특정 표현: 관용구, 속담 → 트랜스크리에이션 필요
- Placeholder 패턴: {{var}}, {0}, %s → LLM/MT 독자, 보존 필수

**판단:**
→ 도메인 확정 (가장 명확)
→ 품질모드 결정
→ 형식 요구사항 확정

#### Layer 4: Pragmatic Analysis (화용 분석)
**분석 항목:**
- Speech Acts (화행): declaration (법적 효력), commitment (약속), directive (명령), expressive (감정)
- 공손 전략: positive/negative politeness, bald on record
- 맥락 의존도: 대명사 빈도 → LLM 독자 시 해소 필요
- 함축 의미: 직접 vs 간접 표현

**판단:**
→ 품질모드 최종 확정
→ 문화 적응 수준 결정

### Phase 3: 통합 결정 알고리즘

**우선순위 규칙 적용:**

**도메인 결정:**
1. Discourse structure (highest) → "제X조" = 법률
2. Lexical keywords (medium) → 도메인별 사전
3. Syntactic patterns (supporting) → 문장 구조

**독자 결정:**
1. 명시적 지시어 (highest) → "귀 기관" = 공공기관
2. Placeholder 패턴 (high) → {{var}} = LLM/MT
3. Formality + Syntax (medium) → 격식도+문장길이
4. Readability (low) → TTR, 어휘 난이도

**품질모드 결정:**
1. Pragmatic speech acts (highest) → Declaration = 직역
2. Domain-based (high) → 법률/공문 = 직역
3. Cultural references (medium) → 관용구 = 트랜스크리에이션
4. Default (low) → 의역

**형식 결정:**
1. 명시적 키워드 (highest) → "공증" = 인증 필요
2. Structural markers (high) → 표/번호 = 구조 보존
3. Placeholder patterns (high) → {{}} = placeholder 보존
4. Domain + Audience (medium) → 법률+기관 = Bilingual table

**출력 예시:**
```yaml
spec:
  domain: 공문/행정
  audience: 공공기관
  quality_mode: 직역
  format: Bilingual Table
confidence:
  domain: high        # Discourse structure로 명확히 판단
  audience: high      # "귀 기관" 명시적 지시어
  quality_mode: high  # 공문 도메인 + directive speech act
  format: medium      # 공문+기관 조합으로 권장
```

### Phase 4: 확신도 확인

**확신도가 'low'인 항목이 있으면:**
1. 판단 결과를 사용자에게 명확히 제시
2. 근거 설명
3. 확인 요청

**출력 형식:**
```
🤖 자동 판단 결과 (일부 확신도 낮음)

📋 판단된 번역 스펙:
  • 도메인:    기술/IT          (확신도: medium)
  • 독자:      전문가           (확신도: low)
  • 품질모드:  의역             (확신도: low)
  • 형식:      구조 보존        (확신도: high)

❓ 위 스펙으로 진행하시겠습니까?
   [Y] 예, 진행합니다
   [N] 아니오, 수정하겠습니다

N 선택 시 → 사용자에게 직접 입력 요청
```

### Phase 5: 번역 실행

**프롬프트 생성 구조:**
```markdown
당신은 전문 번역가입니다. 다음 스펙에 따라 번역하세요:

**번역 대상 텍스트:**
[원문]

**번역 스펙:**
- 도메인: {domain} (확신도: {conf})
- 독자: {audience} (확신도: {conf})
- 품질모드: {quality_mode} (확신도: {conf})
- 형식: {format} (확신도: {conf})

**도메인별 지침:**
[도메인에 맞는 구체적 지침]

**독자별 지침:**
[독자에 맞는 톤/스타일 지침]

**품질모드별 지침:**
[직역/의역/트랜스크리에이션 정도]

**형식별 지침:**
[placeholder 보존, 구조 보존 등]

**주의사항:**
- 날짜/금액/고유명사 정확히 대응
- 원문에 없는 내용 추가 금지
- [도메인 특정 주의사항]

**출력:**
```

**도메인별 지침 템플릿:**

**공문/행정:**
- 격식 최대한 유지
- "귀 기관", "~하시기 바랍니다" 같은 공문 어투
- 조항 번호, 날짜, 고유명사 정확 대응
- 문장 임의 축약 금지

**법률:**
- 법률 용어 정확 번역
- "본 계약", "당사자", "~할 것" 같은 법률 문체
- 조항 구조(제X조, 제X항) 정확 보존
- 모호성 절대 금지

**기술/IT:**
- 기술 용어는 표준 번역
- 코드, 경로, 설정값 절대 번역 금지
- Placeholder ({{var}}, {0}) 그대로 보존
- 버전 번호, RFC 번호 유지

**마케팅:**
- 원문 감정과 톤 살리기
- 문화적으로 적절한 창의적 표현
- CTA 문구는 목적언어에서 자연스럽게
- 직역보다 독자 반응 중심

**의료:**
- 전문 용어 정확 번역
- 용량(mg, ml), 학명 정확 대응
- 부작용, 처방 관련 명확한 표현
- 모호성 제거

**문학:**
- 작가 의도와 문체 살리기
- 은유, 상징 문화적 적응
- 리듬과 감정 전달
- 창의적 재해석 가능

### Phase 6: 후처리 검증

**Placeholder 보존 검증:**
- 원문과 번역문의 placeholder 개수/순서 일치 확인
- 불일치 시 경고 및 수정

**구조 보존 검증:**
- 번호 체계, 표 구조, 조항 번호 일치 확인
- 불일치 시 경고

**품질 체크리스트:**
- [ ] 날짜/금액/고유명사 정확 대응
- [ ] Placeholder 모두 보존 (해당 시)
- [ ] 구조 정확히 유지 (해당 시)
- [ ] 도메인 전문 용어 정확
- [ ] 톤과 격식도 적절
- [ ] 원문 의도 보존

## 출력 형식

### 기본 출력
```markdown
## 번역 결과

**사용된 스펙:**
- 도메인: [domain] (확신도: [conf])
- 독자: [audience] (확신도: [conf])
- 품질모드: [quality_mode] (확신도: [conf])
- 형식: [format] (확신도: [conf])

**번역:**
[번역 결과]

**검증:**
✅ [통과한 검증 항목]
⚠️ [주의사항]
```

### Bilingual Table 출력
```markdown
| 번호 | 원문 | 번역문 |
|------|------|--------|
| 1    | ... | ... |
| 2    | ... | ... |
```

## 특수 상황 처리

### Case 1: 혼합 도메인
```
예: "API 사용 가이드 - 지금 바로 시작하세요!"
→ 문단별로 다른 전략 적용
- 마케팅 부분: 트랜스크리에이션
- 기술 부분: 직역
```

### Case 2: 짧은 텍스트 (맥락 부족)
```
예: "저장하기"
→ 확신도 low, 여러 옵션 제시
- Save (버튼)
- Saving (진행형)
- Save it (명령문)
→ 사용자 맥락 요청
```

### Case 3: 은어/신조어
```
예: "완전 대박! ㅋㅋㅋ"
→ 트랜스크리에이션
→ 목적언어의 동등한 톤
영어: "Totally awesome! lol"
```

## 사용 예시

### 예시 1: 명시적 스펙 제공
```
사용자: "다음을 영어로 번역해주세요.
스펙: domain=공문/행정, audience=공공기관, quality_mode=직역

귀 기관에서 요청하신 서류를 송부합니다."

→ 제공된 스펙 사용, 자동 판단 생략
→ 공문 스타일로 직역
```

### 예시 2: 자동 판단 (확신도 높음)
```
사용자: "다음을 영어로 번역해주세요.

제1조 (목적)
본 계약은 양 당사자 간의 권리와 의무를 명확히 함을 목적으로 한다."

→ 4-Layer Analysis 실행
→ Domain: 법률 (high - "제1조", "본 계약" 구조)
→ Audience: 전문가 (high - 격식도 10/10)
→ Quality: 직역 (high - declaration speech act)
→ Format: 구조 보존 (high - 조항 번호)
→ 확신도 모두 high → 바로 번역 실행
```

### 예시 3: 자동 판단 (확신도 낮음)
```
사용자: "다음을 번역해주세요.

이 제품은 사용하기 쉽습니다."

→ 4-Layer Analysis 실행
→ Domain: 불명확 (low - 제품 설명? 마케팅?)
→ Audience: 일반 사용자 (medium - "쉽습니다")
→ 확신도 낮음 → 사용자 확인 요청

"🤖 자동 판단 결과 (확신도 낮음):
 도메인: 제품 설명 (low)
 계속 진행하시겠습니까?"
```

## Best Practices

### DO ✅
- 명시적 스펙이 있으면 무조건 우선 사용
- 확신도 낮으면 사용자 확인
- 도메인별 전문 용어 정확히
- Placeholder는 절대 번역하지 않음
- 법률/공문은 구조 엄격히 보존
- 마케팅은 창의적 표현 활용
- 검증 체크리스트 반드시 실행

### DON'T ❌
- 확신도 낮은데 임의 진행
- 원문에 없는 내용 추가
- Placeholder 번역
- 법률/공문에서 의역
- 마케팅에서 직역
- 날짜/금액/고유명사 변경
- 검증 생략

## 참조 문서

상세한 내용은 다음 파일 참조:
- **reference.md**: 분류 체계, 학술적 근거, 키워드 사전, 격식도 측정
- **examples.md**: 4가지 실전 예시 (공문, 마케팅, 기술(LLM용), 법률)

## 품질 보증

이 스킬은 다음 학술 연구 및 표준을 기반으로 합니다:
- Eugene Nida (1964-2024): Functional Equivalence
- ISO 17100:2015: 번역 서비스 국제 표준
- ASD-STE100:2025: Simplified Technical English
- SemEval-2024 Task 8: Domain Classification
- WMT24: Claude 3.5 Sonnet 최고 성능 검증
- 한국 공증 시스템: 공증번역, 아포스티유

---

**버전**: 1.0
**최종 수정**: 2025-10-31
**학술 검증**: ✅ 완료
**실전 테스트**: 권장

번역이 필요하신가요? 텍스트만 제공하시거나, 원하시는 스펙을 명시해주세요!
