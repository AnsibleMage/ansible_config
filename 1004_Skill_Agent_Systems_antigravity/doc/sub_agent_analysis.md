# 서브에이전트(Sub-agents) 구조 분석 보고서

**작성일**: 2026-01-24
**목적**: Claude Code의 서브에이전트 개념을 분석하고, Gemini Antigravity 내에서 **Main Agent**와 **Sub-agent**의 계층 관계를 정립하기 위함.

## 1. 개념적 정의 및 계층 구조

사용자께서 명시하신 대로, **Antigravity는 메인 "시스템(플랫폼)"이자 "최상위 에이전트"**입니다. 서브에이전트는 이 플랫폼 위에서 동작하는 **"독립적인 작업자(Worker)"**들입니다.

### 🏛️ 계층 구조 (Hierarchy)

*   **L0: Gemini Antigravity (The Platform & Host)**
    *   **정체성**: Google이 만든 최상위 코딩 에이전트.
    *   **권한**: 서브에이전트의 생성, 실행, 중단, 도구 할당 등 모든 라이프사이클을 관리.
    *   **역할**: 오케스트레이터(Orchestrator). 사용자의 모호한 요청을 해석하여 적절한 서브에이전트에게 위임하거나 직접 처리.
    *   **비유**: 회사의 **CEO** 또는 **작업 총괄 매니저**.

*   **L1: Sub-agents (The Workers)**
    *   **정체성**: 사용자가 정의한 전문 작업자 (e.g., Code Reviewer, System Architect).
    *   **구성**:
        *   **독립 컨텍스트**: 메인 대화와 분리된 자신만의 기억 공간을 가짐 (Clean Slate).
        *   **특화 도구(Specialized Tools)**: 자신의 역할에 필요한 도구만 사용 (예: 리뷰어는 ReadOnly).
        *   **목적 지향**: 특정 태스크(리뷰, 디버깅, 설계)만 수행하고 결과를 보고 후 사라짐.
    *   **비유**: 특정 프로젝트를 위해 고용된 **전문 계약직 프리랜서**.

## 2. Claude Code 서브에이전트의 핵심 메커니즘 (참조 문서 분석)

Claude Code 문서(`code.claude.com/docs/en/sub-agents`)에서 파악한 핵심 동작 원리는 다음과 같습니다:

1.  **Context Isolation (문맥 격리)**: 서브에이전트는 메인 대화의 잡음 없이 깨끗한 상태에서 시작합니다. 복잡한 문제를 해결할 때 메인 대화가 오염되는 것을 막습니다.
2.  **Tool Scoping (도구 제한)**: `code-reviewer`에게는 파일 수정(Edit) 권한을 빼앗고 읽기(Read) 권한만 주는 식으로 안전장치를 둡니다.
3.  **Automatic Delegation (자동 위임)**: 메인 에이전트가 사용자 요청을 보고 "아, 이건 `test-runner` 서브에이전트가 할 일이네"라고 판단하여 자동으로 작업을 넘깁니다.

## 3. Gemini Antigravity 적용 전략 (Sub-agent Pattern)

Antigravity에는 'Sub-agent'라는 명시적 기능명은 없지만, `Browser Subagent`와 같은 내부 구조를 볼 때 이 개념을 완벽하게 모사할 수 있습니다.

### 제안하는 구현 모델: "Workflow-Driven Sub-agents"

서브에이전트를 **"특정 Persona와 Toolset이 고정된 워크플로우"**로 정의합니다.

| 구분 | 구현 방식 | 설명 |
| :--- | :--- | :--- |
| **정의 (Definition)** | `~/.gemini/antigravity/personas/*.md` | 각 서브에이전트의 정체성, 프롬프트, 행동 지침 정의 파일. |
| **실행 (Execution)** | `Workflows (/agent-name)` | `/workflow system-architect` 처럼 호출. 워크플로우가 시작되면 해당 페르소나 파일 내용을 로드하고, **Task Boundary**를 설정하여 모드를 전환함. |
| **격리 (Isolation)** | `Task Boundary` | `task_boundary` 도구를 사용하여 시각적/논리적으로 작업 단위를 분리. |
| **도구 (Tools)** | `Skills` | 각 서브에이전트가 사용할 도구 꾸러미를 `global_skills`에 정의하고 워크플로우에서 "이 스킬을 사용하라"고 지시. |

## 4. 결론 및 요약

1.  **Antigravity (Main)**: 마에스트로. 모든 요청의 진입점. 사용자의 리더.
2.  **Sub-agents (Workers)**: Antigravity가 부리는 전문가들. (사용자가 가져온 Claude Code 기반 정의)
3.  **Skills (Tools)**: Sub-agents가 들고 다니는 공구함.

이 구조대로라면 에이전트(Persona)와 스킬(Tool)의 분리, 그리고 메인 에이전트와의 계층 관계가 명확해집니다. 이 구조로 이전을 진행하시겠습니까?
