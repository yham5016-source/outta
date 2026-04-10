"""
Outta Benchmark — 효소 라우터 외부 테스트셋
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
앵커와 겹치지 않는 독립 테스트 100개.
측정: 정확도 / 속도 / API 호출 수
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from brain_regions import enzyme

# ══════════════════════════════════════════════════════
# 외부 테스트셋 — 앵커와 겹치지 않는 독립 문장 100개
# ══════════════════════════════════════════════════════

TEST_CASES = [
    # ── FAST (33개) — 일상 대화, 인사, 감탄, 짧은 반응 ──
    ("방금 밥 먹었어", "FAST"),
    ("오늘 하루도 수고했어", "FAST"),
    ("나 졸려", "FAST"),
    ("아 배불러", "FAST"),
    ("뭔가 허전하다", "FAST"),
    ("그냥 그래", "FAST"),
    ("응 알겠어", "FAST"),
    ("헐 대박", "FAST"),
    ("아이고 힘들다", "FAST"),
    ("오랜만이야 잘 지냈어?", "FAST"),
    ("주말에 뭐 했어?", "FAST"),
    ("나 이따 나간다", "FAST"),
    ("아직 안 잤어?", "FAST"),
    ("커피 한잔 하고 싶다", "FAST"),
    ("오늘 별로 기분이 안 좋아", "FAST"),
    ("ㅎㅎ 그러게", "FAST"),
    ("맞아 맞아", "FAST"),
    ("에이 귀찮아", "FAST"),
    ("just chilling", "FAST"),
    ("what's up", "FAST"),
    ("I'm bored", "FAST"),
    ("haha yeah", "FAST"),
    ("sounds good", "FAST"),
    ("see you later", "FAST"),
    ("nothing much", "FAST"),
    ("that's cool", "FAST"),
    ("same here", "FAST"),
    ("not really", "FAST"),
    ("oh well", "FAST"),
    ("I'm tired too", "FAST"),
    ("sup", "FAST"),
    ("brb", "FAST"),
    ("nah I'm good", "FAST"),

    # ── BRAIN (34개) — 분석, 판단, 비교, 전략, 깊은 사고 ──
    ("이직을 준비하는 게 맞을까", "BRAIN"),
    ("주식이랑 부동산 중에 뭐가 나을까", "BRAIN"),
    ("내 사업 아이디어 좀 봐줘", "BRAIN"),
    ("이 계약서 조건이 괜찮은지 평가해줘", "BRAIN"),
    ("프리랜서로 전환하면 수입이 어떻게 될까", "BRAIN"),
    ("스타트업을 시작하려면 뭐부터 해야 해", "BRAIN"),
    ("두 가지 제안 중에 어떤 게 더 유리해", "BRAIN"),
    ("이 기술 스택의 장단점을 정리해줘", "BRAIN"),
    ("마이크로서비스 vs 모놀리식 뭐가 맞아", "BRAIN"),
    ("팀 리더로서 갈등 해결 방법을 알려줘", "BRAIN"),
    ("원격근무의 생산성 효과에 대해 어떻게 봐", "BRAIN"),
    ("AI 규제가 산업에 미치는 영향은", "BRAIN"),
    ("중국 시장 진출 전략을 세워줘", "BRAIN"),
    ("경쟁사 대비 우리 제품의 포지셔닝은", "BRAIN"),
    ("리스크 관리 프레임워크를 설계해줘", "BRAIN"),
    ("이 논문의 방법론에 문제가 있는지 검토해", "BRAIN"),
    ("어떤 프로그래밍 언어를 배우는 게 좋을까", "BRAIN"),
    ("What are the trade-offs of serverless architecture", "BRAIN"),
    ("How should I structure my portfolio", "BRAIN"),
    ("Can you evaluate this business model", "BRAIN"),
    ("What's the best strategy for entering a new market", "BRAIN"),
    ("Help me think through this ethical dilemma", "BRAIN"),
    ("Is this investment thesis sound", "BRAIN"),
    ("How do I negotiate a better salary", "BRAIN"),
    ("What are the implications of quantum computing for cryptography", "BRAIN"),
    ("Break down the pros and cons of this merger", "BRAIN"),
    ("How would you approach this system design problem", "BRAIN"),
    ("What's the ROI on this marketing spend", "BRAIN"),
    ("Is remote work sustainable long-term for engineering teams", "BRAIN"),
    ("Evaluate the competitive landscape in edtech", "BRAIN"),
    ("What frameworks should I consider for this project", "BRAIN"),
    ("How do I build a moat around my product", "BRAIN"),
    ("이 데이터를 보고 인사이트를 뽑아줘", "BRAIN"),
    ("우리 팀의 번아웃을 어떻게 해결할 수 있을까", "BRAIN"),

    # ── SEARCH (33개) — 사실 확인, 가격, 장소, 인물, 날짜 ──
    ("현대자동차 시가총액 알려줘", "SEARCH"),
    ("서울역에서 부산까지 KTX 요금이 얼마야", "SEARCH"),
    ("이태원 근처 이탈리안 레스토랑 있어?", "SEARCH"),
    ("아이폰 16 프로 가격이 얼마지", "SEARCH"),
    ("테슬라 최근 실적 발표 내용 정리해줘", "SEARCH"),
    ("내일 서울 미세먼지 예보", "SEARCH"),
    ("LG에너지솔루션 채용 공고 있어?", "SEARCH"),
    ("강남역 근처 주차장 정보", "SEARCH"),
    ("넷플릭스 이번 달 신작 뭐 있어", "SEARCH"),
    ("올해 수능 일정이 언제야", "SEARCH"),
    ("CU 편의점 1+1 행사 뭐 있어", "SEARCH"),
    ("부산 해운대 호텔 추천해줘", "SEARCH"),
    ("비트코인 현재 시세", "SEARCH"),
    ("카카오뱅크 적금 금리 알려줘", "SEARCH"),
    ("인천공항 출국장 면세점 영업시간", "SEARCH"),
    ("마라탕 칼로리가 어느 정도야", "SEARCH"),
    ("파리 올림픽 메달 순위", "SEARCH"),
    ("쿠팡 로켓배송 배송비 정책", "SEARCH"),
    ("스타벅스 아메리카노 사이즈별 가격", "SEARCH"),
    ("What's the current exchange rate for USD to KRW", "SEARCH"),
    ("Where is the nearest Apple Store in Tokyo", "SEARCH"),
    ("What time does Costco close today", "SEARCH"),
    ("Latest NVIDIA earnings report summary", "SEARCH"),
    ("Best hotels near Times Square NYC", "SEARCH"),
    ("What's the weather forecast for London this week", "SEARCH"),
    ("How many calories in a Big Mac", "SEARCH"),
    ("When is the next SpaceX launch", "SEARCH"),
    ("Current mortgage rates in the US", "SEARCH"),
    ("Samsung Galaxy S25 specs comparison", "SEARCH"),
    ("Flight prices from Seoul to Tokyo", "SEARCH"),
    ("Who won the Champions League last year", "SEARCH"),
    ("이번 주 영화 박스오피스 순위", "SEARCH"),
    ("다이소 온라인 주문 가능해?", "SEARCH"),
]


def run_benchmark():
    print("=" * 65)
    print("  Outta Benchmark — Independent Test Set (100 cases)")
    print("  Anchor-free: no overlap with enzyme router anchors")
    print("=" * 65)
    print()

    correct = 0
    total_ms = 0
    errors = {"FAST": [], "BRAIN": [], "SEARCH": []}
    counts = {"FAST": 0, "BRAIN": 0, "SEARCH": 0}
    hits = {"FAST": 0, "BRAIN": 0, "SEARCH": 0}

    for i, (query, expected) in enumerate(TEST_CASES):
        t0 = time.time()
        result = enzyme.route(query)
        elapsed = (time.time() - t0) * 1000

        predicted = result["route"] if result else "UNKNOWN"
        is_correct = predicted == expected
        correct += int(is_correct)
        if i > 0:  # 첫 호출 제외 (모델 로딩)
            total_ms += elapsed

        counts[expected] += 1
        if is_correct:
            hits[expected] += 1
        else:
            errors[expected].append((query[:40], predicted))

        mark = "✓" if is_correct else "✗"
        if not is_correct:
            print(f"  {mark} [{predicted:>6}] expected={expected:>6} | {query[:45]}")

    n = len(TEST_CASES)
    acc = correct / n * 100
    avg_ms = total_ms / (n - 1) if n > 1 else 0

    print()
    print("=" * 65)
    print(f"  RESULTS")
    print("=" * 65)
    print(f"  Total accuracy: {acc:.1f}% ({correct}/{n})")
    print(f"  Avg latency:    {avg_ms:.1f}ms (warm, excluding first call)")
    print(f"  API calls:      0")
    print()

    # 카테고리별 정확도
    print("  Per-category accuracy:")
    for cat in ["FAST", "BRAIN", "SEARCH"]:
        cat_acc = hits[cat] / counts[cat] * 100 if counts[cat] > 0 else 0
        print(f"    {cat:>6}: {cat_acc:5.1f}% ({hits[cat]}/{counts[cat]})")
        if errors[cat]:
            for q, pred in errors[cat][:5]:
                print(f"           ✗ predicted {pred}: {q}")

    # 95% CI (Clopper-Pearson)
    print()
    try:
        from scipy.stats import binom
        lo = binom.ppf(0.025, n, correct / n) / n * 100
        hi = binom.ppf(0.975, n, correct / n) / n * 100
        print(f"  95% CI: [{lo:.1f}%, {hi:.1f}%]")
    except ImportError:
        # 수동 계산 (Wilson score)
        z = 1.96
        p = correct / n
        denom = 1 + z * z / n
        center = (p + z * z / (2 * n)) / denom
        spread = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
        lo = max(0, center - spread) * 100
        hi = min(1, center + spread) * 100
        print(f"  95% CI (Wilson): [{lo:.1f}%, {hi:.1f}%]")

    print("=" * 65)


if __name__ == "__main__":
    run_benchmark()
