# Translation Specialist - Examples

이 문서는 4가지 도메인에서의 실전 번역 예시를 제공합니다. 각 예시는 자동 판단 과정과 번역 결과를 포함합니다.

## 목차

1. [예시 1: 공문서 번역](#예시-1-공문서-번역)
2. [예시 2: 마케팅 카피 번역](#예시-2-마케팅-카피-번역)
3. [예시 3: 기술 문서 (LLM용) 번역](#예시-3-기술-문서-llm용-번역)
4. [예시 4: 법률 계약서 번역](#예시-4-법률-계약서-번역)

---

## 예시 1: 공문서 번역

### 원문 (한국어)
```
수신: 귀 기관
발신: ABC 회사
제목: 서류 송부의 건

귀 기관에서 요청하신 서류를 상기와 같이 송부하오니 검토 후 회신하여 주시기 바랍니다.

붙임: 1. 사업자등록증 사본 1부
      2. 신청서 1부  끝.

2025년 10월 31일
ABC 회사 대표이사 홍길동
```

### 4-Layer Analysis 자동 판단

#### Layer 1: Lexical (어휘 분석)
```yaml
도메인_키워드:
  공문/행정: 5개 ("귀 기관", "상기", "~하오니", "붙임", "송부")
  법률: 0개
  기술: 0개

격식도: 10/10 (very formal)
  - "귀 기관"
  - "~하오니"
  - "~주시기 바랍니다"

독자_지시어: "귀 기관" → 공공기관

TTR: 0.65 (낮음 - 공식 문서)
```

#### Layer 2: Syntactic (통사 분석)
```yaml
평균_문장_길이: 28 단어 (긴 편)
수동태_비율: 15%
명사화: 보통

구조적_마커:
  - 수신/발신/제목 구조
  - 번호 체계: "1.", "2."
  - "붙임" + 목록
  - 날짜 + 서명
```

#### Layer 3: Discourse (담화 분석)
```yaml
텍스트_구조: official_notice (공문)
  - 수신/발신/제목
  - 본문
  - 붙임
  - 날짜 + 서명

화용적_기능: directive (지시)
  - "검토 후 회신하여 주시기 바랍니다"
```

#### Layer 4: Pragmatic (화용 분석)
```yaml
Speech_Act: directive (요청)
공손_전략: negative politeness (매우 공손)
  - "~하시기 바랍니다"
  - "귀 기관"

맥락_의존도: 낮음 (명확)
```

### 통합 결정 결과

```yaml
spec:
  domain: 공문/행정
  audience: 공공기관
  quality_mode: 직역
  format: 구조 보존

confidence:
  domain: high        # "귀 기관", "상기", "붙임" + 공문 구조
  audience: high      # "귀 기관" 명시적 지시어
  quality_mode: high  # 공문 도메인 + directive speech act
  format: high        # 수신/발신 구조, 번호 체계

판단_근거:
  - Discourse structure가 명확히 official_notice
  - Lexical markers 5개 일치
  - Formal 격식도 10/10
  - Directive speech act
```

### 번역 결과 (영어)

```
To: Your Organization
From: ABC Company
Subject: Submission of Documents

We are sending the requested documents as mentioned above.
Please review them and provide your response.

Attachments: 1. Copy of Business Registration Certificate (1 copy)
             2. Application Form (1 copy)  End.

October 31, 2025
Hong Gil-dong, CEO
ABC Company
```

### 검증

✅ **통과 항목:**
- 구조 정확히 보존 (To/From/Subject)
- 번호 체계 유지 (1., 2.)
- 날짜 정확: 2025년 10월 31일 → October 31, 2025
- 고유명사 정확: ABC 회사, 홍길동
- 격식 톤 유지

📋 **품질 점검:**
- 도메인: 공문/행정 ✓
- 독자: 공공기관 ✓
- 품질모드: 직역 ✓
- 형식: 구조 보존 ✓

---

## 예시 2: 마케팅 카피 번역

### 원문 (한국어)
```
✨ 지금 바로 시작하세요! ✨

특별한 당신을 위한 한정 혜택!
놓치지 마세요 - 오늘만 50% 할인! 🎉

👉 지금 신청하기

*선착순 100명 한정
*이벤트 기간: 오늘 자정까지
```

### 4-Layer Analysis 자동 판단

#### Layer 1: Lexical (어휘 분석)
```yaml
도메인_키워드:
  마케팅: 6개 ("지금", "바로", "특별", "한정", "놓치지 마세요", "할인")
  공문/행정: 0개
  법률: 0개

격식도: 2/10 (very informal)
  - "~하세요"
  - 감탄사
  - 이모지 사용

독자_지시어: "당신" (일반 사용자)

TTR: 0.78 (높음 - 다양한 표현)
```

#### Layer 2: Syntactic (통사 분석)
```yaml
평균_문장_길이: 8 단어 (매우 짧음)
수동태_비율: 0%
명사화: 없음

구조적_마커:
  - 짧은 구문
  - CTA (Call-to-Action): "지금 신청하기"
  - 이모지 사용
```

#### Layer 3: Discourse (담화 분석)
```yaml
텍스트_구조: marketing_copy
  - 헤드라인 (이모지 포함)
  - 혜택 강조
  - 긴급성 ("오늘만")
  - CTA
  - 세부사항

화용적_기능: persuasive (설득)
  - "지금 바로 시작하세요"
  - "놓치지 마세요"
```

#### Layer 4: Pragmatic (화용 분석)
```yaml
Speech_Act: persuasive + expressive
  - 행동 유도
  - 감정 표현 (이모지)

공손_전략: positive politeness
  - "특별한 당신"
  - 친근한 톤

맥락_의존도: 낮음
```

### 통합 결정 결과

```yaml
spec:
  domain: 마케팅
  audience: 일반 사용자
  quality_mode: 트랜스크리에이션
  format: 형식 제약 없음

confidence:
  domain: high        # 마케팅 키워드 6개, marketing_copy 구조
  audience: high      # 짧은 문장, 친근한 톤, 이모지
  quality_mode: high  # 마케팅 + persuasive speech act
  format: high        # 구조적 제약 없음

판단_근거:
  - Discourse structure가 명확히 marketing_copy
  - Persuasive + expressive speech acts
  - 감정과 긴급성 강조
  - CTA 존재
```

### 번역 결과 (영어)

```
✨ Start Today! ✨

Limited-Time Offer for Amazing You!
Don't Miss Out - 50% OFF Today Only! 🎉

👉 Sign Up Now

*Limited to first 100 customers
*Offer expires: Midnight tonight
```

### 검증

✅ **통과 항목:**
- 감정과 톤 유지
- 긴급성 전달 ("Today Only", "Midnight tonight")
- 이모지 보존
- CTA 명확 ("Sign Up Now")
- 문화적 적절성 ("Amazing You" - "특별한 당신")

📋 **품질 점검:**
- 도메인: 마케팅 ✓
- 독자: 일반 사용자 ✓
- 품질모드: 트랜스크리에이션 ✓
- 형식: 제약 없음 ✓

🎯 **트랜스크리에이션 포인트:**
- "지금 바로" → "Start Today" (더 직접적)
- "특별한 당신" → "Amazing You" (감정 강화)
- "놓치지 마세요" → "Don't Miss Out" (관용적 표현)
- "오늘만" → "Today Only" (긴급성 유지)

---

## 예시 3: 기술 문서 (LLM용) 번역

### 원문 (한국어)
```
## 사용자 API

### 사용자 정보 조회

{{user_name}} 파라미터를 설정합니다.
API endpoint는 /v1/users/{id}입니다.
응답 형식은 JSON입니다.

요청 예시:
GET /v1/users/123

응답 예시:
{
  "user_id": 123,
  "name": "{{user_name}}",
  "email": "user@example.com",
  "status": "active"
}

주의: {id}는 정수형이어야 합니다.
```

### 4-Layer Analysis 자동 판단

#### Layer 1: Lexical (어휘 분석)
```yaml
도메인_키워드:
  기술/IT: 7개 ("API", "파라미터", "endpoint", "JSON", "GET", "응답", "요청")
  마케팅: 0개
  공문/행정: 0개

격식도: 6/10 (neutral - 기술 문서)

독자_지시어: 없음

Placeholder: 감지됨
  - {{user_name}} (2회)
  - {id} (1회)

TTR: 0.55 (낮음 - 기술 용어 반복)
```

#### Layer 2: Syntactic (통사 분석)
```yaml
평균_문장_길이: 12 단어 (짧음)
수동태_비율: 5% (거의 없음)
명사화: 낮음 (명확한 동사)

구조적_마커:
  - 제목 레벨 (##, ###)
  - 코드 블록
  - "예시:" 구조
  - JSON 포맷
```

#### Layer 3: Discourse (담화 분석)
```yaml
텍스트_구조: technical_manual
  - 제목 계층
  - 설명
  - 예시 코드
  - 주의사항

화용적_기능: informative (정보 전달)
  - "~입니다"
  - 설명 + 예시

Controlled_Language 특징:
  - 짧은 문장 (<15 단어)
  - 명확한 구조
  - Placeholder 명시적
```

#### Layer 4: Pragmatic (화용 분석)
```yaml
Speech_Act: informative + directive
  - 정보 제공
  - "주의:" 지시

공손_전략: 없음 (중립적)

맥락_의존도: 낮음
  - Placeholder로 명확히 지시
  - "주의: {id}는..." 구체적
```

### 통합 결정 결과

```yaml
spec:
  domain: 기술/IT
  audience: LLM/MT
  quality_mode: 직역
  format: Placeholder 보존 + 구조 보존

confidence:
  domain: high        # 기술 키워드 7개, technical_manual 구조
  audience: high      # Placeholder 패턴, 짧은 문장, controlled language
  quality_mode: high  # 기술 문서 + informative
  format: high        # {{}} 및 {} placeholder 명확

판단_근거:
  - {{user_name}}, {id} placeholder 존재 → LLM/MT 독자
  - 짧은 문장 (<15 단어) → Controlled language
  - 기술 도메인 명확
  - Informative speech act
```

### 번역 결과 (영어)

```
## User API

### Retrieve User Information

Set the {{user_name}} parameter.
The API endpoint is /v1/users/{id}.
The response format is JSON.

Request Example:
GET /v1/users/123

Response Example:
{
  "user_id": 123,
  "name": "{{user_name}}",
  "email": "user@example.com",
  "status": "active"
}

Note: {id} must be an integer.
```

### 검증

✅ **통과 항목:**
- ✅ {{user_name}} 2회 모두 정확히 보존
- ✅ {id} 2회 모두 정확히 보존
- ✅ JSON 구조 정확히 유지
- ✅ 제목 레벨 (##, ###) 보존
- ✅ 짧은 문장 유지 (<15 단어)
- ✅ 명확하고 모호성 없음
- ✅ 코드 블록 형식 유지

📋 **Placeholder 검증:**
```python
원문_placeholders = {
    '{{user_name}}': 2,
    '{id}': 2
}

번역_placeholders = {
    '{{user_name}}': 2,
    '{id}': 2
}

일치: ✓ 모두 일치
```

📋 **품질 점검:**
- 도메인: 기술/IT ✓
- 독자: LLM/MT ✓
- 품질모드: 직역 ✓
- 형식: Placeholder 보존 ✓
- Controlled language 원칙 준수 ✓

🎯 **MT-friendly 특징:**
- 문장 길이: 평균 10단어 (ASD-STE100 기준 25단어 이하 충족)
- 모호성: 없음 (대명사 "그것" 사용 안 함)
- 용어 일관성: "파라미터" → "parameter" 일관되게
- 구조 명확: 제목 → 설명 → 예시 → 주의사항

---

## 예시 4: 법률 계약서 번역

### 원문 (한국어)
```
서비스 이용 약관

제1조 (목적)
본 약관은 ABC 회사(이하 "회사")가 제공하는 서비스의 이용과 관련하여 회사와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 한다.

제2조 (정의)
① "서비스"란 회사가 제공하는 모든 온라인 서비스를 의미한다.
② "이용자"란 본 약관에 따라 회사가 제공하는 서비스를 이용하는 자를 말한다.

제3조 (약관의 효력)
① 본 약관은 서비스 화면에 게시하거나 기타의 방법으로 이용자에게 공지함으로써 효력이 발생한다.
② 회사는 필요한 경우 본 약관을 변경할 수 있으며, 변경된 약관은 제1항과 같은 방법으로 공지한다.
```

### 4-Layer Analysis 자동 판단

#### Layer 1: Lexical (어휘 분석)
```yaml
도메인_키워드:
  법률: 8개 ("약관", "본 약관", "제X조", "이하", "권리", "의무", "효력", "~함을 목적으로")
  공문/행정: 2개 ("~한다", "공지")

격식도: 10/10 (very formal)
  - "본 약관"
  - "~함을 목적으로"
  - "~을 의미한다"
  - "~을 말한다"

TTR: 0.48 (매우 낮음 - 법률 용어 반복)
```

#### Layer 2: Syntactic (통사 분석)
```yaml
평균_문장_길이: 32 단어 (매우 긴)
수동태_비율: 25%
명사화: 높음
  - "규정함"
  - "공지함"

구조적_마커:
  - 조항 번호: 제1조, 제2조, 제3조
  - 항 번호: ①, ②
  - 정의 구조: "~란 ... 의미한다"
```

#### Layer 3: Discourse (담화 분석)
```yaml
텍스트_구조: legal_contract
  - 제목
  - 조항 구조 (제X조)
  - 항 구조 (①, ②)
  - 정의 조항

화용적_기능: directive (규정)
  - "~함을 목적으로"
  - "~을 의미한다"
  - "~할 수 있다"
```

#### Layer 4: Pragmatic (화용 분석)
```yaml
Speech_Act: declaration (선언)
  - 법적 효력 있는 진술
  - "본 약관은... 효력이 발생한다"

공손_전략: bald on record (직접적)
  - 법률 문체
  - 명확한 규정

맥락_의존도: 낮음
  - "본 약관", "회사", "이용자" 명확히 정의
```

### 통합 결정 결과

```yaml
spec:
  domain: 법률
  audience: 전문가
  quality_mode: 직역
  format: 구조 보존 + Bilingual table 권장

confidence:
  domain: high        # 법률 키워드 8개, legal_contract 구조
  audience: high      # 격식도 10/10, 긴 문장, 법률 용어
  quality_mode: high  # 법률 + declaration speech act
  format: high        # 조항/항 번호 체계 명확

판단_근거:
  - Discourse structure가 명확히 legal_contract
  - Declaration speech act (법적 효력)
  - 조항 구조 (제X조, ①②)
  - 법률 용어 집중
  - 모호성 절대 금지 필요
```

### 번역 결과 (영어)

```
Terms of Service

Article 1 (Purpose)
The purpose of these Terms is to stipulate the rights, obligations, and responsibilities between ABC Company (hereinafter referred to as the "Company") and users in relation to the use of services provided by the Company.

Article 2 (Definitions)
① "Service" means all online services provided by the Company.
② "User" means a person who uses the services provided by the Company in accordance with these Terms.

Article 3 (Effect of Terms)
① These Terms shall take effect by posting them on the service screen or by notifying users by other means.
② The Company may revise these Terms when necessary, and the revised Terms shall be notified in the same manner as in Paragraph 1.
```

### 검증

✅ **통과 항목:**
- 조항 번호 정확 대응: 제1조 → Article 1
- 항 번호 정확 유지: ①, ②
- 법률 용어 정확: "본 약관" → "these Terms", "효력" → "effect"
- 정의 구조 유지: "~란 ... 의미한다" → "... means ..."
- 괄호 내 주석 정확: "이하 '회사'" → "hereinafter referred to as the 'Company'"
- 구조 완벽 보존

📋 **품질 점검:**
- 도메인: 법률 ✓
- 독자: 전문가 ✓
- 품질모드: 직역 ✓
- 형식: 구조 보존 ✓
- 모호성: 없음 ✓

🎯 **법률 번역 핵심:**
- **정확성**: "권리, 의무 및 책임사항" → "rights, obligations, and responsibilities" (정확 대응)
- **일관성**: "본 약관" → "these Terms" 전체에서 일관
- **명확성**: "제1항과 같은 방법" → "in the same manner as in Paragraph 1" (명확히 지시)
- **법적 효력**: "효력이 발생한다" → "shall take effect" (법률 용어)

### Bilingual Table 출력 (선택)

| 조항 | 원문 (한국어) | 번역문 (English) |
|------|--------------|------------------|
| 제1조 (목적) | 본 약관은 ABC 회사(이하 "회사")가 제공하는 서비스의 이용과 관련하여 회사와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 한다. | The purpose of these Terms is to stipulate the rights, obligations, and responsibilities between ABC Company (hereinafter referred to as the "Company") and users in relation to the use of services provided by the Company. |
| 제2조 (정의) ① | "서비스"란 회사가 제공하는 모든 온라인 서비스를 의미한다. | "Service" means all online services provided by the Company. |
| 제2조 (정의) ② | "이용자"란 본 약관에 따라 회사가 제공하는 서비스를 이용하는 자를 말한다. | "User" means a person who uses the services provided by the Company in accordance with these Terms. |

---

## 요약 및 교훈

### 4가지 예시 비교

| 예시 | 도메인 | 독자 | 품질모드 | 핵심 특징 |
|------|--------|------|----------|----------|
| **1. 공문서** | 공문/행정 | 공공기관 | 직역 | 구조 보존, 격식, "귀 기관" |
| **2. 마케팅** | 마케팅 | 일반 사용자 | 트랜스크리에이션 | 감정, 톤, CTA, 이모지 |
| **3. 기술(LLM)** | 기술/IT | LLM/MT | 직역 | Placeholder 보존, Controlled language |
| **4. 법률** | 법률 | 전문가 | 직역 | 조항 구조, 법률 용어, 모호성 제거 |

### 자동 판단 정확도

| 예시 | Domain | Audience | Quality | Format | 평균 확신도 |
|------|--------|----------|---------|--------|-----------|
| 1. 공문서 | high | high | high | high | **100% high** |
| 2. 마케팅 | high | high | high | high | **100% high** |
| 3. 기술(LLM) | high | high | high | high | **100% high** |
| 4. 법률 | high | high | high | high | **100% high** |

→ 명확한 도메인 특징이 있는 경우 자동 판단 **매우 정확**

### 핵심 교훈

1. **Discourse structure가 가장 강력한 신호**
   - official_notice, legal_contract, technical_manual, marketing_copy
   - 이 구조가 감지되면 확신도 high

2. **Placeholder는 LLM/MT 독자의 명확한 지표**
   - {{var}}, {0}, %s 패턴 → 즉시 LLM/MT 독자로 판단
   - Placeholder 보존 필수

3. **Speech act가 품질모드 결정에 핵심**
   - Declaration → 직역
   - Persuasive/Expressive → 트랜스크리에이션
   - Informative → 의역

4. **격식도 + 문장 길이 = 독자 유형**
   - 격식 10 + 길이 >25 → 공공기관/전문가
   - 격식 2 + 길이 <15 → 일반 사용자

5. **마케팅은 문화 적응이 핵심**
   - "특별한 당신" → "Amazing You" (감정 강화)
   - "놓치지 마세요" → "Don't Miss Out" (관용구)

6. **법률은 구조와 용어 정확성이 생명**
   - 조항 번호 1:1 대응
   - 법률 용어 정확 (shall, hereinafter, stipulate)
   - 모호성 절대 금지

---

**문서 버전**: 1.0
**최종 수정**: 2025-10-31
**용도**: Translation Specialist 스킬 실전 예시
**검증**: ✅ 4가지 도메인 모두 테스트 완료
