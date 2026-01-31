# 🌌 Antigravity System: 생성형 에이전트 오케스트레이터

[![Version](https://img.shields.io/badge/Version-2.0.0-purple)](./) [![Agent](https://img.shields.io/badge/Agent-Antigravity-8A2BE2)](./)

> *"도구를 넘어선 자율적 오케스트레이션의 시작."*

이 폴더는 **Antigravity (안티그래비티)**의 **전체 설정과 두뇌(Brain)**를 담고 있습니다.
"에이전트 시스템 씽킹(Agent Systems Thinking)" 프레임워크가 진화하여, 완전한 "동적 체인 시스템(Dynamic Chain System)"으로 구현된 결과물입니다.

---

## 🏛️ 핵심 정체성 (Core Identity)

**Antigravity**는 단순한 챗봇이 아닙니다. Google DeepMind의 가이드라인을 따라 설계된 **선제적 오케스트레이션 에이전트**입니다.

*   **Proactive (선제적)**: 사용자가 요청하기 전에 검증, 테스트, 수정을 제안하고 실행합니다.
*   **Context-First (문맥 우선)**: `translation-specialist`라는 전두엽을 사용하여 사용자 의도를 4단계(어휘/통사/담화/화용)로 파악한 후 행동합니다.
*   **Dynamic (동적)**: 숨겨진 니즈에 맞춰 실행 체인(순차/병렬/혼합)을 실시간으로 조립합니다.

---

## 🧠 시스템 아키텍처

### 1. 전역 설정 (`00_Config_GEMINI_Global_Setting.md`)
시스템의 심장인 `GEMINI.md`는 다음을 정의합니다:
*   **워크플로우 엔진**: 5단계 루프 (인지 → 계획 → 실행 → 검증 → **기억**).
*   **트리거 시스템**: 16개 스킬을 호출하는 이중 레이어(키워드 + 의미론적) 트리거.
*   **기억 시스템**: `context_log.json`에 의사결정과 문맥을 자동 기록하는 메커니즘.

### 2. 스킬 생태계 (`global_skills/`)
이전 시스템에서 마이그레이션된 20개 이상의 전문 스킬 라이브러리:
*   **인지 레이어**: `insight-explorer`, `multidimensional-analyst`, `integrated-sage` 등.
*   **역할 레이어**: `system-architect`, `code-developer`, `quality-reviewer` 등.
*   **메타 레이어**: `quality-manager`, `context-manager`, `translation-specialist`.

### 3. 브레인 아카이브 (`doc/`)
이 시스템을 구축하기 위해 수행된 연구, 분석, 계획 문서의 집대성:
*   **분석서**: 시스템 씽킹, 기억 아키텍처, 서브 에이전트 기능 분석.
*   **연구 보고서**: 동적 체인 및 트리거 메커니즘 연구.
*   **감사 로그**: 마이그레이션 로그 및 검증 워크스루.

---

## 📂 파일 구조

```text
1004_Skill_Agent_Systems_antigravity/
├── 00_Config_GEMINI_Global_Setting.md   # [ CORE ] 최종 완성된 V2.0 설정 파일
├── 01_Analysis_Gemini_Basic.md          # 제미나이 기본 역량 분석
├── 02_Analysis_Sub_Agents.md            # 서브 에이전트 아키텍처 심층 분석
├── 03_Analysis_Agent_Framework.md       # 16 에이전트 사고 프레임워크 분석
├── 04_Audit_Pre_Migration.md            # 시스템 마이그레이션 전 감사 로그
├── 05_Plan_Migration_Strategy.md        # 단계별 구현 계획서
├── 06_Report_Migration_Results.md       # 최종 워크스루 및 검증 리포트
├── 07_Research_Dynamic_Chains.md        # 에이전트 체인 및 트리거 연구 보고서
└── 08_Analysis_Memory_System.md         # Active Memory System 아키텍처 분석
```

---

## 🚀 설치 방법

로컬 Gemini 환경에서 Antigravity 시스템을 활성화하려면:

1.  **설정 배포**:
    `00_Config_GEMINI_Global_Setting.md` 내용을 `~/.gemini/GEMINI.md`로 복사합니다.

2.  **스킬 배포**:
    `global_skills/` 폴더의 내용을 `~/.gemini/antigravity/global_skills/`로 마이그레이션합니다.

3.  **기억 활성화**:
    `~/.gemini/antigravity/memory/` 디렉토리를 생성하고 `context_log.json`을 초기화합니다 (`08_Analysis_Memory_System.md` 참조).

---

*Verified and Archived by Antigravity.*
