# Gemini Evolution v2.0: 글로벌 스킬 아키텍처 (Global Skills Architecture)

**버전:** 2.0
**일자:** 2026-01-24
**작성자:** Antigravity (Gemini)

## 1. 개요 (Introduction)

Gemini Evolution v2.0은 기존 v1.0의 "서브에이전트(Sub-agent)" 패턴에서 **"통합된 글로벌 스킬 아키텍처(Unified Global Skills Architecture)"**로의 중대한 구조적 전환을 의미합니다.

v1.0에서는 "서브에이전트(정체성)"와 "스킬(도구)"을 구분했습니다. 하지만 v2.0에서는 **"스킬은 서브에이전트의 상위 호환(Superset)"**이라는 개념을 도입했습니다. 잘 구조화된 스킬은 단순한 도구(스크립트)뿐만 아니라, 복잡한 작업을 수행하는 데 필요한 페르소나(정체성)와 규칙을 모두 포함할 수 있기 때문입니다.

## 2. 핵심 개념: 상위 집합으로서의 스킬 (Skill as a Superset)

기존의 서브에이전트 정의는 단일 Markdown 파일에 페르소나를 정의하는 것에 그쳤습니다. 반면 Antigravity의 "스킬(Skill)"은 다음과 같은 요소를 모두 담을 수 있는 **디렉토리 구조**를 가집니다:

1.  **Identity (정체성)**: `SKILL.md`에 정의 (에이전트가 누구인지)
2.  **Rules (규칙)**: `SKILL.md`에 정의 (어떻게 행동해야 하는지)
3.  **Tools (도구)**: `scripts/` 디렉토리 (파이썬/쉘 스크립트를 통한 결정론적 작업 수행)
4.  **Resources (자원)**: `resources/` 디렉토리 (템플릿, 데이터 파일 등)

따라서 별도의 `personas/` 디렉토리가 필요하지 않으며, 모든 기능은 `global_skills/` 아래로 통합됩니다.

## 3. 디렉토리 구조 (Directory Structure)

모든 전역 기능의 새로운 표준 위치는 다음과 같습니다:

```
~/.gemini/antigravity/global_skills/
├── backend-developer/     # [변환된 서브에이전트]
│   └── SKILL.md
├── code-reviewer/         # [변환된 서브에이전트]
│   └── SKILL.md
├── git-commit-helper/     # [기존 스킬]
│   └── SKILL.md
├── skill-generator/       # [기존 스킬]
│   └── SKILL.md
├── system-architect/      # [변환된 서브에이전트]
│   └── SKILL.md
└── translation-specialist/ # [기존 스킬]
    ├── SKILL.md
    └── examples.md
```

## 4. 마이그레이션 전략 (v1.0 -> v2.0)

v1.0에서 v2.0으로 업그레이드하는 절차는 다음과 같습니다:

1.  **통합 (Consolidate)**: 분산된 모든 도구형 스킬을 `global_skills/`로 이동합니다.
2.  **변환 (Transform)**: "페르소나" Markdown 파일(`*.md`)을 스킬 폴더로 변환합니다.
    *   에이전트 역할에 맞는 폴더를 생성합니다 (예: `system-architect`).
    *   내부에 `SKILL.md` 파일을 생성합니다.
    *   기존 페르소나 파일의 "Role", "Expertise", "Rules" 섹션을 `SKILL.md`로 옮깁니다.
    *   표준 YAML Frontmatter를 추가합니다.

## 5. 사용 방법 (Usage)

Antigravity 시스템은 이 스킬들을 자동으로 인덱싱합니다.

- **암시적 호출 (Implicit Invocation)**: 에이전트가 현재 작업에 가장 적합한 스킬을 자연스럽게 선택하여 사용합니다.
- **명시적 호출 (Explicit Invocation)**: 사용자가 특정 기술의 이름을 언급(예: "**code-reviewer**를 사용해줘")하여 특정 페르소나나 전략을 강제로 활성화할 수 있습니다.

---
**상태:** 구현 및 검증 완료
**다음 단계:** 글로벌 스킬 라이브러리의 지속적인 확장
