#!/usr/bin/env python3
"""
memory_indexer.py — 메모리 .md 파일을 Qdrant에 벡터화하여 저장

Phase 2 Step 3 (C1 온톨로지 메모리)
Python: ~/.claude/venv/bin/python3

사용법:
  # 전체 인덱싱 (최초)
  python3 memory_indexer.py --all

  # 단일 파일 인덱싱
  python3 memory_indexer.py --file <path>

  # 특정 디렉토리 인덱싱
  python3 memory_indexer.py --dir <path>
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FilterSelector, FieldCondition, MatchValue

# memory_embedder.py와 같은 디렉토리
sys.path.insert(0, str(Path(__file__).parent))
from memory_embedder import MemoryEmbedder

# 상수
COLLECTION_NAME = "claude_memory"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# 메모리 디렉토리 (기본)
DEFAULT_MEMORY_DIR = Path.home() / ".claude" / "projects" / "-Users-changjaeyou" / "memory"

# 관계 유형
RELATION_TYPES = {
    "precedes": "시간적 선행",
    "follows": "시간적 후속",
    "topic": "동일 주제",
    "evidence": "근거/증거",
    "contrast": "대립/대비",
    "refines": "발전/개선",
}


def generate_point_id(file_path: str, chunk_index: int) -> int:
    """파일경로+청크인덱스로 결정적 포인트 ID 생성 (재인덱싱 시 덮어쓰기)"""
    key = f"{file_path}::{chunk_index}"
    hash_bytes = hashlib.md5(key.encode()).digest()
    # 양수 64비트 정수로 변환
    return int.from_bytes(hash_bytes[:8], byteorder="big") & 0x7FFFFFFFFFFFFFFF


def extract_memory_id(file_path: Path) -> str:
    """파일명에서 memory_id 추출 (YYMM_SEQ_keyword)"""
    stem = file_path.stem
    # YYMM_SEQ_keyword 패턴
    match = re.match(r'^(\d{4}_\d{3}_\w+)', stem)
    if match:
        return match.group(1)
    return stem


def extract_tags_from_frontmatter(metadata: dict) -> list[str]:
    """frontmatter에서 태그 추출"""
    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return tags


def _infer_relation(current_id: str, other_id: str, score: float) -> str:
    """memory_id 순번 비교로 시간 관계 추론, 나머지는 topic"""
    try:
        # YYMM_SEQ_keyword 형식에서 YYMM_SEQ 추출
        cur_prefix = current_id[:8]  # e.g., "2603_035"
        oth_prefix = other_id[:8]
        if cur_prefix > oth_prefix:
            return "follows"  # 현재가 더 나중 → 이전 메모리를 follows
        elif cur_prefix < oth_prefix:
            return "precedes"  # 현재가 더 이전 → 이후 메모리를 precedes
    except (IndexError, ValueError):
        pass
    return "topic"


def find_related_memories(
    client: QdrantClient,
    embedder: MemoryEmbedder,
    text: str,
    current_memory_id: str,
    threshold: float = 0.80,
) -> list[dict]:
    """기존 벡터와 코사인 유사도 비교 → 관계 후보 반환 (시간 관계 자동 추론)"""
    vector = embedder.embed(text)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=5,
        score_threshold=threshold,
    )

    related = []
    seen_ids = set()
    for r in response.points:
        mem_id = r.payload.get("memory_id", "")
        if mem_id == current_memory_id or mem_id in seen_ids:
            continue
        seen_ids.add(mem_id)
        relation = _infer_relation(current_memory_id, mem_id, r.score)
        related.append({
            "id": mem_id,
            "relation": relation,
            "weight": round(r.score, 3),
        })

    return related


def index_file(
    client: QdrantClient,
    embedder: MemoryEmbedder,
    file_path: Path,
    build_relations: bool = True,
) -> int:
    """단일 파일 인덱싱 → Qdrant 저장, 저장된 포인트 수 반환"""
    memory_id = extract_memory_id(file_path)
    str_path = str(file_path)

    # 기존 포인트 삭제 (재인덱싱 지원)
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=FilterSelector(
            filter=Filter(
                must=[FieldCondition(key="memory_id", match=MatchValue(value=memory_id))]
            )
        ),
    )

    # 임베딩
    chunks = embedder.embed_file(str_path)
    if not chunks:
        print(f"  ⚠️ 청크 없음 (텍스트 부족): {file_path.name}")
        return 0

    # metadata 추출
    metadata = chunks[0].get("metadata", {})
    tags = extract_tags_from_frontmatter(metadata)
    created = metadata.get("created", "")
    summary = metadata.get("description", metadata.get("name", ""))

    # 관계 탐색 (첫 번째 청크 텍스트 기준)
    related_to = []
    if build_relations and chunks:
        combined_text = " ".join(c["text"][:200] for c in chunks[:3])
        related_to = find_related_memories(
            client, embedder, combined_text, memory_id, threshold=0.80
        )

    # 포인트 생성
    points = []
    for chunk in chunks:
        point_id = generate_point_id(str_path, chunk["chunk_index"])
        points.append(
            PointStruct(
                id=point_id,
                vector=chunk["vector"],
                payload={
                    "file_path": str_path,
                    "memory_id": memory_id,
                    "created": str(created) if created else "",
                    "tags": tags,
                    "summary": summary,
                    "chunk_section": chunk["section"],
                    "chunk_index": chunk["chunk_index"],
                    "parent_id": memory_id,
                    "word_count": len(chunk["text"].split()),
                    "related_to": json.dumps(related_to, ensure_ascii=False),
                },
            )
        )

    # Qdrant에 저장
    client.upsert(collection_name=COLLECTION_NAME, points=points)

    rel_str = f", 관계 {len(related_to)}개" if related_to else ""
    print(f"  ✅ {file_path.name}: {len(points)}포인트{rel_str}")

    return len(points)


def index_directory(
    client: QdrantClient,
    embedder: MemoryEmbedder,
    directory: Path,
    build_relations: bool = True,
) -> tuple[int, int]:
    """디렉토리 내 모든 .md 파일 인덱싱 (MEMORY.md 제외)"""
    md_files = sorted(directory.glob("*.md"))

    # MEMORY.md는 인덱스 파일이므로 제외
    md_files = [f for f in md_files if f.name != "MEMORY.md"]

    total_files = 0
    total_points = 0

    print(f"\n📂 디렉토리: {directory}")
    print(f"📄 대상 파일: {len(md_files)}개\n")

    for f in md_files:
        count = index_file(client, embedder, f, build_relations=build_relations)
        total_points += count
        total_files += 1

    return total_files, total_points


def main():
    parser = argparse.ArgumentParser(description="메모리 파일 Qdrant 벡터 인덱서")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="기본 메모리 디렉토리 전체 인덱싱")
    group.add_argument("--file", type=str, help="단일 파일 인덱싱")
    group.add_argument("--dir", type=str, help="특정 디렉토리 인덱싱")
    parser.add_argument("--no-relations", action="store_true", help="관계 탐색 비활성화 (빠른 인덱싱)")

    args = parser.parse_args()

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embedder = MemoryEmbedder()

    build_relations = not args.no_relations

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ 파일 없음: {args.file}")
            sys.exit(1)
        count = index_file(client, embedder, path, build_relations=build_relations)
        print(f"\n📊 완료: 1파일, {count}포인트")

    elif args.dir:
        directory = Path(args.dir)
        if not directory.is_dir():
            print(f"❌ 디렉토리 없음: {args.dir}")
            sys.exit(1)
        files, points = index_directory(client, embedder, directory, build_relations=build_relations)
        print(f"\n📊 완료: {files}파일, {points}포인트")

    else:  # --all
        directory = DEFAULT_MEMORY_DIR
        if not directory.is_dir():
            print(f"❌ 기본 메모리 디렉토리 없음: {directory}")
            sys.exit(1)
        files, points = index_directory(client, embedder, directory, build_relations=build_relations)
        print(f"\n📊 완료: {files}파일, {points}포인트")

    # 최종 통계
    info = client.get_collection(COLLECTION_NAME)
    print(f"🗃️ 총 포인트: {info.points_count}")


if __name__ == "__main__":
    main()
