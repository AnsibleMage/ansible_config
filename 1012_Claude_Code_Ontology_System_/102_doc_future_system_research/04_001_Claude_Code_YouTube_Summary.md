---
title: "클로드코드 유튜브 4개"
version: "1.0.0"
created: "2026-03-14"
updated: "2026-03-14"
tags: [claude-code, plugins, skill-creator, code-review, vibe-coding, workflow, youtube]
status: completed
source: Gemini 분석
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Gemini 생성 자료를 옵시디언 형식으로 변환

### 다음 작업 (TODO)
- [ ] 각 영상에서 추출한 워크플로우 패턴을 우리 체인 시스템과 매핑
- [ ] Skill Creator 평가 루프를 우리 quality_reviewer 에이전트에 적용 검토

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 4번 영상 "찐 개발자의 바이브 코딩 워크플로우"가 가장 실행 가능한 인사이트 포함
> - research.md → plan.md → 구현 패턴은 우리 DevChain과 직접 비교 가능
> - [[02_001_Claude_Code_Official_Docs_Core_Engine]]의 스킬/Hook 섹션과 교차 참조할 것

---

## Gemini의 응답

요청하신 4개 동영상의 상세 내용을 제목과 내용 형식으로 정리해 드립니다.

## 1. 프로젝트 생산성을 10배 높여주는 Claude Code 플러그인 10선

- **주요 내용:** 클로드 코드(Claude Code)의 생태계가 확장됨에 따라 생산성을 극대화할 수 있는 10가지 도구와 활용법을 소개합니다.

- **상세 도구:**

    - **Supabase CLI:** 데이터베이스 및 인증 처리에 최적화되어 있으며, MCP 서버보다 오버헤드가 적은 CLI 버전을 추천합니다.

    - **Skill Creator:** 엔스로픽에서 배포한 스킬로, 기존 스킬을 수정 및 개선하고 AB 테스트를 통해 성능을 측정할 수 있습니다.

    - **GSD (Get Stuff Done):** 새 프로젝트 생성 시 단계별 가드레일을 제공하고 컨텍스트를 효율적으로 관리해 주는 프레임워크입니다.

    - **NotebookLM 스킬:** 터미널에서 NotebookLM의 분석 및 산출물 생성 기능을 활용할 수 있게 해줍니다.

    - **기타:** 어브시디언(Obsidian)을 활용한 개인 비서 워크플로우, 배포 관리를 위한 Vercel CLI, 브라우저 자동화를 위한 Playwright CLI, GitHub CLI, 웹 스크래핑을 위한 Firecrawl, 그리고 자연어로 다이어그램을 그려주는 Excalidraw 스킬 등이 포함됩니다.

