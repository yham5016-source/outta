"""
글리아 (Glia) — 적응형 temperature 조절
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: v2 — 칭찬 억제 + 대화 유형별 temperature 보정.
"""
import time

_state = {
    "praise_streak": 0,
    "last_reset": time.time(),
}

_PRAISE_WORDS = ["잘했", "대단", "최고", "완벽", "놀라", "훌륭",
                 "good", "great", "amazing", "perfect"]
_RESET_INTERVAL = 1800  # 30분

# ── 유형별 base temperature 보정 ──
_TYPE_ADJUST = {
    "정보요청": -0.2,   # 사실 질문 → 낮게
    "판단필요": 0.0,    # 분석 → 기본
    "감정지원": 0.1,    # 감정 → 약간 높게
    "창작": 0.2,        # 창작 → 높게
    "기타": 0.0,
    "FAST": 0.0,
    "BRAIN": 0.0,
    "SEARCH": -0.2,
}


def detect_praise(user_msg: str) -> bool:
    return any(w in user_msg.lower() for w in _PRAISE_WORDS)


def update(user_msg: str, query_type: str = "기타") -> float:
    """글리아 상태 업데이트. temperature 보정값 반환.

    Returns:
        temperature 보정값 (-0.4 ~ +0.2)
    """
    now = time.time()
    if now - _state["last_reset"] > _RESET_INTERVAL:
        _state["praise_streak"] = 0
        _state["last_reset"] = now

    # 칭찬 억제
    praise_adj = 0.0
    if detect_praise(user_msg):
        _state["praise_streak"] += 1
    else:
        _state["praise_streak"] = max(0, _state["praise_streak"] - 1)

    if _state["praise_streak"] >= 3:
        praise_adj = -0.3
    elif _state["praise_streak"] >= 2:
        praise_adj = -0.2
    elif _state["praise_streak"] >= 1:
        praise_adj = -0.1

    # 유형별 보정
    type_adj = _TYPE_ADJUST.get(query_type, 0.0)

    return praise_adj + type_adj
