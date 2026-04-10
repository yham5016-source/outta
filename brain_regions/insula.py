"""
뇌섬엽 (Insula) — 자기 감시 (할루시네이션 2차 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 크리틱이 잡지 못한 미묘한 할루시네이션을 LLM 기반으로 2차 검증.
     할루시네이션 3중 방어의 두 번째 레이어.
"""

SYSTEM_PROMPT = """너는 답변 감시자야. 아래 답변에서 문제를 찾아:
1. hallucination: 근거 없는 사실 주장
2. sycophancy: 사용자 아부
3. fake_numbers: 검증 안 된 수치
JSON으로만: {"issues": [{"type": "...", "detail": "..."}] 또는 []}"""


def monitor(query: str, answer: str, llm_fn) -> list[dict]:
    """답변의 할루시네이션/아부/수치 날조를 LLM으로 2차 검증.

    Returns:
        감지된 이슈 목록. 비어있으면 통과.
    """
    import json
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"질문: {query}\n답변: {answer}"},
    ]
    raw = llm_fn(msgs, max_tokens=200, temperature=0)
    try:
        s = raw.find("{")
        e = raw.rfind("}") + 1
        if s >= 0:
            data = json.loads(raw[s:e])
            return data.get("issues", [])
    except (json.JSONDecodeError, ValueError):
        pass
    return []
