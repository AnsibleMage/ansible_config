# CJ AI 개발방법론 2.0 개선 제안서

훌륭한 방법론이지만, **"실제 혼자서 매일 쓰기에는 조금 무거울 수 있다"**는 점과 **"AI와의 상호작용 효율성"** 측면에서 개선이 필요합니다.
특히, 사용자가 직접 CLI를 실행하거나 "Lite 모드"로 타협하는 것은 장기적으로 방법론의 붕괴를 초래할 수 있습니다.

따라서, **"사용자는 자연어로 지시하고, AI가 모든 규율을 준수하는"** 방향으로 개선을 제안합니다.

## 🚀 핵심 개선 제안 3가지

### 1. "Agent-Driven Automation Tools" (도구의 에이전트화)
**문제점**: "CLI 명령어를 외워서 치는 것"조차 마찰(Friction)입니다. 귀찮으면 안 하게 됩니다.
**해결책**: 스크립트는 존재하되, **사용자가 아니라 AI가 실행**하도록 설계합니다.
- **For Agent**: `scripts/create_block.ts` 같은 스크립트를 만들고, 제가(AI) 이 스크립트를 호출하는 **Tool**을 갖습니다.
- **User Experience**: 사용자는 자연어로 "사용자 관리 블록 만들어줘"라고만 하면 됩니다. 제가 알아서 스크립트를 실행해 구조를 잡습니다.
- **강제성**: 제가 작업을 시작할 때 이 스크립트 실행을 "필수 절차"로 인식하므로, 구조가 누락될 일이 없습니다.

### 2. "AI 전용 프롬프트 블록" 내장 (AI 최적화)
**문제점**: 템플릿은 사람이 읽기 좋게 되어 있지만, AI에게 일을 시킬 때는 다시 상황 설명을 해야 할 때가 있습니다.
**제안**: 모든 템플릿의 최상단에 **`<!-- AI_CONTEXT -->`** 섹션을 숨겨두거나 명시합니다.
- 이 섹션만 복사해서 AI에게 주면, AI가 즉시 "아, 나는 지금 Feature 1.2의 Task 3을 맡았구나"라고 인식하게 합니다.
- **Context-Injection**을 템플릿 레벨에서 설계합니다.

### 3. "Zero-Friction Full Mode" (AI 완전 자동화)
**문제점**: "Lite 모드"를 허용하면, 사람은 본능적으로 쉬운 길만 선택하게 되어 결국 방법론이 무너집니다. (Broken Window Theory)
**해결책**: **"타협 없는 Full Track"**을 유지하되, 그 부담을 **AI가 100% 흡수**합니다.
- **Shadow Documentation**: 코드를 수정하면 AI가 *반드시* 역으로 상위 문서(Task → Feature → Block)를 업데이트하도록 강제합니다.
- **Doc-First Enforcement**: "문서 없이는 코드 생성 거부" 원칙을 AI 프롬프트에 하드코딩합니다.
- **결과**: 사용자는 "빠르게" 일한다고 느끼지만, 결과물은 항상 "완벽한 문서"가 갖춰진 상태가 됩니다. **"빠른 것이 아니라, 매끄러운 것(Smooth)"**을 지향합니다.

---

## 🛠 구체적인 실행 계획 (Action Plan)

### Step 1: 템플릿 구조 개선 (AI Context 포함)
기존 템플릿에 **AI Context Block**을 추가하여 AI가 즉시 맥락을 파악할 수 있게 합니다.

```markdown
<!-- AI_CONTEXT
Project: Simple Todo
Level: Feature
Current Focus: Input Validation
Related Files: [Block_1.md, PRD.md]
-->
# Feature: 입력 검증
...
```

### Step 2: Agent 전용 도구(Scripts) 작성
AI가 사용할 자동화 스크립트를 `.agent/tools` 또는 `scripts/`에 배치합니다.
- `agent-create-structure.ts`: 사용자의 자연어 요청을 받아 폴더/파일 구조 생성
- `agent-update-tracker.ts`: 작업 완료 시 Task 문서 및 진행률 자동 업데이트

### Step 3: 시각화 (Dashboard)
사용자는 복잡한 문서 대신 직관적인 대시보드만 확인하면 됩니다.
- `task.md`를 대시보드 형태로 유지 관리하며, AI가 작업할 때마다 실시간으로 업데이트합니다.

---

## ⚖️ 결론
방법론의 타협(Lite 모드)은 없습니다. 대신 **AI가 모든 복잡성을 흡수**하여, 사용자는 **"Zero-Friction(무마찰)"**으로 **"Full Methodology(완전한 방법론)"**의 혜택을 누리게 됩니다.
이것이 진정한 **AI-Native 개발 방법론**입니다.
