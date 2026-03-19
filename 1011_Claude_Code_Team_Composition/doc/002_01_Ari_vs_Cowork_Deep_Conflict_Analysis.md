# 아리 분석 vs Cowork 분석 심층 비교 판정

> 동일 주제(커스텀 체인 vs Agent Teams)에 대한 두 분석 보고서의 상반된 결론 심층 검증
> 작성일: 2026-02-06 | 기준: 공식 문서 팩트체크 + 다차원 분석 + 공정 판정

---

## 결론 요약

| 질문 | 판정 |
|------|------|
| **어느 분석이 맞나?** | **Cowork(001_02)이 실질적으로 더 정확.** 아리(001_01)는 이론적으로 맞지만 실무 문제 간과 |
| **아리 분석은 틀렸나?** | **부분적으로.** 레이어 모델은 정확하나, "호환" 판정이 과도하게 낙관적 |
| **핵심 차이점은?** | **분석 관점 차이.** 아리=이론적 레이어 분리, Cowork=실무적 동시 사용 시나리오 |
| **Agent Teams 활성화해도 되나?** | **조건부.** Hook 분기 + Memory 잠금 구현 후에만 안전 |

---

## 1. 분석 방법

### 사용된 도구
- **WebSearch** × 3: 공식 문서 팩트체크 (hooks, permissions, subagent vs teams)
- **공식 문서**: `Orchestrate teams of Claude Code sessions.md` 재검토
- **multidimensional_analyst** [opus]: 5차원 비교 분석
- **balanced_judge** [opus]: 공정 판정

### 분석 프레임워크
- 시간적 차원: 현재 → 활성화 시 → 장기적
- 추상화 차원: 이론적 레이어 vs 실제 실행 환경
- 인과 차원: 전제 차이 → 결론 차이
- 규모 차원: 단독 사용 vs 동시 사용
- 실용 차원: 사용자에게 도움 되는 정도

---

## 2. 두 분석의 핵심 차이: 전제가 다르다

| | 아리 분석 (001_01) | Cowork 분석 (001_02) |
|--|---|---|
| **분석 질문** | "실행 로직이 충돌하는가?" | "동시에 쓸 때 문제가 생기는가?" |
| **핵심 전제** | Layer가 다르면 충돌 없음 | Teammate가 context 로드 시 Layer 1-2도 재실행 |
| **"호환"의 정의** | 기능적으로 작동함 = 호환 | 작동하지만 부작용 있음 = 문제 |
| **분석 깊이** | 아키텍처 수준 (추상) | 실행 환경 수준 (구체) |

**핵심**: 아리는 "팀메이트가 CLAUDE.md를 로드한다 → 체인이 실행된다 → 좋다!" 라고 봤지만, Cowork은 같은 현상을 **"UserPromptSubmit Hook이 N번 중복 실행된다 → 나쁘다!"** 로 짚었다.

---

## 3. 공식 문서 팩트체크

### 공식 확인된 사실

| 사실 | 출처 | 원문 |
|------|------|------|
| Teammate는 CLAUDE.md 로드 | 공식 문서 | "loads the same project context as a regular session: CLAUDE.md, MCP servers, and skills" |
| 리드의 권한 상속 | 공식 문서 | "Teammates start with the lead's permission settings" |
| 독립 컨텍스트 | 공식 문서 | "each teammate has its own context window" |
| 대화 이력 미상속 | 공식 문서 | "The lead's conversation history does not carry over" |
| 팀 중첩 불가 | 공식 문서 | "teammates cannot spawn their own teams or teammates" |
| 토큰 비용 높음 | 공식 문서 | "Agent teams use significantly more tokens than a single session" |

### 추론되는 사실 (직접 언급 없으나 논리적 귀결)

| 추론 | 근거 |
|------|------|
| **settings.json의 hooks도 로드** | "same project context" = CLAUDE.md + MCP + skills 로드 시 settings도 함께 로드 |
| **UserPromptSubmit Hook 중복 실행** | Teammate가 프롬프트를 처리할 때마다 등록된 hooks 실행 |
| **상태 파일 경합** | `/tmp/claude_prev_prompt_state.json`을 N개 프로세스가 동시 접근 |
| **Memory 동시 쓰기 가능** | 독립 세션이므로 파일 시스템 동시 접근에 대한 보호 없음 |

---

## 4. 쟁점별 판정

### 쟁점 1: Hook 시스템

| | 아리 | Cowork | 판정 |
|--|------|--------|------|
| 판단 | "호환" (한 줄) | "HIGH - 중복 실행" (상세 분석) | **Cowork 정확** |

**분석**: Teammate가 settings.json을 로드하면 `UserPromptSubmit` hook도 활성화됨. Teammate 3명 × 프롬프트 10회 = **4-Layer 분석 30회** 불필요 실행. 특히 `/tmp/claude_prev_prompt_state.json` 상태 파일을 N개 프로세스가 동시 접근하면 데이터 경합 발생.

### 쟁점 2: Memory System

| | 아리 | Cowork | 판정 |
|--|------|--------|------|
| 판단 | 언급 없음 (누락) | "HIGH - Race Condition" | **Cowork 정확, 아리 치명적 누락** |

