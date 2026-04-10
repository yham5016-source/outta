"""
측두엽 (Temporal Lobe) — 맥락/감정 분석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 표면 질문 뒤의 진짜 의도, 감정 상태, 주의사항을 분석.
     전두엽 합성 시 맥락 정보로 활용.
"""
import json

SYSTEM_PROMPT = """너는 언어 분석가야.
입력의 숨은 의미를 분석해서 JSON으로만 반환:
{
  "surface": "표면적 질문",
  "real_need": "진짜로 원하는 것",
  "emotion": "감정 상태",
  "caution": "답할 때 놓치면 안 되는 것"
}
JSON만."""


def analyze(query: str, llm_fn) -> dict:
    """맥락/감정 분석."""
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": query}]
    raw = llm_fn(msgs, max_tokens=150, temperature=0.3)
    try:
        s = raw.find("{")
        e = raw.rfind("}") + 1
        if s >= 0:
            return json.loads(raw[s:e])
    except (json.JSONDecodeError, ValueError):
        pass
    return {"surface": "", "real_need": "", "emotion": "", "caution": ""}
