"""
Outta Pipeline v2 — 증폭형 뇌 구조 파이프라인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

흐름:
  입력 → 기저핵(캐시) → 해마(기억) → 효소(즉시분류, API 0)
    → ACC(경로 결정)
    ↓ FAST: 단순 응답 (LLM 1회)
    ↓ SEARCH: 검색 강제 (FACTUAL 게이트)
    ↓ BRAIN: 측두엽(맥락) → 전두엽(응답) → 소뇌(검증+증폭)
        → 크리틱(패턴차단) → 뇌섬엽(2차검증)
  출력 → 요소회로(정제) → 해마(저장) → 기저핵(캐시)

v1 대비 변경:
  - 편도체 이중신호 제거 → 소뇌가 검증+증폭 통합
  - 뇌간 LLM 분류 → 효소 라우터 (코사인, API 0, ~30ms)
  - FACTUAL 게이트 신설 → 고유명사 → 검색 강제
  - 전두엽 merge→select 전환
  - 크리틱 구조적 환각 2종 추가
  - 글리아 적응형 temperature
  - 요소 회로 (저장 전 정제)

비용: ~$2/월 | FAST: ~1초 | BRAIN: ~5초
"""
from concurrent.futures import ThreadPoolExecutor

from brain_regions import (
    brainstem,
    temporal,
    frontal,
    cerebellum,
    acc,
    glia,
    critic,
    insula,
    hippocampus,
    basal_ganglia,
    enzyme,
)


class OuttaPipeline:
    """증폭형 뇌 구조 파이프라인.

    3개 모델로 뇌 영역을 커버:
      - fast:   효소 폴백 시 뇌간 분류. 경량 모델 추천.
      - think:  측두엽 + 전두엽 응답. 사고력 높은 모델 추천.
      - verify: 소뇌(검증+증폭) + 뇌섬엽(감시). think과 다른 모델 추천.
    """

    def __init__(self, llm_fast, llm_think, llm_verify):
        self.llm_fast = llm_fast
        self.llm_think = llm_think
        self.llm_verify = llm_verify
        self.memory = hippocampus.SimpleMemory()

    def process(self, query: str) -> dict:
        """질문을 뇌 구조로 처리.

        Returns:
            {"answer": str, "route": str, "score": int, "violations": list}
        """
        # 0. 기저핵 — 캐시
        cached = basal_ganglia.lookup(query)
        if cached:
            return {"answer": cached, "route": "CACHE", "score": 10, "violations": []}

        # 1. 해마 — 관련 기억 주입
        mem_context = self.memory.context_string(query)
        enriched = f"{query}\n{mem_context}" if mem_context else query

        # 2. 효소 라우터 — API 0 즉시 분류
        enzyme_result = enzyme.route(query)
        if enzyme_result and enzyme_result["confidence"] >= 20:
            route = enzyme_result["route"]
            classification = {
                "type": route, "complexity": "단순" if route == "FAST" else "복합",
                "urgency": "보통", "route": [],
            }
        else:
            # 효소 실패 → 뇌간 LLM 폴백
            classification = brainstem.classify(enriched, self.llm_fast)
            route = acc.route_by_confidence(classification)

        # 3. 글리아 — 적응형 temperature
        temp_adjust = glia.update(query, classification.get("type", "기타"))

        # 4. SEARCH 경로 — FACTUAL 게이트
        if route == "SEARCH":
            return {
                "answer": "[검색 필요] 이 질문은 사실 확인이 필요합니다. 검색 결과를 기반으로 답변해야 합니다.",
                "route": "SEARCH",
                "score": 5,
                "violations": [],
                "needs_search": True,
            }

        # 5. FAST 경로 — LLM 1회
        if route == "FAST":
            try:
                answer = self.llm_think(
                    [{"role": "user", "content": enriched}],
                    max_tokens=200,
                    temperature=max(0.3, min(0.7, 0.5 + temp_adjust)),
                )
            except Exception:
                answer = "죄송합니다, 응답 생성에 실패했습니다."
            answer, violations = critic.filter_response(answer)
            purified = _urea_cycle(answer)
            if purified is not False:
                self.memory.store(query, purified or answer)
                basal_ganglia.store(query, purified or answer)
            return {"answer": purified or answer, "route": "FAST",
                    "score": 8, "violations": violations}

        # 6. BRAIN 경로 — 증폭 구조: 측두엽 → 전두엽 → 소뇌(검증+증폭)
        # 6a. 측두엽 — 맥락 분석
        try:
            context = temporal.analyze(enriched, self.llm_think)
        except Exception:
            context = {"surface": "", "real_need": "", "emotion": "", "caution": ""}

        # 6b. 전두엽 — 맥락 기반 응답 생성
        try:
            answer = frontal.respond(enriched, context, self.llm_think)
        except Exception:
            answer = "죄송합니다, 응답 생성에 실패했습니다."

        # 6c. 소뇌 — 검증 + 증폭
        try:
            verification = cerebellum.verify_and_amplify(
                query, answer, context, self.llm_verify
            )
            score = verification.get("score", 7)
            amplified = verification.get("amplified")
            if amplified:
                answer = amplified
        except Exception:
            score = 7

        # 7. 크리틱 — 패턴 차단 + 구조적 환각
        answer, violations = critic.filter_response(answer, query=query)

        # 8. 뇌섬엽 — LLM 감시 (소뇌 score < 9일 때만)
        if score < 9:
            try:
                issues = insula.monitor(query, answer, self.llm_verify)
                violations.extend(issues)
            except Exception:
                pass

        # 9. 요소 회로 — 저장 전 정제
        purified = _urea_cycle(answer)
        if purified is not False:
            self.memory.store(query, purified or answer,
                            tags=[classification.get("type", "기타")])
            if classification.get("complexity") == "단순":
                basal_ganglia.store(query, purified or answer)

        return {
            "answer": purified or answer,
            "route": route,
            "score": score,
            "violations": violations,
        }


def _urea_cycle(text: str):
    """요소 회로 — 저장 전 독소 정제.

    Returns:
        str (정화된 텍스트) | False (정화 불가, 저장 차단) | None (독소 없음)
    """
    import re
    if not text:
        return False

    # 시스템 누출
    if re.search(r'\[?(SYSTEM|ALERT|DEBUG|CRITIC)\]?', text):
        text = re.sub(r'\[?(SYSTEM|ALERT|DEBUG|CRITIC)\]?[^\n]*\n?', '', text)

    # 수치 날조 — 2개 이상 패턴 매칭 시 저장 차단
    _fake_patterns = [
        r'\d+\.\d+배',
        r'(효율|정확도|성공률)\s*\d+%',
        r'(속도|지연|레이턴시)\s*\d+ms',
        r'약\s*\d+%',
        r'(연구|논문)에\s*(따르면|의하면)',
    ]
    hits = sum(1 for p in _fake_patterns if re.search(p, text))
    if hits >= 2:
        return False  # 저장 차단

    return text.strip() if text.strip() else False