**분석**: 앤의 메모리 시스템은 단일 세션 기준 설계. 동시 작업 시:
```
Teammate A: 최근 3개 읽기 → SEQ=035 결정 → 파일 생성
Teammate B: 최근 3개 읽기 → SEQ=035 결정 → 파일 덮어쓰기!
```

### 쟁점 3: CLAUDE.md 로딩

| | 아리 | Cowork | 판정 |
|--|------|--------|------|
| 판단 | "팀메이트도 각자 로드 → 호환" | "841줄 × N = 토큰 폭발 MEDIUM" | **Cowork 정확** |

**분석**: CLAUDE.md 841줄 ≈ 15,000+ 토큰. Teammate 4명 = **순수 오버헤드 60,000 토큰**. Rails 섹션, 변경이력 등 teammate에게 불필요한 부분이 대부분.

### 쟁점 4: 레이어 분리 모델

| | 아리 | Cowork | 판정 |
|--|------|--------|------|
| 판단 | "Layer 1-2 vs 3 분리 → 충돌 없음" | "이중 오케스트레이션 MEDIUM" | **둘 다 부분 정확** |

**분석**: 아리의 4-Layer 모델은 아키텍처적으로 정확. 그러나 Teammate가 CLAUDE.md를 로드하면 **Layer 1-2의 시스템이 Layer 3 안에서 재실행**되므로, 레이어 분리가 "완벽한 격리"를 의미하지는 않음.

```
아리가 그린 그림:
Layer 3: Agent Teams ──── 별도
Layer 2: Dynamic Chain ── 별도   → "충돌 없음"
Layer 1: Subagents ────── 별도

실제 일어나는 일:
Layer 3: Agent Teams
  └── Teammate A
       ├── Layer 2: Dynamic Chain (CLAUDE.md에서 로드됨!)
       └── Layer 1: Subagents (Task 도구 사용 가능!)
  └── Teammate B
       ├── Layer 2: Dynamic Chain (또 로드됨!)
       └── Layer 1: Subagents (또 사용 가능!)
  → Layer 1-2가 Layer 3 안에서 N번 복제됨!
```

### 쟁점 5: 동시 사용 시나리오

| | 아리 | Cowork | 판정 |
|--|------|--------|------|
| 판단 | "양립 가능 (장점 강조)" | "가능하나 해결할 문제 있음" | **Cowork이 더 현실적** |

---

## 5. 아리 분석이 맞는 부분

아리 분석이 완전히 틀린 건 아닙니다:

| 맞는 점 | 설명 |
|---------|------|
| **레이어 모델 자체** | 실행 추상화 수준이 다른 것은 사실 |
| **단독 사용 시 무해** | Agent Teams를 활성화만 하고 팀을 생성하지 않으면 기존 시스템 영향 없음 |
| **기술적 양립 가능** | 동시 사용이 불가능한 것은 아님, 대비가 필요할 뿐 |
| **성능 비교** | 커스텀=일상작업, Teams=대규모병렬이라는 용도 구분은 정확 |
| **비유** | 오케스트라 vs 멀티밴드 비유는 직관적이고 정확 |

---

## 6. 수정된 종합 결론

| 질문 | 아리 원래 답변 | 수정 답변 |
|------|-------------|----------|
| 충돌하는가? | "아니오" | **이론적으로 아니오, 실무적으로 조건부** |
| 동시에 쓸 수 있나? | "가능" | **가능하나 Hook 분기 + Memory 잠금 필수** |
| 활성화하면 깨지나? | "아니오" | **활성화만으론 아니오, 팀 생성 시 문제 가능** |
| 뭐가 더 나은가? | "용도가 다름" | **용도가 다름 (이 판단은 유지)** |

---

## 7. Agent Teams 활성화 전 필수 해결 사항

| 우선순위 | 해결 사항 | 구현 방법 |
|---------|----------|----------|
| **필수** | Hook 분기 처리 | auto-analyze.sh에 teammate 감지 → 스킵 로직 추가 |
| **필수** | Memory 잠금 | Lead만 메모리 저장 (teammate는 결과를 Lead에 메시지) |
| **권장** | CLAUDE.md Lite | teammate용 200줄 이하 경량 버전 |
| **권장** | 오케스트레이션 분리 | 순차=Chain, 독립병렬=Teams 명확 구분 |
| **선택** | 상태 파일 분리 | /tmp/claude_prev_prompt_state_{SESSION_ID}.json |

---

## 8. 교훈

| 교훈 | 설명 |
|------|------|
| **이론 vs 실무** | 아키텍처 레이어 분리가 실행 환경 격리를 보장하지 않음 |
| **"호환"의 함정** | "작동한다 ≠ 문제없다". 부작용까지 분석해야 완전한 충돌 분석 |
| **동시성 고려** | 단일 세션 기준 설계는 멀티 세션에서 반드시 재검토 필요 |
| **두 관점의 가치** | 이론적 분석(구조 이해)과 실무적 분석(위험 식별) 모두 필요 |

---

*Deep Analysis by Ari (multidimensional_analyst + balanced_judge) | 2026-02-06*
*Referenced: 001_01 (Ari Analysis), 001_02 (Cowork Analysis), Official Agent Teams Documentation*
