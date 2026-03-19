#!/usr/bin/env python3
"""
memory_mcp.py — Qdrant 벡터 검색 MCP 서버 (5개 도구)

Phase 2 Step 4 (C1 온톨로지 메모리)
Python: ~/.claude/venv/bin/python3

MCP 도구:
  - memory_search: 프롬프트 기반 관련 메모리 검색
  - memory_read: 특정 메모리 섹션 읽기
  - memory_graph: 메모리 간 관계 그래프 탐색
  - memory_index: 새 메모리 파일 수동 인덱싱
  - memory_stats: 메모리 시스템 통계
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path

from fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

# memory_embedder.py와 같은 디렉토리
sys.path.insert(0, str(Path(__file__).parent))
from memory_embedder import MemoryEmbedder

# 환경변수 또는 기본값
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))
COLLECTION_NAME = "claude_memory"

mcp = FastMCP("memory-ontology")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedder = MemoryEmbedder()


@mcp.tool()
def memory_search(query: str, top_k: int = 3, min_score: float = 0.7) -> list:
    """프롬프트와 의미적으로 관련된 과거 메모리를 검색한다.

    Args:
        query: 검색할 텍스트 (한국어/영어 모두 지원)
        top_k: 반환할 최대 결과 수 (기본 3)
        min_score: 최소 유사도 점수 0~1 (기본 0.7)
    """
    vector = embedder.embed_query(query)

    response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=top_k,
        score_threshold=min_score,
        with_payload=True,
    )

    # memory_id별 최고 점수만 반환 (중복 제거)
    seen = {}
    for r in response.points:
        mem_id = r.payload.get("memory_id", "")
        score = round(r.score, 3)
        if mem_id not in seen or score > seen[mem_id]["score"]:
            seen[mem_id] = {
                "id": mem_id,
                "score": score,
                "summary": r.payload.get("summary", ""),
                "file_path": r.payload.get("file_path", ""),
                "section": r.payload.get("chunk_section", ""),
            }

    results = sorted(seen.values(), key=lambda x: x["score"], reverse=True)[:top_k]
    return results


@mcp.tool()
def memory_read(memory_id: str, section: str = None) -> dict:
    """특정 메모리의 내용을 읽는다. 섹션 지정 시 해당 섹션만 반환.

    Args:
        memory_id: 메모리 식별자 (예: 2603_010_v5_improvement_direction)
        section: 특정 섹션명 (None이면 전체)
    """
    # memory_id로 모든 청크 조회
    response = qdrant.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[FieldCondition(key="memory_id", match=MatchValue(value=memory_id))]
        ),
        limit=100,
        with_payload=True,
    )

    points = response[0]
    if not points:
        return {"error": f"메모리 '{memory_id}'를 찾을 수 없습니다."}

    # 섹션 필터링
    chunks = []
    for p in points:
        chunk_section = p.payload.get("chunk_section", "")
        if section and section.lower() not in chunk_section.lower():
            continue
        chunks.append({
            "section": chunk_section,
            "index": p.payload.get("chunk_index", 0),
        })

    chunks.sort(key=lambda x: x["index"])

    # 관계 정보
    related = []
    related_str = points[0].payload.get("related_to", "[]")
    try:
        related = json.loads(related_str)
    except (json.JSONDecodeError, TypeError):
        pass

    return {
        "memory_id": memory_id,
        "file_path": points[0].payload.get("file_path", ""),
        "summary": points[0].payload.get("summary", ""),
        "created": points[0].payload.get("created", ""),
        "tags": points[0].payload.get("tags", []),
        "sections": [c["section"] for c in chunks],
        "chunk_count": len(chunks),
        "related": related,
    }


@mcp.tool()
def memory_graph(memory_id: str, hops: int = 2) -> dict:
    """메모리 간 관계 그래프를 탐색한다.

    Args:
        memory_id: 시작 메모리 식별자
        hops: 탐색 깊이 (기본 2)
    """
    nodes = {}
    edges = []
    visited = set()

    def traverse(mid: str, depth: int):
        if mid in visited or depth > hops:
            return
        visited.add(mid)

        # 해당 메모리의 포인트 조회
        response = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[FieldCondition(key="memory_id", match=MatchValue(value=mid))]
            ),
            limit=1,
            with_payload=True,
        )

        points = response[0]
        if not points:
            return

        p = points[0]
        nodes[mid] = {
            "summary": p.payload.get("summary", ""),
            "created": p.payload.get("created", ""),
            "tags": p.payload.get("tags", []),
        }

        # 관계 파싱
        related_str = p.payload.get("related_to", "[]")
        try:
            related = json.loads(related_str)
        except (json.JSONDecodeError, TypeError):
            related = []

        for rel in related:
            target_id = rel.get("id", "")
            edges.append({
                "source": mid,
                "target": target_id,
                "relation": rel.get("relation", "topic"),
                "weight": rel.get("weight", 0),
            })
            traverse(target_id, depth + 1)

    traverse(memory_id, 0)

    return {
        "root": memory_id,
        "hops": hops,
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }


@mcp.tool()
def memory_index(file_path: str) -> dict:
    """새 메모리 파일을 수동으로 인덱싱한다.

    Args:
        file_path: .md 파일의 절대 경로
    """
    from memory_indexer import index_file

    path = Path(file_path)
    if not path.exists():
        return {"error": f"파일 없음: {file_path}"}

    count = index_file(qdrant, embedder, path, build_relations=True)

    return {
        "file_path": file_path,
        "vector_count": count,
        "status": "indexed",
    }


@mcp.tool()
def memory_stats() -> dict:
    """메모리 시스템 통계를 반환한다."""
    info = qdrant.get_collection(COLLECTION_NAME)

    # 모든 포인트 스캔하여 통계 수집
    all_points = []
    offset = None
    while True:
        response = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            offset=offset,
            with_payload=True,
        )
        points, next_offset = response
        all_points.extend(points)
        if next_offset is None:
            break
        offset = next_offset

    # memory_id별 그룹핑
    memory_ids = set()
    month_counter = Counter()
    tag_counter = Counter()

    for p in all_points:
        mid = p.payload.get("memory_id", "")
        memory_ids.add(mid)

        created = p.payload.get("created", "")
        if created and len(created) >= 7:
            month_counter[created[:7]] += 1

        tags = p.payload.get("tags", [])
        for tag in tags:
            tag_counter[tag] += 1

    return {
        "total_points": info.points_count,
        "total_memories": len(memory_ids),
        "by_month": dict(sorted(month_counter.items())),
        "top_tags": dict(tag_counter.most_common(10)),
        "collection_status": str(info.status),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
