"""
해마 (Hippocampus) — 메모리 저장/검색
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 대화 기억의 저장/검색/관련 기억 주입.
     short_term → long_term → archive 계층.
"""


class SimpleMemory:
    """공개용 간단 메모리. 프로덕션에서는 벡터 DB + SQLite."""

    def __init__(self, max_items: int = 100):
        self._store: list[dict] = []
        self._max = max_items

    def store(self, query: str, answer: str, tags: list[str] | None = None):
        """기억 저장."""
        import time
        self._store.append({
            "query": query[:200],
            "answer": answer[:500],
            "tags": tags or [],
            "ts": time.time(),
        })
        if len(self._store) > self._max:
            self._store = self._store[-self._max:]

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """최근 기억에서 키워드 기반 검색."""
        keywords = set(query.lower().split())
        scored = []
        for mem in self._store:
            overlap = len(keywords & set(mem["query"].lower().split()))
            if overlap > 0:
                scored.append((overlap, mem))
        scored.sort(key=lambda x: -x[0])
        return [m for _, m in scored[:top_k]]

    def context_string(self, query: str) -> str:
        """검색 결과를 컨텍스트 문자열로."""
        memories = self.retrieve(query)
        if not memories:
            return ""
        parts = [f"Q:{m['query'][:40]} A:{m['answer'][:60]}" for m in memories]
        return "관련 기억: " + " | ".join(parts)
