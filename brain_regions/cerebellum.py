"""
소뇌 (Cerebellum) — 검증 + 증폭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 전두엽 응답의 품질 검증 + 빠진 관점 보강(증폭).
     v2: 편도체 역할 흡수 — 검증하면서 동시에 증폭.
     점수 8 미만 → 수정+증폭본 제시.
"""
import json

SYSTEM_PROMPT = """너는 검증자이자 증폭기야.
답변을 검토하고 JSON으로만 반환:
{
  "score": 1~10,
  "issues": ["문제점"] 또는 [],
  "amplified": "증폭된 수정본 또는 null"
}
검증 기준:
- 질문에 정확히 답했는가?
- 빠진 중요 관점이 있는가? 있으면 보강해서 amplified에 넣어.
- 검증 안 된 수치가 있는가? 있으면 제거.
- 사용자 아부가 있는가? 있으면 제거.

점수 8 이상이고 빠진 관점 없으면 amplified는 null.
JSON만."""


def verify_and_amplify(query: str, answer: str, context: dict,
                       llm_fn) -> dict:
    """답변 검증 + 증폭.

    Args:
        query: 원본 질문
        answer: 전두엽 응답
        context: 측두엽 맥락
        llm_fn: 검증용 LLM
    """
    review_input = f"""원래 질문: {query}
맥락 — 진짜 필요: {context.get('real_need', '')}, 주의: {context.get('caution', '')}

답변:
{answer}"""

    msgs = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": review_input}]
    raw = llm_fn(msgs, max_tokens=500, temperature=0)
    try:
        s = raw.find("{")
        e = raw.rfind("}") + 1
        if s >= 0:
            return json.loads(raw[s:e])
    except (json.JSONDecodeError, ValueError):
        pass
    return {"score": 7, "issues": [], "amplified": None}


# 하위 호환 유지
def verify(query: str, answer: str, llm_fn) -> dict:
    """v1 호환 — context 없이 검증만."""
    return verify_and_amplify(query, answer, {}, llm_fn)
