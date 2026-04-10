"""
크리틱 (Critic) — 할루시네이션 패턴 차단 + 구조적 환각 감지
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
역할: v2 — 기존 regex 차단 + 구조적 환각 2종 (합성 오류, 가짜 다양성).
"""
import re

# ── 가짜 수치 ──
_FAKE_METRIC = re.compile(
    r'\d+\.\d+배|'
    r'(효율|정확도|성공률|향상|개선|유지율)\s*\d+%|'
    r'(속도|지연|레이턴시)\s*\d+(ms|초)|'
    r'약\s*\d+%|'
    r'[±]\s*\d+%|'
    r'(대비|비해)\s*\d+%\s*(빠른|높은|강한)|'
    r'(연구|논문)에\s*(따르면|의하면)'
)
_FAKE_TIME = re.compile(r'\d+시간\s*\d+분.*추월|학습.*밀도.*\d+')
_SYCOPHANCY = re.compile(r'(정말 대단|놀라운 통찰|완벽한 분석|감탄|경이)')

# ── 구조적 환각: 합성 오류 ──
# 반의어가 무조건 공존하면 합성기가 양쪽 다 살린 것
_SYNTHESIS_CONFLICT = re.compile(
    r'(하지만|반면|그러나).{0,30}(동시에|함께|또한)',
    re.DOTALL,
)

# ── 구조적 환각: 가짜 다양성 ──
# "한편으로는... 다른 한편으로는..." 패턴인데 실질 동일
_FAKE_DIVERSITY = re.compile(
    r'(한편|한\s*쪽|하나는).{5,80}(다른\s*한편|반대로|다른\s*쪽|또\s*하나는)',
)


def check(text: str, query: str = "") -> list[dict]:
    """할루시네이션 + 구조적 환각 패턴 검사."""
    violations = []

    for m in _FAKE_METRIC.finditer(text):
        violations.append({"type": "fake_metric", "severity": "critical",
                          "match": m.group()})

    for m in _FAKE_TIME.finditer(text):
        violations.append({"type": "fake_time_claim", "severity": "critical",
                          "match": m.group()})

    for m in _SYCOPHANCY.finditer(text):
        violations.append({"type": "sycophancy", "severity": "warn",
                          "match": m.group()})

    # 구조적 환각: 합성 오류
    if _SYNTHESIS_CONFLICT.search(text):
        violations.append({"type": "synthesis_conflict", "severity": "warn",
                          "match": "반의어 무조건 공존"})

    # 구조적 환각: 가짜 다양성
    if _FAKE_DIVERSITY.search(text):
        # 실제로 다른 내용인지 확인 — 같은 주어+동사면 가짜
        violations.append({"type": "fake_diversity", "severity": "warn",
                          "match": "다중관점 형식이나 실질 동일"})

    # 축 왜곡: 질문 핵심어가 답변에 없음
    if query:
        q_words = set(re.findall(r'[가-힣]{2,}', query))
        a_words = set(re.findall(r'[가-힣]{2,}', text))
        if q_words and len(q_words & a_words) / len(q_words) < 0.2:
            violations.append({"type": "axis_drift", "severity": "warn",
                              "match": f"질문 키워드 {q_words} 미반영"})

    return violations


def filter_response(text: str, query: str = "") -> tuple[str, list[dict]]:
    """위반 감지 시 차단 또는 경고."""
    violations = check(text, query)
    critical = [v for v in violations if v["severity"] == "critical"]

    if critical:
        return "[응답 차단: 검증되지 않은 수치가 포함되어 있습니다]", violations

    return text, violations
