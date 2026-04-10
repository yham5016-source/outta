"""
데모 GIF용 터미널 출력 — asciinema 또는 화면 녹화용.
API 키 없이 효소 라우터 + 크리틱만 시연.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

def slow_print(text, delay=0.03):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def demo():
    print()
    slow_print("=" * 55, 0.01)
    slow_print("  Outta — Brain-inspired AI Framework", 0.02)
    slow_print("  743 lines | $2/month | 0 API calls for routing", 0.02)
    slow_print("=" * 55, 0.01)
    print()
    time.sleep(0.5)

    # 효소 라우터 데모
    slow_print("[Enzyme Router] Loading multilingual embeddings...", 0.02)
    from brain_regions import enzyme
    time.sleep(0.3)
    slow_print("[Enzyme Router] Ready.\n", 0.02)

    queries = [
        ("안녕하세요!", "casual greeting"),
        ("이 투자 전략을 분석해줘", "deep analysis"),
        ("삼성전자 주가 얼마야?", "factual — needs search"),
        ("Should I quit my job?", "life decision"),
        ("ㅋㅋㅋ 웃기다", "casual reaction"),
    ]

    for q, desc in queries:
        time.sleep(0.3)
        slow_print(f'  Q: "{q}"', 0.015)
        t0 = time.time()
        result = enzyme.route(q)
        ms = (time.time() - t0) * 1000
        route = result["route"] if result else "?"
        conf = result["confidence"] if result else 0
        slow_print(f'  → {route} ({conf}% confidence, {ms:.0f}ms, 0 API calls)', 0.015)
        slow_print(f'    [{desc}]', 0.015)
        print()

    # 크리틱 데모
    time.sleep(0.5)
    slow_print("[Critic] Hallucination Defense Demo", 0.02)
    print()

    from brain_regions import critic

    test_responses = [
        ("정확도 95%의 모델입니다.", "fake metric"),
        ("당신의 통찰은 정말 놀랍습니다.", "sycophancy"),
        ("이 방법이 가장 효과적입니다.", "clean — passed"),
    ]

    for resp, label in test_responses:
        time.sleep(0.3)
        filtered, violations = critic.filter_response(resp)
        if violations:
            types = [v["type"] for v in violations]
            slow_print(f'  "{resp}"', 0.015)
            slow_print(f'  → BLOCKED: {types}', 0.015)
        else:
            slow_print(f'  "{resp}"', 0.015)
            slow_print(f'  → PASSED', 0.015)
        print()

    slow_print("=" * 55, 0.01)
    slow_print("  github.com/ham-youngjae/outta", 0.02)
    slow_print("=" * 55, 0.01)


if __name__ == "__main__":
    demo()
