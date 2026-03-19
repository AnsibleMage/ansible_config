#!/usr/bin/env python3
"""
Chain Usage Report Generator
일일 체인/에이전트/스킬 사용 패턴 분석 및 리포트 생성

Usage:
    python chain_report_generator.py [--date YYYY-MM-DD]

기본값: 오늘 날짜의 세션 분석
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Any

# 경로 설정
CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
REPORT_DIR = CLAUDE_DIR / "chainreport"

# 알려진 체인 패턴
KNOWN_CHAINS = [
    "SystemDesignChain", "AutomationChain", "GameDevChain", "DevChain",
    "ResearchChain", "DocChain+", "WebDevChain+",
    "MetaThinkChain", "RailsDevChain", "HotfixChain", "Direct"
]

# 알려진 에이전트
KNOWN_AGENTS = {
    # Cognitive Agents
    "insight_explorer": "sonnet",
    "multidimensional_analyst": "opus",
    "connection_creator": "opus",
    "problem_reframer": "opus",
    "solution_innovator": "opus",
    "insight_amplifier": "opus",
    "learning_evolver": "opus",
    "complexity_resolver": "opus",
    "balanced_judge": "opus",
    "integrated_sage": "opus",
    # Role Agents
    "requirements_analyst": "opus",
    "system_architect": "opus",
    "code_developer": "sonnet",
    "quality_reviewer": "sonnet",
    # Built-in Agents
    "Explore": "sonnet",
    "Plan": "opus",
    "general-purpose": "sonnet",
}

# 알려진 스킬
KNOWN_SKILLS = [
    "/translation-specialist", "/docx", "/pdf", "/pptx", "/xlsx",
    "/doc-coauthoring", "/frontend-design", "/web-artifacts-builder",
    "/webapp-testing", "/mcp-builder", "/algorithmic-art", "/brand-guidelines",
    "/canvas-design", "/theme-factory", "/slack-gif-creator",
    "/rails-init", "/rails-prd", "/rails-plan", "/rails-dev",
    "/rails-test", "/rails-deploy", "/rails-verify", "/analyze",
    "/commit-push", "/pr-review", "/project-review", "/memory-save", "/readme-gen"
]


def get_all_project_dirs() -> List[Path]:
    """모든 프로젝트 디렉토리 반환"""
    if not PROJECTS_DIR.exists():
        return []
    return [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]


def get_sessions_for_date(target_date: datetime) -> List[Dict[str, Any]]:
    """특정 날짜의 세션 목록 반환"""
    sessions = []
    target_date_str = target_date.strftime("%Y-%m-%d")

    for project_dir in get_all_project_dirs():
        index_file = project_dir / "sessions-index.json"
        if not index_file.exists():
            continue

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get('entries', []):
                # modified 또는 created 날짜 확인
                modified = entry.get('modified', '')
                created = entry.get('created', '')

                if target_date_str in modified or target_date_str in created:
                    jsonl_path = project_dir / f"{entry['sessionId']}.jsonl"
                    if jsonl_path.exists():
                        sessions.append({
                            'sessionId': entry['sessionId'],
                            'path': jsonl_path,
                            'summary': entry.get('summary', ''),
                            'firstPrompt': entry.get('firstPrompt', ''),
                            'messageCount': entry.get('messageCount', 0),
                            'modified': modified,
                            'projectPath': entry.get('projectPath', '')
                        })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading {index_file}: {e}", file=sys.stderr)
            continue

    return sessions


def parse_jsonl_file(jsonl_path: Path) -> List[Dict[str, Any]]:
    """JSONL 파일 파싱"""
    messages = []
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    messages.append(msg)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {jsonl_path}: {e}", file=sys.stderr)
    return messages


def extract_chain_usage(messages: List[Dict[str, Any]]) -> Counter:
    """메시지에서 체인 사용 추출"""
    chain_counter = Counter()

    # 체인 선언 패턴
    chain_patterns = [
        r"📋\s*체인\s*구성:\s*(\w+)",
        r"Chain:\s*(\w+)",
        r"\[Chain\]:\s*(\w+)",
        r"(\w+Chain)\s*실행",
    ]

    for msg in messages:
        if msg.get('type') != 'assistant':
            continue

        content = msg.get('message', {}).get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text = item.get('text', '')
                    for pattern in chain_patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        for match in matches:
                            # 알려진 체인인지 확인
                            for known in KNOWN_CHAINS:
                                if known.lower() in match.lower():
                                    chain_counter[known] += 1
                                    break
                            else:
                                if 'chain' in match.lower():
                                    chain_counter[match] += 1

    return chain_counter


def extract_agent_usage(messages: List[Dict[str, Any]]) -> Counter:
    """메시지에서 에이전트 사용 추출"""
    agent_counter = Counter()

    for msg in messages:
        if msg.get('type') != 'assistant':
            continue

        content = msg.get('message', {}).get('content', [])
        if isinstance(content, list):
            for item in content:
                # Tool use에서 Task 호출 확인
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_name = item.get('name', '')
                    if tool_name == 'Task':
                        input_data = item.get('input', {})
                        subagent = input_data.get('subagent_type', '')
                        if subagent:
                            agent_counter[subagent] += 1

                # 텍스트에서 에이전트 언급 확인
                if isinstance(item, dict) and item.get('type') == 'text':
                    text = item.get('text', '')
                    for agent_name in KNOWN_AGENTS.keys():
                        if agent_name in text:
                            # Task 호출 컨텍스트에서만 카운트
                            if f'subagent_type: "{agent_name}"' in text or f"subagent_type='{agent_name}'" in text:
                                agent_counter[agent_name] += 1

    return agent_counter


def extract_skill_usage(messages: List[Dict[str, Any]]) -> Counter:
    """메시지에서 스킬 사용 추출"""
    skill_counter = Counter()

    for msg in messages:
        # 사용자 메시지에서 스킬 호출 확인
        if msg.get('type') == 'user':
            user_msg = msg.get('message', {})
            if isinstance(user_msg, dict):
                content = user_msg.get('content', '')
                if isinstance(content, str):
                    for skill in KNOWN_SKILLS:
                        if skill in content:
                            skill_counter[skill] += 1

        # 어시스턴트 메시지에서 Skill 도구 호출 확인
        if msg.get('type') == 'assistant':
            content = msg.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        tool_name = item.get('name', '')
                        if tool_name == 'Skill':
                            input_data = item.get('input', {})
                            skill_name = input_data.get('skill', '')
                            if skill_name:
                                skill_counter[f"/{skill_name}"] += 1

    return skill_counter


def get_next_sequence_number(target_date: datetime) -> int:
    """해당 월의 다음 시퀀스 번호 반환"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    yymm = target_date.strftime("%y%m")
    pattern = f"{yymm}_*_daily_chain_report.md"

    existing = list(REPORT_DIR.glob(pattern))
    if not existing:
        return 1

    max_seq = 0
    for f in existing:
        match = re.match(rf"{yymm}_(\d+)_", f.name)
        if match:
            seq = int(match.group(1))
            max_seq = max(max_seq, seq)

    return max_seq + 1


