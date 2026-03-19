# 012. Skills vs Subagent 구조적 비교 분석

> **작성일**: 2026-02-03
> **버전**: 1.0
> **관련**: [[011_Stop-Hook-Auto-Memory-Save-System]], [[004_Dynamic-Chain-Orchestration-System]]

---

## 개요

Claude Code의 두 가지 확장 메커니즘인 **Skills**와 **Subagent**의 구조적 차이점과 상호보완 관계를 분석한다.

### 핵심 결론

> **Skills는 "무엇을 아는가"를 구조화하고, Subagent는 "어떻게 실행할 것인가"를 분산한다. 둘은 상위호환이 아닌 상호보완 관계다.**

---

## 1. SkillsMP 마켓플레이스

### 기본 정보

| 항목 | 내용 |
|------|------|
| **URL** | https://skillsmp.com |
| **Skills 수** | 87,000+ |
| **API 키** | 불필요 (무료 오픈소스) |
| **포맷** | SKILL.md 오픈 표준 |
| **호환성** | Claude Code, OpenAI Codex CLI |

### 설치 방법

```bash
# GitHub에서 클론
git clone https://github.com/user/some-skill

# 개인 Skills 폴더에 복사
cp -r some-skill ~/.claude/skills/

# 또는 프로젝트 Skills 폴더에 복사
cp -r some-skill .claude/skills/
```

### Skills 폴더 구조

```
my-skill/
├── SKILL.md          # 메타데이터 + 지침 (필수)
├── scripts/
│   ├── validate.py   # 검증 스크립트
│   └── generate.sh   # 생성 스크립트
├── references/
│   ├── api-spec.json # API 명세
│   └── examples/     # 예제 코드
├── assets/
│   └── templates/    # 템플릿 파일
└── docs/
    └── advanced.md   # 고급 가이드
```

### SKILL.md 필수 구조

```yaml
---
name: "My Skill Name"        # 필수, 최대 64자
description: "What it does"  # 필수, 최대 200자
disable-model-invocation: false  # Claude 자동 호출 허용
user-invocable: true             # 사용자 /명령어 허용
---

# Skill Instructions

여기에 Claude가 따를 지침 작성...
```

---

## 2. Skills vs Subagent 비교

### 본질적 차이

| 구분 | Skills | Subagent |
|------|--------|----------|
| **본질** | 주입된 지침 (Injected Instructions) | 독립 프로세스 (Independent Process) |
| **구조** | 다중 파일/폴더 | 단일 프롬프트 |
| **실행** | 메인 컨텍스트 내 | 별도 컨텍스트 |
| **모델** | 메인 세션 모델 사용 | model 파라미터로 선택 가능 |
| **용량** | 무제한 (백과사전 수준 가능) | 컨텍스트 윈도우 제한 (~200K tokens) |

### Skills 강점 (Subagent보다 나은 점)

| 강점 | 설명 |
|------|------|
| **지식 용량** | 폴더 구조로 무제한 확장, 백과사전 수준 룰 가능 |
| **Progressive Disclosure** | 필요시만 파일 로드, 컨텍스트 효율화 |
| **재사용성** | 마켓플레이스 87,000+ 공유 |
| **표준화** | SKILL.md 포맷 강제, 팀 협업 용이 |
| **Git 친화적** | 폴더 구조로 버전 관리 자연스러움 |

### Subagent 강점 (Skills보다 나은 점)

| 강점 | 설명 |
|------|------|
| **병렬 실행** | 여러 태스크 동시 처리 (Skills는 불가) |
| **모델 선택** | opus/sonnet/haiku 태스크별 최적 모델 |
| **비용 최적화** | 단순 작업에 저렴한 모델 사용 |
| **컨텍스트 격리** | 실험/분석 시 오염 방지 |
| **실패 격리** | 한 Subagent 실패가 전체 영향 안함 |

---

## 3. 5차원 분석 요약

### 시간적 차원 (Temporal)

| 시점 | Skills | Subagent |
|------|--------|----------|
| **과거** | 단순 프롬프트 주입 | Task 도구로 병렬 지원 |
| **현재** | SKILL.md 표준화, 마켓플레이스 | 체인 패턴 통합, 오케스트레이션 |
| **미래** | Skills 컴포지션, 자가 진화 | 멀티-에이전트 메모리 공유 |

### 공간적 차원 (Spatial)

| 범위 | Skills | Subagent |
|------|--------|----------|
| **로컬** | 깊은 도메인 지식 | 병렬 실행 필요시 |
| **팀** | 표준화된 협업 (9/10) | 유연하지만 표준 부재 (6/10) |
| **글로벌** | 87,000+ 에코시스템 | 개인/팀 단위 보관 |

