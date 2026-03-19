---
name: analyze
description: Run 4-Layer prompt analysis via prompt_analyzer.py and execute the recommended chain or skill.
user-invocable: true
allowed-tools: [Bash]
---

다음 프롬프트를 4-Layer 분석하고 최적의 에이전트/스킬/체인을 추천해주세요.

## 분석 대상
$ARGUMENTS (분석할 프롬프트)

## 분석 도구
```bash
python3 ~/.claude/scripts/prompt_analyzer.py "$ARGUMENTS"
```

## 수행 작업
1. Python 분석기 실행
2. 분석 결과 출력 (어휘/통사/담화/화용)
3. 추천된 스킬/에이전트/체인 표시
4. **추천에 따라 해당 도구 실행**

## 중요
- 이 커맨드는 모든 복잡한 요청 전에 사용 권장
- 분석 결과의 HIGH 우선순위 항목은 반드시 따를 것
- 번역 의도 감지 시 `/translation-specialist` 사용 필수
