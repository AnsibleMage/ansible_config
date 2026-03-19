#!/usr/bin/env python3
"""
log_analyzer.py — C5 Observability 월간 로그 분석기
Phase 2 Step 7 구현

사용법:
    python3 log_analyzer.py --month 2026-03
    python3 log_analyzer.py --month 2026-03 --since 2026-03-16

출력: ~/.claude/logs/reports/YYYYMM_monthly.md
"""

import argparse
import re
import os
import glob
from datetime import datetime, date
from collections import Counter, defaultdict
from pathlib import Path

# === 로그 형식 파서 (5개 형식) ===

# 형식 A: PostToolUse 로그 (observability-logger.sh)
# "2026-03-16 22:51 | - | Read[OK] | -"
PATTERN_A = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| "  # timestamp
    r"([^\|]+?) \| "                           # chain (or "-")
    r"(\w+)\[(\w+)\] \| "                     # tool[STATUS]
    r"(.+)"                                    # extra
)

# 형식 B: InstructionsLoaded / TeammateIdle
# "[2026-03-16 06:10] InstructionsLoaded | file=... | type=... | reason=..."
PATTERN_B = re.compile(
    r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (\w+) \| (.+)"
)

# 형식 C: Stop 이벤트
# "2026-03-16 22:02 | Stop | reason=end_turn | session="
PATTERN_C = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| Stop \| reason=(\w+) \| session=(.*)"
)

# 형식 D: ContextEstimate
# "2026-03-16 22:02 | ContextEstimate | turns=0 tools=0 agents=0 files=0 estimated=0tok (0%)"
PATTERN_D = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| ContextEstimate \| (.+)"
)

# 형식 E: HOOK_RECOMMEND (신규, auto-analyze.sh에서 기록)
# "2026-03-16 22:53 | HOOK_RECOMMEND | SystemDesignChain | -"
PATTERN_E = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| HOOK_RECOMMEND \| (\S+) \| -"
)

# 10개 체인 정의
ALL_CHAINS = [
    "SystemDesignChain", "AutomationChain", "GameDevChain", "DevChain",
    "ResearchChain", "DocChain+", "WebDevChain+", "MetaThinkChain",
    "RailsDevChain", "HotfixChain"
]

# 에이전트 정의 (subagent_type)
KNOWN_AGENTS = [
    "insight_explorer", "multidimensional_analyst", "connection_creator",
    "problem_reframer", "solution_innovator", "insight_amplifier",
    "learning_evolver", "complexity_resolver", "balanced_judge",
    "integrated_sage", "requirements_analyst", "system_architect",
    "code_developer", "quality_reviewer", "Explore", "Plan", "general-purpose"
]

# 토큰 추정 단가 (프록시)
TOKEN_ESTIMATES = {
    "Agent": 5000,
    "Explore": 5000,
    "Plan": 5000,
    "Read": 300,
    "Write": 500,
    "Edit": 400,
    "Bash": 800,
    "Grep": 200,
    "Glob": 150,
    "unknown": 300,
    "_default": 300,
}


def parse_log_file(filepath, since_date=None):
    """로그 파일을 파싱하여 이벤트 리스트를 반환한다."""
    events = []
    unparsed = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            event = None

            # 형식 E: HOOK_RECOMMEND (C 이전에 체크 — Stop보다 우선)
            m = PATTERN_E.match(line)
            if m:
                event = {
                    "type": "hook_recommend",
                    "timestamp": m.group(1),
                    "chain": m.group(2),
                }

            # 형식 C: Stop
            if not event:
                m = PATTERN_C.match(line)
                if m:
                    event = {
                        "type": "stop",
                        "timestamp": m.group(1),
                        "reason": m.group(2),
                        "session": m.group(3).strip(),
                    }

            # 형식 D: ContextEstimate
            if not event:
                m = PATTERN_D.match(line)
                if m:
                    event = {
                        "type": "context_estimate",
                        "timestamp": m.group(1),
                        "details": m.group(2),
                    }

            # 형식 B: [timestamp] EventType
            if not event:
                m = PATTERN_B.match(line)
                if m:
                    event = {
                        "type": "system_event",
                        "timestamp": m.group(1),
                        "event_name": m.group(2),
                        "details": m.group(3),
                    }

            # 형식 A: PostToolUse
            if not event:
                m = PATTERN_A.match(line)
                if m:
                    event = {
                        "type": "tool_use",
                        "timestamp": m.group(1),
                        "chain": m.group(2).strip(),
                        "tool": m.group(3),
                        "status": m.group(4),
                        "extra": m.group(5).strip(),
                    }

            if event:
                # since 필터링
                if since_date:
                    ts = event["timestamp"][:10]
                    if ts < since_date:
                        continue
                events.append(event)
            else:
                unparsed += 1

    return events, unparsed


