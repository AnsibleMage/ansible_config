# Antigravity System V4.1 Evolution Report
> **Date**: 2026-01-29
> **System Version**: V4.1 (Integrated with Obsidian)
> **Key Feature**: Contextual Awareness & Permanent Memory Linking

---

## 1. System Overview (V4.1)

Antigravity V4.1은 기존의 "독립형 에이전트"에서 **"옵시디언(Obsidian)과 완전히 통합된 확장형 두뇌"**로 진화했습니다.
사용자 주도형 설정(Contextual Config)과 물리적 파일(Artifact)을 통한 기억 매커니즘이 핵심입니다.

### 🌟 Key Changes
1.  **Physical Integration**: 안티그래비티의 작업 로그(`brain`)를 옵시디언 볼트 내 `00_Antigravity_Brain`으로 심볼릭 연결.
2.  **Contextual Integration**: 설정 파일(`GEMINI.md`)과 프로젝트 규칙(`projects`)을 옵시디언에서 직접 제어.
3.  **Memory Architecture**: 'Log(과거) + Artifact(현재) + Context(미래/규칙)'의 3단 기억 구조 확립.

---

## 2. Integration Architecture

### A. Windows (Current Setup)
| Component | System Path | Obsidian Path | Link Type |
| :--- | :--- | :--- | :--- |
| **Brain** (Log) | `.gemini\antigravity\brain` | `Vault\00_Antigravity_Brain` | **Junction** (`mklink /J`) |
| **Config** (Rule) | `.gemini\GEMINI.md` | `Vault\...\Config\GEMINI.md` | **Hardlink** (`mklink /H`) |
| **Projects** (Context) | `.gemini\antigravity\projects` | `Vault\...\Projects` | **Junction** (`mklink /J`) |

### B. New Capabilities
- **실시간 모니터링**: 에이전트가 생각하는 과정(`task.md`)을 옵시디언에서 실시간 시청.
- **룰 핫스왑 (Hot-Swap)**: 옵시디언에서 `GEMINI.md`를 수정하면, 에이전트의 성격이 즉시 변경됨.
- **프로젝트 컨텍스트**: `Projects/[Name]/rules.md`만 작성하면, 별도 프롬프트 없이도 규칙 자동 적용.

---

## 3. Trouble Shooting Log

### 🗑️ Reserved File Deletion (`nul`)
- **문제**: Windows 예약어(`nul`, `con` 등)로 된 파일은 일반 삭제 불가.
- **해결**: UNC Path (`\\?\C:\Path\nul`) 및 `cmd.exe`를 사용하여 커널 레벨에서 우회 삭제.
- **의의**: 에이전트가 OS의 한계를 이해하고 전문적인 스킬(`complexity-resolver`)을 사용하여 해결함.

### 🧠 Memory Persistence Analysis
- **질문**: 왜 안티그래비티는 기억이 초기화되지 않는가?
- **분석**:
    1.  **Session UUID**: 대화 식별자가 바뀌지 않는 한, 이전 대화 로그를 로드함.
    2.  **Artifact Persistence**: 눈에 보이는 파일(`task.md`)이 디스크에 남아있어, 작업 상태(State)가 영구 보존됨.
    3.  **Visual Anchor**: 옵시디언에 연동된 폴더 자체가 사용자와 에이전트의 '공동 기억' 역할을 함.

---

## 4. Next Steps & Todo
- [ ] 집(MacBook) 환경에 동일한 통합 환경 구축 (별첨 가이드 참조)
- [ ] 프로젝트별 상세 규칙(`rules.md`) 작성하여 컨텍스트 실험
