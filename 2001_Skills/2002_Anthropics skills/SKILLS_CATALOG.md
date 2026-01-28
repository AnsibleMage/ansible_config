# Skills Catalog

> **Last Updated**: 2026-01-28  
> **Total Skills**: 16  
> **Repository**: skills-main

이 문서는 `skills-main` 저장소에서 사용 가능한 모든 스킬의 종합 카탈로그입니다. 각 스킬의 명칭, 설명, 트리거 조건, 주요 기능 및 생성 포맷 정보를 포함합니다.

---

## 📑 목차

- [문서 및 데이터 처리](#문서-및-데이터-처리)
- [디자인 및 시각 예술](#디자인-및-시각-예술)
- [웹 및 소프트웨어 개발](#웹-및-소프트웨어-개발)
- [전문 지원 및 커뮤니케이션](#전문-지원-및-커뮤니케이션)

---

## 문서 및 데이터 처리

### 1. docx

**명칭**: DOCX Document Processing  
**라이선스**: Proprietary (LICENSE.txt 참조)

**설명**:  
Microsoft Word 문서(.docx)의 생성, 편집, 분석을 위한 종합 도구입니다. 추적된 변경 사항(tracked changes), 주석(comments), 서식 보존 및 텍스트 추출을 지원합니다.

**트리거 조건**:
- 새 문서 생성 요청
- 기존 문서 수정 또는 편집
- 추적된 변경 사항 작업
- 주석 추가
- 기타 문서 관련 작업

**주요 기능**:
- OOXML 형식 직접 조작 (unpack/pack)
- Redlining 워크플로우 (tracked changes)
- `pandoc` 및 `docx-js`를 통한 문서 생성
- XML 기반 고급 편집

**생성 포맷**:
- `.docx` (Microsoft Word 문서)
- Markdown 변환 출력

**주요 도구**:
- `pandoc` (텍스트 추출)
- `docx-js` (문서 생성)
- OOXML 라이브러리 (고급 편집)

---

### 2. pdf

**명칭**: PDF Processing Toolkit  
**라이선스**: Proprietary (LICENSE.txt 참조)

**설명**:  
PDF 문서의 텍스트 및 테이블 추출, 새 PDF 생성, 병합/분할, 양식 작성을 위한 종합 도구입니다.

**트리거 조건**:
- PDF 양식 작성
- 프로그래밍 방식의 PDF 처리
- 대규모 PDF 문서 생성 또는 분석

**주요 기능**:
- 텍스트 및 테이블 추출 (`pdfplumber`)
- PDF 병합, 분할, 회전 (`pypdf`)
- 새 PDF 생성 (`reportlab`)
- OCR 처리 (스캔된 PDF)
- 양식 자동 기입

**생성 포맷**:
- `.pdf` (PDF 문서)
- 추출된 텍스트 (`.txt`)
- 이미지 (`.jpg`, `.png`)

**주요 도구**:
- `pypdf`, `pdfplumber` (Python)
- `reportlab` (PDF 생성)
- `qpdf`, `pdftotext` (CLI)

---

### 3. pptx

**명칭**: PowerPoint Presentation Creation & Editing  
**라이선스**: Proprietary (LICENSE.txt 참조)

**설명**:  
프레젠테이션(.pptx) 생성, 편집, 분석을 위한 도구입니다. 레이아웃, 주석, 발표자 노트 작업을 지원하며, `html2pptx` 워크플로우를 통해 정밀한 디자인이 가능합니다.

**트리거 조건**:
- 새 프레젠테이션 생성
- 콘텐츠 수정 또는 편집
- 레이아웃 작업
- 주석 또는 발표자 노트 추가

**주요 기능**:
- HTML을 PowerPoint로 변환 (`html2pptx.js`)
- 템플릿 기반 프레젠테이션 생성
- 슬라이드 재배열 및 복제 (`rearrange.py`)
- 텍스트 인벤토리 및 일괄 교체 (`inventory.py`, `replace.py`)
- 썸네일 그리드 생성 (`thumbnail.py`)

**생성 포맷**:
- `.pptx` (PowerPoint 프레젠테이션)
- 썸네일 이미지 (`.jpg`)

**주요 도구**:
- `html2pptx` (JavaScript)
- `python-pptx` (Python)
- `markitdown` (텍스트 추출)

**디자인 원칙**:
- 콘텐츠에 맞는 컬러 팔레트 선택 (18가지 예시 제공)
- 웹 안전 폰트 사용
- 명확한 시각적 계층 구조

---

### 4. xlsx

**명칭**: Excel Spreadsheet Processing  
**라이선스**: Proprietary (LICENSE.txt 참조)

**설명**:  
수식, 서식, 데이터 분석 및 시각화를 지원하는 종합 스프레드시트 도구입니다. 수식 중심의 동적 스프레드시트 생성을 강조합니다.

**트리거 조건**:
- 수식 및 서식이 포함된 새 스프레드시트 생성
- 데이터 읽기 또는 분석
- 수식을 보존하면서 기존 스프레드시트 수정
- 데이터 분석 및 시각화
- 수식 재계산

**주요 기능**:
- 수식 기반 스프레드시트 생성 (`openpyxl`)
- 데이터 분석 (`pandas`)
- 수식 자동 재계산 (`recalc.py` with LibreOffice)
- 재무 모델링 표준 (색상 코딩, 숫자 형식)
- 수식 오류 검증 (#REF!, #DIV/0! 등)

**생성 포맷**:
- `.xlsx`, `.xlsm` (Excel 스프레드시트)
- `.csv`, `.tsv` (데이터 내보내기)

**주요 도구**:
- `openpyxl` (수식 및 서식)
- `pandas` (데이터 분석)
- LibreOffice (수식 재계산)

**중요 원칙**:
- ❌ Python에서 계산하여 값 하드코딩 금지
- ✅ 항상 Excel 수식 사용 (동적 업데이트 가능)

---

### 5. doc-coauthoring

**명칭**: Document Co-authoring Workflow  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
협업 문서 작성을 위한 구조화된 워크플로우입니다. 문맥 수집, 구조화 및 정제, 독자 테스트의 3단계로 구성됩니다.

**트리거 조건**:
- 긴 형식의 문서 작성 프로젝트
- 반복적인 피드백이 필요한 문서
- 독자 관점의 명확성 검증이 필요한 경우

**주요 기능**:
- **1단계: Context Gathering** - 배경, 목표, 대상 독자 파악
- **2단계: Refinement & Structure** - 섹션별 브레인스토밍 및 작성
- **3단계: Reader Testing** - 새로운 Claude 인스턴스로 문서 테스트

**생성 포맷**:
- Markdown 문서 (`.md`)
- 아티팩트 기반 협업 문서

**워크플로우 특징**:
- 섹션별 반복 작업
- 독자 관점의 블라인드 스팟 식별
- 아티팩트 관리 및 버전 관리

---

## 디자인 및 시각 예술

### 6. algorithmic-art

**명칭**: Algorithmic Art with p5.js  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
p5.js를 사용하여 알고리즘 기반 예술을 생성합니다. 먼저 "계산 철학(computational philosophy)"을 정의한 후, 이를 제너레이티브 아트로 표현합니다.

**트리거 조건**:
- 알고리즘 아트 생성 요청
- 제너레이티브 디자인 프로젝트
- p5.js 기반 시각화

**주요 기능**:
- 2단계 프로세스: 철학 정의 → 코드 구현
- Seeded randomness (재현 가능한 무작위성)
- 파라미터화된 디자인
- HTML 아티팩트로 출력

**생성 포맷**:
- `.html` (p5.js 인터랙티브 아트)
- `.md` (철학/매니페스토 문서)

**핵심 원칙**:
- 명확한 예술적 비전
- 전문가 수준의 장인정신
- 파라미터 조정 가능한 구조

---

### 7. brand-guidelines

**명칭**: Anthropic Brand Guidelines  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
Anthropic의 공식 브랜드 컬러 및 타이포그래피를 아티팩트에 적용하기 위한 가이드입니다.

**트리거 조건**:
- Anthropic 브랜딩이 필요한 아티팩트 생성
- 공식 컬러 및 폰트 적용

**주요 기능**:
- 공식 컬러 팔레트 적용
  - Dark: `#141413`
  - Light: `#faf9f5`
  - Orange Accent: `#d97757`
- 타이포그래피 표준
  - 헤딩: Poppins
  - 본문: Lora
- 스마트 폰트 적용 및 텍스트 스타일링

**생성 포맷**:
- 브랜딩이 적용된 HTML, PDF, 이미지 등

**기술적 세부사항**:
- Google Fonts 통합
- Fallback 폰트 지원
- 액센트 컬러를 활용한 도형 강조

---

### 8. canvas-design

**명칭**: Visual Art & Design Artifacts  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
시각 예술 및 디자인 아티팩트(.pdf, .png)를 생성합니다. "시각 철학(visual philosophy)"을 기반으로 형태, 공간, 색상, 구성에 집중합니다.

**트리거 조건**:
- 시각적 디자인 아티팩트 생성
- 포스터, 인포그래픽 등 그래픽 디자인
- 최소한의 텍스트로 강력한 시각적 임팩트 필요

**주요 기능**:
- 시각 철학 정의 (매니페스토)
- 형태, 공간, 색상, 구성 중심 디자인
- 최소한의 텍스트 사용
- 프리미엄 디자인 품질

**생성 포맷**:
- `.pdf` (고품질 벡터)
- `.png` (래스터 이미지)
- 단일 자체 포함 HTML 아티팩트

**디자인 원칙**:
- 대담한 심미적 방향성
- 전문가 수준의 장인정신
- 일반적인 AI 디자인 회피

---

### 9. theme-factory

**명칭**: Theme Factory  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
아티팩트에 테마를 적용하기 위한 도구입니다. 10가지 프리셋 테마 또는 커스텀 테마를 슬라이드, 문서, 리포트, HTML 랜딩 페이지 등에 적용할 수 있습니다.

**트리거 조건**:
- 프레젠테이션 또는 문서 스타일링
- 일관된 컬러 팔레트 및 폰트 적용
- 전문적인 시각적 정체성 필요

**주요 기능**:
- 10가지 프리셋 테마 제공
  - Ocean Depths, Sunset Boulevard, Forest Canopy
  - Modern Minimalist, Golden Hour, Arctic Frost
  - Desert Rose, Tech Innovation, Botanical Garden, Midnight Galaxy
- 커스텀 테마 생성 기능
- 컬러 팔레트 및 폰트 페어링

**생성 포맷**:
- 테마가 적용된 `.pptx`, `.pdf`, `.html` 등

**사용 프로세스**:
1. `theme-showcase.pdf` 표시
2. 사용자 선택 대기
3. 선택된 테마 적용

---

### 10. slack-gif-creator

**명칭**: Slack GIF Creator  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
Slack에 최적화된 애니메이션 GIF를 생성하는 도구입니다. 제약 조건, 검증 도구 및 애니메이션 개념을 제공합니다.

**트리거 조건**:
- Slack용 애니메이션 GIF 요청
- "X가 Y를 하는 GIF 만들어줘" 형태의 요청

**주요 기능**:
- Slack 요구사항 준수 (128x128 이모지, 480x480 메시지)
- PIL ImageDraw 기반 그래픽 생성
- 이징 함수 (easing functions)
- 애니메이션 개념 (shake, pulse, bounce, spin, fade, slide, zoom, explode)

**생성 포맷**:
- `.gif` (최적화된 애니메이션 GIF)

**주요 도구**:
- `GIFBuilder` (core.gif_builder)
- `validators` (core.validators)
- `easing` (core.easing)
- `frame_composer` (core.frame_composer)

**최적화 전략**:
- 낮은 FPS (10-30)
- 적은 색상 (48-128)
- 중복 프레임 제거

---

## 웹 및 소프트웨어 개발

### 11. web-artifacts-builder

**명칭**: Web Artifacts Builder  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
React, Tailwind CSS, shadcn/ui를 사용하여 정교한 멀티 컴포넌트 claude.ai HTML 아티팩트를 생성합니다. 복잡한 아티팩트에 적합합니다.

**트리거 조건**:
- 상태 관리가 필요한 복잡한 아티팩트
- 라우팅이 필요한 경우
- shadcn/ui 컴포넌트 사용
- 단순 단일 파일 HTML/JSX가 아닌 경우

**주요 기능**:
- React 18 + TypeScript + Vite
- Tailwind CSS 3.4.1 + shadcn/ui 테마 시스템
- 40개 이상의 shadcn/ui 컴포넌트 사전 설치
- 단일 HTML 파일로 번들링 (Parcel)

**생성 포맷**:
- `bundle.html` (자체 포함 HTML 아티팩트)

**워크플로우**:
1. `init-artifact.sh` 실행 (프로젝트 초기화)
2. 개발 (React 컴포넌트 편집)
3. `bundle-artifact.sh` 실행 (번들링)
4. 사용자와 아티팩트 공유
5. (선택) 테스트/시각화

**디자인 가이드라인**:
- ❌ 과도한 중앙 정렬, 보라색 그라디언트, 획일적인 둥근 모서리, Inter 폰트 회피
- ✅ "AI slop" 회피

---

### 12. frontend-design

**명칭**: Frontend Design  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
독특한 심미성을 가진 고품질 프로덕션급 프론트엔드 인터페이스를 생성합니다. 타이포그래피, 색상, 모션, 공간 구성에 집중합니다.

**트리거 조건**:
- 프론트엔드 UI/UX 디자인 및 구현
- 프로덕션급 인터페이스 필요
- 독특한 디자인 방향성 요구

**주요 기능**:
- 대담한 디자인 방향 선택 (tone, purpose, differentiation)
- 타이포그래피, 색상, 모션, 공간 구성 중심
- 일반적인 AI 디자인 회피
- 기능적이고 기억에 남는 코드

**생성 포맷**:
- HTML/CSS/JavaScript 프론트엔드 코드

**핵심 원칙**:
- 독특한 디자인 방향성
- 세심한 정제
- 프로덕션 품질

---

### 13. webapp-testing

**명칭**: Web Application Testing  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
Playwright를 사용하여 로컬 웹 애플리케이션과 상호작용하고 테스트하는 도구입니다. 프론트엔드 기능 검증, UI 동작 디버깅, 스크린샷 캡처 및 브라우저 로그 확인을 지원합니다.

**트리거 조건**:
- 웹 애플리케이션 자동화 테스트
- UI 동작 검증
- 브라우저 스크린샷 필요
- 프론트엔드 디버깅

**주요 기능**:
- Playwright 기반 자동화 스크립트
- 서버 라이프사이클 관리 (`with_server.py`)
- 정찰 후 액션 패턴 (Reconnaissance-then-Action)
- 스크린샷 및 DOM 검사

**생성 포맷**:
- Python Playwright 스크립트
- 스크린샷 이미지 (`.png`)

**주요 도구**:
- `scripts/with_server.py` (서버 관리)
- Playwright (브라우저 자동화)

**베스트 프랙티스**:
- 번들 스크립트를 블랙박스로 사용
- `sync_playwright()` 사용
- 동적 앱에서 `networkidle` 대기

---

### 14. mcp-builder

**명칭**: MCP Builder  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
외부 서비스와 LLM 통합을 위한 MCP(Model Context Protocol) 서버를 생성합니다. 연구/계획부터 구현, 테스트까지 4단계 프로세스를 제공합니다.

**트리거 조건**:
- MCP 서버 생성 필요
- 외부 도구/서비스 LLM 통합
- API 래퍼 개발

**주요 기능**:
- **Phase 1: Research & Planning** - MCP 디자인, 프로토콜 문서, 프레임워크 문서
- **Phase 2: Implementation** - 프로젝트 설정, 스키마가 있는 도구 생성
- **Phase 3: Review & Testing** - 코드 품질, 빌드/테스트
- **Phase 4: Evaluation** - 테스트 질문 및 XML 출력 생성

**생성 포맷**:
- TypeScript MCP 서버 프로젝트
- 테스트 스크립트
- 평가 XML

**권장 기술 스택**:
- TypeScript (권장)
- MCP SDK
- 구현 가이드 참조

---

## 전문 지원 및 커뮤니케이션

### 15. skill-creator

**명칭**: Skill Creator  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
효과적인 스킬을 생성하기 위한 가이드입니다. 새 스킬을 만들거나 기존 스킬을 업데이트할 때 사용합니다.

**트리거 조건**:
- 새 스킬 생성 요청
- 기존 스킬 업데이트
- Claude 기능 확장

**주요 기능**:
- 6단계 스킬 생성 프로세스
  1. 구체적인 예시로 스킬 이해
  2. 재사용 가능한 스킬 콘텐츠 계획
  3. 스킬 초기화 (`init_skill.py`)
  4. 스킬 편집 (리소스 구현 및 SKILL.md 작성)
  5. 스킬 패키징 (`package_skill.py`)
  6. 실제 사용을 통한 반복 개선
- Progressive Disclosure 디자인 원칙
- 스크립트, 참조, 에셋 번들링

**생성 포맷**:
- `.skill` 파일 (배포용 패키지)
- `SKILL.md` (스킬 정의)
- `scripts/`, `references/`, `assets/` 디렉토리

**핵심 원칙**:
- 간결함이 핵심 (컨텍스트 윈도우는 공공재)
- 적절한 자유도 설정
- Progressive Disclosure (3단계 로딩)

**스킬 구조**:
```
skill-name/
├── SKILL.md (필수)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (선택)
    ├── scripts/
    ├── references/
    └── assets/
```

---

### 16. internal-comms

**명칭**: Internal Communications  
**라이선스**: Complete terms in LICENSE.txt

**설명**:  
상태 보고서, 뉴스레터, 장애 보고서 등 다양한 유형의 내부 커뮤니케이션 작성을 위한 리소스를 제공합니다.

**트리거 조건**:
- 내부 커뮤니케이션 문서 작성
- 상태 보고서, 뉴스레터, 장애 보고서 등

**주요 기능**:
- 커뮤니케이션 유형 식별
- `examples/` 디렉토리에서 적절한 가이드라인 로드
- 형식, 톤, 콘텐츠 수집 가이드

**생성 포맷**:
- 내부 커뮤니케이션 문서 (형식은 유형에 따라 다름)

**지원 문서 유형**:
- 상태 보고서
- 뉴스레터
- 장애 보고서
- 기타 내부 커뮤니케이션

---

## 📊 스킬 통계

| 범주 | 스킬 수 |
|------|---------|
| 문서 및 데이터 처리 | 5 |
| 디자인 및 시각 예술 | 5 |
| 웹 및 소프트웨어 개발 | 4 |
| 전문 지원 및 커뮤니케이션 | 2 |
| **총계** | **16** |

---

## 🔍 스킬 선택 가이드

### 문서 작업이 필요한 경우
- **Word 문서**: `docx`
- **PDF**: `pdf`
- **프레젠테이션**: `pptx`
- **스프레드시트**: `xlsx`
- **긴 형식 협업 문서**: `doc-coauthoring`

### 디자인 작업이 필요한 경우
- **제너레이티브 아트**: `algorithmic-art`
- **시각 디자인**: `canvas-design`
- **브랜딩**: `brand-guidelines`
- **테마 적용**: `theme-factory`
- **Slack GIF**: `slack-gif-creator`

### 웹 개발이 필요한 경우
- **복잡한 React 아티팩트**: `web-artifacts-builder`
- **프론트엔드 UI**: `frontend-design`
- **웹 앱 테스트**: `webapp-testing`
- **MCP 서버**: `mcp-builder`

### 시스템 확장이 필요한 경우
- **새 스킬 생성**: `skill-creator`
- **내부 문서**: `internal-comms`

---

## 📝 사용 방법

각 스킬을 사용하려면:

1. **스킬 디렉토리 확인**: `skills/[skill-name]/`
2. **SKILL.md 읽기**: 상세 지침 확인
3. **필요한 도구 설치**: 각 스킬의 Dependencies 섹션 참조
4. **워크플로우 따르기**: SKILL.md에 명시된 단계별 프로세스 실행

---

## 🔗 관련 문서

- [README.md](README.md) - 저장소 개요
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) - 라이선스 정보
- 각 스킬의 `SKILL.md` - 상세 사용 지침

---

**Note**: 이 카탈로그는 자동 생성되지 않습니다. 새 스킬 추가 시 수동으로 업데이트해야 합니다.
