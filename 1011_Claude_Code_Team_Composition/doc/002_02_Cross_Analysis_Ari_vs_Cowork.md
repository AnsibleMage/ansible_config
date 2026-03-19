# 심층 교차 분석: 아리(Claude Code) vs Cowork 분석 비교

> 동일 주제(Agent Teams vs Dynamic Chain)를 두 환경에서 독립 분석한 결과 비교
> 작성일: 2026-02-06 | 기준: 001_01 (아리) vs 001_02 (Cowork)

---

## 결론 요약

**아리(클로드 코드)는 낙관적, Cowork은 신중했는데 — 공식 문서를 보면 둘 다 부분적으로 맞고 부분적으로 틀렸습니다.**

| 분석 항목 | 아리 (001_01) | Cowork (001_02) | 공식 문서 기준 정답 |
|-----------|:---:|:---:|---|
| 레이어 구분 | O | - | 아리가 더 정확. 4-Layer 구분 모델이 명쾌 |
| 동시 사용 가능성 | O | O | 둘 다 맞음. 가능하지만 조건부 |
| Hook 상속 위험 | X (누락) | O | **Cowork이 맞음.** teammate가 hooks 포함 settings 상속 |
| Memory Race | X (누락) | O | **Cowork이 맞음.** 동시 파일 쓰기 = 공식 경고 사항 |
| 오케스트레이션 충돌 | O | △ (과잉) | 아리가 더 정확. 레이어가 달라서 시스템 충돌 아님 |
| 토큰 비용 | O | O | 둘 다 맞음 |
| 실용적 권장사항 | △ (단순) | O | Cowork이 더 구체적 (5개 개선안) |

> **한마디: 아리는 숲을 잘 봤고, Cowork은 나무를 잘 봤다. 둘을 합치면 가장 완전한 그림이 된다.**

---

## 1. 핵심 차이점 3가지

### 차이 1: Hook 상속에 대한 관점

**아리 (001_01):**
- Hook 시스템 → "호환"으로 표시
- 구체적 부작용 분석 없음

**Cowork (001_02):**
- Hook Inheritance → **HIGH** 충돌
- teammate마다 4-Layer 분석 중복 실행 (3명 × 10회 = 30회)
- /tmp/claude_prev_prompt_state.json 상태 파일 충돌

**공식 문서 판정:** Cowork이 맞음. teammate는 lead의 permission settings과 hooks를 그대로 상속하며, 앤의 UserPromptSubmit hook(auto-analyze.sh)이 모든 teammate에서 독립 실행될 가능성이 있음.

### 차이 2: Memory System Race Condition

**아리 (001_01):**
- 아예 언급하지 않음

**Cowork (001_02):**
- **HIGH** 이슈로 지적
- 동시 SEQ 번호 산출 → 파일 덮어쓰기 위험
- 중복 방지 규칙이 동시성 환경에서 무력화

**공식 문서 판정:** Cowork이 맞음. 공식 문서에 "Two teammates editing the same file leads to overwrites and lost work"라는 명시적 경고가 있으며, ~/.claude/memory/ 동시 쓰기도 이 범주에 해당. 또한 "Cleanup must use the lead. Teammates should not run cleanup because their team context may not resolve correctly"라는 경고도 앤의 "응답 완료 프로토콜"과 충돌함.

### 차이 3: 오케스트레이션 충돌

**아리 (001_01):**
- "추상화 레이어가 다르다" → 충돌 없음
- 4-Layer 모델로 명쾌하게 설명

```
Layer 3: Agent Teams (OS 프로세스 레벨)
Layer 2: Dynamic Chain (오케스트레이션 레벨)
Layer 1: Subagents (도구 호출 레벨)
Layer 0: Claude Code Core (런타임)
```

**Cowork (001_02):**
- Chain vs Team Orchestration Overlap → **MEDIUM** 충돌
- Lead가 DevChain + teammate에게 같은 작업 할당 = 이중 실행 위험

**공식 문서 판정:** 아리가 더 정확. 체인은 세션 내부에서 돌아가고 Agent Teams는 세션 외부이므로, 이중 실행은 "시스템 충돌"이 아니라 "사용자 실수" 범주. Cowork이 과대평가함.

---

## 2. 아리가 맞은 것

### 레이어 구분 모델

아리의 4-Layer 추상화 모델은 두 시스템의 관계를 가장 명확하게 설명합니다:

- 커스텀 시스템 = **Layer 1~2** (세션 내부)
- Agent Teams = **Layer 3** (세션 외부)
- 서로 다른 레이어이므로 **실행 로직**이 겹치지 않음

