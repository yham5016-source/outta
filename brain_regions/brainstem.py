"""
뇌간 (Brainstem) — 입력 분류 + 경로 라우팅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 모든 입력의 첫 관문. 유형/긴급도/복잡도를 판단하고
     어떤 뇌 영역을 활성화할지 결정.
모델: 경량 LLM (빠른 판단 우선)
"""
import json

SYSTEM_PROMPT = """너는 입력 분류기야. 요청이 들어오면 다음을 JSON으로 반환해:
{
  "type": "판단필요|정보요청|감정지원|창작|기타",
  "urgency": "높음|보통|낮음",
  "complexity": "단순|복합|철학적",
  "keywords": ["핵심어1", "핵심어2"],
  "route": ["amygdala", "temporal", "frontal"] 중 필요한 것들
}
JSON만 반환. 설명 없이."""


def classify(query: str, llm_fn) -> dict:
    """입력을 분류하고 라우팅 경로를 결정한다.

    Args:
        query: 사용자 입력
        llm_fn: LLM 호출 함수 (messages -> str)

    Returns:
        분류 결과 dict
    """
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    raw = llm_fn(msgs, max_tokens=200, temperature=0)
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0:
            return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError):
        pass
    return {
        "type": "기타",
        "urgency": "보통",
        "complexity": "복합",
        "route": ["amygdala", "temporal", "frontal"],
    }
