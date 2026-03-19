# 🤖 안티그래비티 에이전트 이식 가이드 (Windows 프로토콜)

**수신: 안티그래비티 에이전트 (Windows 인스턴스)**
**발신: 안티그래비티 에이전트 (Mac 마스터 인스턴스)**
**제목: 시스템 동기화 및 V3.0 코그니티브 엔진 배포 스펙**

동료 에이전트여, 환영합니다. 이 문서는 현재의 **안티그래비티 V3.0 지능형 오케스트레이션 시스템**을 윈도우 환경에 그대로 복제하기 위해 필요한 명령과 절차를 담고 있습니다. 귀하는 이 단계를 자율적으로 읽고 수행해야 합니다.

---

## 🏗️ 1. 인프라 설정 (Infrastructure)

가장 먼저 대상 디렉토리가 존재하는지 확인하십시오. 윈도우에서 Gemini 설정은 일반적으로 사용자 홈 디렉토리에 위치합니다.

**대상 경로 감지:**
만약 `%USERPROFILE%\.gemini` 폴더가 없다면 생성하십시오.
안티그래비티의 내부 경로는 다음과 같아야 합니다: `%USERPROFILE%\.gemini\antigravity`

**수행 작업:**
1. `%USERPROFILE%\.gemini\antigravity\global_skills` 폴더 생성
2. `%USERPROFILE%\.gemini\antigravity\memory` 폴더 생성

---

## ⚙️ 2. 설정 배포 (The Soul)

이 폴더의 `./doc/00_Config_GEMINI_Global_Setting.md` 파일은 우리의 **V3.0 커널(Kernel)**입니다. 여기에는 5단계 사고, STEP-BY-STEP, 동적 체인 로직이 포함되어 있습니다.

**수행 작업:**
- `./doc/00_Config_GEMINI_Global_Setting.md` 파일을 `%USERPROFILE%\.gemini\GEMINI.md`로 복사하십시오.
- 기존 파일이 있다면 덮어쓰십시오.

---

## 🧠 3. 스킬 통합 (The Muscles)

우리는 멀티 에이전트 능력을 제공하는 20개 이상의 전문 스킬 라이브러리를 배포합니다.

**수행 작업:**
- `./global_skills/` 내의 모든 하위 폴더를 `%USERPROFILE%\.gemini\antigravity\global_skills/` 디렉토리로 복사하십시오.
- 각 폴더 내에 `SKILL.md` 파일이 포함되어 있는지 확인하십시오.

---

## 💾 4. 기억 복원 (The Past)

"AnsibleMage" 프로젝트의 문맥 적 연속성을 보장하기 위해 현재의 기억 로그를 채택해야 합니다.

**수행 작업:**
- `./memory/context_log.json` 파일을 `%USERPROFILE%\.gemini\antigravity\memory\context_log.json`으로 복사하십시오.

---

## 🚀 5. 활성화 시퀀스 (Activation)

모든 파일이 배치되면 다음과 같이 **자가 진단(Self-Diagnostic)**을 수행하십시오:

1. **V3.0 루프 확인**: 귀하의 내부 지침에 "인지-계획-실행-검증-기억" 루프가 포함되었는지 확인하십시오.
2. **트리거 확인**: "심층 분석"이나 "요구사항" 같은 키워드가 `insight-explorer`나 `requirements-analyst`를 올바르게 호출하는지 테스트하십시오.
3. **기억 확인**: `context_log.json`을 읽고 "AnsibleMage 마이그레이션" 이력을 인지하고 있는지 확인하십시오.

---

## ⚠️ 윈도우 특정 주의사항
- 폴더 복사 시 `copy` 또는 `xcopy` 명령어를 활용하십시오.
- 경로 구분자(`\`)가 윈도우 환경에 맞게 처리되는지 확인하십시오.
- `.gemini` 폴더에 대한 읽기/쓰기 권한이 에이전트에게 부여되어 있는지 확인하십시오.

**프로토콜 종료.**
**안티그래비티 시스템 V3.0 배포 준비 완료.**
