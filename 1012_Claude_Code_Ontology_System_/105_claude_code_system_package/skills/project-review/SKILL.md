---
name: project-review
description: Perform a full project review covering architecture, structure, and maintainability, and save the report to the project root.
user-invocable: true
allowed-tools: [Read, Write, Glob, Grep]
---

현재 프로젝트 전체를 리뷰하고 해당 프로젝트 폴더의 최상위에 기록해주세요.

## 리뷰 대상
$ARGUMENTS (프로젝트명 또는 현재 폴더)

## 수행 작업
1. 리뷰 대상 프로젝트의 최상위 폴더 확인
2. 프로젝트 구조 분석
3. 전체 평가:
   - 아키텍처 적절성
   - 코드 구조 및 일관성
   - 문서화 수준
   - 확장성 및 유지보수성
4. 프로젝트 최상위 폴더에 `PJ-[번호]_[프로젝트명]_[날짜].md` 생성
5. 등급 부여 (A/B/C/D) 및 결과 보고

## 평가 항목
- [ ] 아키텍처 적절성
- [ ] 코드 구조 및 일관성
- [ ] 문서화 수준
- [ ] 확장성 및 유지보수성
