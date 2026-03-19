# Claude Code Usage Strategy Template

> 이 템플릿은 프로젝트 특성에 맞는 Claude Code 사용전략 문서를 생성할 때 사용한다.
> 각 섹션의 `{{placeholder}}`를 프로젝트 분석 결과로 대체한다.

---

## Document Structure (12 Sections)

### Section 1: Project Characteristics → Claude Code Mapping

#### 1-1. Task Type Classification Table

| 작업 유형 | 해당 작업 | 특성 | 최적 도구 |
|----------|----------|------|----------|
| {{task_type}} | {{tasks}} | {{characteristics}} | {{optimal_tool}} |

Classification guide:
- 순차+단순 → Bash 직접 실행 (체인 생략)
- 순차+핵심 → **DevChain**
- 독립 병렬 → **Agent Teams** or **WebDevChain+**
- 긴급 → **HotfixChain**
- 문서 생성 → **DocChain+**
- 조사/분석 → **ResearchChain**
- 설계/아키텍처 → **SystemDesignChain**
- 심층 사고 → **MetaThinkChain**

#### 1-2. Dependency Map (ASCII)

```
[작업A]
   │
   ▼
┌──┴──┐
│     │
▼     ▼
[B]  [C]     ← ★ 병렬 가능
│     │
└──┬──┘
   │
   ▼
  [D]        ← 순차
```

Identify parallel points: find independent tasks that can run simultaneously.

---

### Section 2: Chain Selection Strategy

#### 2-1. Phase-Chain Mapping Table

| 단계 | 체인 | 프롬프트 패턴 | 핵심 에이전트 |
|------|------|-------------|-------------|
| {{phase}} | {{chain}} | {{prompt_pattern}} | {{key_agents}} |

#### 2-2. Trigger Keywords per Chain

Chain-keyword mapping from CLAUDE.md Section 2.4:
- **DevChain**: "개발", "TDD", "함수 구현", "코딩", "테스트 작성"
- **WebDevChain+**: "UI", "프론트엔드", "컴포넌트", "shadcn", "디자인"
- **HotfixChain**: "긴급", "버그 수정", "핫픽스", "오류"
- **ResearchChain**: "조사", "분석", "연구", "비교"
- **DocChain+**: "문서 작성", "Word", "docx"
- **SystemDesignChain**: "설계", "아키텍처", "체인 개선"
- **MetaThinkChain**: "왜", "What-if", "심층 분석"
- **GameDevChain**: "게임", "Roblox"
- **RailsDevChain**: "Rails", "레일즈", "Kamal"
- **AutomationChain**: "Hook", "MCP", "스크립트"

#### 2-3. Intentional Prompt Examples

```
❌ vague: "만들어줘"
✅ precise: "[구체적 대상]을 [방법]으로 [체인트리거키워드]. [참고문서] 참고"
```

---

### Section 3: Subagent Strategy

#### 3-1. Agent Usage Timing Table

| 에이전트 | 모델 | 사용 시점 | 비용/속도 |
|---------|------|----------|----------|
| `requirements_analyst` | **O** | Phase 시작 시 요구사항 | 비용↑ 정확↑ |
| `system_architect` | **O** | 구조/아키텍처 설계 | 비용↑ 정확↑ |
| `code_developer` | S | 실제 코드 작성 | 비용↓ 빠름 |
| `quality_reviewer` | S | 코드 리뷰 | 비용↓ 빠름 |
| `Explore` | S | 코드베이스 탐색 | 비용↓ 빠름 |
| `Plan` | **O** | 복잡한 구현 계획 | 비용↑ 정확↑ |

Rule: Opus = design/analysis only, Sonnet = repetitive coding

#### 3-2. Subagent vs Direct Decision

| 상황 | 선택 | 이유 |
|------|------|------|
| 단일 파일 수정 | 직접 | 오버헤드 과다 |
| 3+ 파일 동시 수정 | 서브에이전트 | 컨텍스트 분리 |
| 복잡한 로직 검토 | Plan[O] | 깊은 사고 |
| 간단한 파일 검색 | Glob/Grep | Explore 불필요 |
| 대규모 탐색 | Explore[S] | 다회 검색 |

---

### Section 4: Agent Teams Strategy

#### 4-1. Teams-Suitable Sections

Identify 2-3 parallelization points from the dependency map.

Team template:
```
┌─ Team: {{team_name}} ──────────────────────────┐
│  Lead (메인 세션)                                │
│  ├─ Teammate 1: "{{name}}" ({{agent_type}})     │
│  │   → {{tasks}}                                │
│  └─ Teammate 2: "{{name}}" ({{agent_type}})     │
│      → {{tasks}}                                │
│  Lead: {{lead_tasks}}                           │
└─────────────────────────────────────────────────┘
```

