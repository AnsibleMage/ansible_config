# 📦 Legacy Templates (구버전 템플릿)

**작성일:** 2025-11-07
**상태:** 🔴 Deprecated (사용 중단)

---

## ⚠️ 주의사항

이 폴더의 템플릿들은 **구버전 (3-문서 시스템)**입니다.

**신버전 사용 권장:** 상위 폴더의 4-Layer 템플릿을 사용하세요.
- `Product_PRD_템플릿.md`
- `Block_템플릿.md`
- `Feature_템플릿.md`
- `Task_템플릿.md`

---

## 📄 이 폴더의 파일들

### 1. PRD_템플릿.md
- **대체:** `Product_PRD_템플릿.md`
- **차이:** 계층 구조 없음, E2E Test Plan 없음
- **보존 이유:** 기존 프로젝트 호환성

### 2. DesignDoc_템플릿.md
- **대체:** `Block_템플릿.md` + `Feature_템플릿.md`
- **차이:** 설계가 각 레벨 템플릿에 통합됨
- **보존 이유:** ADR 별도 문서 선호 시 참고

### 3. ImplementationTracker_템플릿.md
- **대체:** `Feature_템플릿.md`의 일일 진행 섹션
- **차이:** Feature별 추적 vs 프로젝트 전체 대시보드
- **보존 이유:** 팀 규모 3명 이상 시 통합 대시보드 필요 시 참고

---

## 🆚 구버전 vs 신버전 비교

| 항목 | 구버전 (3-문서) | 신버전 (4-Layer) |
|------|----------------|-----------------|
| 템플릿 수 | 3개 | 4개 |
| 구조 | 평면적 | 계층적 (프랙탈) |
| TDD 레벨 | Task만 | 모든 레벨 (E2E, Module, Integration, Unit) |
| 1 제품 구조 | 불명확 | 3 블럭 = 9 중단위 = 45 작은단위 |
| 1인 개발 적합성 | 문서 부담 | 최적화 ✅ |

---

## 💡 마이그레이션 가이드

기존 프로젝트를 신버전으로 전환하려면:

### Step 1: PRD 변환
```bash
# 구버전
PRD_템플릿.md

# 신버전
Product_PRD_템플릿.md
└─ 추가: 계층 구조 섹션 (3 Blocks → 9 Features → 45 Tasks)
└─ 추가: E2E Test Plan 섹션
```

### Step 2: DesignDoc 분할
```bash
# 구버전
DesignDoc_템플릿.md (1개 파일)
├─ Architecture
├─ Solution Exploration
└─ Test Strategy

# 신버전 (계층별 분산)
Block_템플릿.md (3개)
├─ Architecture (SOLID, DI)
└─ Module Test

Feature_템플릿.md (9개)
├─ 5단계 프로세스 (Explore, Select)
└─ Integration Test
```

### Step 3: Tracker 통합
```bash
# 구버전
ImplementationTracker_템플릿.md (1개 통합 문서)
└─ 전체 프로젝트 진행 추적

# 신버전 (Feature별 분산)
Feature_템플릿.md (각 Feature마다)
└─ Day 1~5 일일 진행 추적
```

---

## 📅 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| **v1.0** | 2025-11-07 이전 | 3-문서 시스템 (PRD, DesignDoc, Tracker) |
| **v2.0** | 2025-11-07 | 4-Layer 프랙탈 TDD 시스템 (Product, Block, Feature, Task) |

---

## 🔗 관련 문서

- [[../Product_PRD_템플릿|Product PRD 템플릿]] - 신버전 Layer 0
- [[../Block_템플릿|Block 템플릿]] - 신버전 Layer 1
- [[../Feature_템플릿|Feature 템플릿]] - 신버전 Layer 2
- [[../Task_템플릿|Task 템플릿]] - 신버전 Layer 3
- [[../../CJ_AI_개발방법론|CJ_AI_개발방법론]] - 메인 문서
- [[../../계층적_TDD_가이드|계층적 TDD 가이드]] - 프랙탈 TDD 설명

---

**마지막 업데이트:** 2025-11-07
**담당자:** CJ (Claude Code + 개발자)