- **동영상 링크:** [https://youtu.be/E3CUMPzrsCM](https://www.google.com/search?q=https://youtu.be/E3CUMPzrsCM)


## 2. 클로드 코드 리뷰 기능 출시! 코드 검증 자동화 방법

- **주요 내용:** 엔스로픽이 공개한 '클로드 코드 리뷰' 기능을 통해 AI가 작성한 코드의 품질을 자동 검증하고 보안 취약점을 잡는 방법을 다룹니다.

- **핵심 기능:**

    - **에이전트 팀 구성:** 코드를 작성한 AI와 별개의 전문 에이전트들이 팀을 이뤄 논리 오류, 보안, 엣지 케이스를 검토하여 객관성을 유지합니다.

    - **심각도 표시:** 발견된 문제에 대해 반드시 고쳐야 할 버그(빨강), 권장 수정 사항(노랑), 기존 코드의 버그(보라)로 구분하여 표시합니다.

    - **커스터마이징:** `CLAUDE.md` 또는 `REVIEW.md` 파일을 통해 프로젝트별 특정 리뷰 규칙을 설정할 수 있습니다.

- **가치:** 사람이 직접 리뷰하기 어려운 방대한 양의 AI 생성 코드를 1차적으로 검증하여 시니어 엔지니어의 병목 현상을 해결해 줍니다.

- **동영상 링크:** [https://youtu.be/5-TTCYop5bo](https://www.google.com/search?q=https://youtu.be/5-TTCYop5bo)


## 3. 클로드 스킬 사용하신다면 skill-creator는 무조건 쓰세요

- **주요 내용:** 클로드 코드의 커스텀 스킬을 개발하고 개선하는 데 필수적인 'Skill Creator' 플러그인의 최신 업데이트 내용을 상세히 설명합니다.

- **주요 기능:**

    - **스킬 개선 루프:** 단순히 스킬을 생성하는 것을 넘어, 기존 스킬의 버그를 분석하고 개선 제안을 하는 기능이 추가되었습니다.

    - **워크스페이스 구조:** 개선 과정에서 `workspace` 디렉토리를 생성하여 구버전(Old)과 신버전(New)의 결과를 비교 분석하고 테스트 케이스를 관리합니다.

    - **에이전트 역할:** 채점을 담당하는 Grader, 비교 테스트를 하는 Comparator, 원인 분석을 하는 Analyzer 등 3개의 에이전트가 협업합니다.

- **실전 사례:** 영상의 무음 구간을 제거하는 스킬에서 발생한 싱크 오류를 Skill Creator를 통해 분석하고 해결하는 과정을 시연합니다.

- **동영상 링크:** [https://youtu.be/1Ffh2Obqxks](https://www.google.com/search?q=https://youtu.be/1Ffh2Obqxks)


## 4. 찐 개발자의 바이브 코딩은 다릅니다 - 클로드코드 실전 워크플로우

- **주요 내용:** 단순한 코드 생성이 아닌, 아키텍처 주도권을 유지하면서 복잡한 프로젝트를 성공시키는 실전 '바이브 코딩' 워크플로우를 공개합니다.

- **핵심 원칙:** "작성된 계획을 직접 검토하고 승인하기 전까지 클로드에게 코드를 절대 쓰게 하지 마라"는 기획과 코딩의 분리를 강조합니다.

- **워크플로우 단계:**

    1. **리서치 단계:** 관련 코드를 깊이 읽게 하고 `research.md`에 상세 보고서를 작성하게 합니다.

    2. **계획 단계:** 별도의 `plan.md` 파일을 생성하여 상세 구현 계획을 짜게 합니다.

    3. **주석 달기 및 반복:** 사람이 `plan.md`에 직접 메모를 달아 수정 사항을 반영시키며, 만족할 때까지 구현을 금지합니다.

    4. **구현 단계:** 모든 결정이 끝난 후 표준 프롬프트를 통해 기계적으로 코드를 생성하게 합니다.

- **동영상 링크:** [https://youtu.be/6Z6Le3Xwqdg](https://www.google.com/search?q=https://youtu.be/6Z6Le3Xwqdg)

## 관련 문서

### 직접 참조 (Direct Links)
- [[06_001_Agentic_Software_Engineering_Analysis#2.1 마크다운 기반의 영구적 메모리와 상태 공유 메커니즘|바이브 코딩 심층 분석]] — 4번 영상의 3단계 워크플로우를 테이블 + 역할 전환 개념으로 심화
- [[06_001_Agentic_Software_Engineering_Analysis#2.2 다중 에이전트 코드 검토|코드 리뷰 심층 분석]] — 2번 영상의 에이전트 팀 리뷰를 비용($15-25/PR), 커버리지(16%→54%) 수치와 함께 상세화
- [[06_001_Agentic_Software_Engineering_Analysis#3. 평가 루프 메커니즘|Skill Creator 심층 분석]] — 3번 영상의 Grader/Comparator/Analyzer를 "CFR/VFR 싱크 오류 자율 해결" 사례로 완전 전개

### 관련 주제 (Topic Links)
- [[02_001_Claude_Code_Official_Docs_Core_Engine#5.2 핵심 Frontmatter 필드|스킬 Frontmatter 스펙]] — 1번 영상의 Skill Creator가 활용하는 공식 스킬 시스템
- [[06_001_Agentic_Software_Engineering_Analysis#8. 결론 및 전략적 제언|에이전틱 결론]] — 4번 영상의 "계획 승인 전 코드 작성 금지" 원칙과 동일 철학
- [[05_001_Intelligence_Architecture_Ontology_Research#3.3 안드레이 카파시: 소프트웨어 3.0과 바이브 코딩|카파시의 SW 3.0]] — 4번 영상의 바이브 코딩이 카파시 비전의 실전 구현
- [[02_001_Claude_Code_Official_Docs_Core_Engine#6.1 핵심 패턴 요약|Plan Mode]] — 4번 영상의 외부 plan.md 방식과 공식 Plan Mode(Shift+Tab)의 대안적 비교

### 역참조 (Backlinks)
- [[06_001_Agentic_Software_Engineering_Analysis#2. 미시적 워크플로우 분석]] — 이 영상 요약을 산업 분석으로 확장

---

## Release Notes

### v1.0.0 (2026-03-14)
- Gemini 생성 자료를 옵시디언 형식으로 변환 (frontmatter, handoff, release notes, 위키링크 추가)
> **프롬프트 (형식 변환):** "102_doc_future_system_research 폴더에 신규파일이 4개 추가 되었어 제미나이로 만든 자료야. 현재 폴더의 옵시디언 문법으로 형식을 수정해줘 내용은 절대 건드리지마"
> **프롬프트 (파일명 변경):** "파일명도 규칙 지켜서 변경해줘"
> **원본 생성:** Gemini (앤 직접 생성)