def generate_report(
    target_date: datetime,
    sessions: List[Dict[str, Any]],
    chain_usage: Counter,
    agent_usage: Counter,
    skill_usage: Counter
) -> str:
    """마크다운 리포트 생성"""

    date_str = target_date.strftime("%Y-%m-%d")
    total_sessions = len(sessions)

    # 가장 많이 사용한 항목들
    top_chain = chain_usage.most_common(1)[0] if chain_usage else ("Direct", 0)
    top_agent = agent_usage.most_common(1)[0] if agent_usage else ("없음", 0)
    top_skill = skill_usage.most_common(1)[0] if skill_usage else ("없음", 0)

    # 총 사용 횟수
    total_chains = sum(chain_usage.values())
    total_agents = sum(agent_usage.values())
    total_skills = sum(skill_usage.values())

    report = f"""# 일일 Chain 사용 리포트

## 메타 정보
- **작성일**: {date_str}
- **분석 기간**: {date_str} (1일)
- **총 세션 수**: {total_sessions}개
- **요약**:
  - 가장 많이 사용한 체인: **{top_chain[0]}** ({top_chain[1]}회)
  - 가장 많이 사용한 에이전트: **{top_agent[0]}** ({top_agent[1]}회)
  - 가장 많이 사용한 스킬: **{top_skill[0]}** ({top_skill[1]}회)

---

## Chain 사용 통계

| 순위 | Chain | 사용 횟수 | 비율 |
|:----:|-------|:--------:|:----:|
"""

    if chain_usage:
        for i, (chain, count) in enumerate(chain_usage.most_common(10), 1):
            ratio = (count / total_chains * 100) if total_chains > 0 else 0
            report += f"| {i} | {chain} | {count} | {ratio:.1f}% |\n"
    else:
        report += "| - | 체인 사용 기록 없음 | 0 | 0% |\n"

    report += f"\n**총 체인 호출**: {total_chains}회\n"

    report += """
---

## Agent 사용 통계

| 순위 | Agent | Model | 사용 횟수 |
|:----:|-------|:-----:|:--------:|
"""

    if agent_usage:
        for i, (agent, count) in enumerate(agent_usage.most_common(15), 1):
            model = KNOWN_AGENTS.get(agent, "unknown")
            report += f"| {i} | {agent} | {model} | {count} |\n"
    else:
        report += "| - | 에이전트 사용 기록 없음 | - | 0 |\n"

    report += f"\n**총 에이전트 호출**: {total_agents}회\n"

    # 모델별 집계
    opus_count = sum(count for agent, count in agent_usage.items() if KNOWN_AGENTS.get(agent) == "opus")
    sonnet_count = sum(count for agent, count in agent_usage.items() if KNOWN_AGENTS.get(agent) == "sonnet")

    if total_agents > 0:
        report += f"""
### 모델별 분포
- **Opus**: {opus_count}회 ({opus_count/total_agents*100:.1f}%)
- **Sonnet**: {sonnet_count}회 ({sonnet_count/total_agents*100:.1f}%)
"""

    report += """
---

## Skill 사용 통계

| 순위 | Skill | 사용 횟수 |
|:----:|-------|:--------:|
"""

    if skill_usage:
        for i, (skill, count) in enumerate(skill_usage.most_common(15), 1):
            report += f"| {i} | {skill} | {count} |\n"
    else:
        report += "| - | 스킬 사용 기록 없음 | 0 |\n"

    report += f"\n**총 스킬 호출**: {total_skills}회\n"

    report += """
---

## 세션 목록

| # | 세션 ID | 요약 | 메시지 수 |
|:-:|---------|------|:--------:|
"""

    for i, session in enumerate(sessions[:20], 1):  # 최대 20개
        session_id = session['sessionId'][:8]  # 축약
        summary = session['summary'][:40] + "..." if len(session['summary']) > 40 else session['summary']
        msg_count = session['messageCount']
        report += f"| {i} | {session_id} | {summary} | {msg_count} |\n"

    if len(sessions) > 20:
        report += f"\n*... 외 {len(sessions) - 20}개 세션*\n"

    report += """
---

## 시사점

"""

    # 자동 인사이트 생성
    insights = []

    if not chain_usage:
        insights.append("- 체인 사용 기록이 없습니다. 체인 선언 형식(`📋 체인 구성:`)을 사용해보세요.")
    elif top_chain[0] == "Direct":
        insights.append("- 'Direct' 사용이 많습니다. 복잡한 작업에는 체인 패턴 적용을 고려해보세요.")

    if total_agents > 0:
        if opus_count > sonnet_count * 2:
            insights.append("- Opus 모델 사용이 많습니다. 간단한 작업은 Sonnet으로 대체하면 비용 절감이 가능합니다.")
        if sonnet_count > opus_count * 3:
            insights.append("- Sonnet 모델 사용이 많습니다. 복잡한 분석 작업에는 Opus를 고려해보세요.")

    # 미사용 체인 확인
    used_chains = set(chain_usage.keys())
    unused_chains = set(KNOWN_CHAINS) - used_chains - {"Direct"}
    if unused_chains and len(unused_chains) < len(KNOWN_CHAINS):
        insights.append(f"- 미사용 체인: {', '.join(list(unused_chains)[:5])}")

    if not insights:
        insights.append("- 균형 잡힌 사용 패턴입니다.")

    report += "\n".join(insights)

    report += f"""

---

*이 리포트는 chain_report_generator.py에 의해 자동 생성되었습니다.*
*생성 시각: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return report


def main():
    """메인 함수"""
    # 인자 파싱
    target_date = datetime.now()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--date" and len(sys.argv) > 2:
            try:
                target_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
            except ValueError:
                print(f"Invalid date format: {sys.argv[2]}. Use YYYY-MM-DD", file=sys.stderr)
                sys.exit(1)
        elif sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)

    print(f"📊 Chain Usage Report Generator")
    print(f"분석 대상 날짜: {target_date.strftime('%Y-%m-%d')}")
    print("-" * 50)

    # 세션 수집
    sessions = get_sessions_for_date(target_date)
    print(f"발견된 세션: {len(sessions)}개")

    if not sessions:
        print("해당 날짜의 세션이 없습니다.")
        sys.exit(0)

    # 사용 패턴 분석
    total_chain_usage = Counter()
    total_agent_usage = Counter()
    total_skill_usage = Counter()

    for session in sessions:
        messages = parse_jsonl_file(session['path'])
        total_chain_usage.update(extract_chain_usage(messages))
        total_agent_usage.update(extract_agent_usage(messages))
        total_skill_usage.update(extract_skill_usage(messages))

    print(f"체인 사용: {sum(total_chain_usage.values())}회")
    print(f"에이전트 사용: {sum(total_agent_usage.values())}회")
    print(f"스킬 사용: {sum(total_skill_usage.values())}회")

    # 리포트 생성
    report = generate_report(
        target_date, sessions,
        total_chain_usage, total_agent_usage, total_skill_usage
    )

    # 파일 저장
    seq = get_next_sequence_number(target_date)
    yymm = target_date.strftime("%y%m")
    filename = f"{yymm}_{seq:03d}_daily_chain_report.md"
    output_path = REPORT_DIR / filename

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print("-" * 50)
    print(f"✅ 리포트 생성 완료: {output_path}")

    return str(output_path)


if __name__ == "__main__":
    main()
