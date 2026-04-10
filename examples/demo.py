"""
Outta Demo v2 — 증폭형 뇌 구조 실행
"""
import os
import sys
import json
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pipeline import OuttaPipeline

# ── API 키 ──
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")


def _api_call(url, key, model, messages, max_tokens=200, temperature=0.7):
    data = json.dumps({
        "model": model, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
        text = resp["choices"][0]["message"]["content"]
        # <think> 태그 제거
        if "<think>" in text:
            import re
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        return text.strip()


def llm_fast(messages, max_tokens=200, temperature=0.7):
    """Groq — 빠른 경로."""
    return _api_call(
        "https://api.groq.com/openai/v1/chat/completions",
        GROQ_KEY, "llama-3.3-70b-versatile",
        messages, max_tokens, temperature,
    )


def llm_think(messages, max_tokens=400, temperature=0.7):
    """DeepSeek — 사고 경로."""
    return _api_call(
        "https://api.deepseek.com/chat/completions",
        DEEPSEEK_KEY, "deepseek-chat",
        messages, max_tokens, temperature,
    )


def main():
    if not GROQ_KEY or not DEEPSEEK_KEY:
        print("GROQ_API_KEY, DEEPSEEK_API_KEY 환경변수를 설정해주세요.")
        return

    pipeline = OuttaPipeline(
        llm_fast=llm_fast,
        llm_think=llm_think,
        llm_verify=llm_think,  # 다른 모델 쓰면 교차검증 효과↑
    )

    queries = [
        "친한 친구가 나한테 거짓말을 했어. 어떻게 해야 해?",
        "직장을 그만둬야 할지 모르겠어.",
        "오늘 너무 힘들었어.",
        "삼성전자 주가 어때?",  # FACTUAL → SEARCH
    ]

    for q in queries:
        print(f"\n{'=' * 60}")
        print(f"  Q: {q}")
        result = pipeline.process(q)
        print(f"  경로: {result['route']} | 점수: {result['score']}")
        if result["violations"]:
            print(f"  위반: {[v['type'] for v in result['violations']]}")
        print(f"\n  A: {result['answer']}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
