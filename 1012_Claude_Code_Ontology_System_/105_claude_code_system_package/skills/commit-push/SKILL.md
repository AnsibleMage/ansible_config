---
name: commit-push
description: Stage, commit with Conventional Commit format, and push the current branch to origin.
user-invocable: true
allowed-tools: [Bash]
---

현재 변경사항을 확인하고 커밋 후 푸시해주세요.

1. `git status`로 변경사항 확인
2. 변경된 파일들을 스테이징 (`git add`)
3. Conventional Commit 형식으로 커밋 메시지 작성
4. `git push origin [현재브랜치]`로 푸시
5. 결과 보고

커밋 메시지 형식:
- feat: 새 기능
- fix: 버그 수정
- docs: 문서 변경
- refactor: 리팩토링
- chore: 기타 변경

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com> 포함
