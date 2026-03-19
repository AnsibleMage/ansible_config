#!/usr/bin/env python3
"""
memory_recall.py — Hook용 메모리 리콜 (3초 타임아웃)

프롬프트를 받아 Qdrant에서 관련 메모리를 검색하고 포맷팅된 결과를 stdout으로 출력.
auto-analyze.sh에서 호출됨.

사용법: python3 memory_recall.py "프롬프트 텍스트"
"""

import signal
import sys

# 3초 타임아웃 — 실패 시 조용히 종료 (기존 분석은 정상 동작)
def timeout_handler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)

try:
    import json
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))

    from memory_embedder import MemoryEmbedder
    from qdrant_client import QdrantClient

    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if len(query) < 10:
        sys.exit(0)

    embedder = MemoryEmbedder()
    client = QdrantClient(host="localhost", port=6333)

    vector = embedder.embed_query(query)
    response = client.query_points(
        collection_name="claude_memory",
        query=vector,
        limit=5,
        score_threshold=0.7,
        with_payload=True,
    )

    # memory_id별 최고 점수만 (중복 제거)
    seen = {}
    for r in response.points:
        mem_id = r.payload.get("memory_id", "")
        score = round(r.score, 3)
        if mem_id not in seen or score > seen[mem_id]["score"]:
            seen[mem_id] = {
                "id": mem_id,
                "score": score,
                "summary": r.payload.get("summary", "요약 없음"),
            }

    results = sorted(seen.values(), key=lambda x: x["score"], reverse=True)[:3]

    if results:
        lines = []
        for r in results:
            score_pct = int(r["score"] * 100)
            lines.append(f"- [{score_pct}%] {r['id']}: {r['summary']}")

        output = "\n".join(lines)
        print(output)

except SystemExit:
    raise
except Exception:
    pass  # 모든 에러 무시 — Hook 안정성 최우선
