"""
효소 라우터 (Enzyme Router) — 코사인 유사도 즉시 분류
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: LLM 호출 없이 입력을 즉시 분류. API 0회, ~30ms.
     sentence-transformers 없으면 키워드 폴백.
"""
import hashlib
import time

_vectors: dict[str, list] = {}  # {route: [vectors]}
_loaded = False
_embed_fn = None

# ── 라우팅 앵커 ──
_ANCHORS = {
    "FAST": [
        "안녕", "뭐해", "고마워", "잘자", "ㅋㅋ", "심심해", "피곤해",
        "배고파", "좋은 아침", "기분 어때", "ㅎㅎ", "웃기다", "재밌다",
        "hello", "thanks", "good morning", "lol", "hi there",
        # 감정/짧은 반응 보강
        "수고했어", "배불러", "허전하다", "힘들다", "졸려", "귀찮아",
        "나간다", "안 잤어", "기분이 안 좋아", "맞아 맞아", "그러게",
        "대박", "그냥 그래", "별로야",
        "just chilling", "nothing much", "same here", "not really",
        "oh well", "sounds good", "see you", "sup", "brb", "nah",
        "I'm bored", "I'm tired",
    ],
    "BRAIN": [
        "어떻게 생각해", "분석해줘", "비교해줘", "장단점",
        "고민", "진로", "투자", "전략", "설계", "검증",
        "왜 그런걸까", "어떻게 해야 해", "판단", "조언",
        "should I", "what do you think", "pros and cons",
        "compare", "analyze", "quit my job", "advice",
        # 실용 분석 보강 (SEARCH 유출 방지)
        "평가해줘", "아이디어 봐줘", "계약서 검토", "전략 분석",
        "ROI 분석", "경쟁 분석", "인사이트 뽑아줘", "데이터 분석",
        "산업 분석", "영향 분석", "시장 분석", "포지셔닝",
        "번아웃 해결", "팀 문제", "조직 문제", "규제 영향",
        "evaluate this", "implications of", "competitive landscape",
        "negotiate salary", "sustainable long-term", "ROI on",
        "how should I", "is it worth",
    ],
    "SEARCH": [
        "검색해줘", "찾아봐", "뉴스", "날씨", "가격",
        "어디서", "언제", "몇시", "얼마", "맛집", "근처",
        "find me", "search for", "where is", "how much",
        "price of", "nearby",
        # 정보 검색 보강
        "몇 시에", "영업시간", "공고", "채용", "신작",
        "칼로리", "스펙", "순위", "예보", "일정",
        "forecast", "specs", "latest", "current",
        "when is", "what time", "who won",
        # 조회형 보강
        "실적 발표", "행사", "이벤트", "뭐 있어", "뭐 나와",
        "호텔 추천", "공고 있어", "일정이 언제",
        "earnings", "report summary", "comparison",
    ],
}

# ── FACTUAL 감지 키워드 ──
# FACTUAL: 구체적 사실 확인. "알려줘/추천해줘"는 BRAIN에서도 쓰이므로 제외
_FACTUAL_KEYWORDS = [
    "산업", "기업", "회사", "그룹", "가격", "얼마", "매장",
    "영업시간", "전화번호", "주소", "원산지", "시가총액",
    "시세", "환율", "요금", "배송비", "금리",
    # 정보 조회 시그널
    "채용", "공고", "행사", "이벤트", "신작", "칼로리",
    "호텔", "편의점", "추천해줘", "실적", "일정",
    "mortgage", "earnings",
]


def _load():
    global _vectors, _loaded, _embed_fn
    if _loaded:
        return
    try:
        from sentence_transformers import SentenceTransformer
        # paraphrase-multilingual: 다국어 지원 (한국어+영어+일본어+중국어)
        # all-MiniLM-L6-v2보다 크지만 다국어 정확도 훨씬 높음
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        _embed_fn = lambda texts: _model.encode(texts, normalize_embeddings=True).tolist()
        for route, anchors in _ANCHORS.items():
            _vectors[route] = _embed_fn(anchors)
    except ImportError:
        _embed_fn = None
    _loaded = True


def _cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb + 1e-9)


def route(query: str) -> dict | None:
    """코사인 유사도 기반 라우팅.

    Returns:
        {"route": str, "confidence": int} or None (폴백 필요)
    """
    _load()
    q = query.lower()

    # FACTUAL 감지 (강제가 아닌 가산점)
    has_factual = any(kw in q for kw in _FACTUAL_KEYWORDS)
    # 분석 동사 억제 — 분석 질문은 FACTUAL로 빼지 않음
    _ANALYSIS = ["분석", "평가", "검토", "비교", "설계", "전략",
                 "analyze", "evaluate", "compare", "implications",
                 "인사이트", "장단점", "어떻게 생각"]
    has_analysis = any(v in q for v in _ANALYSIS)

    # 임베딩 라우팅
    if _embed_fn and _vectors:
        q_vec = _embed_fn([query])[0]

        # top-1 매칭 + FACTUAL 가산점
        route_scores = {}
        for r, vecs in _vectors.items():
            best = max(_cosine(q_vec, v) for v in vecs) if vecs else 0
            route_scores[r] = best

        # FACTUAL 가산점 (분석 동사 없을 때만)
        if has_factual and not has_analysis:
            route_scores["SEARCH"] = route_scores.get("SEARCH", 0) + 0.12

        best_route = max(route_scores, key=route_scores.get)
        best_score = route_scores[best_route]
        conf = int(best_score * 100)

        if conf >= 20:
            return {"route": best_route, "confidence": conf}
        return None

    # 키워드 폴백
    if has_factual and not has_analysis:
        return {"route": "SEARCH", "confidence": 60}
    for r, anchors in _ANCHORS.items():
        if any(kw in q for kw in anchors):
            return {"route": r, "confidence": 60}
    return None
