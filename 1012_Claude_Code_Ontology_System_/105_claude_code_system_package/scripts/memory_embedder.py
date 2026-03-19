#!/usr/bin/env python3
"""
memory_embedder.py — 텍스트를 multilingual-e5-large 1024차원 벡터로 변환

Phase 2 Step 2 (C1 온톨로지 메모리)
Python: ~/.claude/venv/bin/python3
"""

import re
from pathlib import Path

import yaml
from sentence_transformers import SentenceTransformer


class MemoryEmbedder:
    MODEL_NAME = "intfloat/multilingual-e5-large"
    DIMENSION = 1024
    BATCH_SIZE = 32  # CPU 모드 메모리 초과 방지

    def __init__(self):
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy loading — 첫 호출 시 모델 로드"""
        if self._model is None:
            self._model = SentenceTransformer(self.MODEL_NAME)
        return self._model

    def embed(self, text: str) -> list[float]:
        """단일 텍스트 → 1024차원 벡터"""
        # e5 모델은 query: 또는 passage: 접두사 필요
        prefixed = f"passage: {text}"
        vector = self.model.encode(prefixed, normalize_embeddings=True)
        return vector.tolist()

    def embed_query(self, query: str) -> list[float]:
        """검색 쿼리용 임베딩 (query: 접두사)"""
        prefixed = f"query: {query}"
        vector = self.model.encode(prefixed, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """배치 처리 — 전체 인덱싱 시 사용"""
        prefixed = [f"passage: {t}" for t in texts]
        vectors = self.model.encode(
            prefixed,
            normalize_embeddings=True,
            batch_size=self.BATCH_SIZE,
            show_progress_bar=True,
        )
        return vectors.tolist()

    def embed_file(self, file_path: str) -> list[dict]:
        """
        .md 파일 → 섹션별 청크 리스트
        Returns: [{"chunk_index", "section", "text", "vector", "metadata"}, ...]
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"파일 없음: {file_path}")

        content = path.read_text(encoding="utf-8")

        # frontmatter 파싱
        metadata = self._parse_frontmatter(content)

        # 본문 추출 (frontmatter 제거)
        body = self._strip_frontmatter(content)

        # 청킹
        chunks = self.chunk_markdown(body)

        # 배치 임베딩
        texts = [c["text"] for c in chunks]
        if not texts:
            return []

        vectors = self.embed_batch(texts)

        # 결과 조합
        results = []
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            results.append({
                "chunk_index": i,
                "section": chunk["section"],
                "text": chunk["text"],
                "vector": vector,
                "metadata": metadata,
            })

        return results

    def chunk_markdown(self, content: str) -> list[dict]:
        """헤딩(##, ###) 기준으로 섹션 분할, 200~500자 청크"""
        # 헤딩 기준 분할
        sections = re.split(r'\n(?=#{1,3}\s)', content)

        chunks = []
        for section in sections:
            section = section.strip()
            if not section:
                continue

            # 섹션명 추출
            heading_match = re.match(r'^(#{1,3})\s+(.+)', section)
            if heading_match:
                section_name = heading_match.group(2).strip()
            else:
                section_name = "intro"

            # 코드블록, 테이블 등 제거 (순수 텍스트)
            clean_text = self._clean_for_embedding(section)

            if len(clean_text) < 50:
                # 너무 짧은 섹션은 스킵
                continue

            # 500자 초과 시 분할
            if len(clean_text) > 500:
                sub_chunks = self._split_long_text(clean_text, 300, 500)
                for j, sub in enumerate(sub_chunks):
                    chunks.append({
                        "section": f"{section_name} ({j+1})",
                        "text": sub,
                    })
            else:
                chunks.append({
                    "section": section_name,
                    "text": clean_text,
                })

        return chunks

    def _parse_frontmatter(self, content: str) -> dict:
        """YAML frontmatter 파싱"""
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}

    def _strip_frontmatter(self, content: str) -> str:
        """frontmatter 제거"""
        return re.sub(r'^---\s*\n.*?\n---\s*\n?', '', content, count=1, flags=re.DOTALL)

    def _clean_for_embedding(self, text: str) -> str:
        """임베딩용 텍스트 정제 — 코드블록/테이블/링크 제거"""
        # 코드블록 제거
        text = re.sub(r'```[\s\S]*?```', '', text)
        # 인라인 코드 제거
        text = re.sub(r'`[^`]+`', '', text)
        # Obsidian 위키링크 → 표시명만
        text = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', text)
        text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
        # 마크다운 이미지/링크
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'\[([^\]]+)\]\(.*?\)', r'\1', text)
        # 헤딩 마크다운 기호 제거
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # 테이블 구분선
        text = re.sub(r'\|[-:]+\|[-:|\s]+\|', '', text)
        # 콜아웃 접두사
        text = re.sub(r'>\s*\[!.*?\]\s*', '', text)
        # 연속 공백/줄바꿈 정리
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def _split_long_text(self, text: str, min_len: int, max_len: int) -> list[str]:
        """긴 텍스트를 문장 단위로 분할"""
        sentences = re.split(r'(?<=[.!?。])\s+', text)
        chunks = []
        current = ""

        for sent in sentences:
            if len(current) + len(sent) > max_len and len(current) >= min_len:
                chunks.append(current.strip())
                current = sent
            else:
                current = f"{current} {sent}" if current else sent

        if current.strip():
            chunks.append(current.strip())

        return chunks


if __name__ == "__main__":
    import sys

    embedder = MemoryEmbedder()

    if len(sys.argv) > 1:
        # 파일 임베딩 테스트
        file_path = sys.argv[1]
        results = embedder.embed_file(file_path)
        print(f"파일: {file_path}")
        print(f"청크 수: {len(results)}")
        for r in results:
            print(f"  [{r['chunk_index']}] {r['section']}: {len(r['text'])}자, 벡터 {len(r['vector'])}차원")
    else:
        # 단순 테스트
        test_text = "Claude Code의 메모리 시스템을 벡터 DB로 개선하는 프로젝트"
        vec = embedder.embed(test_text)
        print(f"테스트 텍스트: {test_text}")
        print(f"벡터 차원: {len(vec)}")
        print(f"벡터 샘플 (첫 5개): {vec[:5]}")
