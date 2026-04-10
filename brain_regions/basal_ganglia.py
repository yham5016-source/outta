"""
기저핵 (Basal Ganglia) — 패턴 캐시
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 반복 질문에 대한 빠른 응답. 해시 기반 캐시.
     단순 질문은 LLM 호출 없이 즉시 반환.
"""
import hashlib
import time

_CACHE: dict = {}
_TTL = 600  # 10분


def lookup(query: str) -> str | None:
    """캐시에서 조회."""
    key = hashlib.md5(query.encode()).hexdigest()
    if key in _CACHE:
        resp, ts = _CACHE[key]
        if time.time() - ts < _TTL:
            return resp
        del _CACHE[key]
    return None


def store(query: str, response: str):
    """캐시에 저장."""
    key = hashlib.md5(query.encode()).hexdigest()
    _CACHE[key] = (response, time.time())