### 추상화 수준 (Abstraction)

| 수준 | Skills | Subagent |
|------|--------|----------|
| **구체적** | 폴더/파일 구조 | 단일 프롬프트 |
| **설계 패턴** | Progressive Disclosure | Composition |
| **철학** | "지식을 구조화하라" | "실행을 분산하라" |

### 인과 관계 (Causal)

```
문제 공간
    │
┌───┴───┐
│       │
지식    실행
복잡성  복잡성
│       │
▼       ▼
Skills  Subagent
```

### 규모 차원 (Scale)

| 규모 | Skills | Subagent | 권장 |
|------|--------|----------|------|
| 소규모 | ★★★ | ★★ | Skills 또는 직접 |
| 중규모 | ★★★★ | ★★★ | **조합** |
| 대규모 | ★★★★★ | ★★★★ | **조합** |

---

## 4. 선택 가이드

### Skills 사용 시점

```
[Skills 선택 체크리스트]
□ 도메인 지식이 복잡하고 방대함
□ 규칙/체크리스트/템플릿이 필요함
□ 재사용 빈도가 높음
□ 팀 간 표준화가 필요함
□ Progressive disclosure가 유리함
```

### Subagent 사용 시점

```
[Subagent 선택 체크리스트]
□ 병렬 처리가 필요함
□ 태스크별 다른 모델이 최적
□ 비용 최적화가 중요함
□ 컨텍스트 격리가 필요함
□ 실패 격리가 중요함
```

### 결정 플로우차트

```
시작
  │
  ▼
┌─────────────────────┐
│ 병렬 실행 필요?      │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
   Yes         No
    │           │
    ▼           ▼
Subagent   ┌─────────────────┐
           │ 모델 선택 필요?  │
           └─────────┬───────┘
                     │
               ┌─────┴─────┐
              Yes         No
               │           │
               ▼           ▼
          Subagent    ┌─────────────────┐
                      │ 지식 복잡도 높음?│
                      └─────────┬───────┘
                                │
                          ┌─────┴─────┐
                         Yes         No
                          │           │
                          ▼           ▼
                       Skills      직접 처리
```

---

## 5. 최적 조합 패턴

### 패턴 1: Skills-First, Subagent-Execute

```
Skills로 지식/규칙 로드 → Subagent로 병렬 실행

예시: Rails 8 개발
/rails-dev (Skill: TDD 규칙 로드)
    → code_developer (Subagent, sonnet: 코드 생성)
    → quality_reviewer (Subagent, sonnet: 리뷰)
```

### 패턴 2: Subagent-Analyze, Skills-Apply

```
Subagent로 분석 → Skills로 적용

예시: 코드베이스 분석
multidimensional_analyst (Subagent, opus: 분석)
    → /coding-standards (Skill: 표준 적용)
```

### 패턴 3: Hybrid Chain (제안)

```
[Skill로 지식 로드] → (Subagent[O] ∥ Subagent[S]) → [Skill로 결과 적용]

사용 시점:
- 복잡한 도메인 지식 + 병렬 분석 필요
- 비용 최적화 + 품질 유지 동시 필요
- 대규모 프로젝트의 반복 워크플로우
```

---

## 6. Stop Hook 에러 해결 (부록)

### 문제

Stop hook에서 `hookSpecificOutput` 사용 시 스키마 에러 발생

```
Stop hook error: JSON validation failed
- hookSpecificOutput → Stop hook에서 미지원
```

### 원인

Stop hook은 응답 **완료 후** 실행되어 Claude에게 추가 작업을 시킬 수 없음

### 해결책

Stop hook 제거 → **지침 기반 메모리 저장**으로 전환 (CLAUDE.md V3.6)

```
작업 완료
    ↓
메모리 저장 여부 판단 (응답 내에서)
    ↓
저장 실행
    ↓
🎵 완료!
```

---

## 참고 자료

### 외부 링크

- [SkillsMP - Agent Skills Marketplace](https://skillsmp.com/)
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [GitHub - anthropics/skills](https://github.com/anthropics/skills)
- [Claude Code Has a Skills Marketplace Now - Medium](https://medium.com/@markchen69/claude-code-has-a-skills-marketplace-now-a-beginner-friendly-walkthrough-8adeb67cdc89)

### 관련 문서

- [[004_Dynamic-Chain-Orchestration-System]]
- [[007_Claude-Code-Settings-Configuration]]
- [[011_Stop-Hook-Auto-Memory-Save-System]]

---

*Skills vs Subagent 구조적 비교 분석 - 2026-02-03*