#### 4-2. Teams Rules

| 규칙 | 적용 |
|------|------|
| 메모리 저장은 Lead만 | Teammate memory/ 접근 금지 |
| 착수 보고 30초 내 | spawn 후 무응답 → 120초 후 shutdown |
| 파일 충돌 방지 | Teammate별 작업 폴더 분리 |
| 동일 파일 동시 수정 금지 | Lead가 TaskCreate로 할당 |

#### 4-3. Teams NOT Suitable

- 순차 의존 작업
- 단일 명령어 작업
- 긴급 버그 수정 (HotfixChain 더 빠름)

---

### Section 5: Skill Usage Strategy

Map applicable skills to development phases:

| 스킬 | 사용 시점 | 프롬프트 패턴 |
|------|----------|-------------|
| `/frontend-design` | UI 개발 | "컴포넌트를 개발해줘" |
| `/web-artifacts-builder` | React 컴포넌트 | "shadcn으로 만들어줘" |
| `/theme-factory` | 테마 구축 | "테마를 만들어줘" |
| `/webapp-testing` | E2E 테스트 | "Playwright로 테스트" |
| `/commit-push` | 커밋 | `/commit-push` |
| `/project-review` | Phase 완료 리뷰 | "프로젝트 리뷰해줘" |
| `/docx` | 문서 생성 | "Word 문서 만들어줘" |

Skill combination patterns:
- UI cycle: `/theme-factory` → `/frontend-design` → `/webapp-testing` → `/commit-push`
- Code cycle: `[code_developer]` → `/project-review` → `/commit-push`
- Hotfix cycle: `HotfixChain` → `/webapp-testing` → `/commit-push`

---

### Section 6: Slash Command Strategy

| 커맨드 | 시점 | 빈도 |
|--------|------|------|
| `/commit-push` | 기능 단위 완성 | 매우 자주 |
| `/project-review` | Phase 완료 | Phase당 1회 |
| `/pr-review` | merge 전 | Phase당 1회 |
| `/memory-save` | 세션 종료 전 | 매 세션 |
| `/analyze` | 프롬프트 디버그 | 필요시 |
| `/readme-gen` | 배포 전 | 1회 |

---

### Section 7: Hook Utilization Strategy

| Hook | 역할 | 프로젝트 효과 |
|------|------|------------|
| **UserPromptSubmit** | 4-Layer 분석 → 체인 추천 | 자동 도구 추천 |
| **PreToolUse:Write** | .env/.secret 보호 | 보안 |
| **PostToolUse:Write** | Prettier 자동 포매팅 | 코드 일관성 |
| **PostToolUse** | Git 상태 표시 | 변경 추적 |

---

### Section 8: Prompt Design Strategy

#### Template Structure
```
[작업 목표] + [참고 문서] + [구체적 범위] + [검증 방법]
```

Include phase-specific prompt templates.

---

### Section 9: Session Management Strategy

#### Session Split Criteria

| 세션 | 작업 범위 | 예상 프롬프트 |
|------|----------|-------------|
| {{session_n}} | {{scope}} | {{prompt_count}} |

#### Start/End Protocol
- Start: Hook 자동 메모리 저장 → MEMORY.md 확인 → 이전 세션 이어서
- End: `/memory-save` → 응답 완료 프로토콜

---

### Section 10: Development Order Roadmap

Phase-by-phase with dependency annotations:
- Phase 0: 초기화
- Phase N: 각 개발 단계 (병렬 가능 여부 표시)
- Final: 통합/배포

---

### Section 11: Cost/Speed Optimization

| 전략 | 효과 |
|------|------|
| Opus=설계, Sonnet=코딩 | 비용 60%↓ |
| 독립 작업 Teams 병렬 | 시간 40~50%↓ |
| 문서 참조로 프롬프트 축소 | 토큰 절약 |
| PostToolUse Prettier | 포매팅 프롬프트 불필요 |
| `/commit-push` 자동화 | 수동 git 제거 |

---

### Section 12: Pre-Prompt Checklist

```
□ 단순한가? → 체인 생략
□ 복잡한가? → 체인 키워드 포함
□ 병렬 가능 2+ 작업? → Teams 또는 "병렬로"
□ 참고 문서 있는가? → 문서명 명시
□ 테스트 필요? → "TDD", "테스트 포함"
□ 커밋 필요? → /commit-push
□ 세션 마지막? → /memory-save
```