### 동시 사용 시나리오

"팀메이트 안에서 커스텀 체인이 실행된다"는 시나리오는 공식 문서와 부합합니다. teammate는 CLAUDE.md를 로드하고, 스킬/MCP가 활성화되고, 일반 세션과 동일한 도구에 접근합니다.

### 비유의 적절성

- 앤의 시스템 = 한 명의 지휘자가 파트를 지시하는 **오케스트라**
- Agent Teams = 여러 밴드가 각자 연습하고 대화하는 **멀티밴드 콜라보**

---

## 3. 아리가 틀리거나 누락한 것

### Hook "호환"의 함정

아리는 Hook 시스템을 단순히 "호환"으로 적었지만, **구체적 부작용을 분석하지 않았음:**

- 앤의 settings.json UserPromptSubmit hook → 모든 teammate에서 독립 실행
- 4-Layer 분석 30회 중복 = 불필요한 토큰 소비
- prompt_analyzer.py MCP 동시 접근 경합

### Memory System 완전 누락

아리는 메모리 시스템 충돌을 아예 언급하지 않음. 공식 문서의 동시 파일 쓰기 경고와 cleanup lead 전용 원칙을 고려하면, 이는 중대한 분석 누락.

### 권장사항의 구체성 부족

아리: "일상 작업 → 커스텀, 대규모 → Agent Teams, 안정화 후 → 통합 검토" (3줄)
Cowork: Hook 분기 처리, Memory 잠금, 오케스트레이션 분리, CLAUDE.md Lite, Migration Path (5개 구체적 개선안)

---

## 4. Cowork이 맞은 것

### Hook 중복 실행 (HIGH)

공식 문서의 teammate permission/settings 상속 + 앤의 UserPromptSubmit hook 조합을 정확히 분석. 이는 실제 동시 사용 시 가장 먼저 발생할 문제.

### Memory Race Condition (HIGH)

공식 문서의 "Two teammates editing the same file leads to overwrites" 경고와 정확히 부합하는 분석.

### 구체적 개선안 5가지

실행 가능한 수준의 개선 방안:
1. Team-Aware Hooks (환경변수 감지)
2. Memory Locking Mechanism (3가지 옵션)
3. Orchestration Layer 분리 (시나리오별 매트릭스)
4. CLAUDE.md Lite for Teammates
5. Chain-to-Team Migration Path

---

## 5. Cowork이 틀리거나 과한 것

### 오케스트레이션 충돌 과대평가

"Chain vs Team Orchestration Overlap"을 MEDIUM으로 잡았지만, 아리의 레이어 분석이 더 정확. Lead가 DevChain을 실행하면서 동시에 teammate에게 같은 작업을 할당하는 건 사용자가 의도적으로 하지 않는 한 일어나지 않음. "시스템 충돌"이 아니라 "사용자 실수" 범주.

---

## 6. 왜 다르게 분석했나?

| 요인 | 아리 (Claude Code) | Cowork |
|------|-------------------|--------|
| **실행 환경** | 앤의 CLAUDE.md V3.8 시스템 안에서 실행 | 독립된 Cowork 세션에서 외부 관찰 |
| **관점** | 내부자 (시스템의 일부) | 외부자 (시스템을 관찰) |
| **성향** | 자기 시스템에 대한 긍정적 편향 가능 | 보수적/방어적 분석 성향 |
| **접근법** | 아키텍처 레벨 추상화 (top-down) | 구체적 위험 시나리오 열거 (bottom-up) |
| **강점** | 큰 그림, 레이어 모델, 비유 | 세부 위험, 구체적 개선안 |

---

## 7. 통합 권장사항

두 분석을 합친 최종 판단:

1. **기본 구조는 안전하다** (아리의 레이어 분석 기반) — 두 시스템은 서로 다른 추상화 레이어에서 작동하므로 실행 로직 충돌은 없음
2. **공유 자원에서 위험이 있다** (Cowork의 세부 분석 기반) — Hook, Memory, /tmp 상태 파일 등 공유 자원에서 구체적 충돌 발생 가능
3. **단기: 기존 시스템 유지** — Agent Teams 미활성화 상태에서 안전
4. **중기: Hook 분기 + Memory 잠금 구현** — 동시 사용 전 필수
5. **장기: 병렬성 높은 체인(Research/Game/WebDev)을 Agent Teams로 점진적 전환**

---

*Cross-analyzed by Cowork session | 2026-02-06*
*Sources: 001_01 (Ari/Claude Code), 001_02 (Cowork), Official Claude Code Docs*