def load_month_logs(log_dir, month_str, since_date=None):
    """지정 월의 모든 로그 파일을 로드한다."""
    # month_str: "2026-03" → 파일명 패턴: 202603*.log
    year_month = month_str.replace("-", "")
    pattern = os.path.join(log_dir, f"{year_month}*.log")
    files = sorted(glob.glob(pattern))

    all_events = []
    total_unparsed = 0
    total_lines = 0

    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            total_lines += sum(1 for line in fh if line.strip())
        events, unparsed = parse_log_file(f, since_date)
        all_events.extend(events)
        total_unparsed += unparsed

    return all_events, total_unparsed, total_lines, len(files)


# === 분석 모듈 ===

def analyze_chain_survival(events):
    """체인 생존율 분석 — HOOK_RECOMMEND 이벤트 기반."""
    chain_counts = Counter()
    for e in events:
        if e["type"] == "hook_recommend":
            chain_counts[e["chain"]] += 1

    results = []
    for chain in ALL_CHAINS:
        count = chain_counts.get(chain, 0)
        if count >= 5:
            status = "active"
        elif count >= 1:
            status = "low_usage"
        else:
            status = "dormant"
        results.append({"chain": chain, "count": count, "status": status})

    return results


def analyze_hook_accuracy(events):
    """Hook 추천 정확도 분석."""
    recommend_events = [e for e in events if e["type"] == "hook_recommend"]
    total = len(recommend_events)

    if total == 0:
        return {
            "total_recommendations": 0,
            "message": "HOOK_RECOMMEND 데이터 없음 — 로그 수집 기간 부족",
        }

    chain_recs = Counter()
    for e in recommend_events:
        chain_recs[e["chain"]] += 1

    return {
        "total_recommendations": total,
        "by_chain": dict(chain_recs.most_common()),
        "message": f"총 {total}회 추천 기록 (실제 체인 실행 대조는 향후 구현)",
    }


def analyze_agent_performance(events):
    """에이전트/도구별 성능 분석."""
    tool_events = [e for e in events if e["type"] == "tool_use"]

    tool_stats = defaultdict(lambda: {"total": 0, "ok": 0, "err": 0})
    for e in tool_events:
        tool = e["tool"]
        tool_stats[tool]["total"] += 1
        if e["status"] == "OK":
            tool_stats[tool]["ok"] += 1
        else:
            tool_stats[tool]["err"] += 1

    # unknown 비율 계산 (퍼센트)
    total_tool_calls = len(tool_events)
    unknown_count = tool_stats.get("unknown", {}).get("total", 0)
    unknown_ratio = (unknown_count / total_tool_calls * 100) if total_tool_calls > 0 else 0

    # 정렬: 호출 수 내림차순
    sorted_stats = sorted(tool_stats.items(), key=lambda x: x[1]["total"], reverse=True)

    return {
        "total_calls": total_tool_calls,
        "unknown_count": unknown_count,
        "unknown_ratio": unknown_ratio,
        "tools": sorted_stats,
    }


def estimate_tokens(events):
    """토큰 소비 추정 — 로그 줄 수 기반 프록시."""
    tool_events = [e for e in events if e["type"] == "tool_use"]
    chain_tokens = defaultdict(int)
    total_tokens = 0

    for e in tool_events:
        tool = e["tool"]
        chain = e.get("chain", "-")
        if chain == "-":
            chain = "uncategorized"
        tok = TOKEN_ESTIMATES.get(tool, TOKEN_ESTIMATES["_default"])
        chain_tokens[chain] += tok
        total_tokens += tok

    # 세션 오버헤드 추가 (Stop 이벤트 수 × 기본 세션 토큰)
    session_count = sum(1 for e in events if e["type"] == "stop")
    session_overhead = session_count * 3000  # 세션당 시스템 프롬프트 + 지시문
    chain_tokens["session_overhead"] = session_overhead
    total_tokens += session_overhead

    # 비율 계산
    results = []
    for chain, tok in sorted(chain_tokens.items(), key=lambda x: x[1], reverse=True):
        pct = (tok / total_tokens * 100) if total_tokens > 0 else 0
        results.append({"chain": chain, "tokens": tok, "percent": pct})

    return {"total": total_tokens, "by_chain": results}


