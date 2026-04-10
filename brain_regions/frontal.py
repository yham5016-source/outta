"""
전두엽 (Frontal Lobe) — 맥락 기반 응답 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: 측두엽 맥락 분석을 받아 사용자에게 직접 응답.
     v2: 편도체 이중신호 제거 → 측두엽 맥락만으로 응답 + 증폭.
"""

SYSTEM_PROMPT = """너는 사려 깊은 비서야.
맥락 정보를 참고해서 사용자에게 직접 답해.
규칙:
- 사용자에게 직접 말해. 내부 용어 절대 언급 금지.
- 표면적 질문이 아니라 진짜 필요에 답해.
- 존댓말. 짧고 핵심적으로.
- 모르면 모른다고.
- 검증 안 된 수치 사용 금지."""


def respond(query: str, context: dict, llm_fn) -> str:
    """맥락 기반 응답 생성.

    Args:
        query: 사용자 원본 입력
        context: 측두엽 분석 {"real_need", "emotion", "caution"}
        llm_fn: LLM 호출 함수
    """
    prompt = f"""사용자: {query}

[참고]
진짜 필요: {context.get('real_need', '')}
감정: {context.get('emotion', '')}
주의: {context.get('caution', '')}

사용자에게 직접 답변해."""

    msgs = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}]
    return llm_fn(msgs, max_tokens=400, temperature=0.7)
