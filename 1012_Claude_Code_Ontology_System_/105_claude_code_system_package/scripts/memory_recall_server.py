#!/usr/bin/env python3
"""
memory_recall_server.py — 상주형 메모리 리콜 HTTP 서버

모델을 메모리에 한 번만 로드하고, Hook에서 curl로 빠르게 쿼리.
포트: 18765 (localhost only)

사용법:
  # 서버 시작 (백그라운드)
  ~/.claude/venv/bin/python3 ~/.claude/scripts/memory_recall_server.py &

  # Hook에서 호출
  curl -s --max-time 2 "http://localhost:18765/recall?q=프롬프트텍스트&top_k=3&min_score=0.7"

  # 헬스체크
  curl -s http://localhost:18765/health

  # 서버 종료
  curl -s http://localhost:18765/shutdown
"""

import json
import os
import signal
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# scripts 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

from memory_embedder import MemoryEmbedder
from qdrant_client import QdrantClient

HOST = "127.0.0.1"
PORT = int(os.environ.get("MEMORY_RECALL_PORT", "18765"))
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))
COLLECTION = "claude_memory"

# 전역 인스턴스 (서버 시작 시 1회 로드)
embedder = None
qdrant = None


class RecallHandler(BaseHTTPRequestHandler):
    """메모리 리콜 HTTP 핸들러"""

    def log_message(self, format, *args):
        """접근 로그 무음 처리"""
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/health":
            self._respond(200, {"status": "ok", "model": "multilingual-e5-large"})

        elif path == "/recall":
            query = params.get("q", [""])[0]
            top_k = int(params.get("top_k", ["3"])[0])
            min_score = float(params.get("min_score", ["0.7"])[0])

            if len(query) < 5:
                self._respond(200, [])
                return

            results = self._search(query, top_k, min_score)
            self._respond(200, results)

        elif path == "/shutdown":
            self._respond(200, {"status": "shutting_down"})
            # 서버 종료
            import threading
            threading.Thread(target=self.server.shutdown).start()

        else:
            self._respond(404, {"error": "Not found"})

    def _search(self, query: str, top_k: int, min_score: float) -> list:
        """벡터 검색 실행"""
        try:
            vector = embedder.embed_query(query)
            response = qdrant.query_points(
                collection_name=COLLECTION,
                query=vector,
                limit=top_k * 2,  # 중복 제거 후 top_k 확보
                score_threshold=min_score,
                with_payload=True,
            )

            # memory_id별 최고 점수만
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

            return sorted(seen.values(), key=lambda x: x["score"], reverse=True)[:top_k]

        except Exception as e:
            return [{"error": str(e)}]

    def _respond(self, code: int, data):
        """JSON 응답"""
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    global embedder, qdrant

    # PID 파일 (중복 실행 방지)
    pid_file = Path("/tmp/memory_recall_server.pid")

    # 이미 실행 중인지 확인
    if pid_file.exists():
        old_pid = int(pid_file.read_text().strip())
        try:
            os.kill(old_pid, 0)  # 프로세스 존재 확인
            print(f"이미 실행 중 (PID {old_pid})")
            sys.exit(0)
        except OSError:
            pass  # 이전 프로세스 죽음 → 계속 진행

    # PID 기록
    pid_file.write_text(str(os.getpid()))

    # 종료 시 PID 파일 삭제
    def cleanup(signum=None, frame=None):
        pid_file.unlink(missing_ok=True)
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    # 모델 로드 (1회만)
    print("🧠 메모리 리콜 서버 시작...")
    print(f"  모델 로딩: multilingual-e5-large...")
    embedder = MemoryEmbedder()
    _ = embedder.model  # 즉시 로드 (lazy 해제)
    print(f"  ✅ 모델 로드 완료")

    qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    print(f"  ✅ Qdrant 연결 ({QDRANT_HOST}:{QDRANT_PORT})")

    # HTTP 서버 시작
    server = HTTPServer((HOST, PORT), RecallHandler)
    print(f"  🌐 http://{HOST}:{PORT}/recall 대기 중")
    print(f"  PID: {os.getpid()}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        cleanup()


if __name__ == "__main__":
    main()