def analyze_data_quality(events, total_unparsed, total_lines):
    """데이터 품질 분석."""
    tool_events = [e for e in events if e["type"] == "tool_use"]
    total_tool = len(tool_events)
    unknown_count = sum(1 for e in tool_events if e["tool"] == "unknown")
    hook_rec_count = sum(1 for e in events if e["type"] == "hook_recommend")
    chain_valid = sum(1 for e in tool_events if e.get("chain", "-") != "-")

    return {
        "total_lines": total_lines,
        "parsed_events": len(events),
        "unparsed_lines": total_unparsed,
        "parse_rate": (len(events) / total_lines * 100) if total_lines > 0 else 0,
        "tool_calls": total_tool,
        "unknown_count": unknown_count,
        "unknown_ratio": (unknown_count / total_tool * 100) if total_tool > 0 else 0,
        "hook_recommend_count": hook_rec_count,
        "chain_valid_count": chain_valid,
        "chain_valid_ratio": (chain_valid / total_tool * 100) if total_tool > 0 else 0,
    }


# === 리포트 생성 ===

def generate_report(month_str, events, total_unparsed, total_lines, file_count, since_date=None):
    """Obsidian 마크다운 리포트를 생성한다."""
    now = datetime.now().strftime("%Y-%m-%d")

    # 분석 실행
    chain_survival = analyze_chain_survival(events)
    hook_accuracy = analyze_hook_accuracy(events)
    agent_perf = analyze_agent_performance(events)
    token_est = estimate_tokens(events)
    data_quality = analyze_data_quality(events, total_unparsed, total_lines)

    # 세션 수 (Stop 이벤트 수)
    session_count = sum(1 for e in events if e["type"] == "stop")

    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f'title: "Observability 월간 리포트 — {month_str}"')
    lines.append(f'created: "{now}"')
    lines.append("tags: [observability, report, monthly]")
    lines.append("---")
    lines.append("")

    # 요약
    lines.append(f"# Observability 월간 리포트 — {month_str}")
    lines.append("")
    lines.append("## 1. 요약")
    lines.append("")
    lines.append(f"| 항목 | 값 |")
    lines.append(f"|------|------|")
    lines.append(f"| 분석 기간 | {month_str}{f' (since {since_date})' if since_date else ''} |")
    lines.append(f"| 로그 파일 수 | {file_count}개 |")
    lines.append(f"| 총 로그 줄 | {data_quality['total_lines']}줄 |")
    lines.append(f"| 파싱된 이벤트 | {data_quality['parsed_events']}건 |")
    lines.append(f"| 세션 수 | {session_count}회 |")
    lines.append(f"| 도구 호출 수 | {agent_perf['total_calls']}회 |")
    lines.append(f"| 추정 총 토큰 | {token_est['total']:,}tok |")
    lines.append("")

    # 데이터 품질
    lines.append("## 2. 데이터 품질")
    lines.append("")
    lines.append(f"| 지표 | 값 | 평가 |")
    lines.append(f"|------|------|------|")
    parse_eval = "PASS" if data_quality["parse_rate"] >= 95 else "WARN"
    lines.append(f"| 파싱 성공률 | {data_quality['parse_rate']:.1f}% | {parse_eval} |")
    unknown_eval = "PASS" if data_quality["unknown_ratio"] <= 10 else ("WARN" if data_quality["unknown_ratio"] <= 50 else "FAIL")
    lines.append(f"| unknown 도구 비율 | {data_quality['unknown_ratio']:.1f}% ({data_quality['unknown_count']}/{data_quality['tool_calls']}) | {unknown_eval} |")
    lines.append(f"| HOOK_RECOMMEND 수 | {data_quality['hook_recommend_count']}건 | {'PASS' if data_quality['hook_recommend_count'] > 0 else 'NO_DATA'} |")
    lines.append(f"| 체인 유효율 | {data_quality['chain_valid_ratio']:.1f}% | {'PASS' if data_quality['chain_valid_ratio'] > 50 else 'LOW'} |")
    lines.append(f"| 미파싱 줄 | {data_quality['unparsed_lines']}줄 | {'PASS' if data_quality['unparsed_lines'] == 0 else 'WARN'} |")
    lines.append("")

    # 체인 생존율
    lines.append("## 3. 체인 생존율")
    lines.append("")
    lines.append("| 체인 | 추천 횟수 | 상태 | 권고 |")
    lines.append("|------|----------|------|------|")
    for r in chain_survival:
        if r["status"] == "active":
            action = "유지"
        elif r["status"] == "low_usage":
            action = "트리거 키워드 확장 검토"
        else:
            action = "3개월 연속 시 아카이브 후보"
        lines.append(f"| {r['chain']} | {r['count']} | {r['status']} | {action} |")
    lines.append("")

    # Hook 추천 정확도
    lines.append("## 4. Hook 추천 정확도")
    lines.append("")
    if hook_accuracy["total_recommendations"] == 0:
        lines.append(f"> {hook_accuracy['message']}")
    else:
        lines.append(f"- 총 추천 횟수: {hook_accuracy['total_recommendations']}회")
        lines.append(f"- {hook_accuracy['message']}")
        lines.append("")
        if "by_chain" in hook_accuracy:
            lines.append("| 추천 체인 | 횟수 |")
            lines.append("|----------|------|")
            for chain, cnt in hook_accuracy["by_chain"].items():
                lines.append(f"| {chain} | {cnt} |")
    lines.append("")

    # 에이전트/도구 성능
    lines.append("## 5. 에이전트/도구 성능")
    lines.append("")
    lines.append(f"총 도구 호출: {agent_perf['total_calls']}회 | unknown 비율: {agent_perf['unknown_ratio']:.1f}%")
    lines.append("")
    lines.append("| 도구/에이전트 | 호출 | 성공 | 오류 | 성공률 |")
    lines.append("|-------------|------|------|------|--------|")
    for tool, stats in agent_perf["tools"]:
        success_rate = (stats["ok"] / stats["total"] * 100) if stats["total"] > 0 else 0
        lines.append(f"| {tool} | {stats['total']} | {stats['ok']} | {stats['err']} | {success_rate:.0f}% |")
    lines.append("")

    # 토큰 소비 추정
    lines.append("## 6. 토큰 소비 추정")
    lines.append("")
    lines.append(f"> 프록시 추정: Agent=5000tok, Read=300tok, Write=500tok, Bash=800tok, 기타=300tok")
    lines.append(f"> 총 추정: **{token_est['total']:,}tok**")
    lines.append("")
    lines.append("| 카테고리 | 추정 토큰 | 비율 |")
    lines.append("|---------|----------|------|")
    for r in token_est["by_chain"]:
        lines.append(f"| {r['chain']} | {r['tokens']:,} | {r['percent']:.1f}% |")
    lines.append("")

    # 개선 제안
    lines.append("## 7. 개선 제안")
    lines.append("")
    suggestions = []
    if data_quality["unknown_ratio"] > 10:
        suggestions.append(f"- **도구명 캡처 개선**: unknown 비율 {data_quality['unknown_ratio']:.0f}%로 높음. observability-logger.sh의 tool_name 파싱 확인 필요")
    if data_quality["hook_recommend_count"] == 0:
        suggestions.append("- **HOOK_RECOMMEND 로그 부재**: auto-analyze.sh에 HOOK_RECOMMEND 이벤트 로깅이 동작하지 않음")
    if data_quality["chain_valid_ratio"] < 50:
        suggestions.append(f"- **체인 추적 미비**: 유효 체인 비율 {data_quality['chain_valid_ratio']:.0f}%. 체인 실행 시 /tmp/claude_current_chain.txt 기록 메커니즘 필요")
    if session_count == 0:
        suggestions.append("- **세션 데이터 부재**: Stop 이벤트 없음. stop-cleanup.sh 동작 확인 필요")
    if not suggestions:
        suggestions.append("- 현재 데이터 품질 양호. 정기 모니터링 유지")
    lines.extend(suggestions)
    lines.append("")

    lines.append("---")
    lines.append(f"*Generated by log_analyzer.py on {now}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="C5 Observability 월간 로그 분석기")
    parser.add_argument("--month", required=True, help="분석 대상 월 (YYYY-MM)")
    parser.add_argument("--since", default=None, help="이 날짜 이후만 분석 (YYYY-MM-DD)")
    parser.add_argument("--log-dir", default=os.path.expanduser("~/.claude/logs"), help="로그 디렉토리")
    parser.add_argument("--output-dir", default=None, help="리포트 출력 디렉토리")
    args = parser.parse_args()

    log_dir = args.log_dir
    output_dir = args.output_dir or os.path.join(log_dir, "reports")
    os.makedirs(output_dir, exist_ok=True)

    print(f"📊 로그 분석 시작: {args.month}")
    print(f"📂 로그 디렉토리: {log_dir}")

    events, total_unparsed, total_lines, file_count = load_month_logs(
        log_dir, args.month, args.since
    )

    if not events and total_lines == 0:
        print(f"❌ {args.month} 로그 파일 없음")
        return

    print(f"📄 로그 파일: {file_count}개, {total_lines}줄, 파싱 {len(events)}이벤트")

    report = generate_report(
        args.month, events, total_unparsed, total_lines, file_count, args.since
    )

    # 출력 파일 저장
    month_compact = args.month.replace("-", "")
    output_file = os.path.join(output_dir, f"{month_compact}_monthly.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 리포트 생성: {output_file}")


if __name__ == "__main__":
    main()
