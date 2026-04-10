"""
Demo GIF — terminal output for asciinema / screen recording.
No API keys needed. Enzyme router + critic only.
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
    slow_print("  ~750 lines | $2/month | 0 API calls for routing", 0.02)
    slow_print("=" * 55, 0.01)
    print()
    time.sleep(0.5)

    slow_print("[Enzyme Router] Loading multilingual embeddings...", 0.02)
    from brain_regions import enzyme
    time.sleep(0.3)
    slow_print("[Enzyme Router] Ready.\n", 0.02)

    queries = [
        ("Hey, how's it going?", "casual greeting"),
        ("Analyze the pros and cons of this investment", "deep analysis"),
        ("What's the current price of Tesla stock?", "factual — needs search"),
        ("Should I quit my job?", "life decision"),
        ("haha that's funny", "casual reaction"),
    ]

    for q, desc in queries:
        time.sleep(0.3)
        slow_print(f'  Q: "{q}"', 0.015)
        t0 = time.time()
        result = enzyme.route(q)
        ms = (time.time() - t0) * 1000
        route = result["route"] if result else "?"
        conf = result["confidence"] if result else 0
        slow_print(f'  > {route} ({conf}% confidence, {ms:.0f}ms, 0 API calls)', 0.015)
        slow_print(f'    [{desc}]', 0.015)
        print()

    time.sleep(0.5)
    slow_print("[Critic] Hallucination Defense Demo", 0.02)
    print()

    from brain_regions import critic

    test_responses = [
        ("Our model achieves 95% accuracy.", "fake metric"),
        ("Your insight is truly remarkable.", "sycophancy"),
        ("This approach is the most effective.", "clean — passed"),
    ]

    for resp, label in test_responses:
        time.sleep(0.3)
        filtered, violations = critic.filter_response(resp)
        if violations:
            types = [v["type"] for v in violations]
            slow_print(f'  "{resp}"', 0.015)
            slow_print(f'  > BLOCKED: {types}', 0.015)
        else:
            slow_print(f'  "{resp}"', 0.015)
            slow_print(f'  > PASSED', 0.015)
        print()

    slow_print("=" * 55, 0.01)
    slow_print("  github.com/yham5016-source/outta", 0.02)
    slow_print("=" * 55, 0.01)


if __name__ == "__main__":
    demo()
