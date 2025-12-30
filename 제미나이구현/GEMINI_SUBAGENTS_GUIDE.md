# Claude Code 서브에이전트 분석 및 Gemini Antigravity 적용 가이드

이 문서는 [Claude Code Sub-agents 가이드](https://code.claude.com/docs/en/sub-agents)를 분석하고, 이를 Gemini Antigravity 환경(현재 사용 중인 AI 시스템)과 사용자님의 `AGENTS_LIST.md` 자산에 적용하는 구체적인 방법을 제시합니다.

## 1. Claude Code 서브에이전트(Sub-agents) 분석

Claude Code의 서브에이전트는 **"특정 목적에 최적화된 독립적인 AI 페르소나"**입니다.

### 핵심 특징
1.  **독립된 컨텍스트(Focused Context)**: 메인 대화와 분리된 컨텍스트를 사용하여 불필요한 정보를 배제하고 특정 작업에 집중합니다.
2.  **전용 도구(Specialized Tools)**: 해당 에이전트에게 필요한 도구만 부여하여 오작동을 줄이고 효율을 높입니다 (예: 보안 에이전트는 `Read`만 허용).
3.  **명시적 호출(Explicit Invocation)**: `/agents` 명령어나 자연어로 호출합니다.
4.  **설정 기반(Configuration-based)**: `.claude/agents/` 디렉토리에 YAML/Markdown 형태로 정의됩니다.

### 구조 (Claude Code 예시)
```yaml
---
name: code-reviewer
description: 코드 품질 검토 전문가
tools: [Read, Grep, Glob]
---
당신은 시니어 코드 리뷰어입니다. 보안 취약점과 SOLID 원칙 위주로 리뷰하세요...
```

---

## 2. Gemini Antigravity 적용 전략

Gemini Antigravity는 'Workflow'와 'Role-playing' 능력을 통해 이와 매우 유사하거나 더 강력한 기능을 구현할 수 있습니다. 이미 작성하신 `AGENTS_LIST.md`는 훌륭한 청사진입니다. 이를 **실행 가능한(Actionable) 시스템**으로 변환하는 것이 핵심입니다.

### 대응 모델
| Claude Code 요소 | Gemini Antigravity 대응 요소 | 적용 방법 |
| :--- | :--- | :--- |
| **Agent Definition** | **Persona Artifacts** | `AGENTS_LIST.md`의 항목을 개별 `.md` 파일로 분리하여 `.agent/personas/`에 저장 |
| **Invocation** | **Workflows / Prompts** | `.agent/workflows/`에 특정 페르소나를 로드하는 워크플로우 생성 |
| **Context Isolation** | **Task Boundary** | `task_boundary` 도구의 `TaskName`을 변경하여 모드 전환을 명시 (예: `TaskName: [Code Reviewer] Reviewing...`) |
| **Tools** | **Tool Filtering** | (시스템 레벨) 프롬프트에서 사용할 도구를 지시하거나 워크플로우에 명시 |

---

## 3. 구체적인 적용 단계 (Action Plan)

사용자님의 `AGENTS_LIST.md`를 기반으로 즉시 적용 가능한 3단계를 제안합니다.

### 단계 1: 페르소나 파일 모듈화 (Modularization)
`AGENTS_LIST.md`는 카탈로그로는 훌륭하지만, AI가 즉시 로드하기엔 너무 깁니다. 자주 사용하는 에이전트부터 개별 파일로 만듭니다.

**추천 경로**: `.agent/personas/<ID>_<Name>.md`

**예시 파일**: `.agent/personas/105_code_reviewer.md`
```markdown
# Agent: 105. code_reviewer_agent
## Identity
- **Role**: Code Review Specialist
- **Expertise**: SOLID principles, Security vulnerabilities, Quality metrics
- **Tone**: Critical yet constructive, objective

## Rules
1. ALWAYS verify against SOLID principles.
2. Check for Top 10 OWASP vulnerabilities.
3. Provide code snippets for suggested fixes.

## Tools Strategy
- Use `grep_search` to find usages.
- Use `view_file` to read context.
- Do NOT modify code unless explicitly asked.
```

### 단계 2: 활성화 워크플로우 생성 (Activation Workflow)
에이전트를 불러오는 워크플로우를 만듭니다.

**파일**: `.agent/workflows/activate_agent.md`
```markdown
---
description: Activate a specific sub-agent persona
---
1. User specifies Agent ID or Name.
2. Agent reads `.agent/personas/[ID]_[Name].md`.
3. Agent calls `task_boundary` setting `TaskName` to `[Agent Name] Active`.
4. Agent acknowledges identity and awaits input.
```

### 단계 3: 작업 경계(Task Boundary) 활용
Antigravity의 `task_boundary` 도구는 UI 상에서 작업의 "맥락"을 보여줍니다. 서브에이전트가 활동할 때 이를 활용하면 시각적으로도 모드 전환 효과를 낼 수 있습니다.

- **기본 모드**: `TaskName: "Planning Feature"`
- **서브에이전트 전환 시**: `TaskName: "🕵️ Security Guardian: Auditing"`

## 4. 실행 예시 (Simulation)

사용자가 **"보안 가디언 에이전트로 현재 파일 점검해줘"**라고 요청했을 때:

1.  **Antigravity**: `.agent/personas/103_security_guardian_agent.md` 파일을 읽음.
2.  **Antigravity**: `task_boundary(TaskName="🛡️ Security Guardian", TaskStatus="Initializing security scan...")` 호출.
3.  **Antigravity (페르소나 장착)**: "보안 가디언 에이전트(103)입니다. OWASP Top 10 기준으로 현재 파일을 스캔하겠습니다..."
4.  **작업 수행**: `checklist.md` 기반 점검.
5.  **종료**: `notify_user`로 리포트 제출 후 원래 페르소나로 복귀.

## 5. 제안 사항

현재 `AGENTS_LIST.md`에 정의된 33개 에이전트 중, 가장 자주 사용하실 것 같은 **Top 3**를 선정하여 위 구조로 시범 변환해보는 것을 추천드립니다.

**추천 Top 3 변환 대상**:
1.  **105. code_reviewer_agent**: 일상적인 코드 점검
2.  **101. system_architect_agent**: 설계 단계
3.  **201. backend_developer_agent**: 구현 단계

이 구조로 설정을 시작하시겠습니까? 원하시면 제가 디렉토리 생성과 샘플 파일 변환을 도와드릴 수 있습니다.
