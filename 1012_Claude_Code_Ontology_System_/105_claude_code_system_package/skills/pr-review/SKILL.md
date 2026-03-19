---
name: pr-review
description: Review a PR or git diff and write a structured report to .pr-reviews/ folder.
user-invocable: true
allowed-tools: [Bash, Read, Grep]
---

Git 변경사항을 리뷰하고 `.pr-reviews/` 폴더에 기록해주세요.

## 리뷰 대상
$ARGUMENTS (PR 번호, 브랜치명, 또는 현재 변경사항)

## 수행 작업
1. `.pr-reviews/` 폴더 존재 확인 (없으면 생성)
2. `git diff` 또는 PR 정보 조회
3. 변경사항(diff) 분석:
   - 문법/구문 오류
   - 잠재적 버그
   - 보안 취약점
   - 불필요한 파일
4. `.pr-reviews/PR-[번호]_[브랜치]_[날짜].md` 생성
5. 결과 보고: 승인/수정요청/반려

## 체크리스트
- [ ] 문법/구문 오류 없음
- [ ] 잠재적 버그 없음
- [ ] 보안 취약점 없음
- [ ] 불필요한 파일 미포함
- [ ] 코드 스타일 준수
